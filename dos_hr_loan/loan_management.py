import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta

from openerp import netsvc
from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.tools.safe_eval import safe_eval as eval

# class loan_account(osv.osv):
#     _name = 'loan.account'
#     _description = "account for loan"
#     _columns={ 
#               'name':fields.char('Name', size=64, required=True, select=1),
#               'note': fields.text('Note'),
#               'account_analytic_id': fields.many2one('account.analytic.account', 'Analytic account'),
#               'account_loan_id': fields.many2one('account.account', 'Loan Account', required=True),
#               'account_payment_id': fields.many2one('account.account', 'Payment Account', required=True),
# #              'account_expense_salary_id': fields.many2one('account.account', 'Salaries Account', required=True),
#               'journal_id': fields.many2one('account.journal', 'Journal', required=True),
#               'company_id': fields.many2one('res.company', 'Company', required=True),
# #              'employe_id': fields.many2one('hr.employee', 'Employee', required=True),
# #              'paymentmethode':fields.selection([('salaries_discount','Salaries Discount'),('directcash','Direct Cash')], 'Payment Methode',  required=False, help="this is the methode of how the loan is paid"),
#               }
#      
#     _defaults = {
#         'company_id': lambda self, cr, uid, context: self.pool.get('res.company')._company_default_get(cr, uid, 'loan.account', context=context),
#     }
#     
#     def onchange_account_loan(self,cr,uid, ids,account_loan_id,context=None):
#         res = {'value':{}}
#         if account_loan_id:
#             res['value']={'account_loan_id':account_loan_id}
#         return res
#     
# loan_account()


class loan_management(osv.osv):
    _name = 'loan.management'
    _description = "loan for employeee"
    
#    def _cal_payment(self, cr, uid, ids, name, args, context=None):
#        loan = {'value': {'loansum'}}
#        installment = {'value':{'installment'}}
#        payment = loan/installment
#
#        return payment
    
#    def _calc_res(self,cr, uid, ids, name, args, context=None):
#        res = {}
#        
##        for period in self.read(cr, uid, ids, ['name'], context=context):
##            date1,date2 = period['name'].split(' to ')
##            cr.execute("SELECT SUM(loansum-paymentsum) FROM loan_management AS residu \
##                        WHERE (residu.installment_ids=ac.id) ",(str(date2),str(date1),))
##            amount = cr.fetchone()
##            amount = amount[0] or 0.00
##            res[period['id']] = amount
#
#        return res
#    
#    def _cal_paymentsum(self,cr,uid,ids,name,args,contex=None):
#        
#        return

    def _get_period(self, cr, uid, context={}):
        periods = self.pool.get('account.period').find(cr, uid)
        if periods:
            return periods[0]
        else:
            return False
    
    def _cal_payment(self, cr, uid, ids, name, arg, context={}):
        result={}
        for loan in self.browse(cr,uid,ids):
            
            result[loan.id] = 0
#        for emp in self.pool.get('hr.employee').browse(cr, uid, ids, context=context):
#            result[emp.id] = 10000
        return result
    
    def _cal_installment(self, cr, uid, ids, name, arg, context={}):
        result={}
        loan_data = self.pool.get('loan.management').browse(cr,uid,ids)
        for loan in loan_data:
#            print loan.loansum
#            print loan.installment
            xxx = loan.loansum/loan.installment
            result[loan.id] = xxx
        return result
    
    def _cal_residu(self,cr,uid,ids,name,arg,context={}):
        result={}
        loan_data = self.pool.get('loan.installment').browse(cr,uid,ids)
        loan_residu = loan_data.search(cr, uid, [('state_id', '=', 'unpaid')])
        if loan_data :
            residu += loan_residu
        
        print "YYYYYYYYYYY", residu
        
        return result
#            
    
    def _compute_board_amount(self, cr, uid, loan, i
                              , residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids
                              , total_days, depreciation_date, context=None):
        #by default amount = 0
        amount = 0
        if i == undone_dotation_number:
            amount = residual_amount
        else:
            
            amount = amount_to_depr / (undone_dotation_number - len(posted_depreciation_line_ids))
            amount = amount_to_depr / loan.installment
            days = total_days - float(depreciation_date.strftime('%j'))
            if i == 1:
                amount = (amount_to_depr / loan.installment) / total_days * days
            elif i == undone_dotation_number:
                amount = (amount_to_depr / loan.installment) / total_days * (total_days - days)
#            if loan.prorata:
#                amount = amount_to_depr / loan.method_number
#                days = total_days - float(depreciation_date.strftime('%j'))
#                if i == 1:
#                    amount = (amount_to_depr / loan.method_number) / total_days * days
#                elif i == undone_dotation_number:
#                    amount = (amount_to_depr / loan.method_number) / total_days * (total_days - days)
           
        return amount
    
    
    def _compute_board_undone_dotation_nb(self, cr, uid, loan, payment_date, total_days, context=None):
        undone_dotation_number = loan.installment

#        while payment_date <= end_date:
#            payment_date = (datetime(payment_date.year, payment_date.month, payment_date.day) + relativedelta(months=+loan.method_period))
#            undone_dotation_number += 1
        return undone_dotation_number
    
    def compute_installment(self, cr, uid, ids, context=None):
        installment_lin_obj = self.pool.get('loan.installment')
        for loan in self.browse(cr, uid, ids, context=context):
#            if loan.value_residual == 0.0:
#                continue
            posted_depreciation_line_ids = installment_lin_obj.search(cr, uid, [('loan_id', '=', loan.id), ('move_check', '=', True)])
            old_loan_line_ids = installment_lin_obj.search(cr, uid, [('loan_id', '=', loan.id), ('move_id', '=', False)])
            if old_loan_line_ids:
                installment_lin_obj.unlink(cr, uid, old_loan_line_ids, context=context)

            amount_to_depr = residual_amount = loan.loansum
                # depreciation_date = 1st January of purchase year
            loan_date = datetime.strptime(loan.loandate, '%Y-%m-%d')
            payment_date = datetime(loan_date.year, loan_date.month, loan_date.day)
            day = payment_date.day
            month = payment_date.month
            year = payment_date.year
            total_days = (year % 4) and 365 or 366

            undone_dotation_number = self._compute_board_undone_dotation_nb(cr, uid, loan, payment_date, total_days, context=context)
            print "********************",len(posted_depreciation_line_ids), undone_dotation_number
            for x in range(len(posted_depreciation_line_ids), int(undone_dotation_number)):
                i = x + 1
                amount = loan.installment_amount #self._compute_board_amount(cr, uid, loan, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, payment_date, context=context)
                residual_amount -= amount
                vals = {
                     'amount': amount,
                     'loan_id': loan.id,
                     'sequence': i,
                     'name': str(loan.id) +'/' + str(i),
                     'loan_value': residual_amount,
                     'payment_value': (loan.loansum) - (residual_amount + amount),
                     'Payment_date': payment_date.strftime('%Y-%m-%d'),
                }
                installment_lin_obj.create(cr, uid, vals, context=context)
                # Considering Depr. Period as months
                payment_date = (datetime(year, month, day) + relativedelta(months=+1))
                day = payment_date.day
                month = payment_date.month
                year = payment_date.year
        return True
    
    
    def validate(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {
            'state':'open'
        }, context)

    def set_to_close(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'close'}, context=context)

    def set_to_draft(self, cr, uid, ids, context=None):
#        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)
        return True;

    
    
    def onchange_company_id(self, cr, uid, ids, company_id=False, context=None):
        val = {}
        if company_id:
            company = self.pool.get('res.company').browse(cr, uid, company_id, context=context)
            if company.currency_id.company_id and company.currency_id.company_id.id != company_id:
                val['currency_id'] = False
            else:
                val['currency_id'] = company.currency_id.id
        return {'value': val}
    
    
 
    
    _columns = {
                'name':fields.char('Name', required=True, size=64),
                #'account_move_line_ids': fields.one2many('account.move.line', 'loan_id', 'Entries', readonly=True, states={'draft':[('readonly',False)]}),
                'employee_id':fields.many2one('hr.employee', 'Employee', required=True, ondelete="cascade"),   
                'loansum':fields.float("Loan Sum", required=True),
                'loandate':fields.date("date", required=True),
                'paymentmethode':fields.selection([('salaries_discount','Salaries Discount'),('directcash','Direct Cash')], 'Payment Methode',  required=True, help="this is the methode of how the loan is paid"),
                'installment': fields.float("Installment"),
                'installment_amount' : fields.function(_cal_installment, method=True, type='integer', string='Installment Amount'),
                'total_paid' : fields.function(_cal_payment, method=True, type='integer', string='Total Paid'),
                'residu':fields.function(_cal_residu, method=True,type='float', string='Residu'),
                'account_id': fields.many2one('loan.account', 'Loan Account', required=True, change_default=True, readonly=True, states={'draft':[('readonly',False)]}),
                'installment_ids' : fields.one2many('loan.installment','loan_id', 'loan id', readonly=True, states={'draft':[('readonly',False)],'open':[('readonly',False)]}),
                'history_ids': fields.one2many('loan.history', 'loan_id', 'History', readonly=True),
                'currency_id': fields.many2one('res.currency','Currency',),
                'company_id': fields.many2one('res.company', 'Company', required=True, states={'draft':[('readonly',False)]}),
                'state': fields.selection([('draft','Draft'),('verify','Verify'),('agree','Agree'),('open','Running'),('close','Close')], 'State', required=True,
                                  help="When a loan is execute, the state is 'Draft'.\n" \
                                       "If the loan is confirmed, the state goes in 'Running' and the payment lines can be posted in the accounting.\n" \
                                       "You can manually close an loan when the payment is over. If the last line of depreciation is posted, the loan automatically goes in that state."),
                'user_verify_id': fields.integer('User Who Verify'),
                'user_agree_id' : fields.integer('user Who Agree'),
                'verify_date':fields.date("date verify"),
                'agree_date' :fields.date("date agree"),

                }
    
    _defaults = {
#        'code': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'account.asset.code'),
        'loandate': lambda obj, cr, uid, context: time.strftime('%Y-%m-%d'),
#        'active': True,
        'state': 'draft',
#        'method': 'linear',
#        'method_number': 5,
#        'method_time': 'number',
#        'method_period': 12,
#        'method_progress_factor': 0.3,
        'currency_id': lambda self,cr,uid,c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.currency_id.id,
        'company_id': lambda self, cr, uid, context: self.pool.get('res.company')._company_default_get(cr, uid, 'loan.management',context=context),
    }
    
    def onchange_name_id(self,cr,uid,ids,employee_id):
        res = {'value':{}}
        if employee_id:
            res['value']={'name':employee_id}
        return res
    
    def workflow_action_Verifikasi(self,cr,uid,ids,contex=None):
        for id in ids:
            self.write(cr,uid,[id],{'state':'verify'})
            self.write(cr,uid,[id],{'user_verify_id':uid})
            self.write(cr,uid,[id],{'verify_date':time.strftime('%Y-%m-%d')})
        return True
    
    def workflow_action_Setuju(self,cr,uid,ids,contex=None):
        for id in ids:
            self.write(cr,uid,[id],{'state':'agree'})
            self.write(cr,uid,[id],{'user_agree_id':uid})
            self.write(cr,uid,[id],{'agree_date':time.strftime('%Y-%m-%d')})
        return True
    
    def workflow_action_Cairkan(self,cr,uid,ids,contex=None):
        for id in ids:
            self.write(cr,uid,[id],{'state':'open'})
        self._cairkan(cr, uid, ids, contex)
        return True
    
    def workflow_action_Batalkan(self,cr,uid,ids,contex=None):
        for id in ids:
            self.write(cr,uid,[id],{'state':'cancel'})
        return True
            
    
#     def _cairkan(self,cr,uid,ids,context=None):
#         can_close = False
#         if context is None:
#             context = {}
#         loan_obj = self.pool.get('loan.management')
#         period_obj = self.pool.get('account.period')
#         move_obj = self.pool.get('account.move')
#         move_line_obj = self.pool.get('account.move.line')
#         currency_obj = self.pool.get('res.currency')
#         created_move_ids = []
#         for line in self.browse(cr,uid, ids, context=context):
# #            if currency_obj.is_zero(cr,uid, line.currency_id, line.loan_value):
# #                can_close = True
#             payment_date = line.loandate or time.strftime('%Y-%m-%d')
#             period_ids = period_obj.find(cr,uid,payment_date,context=context)
#             company_currency = line.company_id.currency_id.id
#             current_currency = line.currency_id.id
#             context.update({'date':payment_date})
#             amount = currency_obj.compute(cr, uid, current_currency, company_currency, line.loansum)
# #            amount = line.amount
#             sign = line.account_id.journal_id.type = 'Cash' and 1 or -1
#             loan_name = line.employee_id
#             reference = line.name
#             move_vals={
#                     'name':loan_name,
#                     'date':payment_date,
#                     'ref': reference,
#                     'period_id':period_ids and period_ids[0] or False,
#                     'journal_id':line.account_id.journal_id.id,
#                     }
#             move_id = move_obj.create(cr,uid,move_vals,context=context)
#             journal_id=line.account_id.journal_id.id
#             employee_id = line.employee_id.id
#             move_line_obj.create(cr, uid, {
#                 'name': loan_name,
#                 'ref': reference,
#                 'move_id': move_id,
#                 'account_id': line.account_id.account_loan_id.id,
#                 'debit': 0.0,
#                 'credit': amount,
#                 'period_id': period_ids and period_ids[0] or False,
#                 'journal_id': journal_id,
#                 'partner_id': employee_id,
#                 'currency_id': company_currency <> current_currency and  current_currency or False,
#                 'amount_currency': company_currency <> current_currency and - sign * line.amount or 0.0,
#                 'date': payment_date,
#             })
#             move_line_obj.create(cr, uid, {
#                 'name': loan_name,
#                 'ref': reference,
#                 'move_id': move_id,
#                 'account_id': line.account_id.account_payment_id.id,
#                 'credit': 0.0,
#                 'debit': amount,
#                 'period_id': period_ids and period_ids[0] or False,
#                 'journal_id': journal_id,
#                 'partner_id': employee_id,
#                 'currency_id': company_currency <> current_currency and  current_currency or False,
#                 'amount_currency': company_currency <> current_currency and sign * line.amount or 0.0,
#                 'analytic_account_id': line.account_id.account_analytic_id.id,
#                 'date': payment_date,
#                 'loan_id': line.id
#             })
#             self.write(cr, uid, line.id, {'move_id': move_id}, context=context)
#             created_move_ids.append(move_id)
# #            if can_close:
# #                loan_obj.write(cr, uid, [line.asset_id.id], {'state': 'close'}, context=context)
#         return created_move_ids
            
   
            


#    def onchange_account_id(self, cr, uid, ids, category_id, context=None):
#        res = {'value':{}}
#        loan_categ_obj = self.pool.get('loan.account')
#        if category_id:
#            account_obj = loan_categ_obj.browse(cr, uid, category_id, context=context)
#            res['value'] = {
#                            'method': category_obj.method,
#                            'method_number': category_obj.method_number,
#                            'method_time': category_obj.method_time,
#                            'method_period': category_obj.method_period,
#                            'method_progress_factor': category_obj.method_progress_factor,
#                            'method_end': category_obj.method_end,
#                            'prorata': category_obj.prorata,
#            }
#        return res



loan_management()


class loan_installment(osv.osv):
    _name = "loan.installment"
    _description = "loan installment"
    
    def _get_move_check(self, cr, uid, ids, name, args, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = bool(line.move_id)
        return res
    
    _columns = {
                'name': fields.char('Loan Name', size=64, required=True, select=1),
                'loan_id':fields.many2one('loan.management', 'Loan ID', required=True, ondelete="cascade"),
                'parent_state': fields.related('loan_id', 'state', type='char', string='State of Loan'),
                'sequence': fields.integer('Sequence of the payment', required=True),
                'amount': fields.float('Payment Amount', required=True),
                'loan_value': fields.float('Amount to paid', required=True),
                'payment_value': fields.float('Accumulated Payment', required=True),
                'Payment_date': fields.char('Payment Date', size=64, select=1),
                'move_id': fields.many2one('account.move', 'Loan Payment Entry'),
                'move_check': fields.function(_get_move_check, method=True, type='boolean', string='Posted', store=True)
                }
    def create_move(self, cr, uid, ids, context=None):
        print "xxxxxxxxxxxxxxx        "
        can_close = False
        if context is None:
            context = {}
        loan_obj = self.pool.get('loan.management')
        period_obj = self.pool.get('account.period')
        move_obj = self.pool.get('account.move')
        move_line_obj = self.pool.get('account.move.line')
        currency_obj = self.pool.get('res.currency')
        created_move_ids = []
        for line in self.browse(cr,uid, ids, context=context):
            if currency_obj.is_zero(cr,uid, line.loan_id.currency_id, line.loan_value):
                can_close = True
            payment_date = line.loan_id.loandate or time.strftime('%Y-%m-%d')
            period_ids = period_obj.find(cr,uid,payment_date,context=context)
            company_currency = line.loan_id.company_id.currency_id.id
            current_currency = line.loan_id.currency_id.id
            context.update({'date':payment_date})
            amount = currency_obj.compute(cr, uid, current_currency, company_currency, line.amount)
#            amount = line.amount
            sign = line.loan_id.account_id.journal_id.type = 'cash' and 1 or -1
            loan_name = line.loan_id.employee_id
            reference = line.name
            move_vals={
                    'name':loan_name,
                    'date':payment_date,
                    'ref': reference,
                    'period_id':period_ids and period_ids[0] or False,
                    'journal_id':line.loan_id.account_id.journal_id.id,
                    }
            print "move_vals", move_vals
            move_id = move_obj.create(cr,uid,move_vals,context=context)
            journal_id=line.loan_id.account_id.journal_id.id
            employee_id = line.loan_id.employee_id.id
            move_line_obj.create(cr, uid, {
                'name': loan_name,
                'ref': reference,
                'move_id': move_id,
                'account_id': line.loan_id.account_id.account_loan_id.id,
                'debit': 0.0,
                'credit': amount,
                'period_id': period_ids and period_ids[0] or False,
                'journal_id': journal_id,
                'partner_id': employee_id,
                'currency_id': company_currency <> current_currency and  current_currency or False,
                'amount_currency': company_currency <> current_currency and - sign * line.amount or 0.0,
                'date': payment_date,
            })
            move_line_obj.create(cr, uid, {
                'name': loan_name,
                'ref': reference,
                'move_id': move_id,
                'account_id': line.loan_id.account_id.account_payment_id.id,
                'credit': 0.0,
                'debit': amount,
                'period_id': period_ids and period_ids[0] or False,
                'journal_id': journal_id,
                'partner_id': employee_id,
                'currency_id': company_currency <> current_currency and  current_currency or False,
                'amount_currency': company_currency <> current_currency and sign * line.amount or 0.0,
                'analytic_account_id': line.loan_id.account_id.account_analytic_id.id,
                'date': payment_date,
                'loan_id': line.loan_id.id
            })
            self.write(cr, uid, line.id, {'move_id': move_id}, context=context)
            created_move_ids.append(move_id)
            if can_close:
                loan_obj.write(cr, uid, [line.asset_id.id], {'state': 'close'}, context=context)
        return created_move_ids
            
            
    
loan_installment()


class hr_employee(osv.osv):
    _inherit = "hr.employee"
    _columns = {
                'loan_ids' : fields.one2many('loan.management','employee_id','Loan'),
                }
hr_employee()


# class account_move_line(osv.osv):
#     _inherit = 'account.move.line'
#     _columns = {
#         'loan_id': fields.many2one('loan.management', 'Loan'),
#         'l_entry_ids': fields.one2many('account.move.line', 'loan_id', 'Entries', readonly=True, states={'draft':[('readonly',False)]}),
# 
#     }
# account_move_line() 



class loan_history(osv.osv):
    _name = "loan.history"
    _description = "describe payment account of loan"
    _columns = {
                'name': fields.char('History name', size=64, select=1),
                'user_id': fields.many2one('res.users', 'User', required=True),
                'date': fields.date('Date', required=True),
                'loan_id': fields.many2one('account.asset.asset', 'Asset', required=True),
                'method_number': fields.integer('Number of Installment'),
                'method_period': fields.integer('Period Length', help="Time in month between two depreciations"),
                'note': fields.text('Note'),
                }
    _default = {
                'date' : lambda *args: time.strftime('%y-%m-%d')
                }

loan_history()



