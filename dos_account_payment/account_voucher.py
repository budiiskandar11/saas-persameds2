import time
from lxml import etree

import openerp.netsvc
from openerp.osv import osv, fields
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

# class account_invoice(osv.osv):
#     _inherit = 'account.invoice'
#     
#     def invoice_pay_customer(self, cr, uid, ids, context=None):
#         if not ids: return []
#         inv = super(account_invoice, self).invoice_pay_customer(cr, uid, ids, context=context)
#         inv['payment_adm'] = 'cash'
#         return inv
#     
# account_invoice()

class account_voucher(osv.osv):
    _inherit = "account.voucher"
    
    def create(self, cr, uid, vals, context=None):
        voucher_obj = self.pool.get('account.voucher')
        voc_search  = voucher_obj.search(cr,uid,[],context=None)
        last_number = 0
        new_number  = 0
        cr.execute("select MAX(payment_voucher_order_number) from account_voucher where type='payment'")
        search = cr.fetchone()[0]
        
        if search:
            last_number = search
        new_number = last_number+1 
        
        vals['payment_voucher_order_number'] = new_number
        order =  super(account_voucher, self).create(cr, uid, vals, context=context)
        return order
    
    def _get_rate(self, cr, uid, ids, name, args, context=None):
        a = {}
        rate = {}
        journal = self.browse(cr, uid, ids, context)
        for b in journal:
            if b.journal_id.currency.id:
                currency_id = b.journal_id.currency.id
                rate_cur1 = self.pool.get('res.currency.rate').search(cr, uid, [('currency_id','=',currency_id)], context=context)
                rate_cur = self.pool.get('res.currency.rate').browse(cr, uid, rate_cur1, context=context)
                i = 0
                for c in rate_cur:
                    if c.name == b.date:
                        rate[i] = c.rate
                        i+=1
                    else:
                        if b.date > c.name:
                            rate[i] = c.rate
                            i+=1
            else:
                rate[0] = 1
        for d in journal:
            a[d.id] = rate[0]
        return a


    
    _columns = {
        'payment_voucher_order_number' : fields.integer('No.'),
        'payment_adm'       : fields.selection([
            ('cash','Cash'),
            ('free_transfer','Non Payment Administration Transfer'),
            ('transfer','Transfer'),
            ('check','Cheque'),
            ('letter','Letter Credit'),
            ('cc','Credit Card'),
            ('debit','Debit Card'),
            ],'Payment Adm', readonly=True, select=True, states={'draft': [('readonly', False)],'proforma': [('readonly', False)]}),
        'adm_acc_id'        : fields.many2one('account.account', 'Account Adm', readonly=True, states={'draft': [('readonly', False)],'proforma': [('readonly', False)]}),
        'adm_comment'       : fields.char('Comment Adm', size=128, required=False, readonly=True, states={'draft': [('readonly', False)],'proforma': [('readonly', False)]}),
        'card_number'       : fields.char('Card Number', size=128, required=False, readonly=True, states={'draft': [('readonly', False)],'proforma': [('readonly', False)]}),
        'card_type'         : fields.selection([
            ('visa','Visa'),
            ('master','Master'),
            ('bca','BCA Card'),
            ('citi','CITI Card'),
            ('amex','AMEX'),
            ],'Card Type', size=128, required=False, readonly=True, states={'draft': [('readonly', False)],'proforma': [('readonly', False)]}),
        'adm_amount'        : fields.float('Amount Adm', readonly=True, states={'draft': [('readonly', False)],'proforma': [('readonly', False)]}),
        'bank_id'           : fields.many2one("res.bank", "Bank", required=False, readonly=True, states={"draft":[("readonly", False)],'proforma': [('readonly', False)]}, select=2),
        'check_number'      : fields.char('Check No', size=128, required=False, readonly=True, states={'draft': [('readonly', False)],'proforma': [('readonly', False)]}),
        "check_start_date"  : fields.date("Check Date", required=False, readonly=True, states={"draft":[("readonly", False)],'proforma': [('readonly', False)]}),
        "check_end_date": fields.date("Check Expire Date", required=False, readonly=True, states={"draft":[("readonly", False)],'proforma': [('readonly', False)]}),
        "check_registered"  : fields.many2one('account.check.line', "Check Registered"),
        'rate'              : fields.function(_get_rate, type='float', string='Rate', store=False),
        'letter_id'         : fields.many2one('letter.credit','Letter Credit'),
        'letter_name'       : fields.related('letter_id','name',type="char",string="Letter Credit Number",readonly=True),
        'letter_amount'     : fields.related('letter_id','amount',type="float",string="Amount",readonly=True),
        'letter_bank'       : fields.related('letter_id','bank_name',type="char",string="Bank",readonly=True),
        
        'payment_rate': fields.float('Exchange Rate', digits=(12,12), required=True, readonly=True, states={'draft': [('readonly', False)]},
            help='The specific rate that will be used, in this voucher, between the selected currency (in \'Payment Rate Currency\' field)  and the voucher currency.'),
    }
    _defaults = {
        # 'payment_adm': 'cash'
    }
    
    ####TESTING - untuk perubahan tanggal ###
    def onchange_date(self, cr, uid, ids, date, currency_id, payment_rate_currency_id, amount, company_id, context=None):
        """
        @param date: latest value from user input for field date
        @param args: other arguments
        @param context: context arguments, like lang, time zone
        @return: Returns a dict which contains new values, and context
        """
        if context is None:
            context ={}
        res = {'value': {}}
        
       
        #set the period of the voucher
        period_pool = self.pool.get('account.period')
        currency_obj = self.pool.get('res.currency')
        ctx = context.copy()
        ctx.update({'company_id': company_id, 'account_period_prefer_normal': True})
        voucher_currency_id = currency_id or self.pool.get('res.company').browse(cr, uid, company_id, context=ctx).currency_id.id
        pids = period_pool.find(cr, uid, date, context=ctx)
        if pids:
            res['value'].update({'period_id':pids[0]})
        if payment_rate_currency_id:
            ctx.update({'date': date})
            payment_rate = 1.0
            if payment_rate_currency_id != currency_id:
                tmp = currency_obj.browse(cr, uid, payment_rate_currency_id, context=ctx).rate
                payment_rate = tmp / currency_obj.browse(cr, uid, voucher_currency_id, context=ctx).rate
            vals = self.onchange_payment_rate_currency(cr, uid, ids, voucher_currency_id, payment_rate, payment_rate_currency_id, date, amount, company_id, context=context)
            vals['value'].update({'payment_rate': payment_rate})
            for key in vals.keys():
                res[key].update(vals[key])
        return res
    
    def recompute_voucher_lines(self, cr, uid, ids, partner_id, journal_id, price, currency_id, ttype, date, context=None):
        print "***************************************************%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", journal_id, price, currency_id, ids, context
        """
        Returns a dict that contains new values and context

        @param partner_id: latest value from user input for field partner_id
        @param args: other arguments
        @param context: context arguments, like lang, time zone

        @return: Returns a dict which contains new values, and context
        """
        def _remove_noise_in_o2m():
            """if the line is partially reconciled, then we must pay attention to display it only once and
                in the good o2m.
                This function returns True if the line is considered as noise and should not be displayed
            """
            if line.reconcile_partial_id:
                if currency_id == line.currency_id.id:
                    if line.amount_residual_currency <= 0:
                        return True
                else:
                    if line.amount_residual <= 0:
                        return True
            return False

        if context is None:
            context = {}
        context_multi_currency = context.copy()
        #########
        currency_journal = currency_id or journal.company_id.currency_id.id#line.voucher_id.journal_id.currency
        #########
        currency_pool = self.pool.get('res.currency')
        move_line_pool = self.pool.get('account.move.line')
        partner_pool = self.pool.get('res.partner')
        journal_pool = self.pool.get('account.journal')
        line_pool = self.pool.get('account.voucher.line')

        #set default values
        default = {
            'value': {'line_dr_ids': [], 'line_cr_ids': [], 'pre_line': False},
        }

        # drop existing lines
        line_ids = ids and line_pool.search(cr, uid, [('voucher_id', '=', ids[0])])
        for line in line_pool.browse(cr, uid, line_ids, context=context):
            if line.type == 'cr':
                default['value']['line_cr_ids'].append((2, line.id))
            else:
                default['value']['line_dr_ids'].append((2, line.id))

        if not partner_id or not journal_id:
            return default

        journal = journal_pool.browse(cr, uid, journal_id, context=context)
        partner = partner_pool.browse(cr, uid, partner_id, context=context)
        currency_id = currency_id or journal.company_id.currency_id.id

        total_credit = 0.0
        total_debit = 0.0
        account_type = None
        if context.get('account_id'):
            account_type = self.pool['account.account'].browse(cr, uid, context['account_id'], context=context).type
        if ttype == 'payment':
            if not account_type:
                account_type = 'payable'
            total_debit = price or 0.0
        else:
            total_credit = price or 0.0
            if not account_type:
                account_type = 'receivable'

        if not context.get('move_line_ids', False):
            #####AR vs AP######
            if account_type in ('payable', 'receivable'):
                ids = move_line_pool.search(cr, uid, [('state','=','valid'), ('account_id.type', 'in', ('payable', 'receivable')), ('reconcile_id', '=', False), ('partner_id', '=', partner_id)], context=context)
            else:
                ids = move_line_pool.search(cr, uid, [('state','=','valid'), ('account_id.type', '=', account_type), ('reconcile_id', '=', False), ('partner_id', '=', partner_id)], context=context)
            ###################
            ##Asli##
            #ids = move_line_pool.search(cr, uid, [('state','=','valid'), ('account_id.type', '=', account_type), ('reconcile_id', '=', False), ('partner_id', '=', partner_id)], context=context)
        else:
            ids = context['move_line_ids']
        invoice_id = context.get('invoice_id', False)
        company_currency = journal.company_id.currency_id.id
        move_lines_found = []

        #order the lines by most old first
        ids.reverse()
        account_move_lines = move_line_pool.browse(cr, uid, ids, context=context)

        #compute the total debit/credit and look for a matching open amount or invoice
        for line in account_move_lines:
            if _remove_noise_in_o2m():
                continue

            if invoice_id:
                if line.invoice.id == invoice_id:
                    #if the invoice linked to the voucher line is equal to the invoice_id in context
                    #then we assign the amount on that line, whatever the other voucher lines
                    move_lines_found.append(line.id)
            elif currency_id == company_currency:
                #otherwise treatments is the same but with other field names
                if line.amount_residual == price:
                    #if the amount residual is equal the amount voucher, we assign it to that voucher
                    #line, whatever the other voucher lines
                    move_lines_found.append(line.id)
                    break
                #otherwise we will split the voucher amount on each line (by most old first)
                total_credit += line.credit or 0.0
                total_debit += line.debit or 0.0
            elif currency_id == line.currency_id.id:
                if line.amount_residual_currency == price:
                    move_lines_found.append(line.id)
                    break
                total_credit += line.credit and line.amount_currency or 0.0
                total_debit += line.debit and line.amount_currency or 0.0

        remaining_amount = price
        #voucher line creation
        for line in account_move_lines:

            if _remove_noise_in_o2m():
                continue

            if line.currency_id and currency_id == line.currency_id.id:
                amount_original = abs(line.amount_currency)
                amount_unreconciled = abs(line.amount_residual_currency)
            else:
                #always use the amount booked in the company currency as the basis of the conversion into the voucher currency
                ############
                original_currency = line.currency_id.id or company_currency
                print "CEK Currency", currency_journal, company_currency, original_currency
                
                if currency_journal <> original_currency and currency_journal == company_currency:
                #if currency_journal == company_currency and original_currency <> company_currency:
                    ####
                    context_multi_currency['force_rate']   = context.get('voucher_special_currency_rate')
                    ####
                    amount_original     = currency_pool.compute(cr, uid, original_currency, company_currency, abs(line.amount_currency) or 0.0, context=context_multi_currency)
                    amount_unreconciled = currency_pool.compute(cr, uid, original_currency, company_currency, abs(line.amount_currency) or 0.0, context=context_multi_currency)
                else:
                    amount_original = currency_pool.compute(cr, uid, company_currency, currency_id, line.credit or line.debit or 0.0, context=context_multi_currency)
                    amount_unreconciled = currency_pool.compute(cr, uid, company_currency, currency_id, abs(line.amount_residual), context=context_multi_currency)
            line_currency_id = line.currency_id and line.currency_id.id or company_currency
            rs = {
                'name':line.move_id.name,
                'type': line.credit and 'dr' or 'cr',
                'move_line_id':line.id,
                'account_id':line.account_id.id,
                'amount_original': amount_original,
                'amount': (line.id in move_lines_found) and min(abs(remaining_amount), amount_unreconciled) or 0.0,
                'date_original':line.date,
                'date_due':line.date_maturity,
                'amount_unreconciled': amount_unreconciled,
                'currency_id': line_currency_id,
            }
            remaining_amount -= rs['amount']
            #in case a corresponding move_line hasn't been found, we now try to assign the voucher amount
            #on existing invoices: we split voucher amount by most old first, but only for lines in the same currency
            if not move_lines_found:
                if currency_id == line_currency_id:
                    if line.credit:
                        amount = min(amount_unreconciled, abs(total_debit))
                        rs['amount'] = amount
                        total_debit -= amount
                    else:
                        amount = min(amount_unreconciled, abs(total_credit))
                        rs['amount'] = amount
                        total_credit -= amount

            if rs['amount_unreconciled'] == rs['amount']:
                rs['reconcile'] = True

            if rs['type'] == 'cr':
                default['value']['line_cr_ids'].append(rs)
            else:
                default['value']['line_dr_ids'].append(rs)

            if len(default['value']['line_cr_ids']) > 0:
                default['value']['pre_line'] = 1
            elif len(default['value']['line_dr_ids']) > 0:
                default['value']['pre_line'] = 1
            default['value']['writeoff_amount'] = self._compute_writeoff_amount(cr, uid, default['value']['line_dr_ids'], default['value']['line_cr_ids'], price, ttype)
        return default
    
    def check_checking(self, cr, uid, ids, context=None):
        for voc in self.browse(cr, uid, ids, context=None):
            if voc.check_registered.check_id:
                if voc.check_registered.check_id.state <> "confirm":
                    raise osv.except_osv(_('Warning !'), _('This Check is not Confirm.'))
        return True
    
    def update_check(self, cr, uid, ids, context=None):
        total=0
        for voc in self.browse(cr, uid, ids, context=None):
            self.pool.get('account.check.line').write(cr, uid, [voc.check_registered.id], {'state':'paid'})
            cheque_line=self.pool.get('account.check.line').browse(cr, uid, [voc.check_registered.id], {'state':'hold'})
            cheque=self.pool.get('account.check').browse(cr,uid,[voc.check_registered.check_id.id],{'state':'confirm'})
            total+=cheque_line.amount
            self.pool.get('account.check').write(cr, uid, [voc.check_registered.check_id.id], {'total_check2':total})
            cheque.qty-=1
            if cheque.qty==0:
                self.pool.get('account.check').write(cr, uid, [voc.check_registered.check_id.id], {'state':'used'})
                self.pool.get('account.check').write(cr, uid, [voc.check_registered.check_id.id], {'total_check2':0.0})
        return True
    
    def update_letter(self, cr, uid, ids, context=None):
        voucher_ids = self.pool.get('account.voucher').browse(cr, uid, ids)[0]
        for voc in self.browse(cr, uid, ids, context=None):
            self.pool.get('letter.credit').write(cr, uid, [voc.letter_id.id], {'date_paid':time.strftime('%Y-%m-%d'),'state':'paid','voucher_id':voucher_ids.id})
        return True
    
    def proforma_voucher(self, cr, uid, ids, context=None):
        self.check_checking(cr, uid, ids, context)
        voucher = self.browse(cr, uid, ids)[0]
        if voucher.payment_adm == 'check':
            self.update_check(cr, uid, ids, context=context)
        if voucher.payment_adm == 'letter':
            self.update_letter(cr, uid, ids, context=context)
        self.action_move_line_create(cr, uid, ids, context=context)
        return True

    def cancel_voucher(self, cr, uid, ids, context=None):
        reconcile_pool = self.pool.get('account.move.reconcile')
        move_pool = self.pool.get('account.move')
        #---
        #tambahan untuk ad_payment_adm
        #---
        check_pool = self.pool.get('account.check')
        #-----------------------------
        for voucher in self.browse(cr, uid, ids, context=context):
            recs = []
            for line in voucher.move_ids:
                if line.reconcile_id:
                    recs += [line.reconcile_id.id]
                if line.reconcile_partial_id:
                    recs += [line.reconcile_partial_id.id]

            reconcile_pool.unlink(cr, uid, recs)
            if voucher.move_id:
                move_pool.button_cancel(cr, uid, [voucher.move_id.id])
                move_pool.unlink(cr, uid, [voucher.move_id.id])
        
        #tambah untuk ad_payment_adm
            if voucher.payment_adm == 'check':
                self.pool.get('account.check').write(cr, uid, [voucher.check_registered.check_id.id], {'state':'confirm'})
                self.pool.get('account.check.line').write(cr, uid, [voucher.check_registered.id], {'state':'hold'})
                cheque_line=self.pool.get('account.check.line').browse(cr, uid, [voucher.check_registered.id], {'state':'hold'})
                cheque=self.pool.get('account.check').browse(cr,uid,[voucher.check_registered.check_id.id],{'state':'confirm'})
                cheque.qty+=1

        #---------------------------
        res = {
            'state':'cancel',
            'move_id':False,
        }
        self.write(cr, uid, ids, res)
        return True
    
    def create_check(self, cr, uid, ids, context=None):
        #---
        #self.action_move_line_create(cr, uid, ids, context=context)
        #---
        voucher_pool = self.pool.get('account.voucher')
        check_pool = self.pool.get('account.check.line')
        voucher_ids = voucher_pool.browse(cr, uid, ids)[0]
        #---
        #print "vocer",voucher_ids.id
        #---
        if voucher_ids.payment_adm == 'check':
            check = {
                'name': voucher_ids.check_number,
                'type_voucher': 'payment',
                #---
                #'voucher': voucher_ids.number,
                #---
                'voucher': "/",
                'date': voucher_ids.check_start_date,
                'date_end': voucher_ids.check_end_date,
                'amount': voucher_ids.amount,
                'voucher_id': voucher_ids.id,
                'partner_id': voucher_ids.partner_id.id,
                'state': 'paid',
            }
            #--
            #print "xxx",check
            #---
            check_pool.create(cr, uid, check)
        return True
    
    def action_move_line_create2(self, cr, uid, ids, context=None):
        print "XXXXXXXXXXXX123"
        '''
        Confirm the vouchers given in ids and create the journal entries for each of them
        '''
        if context is None:
            context = {}
        move_pool = self.pool.get('account.move')
        move_line_pool = self.pool.get('account.move.line')
        for voucher in self.browse(cr, uid, ids, context=context):
            if voucher.move_id:
                continue
            company_currency = self._get_company_currency(cr, uid, voucher.id, context)
            current_currency = self._get_current_currency(cr, uid, voucher.id, context)
            #---
            # we select the context to use accordingly if it's a multicurrency case or not
            #---
            context = self._sel_context(cr, uid, voucher.id, context)
            #---
            # But for the operations made by _convert_amount, we always need to give the date in the context
            #---
            ctx = context.copy()
            ctx.update({'date': voucher.date})
            #---
            # Create the account move record.
            #---
            move_id = move_pool.create(cr, uid, self.account_move_get(cr, uid, voucher.id, context=context), context=context)
            #---
            # Get the name of the account_move just created
            #---
            name = move_pool.browse(cr, uid, move_id, context=context).name
            #---
            # Create the first line of the voucher
            #---
            move_line_id = move_line_pool.create(cr, uid, self.first_move_line_get(cr,uid,voucher.id, move_id, company_currency, current_currency, context), context)
            move_line_brw = move_line_pool.browse(cr, uid, move_line_id, context=context)
            line_total = move_line_brw.debit - move_line_brw.credit
            #---
            #print "move_line_brw.debit - move_line_brw.credit", move_line_brw.debit , move_line_brw.credit
            #---
            rec_list_ids = []
            if voucher.type == 'sale':
                line_total = line_total - self._convert_amount(cr, uid, voucher.tax_amount, voucher.id, context=ctx)
            elif voucher.type == 'purchase':
                line_total = line_total + self._convert_amount(cr, uid, voucher.tax_amount, voucher.id, context=ctx)
            #---
            # Create one move line per voucher line where amount is not 0.0
            #----
            
            
            line_total, rec_list_ids = self.voucher_move_line_create(cr, uid, voucher.id, line_total, move_id, company_currency, current_currency, context)
            
            #----------------UNTUK check----------------------
            currency_pool = self.pool.get('res.currency')
            diff_adm = voucher.adm_amount
            if voucher.payment_adm == 'transfer' or voucher.payment_adm == 'check':
                debit_adm = currency_pool.compute(cr, uid, current_currency, company_currency, diff_adm, context=ctx)
                credit_adm = currency_pool.compute(cr, uid, current_currency, company_currency, diff_adm, context=ctx)
                sign_adm = debit_adm - credit_adm < 0 and -1 or 1
                if voucher.payment_adm == 'transfer':
                    cost_name = voucher.adm_comment
                else:
                    cost_name = 'Check Fee'
                    
                move_line_adm_c = {
                    'name': cost_name,
                    'account_id': voucher.account_id.id,
                    'move_id': move_id,
                    #---
                    #'partner_id': voucher.partner_id.id,
                    #---
                    'date': voucher.date,
                    'debit': 0,
                    #---
                    # < 0 and -diff or 0.0,
                    #---
                    'credit': credit_adm,
                    #---
                    #diff > 0 and diff or 0.0,
                    #---
                    'currency_id': company_currency <> current_currency and current_currency or False,
                    'amount_currency': company_currency <> current_currency and sign_adm * -diff_adm or 0.0,
                }
                #----
                #account_id = voucher.adm_acc_id.id
                #----
                move_line_adm_d = {
                    'name': cost_name,
                    'account_id': voucher.adm_acc_id.id,
                    'move_id': move_id,
                    #----
                    #'partner_id': voucher.partner_id.id,
                    #----
                    'date': voucher.date,
                    'debit': debit_adm,
                    #----
                    # < 0 and -diff or 0.0,
                    #----
                    'credit': 0,
                    #----
                    #diff > 0 and diff or 0.0,
                    #----
                    'currency_id': company_currency <> current_currency and current_currency or False,
                    'amount_currency': company_currency <> current_currency and sign_adm * diff_adm or 0.0,
                }
                #-----
                #print "xxxx3xxxx",move_line_adm_c
                #print "xxxx4xxxx",move_line_adm_d
                #----
                if diff_adm != 0:
                    move_line_pool.create(cr, uid, move_line_adm_c)
                    move_line_pool.create(cr, uid, move_line_adm_d)
            #------------------------------------------------------
            # Create the writeoff line if needed
            #----
            ml_writeoff = self.writeoff_move_line_get(cr, uid, voucher.id, line_total, move_id, name, company_currency, current_currency, context)
            if ml_writeoff:
                ########################
                if voucher.type == 'payment':
                    writeoff_amount = voucher.writeoff_amount
                    if (writeoff_amount > 0 and ml_writeoff['credit'] <> 0.0 or writeoff_amount < 0 and ml_writeoff['debit']) and (ml_writeoff['debit'] <= 0.01 or ml_writeoff['credit'] <= 0.01):
                        ml_writeoff_balance = ml_writeoff.copy()
                        ml_writeoff_balance.update({
                            'name'          : ml_writeoff_balance['name'] + "Balance",
                            'debit'         : ml_writeoff_balance['debit'] * 2,
                            'credit'        : ml_writeoff_balance['credit'] * 2,
                            'amount_currency' : 0.0
                        })
                        move_line_pool.create(cr, uid, ml_writeoff_balance, context)
                        ml_writeoff.update({
                                    'debit'     : ml_writeoff['credit'],
                                    'credit'    : ml_writeoff['debit'],
                                })
                move_line_pool.create(cr, uid, ml_writeoff, context)
                #-----
            # We post the voucher.
            #-----
            self.write(cr, uid, [voucher.id], {
                'move_id': move_id,
                'state': 'posted',
                'number': name,
            })
            if voucher.journal_id.entry_posted:
                move_pool.post(cr, uid, [move_id], context={})
                #-----
            # We automatically reconcile the account move lines.
            #-----
            for rec_ids in rec_list_ids:
                if len(rec_ids) >= 2:
                    move_line_pool.reconcile_partial(cr, uid, rec_ids, writeoff_acc_id=voucher.writeoff_acc_id.id, writeoff_period_id=voucher.period_id.id, writeoff_journal_id=voucher.journal_id.id)
        return True
    
account_voucher()

class account_voucher_line(osv.osv):
    _inherit = 'account.voucher.line'
     
    def _compute_balance(self, cr, uid, ids, name, args, context=None):
        print "############_compute_balance BARU"
        currency_pool = self.pool.get('res.currency')
        rs_data = {}
        for line in self.browse(cr, uid, ids, context=context):
            ctx = context.copy()
            ctx.update({'date': line.voucher_id.date})
            voucher_rate = self.pool.get('res.currency').read(cr, uid, line.voucher_id.currency_id.id, ['rate'], context=ctx)['rate']
            ctx.update({
                'voucher_special_currency': line.voucher_id.payment_rate_currency_id and line.voucher_id.payment_rate_currency_id.id or False,
                'voucher_special_currency_rate': line.voucher_id.payment_rate * voucher_rate})
            res = {}
            company_currency = line.voucher_id.journal_id.company_id.currency_id.id
            voucher_currency = line.voucher_id.currency_id and line.voucher_id.currency_id.id or company_currency
            move_line = line.move_line_id or False

            if not move_line:
                print "1111111111111"
                res['amount_original'] = 0.0
                res['amount_unreconciled'] = 0.0
            elif move_line.currency_id and voucher_currency==move_line.currency_id.id:
                print "2222222222222"
                res['amount_original'] = abs(move_line.amount_currency)
                res['amount_unreconciled'] = abs(move_line.amount_residual_currency)
            else:
                print "3333333333333", move_line.name
                #always use the amount booked in the company currency as the basis of the conversion into the voucher currency
                currency_journal    = line.voucher_id.journal_id.currency or company_currency
                original_currency   = line.move_line_id.currency_id.id or company_currency
                
                print "zzzzzzzzzzzzzzzzzzzzzBARU", currency_journal, original_currency, company_currency
                
                #if not currency_journal and original_currency <> company_currency:
                    
                if currency_journal <> original_currency and currency_journal == company_currency:
                    print "AAAAAAAAAAAAAA"
                    ctx.update({
                        'force_rate':line.voucher_id.payment_rate})
                    res['amount_original']     = currency_pool.compute(cr, uid, original_currency, company_currency, abs(line.move_line_id.amount_currency) or 0.0, context=ctx)
                    res['amount_unreconciled'] = currency_pool.compute(cr, uid, original_currency, company_currency, abs(line.move_line_id.amount_currency) or 0.0, context=ctx)
                else:
                    print "BBBBBBBBBBBBBB"
                    res['amount_original']     = currency_pool.compute(cr, uid, company_currency, voucher_currency, move_line.credit or move_line.debit or 0.0, context=ctx)
                    res['amount_unreconciled'] = currency_pool.compute(cr, uid, company_currency, voucher_currency, abs(move_line.amount_residual), context=ctx)
                
                print "CCCCCCCCCCCCCC", move_line.credit or move_line.debit, abs(move_line.amount_residual)
                
                #res['amount_original']     = currency_pool.compute(cr, uid, company_currency, voucher_currency, move_line.credit or move_line.debit or 0.0, context=ctx)
                #res['amount_unreconciled'] = currency_pool.compute(cr, uid, company_currency, voucher_currency, abs(move_line.amount_residual), context=ctx)
                
            rs_data[line.id] = res
        return rs_data
     
    _columns = {
            'amount_original': fields.function(_compute_balance, multi='dc', type='float', string='Original Amountxxx', store=True, digits_compute=dp.get_precision('Account')),
            'amount_unreconciled': fields.function(_compute_balance, multi='dc', type='float', string='Open Balance', store=True, digits_compute=dp.get_precision('Account')),
                }
     
account_voucher_line()