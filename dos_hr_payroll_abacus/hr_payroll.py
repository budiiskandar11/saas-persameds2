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

class hr_payslip(osv.osv):
    _inherit = "hr.payslip"
    
    def _overtime(self, cr, uid, ids, name, args, context):
        if not ids: return {}
        
        #bit_payment_obj   = self.pool.get('bit.payment')
        #percentage          = 0.0
        res = {}
        for val in self.browse(cr, uid, ids, context=context):
            ###Check Period###
            #cr.execute("select id from account_period where date_start <= %s and date_stop >= %s and company_id = %s", (val.date_to, val.date_to, val.company_id.id))
            #period_id = cr.fetchone()[0]
            #################
            #bit_search = bit_payment_obj.search(cr, uid, [('employee_id','=',val.employee_id.id),('effective_period','=',period_id),('state','=', 'confirm')])
            
            #for bit in bit_payment_obj.browse(cr, uid, bit_search):
            #    percentage += bit.percentage 
                
            res[val.id] = val.overtime_adjustment
        return res
    
    def _benefit(self, cr, uid, ids, name, args, context):
        if not ids: return {}
        
        benefit_obj   = self.pool.get('hr.benefit')
        
        res = {}
        
        record = {'bonus'       : 0.0,
                  'benefit'     : 0.0,
                  'thr'         : 0.0,
                  'spp'         : 0.0,
                  'insentif'    : 0.0,
                  'gaji13'      : 0.0,
                  'reward'      : 0.0,}
        
        for val in self.browse(cr, uid, ids, context=context):
            ###Check Period###
            cr.execute("select id from account_period where date_start <= %s and date_stop >= %s and company_id = %s", (val.date_to, val.date_to, val.company_id.id))
            period_id = cr.fetchone()[0]
            #################
            for type in ['bonus','benefit','thr','spp','insentif','gaji13','reward']:
                percentage    = 0.0
                correction_search = benefit_obj.search(cr, uid, [('employee_id','=',val.employee_id.id),('effective_period','=',period_id),
                                                                 ('state','=', 'confirm'),('type','=',type)])
                
                for benefit in benefit_obj.browse(cr, uid, correction_search):
                    percentage += benefit.percentage
                
                record.update({type : percentage/100 * val.thp})
                
            res[val.id] = record
            #res[val.id] = { 'benefit' : percentage}
        return res
    
    def _abacus_bhakti(self, cr, uid, ids, name, args, context):
        if not ids: return {}
        
        abacus_bhakti_obj   = self.pool.get('hr.abacus.bhakti')
        percentage          = 0.0
        res = {}
        for val in self.browse(cr, uid, ids, context=context):
            ###Check Period###
            cr.execute("select id from account_period where date_start <= %s and date_stop >= %s and company_id = %s", (val.date_to, val.date_to, val.company_id.id))
            period_id = cr.fetchone()[0]
            #################
            correction_search = abacus_bhakti_obj.search(cr, uid, [('employee_id','=',val.employee_id.id),('effective_period','=',period_id),('state','=', 'confirm')])
            
            for bhakti in abacus_bhakti_obj.browse(cr, uid, correction_search):
                percentage += bhakti.percentage 
                
            res[val.id] = percentage/100 * val.thp
        return res
    
    def _bit(self, cr, uid, ids, name, args, context):
        print "xxxxxxxxxxxBIT"
        if not ids: return {}
        
        bit_payment_obj   = self.pool.get('bit.payment')
        percentage          = 0.0
        res = {}
        for val in self.browse(cr, uid, ids, context=context):
            ###Check Period###
            cr.execute("select id from account_period where date_start <= %s and date_stop >= %s and company_id = %s", (val.date_to, val.date_to, val.company_id.id))
            period_id = cr.fetchone()[0]
            #################
            bit_search = bit_payment_obj.search(cr, uid, [('employee_id','=',val.employee_id.id),('effective_period','=',period_id),('state','=', 'confirm')])
            
            for bit in bit_payment_obj.browse(cr, uid, bit_search):
                percentage += bit.percentage 
                
            res[val.id] = percentage/100 * val.thp
        return res
    
    def _kokara(self, cr, uid, ids, name, args, context):
        if not ids: return {}
        
        kokara_obj      = self.pool.get('hr.kokara')
        kokara_amount   = 0.0
        res = {}
        for val in self.browse(cr, uid, ids, context=context):
            ###Check Period###
            cr.execute("select id from account_period where date_start <= %s and date_stop >= %s and company_id = %s", (val.date_to, val.date_to, val.company_id.id))
            period_id = cr.fetchone()[0]
            #################
            kokara_search = kokara_obj.search(cr, uid, [('employee_id','=',val.employee_id.id),('effective_period','=',period_id),('state','=', 'confirm')])
            
            for kokara in kokara_obj.browse(cr, uid, kokara_search):
                kokara_amount += kokara.amount 
                
            res[val.id] = kokara_amount
        return res
    
    def _correction(self, cr, uid, ids, name, args, context):
        if not ids: return {}
        
        correction_obj      = self.pool.get('hr.payroll.correction')
        correction_amount   = 0.0
        res = {}
        for val in self.browse(cr, uid, ids, context=context):
            ###Check Period###
            cr.execute("select id from account_period where date_start <= %s and date_stop >= %s and company_id = %s", (val.date_to, val.date_to, val.company_id.id))
            period_id = cr.fetchone()[0]
            #################
            correction_search = correction_obj.search(cr, uid, [('employee_id','=',val.employee_id.id),('effective_period','=',period_id),('state','=', 'confirm')])
            
            for correction in correction_obj.browse(cr, uid, correction_search):
                correction_amount += correction.amount 
                
            res[val.id] = correction_amount
        return res
    
    def _allowance_days(self, cr, uid, ids, name, args, context):
        if not ids: return {}
        
        attendance_obj      = self.pool.get('hr.attendance')
        allowance_day       = 0
        attendance_day      = 0
        absence_allowance_day = 0
        res = {}
        for val in self.browse(cr, uid, ids, context=context):
            if val.date_from:
                cr.execute("select count(id) from hr_attendance where day <= %s and day >= %s and employee_id = %s and action = %s", (val.date_to, val.date_from, val.employee_id.id, "sign_in"))
                attendance_day = cr.fetchone()[0]
                
                ###Filter Reason Allowance###
                cr.execute("select id from absence_reason where allowance = True")
                reason_allowance = tuple(map(lambda x: x[0], cr.fetchall()))
                
                print "reason_allowance---------->>", reason_allowance
                
                ###
                cr.execute("select count(id) from hr_absence where date <= %s and date >= %s and employee_id = %s and reason in %s", (val.date_to, val.date_from, val.employee_id.id, reason_allowance))
                absence_allowance_day = cr.fetchone()[0]
                
                print "allowance_day---------->>", allowance_day
                print "absence_day", absence_allowance_day
            
            res[val.id] = attendance_day + absence_allowance_day
        return res
    
    _columns = {
        ###Additional###
        'basic_wage'     : fields.float('Basic Salary', readonly=True),
        'thp'            : fields.float('Take Home Pay', readonly=True),
        
        'bpjs_tk_p'     : fields.float('By Company'),
        'bpjs_tk_k'     : fields.float('By Employee'),
        
        'bpjs_kes_p'      : fields.float('By Company'),
        'bpjs_kes_k'      : fields.float('By Employee'),
        
        'dplk_p'      : fields.float('By Company'),
        'dplk_k'      : fields.float('By Employee'),
        
        'overtime_adjustment' : fields.float("Overtime"),
        'overtime'          : fields.function(_overtime, method=True, type='float', string='Overtime', digits_compute=dp.get_precision('Payroll')),
        'bonus'             : fields.function(_benefit, method=True, type='float', string='Bonus', digits_compute=dp.get_precision('Payroll'),multi='dc'),
        'benefit'           : fields.function(_benefit, method=True, type='float', string='Benefit', digits_compute=dp.get_precision('Payroll'),multi='dc'),
        'thr'               : fields.function(_benefit, method=True, type='float', string='THR', digits_compute=dp.get_precision('Payroll'),multi='dc'),
        'spp'               : fields.function(_benefit, method=True, type='float', string='SPP', digits_compute=dp.get_precision('Payroll'),multi='dc'),
        'insentif'       : fields.function(_benefit, method=True, type='float', string='Insentif', digits_compute=dp.get_precision('Payroll'),multi='dc'),
        'gaji13'         : fields.function(_benefit, method=True, type='float', string='Gaji ke-13', digits_compute=dp.get_precision('Payroll'),multi='dc'),
        'reward'         : fields.function(_benefit, method=True, type='float', string='Reward', digits_compute=dp.get_precision('Payroll'),multi='dc'),
        'bit'         : fields.function(_bit, method=True, type='float', string='BIT', digits_compute=dp.get_precision('Payroll')),
        
        'abacus_bhakti' : fields.function(_abacus_bhakti, method=True, type='float', string='Abacus Bhakti %', digits_compute=dp.get_precision('Payroll'),),
        'correction'    : fields.function(_correction, method=True, type='float', string='Correction', digits_compute=dp.get_precision('Payroll'),),
        'kokara'    : fields.function(_kokara, method=True, type='float', string='Potongan Kokara', digits_compute=dp.get_precision('Payroll'),),
        'allowance_days' : fields.function(_allowance_days, method=True, type='integer', string='Allowances Days', digits_compute=dp.get_precision('Payroll'),),
        #'total': fields.function(_calculate_total, method=True, type='float', string='Total', digits_compute=dp.get_precision('Payroll'),store=True ),
        
        ################
        'state': fields.selection([
            ('draft', 'Draft'),
            ('verify', 'Waiting'),
            ('verify_account','Submit to Accounting'),
            ('done', 'Done'),
            ('cancel', 'Rejected'),
        ], 'State', select=True, readonly=True,
            help='* When the payslip is created the state is \'Draft\'.\
            \n* If the payslip is under verification, the state is \'Waiting\'. \
            \n* If the payslip is need to be posted by accounting, the state is \'Submit to Accounting\'. \
            \n* If the payslip is confirmed then state is set to \'Done\'.\
            \n* When user cancel payslip the state is \'Rejected\'.'),
                }
    
    _defaults = {
        'date_from': lambda *a: time.strftime('%Y-%m-21'),
        'date_to': lambda *a: str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10],
        'state': 'draft',
        'credit_note': False,
        'company_id': lambda self, cr, uid, context: \
                self.pool.get('res.users').browse(cr, uid, uid,
                    context=context).company_id.id,
    }
    
    def onchange_employee_id(self, cr, uid, ids, date_from, date_to, employee_id=False, contract_id=False, context=None):
        empolyee_obj = self.pool.get('hr.employee')
        contract_obj = self.pool.get('hr.contract')
        worked_days_obj = self.pool.get('hr.payslip.worked_days')
        input_obj = self.pool.get('hr.payslip.input')

        if context is None:
            context = {}
        #delete old worked days lines
        old_worked_days_ids = ids and worked_days_obj.search(cr, uid, [('payslip_id', '=', ids[0])], context=context) or False
        if old_worked_days_ids:
            worked_days_obj.unlink(cr, uid, old_worked_days_ids, context=context)

        #delete old input lines
        old_input_ids = ids and input_obj.search(cr, uid, [('payslip_id', '=', ids[0])], context=context) or False
        if old_input_ids:
            input_obj.unlink(cr, uid, old_input_ids, context=context)


        #defaults
        res = {'value':{
                      'line_ids':[],
                      'input_line_ids': [],
                      'worked_days_line_ids': [],
                      #'details_by_salary_head':[], TODO put me back
                      'name':'',
                      'contract_id': False,
                      'struct_id': False,
                      }
            }
        if (not employee_id) or (not date_from) or (not date_to):
            return res
        ttyme = datetime.fromtimestamp(time.mktime(time.strptime(date_to, "%Y-%m-%d")))
        employee_id = empolyee_obj.browse(cr, uid, employee_id, context=context)
        res['value'].update({
                    'name': _('Salary Slip of %s for %s') % (employee_id.name, tools.ustr(ttyme.strftime('%B-%Y'))),
                    'company_id': employee_id.company_id.id
        })

        if not context.get('contract', False):
            #fill with the first contract of the employee
            contract_ids = self.get_contract(cr, uid, employee_id, date_from, date_to, context=context)
        else:
            if contract_id:
                #set the list of contract for which the input have to be filled
                contract_ids = [contract_id]
            else:
                #if we don't give the contract, then the input to fill should be for all current contracts of the employee
                contract_ids = self.get_contract(cr, uid, employee_id, date_from, date_to, context=context)

        if not contract_ids:
            return res
        contract_record = contract_obj.browse(cr, uid, contract_ids[0], context=context)
        res['value'].update({
                    'contract_id': contract_record and contract_record.id or False
        })
        struct_record = contract_record and contract_record.struct_id or False
        if not struct_record:
            return res
        res['value'].update({
                    'struct_id': struct_record.id,
        })
        #computation of the salary input
        worked_days_line_ids = self.get_worked_day_lines(cr, uid, contract_ids, date_from, date_to, context=context)
        input_line_ids = self.get_inputs(cr, uid, contract_ids, date_from, date_to, context=context)
        res['value'].update({
                    'worked_days_line_ids': worked_days_line_ids,
                    'input_line_ids': input_line_ids,
        })
        return res
    
    def compute_sheet(self, cr, uid, ids, context=None):
        print "XXXXXXXXXXXXcompute_sheet"
        slip_line_pool = self.pool.get('hr.payslip.line')
        sequence_obj = self.pool.get('ir.sequence')
        for payslip in self.browse(cr, uid, ids, context=context):
            number = payslip.number or sequence_obj.get(cr, uid, 'salary.slip')
            #delete old payslip lines
            old_slipline_ids = slip_line_pool.search(cr, uid, [('slip_id', '=', payslip.id)], context=context)
#            old_slipline_ids
            if old_slipline_ids:
                slip_line_pool.unlink(cr, uid, old_slipline_ids, context=context)
            if payslip.contract_id:
                #set the list of contract for which the rules have to be applied
                contract_ids = [payslip.contract_id.id]
            else:
                #if we don't give the contract, then the rules to apply should be for all current contracts of the employee
                contract_ids = self.get_contract(cr, uid, payslip.employee_id, payslip.date_from, payslip.date_to, context=context)
            lines = [(0,0,line) for line in self.pool.get('hr.payslip').get_payslip_lines(cr, uid, contract_ids, payslip.id, context=context)]
            
            ###BPJS###
            bpjs_tk_p   = 0.0
            bpjs_tk_k   = 0.0
            bpjs_kes_p  = 0.0
            bpjs_kes_k  = 0.0
            dplk_p      = 0.0
            dplk_k      = 0.0
            
            
            bpjs_tk_obj     = self.pool.get('hr.bpjs.tk')
            bpjs_kes_obj    = self.pool.get('hr.bpjs.kes')
            dplk_obj        = self.pool.get('hr.dplk')
            
            basic_wage      = payslip.contract_id.wage
            thp             = payslip.contract_id.thp
            
            bpjs_tk_search = bpjs_tk_obj.search(cr, uid, [('name','=',payslip.employee_id.id),('state','=','registered')], order='reg_date DESC')
            for bpjs_tk in bpjs_tk_obj.browse(cr, uid, bpjs_tk_search):
                bpjs_tk_p = bpjs_tk.jht_by_company + bpjs_tk.jk_pensiun_company + bpjs_tk.jkk_amount + bpjs_tk.jk_amount
                bpjs_tk_k = bpjs_tk.jht_by_employee + bpjs_tk.jk_pensiun_employee  
            
            bpjs_kes_search = bpjs_kes_obj.search(cr, uid, [('name','=',payslip.employee_id.id),('state','=','registered')], order='reg_date DESC')
            for bpjs_kes in bpjs_kes_obj.browse(cr, uid, bpjs_kes_search):
                bpjs_kes_p = bpjs_kes.jpk_by_company 
                bpjs_kes_k = bpjs_kes.jpk_by_employee
                
            dplk_obj_search = dplk_obj.search(cr, uid, [('name','=',payslip.employee_id.id),('state','=','registered')], order='reg_date DESC')
            for dplk in dplk_obj.browse(cr, uid, dplk_obj_search):
                dplk_p = dplk.dplk_by_company 
                dplk_k = dplk.dplk_by_employee
            
            
            self.write(cr, uid, [payslip.id], {
                                               'basic_wage' : basic_wage,
                                               'thp'        : thp,
                                               'line_ids'   : lines, 
                                               'number'     : number,
                                               'bpjs_tk_p'  : bpjs_tk_p,
                                               'bpjs_tk_k'  : bpjs_tk_k,
                                               
                                               'bpjs_kes_p'  : bpjs_kes_p,
                                               'bpjs_kes_k'  : bpjs_kes_k,
                                               
                                               'dplk_p'  : dplk_p,
                                               'dplk_k'  : dplk_k,
                                               }, context=context)
        return True
    
    def hr_verify_sheet_1(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'verify_account'}, context=context)
    
    def get_holidays(self,cr,uid,day):
        return self.pool.get('hr.holiday.year').search(cr,uid,[('date','=',day)])
        
    def get_worked_day_lines(self, cr, uid, contract_ids, date_from, date_to, context=None):
      
        """
        @param contract_ids: list of contract id
        @return: returns a list of dict containing the input that should be applied for the given contract between date_from and date_to
        """
        def was_on_leave(employee_id, datetime_day, context=None):
            res = False
            day = datetime_day.strftime("%Y-%m-%d")
            holiday_ids = self.pool.get('hr.holidays').search(cr, uid, [('state','=','validate'),('employee_id','=',employee_id),('type','=','remove'),('date_from','<=',day),('date_to','>=',day)])
            if holiday_ids:
                res = self.pool.get('hr.holidays').browse(cr, uid, holiday_ids, context=context)[0].holiday_status_id.name
            return res

        res = []
        for contract in self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context):
            if not contract.working_hours:
                #fill only if the contract as a working schedule linked
                continue
            
            leaves1 = {}
            day_from = datetime.strptime(date_from,"%Y-%m-%d")
            day_to = datetime.strptime(date_to,"%Y-%m-%d")
##################################################################################################################
            nb_of_days = (day_to - day_from).days + 1
            for day in range(0, nb_of_days):
                currday=(day_from + timedelta(days=day)).strftime("%Y-%m-%d")
                working_hours_on_day = self.pool.get('resource.calendar').working_hours_on_day(cr, uid, contract.working_hours, day_from + timedelta(days=day), context)
                leave_ids=holiday_ids = self.pool.get('hr.holidays').search(cr, uid, [('state','=','validate'),('employee_id','=',contract.employee_id.id),('type','=','remove'),('date_from','<=',currday),('date_to','>=',currday)])
                if leave_ids:
                    leave_data=self.pool.get('hr.holidays').browse(cr,uid,leave_ids[0])
                if working_hours_on_day:
                    #the employee had to work
                    leave_type = was_on_leave(contract.employee_id.id, day_from + timedelta(days=day), context=context)
                    if leave_type:
                        #if he was on leave, fill the leaves dict
    
                        if leave_type in leaves1:
                            leaves1[leave_type]['number_of_days'] += leave_data.number_of_days_temp
                            leaves1[leave_type]['number_of_hours'] += working_hours_on_day
                        else:
                            #print "----------------->",leave_type
                            leaves1[leave_type] = {
                                'name': leave_type,
                                'sequence': 5,
                                'code': leave_type.replace(" ","_"),
                                'number_of_days': leave_data.number_of_days_temp,
                                'number_of_hours': working_hours_on_day,
                                'contract_id': contract.id,
                            }
#                    else:
#                        #add the input vals to tmp (increment if existing)
#                        attendances['number_of_days'] += 1.0
#                        attendances['number_of_hours'] += working_hours_on_day
            leaves1 = [value for key,value in leaves1.items()]
#            res += [attendances] + leaves

##################################################################################################################

#            print "res",res
#            print "atts",attendances
#            print "leaves",leaves
            ##========================================================================================
            ##get hr overtime and latetime
            ##========================================================================================
            
            #compute work days
            #overtime_lines=self.pool.get('hr.attendance.summary.lines').search(cr,uid,[('name','>=',date_from),('name','<=',date_to)])
            query="select a.id from hr_attendance_summary_lines a left join hr_attendance_summary b on a.summary_id=b.id where a.name>='%s' and a.name<='%s' and b.employee_id=%s"%(date_from,date_to,contract.employee_id.id)
            #print "query========>",query
            cr.execute(query)
            overtime_lines=map(lambda x: x[0], cr.fetchall())
            print "count overtime_lines"
            if overtime_lines:
                attendances = {
                 'name': _("Normal Working Days paid at 100%"),
                 'sequence': 1,
                 'code': 'WORK100',
                 'number_of_days': 0.0,
                 'number_of_hours': 0.0,
                 'contract_id': contract.id,
                 }
                extra = {
                 'name': _("HOLIDAYWORK to be Paid"),
                 'sequence': 2,
                 'code': 'HOLIDAYWORK',
                 'number_of_days': 0.0,
                 'number_of_hours': 0.0,
                 'contract_id': contract.id,
                 }
                
                overtimes=self.pool.get('hr.attendance.summary.lines').browse(cr,uid,overtime_lines)
                working_hours_on_day=0
                working_day=0
                extra_day_hours=0
                extra_day=0
                for work in overtimes:
#                    if work.worktime and not work.extra_day:
#                        working_hours_on_day=sum(int(x) * 60 ** i for i,x in enumerate(reversed(work.worktime.split(":"))))
#                        if datetime.strptime(work.worktime,"%H:%M:%S")>datetime.strptime("00:00:00","%H:%M:%S"):
#                            working_day+=1
                    working_day+=1
                    if work.extra_day or self.get_holidays(cr,uid,work.name):
                        extra_day_hours=sum(int(x) * 60 ** i for i,x in enumerate(reversed(work.worktime.split(":"))))
                        if datetime.strptime(work.worktime,"%H:%M:%S")>datetime.strptime("00:00:00","%H:%M:%S"):
                            extra_day+=1
                            
                attendances['number_of_hours']=float(working_hours_on_day)/3600
                attendances['number_of_days']=working_day
                extra['number_of_hours']=float(extra_day_hours)/3600
                extra['number_of_days']=extra_day
                if attendances['number_of_days']>0.0:
                    res.append(attendances)
                    
                if extra['number_of_days']>0.0:
                    res.append(extra)
                
                overtime = {
                 'name': _("Overtime Days paid"),
                 'sequence': 3,
                 'code': 'OVERTIME',
                 'number_of_days': 0.0,
                 'number_of_hours': 0.0,
                 'contract_id': contract.id,
                 }
            
                number_of_hours=0
                hour=0
                number_of_days=0
                
                for overtime_id in overtimes:
                    if overtime_id.overtime:
                        hour=sum(int(x) * 60 ** i for i,x in enumerate(reversed(overtime_id.overtime.split(":"))))
                        number_of_hours+=hour
                        if datetime.strptime(overtime_id.overtime,"%H:%M:%S")>datetime.strptime("00:00:00","%H:%M:%S"):
                            number_of_days+=1
                overtime['number_of_hours']=float(number_of_hours)/3600
                overtime['number_of_days']=number_of_days
                
                hour=0
                number_of_hours=0
                number_of_days=0
                latetimex = {
                 'name': _("Late Days as penalty"),
                 'sequence': 4,
                 'code': 'LATETIME',
                 'number_of_days': 0.0,
                 'number_of_hours': 0.0,
                 'contract_id': contract.id,
                 }
                for latetime in overtimes:
                    if latetime.late_time:
                        hour=sum(int(x) * 60 ** i for i,x in enumerate(reversed(latetime.late_time.split(":"))))
                        if hour > 0:
                            number_of_hours+=hour
                        if datetime.strptime(latetime.late_time,"%H:%M:%S")>datetime.strptime("00:00:00","%H:%M:%S"):
                            number_of_days+=1
                latetimex['number_of_hours']=float(number_of_hours)/3600
                latetimex['number_of_days']=number_of_days
                if overtime['number_of_days']>0.0:
                    res.append(overtime)
                if latetimex['number_of_days']>0.0:
                    res.append(latetimex)
            leaves={}
            queryabs="select a.id from hr_absence_summary_lines a left join hr_attendance_summary b on a.summary_id=b.id where a.name>='%s' and a.name<='%s' and b.employee_id=%s"%(date_from,date_to,contract.employee_id.id)
            #print "query========>",query
            cr.execute(queryabs)
            #absence_ids=self.pool.get('hr.absence.summary.lines').search(cr,uid,[('name','>=',date_from),('name','<=',date_to)])
            absence_ids=map(lambda x: x[0], cr.fetchall())
            if absence_ids:
                absence=self.pool.get('hr.absence.summary.lines').browse(cr,uid,absence_ids)
                abspresday=0.0
                absnotpresday=0.0
                absnotpreshour=0.0
                alpha = {
                        'name': 'Absent with no reason',
                        'sequence': 6,
                        'code': "ALPHA",
                        'number_of_days': 0.0,
                        'number_of_hours': absnotpreshour,
                        'contract_id': contract.id,
                        }
                for absent in absence:
                    dt_abs=datetime.strptime(absent.name,"%Y-%m-%d")
                    day={
                         'Monday':0,
                         'Tuesday':1,
                         'Wednesday':2,
                         'Thursday':3,
                         'Friday':4,
                         'Saturday':5,
                         'Sunday':6,
                         }
                    dt_abs=day[dt_abs.strftime("%A")]
                    querysignin="select min(hour_from) from resource_calendar_attendance where calendar_id=%s and dayofweek='%s'"%(contract.working_hours.id,dt_abs)
                    cr.execute(querysignin)
                    res_in = cr.fetchone()[0]
                    
                    querysignout="select max(hour_from) from resource_calendar_attendance where calendar_id=%s and dayofweek='%s'"%(contract.working_hours.id,dt_abs)
                    cr.execute(querysignout)
                    res_out = cr.fetchone()[0]
                    
                    abspreshour = 10.0
                    if res_in and res_out:
                        abspreshour=res_out-res_in
                        
                    if absent.leave_id and absent.leave_id.id:
                        if absent.leave_id.holiday_status_id.name.replace(" ","_") in leaves:
                            leaves[absent.leave_id.holiday_status_id.name.replace(" ","_")]['number_of_days'] += 1.0
                            leaves[absent.leave_id.holiday_status_id.name.replace(" ","_")]['number_of_hours'] += abspreshour
                        else:
                            leaves[absent.leave_id.holiday_status_id.name.replace(" ","_")] = {
                                    'name': absent.leave_id.holiday_status_id.name.replace(" ","_"),
                                    'sequence': 5,
                                    'code': absent.leave_id.holiday_status_id.name.replace(" ","_"),
                                    'number_of_days': 1.0,
                                    'number_of_hours': abspreshour,
                                    'contract_id': contract.id,
                                }
                    else:
                        absnotpreshour+=abspreshour
                        absnotpresday+=1.0
                alpha.update({'number_of_days':absnotpresday,'number_of_hours':absnotpreshour})
                if alpha['number_of_days']>0.0:
                    res.append(alpha)
                if leaves and len(leaves)>0:
                    for key in leaves:
                        res.append(leaves[key])
                if leaves1 and len(leaves1)>0:
                    for x in leaves1:
                        res.append(x)
        return res
    
hr_payslip()

class hr_payslip_run(osv.osv):
    _inherit="hr.payslip.run"
    _columns = {
                'state': fields.selection([('draft', 'Draft'),('close', 'Close'),], 'State', select=True, readonly=True),
                'partner_id':fields.many2one('res.partner',"Partner",required=True),
                'move_id':fields.many2one('account.move',"Jurnal Entries"),
                }
    def draft_payslip_run(self, cr, uid, ids, context=None):
        if not context:
            context={}
        batches=self.browse(cr,uid,ids,context)
        for batch in batches:
            if batch.slip_ids:
                all_slip_id=[x.id for x in batch.slip_ids]
                self.pool.get('hr.payslip').write(cr, uid, all_slip_id, {"state":'draft'}, context=context)
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)
    
    def close_payslip_run(self, cr, uid, ids, context=None):
        if not context:
            context={}
        move_pool = self.pool.get('account.move')
        period_pool = self.pool.get('account.period')
        timenow = time.strftime('%Y-%m-%d')
        batches=self.browse(cr,uid,ids)
        for batch in batches:
            if batch.slip_ids:
                line_ids = []
                debit_sum = 0.0
                credit_sum = 0.0
                partner_id = batch.partner_id.id
                if not batch.slip_ids[0].period_id:
                    search_periods = period_pool.find(cr, uid, batch.date_start, context=context)
                    period_id = search_periods[0]
                else:
                    period_id = batch.slip_ids[0].period_id.id
    
                name = _('Payslip Batch - %s') % (batch.name)
                move = {
                    'narration': name,
                    'date': timenow,
                    'ref': batch.name,
                    'journal_id': batch.slip_ids[0].journal_id.id,
                    'period_id': period_id,
                }
                debit_line ={}
                credit_line ={}
                debit_sum=0.0
                credit_sum=0.0
                for slip in batch.slip_ids:
                    if slip.line_ids:
                        for line in slip.line_ids:
                            debit_account_id = line.salary_rule_id.account_debit.id
                            credit_account_id = line.salary_rule_id.account_credit.id
                            #print "slip.credit_note",slip.credit_note
                            amt = slip.credit_note and -line.total or line.total
                            #print "========================================================================="
                            #print line.name," - ",amt, " - ",line.total," - D: ",line.salary_rule_id.account_debit.id," - -C: ",line.salary_rule_id.account_credit.id
                            #print "========================================================================="
                            if debit_account_id:
                                if not debit_line.has_key(debit_account_id):
                                    debit_line.update({debit_account_id:(0, 0, {
                                            'name': line.name,
                                            'date': timenow,
                                            'partner_id': partner_id,
                                            'account_id': debit_account_id,
                                            'journal_id': slip.journal_id.id,
                                            'period_id': period_id,
                                            'debit': amt > 0.0 and amt or 0.0,
                                            'credit': amt < 0.0 and -amt or 0.0,
                                            'analytic_account_id': line.salary_rule_id.analytic_account_id and line.salary_rule_id.analytic_account_id.id or False,
                                            'tax_code_id': line.salary_rule_id.account_tax_id and line.salary_rule_id.account_tax_id.id or False,
                                            'tax_amount': line.salary_rule_id.account_tax_id and amt or 0.0,
                                        })
                                        })
                                else:
                                    debit_line[debit_account_id][2]['debit'] += amt > 0.0 and amt or 0.0
                                    debit_line[debit_account_id][2]['credit'] += amt < 0.0 and -amt or 0.0
                            
                            if credit_account_id:
                                if not credit_line.has_key(credit_account_id):
                                    credit_line.update({credit_account_id: (0, 0, {
                                        'name': line.name,
                                        'date': timenow,
                                        'partner_id': partner_id,
                                        'account_id': credit_account_id,
                                        'journal_id': slip.journal_id.id,
                                        'period_id': period_id,
                                        'debit': amt < 0.0 and -amt or 0.0,
                                        'credit': amt > 0.0 and amt or 0.0,
                                        'analytic_account_id': line.salary_rule_id.analytic_account_id and line.salary_rule_id.analytic_account_id.id or False,
                                        'tax_code_id': line.salary_rule_id.account_tax_id and line.salary_rule_id.account_tax_id.id or False,
                                        'tax_amount': line.salary_rule_id.account_tax_id and amt or 0.0,
                                        })
                                    })
                                else:
                                    credit_line[credit_account_id][2]['debit'] += amt < 0.0 and -amt or 0.0
                                    credit_line[credit_account_id][2]['credit'] += amt > 0.0 and amt or 0.0
                        for cred_key in credit_line:
                            credit_sum += credit_line[cred_key][2]['credit'] - credit_line[cred_key][2]['debit']
                        for deb_key in debit_line:
                            debit_sum += debit_line[deb_key][2]['debit'] - debit_line[deb_key][2]['credit']
                for key in debit_line :
                    line_ids.append(debit_line[key])
                    
                for key in credit_line :
                    line_ids.append(credit_line[key])
                    
                if debit_sum > credit_sum:
                    acc_id = batch.slip_ids[0].journal_id.default_credit_account_id.id
                    if not acc_id:
                        raise osv.except_osv(_('Configuration Error!'),_('The Expense Journal "%s" has not properly configured the Credit Account!')%(slip.journal_id.name))
                    adjust_credit = (0, 0, {
                        'name': _('Adjustment Entry'),
                        'date': timenow,
                        'partner_id': partner_id,
                        'account_id': acc_id,
                        'journal_id': batch.slip_ids[0].journal_id.id,
                        'period_id': period_id,
                        'debit': 0.0,
                        'credit': debit_sum - credit_sum,
                    })
                    raise osv.except_osv(_('Difference in sum debit_sum > credit_sum!'),_('Debit Sum "%s" & Credit Sum "%s"')%(debit_sum,credit_sum))
                    line_ids.append(adjust_credit)
    
                elif debit_sum < credit_sum:
                    acc_id = batch.slip_ids[0].journal_id.default_debit_account_id.id
                    if not acc_id:
                        raise osv.except_osv(_('Configuration Error!'),_('The Expense Journal "%s" has not properly configured the Debit Account!')%(slip.journal_id.name))
                    adjust_debit = (0, 0, {
                        'name': _('Adjustment Entry'),
                        'date': timenow,
                        'partner_id': partner_id,
                        'account_id': acc_id,
                        'journal_id': batch.slip_ids[0].journal_id.id,
                        'period_id': period_id,
                        'debit': credit_sum - debit_sum,
                        'credit': 0.0,
                    })
                    raise osv.except_osv(_('Difference in sum debit_sum < credit_sum!'),_('Debit Sum "%s" & Credit Sum "%s"')%(debit_sum,credit_sum))
                    line_ids.append(adjust_debit)
                move.update({'line_id': line_ids})
#                print "moveeeeeeeeeee==========\n\n\r"
                all_slip_id=[x.id for x in batch.slip_ids]
#                print 'all_slip_id',all_slip_id
#                print "==========\n\n\r"
                move_id = move_pool.create(cr, uid, move, context=context)
                
                self.pool.get('hr.payslip').write(cr, uid, all_slip_id, {'move_id': move_id, 'period_id' : period_id, "state":'done'}, context=context)
                if slip.journal_id.entry_posted:
                    move_pool.post(cr, uid, [move_id], context=context)             
        return self.write(cr, uid, ids, {'move_id': move_id,'state': 'close'}, context=context)
    
hr_payslip_run()