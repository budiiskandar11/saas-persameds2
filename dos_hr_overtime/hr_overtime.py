from openerp.osv import osv,fields
from openerp.addons import decimal_precision as dp
from openerp.tools.translate import _
import datetime
from datetime import date
from openerp import tools
import time

class hr_overtime(osv.osv):
    _name = "hr.overtime"
    
    _columns = {
                'name'      : fields.char('Overtime Name',size=32,required=True,),
                'department': fields.many2one('hr.department','Department'),
                'manager'   : fields.many2one('hr.employee','Manager'),
                'date'      : fields.date('Date'),
                'state'     : fields.selection([('draft','Draft'),
                                                ('proposed','Proposed - Waiting for Approval'),
                                                ('approved','Approved'),
                                                ('done','Done')],'State',readonly=True),
                'note'      : fields.char('Note', size=84),
                'periode'   : fields.char('Periode', size=32, readonly=True, states={'new': [('readonly', False)]}),
                'line_ids'  : fields.one2many('hr.overtime.lines','overtime_id','Overtime Lines'),
                }
    _defaults = {
                 'state'    : 'draft',
                 'date'     : lambda *a:time.strftime('%Y-%m-%d'),
                 }
  
hr_overtime()

class hr_overtime_lines(osv.osv):
    _name       = 'hr.overtime.lines'
    
    def convert_timeformat(self,time_string):
        split_list = str(time_string).split('.')
        hour_part = split_list[0]
        mins_part = split_list[1]
        round_mins = int(round(float(mins_part) * 60,-2))
        converted_string = hour_part + ':' + str(round_mins)[0:2]
        return converted_string
    
    def compute_paid_duration(self,cr,uid,ids,time_start,time_end,contract_data):
        sched=contract_data.working_hours.id
        emp_id=contract_data.employee_id
        emp_level=emp_id.level_id.id
        day={
             'Monday':0,
             'Tuesday':1,
             'Wednesday':2,
             'Thursday':3,
             'Friday':4,
             'Saturday':5,
             'Sunday':6,
             }
        total=datetime.timedelta(seconds=0)
        t0=datetime.datetime.strptime(time_start,"%Y-%m-%d %H:%M:%S")
        t0dayofweek=day[t0.strftime("%A")]
        querysignin="select max(hour_to) from resource_calendar_attendance where calendar_id=%s and dayofweek='%s'"%(sched,t0dayofweek)
        
        cr.execute(querysignin)
        res = cr.fetchone()[0]

        if res:
            timeformat=self.convert_timeformat(res)
            axx=t0.strftime("%Y-%m-%d")+" %s:00"%(timeformat)
            t1=datetime.datetime.strptime(axx,"%Y-%m-%d %H:%M:%S")
            ovtimeconfig=self.pool.get('hr.overtime.hours.config').search(cr,uid,[('job_level','=',emp_level),('type','=','schedule')])
            ovtimeconfdata=self.pool.get('hr.overtime.hours.config').browse(cr,uid,ovtimeconfig)[0]
            if t0>t1 and (t0-t1)>=datetime.timedelta(hours=4):
                diff=((t0-t1).seconds/3600/5)*5*ovtimeconfdata.hours_multiplier
                total=datetime.timedelta(hours=diff)
        else:
            t1=datetime.datetime.strptime(time_end,"%Y-%m-%d %H:%M:%S")
            t1date=t1.strftime("%Y-%m-%d")
            holiday_id=self.pool.get('hr.holiday.year').search(cr,uid,[('date','=',t1date)])
            t1dayofweek=day[t1.strftime("%A")]
            if t1dayofweek=='6':
                ovtimeconfig=self.pool.get('hr.overtime.hours.config').search(cr,uid,[('job_level','=',emp_level),('type','=','sunday')])[0]
                ovtimeconfdata=self.pool.get('hr.overtime.hours.config').browse(cr,uid,ovtimeconfig)
                if t1>t0 and (t1-t0)>=datetime.timedelta(hours=3):
                    diff=((t1-t0).seconds/3600/4)*4*ovtimeconfdata.hours_multiplier
                    total=datetime.timedelta(hours=diff)
            elif t1dayofweek!='6' and holiday_id:
                ovtimeconfig=self.pool.get('hr.overtime.hours.config').search(cr,uid,[('job_level','=',emp_level),('type','=','holiday')])[0]
                ovtimeconfdata=self.pool.get('hr.overtime.hours.config').browse(cr,uid,ovtimeconfig)
                if t1>t0 and (t1-t0)>=datetime.timedelta(hours=3):
                    diff=((t1-t0).seconds/3600/4)*4*ovtimeconfdata.hours_multiplier
                    total=datetime.timedelta(hours=diff)
            else:
                ovtimeconfig=self.pool.get('hr.overtime.hours.config').search(cr,uid,[('job_level','=',emp_level),('type','=','common')])[0]
                ovtimeconfdata=self.pool.get('hr.overtime.hours.config').browse(cr,uid,ovtimeconfig)
                if t1>t0 and (t1-t0)>=datetime.timedelta(hours=3):
                    diff=((t1-t0).seconds/3600/4)*4*ovtimeconfdata.hours_multiplier
                    total=datetime.timedelta(hours=diff)
        return str(total) or '0:00:00'
    
    def compute_duration(self,cr,uid,ids,time_start,time_end,contract_data):
        sched=contract_data.working_hours.id
        day={
             'Monday':0,
             'Tuesday':1,
             'Wednesday':2,
             'Thursday':3,
             'Friday':4,
             'Saturday':5,
             'Sunday':6,
             }
        total=datetime.timedelta(seconds=0)
        t0=datetime.datetime.strptime(time_start,"%Y-%m-%d %H:%M:%S")
        t0dayofweek=day[t0.strftime("%A")]
        querysignin="select max(hour_to) from resource_calendar_attendance where calendar_id=%s and dayofweek='%s'"%(sched,t0dayofweek)
        
        cr.execute(querysignin)
        res = cr.fetchone()[0]
        if res:
            timeformat=self.convert_timeformat(res)
            axx=t0.strftime("%Y-%m-%d")+" %s:00"%(timeformat)
            t1=datetime.datetime.strptime(axx,"%Y-%m-%d %H:%M:%S")
            if t0>t1 and (t0-t1)>=datetime.timedelta(hours=4):
                diff=((t1-t0).seconds/3600/4)*4
                total=datetime.timedelta(hours=diff)
        else:
            t1=datetime.datetime.strptime(time_end,"%Y-%m-%d %H:%M:%S")
            t1date=t1.strftime("%Y-%m-%d")
            holiday_id=self.pool.get('hr.holiday.year').search(cr,uid,[('date','=',t1date)])
            t1dayofweek=day[t1.strftime("%A")]
            if t1dayofweek=='6':
                if t1>t0 and (t1-t0)>=datetime.timedelta(hours=3):
                    diff=((t1-t0).seconds/3600/4)*4
                    total=datetime.timedelta(hours=diff)
            elif t1dayofweek!='6' and holiday_id:
                if t1>t0 and (t1-t0)>=datetime.timedelta(hours=3):
                    diff=((t1-t0).seconds/3600/4)*4
                    total=datetime.timedelta(hours=diff)
            else:
                if t1>t0 and (t1-t0)>=datetime.timedelta(hours=3):
                    diff=((t1-t0).seconds/3600/4)*4
                    total=datetime.timedelta(hours=diff)
        return str(total) or '0:00:00'
    
    def _calculate_duration(self, cr, uid, ids, field_names, arg=None, context=None):
        result = {}
        res={'value':{}}
        if not ids: return result
        for idx in ids:
            sl=self.browse(cr,uid,idx)
            start_date=datetime.datetime.strptime(sl.time_start,"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            end_date=datetime.datetime.strptime(sl.time_end,"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            contract_id=self.pool.get('hr.payslip').get_contract(cr,uid,sl.name,start_date,end_date,context)
            if contract_id:
                contract_data=self.pool.get('hr.contract').browse(cr,uid,contract_id)[0]
                result.update({idx:{'duration':False,'paid':False}})
                result[idx]['duration']=self.compute_duration(cr,uid,ids,sl.time_start,sl.time_end,contract_data)
                result[idx]['paid']=self.compute_paid_duration(cr,uid,ids,sl.time_start,sl.time_end,contract_data)
            else:
                warning={
                        "title": ("No Contract Found !"),
                        'message':("You should define a contract for employee : %s!"%(sl.name.resource_id.name))
                        }
                res.update({'warning':warning})
                res['value'].update({'employee_id':False,'end_date':start_date and start_date<end_date and end_date or False})
                return res
        return result
    
    _columns    = {
                   'name'       : fields.many2one('hr.employee',"Employee",required=True),
                   'overtime_id': fields.many2one('hr.overtime','ID'),
                   'time_start' : fields.datetime('Time Start',required=True),
                   'time_end'   : fields.datetime('Time End',required=True),
                   'note'       : fields.text('Note'),
                   'duration'   : fields.function(_calculate_duration, method=True, type='char', store=True, multi='dc', string='Duration (hours)',help="Overtime duration (hours)"),
                   'paid'       : fields.function(_calculate_duration, method=True, type='char', store=True, multi='dc', string='Paid (hours)', help="Paid overtime duration, according to Indonesian Labor Laws 2004 (hours)"),
                   }
    _defaults = {
                 'time_start'     : lambda *a:time.strftime('%Y-%m-%d %H:%M:%S'),
                 'time_end'     : lambda *a:time.strftime('%Y-%m-%d %H:%M:%S'),
                 }
hr_overtime_lines()

class hr_overtime_config(osv.osv):
    _name="hr.overtime.hours.config"
    _columns = {
        'name': fields.char('Name',size=32,required=True),
        'job_level':fields.many2one('hr.employee.level',"Employee Level",required=True),
        'type':fields.selection([("schedule","Scheduled Day"),("sunday","Sunday"),('common',"Common Day out of Sunday & Schedule"),('holiday',"Holiday")],"Type",required=True),
        'hours_multiplier':fields.float("Hours Multiplier"),
        'wage_computation':fields.text("Wage Computation"),
                }
hr_overtime_config()