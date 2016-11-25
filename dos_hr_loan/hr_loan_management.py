import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from openerp import netsvc
from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.tools.safe_eval import safe_eval as eval

class loan_management(osv.osv):
    _name = 'loan.management'
    _description = "loan for employeee"
    
    def _cal_payment(self, cr, uid, ids, name, arg, context={}):
        result={}
        for loan in self.browse(cr,uid,ids):
            
            result[loan.id] = 0

        return result
    
    def _cal_installment(self, cr, uid, ids, name, arg, context={}):
        result={}
        loan_data = self.pool.get('loan.management').browse(cr,uid,ids)
        for loan in loan_data:

            xxx = loan.loansum/loan.installment
            result[loan.id] = xxx
        return result
    
    def _cal_residu(self,cr,uid,ids,name,arg,context={}):
        result={}
#         loan_data = self.pool.get('loan.installment').browse(cr,uid,ids)
#         for loans in self.browse(cr,uid,ids, context=context):
# 
#             yyy += loan_data.search(cr, uid, [('state_id', '=', 'unpaid')])
#             result[residu] = yyy
        return result
    
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
         
        return amount
    
    def onchange_name_id(self,cr,uid,ids,employee_id):
        res = {'value':{}}
        if employee_id:
            res['value']={'name':employee_id}
        return res
    
    def onchange_company_id(self, cr, uid, ids, company_id=False, context=None):
        val = {}
        if company_id:
            company = self.pool.get('res.company').browse(cr, uid, company_id, context=context)
            if company.currency_id.company_id and company.currency_id.company_id.id != company_id:
                val['currency_id'] = False
            else:
                val['currency_id'] = company.currency_id.id
        return {'value': val}
    
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
            posted_depreciation_line_ids = installment_lin_obj.search(cr, uid, [('loan_id', '=', loan.id)])
            old_loan_line_ids = installment_lin_obj.search(cr, uid, [('loan_id', '=', loan.id)])
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
    
    
    
    
    _columns = {
                'name':fields.char('Name', required=True, size=64),
                'employee_id':fields.many2one('hr.employee', 'Employee', required=True, ondelete="cascade"),   
                'loansum':fields.float("Loan Sum", required=True),
                'loandate':fields.date("date", required=True),
                'paymentmethode':fields.selection([('salaries_discount','Salaries Discount'),('directcash','Direct Cash')], 'Payment Methode',  required=True, help="this is the methode of how the loan is paid"),
                'installment': fields.float("Installment"),
                'installment_amount' : fields.function(_cal_installment, method=True, type='integer', string='Installment Amount'),
                'total_paid' : fields.function(_cal_payment, method=True, type='integer', string='Total Paid'),
                'residu':fields.function(_cal_residu, method=True,type='float', string='Residu'),
                #'account_id': fields.many2one('loan.account', 'Loan Account', required=True, change_default=True, readonly=True, states={'draft':[('readonly',False)]}),
                'installment_ids' : fields.one2many('loan.installment','loan_id', 'loan id', readonly=True, states={'draft':[('readonly',False)],'open':[('readonly',False)]}),
               # 'history_ids': fields.one2many('loan.history', 'loan_id', 'History', readonly=True),
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

        'loandate': lambda obj, cr, uid, context: time.strftime('%Y-%m-%d'),

        'state': 'draft',
        'currency_id': lambda self,cr,uid,c: self.pool.get('res.users').browse(cr, uid, uid, c).company_id.currency_id.id,
        'company_id': lambda self, cr, uid, context: self.pool.get('res.company')._company_default_get(cr, uid, 'loan.management',context=context),
    }

loan_management()


class loan_installment(osv.osv):
    _name = "loan.installment"
    _description = "loan installment"
    
    def paid (self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {
            'state_id':'paid'
        }, context)
        
        
    _columns = {
                'name': fields.char('Loan Name', size=64, required=True, select=1),
                'loan_id':fields.many2one('loan.management', 'Loan ID', required=True, ondelete="cascade"),
                'parent_state': fields.related('loan_id', 'state', type='char', string='State of Loan'),
                'sequence': fields.integer('Sequence of the payment', required=True),
                'amount': fields.float('Payment Amount', required=True),
                'loan_value': fields.float('Amount to paid', required=True),
                'payment_value': fields.float('Accumulated Payment', required=True),
                'Payment_date': fields.char('Payment Date', size=64, select=1),
                'state_id'  : fields.selection([('paid','Paid'),('unpaid','Unpaid')],"State"),
#                 'move_id': fields.many2one('account.move', 'Loan Payment Entry'),
#                 'move_check': fields.function(_get_move_check, method=True, type='boolean', string='Posted', store=True)
                }
    _defaults = {
        'state_id': 'unpaid',  
        }     
            
    
loan_installment()


class hr_employee(osv.osv):
    _inherit = "hr.employee"
    _columns = {
                'loan_ids' : fields.one2many('loan.management','employee_id','Loan'),
                }
hr_employee()


# 
# class loan_history(osv.osv):
#     _name = "loan.history"
#     _description = "describe payment account of loan"
#     _columns = {
#                 'name': fields.char('History name', size=64, select=1),
#                 'user_id': fields.many2one('res.users', 'User', required=True),
#                 'date': fields.date('Date', required=True),
#                 'method_number': fields.integer('Number of Installment'),
#                 'method_period': fields.integer('Period Length', help="Time in month between two depreciations"),
#                 'note': fields.text('Note'),
# #                 }
# #     _default = {
# #                 'date' : lambda *args: time.strftime('%y-%m-%d')
# #                 }
# 
# loan_history()



