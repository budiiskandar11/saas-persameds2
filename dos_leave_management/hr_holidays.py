import datetime
import math
import time
from operator import attrgetter

from openerp.exceptions import Warning
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import workflow

class hr_holidays_propose(osv.osv):
    _name = 'hr.holidays.propose'
    #_inherit = ['mail.thread', 'ir.needaction_mixin']
    
    def _compute_total_leave(self, cr, uid, ids, name, args, context=None):
        res = {}
        if not context: context={}
        total_leave = 0.0
        
        for leave in self.browse(cr, uid, ids, context=context):
            for line in leave.holiday_line:
                total_leave += line.number_of_days_temp
            res[leave.id] = { 'total_request_leave'  : total_leave}
        return res
    
    def _proposed_to(self, cr, uid, ids, name, args, context=None):
        print "proposed_to-------------------->>"
        res = {}
        if not context: context={}
        proposed_to = False
        employee_obj = self.pool.get('hr.employee')
        for leave in self.browse(cr, uid, ids, context=context):
            if leave.employee_id.leave_job_approval:
                print "leave.employee_id.leave_job_approval.name", leave.employee_id.leave_job_approval.name
                search_leave_approval = employee_obj.search(cr, uid, [('job_id','=', leave.employee_id.leave_job_approval.id)])
                
                print "search_leave_approval", search_leave_approval
                
                if search_leave_approval:
                    print "proposed_to", employee_obj.browse(cr, uid, search_leave_approval)[0].name
                    proposed_to = employee_obj.browse(cr, uid, search_leave_approval)[0].id
                else:
                    proposed_to = leave.department_id.manager_id.id 
            else:
                proposed_to = leave.department_id.manager_id.id
            res[leave.id] = { 'proposed_to_temp'  : proposed_to}
            if ids:
                self.write(cr, uid, ids, {'proposed_to_temp' : proposed_to})
        return res
    
    def _leave_remaining(self, cr, uid, ids, name, args, context=None):
        print "########_leave_remaining#########################"
        res = {}
        if not context: context={}
        proposed_to = False
        
        for leave in self.browse(cr, uid, ids, context=context):
            print "XXXXXXXXXXXX123", leave.holiday_status_id.id, leave.employee_id.id
            cr.execute("select SUM(number_of_days) from hr_holidays where employee_id = %s and holiday_status_id = %s and state = 'validate'", (leave.employee_id.id, leave.holiday_status_id.id,))
            leave_remaining = cr.fetchone()[0]
            
            res[leave.id] = { 'leave_remaining'  : leave_remaining}
        return res
    
    def _user_login_id(self, cr, uid, ids, name, args, context=None):
        
        res = {}
        if not context: context={}
        user_login = False
        for leave in self.browse(cr, uid, ids, context=context):
            user_login = uid
            res[leave.id] = { 'user_login_id'  : user_login}
            
        return res
        
    _columns = {
            'name': fields.char('Description', size=64),
            'state': fields.selection([('draft', 'To Submit'), ('cancel', 'Cancelled'),('confirm', 'To Approve'), ('refuse', 'Refused'), ('validate1', 'Second Approval'), ('validate', 'Approved')],
            'Status', readonly=True, track_visibility='onchange', copy=False,
            help='The status is set to \'To Submit\', when a holiday request is created.\
            \nThe status is \'To Approve\', when holiday request is confirmed by user.\
            \nThe status is \'Refused\', when holiday request is refused by manager.\
            \nThe status is \'Approved\', when holiday request is approved by manager.'),
            'user_id':fields.related('employee_id', 'user_id', type='many2one', relation='res.users', string='User', store=True),
            
            'employee_id': fields.many2one('hr.employee', "Employee", select=True,),
            'department_id':fields.related('employee_id', 'department_id', string='Department', type='many2one', relation='hr.department', readonly=True, store=True),
            
            #'type': fields.selection([('remove','Leave Request'),('add','Allocation Request')], 'Request Type', select=True),
            #'leave_type': fields.selection([('annual','Annual Leave'),('bit','BIT')], 'Request Type', select=True),
            'holiday_status_id': fields.many2one("hr.holidays.status", "Leave Type", required=True,readonly=True, states={'draft':[('readonly',False)], 'confirm':[('readonly',False)]}),
            
            'reason'           : fields.selection([('nikah','Pernikahan karyawan'),
                                                        ('nikah_anak','Pernikahan anak'),
                                                        ('khitanan','Khitanan anak'),
                                                        ('babtis','Babtisan anak'),
                                                        ('natalitas','Istri melahirkan/keguguran'),
                                                        ('mortalitas','Sanak keluarga meninggal'),
                                                        ('mortalitas_serumah','Keluarga serumah meninggal'),
                                                        ('sakit','Sakit'),
                                                        ('sakit_haid','Sakit haid'),
                                                        ('keluar','Keluar perusahaan'),
                                                        ('tugas_negara','Tugas negara'),
                                                        ('haji','Naik Haji Karyawan'),
                                                        ('no_pay','Ijin tanpa upah'),], 'Alasan Ijin'),
            
            
            'available_leave' : fields.related('holiday_status_id', 'remaining_leaves', type='float', relation='hr.holidays.status', string='Available'),
            
            'total_request_leave' : fields.function(_compute_total_leave, method=True, multi="all", type='float', string='Total Leave Request', digits=(16, 0)),
            
            'holiday_line' : fields.one2many('hr.holidays', 'hr_holidays_propose_id', 'Holiday Line'),

            'delegate_employee_id': fields.many2one('hr.employee', "Employee", select=True,),
            'delegate_department_id':fields.related('delegate_employee_id', 'department_id', string='Department', type='many2one', relation='hr.department', readonly=True, store=True),
            
            'proposed_to_temp'  : fields.function(_proposed_to, method=True, store=False, multi="proposed", type='many2one', relation='hr.employee', string='Proposed to'),
            'proposed_to'       : fields.many2one('hr.employee', "Proposed to", select=True,),
            
            'leave_remaining'  : fields.function(_leave_remaining, method=True, store=False, multi="leave_remaining", type='integer', string='Leave Remaining'),
            #'user_login_id' : fields.function(_user_login_id, method=True, store=False, multi="user_login_id", type='many2one', relation='res.users', string='User Login'),
                }
    
    def create_bit_payment(self, cr, uid, ids, val, context=None):
        print "################################"
        #raise Warning(_("You need 5 days for propose BIT Leave"))
        bit_payment_obj = self.pool.get('bit.payment')
        ###
        cr.execute("select id from account_period where date_start <= %s and date_stop >= %s", (val.holiday_line[0].date_from, val.holiday_line[0].date_from))
        period_id = cr.fetchone()[0]
        ###
        bit = {
               'name'       : "BIT - " + val.name,
               'leave_id'   : val.id,
               'create_date': val.holiday_line[0].date_from,
               'percentage' : 100,
               'effective_period' : period_id,
               'employee_id' : val.employee_id.id,  
               }
        
        bit_payment_obj.create(cr, uid, bit)
        
        return True
    
    def confirm(self, cr, uid, ids, context=None):
        print "confirm>>>>>>>>>>>>"
        for val in self.browse(cr, uid, ids, context=None):
            total_request_leave = val.total_request_leave
            print "MMMMMMMMM", total_request_leave
            #if val.leave_type == 'bit' and total_request_leave <> 5:
            #    raise Warning(_("You need 5 days for propose BIT Leave"))
            
            for line in val.holiday_line:
                self.pool.get('hr.holidays').write(cr, uid, line.id, {'employee_id'         : val.employee_id.id, 
                                                                      'department_id'       : val.department_id.id,
                                                                      'holiday_status_id'  : val.holiday_status_id.id})
                workflow.trg_validate(uid, 'hr.holidays', line.id, 'confirm', cr)
        
        template_id = self.pool.get('email.template').search(cr, uid, [('model_id','=','hr.holidays.propose')])[0]
        if template_id:
            print "XXXXXXXXXXXXX", template_id, ids[0]    
            self.pool.get('email.template').send_mail(cr, uid, template_id, ids[0],True, context=context)
        
        self.write(cr, uid, ids, {
                                  'proposed_to' :  val.proposed_to_temp.id,
                                  'state'       : 'confirm',
                                  })
        return True
    
    def validate(self, cr, uid, ids, context=None):
        print "approve>>>>>>>>>>>>"
        for val in self.browse(cr, uid, ids, context=None):
            for line in val.holiday_line:
                workflow.trg_validate(uid, 'hr.holidays', line.id, 'validate', cr)
        
        if val.holiday_status_id.name == 'Cuti BIT':
            print "-------------------------------"
            self.create_bit_payment(cr, uid, ids, val)
        self.write(cr, uid, ids, {'state' : 'validate1'})
        return True
    
    def second_validate(self, cr, uid, ids, context=None):
        print "approve>>>>>>>>>>>>"
        for val in self.browse(cr, uid, ids, context=None):
            for line in val.holiday_line:
                workflow.trg_validate(uid, 'hr.holidays', line.id, 'second_validate', cr)
        
        self.write(cr, uid, ids, {'state' : 'validate'})
        return True
    
    def reset(self, cr, uid, ids, context=None):
        print "reset>>>>>>>>>>>>"
        for val in self.browse(cr, uid, ids, context=None):
            for line in val.holiday_line:
                workflow.trg_validate(uid, 'hr.holidays', line.id, 'reset', cr)
        self.write(cr, uid, ids, {'state' : 'draft'})
        return True
    
    def refuse(self, cr, uid, ids, context=None):
        print "reset>>>>>>>>>>>>"
        for val in self.browse(cr, uid, ids, context=None):
            #if val.state == '':
                
            for line in val.holiday_line:
                workflow.trg_validate(uid, 'hr.holidays', line.id, 'refuse', cr)
        self.write(cr, uid, ids, {'state' : 'refuse'})
        return True
        
    _defaults = {
            'state'         : 'draft',
            'employee_id'   : lambda self, cr, uid, c: self.pool.get('hr.employee')._employee_default_get(cr, uid, 'hr.holidays.propose', context=c),
                 }
    
hr_holidays_propose()

class hr_holidays(osv.osv):
    _inherit = 'hr.holidays'
    
#     def _user_left_days(self, cr, uid, ids, name, args, context=None):
#         print "_user_left_days"
#         res = {}
#         if not context: context={}
#         res = dict.fromkeys(ids, {'available_leave': 0.0, 'remaining_leave': 0.0})
# 
#         for leave in self.browse(cr, uid, ids, context=context):
#             if leave:
#                 employee_id = leave.employee_id.id
# 
#                 holidays_ids = self.search(cr,uid,[('employee_id','=',employee_id)])
# 
#                 holidays_id = self.browse(cr,uid,holidays_ids)
#                 total_days = 0.0
#                 for i in holidays_id:
#                     if i.type == 'add' and i.state == 'validate':
#                         total_days += i.number_of_days_temp
#                     elif i.type == 'remove' and i.state == 'validate':
#                         total_days -= i.number_of_days_temp
# 
#                 remaining = total_days - leave.number_of_days_temp
#                 res[leave.id] = { 'available_leave'  : total_days, 'remaining_leave' : remaining }
#             else:
#                 res[leave.id] = { 'available_leave'  : 0.0, 'remaining_leave' : 0.0}
#         return res
    
    _columns = {
            'hr_holidays_propose_id': fields.many2one('hr.holidays.propose', 'Holidays Propose',),
            
            #'available_leave': fields.function(_user_left_days, method=True, multi="all", store=True, type='float', string='Available Leave', digits=(16, 2)),
            #'remaining_leave': fields.function(_user_left_days, method=True, multi="all", store=True, type='float', string='Remaining Leave', digits=(16, 2)),
                }
    
    _defaults = {
            'holiday_status_id' : 1,
                 }
    
    _sql_constraints = [
        ('type_value', "CHECK( (holiday_type='employee' AND employee_id IS NOT NULL) or (holiday_type='category' AND category_id IS NOT NULL))", 
         "The employee or employee category of this request is missing. Please make sure that your user login is linked to an employee."),
#         ('date_check2', "CHECK ( (type='add') OR (date_from < date_to))", "The start date must be anterior to the end date."),
        ('date_check', "CHECK ( number_of_days_temp >= 0 )", "The number of days must be greater than 0."),
            ]
    
    def _get_number_of_days(self, date_from, date_to):
        """Returns a float equals to the timedelta between two dates given as string."""

        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        ###DIubah jadi Date###
        from_dt = datetime.datetime.strptime(date_from, DATETIME_FORMAT).date()
        to_dt = datetime.datetime.strptime(date_to, DATETIME_FORMAT).date()
        ######################
        print "from_dt----------->>", from_dt
        print "to_dt----------->>", to_dt
        
        timedelta = to_dt - from_dt
        print "timedelta--------------->>", timedelta
        print "timedelta.days---------->>", timedelta.days
        ###Diganti###
        #diff_day = timedelta.days + float(timedelta.seconds) / 86400
        diff_day= timedelta.days
        #############
        print "diff_day----------->>", diff_day
        return diff_day
    
hr_holidays()