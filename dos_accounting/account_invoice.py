# -*- coding: utf-8 -*-
##############################################################################
#
#    Databit Solusi Indonesia, PT
#    Copyright (C) 2014 DatabitL (<http://www.databit.co.id>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import itertools
from lxml import etree
import time
from openerp.osv import fields, osv
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp
from openerp.addons.dos_amount2text_idr import amount_to_text_id

class account_invoice(models.Model):
    _inherit    = "account.invoice"
    
    def _paid_date(self, cr, uid, ids, paid_date, arg, context=None):
        res = {}
        for inv in self.browse(cr, uid, ids, context):
            if inv.payment_ids:
                res[inv.id] = inv.payment_ids[0].date            
        return res
    
    def _nomor_faktur_company(self, cr, uid, ids, nomorfaktur, arg, context=None):
        res = {}
        for nomor in self.browse(cr, uid, ids, context):
            if nomor.partner_id.kode_transaksi:# and nomor.partner_id.kode_status != False:
                res[nomor.id] = "%s.%s" % (nomor.partner_id.kode_transaksi,nomor.nomor_faktur_id and nomor.nomor_faktur_id.name)
            else:
                res[nomor.id] = ""
        return res
    
    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount', 'add_disc_type', 'amount_add_disc')
    def _compute_amount(self):
        val = val1 = net_untaxed = discount_sum = disc_amt = 0.0
        for line in self.invoice_line:                
            # Discount Line
            disc_amt += line.disc_amount
            discount = line.discount * line.price_unit / 100
            net_price_unit = line.price_unit - discount - line.disc_amount
            net_untaxed += (net_price_unit * line.quantity)
            discount_sum += (discount * line.quantity) + disc_amt           
            val1 += line.price_subtotal
        #self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line)
        #self.amount_tax = sum(line.amount for line in self.tax_line)        
        #self.gross_total = sum(line.price_unit * line.quantity for line in self.invoice_line)
        self.gross_total = val1+discount_sum
        #==========================discount global==========================
        if self.amount_add_disc:
            if self.add_disc_type == 'percent':
                discount_sum = discount_sum + (self.gross_total * (self.amount_add_disc / 100.0))
                discount_add = (self.gross_total * (self.amount_add_disc / 100.0))
            else:
                discount_sum = discount_sum + self.amount_add_disc
                discount_add = self.amount_add_disc
            net_untaxed = self.gross_total - discount_sum
            self.discount_additional = discount_add
        #===================================================================
        self.discount_total = discount_sum#sum(line.quantity* (line.price_unit * (line.discount or 0.0)/100) for line in self.invoice_line)
        self.amount_untaxed = net_untaxed
        #self.amount_downpayment = self.payment_request_dp_id.amount_total or 0.0
        self.amount_tax = sum(line.amount for line in self.tax_line)
        self.amount_total = self.amount_untaxed + self.amount_tax# - self.amount_downpayment
    #####################
    
    gross_total = fields.Float(string='Gross Total', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount' )
    discount_total = fields.Float(string='Total Discount', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount')
    discount_additional = fields.Float(string='Total Additional', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount')

    add_disc_type = fields.Selection([
            ('fix','Fix Amount'),
            ('percent','Percentage (%)'),
        ], string='Type Discount', required=False, readonly=True, states={'draft': [('readonly', False)]})
    amount_add_disc = fields.Float(string='Additional Discount', required=False, readonly=True, states={'draft': [('readonly', False)]},
        digits= dp.get_precision('Account'))
    
    amount_total = fields.Float(string='Total', digits=dp.get_precision('Account'),
            store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    
#     ap_tax_account_id = fields.Many2one('account.account', string='Tax Payable',
#         required=False, readonly=True, states={'draft': [('readonly', False)]},
#         help="The partner account used for this invoice.")
    
    ###Prepayment Downpayment###
    #payment_request_dp_id   = fields.Many2one('purchase.request',string="NOI DP")
    #amount_downpayment      = fields.Float(string='Downpayment', digits=dp.get_precision('Account'),  store=True, readonly=True, compute='_compute_amount')
    ###
    reference_invoice_id = fields.Many2one('account.invoice', string='Invoice Reference',)
    ###
    phone = fields.Char(string='Phone', related='partner_id.mobile', readonly=True)
    nomor_faktur_id = fields.Many2one('nomor.faktur.pajak', string='Nomor Faktur Pajak', change_default=True,
        required=False, readonly=True, states={'draft': [('readonly', False)]})
    kode_transaksi = fields.Selection([
            ('010','010.'),('020','020.'),('030','030.'),('080','080.')
        ], string='Kode Faktur', required=False, readonly=True, states={'draft': [('readonly', False)]})
    nomor_faktur_company = fields.Char(string='Nomor Faktur', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_nomor_faktur_company')
    npwp_no = fields.Char(string='NPWP', readonly=True, states={'draft': [('readonly', False)]})
    paid_date = fields.Date(string='Paid Date', compute='_paid_date', readonly=True)    
    
    @api.multi
    def onchange_partner_npwp(self, npwp=False):
        return {'value': {}}
    
    @api.multi
    def onchange_partner_id(self, type, partner_id, date_invoice=False,
            payment_term=False, partner_bank_id=False, company_id=False):
        account_id = False
        payment_term_id = False
        fiscal_position = False
        bank_id = False
        faktur = False
        npwp = False
        npwp_no = False

        if partner_id:
            p = self.env['res.partner'].browse(partner_id)
            rec_account = p.property_account_receivable
            pay_account = p.property_account_payable
            if company_id:
                if p.property_account_receivable.company_id and \
                        p.property_account_receivable.company_id.id != company_id and \
                        p.property_account_payable.company_id and \
                        p.property_account_payable.company_id.id != company_id:
                    prop = self.env['ir.property']
                    rec_dom = [('name', '=', 'property_account_receivable'), ('company_id', '=', company_id)]
                    pay_dom = [('name', '=', 'property_account_payable'), ('company_id', '=', company_id)]
                    res_dom = [('res_id', '=', 'res.partner,%s' % partner_id)]
                    rec_prop = prop.search(rec_dom + res_dom) or prop.search(rec_dom)
                    pay_prop = prop.search(pay_dom + res_dom) or prop.search(pay_dom)
                    rec_account = rec_prop.get_by_record(rec_prop)
                    pay_account = pay_prop.get_by_record(pay_prop)
                    if not rec_account and not pay_account:
                        action = self.env.ref('account.action_account_config')
                        msg = _('Cannot find a chart of accounts for this company, You should configure it. \nPlease go to Account Configuration.')
                        raise RedirectWarning(msg, action.id, _('Go to the configuration panel'))

            if type in ('out_invoice', 'out_refund'):
                account_id = rec_account.id
                payment_term_id = p.property_payment_term.id
            else:
                account_id = pay_account.id
                payment_term_id = p.property_supplier_payment_term.id
            fiscal_position = p.property_account_position.id
            bank_id = p.bank_ids and p.bank_ids[0].id or False
            npwp = p.npwp or False 
            #faktur = p.kode_transaksi and "%s" % (p.kode_transaksi)
            
        result = {'value': {
            'account_id': account_id,
            'payment_term': payment_term_id,
            'fiscal_position': fiscal_position,
            #'kode_transaksi': faktur or '',
            'npwp_no' : npwp,
        }}

        if type in ('in_invoice', 'in_refund'):
            result['value']['partner_bank_id'] = bank_id

        if payment_term != payment_term_id:
            if payment_term_id:
                to_update = self.onchange_payment_term_date_invoice(payment_term_id, date_invoice)
                result['value'].update(to_update.get('value', {}))
            else:
                result['value']['date_due'] = False

        if partner_bank_id != bank_id:
            to_update = self.onchange_partner_bank(bank_id)
            result['value'].update(to_update.get('value', {}))
        
        if npwp_no != npwp:
            to_update = self.onchange_partner_npwp(npwp)
            result['value'].update(to_update.get('value', {}))

        return result
    
    @api.multi
    def compute_invoice_totals(self, company_currency, ref, invoice_move_lines):
        total = 0
        total_currency = 0
        amount_tax_total =0.0
        amount_currency_tax_total =0.0
        for line in invoice_move_lines:
            if self.currency_id != company_currency:
                if line['type'] == 'tax':
                    try:
                        amount_tax = line['tax_amount']
                    except:
                        amount_tax = False
                    
                    currency = self.currency_id.with_context(date=self.date_invoice or fields.Date.context_today(self))
                    line['currency_id'] = currency.id
                    line['amount_currency'] = line['price']
                    line['price'] = amount_tax or currency.compute_tax(line['price'], company_currency)
                    amount_tax_total += line['price'] 
                    amount_currency_tax_total += line['amount_currency']
                elif line['type'] == 'tax_total':
                    if amount_tax_total > 0.0:
                        line['amount_currency'] = -1 * amount_currency_tax_total
                        line['price'] = -1 * amount_tax_total or currency.compute_tax(line['price'], company_currency)
                    else:
                        line['price'] = 0.0
                        line['amount_currency'] = 0.0
                else:
                    currency = self.currency_id.with_context(date=self.date_invoice or fields.Date.context_today(self))
                    line['currency_id'] = currency.id
                    line['amount_currency'] = line['price']
                    line['price'] = currency.compute(line['price'], company_currency)
            else:
                line['currency_id'] = False
                line['amount_currency'] = False
            line['ref'] = ref
            if self.type in ('out_invoice','in_refund'):
                total += line['price']
                total_currency += line['amount_currency'] or line['price']
                line['price'] = - line['price']
            else:
                total -= line['price']
                total_currency -= line['amount_currency'] or line['price']
        return total, total_currency, invoice_move_lines
    
    def invoice_reverse(self, cr, uid, ids, context=None):
        move_obj        = self.pool.get('account.move')
        move_line_obj   = self.pool.get('account.move.line')
        period_obj      = self.pool.get('account.period')
        
        rec_list_ids = []
        for val in self.browse(cr, uid, ids, context=None):
            if val.payment_ids:
                raise except_orm(_('Error!'), _('You Can not Reverse Invoice with Partial Payments'))
            now         = time.strftime('%Y-%m-%d')
            period_id   = period_obj.find(cr, uid, now, context=None)[0]
            move_vals = {
                'name'      : val.number + " Reverse" or "/",
                'journal_id': val.journal_id.id,
                'narration' : "Reverse Journal" + val.number or "/",
                'date'      : val.date_invoice,
                'ref'       : "Reverse Journal" + val.number or "/",
                'period_id' : period_id,
            }
            move_id = move_obj.create(cr, uid, move_vals, context=None)
            
            for move_line in val.move_id.line_id:
                move_line_vals = {
                    'name'                  : move_line.name or '/',
                    'debit'                 : move_line.credit,
                    'credit'                : move_line.debit,
                    'account_id'            : move_line.account_id.id,
                    'move_id'               : move_id,
                    'journal_id'            : move_line.journal_id.id,
                    'period_id'             : move_line.period_id.id,
                    'analytic_account_id'   : move_line.analytic_account_id.id,
                    'partner_id'            : move_line.partner_id.id,
                    'currency_id'           : move_line.currency_id.id,
                    'amount_currency'       : -move_line.amount_currency,
                    'date'                  : move_line.date,
                            }
                new_move_line_id = move_line_obj.create(cr, uid, move_line_vals, context=None)
                if move_line.account_id.type == 'payable' and move_line.account_id.reconcile == True:
                    rec_list_ids.append(move_line.id)
                    rec_list_ids.append(new_move_line_id)
            if rec_list_ids:
                cr.execute("select account_id from account_move_line where id in %s group by account_id", (tuple(rec_list_ids),))
                account_list = map(lambda x: x[0], cr.fetchall())
            rec_data = move_line_obj.browse(cr,uid,rec_list_ids)
            acc_ids = [m.account_id.id for m in rec_data]            
            ######################
            d = {}
            i=0
            m_ids = []
            old_acc_id = False
            for acc_id in acc_ids:
                a = rec_list_ids[i]
                if old_acc_id == acc_id:
                    m_ids.append(rec_list_ids[i])
                else:
                    old_acc_id = acc_id
                    m_ids = []
                    m_ids.append(rec_list_ids[i])
                d[acc_id] = m_ids
                i+=1
            ######################            
            for key in d.keys():
                if len(d[key]) >= 2:
                    reconcile = move_line_obj.reconcile(cr, uid, d[key], 'auto', False, False, False, context=None)
        return True
    
    def gainloss_create(self, amount_src, amount_dest, account_counter, gainloss_account):
        line_gainloss_gl = []
        gainloss_account_default = self.company_id.income_currency_exchange_account_id.id
        diff_amount = amount_dest - amount_src
        
        if not gainloss_account:
            gainloss_account = gainloss_account_default
        move_line_d = {
            'name'      : "Gain Loss" or '/',
            'debit'     : abs(diff_amount),
            'credit'    : 0.0,
            'account_id': diff_amount > 0.0 and account_counter or gainloss_account,
            'journal_id': self.journal_id.id,
            'date'      : self.date_invoice,
        }
        move_line_c = {
            'name'      : "Gain Loss" or '/',
            'debit'     : 0.0,
            'credit'    : abs(diff_amount),
            'account_id': diff_amount > 0.0 and gainloss_account or account_counter,
            'journal_id': self.journal_id.id,
            'date'      : self.date_invoice,
        }        
        line_gainloss_gl.append(move_line_d)
        line_gainloss_gl.append(move_line_c)        
        return line_gainloss_gl
    
    @api.multi
    def compute_discount_additional(self, company_currency, discount_additional):
        total = 0
        total_currency = 0
        if self.currency_id != company_currency:
            currency = self.currency_id.with_context(date=self.date_invoice or fields.Date.context_today(self))
            currency_id = currency.id
            amount_currency = discount_additional
            price = currency.compute(discount_additional, company_currency)
        else:
            currency_id = False
            amount_currency = False
        total = price#line['price']
        total_currency = amount_currency or price   
#         if self.type in ('out_invoice','in_refund'):
#             total = price#line['price']
#             total_currency = amount_currency or price#line['amount_currency'] or line['price']
#             #price = amount_currency#line['price']
#         else:
#             total = -price#line['price']
#             total_currency = -amount_currency or -price#line['amount_currency'] or line['price']
        return total, total_currency, currency_id#, invoice_move_lines
    
    @api.multi
    def action_move_create(self):
        """ Creates invoice related analytics and financial move lines """
        account_invoice_tax = self.env['account.invoice.tax']
        account_move = self.env['account.move']

        for inv in self:
            if not inv.journal_id.sequence_id:
                raise except_orm(_('Error!'), _('Please define sequence on the journal related to this invoice.'))
            if not inv.invoice_line:
                raise except_orm(_('No Invoice Lines!'), _('Please create some invoice lines.'))
            if inv.move_id:
                continue

            ctx = dict(self._context, lang=inv.partner_id.lang)

            if not inv.date_invoice:
                inv.with_context(ctx).write({'date_invoice': fields.Date.context_today(self)})
            date_invoice = inv.date_invoice

            company_currency = inv.company_id.currency_id
            # create the analytical lines, one move line per invoice line
            iml = inv._get_analytic_lines()
            # check if taxes are all computed
            compute_taxes = account_invoice_tax.compute(inv.with_context(lang=inv.partner_id.lang))
            inv.check_tax_lines(compute_taxes)

            # I disabled the check_total feature
            if self.env['res.users'].has_group('account.group_supplier_inv_check_total'):
                if inv.type in ('in_invoice', 'in_refund') and abs(inv.check_total - inv.amount_total) >= (inv.currency_id.rounding / 2.0):
                    raise except_orm(_('Bad Total!'), _('Please verify the price of the invoice!\nThe encoded total does not match the computed total.'))

            if inv.payment_term:
                total_fixed = total_percent = 0
                for line in inv.payment_term.line_ids:
                    if line.value == 'fixed':
                        total_fixed += line.value_amount
                    if line.value == 'procent':
                        total_percent += line.value_amount
                total_fixed = (total_fixed * 100) / (inv.amount_total or 1.0)
                if (total_fixed + total_percent) > 100:
                    raise except_orm(_('Error!'), _("Cannot create the invoice.\nThe related payment term is probably misconfigured as it gives a computed amount greater than the total invoiced amount. In order to avoid rounding issues, the latest line of your payment term must be of type 'balance'."))

            # one move line per tax line
            iml += account_invoice_tax.move_line_get(inv.id)

            if inv.type in ('in_invoice', 'in_refund'):
                ref = inv.reference
            else:
                ref = inv.number
                
            diff_currency = inv.currency_id != company_currency
            # create one move line for the total and possibly adjust the other lines amount
            total, total_currency, iml = inv.with_context(ctx).compute_invoice_totals(company_currency, ref, iml)

            name = inv.supplier_invoice_number or inv.name or '/'
            totlines = []
            #===============================================================
            if inv.discount_additional > 0:
                if inv.type in ('out_invoice', 'out_refund'):
                    discount_view = inv.discount_additional
                    acc_disc_id = inv.company_id.sale_account_additional_discount_id and inv.company_id.sale_account_additional_discount_id.id
                    discount_add, discount_currency, currency_id = inv.with_context(ctx).compute_discount_additional(company_currency, discount_view)
                    if not inv.company_id.sale_account_additional_discount_id:
                        raise osv.except_osv(_('Account Discount'),
                           _('Please insert Account Discount for this Customer Invoice'))
                elif inv.type in ('in_invoice', 'in_refund'):
                    discount_view = -inv.discount_additional
                    acc_disc_id = inv.company_id.purchase_account_additional_discount_id and inv.company_id.purchase_account_additional_discount_id.id
                    #discount_add = -inv.discount_additional
                    discount_add, discount_currency, currency_id = inv.with_context(ctx).compute_discount_additional(company_currency, discount_view)                    
                    if not inv.company_id.purchase_account_additional_discount_id:
                        raise osv.except_osv(_('Account Discount'),
                           _('Please insert Account Discount for this Supplier Invoice'))
                iml.append({
                    'type': 'dest',
                    'name': 'Additional Discount',
                    'price': discount_add,
                    'account_id': acc_disc_id,
                    'date_maturity': inv.date_due or False,
                    'amount_currency': diff_currency \
                            and discount_currency or False,
                    'currency_id': diff_currency \
                            and currency_id or False,
                    'ref': ref
                })
            #===============================================================
            if inv.payment_term:
                totlines = inv.with_context(ctx).payment_term.compute(total, date_invoice)[0]
            if totlines:
                #===============================================================
                split_disc = tdisc = 0.0
                for i, t in enumerate(totlines):
                    split_disc+=1
                if inv.discount_additional > 0:
                    tdisc = discount_add / split_disc           
                #===============================================================         
                res_amount_currency = total_currency - tdisc
                ctx['date'] = date_invoice
                for i, t in enumerate(totlines):
                    if inv.currency_id != company_currency:
                        amount_currency = company_currency.with_context(ctx).compute(t[1]-tdisc, inv.currency_id)
                    else:
                        amount_currency = False

                    # last line: add the diff
                    res_amount_currency -= amount_currency or 0
                    if i + 1 == len(totlines):
                        amount_currency += res_amount_currency

                    iml.append({
                        'type': 'dest',
                        'name': name,
                        'price': t[1]-tdisc,
                        'account_id': inv.account_id.id,
                        'date_maturity': t[0],
                        'amount_currency': diff_currency and amount_currency,
                        'currency_id': diff_currency and inv.currency_id.id,
                        'ref': ref,
                    })
            else:
                if inv.discount_additional > 0:
                    total = total - discount_add
                    total_currency = total_currency - discount_view
                else:
                    total = total 
                    #total_currency = total_currency
                iml.append({
                    'type': 'dest',
                    'name': name,
                    'price': total,
                    'account_id': inv.account_id.id,
                    'date_maturity': inv.date_due,
                    'amount_currency': diff_currency and total_currency,
                    'currency_id': diff_currency and inv.currency_id.id,
                    'ref': ref
                })
            #print "-----------",iml
            #===============================================================
            date = date_invoice

            part = self.env['res.partner']._find_accounting_partner(inv.partner_id)

            line = [(0, 0, self.line_get_convert(l, part.id, date)) for l in iml]
            line = inv.group_lines(iml, line)

            journal = inv.journal_id.with_context(ctx)
            if journal.centralisation:
                raise except_orm(_('User Error!'),
                        _('You cannot create an invoice on a centralized journal. Uncheck the centralized counterpart box in the related journal from the configuration menu.'))

            line = inv.finalize_invoice_move_lines(line)

            move_vals = {
                'ref': inv.reference or inv.name,
                'line_id': line,
                'journal_id': journal.id,
                'date': inv.date_invoice,
                'narration': inv.comment,
                'company_id': inv.company_id.id,
            }
            ctx['company_id'] = inv.company_id.id
            period = inv.period_id
            if not period:
                period = period.with_context(ctx).find(date_invoice)[:1]
            if period:
                move_vals['period_id'] = period.id
                for i in line:
                    i[2]['period_id'] = period.id

            ctx['invoice'] = inv
            move = account_move.with_context(ctx).create(move_vals)
            # make the invoice point to that move
            vals = {
                'move_id': move.id,
                'period_id': period.id,
                'move_name': move.name,
            }
            inv.with_context(ctx).write(vals)
            # Pass invoice in context in method post: used if you want to get the same
            # account move reference when creating the same invoice after a cancelled one:
            move.post()
            
#             == coba ah testing create faktur pajak ==
            
            obj_no_faktur = self.env['nomor.faktur.pajak'].browse(inv.nomor_faktur_id.id)
            #invoice = self.env['account.invoice'].browse(context['default_res_id'])
           
            if inv.nomor_faktur_id and inv.type == 'out_invoice':
                obj_no_faktur.write({
                    'invoice_id': inv.id, 
                    'partner_id': inv.partner_id.id, 
                    'dpp': inv.amount_untaxed, 
                    'tax_amount': inv.amount_tax,
                    'date_used': inv.date_invoice,
                    'company_id': inv.company_id.id,
                     'status': '1', 
                 })
            elif inv.nomor_faktur_id and inv.type == 'in_invoice':                
                if inv.nomor_faktur_id[3] == "." and inv.nomor_faktur_id[6] == '.':
                    if len(str(inv.nomor_faktur_id).split('.')[2]) > 8:
                        raise osv.except_osv(_('Wrong Faktur Number'), _('Nomor Urut max 8 Digit'))                
                    vals = {
                        'company_id'        : inv.company_id.id,
                        'nomor_perusahaan'  : str(inv.vat_supplier).split('.')[0],
                        'tahun_penerbit'    : str(inv.vat_supplier).split('.')[1], 
                        'nomor_urut'        : str(inv.vat_supplier).split('.')[2],
                        'invoice_id'        : inv.id,
                        'partner_id'        : inv.partner_id.id,
                        'dpp'               : inv.amount_untaxed,
                        'tax_amount'        : inv.amount_tax,
                        'date_used'         : inv.date_invoice,
                        'currency_id'       : inv.currency_id.id,
                        'type'              : 'in',
                        'status'            : '1',
                    }
                else:
                    raise osv.except_osv(_('Faktur Number Wrong'), _('Please input Faktur Number use SEPARATOR "."(DOT).'))
                obj_no_faktur.create(vals)
            
        self._log_event()
        return True
#     @api.multi
#     def action_move_create(self):
#         print "action_move_create--------------------->>"
#         """ Creates invoice related analytics and financial move lines """
#         account_invoice_tax = self.env['account.invoice.tax']
#         account_move = self.env['account.move']
#         line_sett_gl = []
#         account_move_line_obj = self.env['account.move.line']
# 
#         for inv in self:
#             if not inv.journal_id.sequence_id:
#                 raise except_orm(_('Error!'), _('Please define sequence on the journal related to this invoice.'))
#             if not inv.invoice_line:
#                 raise except_orm(_('No Invoice Lines!'), _('Please create some invoice lines.'))
#             if inv.move_id:
#                 continue
# 
#             ctx = dict(self._context, lang=inv.partner_id.lang)
# 
#             if not inv.date_invoice:
#                 inv.with_context(ctx).write({'date_invoice': fields.Date.context_today(self)})
#             date_invoice = inv.date_invoice
# 
#             company_currency = inv.company_id.currency_id
#             # create the analytical lines, one move line per invoice line
#             iml = inv._get_analytic_lines()
#             # check if taxes are all computed
#             compute_taxes = account_invoice_tax.compute(inv)
#             inv.check_tax_lines(compute_taxes)
# 
#             # I disabled the check_total feature
#             if self.env['res.users'].has_group('account.group_supplier_inv_check_total'):
#                 if inv.type in ('in_invoice', 'in_refund') and abs(inv.check_total - inv.amount_total) >= (inv.currency_id.rounding / 2.0):
#                     raise except_orm(_('Bad Total!'), _('Please verify the price of the invoice!\nThe encoded total does not match the computed total.'))
# 
#             if inv.payment_term:
#                 total_fixed = total_percent = 0
#                 for line in inv.payment_term.line_ids:
#                     if line.value == 'fixed':
#                         total_fixed += line.value_amount
#                     if line.value == 'procent':
#                         total_percent += line.value_amount
#                 total_fixed = (total_fixed * 100) / (inv.amount_total or 1.0)
#                 if (total_fixed + total_percent) > 100:
#                     raise except_orm(_('Error!'), _("Cannot create the invoice.\nThe related payment term is probably misconfigured as it gives a computed amount greater than the total invoiced amount. In order to avoid rounding issues, the latest line of your payment term must be of type 'balance'."))
# 
#             # one move line per tax line
#             iml += account_invoice_tax.move_line_get(inv.id)
#             if inv.type in ('in_invoice', 'in_refund'):
#                 ref = inv.reference
#             else:
#                 ref = inv.number
#             ##########Calculate Total AP Vendor & AP Tax###########
#             diff_currency = inv.currency_id != company_currency
#             total_ap_cur_tax    = 0.0
#             total_ap_tax        = 0.0
#             total_disc_add    = 0.0
#             ####Gain Loss####
#             #currency_obj    = self.pool.get('res.currency')
#             #tax_obj         = self.pool.get('account.tax')
#             line_principle_gl = []
#             line_tax_gl       = []
#             line_dp_gl        = []            
# #             #####Downpayment######
# #             if inv.payment_request_dp_id:
# #                 iml.append({
# #                         'type': 'src',
# #                         'name': "Downpayment",
# #                         'price': -inv.amount_downpayment,
# #                         'account_id': inv.payment_request_dp_id.order_line[0].product_id.property_account_expense.id,
# #                         'date_maturity': inv.date_due,
# #                         'amount_currency': diff_currency and total_ap_cur_tax,
# #                         'currency_id': diff_currency and inv.currency_id.id,
# #                         'ref': ref,
# #                 })
# #                 #print "inv.payment_request_dp_id.id????????????????????", inv.payment_request_dp_id.id
# #                 dp_env = self.env['purchase.request'].browse(inv.payment_request_dp_id.id)
# #                 dp_env.write({'prepayment_status' : True})
# #                 if inv.payment_request_dp_id.purchase_id:
# #                     po_env = self.env['purchase.order'].browse(inv.payment_request_dp_id.purchase_id.id)
# #                     po_env.write({'dp_status' : 'used'})
#                     
#             if inv.currency_id <> company_currency:
#                 ######Gain Loss Downpayment######
#                 if inv.payment_request_dp_id:
#                     currency = self.currency_id.with_context(date=inv.payment_request_dp_id.invoice_ids[0].date_invoice)
#                     dp_original_amount_convert = currency.compute(inv.amount_downpayment, company_currency)
#                     
#                     currency = self.currency_id.with_context(date=self.date_invoice)
#                     inv_original_amount_convert = currency.compute(inv.amount_downpayment, company_currency)
#                     
#                     diff_downpayment_gl = inv_original_amount_convert - dp_original_amount_convert
#                     
#                     if diff_downpayment_gl <> 0.0:
#                         if diff_downpayment_gl > 0.0:
#                             account_gl_downpayment_d = inv.company_id.expense_currency_exchange_account_id.id#427
#                             account_gl_downpayment_c = inv.payment_request_dp_id.order_line[0].product_id.property_account_expense.id
#                         else:
#                             account_gl_downpayment_d = inv.payment_request_dp_id.order_line[0].product_id.property_account_expense.id
#                             account_gl_downpayment_c = inv.company_id.income_currency_exchange_account_id.id#427
#                         
#                         
#                         move_line_d = {
#                             'name'      : "Gain Loss Downpayment" or '/',
#                             'debit'     : abs(diff_downpayment_gl),
#                             'credit'    : 0.0,
#                             'account_id': account_gl_downpayment_d,
#                             'journal_id': inv.journal_id.id,
#                             'date'      : inv.date_invoice,
#                         }
#                         move_line_c = {
#                             'name'      : "Gain Loss Downpayment" or '/',
#                             'debit'     : 0.0,
#                             'credit'    : abs(diff_downpayment_gl),
#                             'account_id': account_gl_downpayment_c,
#                             'journal_id': inv.journal_id.id,
#                             'date'      : inv.date_invoice,
#                         }
#                         print "qqqqqqqqqqqqq",move_line_d
#                         print "eeeeeeeeeeeee",move_line_c
#                         line_dp_gl.append(move_line_d)
#                         line_dp_gl.append(move_line_c)
#                 ###############Gain Loss Settlement#################
# #                 if inv.settlement_id:
# #                     currency = self.currency_id.with_context(date=inv.settlement_id.cash_advance_id.invoice_id.date_invoice)
# #                     adv_original_amount_convert = currency.compute(inv.settlement_id.reserved, company_currency)
# #                     
# #                     currency = self.currency_id.with_context(date=self.date_invoice)
# #                     inv_original_amount_convert = currency.compute(inv.settlement_id.reserved, company_currency)
# #                     
# #                     diff_advance_gl = inv_original_amount_convert - adv_original_amount_convert
# #                     
# #                     line_sett_gl = self.gainloss_create(adv_original_amount_convert, inv_original_amount_convert, inv.settlement_id.account_advance_id.id, False)
#                 for l_gl in inv.invoice_line:
#                     ####Cek hanya untuk invoice from picking####
#                     if l_gl.stock_move_id:
#                         #####Selisih Kurs Principle########
#                         tax_of_move         = l_gl.stock_move_id.taxes_id
#                         tax_unit_amount     = l_gl.stock_move_id.tax_unit
#                         ###Cek Gain Loss Per Unit###
#                         inv_original_amount = l_gl.price_unit * 1#l_gl.quantity                        
#                         move_unit_amount    = l_gl.stock_move_id.price_unit                          
#                         currency = self.currency_id.with_context(date=self.date_invoice)
#                         inv_original_amount_convert = currency.compute(inv_original_amount, company_currency)                        
#                         ###Gain Loss dikali jumlah Quantity yg diinvoicekan###
#                         diff_principle_gl = (inv_original_amount_convert - move_unit_amount) * l_gl.quantity                        
#                         #print "Selisih Kurs Principle------>>", diff_principle_gl                        
#                         if diff_principle_gl <> 0.0:
#                             if diff_principle_gl > 0.0:
#                                 account_gl_principle_d = inv.company_id.expense_currency_exchange_account_id.id#427
#                                 account_gl_principle_c = l_gl.account_id.id
#                             else:
#                                 account_gl_principle_d = l_gl.account_id.id
#                                 account_gl_principle_c = inv.company_id.income_currency_exchange_account_id.id#427                           
#                             move_line_d = {
#                                 'name'      : "Gain Loss Principle" or '/',
#                                 'debit'     : abs(diff_principle_gl),
#                                 'credit'    : 0.0,
#                                 'account_id': account_gl_principle_d,
#                                 'journal_id': inv.journal_id.id,
#                                 'date'      : inv.date_invoice,
#                             }
#                             move_line_c = {
#                                 'name'      : "Gain Loss Principle" or '/',
#                                 'debit'     : 0.0,
#                                 'credit'    : abs(diff_principle_gl),
#                                 'account_id': account_gl_principle_c,
#                                 'journal_id': inv.journal_id.id,
#                                 'date'      : inv.date_invoice,
#                             }
#                             line_principle_gl.append(move_line_d)
#                             line_principle_gl.append(move_line_c)
#                         #####Selisih Kurs Taxes########
#                         for tax_l_gl in list(l_gl.invoice_line_tax_id):
#                             #original_tax_amount = tax_obj.compute([tax_of_move], l_gl.price_unit, l_gl.quantity, None, None)
#                             ###Gain Loss dikali jumlah Quantity yg diinvoicekan###
#                             inv_original_tax_amount = tax_of_move.amount * (l_gl.price_unit * 1)#l_gl.quantity)
#                             inv_original_tax_amount_convert = currency.compute_tax(inv_original_tax_amount, company_currency)
#                             ###Cek Tax di Invoice & Picking###                            
#                             if tax_l_gl.id == tax_of_move.id:
#                                 diff_tax_gl = (inv_original_tax_amount_convert - tax_unit_amount) * l_gl.quantity
#                                 if diff_tax_gl > 0.0:
#                                     account_gl_tax_d = inv.company_id.expense_currency_exchange_account_id.id
#                                     account_gl_tax_c = tax_l_gl.account_collected_id.id or l_gl.account_id.id
#                                 else:
#                                     account_gl_tax_d = tax_l_gl.account_collected_id.id or l_gl.account_id.id
#                                     account_gl_tax_c = inv.company_id.income_currency_exchange_account_id.id                                
#                                 if diff_tax_gl <> 0.0:
#                                     move_line_d = {
#                                         'name'      : "Gain Loss Tax" or '/',
#                                         'debit'     : abs(diff_tax_gl),
#                                         'credit'    : 0.0,
#                                         'account_id': account_gl_tax_d,
#                                         'journal_id': inv.journal_id.id,
#                                         'date'      : inv.date_invoice,
#                                     }                                    
#                                     move_line_c = {
#                                         'name'      : "Gain Loss Tax" or '/',
#                                         'debit'     : 0.0,
#                                         'credit'    : abs(diff_tax_gl),
#                                         'account_id': account_gl_tax_c,
#                                         'journal_id': inv.journal_id.id,
#                                         'date'      : inv.date_invoice,
#                                     }                                    
#                                     line_tax_gl.append(move_line_d)
#                                     line_tax_gl.append(move_line_c)
#             for taxl in iml:                
#                 ####Cek Gain loss####
#                 if taxl['type'] == 'tax':
#                     total_ap_tax        += taxl['tax_amount']
#                     total_ap_cur_tax    += taxl['price']            
#             #print "total_ap_cur_taxzzzzzzzzzzzzzzzzzzz", total_ap_cur_tax
#             if total_ap_cur_tax:
#                 iml.append({
#                     'type': 'tax_total',
#                     'name': "Total AP Tax",
#                     'price': 0.0,#-(total_ap_cur_tax),
#                     'account_id': inv.ap_tax_account_id.id or inv.account_id.id,
#                     'date_maturity': inv.date_due,
#                     'amount_currency': 0.0, #diff_currency and total_ap_cur_tax,
#                     'currency_id': diff_currency and inv.currency_id.id,
#                     'ref': ref,
#                 })
#             ########################################################
#             diff_currency = inv.currency_id != company_currency
#             # create one move line for the total and possibly adjust the other lines amount
#             total, total_currency, iml = inv.with_context(ctx).compute_invoice_totals(company_currency, ref, iml)
#             #print "@@@@@@@@@@@@@@@@@@@@@@@total, total_currency, iml", total, total_currency, iml
#             name = inv.name or inv.supplier_invoice_number or '/'
#             totlines = []
#             if inv.payment_term:
#                 totlines = inv.with_context(ctx).payment_term.compute(total, date_invoice)[0]
#             if totlines:
#                 split_disc = tdisc = 0.0
#                 for i, t in enumerate(totlines):
#                     split_disc+=1
#                 if inv.discount_additional > 0:
#                     tdisc = inv.discount_additional / split_disc                
#                 res_amount_currency = total_currency
#                 ctx['date'] = date_invoice
#                 for i, t in enumerate(totlines):
#                     if inv.currency_id != company_currency:
#                         amount_currency = company_currency.with_context(ctx).compute(t[1], inv.currency_id)
#                     else:
#                         amount_currency = False
# 
#                     # last line: add the diff
#                     res_amount_currency -= amount_currency or 0
#                     if i + 1 == len(totlines):
#                         amount_currency += res_amount_currency
#                     iml.append({
#                         'type': 'dest',
#                         'name': name,
#                         'price': t[1]-tdisc,
#                         'account_id': inv.account_id.id,
#                         'date_maturity': t[0],
#                         'amount_currency': diff_currency and amount_currency,
#                         'currency_id': diff_currency and inv.currency_id.id,
#                         'ref': ref,
#                     })
#             else:
#                 #print "total------------>>", total
#                 if inv.discount_additional > 0:
#                     total = total - inv.discount_additional
#                 else:
#                     total = total 
#                 iml.append({
#                     'type': 'dest',
#                     'name': name,
#                     'price': total,
#                     'account_id': inv.account_id.id,
#                     'date_maturity': inv.date_due,
#                     'amount_currency': diff_currency and total_currency,
#                     'currency_id': diff_currency and inv.currency_id.id,
#                     'ref': ref
#                 })
#             #print "tot",tot,totalAR#,inv.add_disc_amt
#             if inv.discount_additional > 0:
#                 if inv.type in ('out_invoice', 'out_refund'):
#                     acc_disc_id = inv.company_id.sale_account_additional_discount_id and inv.company_id.sale_account_additional_discount_id.id
#                     if not inv.company_id.sale_account_additional_discount_id:
#                         raise osv.except_osv(_('Account Discount'),
#                            _('Please insert Account Discount for this Customer Invoice'))
#                 elif inv.type in ('in_invoice', 'in_refund'):
#                     acc_disc_id = inv.company_id.purchase_account_additional_discount_id and inv.company_id.purchase_account_additional_discount_id.id                    
#                     if not inv.company_id.purchase_account_additional_discount_id:
#                         raise osv.except_osv(_('Account Discount'),
#                            _('Please insert Account Discount for this Supplier Invoice'))
#                 iml.append({
#                     'type': 'dest',
#                     'name': 'Additional Discount',
#                     'price': inv.discount_additional,
#                     'account_id': acc_disc_id,
#                     'date_maturity': inv.date_due or False,
#                     'amount_currency': diff_currency \
#                             and total_currency or False,
#                     'currency_id': diff_currency \
#                             and inv.currency_id.id or False,
#                     'ref': ref
#                 })
#             date = date_invoice
#             
#             part = self.env['res.partner']._find_accounting_partner(inv.partner_id)
#             ###
#             line = [(0, 0, self.line_get_convert(l, part.id, date)) for l in iml]            
#             ###
#             line = inv.group_lines(iml, line)
#             #####Add Gain Loss Journal###
#             #line_sett_gl = False
#             for lp in line_principle_gl:
#                 line.append((0, 0, lp))
#             for lt in line_tax_gl:
#                 line.append((0, 0, lt))
#             for ld in line_dp_gl:
#                 line.append((0, 0, ld))
#             
#             for ls in line_sett_gl:    
#                 line.append((0, 0, ls))
#             #############################
#             journal = inv.journal_id.with_context(ctx)
#             if journal.centralisation:
#                 raise except_orm(_('User Error!'),
#                         _('You cannot create an invoice on a centralized journal. Uncheck the centralized counterpart box in the related journal from the configuration menu.'))
#             line = inv.finalize_invoice_move_lines(line)
#             i = 0
#             ########################
#             ######Gain Loss######
#             #line.append(line_principle_gl)
#             #####################
#             move_vals = {
#                 'ref'           : inv.reference or inv.name,
#                 'line_id'       : line,
#                 'journal_id'    : journal.id,
#                 'date'          : inv.date_invoice,
#                 'narration'     : inv.comment,
#                 'company_id'    : inv.company_id.id,
#             }
#             ctx['company_id'] = inv.company_id.id
#             period = inv.period_id
#             
#             if not period:
#                 period = period.with_context(ctx).find(date_invoice)[:1]
#             if period:
#                 move_vals['period_id'] = period.id
#                 for i in line:
#                     i[2]['period_id'] = period.id
#             ctx['invoice'] = inv
#             move = account_move.with_context(ctx).create(move_vals)
#             # make the invoice point to that move
#             vals = {
#                 'move_id': move.id,
#                 'period_id': period.id,
#                 'move_name': move.name,
#             }
#             inv.with_context(ctx).write(vals)
#             # Pass invoice in context in method post: used if you want to get the same
#             # account move reference when creating the same invoice after a cancelled one:
#             move.post()            
#             # == coba ah testing ==
#             obj_no_faktur = self.env['nomor.faktur.pajak'].browse(inv.nomor_faktur_id.id)
#             #invoice = self.env['account.invoice'].browse(context['default_res_id'])
#             if inv.nomor_faktur_id and inv.type == 'out_invoice':
#                 obj_no_faktur.write({
#                      'invoice_id': inv.id, 
#                      'partner_id': inv.partner_id.id, 
#                      'dpp': inv.amount_untaxed, 
#                      'tax_amount': inv.amount_tax,
#                      'date_used': inv.date_invoice,
#                      'company_id': inv.company_id.id,
#                      'status': '1', 
#                  })
#             elif inv.nomor_faktur_id and inv.type == 'in_invoice':                
#                 if inv.nomor_faktur_id[3] == "." and inv.nomor_faktur_id[6] == '.':
#                     if len(str(inv.nomor_faktur_id).split('.')[2]) > 8:
#                         raise osv.except_osv(_('Wrong Faktur Number'), _('Nomor Urut max 8 Digit'))                
#                     vals = {
#                         'company_id'        : inv.company_id.id,
#                         'nomor_perusahaan'  : str(inv.vat_supplier).split('.')[0],
#                         'tahun_penerbit'    : str(inv.vat_supplier).split('.')[1], 
#                         'nomor_urut'        : str(inv.vat_supplier).split('.')[2],
#                         'invoice_id'        : inv.id,
#                         'partner_id'        : inv.partner_id.id,
#                         'dpp'               : inv.amount_untaxed,
#                         'tax_amount'        : inv.amount_tax,
#                         'date_used'         : inv.date_invoice,
#                         'currency_id'       : inv.currency_id.id,
#                         'type'              : 'in',
#                         'status'            : '1',
#                     }
#                 else:
#                     raise osv.except_osv(_('Faktur Number Wrong'), _('Please input Faktur Number use SEPARATOR "."(DOT).'))
#                 obj_no_faktur.create(vals)
#         self._log_event()
#         return True
        
    @api.multi
    def action_cancel(self):
        #print "=====action_cancel==="
        moves = self.env['account.move']
        env_faktur = self.env['nomor.faktur.pajak']
        for inv in self:
            if inv.move_id:
                moves += inv.move_id
            if inv.payment_ids:
                for move_line in inv.payment_ids:
                    if move_line.reconcile_partial_id.line_partial_ids:
                        raise except_orm(_('Error!'), _('You cannot cancel an invoice which is partially paid. You need to unreconcile related payment entries first.'))
            if inv.nomor_faktur_id:
                env_faktur = env_faktur.browse(inv.nomor_faktur_id.id)
                
        # First, set the invoices as cancelled and detach the move ids
        self.write({'state': 'cancel', 'move_id': False})
        if env_faktur:
            env_faktur.write({'status': '0'})
        if moves:
            # second, invalidate the move(s)
            moves.button_cancel()
            # delete the move this invoice was pointing to
            # Note that the corresponding move_lines and move_reconciles
            # will be automatically deleted too
            moves.unlink()
        self._log_event(-1.0, 'Cancel Invoice')
        return True
 
account_invoice()

class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'
    
    disc_amount = fields.Float(string='Disc Amt', digits=dp.get_precision('Account'))
    
    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_id', 'quantity',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id')
    def _compute_price(self):
        price = (self.price_unit * (1 - (self.discount or 0.0) / 100.0)-self.disc_amount)
        taxes = self.invoice_line_tax_id.compute_all(price, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal = taxes['total']
        if self.invoice_id:
            self.price_subtotal = self.invoice_id.currency_id.round(self.price_subtotal)

    
    
    @api.model
    def move_line_get(self, invoice_id):
        inv = self.env['account.invoice'].browse(invoice_id)
        currency = inv.currency_id.with_context(date=inv.date_invoice)
        company_currency = inv.company_id.currency_id
        res = []
        for line in inv.invoice_line:
            mres = self.move_line_get_item(line)
            mres['invl_id'] = line.id
            res.append(mres)
            tax_code_found = False
            taxes = line.invoice_line_tax_id.compute_all(
                ((line.price_unit * (1.0 - (line.discount or 0.0) / 100.0)-line.disc_amount)),
                line.quantity, line.product_id, inv.partner_id)['taxes']
            for tax in taxes:
                if inv.type in ('out_invoice', 'in_invoice'):
                    tax_code_id = tax['base_code_id']
                    tax_amount = tax['price_unit'] * line.quantity * tax['base_sign']
                else:
                    tax_code_id = tax['ref_base_code_id']
                    tax_amount = tax['price_unit'] * line.quantity * tax['ref_base_sign']

                if tax_code_found:
                    if not tax_code_id:
                        continue
                    res.append(dict(mres))
                    res[-1]['price'] = 0.0
                    res[-1]['account_analytic_id'] = False
                elif not tax_code_id:
                    continue
                tax_code_found = True
                res[-1]['tax_code_id'] = tax_code_id                
                res[-1]['tax_amount'] = currency.compute(tax_amount, company_currency)
                #######
        return res
    
account_invoice_line()

class account_invoice_tax(models.Model):
    _inherit = 'account.invoice.tax'
    
    invoice_line_ids = fields.Many2many('account.invoice.line', 'tax_invoice_rel','tax_inv_id', 'tax_invoice_line_id',string='Tax Invoice Line',)
            
    @api.v8
    def compute(self, invoice):
        #print "compute***************"
        tax_grouped = {}
        currency = invoice.currency_id.with_context(date=invoice.date_invoice or fields.Date.context_today(invoice))
        company_currency = invoice.company_id.currency_id
        for line in invoice.invoice_line:
            taxes = line.invoice_line_tax_id.compute_all(
                ((line.price_unit * (1 - (line.discount or 0.0) / 100.0))-line.disc_amount),
                line.quantity, line.product_id, invoice.partner_id)['taxes']                
            #print "########", line.stock_move_id ,"##########", line.stock_move_id.taxes_id
            for tax in taxes:
                val = {
                    'invoice_id': invoice.id,
                    'name': tax['name'],
                    'amount': tax['amount'],
                    'manual': False,
                    'sequence': tax['sequence'],
                    'base': currency.round(tax['price_unit'] * line['quantity']),
                }
                if invoice.type in ('in_invoice','out_invoice'):                    
                    ###Cek Tax Invoice dan Stock Picking###
                    #===========================================================
                    # account_tax = False
                    # if line.stock_move_id and not line.stock_move_id.taxes_id and not tax['account_collected_id']:
                    #     account_tax = line.product_id and \
                    #                   line.product_id.categ_id.property_stock_valuation_account_id and \
                    #                   line.product_id.categ_id.property_stock_valuation_account_id.id
                    #===========================================================
                    #######
                   # if val['amount'] > 0.0 and line.date_fp:
                    if val['amount'] > 0.0 :
                        currency = invoice.currency_id.with_context(date=invoice.date_invoice or fields.Date.context_today(invoice))
                    elif val['amount'] < 0.0 :
                        currency = invoice.currency_id.with_context(date= invoice.date_invoice or fields.Date.context_today(invoice))
                    #######                   
                    val['base_code_id'] = tax['base_code_id']
                    val['tax_code_id'] = tax['tax_code_id']
                    val['base_amount'] = currency.compute_tax(val['base'] * tax['base_sign'], company_currency, round=False)
                    val['tax_amount'] = currency.compute_tax(val['amount'] * tax['tax_sign'], company_currency, round=False)
                    val['account_id'] = tax['account_collected_id'] or line.account_id.id
                    val['account_analytic_id'] = tax['account_analytic_collected_id']
                else:
                    val['base_code_id'] = tax['ref_base_code_id']
                    val['tax_code_id'] = tax['ref_tax_code_id']
                    val['base_amount'] = currency.compute_tax(val['base'] * tax['ref_base_sign'], company_currency, round=False)
                    val['tax_amount'] = currency.compute_tax(val['amount'] * tax['ref_tax_sign'], company_currency, round=False)
                    val['account_id'] = tax['account_paid_id'] or line.account_id.id
                    val['account_analytic_id'] = tax['account_analytic_paid_id']

                # If the taxes generate moves on the same financial account as the invoice line
                # and no default analytic account is defined at the tax level, propagate the
                # analytic account from the invoice line to the tax line. This is necessary
                # in situations were (part of) the taxes cannot be reclaimed,
                # to ensure the tax move is allocated to the proper analytic account.
                if not val.get('account_analytic_id') and line.account_analytic_id and val['account_id'] == line.account_id.id:
                    val['account_analytic_id'] = line.account_analytic_id.id

                key = (val['tax_code_id'], val['base_code_id'], val['account_id'])
                if not key in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['base'] += val['base']
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base_amount'] += val['base_amount']
                    tax_grouped[key]['tax_amount'] += val['tax_amount']

        for t in tax_grouped.values():
            t['base'] = currency.round(t['base'])
            t['amount'] = currency.round(t['amount'])
            t['base_amount'] = currency.round(t['base_amount'])
            t['tax_amount'] = currency.round(t['tax_amount'])
        return tax_grouped
    

