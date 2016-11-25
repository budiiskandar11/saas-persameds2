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