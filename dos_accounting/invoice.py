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
    
    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount')
    def _compute_amount(self):
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line)
        self.amount_tax = sum(line.amount for line in self.tax_line)
        
        self.gross_total = sum(line.price_unit * line.quantity for line in self.invoice_line)
        self.discount_total = sum(line.quantity* (line.price_unit * (line.discount or 0.0)/100) for line in self.invoice_line)
        self.amount_downpayment = self.payment_request_dp_id.amount_total or 0.0
        self.amount_total = self.amount_untaxed + self.amount_tax - self.amount_downpayment
    #####################
    
    gross_total = fields.Float(string='Total', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount' )
    discount_total = fields.Float(string='Total Disc', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount')
    amount_total = fields.Float(string='Total', digits=dp.get_precision('Account'),
            store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    
    ap_tax_account_id = fields.Many2one('account.account', string='Tax Payable',
        required=False, readonly=True, states={'draft': [('readonly', False)]},
        help="The partner account used for this invoice.")
    
    ###Prepayment Downpayment###
    payment_request_dp_id   = fields.Many2one('purchase.request',string="NOI DP")
    amount_downpayment      = fields.Float(string='Downpayment', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount')
    ###
    reference_invoice_id = fields.Many2one('account.invoice', string='Invoice Reference',)
    ###
    
    @api.multi
    def compute_invoice_totals(self, company_currency, ref, invoice_move_lines):
        total = 0
        total_currency = 0
        amount_tax_total =0.0
        amount_currency_tax_total =0.0
        for line in invoice_move_lines:
            
            print "line>>>>>>>>>>>>>>>>>>>>", line
            
            if self.currency_id != company_currency:
                ####
                ####
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
                    print "11111111111@@@@@@@@@@@@@@@amount_tax_total", amount_currency_tax_total, amount_tax_total
                ####
                
                elif line['type'] == 'tax_total':
                    if amount_tax_total > 0.0:
                        print "@@@@@@@@@@@@@@@amount_tax_total", amount_tax_total
                        line['amount_currency'] = -1 * amount_currency_tax_total
                        line['price'] = -1 * amount_tax_total or currency.compute_tax(line['price'], company_currency)
                    else:
                        line['price'] = 0.0
                        line['amount_currency'] = 0.0
                
                
                ####
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
                print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%@@@@@@@@@@@@@@@line['price']", line['amount_currency'], line['price']
                
                
                total -= line['price']
                total_currency -= line['amount_currency'] or line['price']
        
        
        #print "TOTAL.>>>>>>>>>>>>>>>>>>>>", total, total_currency, invoice_move_lines
        
        #raise except_orm(_('Warning!'), _('SSSSSSSSSSS'))
        return total, total_currency, invoice_move_lines
    
    def invoice_reverse(self, cr, uid, ids, context=None):
        print "####invoice_reverse####"
        
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
                
                #raise except_orm(_('Error!'), _('Please Check Payable Account Setting'))
            
            print "move_line.account_id.id+++++++++++++==", account_list, move_line.account_id.name
            print "rec_list_ids--------->>", rec_list_ids
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
            
            ###
            for key in d.keys():
                print "KEYS-->>", key, 'value', d[key]
                if len(d[key]) >= 2:
                    reconcile = move_line_obj.reconcile(cr, uid, d[key], 'auto', False, False, False, context=None)
            
        return True
    
    def gainloss_create(self, amount_src, amount_dest, account_counter, gainloss_account):
        line_gainloss_gl = []
        #for inv in self.browse(cr, uid, ids, context=None):
        #    gainloss_account_default = inv.company_id.income_currency_exchange_account_id.id
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
    def action_move_create(self):
        print "action_move_create--------------------->>"
        """ Creates invoice related analytics and financial move lines """
        account_invoice_tax = self.env['account.invoice.tax']
        account_move = self.env['account.move']
        line_sett_gl = []
        account_move_line_obj = self.env['account.move.line']

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
            compute_taxes = account_invoice_tax.compute(inv)
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
            
            print "iml>>>>>>>>>>>>>>>...TAX", iml
            
            if inv.type in ('in_invoice', 'in_refund'):
                ref = inv.reference
            else:
                ref = inv.number
            
            ##########Calculate Total AP Vendor & AP Tax###########
            diff_currency = inv.currency_id != company_currency
            total_ap_cur_tax    = 0.0
            total_ap_tax        = 0.0
            
            ####Gain Loss####
            #currency_obj    = self.pool.get('res.currency')
            #tax_obj         = self.pool.get('account.tax')
            line_principle_gl = []
            line_tax_gl       = []
            line_dp_gl        = []
            
            #####Downpayment######
            if inv.payment_request_dp_id:
                iml.append({
                        'type': 'src',
                        'name': "Downpayment",
                        'price': -inv.amount_downpayment,
                        'account_id': inv.payment_request_dp_id.order_line[0].product_id.property_account_expense.id,
                        'date_maturity': inv.date_due,
                        'amount_currency': diff_currency and total_ap_cur_tax,
                        'currency_id': diff_currency and inv.currency_id.id,
                        'ref': ref,
                                })
                print "inv.payment_request_dp_id.id????????????????????", inv.payment_request_dp_id.id
                dp_env = self.env['purchase.request'].browse(inv.payment_request_dp_id.id)
                dp_env.write({'prepayment_status' : True})
                
                po_env = self.env['purchase.order'].browse(inv.payment_request_dp_id.purchase_id.id)
                po_env.write({'dp_status' : 'used'})
                    
            if inv.currency_id <> company_currency:
                ######Gain Loss Downpayment######
                if inv.payment_request_dp_id:
                    currency = self.currency_id.with_context(date=inv.payment_request_dp_id.invoice_ids[0].date_invoice)
                    dp_original_amount_convert = currency.compute(inv.amount_downpayment, company_currency)
                    
                    currency = self.currency_id.with_context(date=self.date_invoice)
                    inv_original_amount_convert = currency.compute(inv.amount_downpayment, company_currency)
                    
                    diff_downpayment_gl = inv_original_amount_convert - dp_original_amount_convert
                    
                    if diff_downpayment_gl <> 0.0:
                        if diff_downpayment_gl > 0.0:
                            account_gl_downpayment_d = inv.company_id.expense_currency_exchange_account_id.id#427
                            account_gl_downpayment_c = inv.payment_request_dp_id.order_line[0].product_id.property_account_expense.id
                        else:
                            account_gl_downpayment_d = inv.payment_request_dp_id.order_line[0].product_id.property_account_expense.id
                            account_gl_downpayment_c = inv.company_id.income_currency_exchange_account_id.id#427
                        
                        
                        move_line_d = {
                                    'name'      : "Gain Loss Downpayment" or '/',
                                    'debit'     : abs(diff_downpayment_gl),
                                    'credit'    : 0.0,
                                    'account_id': account_gl_downpayment_d,
                                    'journal_id': inv.journal_id.id,
                                    'date'      : inv.date_invoice,
                                }
                        
                        move_line_c = {
                                    'name'      : "Gain Loss Downpayment" or '/',
                                    'debit'     : 0.0,
                                    'credit'    : abs(diff_downpayment_gl),
                                    'account_id': account_gl_downpayment_c,
                                    'journal_id': inv.journal_id.id,
                                    'date'      : inv.date_invoice,
                                        }
                        
                        line_dp_gl.append(move_line_d)
                        line_dp_gl.append(move_line_c)
                ###############Gain Loss Settlement#################
                if inv.settlement_id:
                    currency = self.currency_id.with_context(date=inv.settlement_id.cash_advance_id.invoice_id.date_invoice)
                    adv_original_amount_convert = currency.compute(inv.settlement_id.reserved, company_currency)
                    
                    currency = self.currency_id.with_context(date=self.date_invoice)
                    inv_original_amount_convert = currency.compute(inv.settlement_id.reserved, company_currency)
                    
                    diff_advance_gl = inv_original_amount_convert - adv_original_amount_convert
                    
                    line_sett_gl = self.gainloss_create(adv_original_amount_convert, inv_original_amount_convert, inv.settlement_id.account_advance_id.id, False)
                    
                    #print "diff_advance_gl>>>>>>>", diff_advance_gl
                    #raise except_orm(_('User Error!'),_('xxx'))
                
                for l_gl in inv.invoice_line:
                    ####Cek hanya untuk invoice from picking####
                    if l_gl.stock_move_id:
                        print "*******************", list(l_gl.invoice_line_tax_id)
                        
                        #####Selisih Kurs Principle########
                        tax_of_move         = l_gl.stock_move_id.taxes_id
                        tax_unit_amount     = l_gl.stock_move_id.tax_unit
                        ###Cek Gain Loss Per Unit###
                        inv_original_amount = l_gl.price_unit * 1#l_gl.quantity
                        
                        move_unit_amount    = l_gl.stock_move_id.price_unit  
                        
                        currency = self.currency_id.with_context(date=self.date_invoice)
                        inv_original_amount_convert = currency.compute(inv_original_amount, company_currency)
                        
                        ###Gain Loss dikali jumlah Quantity yg diinvoicekan###
                        diff_principle_gl = (inv_original_amount_convert - move_unit_amount) * l_gl.quantity
                        
                        print "Selisih Kurs Principle------>>", diff_principle_gl
                        
                        if diff_principle_gl <> 0.0:
                            if diff_principle_gl > 0.0:
                                account_gl_principle_d = inv.company_id.expense_currency_exchange_account_id.id#427
                                account_gl_principle_c = l_gl.account_id.id
                            else:
                                account_gl_principle_d = l_gl.account_id.id
                                account_gl_principle_c = inv.company_id.income_currency_exchange_account_id.id#427
                            
                            
                            move_line_d = {
                                        'name'      : "Gain Loss Principle" or '/',
                                        'debit'     : abs(diff_principle_gl),
                                        'credit'    : 0.0,
                                        'account_id': account_gl_principle_d,
                                        'journal_id': inv.journal_id.id,
                                        'date'      : inv.date_invoice,
                                    }
                            
                            move_line_c = {
                                        'name'      : "Gain Loss Principle" or '/',
                                        'debit'     : 0.0,
                                        'credit'    : abs(diff_principle_gl),
                                        'account_id': account_gl_principle_c,
                                        'journal_id': inv.journal_id.id,
                                        'date'      : inv.date_invoice,
                                            }
                            
                            line_principle_gl.append(move_line_d)
                            line_principle_gl.append(move_line_c)
                        
                        #####Selisih Kurs Taxes########
                        for tax_l_gl in list(l_gl.invoice_line_tax_id):
                            #original_tax_amount = tax_obj.compute([tax_of_move], l_gl.price_unit, l_gl.quantity, None, None)
                            ###Gain Loss dikali jumlah Quantity yg diinvoicekan###
                            inv_original_tax_amount = tax_of_move.amount * (l_gl.price_unit * 1)#l_gl.quantity)
                        
                            ###Pajak Date###
                            #currency = self.currency_id.with_context(date =  
                            #                                               (tax_l_gl.amount > 0.0 and l_gl.date_fp) or 
                            #                                               (tax_l_gl.amount < 0.0 and l_gl.date_bukti_potong) or 
                            #                                               self.date_invoice
                            #                                         )
                            inv_original_tax_amount_convert = currency.compute_tax(inv_original_tax_amount, company_currency)
                            ###Cek Tax di Invoice & Picking###
                            
                            if tax_l_gl.id == tax_of_move.id:
                                diff_tax_gl = (inv_original_tax_amount_convert - tax_unit_amount) * l_gl.quantity
                                if diff_tax_gl > 0.0:
                                    account_gl_tax_d = inv.company_id.expense_currency_exchange_account_id.id
                                    account_gl_tax_c = tax_l_gl.account_collected_id.id or l_gl.account_id.id
                                else:
                                    account_gl_tax_d = tax_l_gl.account_collected_id.id or l_gl.account_id.id
                                    account_gl_tax_c = inv.company_id.income_currency_exchange_account_id.id
                                
                                if diff_tax_gl <> 0.0:
                                    move_line_d = {
                                                'name'      : "Gain Loss Tax" or '/',
                                                'debit'     : abs(diff_tax_gl),
                                                'credit'    : 0.0,
                                                'account_id': account_gl_tax_d,
                                                'journal_id': inv.journal_id.id,
                                                'date'      : inv.date_invoice,
                                            }
                                    
                                    move_line_c = {
                                                'name'      : "Gain Loss Tax" or '/',
                                                'debit'     : 0.0,
                                                'credit'    : abs(diff_tax_gl),
                                                'account_id': account_gl_tax_c,
                                                'journal_id': inv.journal_id.id,
                                                'date'      : inv.date_invoice,
                                                    }
                                    
                                    line_tax_gl.append(move_line_d)
                                    line_tax_gl.append(move_line_c)
                    
            #################
            
            for taxl in iml:
                print "taxl.type---------->>", taxl['type'] 
                
                ####Cek Gain loss####
                print "GAIN123#################123", taxl
                #####################
                
                if taxl['type'] == 'tax':
                    
                    print "total_ap_tax------------>>", total_ap_tax
                    print "total_ap_cur_tax---------->>", total_ap_cur_tax
                    
                    total_ap_tax        += taxl['tax_amount']
                    total_ap_cur_tax    += taxl['price']
            
            print "total_ap_cur_taxzzzzzzzzzzzzzzzzzzz", total_ap_cur_tax
            if total_ap_cur_tax:
                iml.append({
                        'type': 'tax_total',
                        'name': "Total AP Tax",
                        'price': 0.0,#-(total_ap_cur_tax),
                        'account_id': inv.ap_tax_account_id.id or inv.account_id.id,
                        'date_maturity': inv.date_due,
                        'amount_currency': 0.0, #diff_currency and total_ap_cur_tax,
                        'currency_id': diff_currency and inv.currency_id.id,
                        'ref': ref,
                    })
                
            #raise except_orm(_('User Error!'),
             #           _('xxx'))
            #for i in iml:
            #    print "IML--------->>", i 
            #raise except_orm(_('User Error!'),
            #            _('xxx'))
            
            ########################################################
            
            
            diff_currency = inv.currency_id != company_currency
            # create one move line for the total and possibly adjust the other lines amount
            total, total_currency, iml = inv.with_context(ctx).compute_invoice_totals(company_currency, ref, iml)
            
            print "@@@@@@@@@@@@@@@@@@@@@@@total, total_currency, iml", total, total_currency, iml
            
            
            #raise except_orm(_('User Error!'),
            #            _('oooooooooooooooooooooooo'))
            
            name = inv.name or inv.supplier_invoice_number or '/'
            totlines = []
            if inv.payment_term:
                totlines = inv.with_context(ctx).payment_term.compute(total, date_invoice)[0]
            if totlines:
                res_amount_currency = total_currency
                ctx['date'] = date_invoice
                for i, t in enumerate(totlines):
                    if inv.currency_id != company_currency:
                        amount_currency = company_currency.with_context(ctx).compute(t[1], inv.currency_id)
                    else:
                        amount_currency = False

                    # last line: add the diff
                    res_amount_currency -= amount_currency or 0
                    if i + 1 == len(totlines):
                        amount_currency += res_amount_currency
                    print "@@@@@@@@@@@@@@@@@@@@@@t[1]------------>>", t[1]
                    iml.append({
                        'type': 'dest',
                        'name': name,
                        'price': t[1],
                        'account_id': inv.account_id.id,
                        'date_maturity': t[0],
                        'amount_currency': diff_currency and amount_currency,
                        'currency_id': diff_currency and inv.currency_id.id,
                        'ref': ref,
                    })
            else:
                print "total------------>>", total
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

            date = date_invoice
            
            part = self.env['res.partner']._find_accounting_partner(inv.partner_id)
            
            print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@iml2-------------------------------->>", iml
            #raise except_orm(_('User Error!'),
            #            _('You cannot create an invoice on a centralized journal. Uncheck the centralized counterpart box in the related journal from the configuration menu.'))
            ###
            line = [(0, 0, self.line_get_convert(l, part.id, date)) for l in iml]
            
            ###
            line = inv.group_lines(iml, line)

            #####Add Gain Loss Journal###
            #line_sett_gl = False
            for lp in line_principle_gl:
                line.append((0, 0, lp))
            for lt in line_tax_gl:
                line.append((0, 0, lt))
            for ld in line_dp_gl:
                line.append((0, 0, ld))
            
            for ls in line_sett_gl:    
                line.append((0, 0, ls))
            #############################

            journal = inv.journal_id.with_context(ctx)
            if journal.centralisation:
                raise except_orm(_('User Error!'),
                        _('You cannot create an invoice on a centralized journal. Uncheck the centralized counterpart box in the related journal from the configuration menu.'))

            line = inv.finalize_invoice_move_lines(line)
            ###Update Data Ditrik###
            i = 0
#             for l_d in line:
#                 line[i][2]['district'] = inv.distrik_id.id or False
#                 print "LINE**************", line[i][2]
#                 i += 1
            
            print "Line++++++++++++++++++++++++", line
            #raise except_orm(_('User Error!'),
            #            _('XXXXXXXXXXXXXXX'))
            ########################
            ######Gain Loss######
            #line.append(line_principle_gl)
            #####################
            move_vals = {
                'ref'           : inv.reference or inv.name,
                'line_id'       : line,
                'journal_id'    : journal.id,
                'date'          : inv.date_invoice,
                'narration'     : inv.comment,
                'company_id'    : inv.company_id.id,
                ###Distrik###
#                 'district'      : inv.distrik_id.id or False,
                ############
            }
            ctx['company_id'] = inv.company_id.id
            period = inv.period_id
            
            for f in line:
                print "#################", f
                print "----------"
            
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
            # == coba ah testing ==
            obj_no_faktur = self.env['nomor.faktur.pajak'].browse(inv.nomor_faktur_id.id)
            #invoice = self.env['account.invoice'].browse(context['default_res_id'])
            if inv.nomor_faktur_id and inv.type == 'out_invoice':
                obj_no_faktur.write({'invoice_id': inv.id, 
                                     'partner_id': inv.partner_id.id, 
                                     'dpp': inv.amount_untaxed, 
                                     'tax_amount': inv.amount_tax,
                                     'date_used': inv.date_invoice,
                                     'company_id': inv.company_id.id,
                                     #'currency_id': inv.currency_id.id,
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
    
    stock_move_id = fields.Many2one('stock.move', string='Stock Move')
    
    @api.model
    def move_line_get(self, invoice_id):
        inv = self.env['account.invoice'].browse(invoice_id)
        currency = inv.currency_id.with_context(date=inv.date_invoice)
        company_currency = inv.company_id.currency_id

        res = []
        for line in inv.invoice_line:
            print "XXXXXXXXXXXX"
            mres = self.move_line_get_item(line)
            mres['invl_id'] = line.id
            res.append(mres)
            tax_code_found = False
            taxes = line.invoice_line_tax_id.compute_all(
                (line.price_unit * (1.0 - (line.discount or 0.0) / 100.0)),
                line.quantity, line.product_id, inv.partner_id)['taxes']
            for tax in taxes:
                print "YYYYYYYYYYYYY"
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
                
                res[-1]['tax_amount'] = currency.compute_tax(tax_amount, company_currency)
                #######
        
        return res
    
account_invoice_line()

class account_invoice_tax(models.Model):
    _inherit = 'account.invoice.tax'
    
    invoice_line_ids = fields.Many2many('account.invoice.line', 'tax_invoice_rel','tax_inv_id', 
                                    'tax_invoice_line_id',string='Tax Invoice Line',)
            
            
    
    @api.v8
    def compute(self, invoice):
        print "compute***************"
        tax_grouped = {}
        currency = invoice.currency_id.with_context(date=invoice.date_invoice or fields.Date.context_today(invoice))
        company_currency = invoice.company_id.currency_id
        for line in invoice.invoice_line:
            taxes = line.invoice_line_tax_id.compute_all(
                (line.price_unit * (1 - (line.discount or 0.0) / 100.0)),
                line.quantity, line.product_id, invoice.partner_id)['taxes']                
            #print "########", line.stock_move_id ,"##########", line.stock_move_id.taxes_id
            for tax in taxes:
                print "tax-------->>", tax
                val = {
                    'invoice_id': invoice.id,
                    'name': tax['name'],
                    'amount': tax['amount'],
                    'manual': False,
                    'sequence': tax['sequence'],
                    'base': currency.round(tax['price_unit'] * line['quantity']),
                        }
                if invoice.type in ('out_invoice','in_invoice'):
                    
                    ###Cek Tax Invoice dan Stock Picking###
                    account_tax = False
                    if line.stock_move_id and not line.stock_move_id.taxes_id and not tax['account_collected_id']:
                        account_tax = line.product_id and \
                                      line.product_id.categ_id.property_stock_valuation_account_id and \
                                      line.product_id.categ_id.property_stock_valuation_account_id.id
                    print "########val['base']", val['base'], val['amount']
                    #######
                    if val['amount'] > 0.0 and line.date_fp:
                        currency = invoice.currency_id.with_context(date=line.date_fp or invoice.date_invoice or fields.Date.context_today(invoice))
                    elif val['amount'] < 0.0 and line.date_bukti_potong:
                        currency = invoice.currency_id.with_context(date=line.date_bukti_potong or invoice.date_invoice or fields.Date.context_today(invoice))
                    #######
                    
                    
                    val['base_code_id'] = tax['base_code_id']
                    val['tax_code_id'] = tax['tax_code_id']
                    val['base_amount'] = currency.compute_tax(val['base'] * tax['base_sign'], company_currency, round=False)
                    val['tax_amount'] = currency.compute_tax(val['amount'] * tax['tax_sign'], company_currency, round=False)
                    val['account_id'] = account_tax or tax['account_collected_id'] or line.account_id.id
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
    

