from openerp.osv import fields,osv
from openerp.tools.translate import _
import datetime
from dateutil import parser
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import dateutil.relativedelta as rd
import dateutil.rrule as rrule
from datetime import date
import time

from dateutil import tz

class hr_attendance_summary(osv.osv):
    _name = "hr.attendance.summary"
    
    def convert_timeformat(self,time_string):
        split_list = str(time_string).split('.')
        hour_part = split_list[0]
        mins_part = split_list[1]
        round_mins = int(round(float(mins_part) * 60,-2))
        converted_string = hour_part + ':' + str(round_mins)[0:2]
        return converted_string
    
    def get_login_logout(self,cr,uid,employee_id,day):
        attendance_ids=False
        attendance_ids=self.pool.get('hr.attendance').search(cr,uid,[('employee_id','=',employee_id),('day','=',day)],order='name ASC')
        print "attendance_ids11111", attendance_ids
        att=self.pool.get('hr.attendance').browse(cr,uid,attendance_ids)
        day_plus_one=datetime.datetime.strftime(datetime.datetime.strptime(day,'%Y-%m-%d')+datetime.timedelta(days=1),'%Y-%m-%d')
        if len(attendance_ids)==1:
            next_day=self.pool.get('hr.attendance').search(cr,uid,[('day','=',day_plus_one),('employee_id','=',employee_id)],order="name ASC")
            print "next_day__________", next_day
            if next_day:
                att_next_day=self.pool.get('hr.attendance').browse(cr,uid,next_day)
                #print att_next_day[0]
                if att_next_day[0].action=='sign_out':
                    attendance_ids.append(att_next_day[0].id)
        attendance_ids=self.pool.get('hr.attendance').search(cr,uid,[('id','in',attendance_ids)],order="name DESC")
        
        print "attendance_ids", attendance_ids
        
        return attendance_ids
        
    def _get_worktime(self,cr,uid,date,employee_id,context=None):
        attendance_ids=self.get_login_logout(cr,uid,employee_id,date)
        attendances=self.pool.get('hr.attendance').browse(cr,uid,attendance_ids)
        total=datetime.timedelta(seconds=0)
        for attendance in attendances:
            if attendance['action']=='sign_out':
                t1=False
                t2=False
                t2=datetime.datetime.strptime(attendance['name'],"%Y-%m-%d %H:%M:%S")
            else:
                t1=False
                t1=datetime.datetime.strptime(attendance['name'],"%Y-%m-%d %H:%M:%S")
                total+=(t2-t1)
        return str(total) or '0:00:00'
    
    def _get_sign_in(self,cr,uid,date,employee_id,context=None):
        attendance_ids=self.get_login_logout(cr,uid,employee_id,date)
        attendance_ids=self.pool.get('hr.attendance').search(cr,uid,[('id','in',attendance_ids),('action','=','sign_in')],order='name ASC')
        if attendance_ids:
            attendances=self.pool.get('hr.attendance').browse(cr,uid,attendance_ids[0])
            return attendances.name
        return False
    
    def _get_sign_out(self,cr,uid,date,employee_id,context=None):
        attendance_ids=self.get_login_logout(cr,uid,employee_id,date)
        attendance_ids=self.pool.get('hr.attendance').search(cr,uid,[('id','in',attendance_ids),('action','=','sign_out')],order='name ASC')
        if attendance_ids:
            attendances=self.pool.get('hr.attendance').browse(cr,uid,attendance_ids[0])
            return attendances.name
        return False

    def _get_extra_day(self,cr,uid,date,employee_id,contract_id,context=None):
        attendance_ids=self.get_login_logout(cr,uid,employee_id,date)
        attendances=self.pool.get('hr.attendance').browse(cr,uid,attendance_ids)
        total=datetime.timedelta(seconds=0)
        day={
             'Monday':0,
             'Tuesday':1,
             'Wednesday':2,
             'Thursday':3,
             'Friday':4,
             'Saturday':5,
             'Sunday':6,
             }
        contract=self.pool.get('hr.contract').browse(cr,uid,contract_id,context=context)[0]
        for attendance in attendances:
            if attendance['action']=='sign_out':
                t1=False
                t2=False
                t2=datetime.datetime.strptime(attendance['name'],"%Y-%m-%d %H:%M:%S")
            else:
                t1=datetime.datetime.strptime(attendance['name'],"%Y-%m-%d %H:%M:%S")
                t1day=day[t1.strftime("%A")]
                #print "t1day=>",t1day
                if contract.extraday_working_hours and contract.extraday_working_hours.id:
                    querysignout="select max(hour_to) from resource_calendar_attendance where calendar_id=%s and dayofweek='%s'"%(contract.extraday_working_hours.id,t1day)
                else:
                    querysignout="select max(hour_to) from resource_calendar_attendance where calendar_id=%s and dayofweek='%s'"%(contract.working_hours.id,t1day)
                cr.execute(querysignout)
                resout = cr.fetchone()[0]
                totalot=datetime.timedelta(seconds=0)
                holiday_check=self.pool.get('hr.holiday.year').search(cr,uid,[('date','=',attendance['day'])])
                contractdaycheck=self.pool.get('resource.calendar.attendance').search(cr,uid,[('calendar_id','=',contract.working_hours.id),('dayofweek','=',str(t1day))])
                if resout and (holiday_check or (not contractdaycheck)):
                    timeformat2=self.convert_timeformat(resout)
                    t1date=attendance['day']+" %s:00"%(timeformat2)
                    t1=datetime.datetime.strptime(t1date,"%Y-%m-%d %H:%M:%S")
# Editan Deby
                    if contract.employee_id:
                        axx=attendance['day']+" %s:00"%(timeformat2)
                        t6=datetime.datetime.strptime(axx,"%Y-%m-%d %H:%M:%S")
                        if (t2-t6-datetime.timedelta(minutes=contract.employee_id.level_id.start_overtime))>datetime.timedelta(seconds=0):
                            totalot+=(t2-t6-datetime.timedelta(minutes=contract.employee_id.level_id.start_overtime))
                            if totalot>datetime.timedelta(minutes=contract.employee_id.level_id.minimum_overtime):
                                return str(totalot) or False
                    elif contract.employee_id.level_id.overtime_type=='hour':
                        timeformat2=self.convert_timeformat(resout)
                        axx=attendance['day']+" %s:00"%(timeformat2)
                        t6=datetime.datetime.strptime(axx,"%Y-%m-%d %H:%M:%S")
                        if ((t2-t6-datetime.timedelta(minutes=contract.employee_id.level_id.start_overtime))>datetime.timedelta(seconds=0)):
                            totalot+=(t2-t6-datetime.timedelta(minutes=contract.employee_id.level_id.start_overtime))
                            if totalot>datetime.timedelta(hours=contract.employee_id.level_id.minimum_overtime):
                                return str(totalot) or False
# Editan Deby End
        return False

    
    def _get_extra_day(self,cr,uid,date,employee_id,contract_id,context=None):
        attendance_ids=self.get_login_logout(cr,uid,employee_id,date)
        attendances=self.pool.get('hr.attendance').browse(cr,uid,attendance_ids)
        total=datetime.timedelta(seconds=0)
        for attendance in attendances:
            if attendance['action']=='sign_out':
                t1=False
                t2=False
                t2=datetime.datetime.strptime(attendance['name'],"%Y-%m-%d %H:%M:%S")
            else:
                t1=False
                t1=datetime.datetime.strptime(attendance['name'],"%Y-%m-%d %H:%M:%S")
                total+=(t2-t1)
                holiday_check=self.pool.get('hr.holiday.year').search(cr,uid,[('date','=',attendance['day'])])
                if holiday_check: 
                    return str(total)
                contract=self.pool.get('hr.contract').browse(cr,uid,contract_id,context=context)[0]
                day={
                     'Monday':0,
                     'Tuesday':1,
                     'Wednesday':2,
                     'Thursday':3,
                     'Friday':4,
                     'Saturday':5,
                     'Sunday':6,
                     }
                t5=datetime.datetime.strptime(attendance['name'],"%Y-%m-%d %H:%M:%S")
                t5dayofweek=day[t5.strftime("%A")]
                querysignout="select max(hour_to) from resource_calendar_attendance where calendar_id=%s and dayofweek='%s'"%(contract.working_hours.id,t5dayofweek)
                cr.execute(querysignout)
                resout = cr.fetchone()[0]
                if not resout: 
                    return str(total)
        return False
    
    def _check_substitute(self,cr,uid,date,employee_id):
        subst_id=self.pool.get('hr.substitute.working.schedule').search(cr,uid,[('substitution_date','=',date),'|',('name','=',employee_id),('substituen_id','=',employee_id)])
        return subst_id or False
    
    def _get_latetime(self,cr,uid,date,employee_id,contract_id,context=None):
        print "####_get_latetime####"
        attendance_ids=self.get_login_logout(cr,uid,employee_id,date)
        attendances=self.pool.get('hr.attendance').browse(cr,uid,attendance_ids)
        contract=self.pool.get('hr.contract').browse(cr,uid,contract_id)[0]
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
        x=False
        check_subs_id=self._check_substitute(cr,uid,date,employee_id)
        print "check_subs_id----------->>", check_subs_id
        
        if check_subs_id:
            check_substitute=self.pool.get('hr.substitute.working.schedule').browse(cr,uid,check_subs_id[0])
        for attendance in attendances:
            print "attendance", attendance
            print "attendance [name]", attendance['id'], attendance['name']
            if attendance['action']=='sign_in':
                t1=False
                t2=False
                
                t2=datetime.datetime.strptime(attendance['name'],"%Y-%m-%d %H:%M:%S")+timedelta(hours=7)
                
                t2dayofweek=day[t2.strftime("%A")]
                working_hours_id=contract.working_hours.id
                if check_subs_id:
                    if check_substitute.name.id==employee_id and check_substitute.substituen_id.id and check_substitute.substituen_contract_id.id:
                        working_hours_id=check_substitute.substituen_contract_id.working_hours.id
                        querysignin="select min(hour_from) from resource_calendar_attendance where calendar_id=%s and dayofweek='%s'"%(working_hours_id,str(t2dayofweek))
                        cr.execute(querysignin)
                        res = cr.fetchone()[0]
                    elif check_substitute.substituen_id.id==employee_id and check_substitute.name.id and check_substitute.contract_id.id:
                        working_hours_id=check_substitute.contract_id.working_hours.id
                        querysignin="select min(hour_from) from resource_calendar_attendance where calendar_id=%s and dayofweek='%s'"%(working_hours_id,str(t2dayofweek))
                        cr.execute(querysignin)
                        res = cr.fetchone()[0]
                    else:
                        res=check_substitute.hour_from
                else:
                    print "ELSE"
                    querysignin="select min(hour_from) from resource_calendar_attendance where calendar_id=%s and dayofweek='%s'"%(working_hours_id,str(t2dayofweek))  
                    cr.execute(querysignin)
                    res = cr.fetchone()[0]
                    print "res--------------------->>", res
                if res:
                    timeformat=self.convert_timeformat(res)
                    axx=attendance['day']+" %s:00"%(timeformat)
                    t1=datetime.datetime.strptime(axx,"%Y-%m-%d %H:%M:%S")
                    total=False or (t1-t2)<datetime.timedelta(seconds=0) and datetime.timedelta(seconds=0) 
                    if (t1-t2)<datetime.timedelta(seconds=0):
                        total+=(t2-t1)
                        x=str(total)
                    print "TTTTTTTTTTTTTT", t1, t2, datetime.timedelta(seconds=0), x
        print "LATE :::::", x
        return x 
    
    def _get_halfday(self,cr,uid,date,employee_id,contract_id,context=None):
        attendance_ids=self.get_login_logout(cr,uid,employee_id,date)
        attendances=self.pool.get('hr.attendance').browse(cr,uid,attendance_ids)
        leave={}
        found=False
        for i in attendances:
            if i.action=='sign_in':found=True
        
        if found==False:
            return leave
        
        contract=self.pool.get('hr.contract').browse(cr,uid,contract_id)[0]
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
        for attendance in attendances:
            if attendance['action']=='sign_in':
                t1=False
                t2=False
                t2=datetime.datetime.strptime(attendance['name'],"%Y-%m-%d %H:%M:%S")
                getdate=t2.strftime('%Y-%m-%d')
                t2dayofweek=day[t2.strftime("%A")]
                querysignin="select min(hour_from) from resource_calendar_attendance where calendar_id=%s and dayofweek='%s'"%(contract.working_hours.id,t2dayofweek)
                subst_ids=self.pool.get('hr.substitute.working.schedule').search(cr,uid,[('state','=','approved'),('name','=',attendance['employee_id'].id),('substitution_date','=',getdate)])
                if not subst_ids:
                    cr.execute(querysignin)
                    res = cr.fetchone()[0]
                else:
                    subst_data=self.pool.get('hr.substitute.working.schedule').browse(cr,uid,subst_ids)[0]
                    res=subst_data.hour_from
                if res:
                    timeformat=self.convert_timeformat(res)
                    axx=attendance['day']+" %s:00"%(timeformat)
                    t1=datetime.datetime.strptime(axx,"%Y-%m-%d %H:%M:%S")
                    total=False or (t1-t2)<datetime.timedelta(seconds=0) and datetime.timedelta(seconds=0) 
                    
                    if (t1-t2)<datetime.timedelta(seconds=0):
                        total+=(t2-t1)
                        if total>datetime.timedelta(hours=2):
                            hol_stat=self.pool.get('hr.holidays.status').search(cr,uid,[('name','like','Annual Leave')])
                            date_to=datetime.datetime.strptime(date+" "+timeformat,"%Y-%m-%d %H:%M")+total
                            date_from=datetime.datetime.strptime(date+" "+timeformat,"%Y-%m-%d %H:%M")
                            print "111111111111111"
                            print "hol_stat[0]",hol_stat[0]
                            
                            leave={
                                'name':"Half Day Leave",
                                'holiday_type':'employee',
                                'holiday_status_id': hol_stat[0],
                                'employee_id':employee_id,
                                'date_from':datetime.datetime.strftime(date_from,'%Y-%m-%d %H:%M:%S'),
                                'date_to':datetime.datetime.strftime(date_to,'%Y-%m-%d %H:%M:%S'),
                                'type':'remove',
                                'number_of_days':-0.5,
                                'number_of_days_temp':0.5,
                                'state':'draft',
                                'manager_id':1,
                                   }
            if attendance['action']=='sign_out':
                t1=False
                t2=False
                t2=datetime.datetime.strptime(attendance['name'],"%Y-%m-%d %H:%M:%S")
                getdate=t2.strftime('%Y-%m-%d')
                t2dayofweek=day[t2.strftime("%A")]
                querysignout="select max(hour_to) from resource_calendar_attendance where calendar_id=%s and dayofweek='%s'"%(contract.working_hours.id,t2dayofweek)
                substout_ids=self.pool.get('hr.substitute.working.schedule').search(cr,uid,[('state','=','approved'),('name','=',attendance['employee_id'].id),('substitution_date','=',getdate)])
                if not substout_ids:
                    cr.execute(querysignout)
                    res = cr.fetchone()[0]
                else:
                    substout_data=self.pool.get('hr.substitute.working.schedule').browse(cr,uid,substout_ids)[0]
                    res=substout_data.hour_from
                if res:
                    timeformat=self.convert_timeformat(res)
                    axx=attendance['day']+" %s:00"%(timeformat)
                    t1=datetime.datetime.strptime(axx,"%Y-%m-%d %H:%M:%S")
                    total=False or (t1-t2)>datetime.timedelta(seconds=0) and datetime.timedelta(seconds=0) 
                    if (t1-t2)>datetime.timedelta(seconds=0):
                        total+=(t1-t2)
                        if total>datetime.timedelta(hours=2):
                            hol_stat=self.pool.get('hr.holidays.status').search(cr,uid,[('name','like','Annual Leave')])
                            date_to=datetime.datetime.strptime(date+" "+timeformat,"%Y-%m-%d %H:%M")+total
                            date_from=datetime.datetime.strptime(date+" "+timeformat,"%Y-%m-%d %H:%M")
                            print "22222222222222222222"
                            print "hol_stat[0]222",hol_stat[0]
                            leave={
                                'name':"Half Day Leave",
                                'holiday_type':'employee',
                                'holiday_status_id': hol_stat[0],
                                'employee_id':employee_id,
                                'date_from':datetime.datetime.strftime(date_from,'%Y-%m-%d %H:%M:%S'),
                                'date_to':datetime.datetime.strftime(date_to,'%Y-%m-%d %H:%M:%S'),
                                'type':'remove',
                                'number_of_days':-0.5,
                                'number_of_days_temp':0.5,
                                'state':'draft',
                                'manager_id':1,
                                   }                
        return leave
    
    def _get_overtime(self,cr,uid,date,employee_id,contract_id,context=None):
        x=False
        if not context: context={}
        attendance_ids=self.get_login_logout(cr,uid,employee_id,date)
        attendances=self.pool.get('hr.attendance').browse(cr,uid,attendance_ids)
        check_subs_id=self._check_substitute(cr,uid,date,employee_id)
        if check_subs_id:
            check_substitute=self.pool.get('hr.substitute.working.schedule').browse(cr,uid,check_subs_id[0])
        for attendance in attendances:
            holiday_check=self.pool.get('hr.holiday.year').search(cr,uid,[('date','=',attendance['day'])])
            if holiday_check: return False
            else:
                if attendance['action']=='sign_out':
                    contract=self.pool.get('hr.contract').browse(cr,uid,contract_id,context=context)[0]
                    day={
                         'Monday':0,
                         'Tuesday':1,
                         'Wednesday':2,
                         'Thursday':3,
                         'Friday':4,
                         'Saturday':5,
                         'Sunday':6,
                         }
                    t5=datetime.datetime.strptime(attendance['name'],"%Y-%m-%d %H:%M:%S")
                    t5dayofweek=day[t5.strftime("%A")]
                    if check_subs_id:
                        if check_substitute.name.id==employee_id and check_substitute.substituen_id.id and check_substitute.substituen_contract_id.id:
                            working_hours_id=check_substitute.substituen_contract_id.working_hours.id
                            querysignout="select max(hour_to) from resource_calendar_attendance where calendar_id=%s and dayofweek='%s'"%(working_hours_id,t5dayofweek)
                            cr.execute(querysignout)
                            resout = cr.fetchone()[0]
                        elif check_substitute.substituen_id.id==employee_id and check_substitute.name.id and check_substitute.contract_id.id:
                            working_hours_id=check_substitute.contract_id.working_hours.id
                            querysignout="select max(hour_to) from resource_calendar_attendance where calendar_id=%s and dayofweek='%s'"%(working_hours_id,t5dayofweek)  
                            cr.execute(querysignout)
                            resout = cr.fetchone()[0]
                        else:
                            resout=check_substitute.hour_to
                    else:
                        querysignout="select max(hour_to) from resource_calendar_attendance where calendar_id=%s and dayofweek='%s'"%(contract.working_hours.id,t5dayofweek)
                        cr.execute(querysignout)
                        resout = cr.fetchone()[0]
                    totalot=datetime.timedelta(seconds=0)
# EditanDeby
                    if resout:
                        if contract.employee_id:
                            timeformat2=self.convert_timeformat(resout)
                            axx=attendance['day']+" %s:00"%(timeformat2)
                            t6=datetime.datetime.strptime(axx,"%Y-%m-%d %H:%M:%S")
#                             if (t5-t6-datetime.timedelta(minutes=contract.employee_id.level_id.start_overtime))>datetime.timedelta(seconds=0):
#                                 totalot+=(t5-t6-datetime.timedelta(minutes=contract.employee_id.level_id.start_overtime))
#                                 if totalot>datetime.timedelta(minutes=contract.employee_id.level_id.minimum_overtime):
#                                     return str(totalot) or False
                        elif contract.employee_id.level_id.overtime_type=='hour':
                            timeformat2=self.convert_timeformat(resout)
                            axx=attendance['day']+" %s:00"%(timeformat2)
                            t6=datetime.datetime.strptime(axx,"%Y-%m-%d %H:%M:%S")
#                             if ((t5-t6-datetime.timedelta(minutes=contract.employee_id.level_id.start_overtime))>datetime.timedelta(seconds=0)):
#                                 totalot+=(t5-t6-datetime.timedelta(minutes=contract.employee_id.level_id.start_overtime))
#                                 if totalot>datetime.timedelta(hours=contract.employee_id.level_id.minimum_overtime):
#                                     return str(totalot) or False
# EditanDeby End

        return x
    
    def _compute_summary_lines(self,cr,uid,name,employee_id,contract_id,context=None):
        if name and employee_id:
            result={}
            attendance_ids=self.pool.get('hr.attendance').search(cr,uid,[('employee_id','=',employee_id),('name','>=',name+" 00:00:00"),('name','<=',name+" 23:59:59"),('action','=','sign_in')])
            if attendance_ids:
                dummy={
                    'name':name,
                    'attendance_ids':False,
                    'worktime':self._get_worktime(cr,uid,name,employee_id,context=context),
                    'late_time':self._get_latetime(cr,uid,name,employee_id,contract_id,context=context),
                    'overtime':self._get_overtime(cr,uid,name,employee_id,contract_id,context=context),
                    'extra_day':self._get_extra_day(cr,uid,name,employee_id,contract_id,context=context),
                    'sign_in':self._get_sign_in(cr,uid,name,employee_id,context=context),
                    'sign_out':self._get_sign_out(cr,uid,name,employee_id,context=context)
                       }
                result.update(dummy)
        return result
    
    def _compute_absence_lines(self,cr,uid,name,employee_id,contract_id,context=None):
        #print "_compute_absence_lines"
        if name and employee_id:
            result={}
            day={
             'Monday':0,
             'Tuesday':1,
             'Wednesday':2,
             'Thursday':3,
             'Friday':4,
             'Saturday':5,
             'Sunday':6,
             }
            attendance_ids=self.pool.get('hr.attendance').search(cr,uid,[('employee_id','=',employee_id),('name','>=',name+" 00:00:00"),('name','<=',name+" 23:59:59")])
            holiday_check=self.pool.get('hr.holiday.year').search(cr,uid,[('date','=',name)])
            t1=datetime.datetime.strptime(name,"%Y-%m-%d")
            #print "t1", t1
            t1day=day[t1.strftime("%A")]
            #print "t1day", t1day
            contract=self.pool.get('hr.contract').browse(cr,uid,contract_id)[0]
            contractdaycheck=self.pool.get('resource.calendar.attendance').search(cr,uid,[('calendar_id','=',contract.working_hours.id),('dayofweek','=',str(t1day))])
            
            #print "contractdaycheck----------->>", contractdaycheck
            
            if holiday_check: return False
            if not attendance_ids and not holiday_check and contractdaycheck :
                leave_id=self.pool.get('hr.holidays').search(cr,uid,[('employee_id','=',employee_id),('date_from',"<=",name),('date_to',">=",name),('state','=','validate')])
                if leave_id:
                    leave=self.pool.get('hr.holidays').browse(cr,uid,leave_id[0])
                dummy={
                    'name':name,
                    'type':leave_id and 'with_reason' or 'no_reason',
                    'leave_id':leave_id and leave_id[0] or False,
                    'description':leave_id and (leave.name or leave.description) or "No Reason Defined",
                       }
                result.update(dummy)
        return result
    
    def _compute_spt_lines(self,cr,uid,name,employee_id,contract_id,context=None):
        
        
        
        print "name>>>>>>>>>>>>>>>", name
        if name and employee_id:
            result={}
            day={
             'Monday':0,
             'Tuesday':1,
             'Wednesday':2,
             'Thursday':3,
             'Friday':4,
             'Saturday':5,
             'Sunday':6,
             }
            attendance_ids=self.pool.get('hr.attendance').search(cr,uid,[('employee_id','=',employee_id),('name','>=',name+" 00:00:00"),('name','<=',name+" 23:59:59")])
            holiday_check=self.pool.get('hr.holiday.year').search(cr,uid,[('date','=',name)])
            t1=datetime.datetime.strptime(name,"%Y-%m-%d")
            print "t1", t1
            t1day=day[t1.strftime("%A")]
            print "t1day", t1day
            contract=self.pool.get('hr.contract').browse(cr,uid,contract_id)[0]
            contractdaycheck=self.pool.get('resource.calendar.attendance').search(cr,uid,[('calendar_id','=',contract.working_hours.id),('dayofweek','=',str(t1day))])
            print "contractdaycheck11111111111111111", contractdaycheck
        
        if name and employee_id:
            result={}
            attendance_ids=self.pool.get('hr.attendance').search(cr,uid,[('employee_id','=',employee_id),('name','>=',name+" 00:00:00"),('name','<=',name+" 23:59:59")])
            holiday_check=self.pool.get('hr.holiday.year').search(cr,uid,[('date','=',name)])
            if holiday_check: return False
            if not attendance_ids and not holiday_check:
                query="select a.id from hr_spt a left join hr_spt_lines b on a.id=b.spt_id where a.date_from <= '%s' and a.date_to >= '%s' and b.employee_id= %s "%(name,name,employee_id)
                cr.execute(query)
                spt_id=cr.fetchone()
                if spt_id:
                    spt=self.pool.get('hr.spt').browse(cr,uid,spt_id[0])
                    dummy={
                        'name':name,
                        'spt_id':spt_id[0] and spt.id or False,
                        'description':spt and spt.name or "No SPT Defined",
                           }
                    result.update(dummy)
        return result
    
    def get_normal_days(self,cr,uid,ids, start_date,end_date):
        
        ####
        day     = [1,2,3,4,5,6]
        workday = []
        holiday = []
        
        for val in self.browse(cr, uid, ids):
            employee_id = val.employee_id.id
            emp_data=self.pool.get('hr.employee').browse(cr,uid,employee_id)
            contract_id=self.pool.get('hr.payslip').get_contract(cr,uid,emp_data,start_date,end_date)
            
            work_schedule = self.pool.get('hr.contract').browse(cr, uid, contract_id).working_hours.attendance_ids
            
            if work_schedule:
                for work_day in work_schedule:
                    print "work_day.dayofweek[0]", work_day.dayofweek
                    workday.append(int(work_day.dayofweek))
        print "day", day, "workday", workday
        holiday = list(set(day) - set(workday))
        print "holiday-------------->>", holiday
        
        tahun = datetime.datetime.strptime(start_date,"%Y-%m-%d").year
        bulan = datetime.datetime.strptime(start_date,"%Y-%m-%d").month
        from calendar import weekday, monthrange, SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY
        
        y, m = tahun, bulan
        
        days = [weekday(y, m, d+1) for d in range(*monthrange(y, m))]
        print "/////////", days[SATURDAY], days[SUNDAY]
        if holiday:
            holidayofmonth = 0
            for holiday in holiday:
                if holiday == 0:
                    holidayofmonth += days[MONDAY]
                elif holiday == 1:
                    holidayofmonth += days[TUESDAY]
                elif holiday == 2:
                    holidayofmonth += days[WEDNESDAY]
                elif holiday == 3:
                    holidayofmonth += days[THURSDAY]
                elif holiday == 4:
                    holidayofmonth += days[FRIDAY]
                elif holiday == 5:
                    print "holidayofmonthxxxxx", holidayofmonth
                    holidayofmonth += days[SATURDAY]
                elif holiday == 6:
                    print "holidayofmonthyyyy", holidayofmonth
                    holidayofmonth += days[SUNDAY]
            print "holidayofmonth", holidayofmonth
        ####
        
        holiday_years_id=self.pool.get('hr.holiday.year').search(cr,uid,[('date','>=',start_date),('date','<=',end_date)])
        holidays=[]
        numberofdays=25
        if holiday_years_id:
            holiday_years=self.pool.get('hr.holiday.year').browse(cr,uid,holiday_years_id)
            holidays=[x.date for x in holiday_years]
            
        start_d=datetime.datetime.strptime(start_date,"%Y-%m-%d")
        end_d=datetime.datetime.strptime(end_date,"%Y-%m-%d")
        #rr = rrule.rrule(rrule.WEEKLY,byweekday=rd.SU,dtstart=start_d)
        #print "rr", rr
        #ll=[l.strftime("%Y-%m-%d") for l in rr.between(start_d,end_d,inc=True)]
        #print "ll", ll
        #for dd in ll:
        #    if dd not in holidays:
        #        holidays.append(dd)
        #print "(end_d-start_d)", (end_d-start_d)
        #print "Holiday", len(holidays)
        
        #raise Warning(_('The number of remaining leaves is not sufficient for this leave type.\n'
        #                        'Please verify also the leaves waiting for validation.'))
        
        #numberofdays=(end_d-start_d).days+1-len(holidays)-holidayofmonth
        work    = len(val.summary_lines)
        absence = len(val.absence_ids)
        
        numberofdays = work + absence
        return numberofdays
        
    def onchange_date(self, cr, uid, ids, start_date,end_date,employee_id, context=None):
        print "HHHHHHHHHHHHHHHHH", start_date,end_date,employee_id
        
        if context is None:
            context = {}
        res={'value':{}}
        if not employee_id:
            warning={
                    "title": ("Input Data Error !"),
                    'message':("Employee should be defined!")
                    }
            res['value'].update({'end_date':start_date and start_date<end_date and end_date or False})
            res.update({'warning':warning})
        else:
            if start_date and end_date:
                emp_data=self.pool.get('hr.employee').browse(cr,uid,employee_id)
                contract_id=self.pool.get('hr.payslip').get_contract(cr,uid,emp_data,start_date,end_date,context)
                if not contract_id:
                    warning={
                        "title": ("No Contract Found !"),
                        'message':("You should define a contract for employee : %s!"%(emp_data.resource_id.name))
                        }
                    res['value'].update({'employee_id':False,'end_date':start_date and start_date<end_date and end_date or False})
                    res.update({'warning':warning})
                else:
                    if end_date<start_date or end_date==start_date:
                        warning={"title": ("Input Data Error !"),
                                 'message':("End Date must be greater than Start Date!")}
                        res['value'].update({'end_date':False})
                        res.update({'warning':warning})
                    else:
                        if ids:
                            summ_id=self.browse(cr,uid,ids)
                            for i in summ_id:
                                i_summary_lines=[j.id for j in i.summary_lines]
                                self.pool.get('hr.attendance.summary.lines').unlink(cr,uid,i_summary_lines)
                                i_absence_ids=[k.id for k in i.absence_ids]
                                self.pool.get('hr.absence.summary.lines').unlink(cr,uid,i_absence_ids)
                                i_spt_lines=[l.id for l in i.spt_lines]
                                self.pool.get('hr.spt.summary').unlink(cr,uid,i_spt_lines)
                                i_half_day_leaves=[m.id for m in i.half_day_leaves]
                                self.pool.get('hr.holidays').holidays_reset(cr,uid,i_half_day_leaves)
                                self.pool.get('hr.holidays').unlink(cr,uid,i_half_day_leaves)
                        d1 = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
                        d2 = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
                        diff = d2 - d1
                        summary_lines=[]
                        absence_lines=[]
                        spt_lines=[]
                        half_day_leaves=[]
                        for i in range(diff.days + 1):
                            name=(d1 + datetime.timedelta(i)).isoformat()
                            dump=self._compute_summary_lines(cr,uid,name,employee_id,contract_id,context=context)
                            half_day=self._get_halfday(cr,uid,name,employee_id,contract_id,context=context)
                            if half_day!={}:
                                half_day_leaves.append(half_day)
                            if dump:
                                summary_lines.append(dump)
                                
                            else:
                                dumpspt=self._compute_spt_lines(cr,uid,name,employee_id,contract_id,context=context)
                                if not dumpspt:
                                    dump2=self._compute_absence_lines(cr,uid,name,employee_id,contract_id,context=context)
                                    if dump2:
                                        absence_lines.append(dump2)
                                else:
                                    spt_lines.append(dumpspt)
                        
                        #####Absence Reason#####
                        hr_absence_obj = self.pool.get('hr.absence')
                        absence_reason_line = []
                        hr_absence_search = hr_absence_obj.search(cr, uid, [('employee_id','=',employee_id),('date','>=',start_date),('date','<=',end_date)], order='date')
                        for absence_reason in hr_absence_obj.browse(cr, uid, hr_absence_search):
                            val = {
                                'name'          : absence_reason.name,
                                'employee_id'   : absence_reason.employee_id.id,
                                'date'          : absence_reason.date,
                                'reason'        : absence_reason.reason.id, 
                                   }
                            absence_reason_line.append(val)
                        
                        ########################
                        
                        #print "half_day_leaves",half_day_leaves
                        res={'value':{
                              'summary_lines':summary_lines,
                              'absence_ids':absence_lines,
                              'absence_reason_ids' : absence_reason_line,
                              'spt_lines':spt_lines,
                              'half_day_leaves':half_day_leaves,
                              'normalwork':False,
                              'late':False,
                              'overtime':False,
                              'extraday':False
                              }
                             }
        
        return res
    
    def _get_summary(self, cr, uid, ids, field_names, arg=None, context=None):
        result={}
        if not context:
            context={}
        for summary in self.browse(cr,uid,ids,context=context):
            total_normal_working_days=0
            total_normal_working_days=self.get_normal_days(cr,uid,ids,summary.start_date,summary.end_date)
            value={}
            workdays=False
            normalwork=False
            late=False
            overtime=False
            total_day=False
            sundayworking=False
            fields=['late_time', 'overtime', 'extra_day', 'worktime', 'longshift']
            if summary.summary_lines:
                for line in summary.summary_lines:
                    if line.worktime:
                        workdays+=1
                    if line.late_time:
                        late+=1
                    if line.extra_day:
                        sundayworking+=1
                    total_day+=1
                    if line.overtime:
                        overtime+=1
                extra_day=workdays>total_normal_working_days and workdays-total_normal_working_days or 0
                value.update({
                              'workdays':workdays,
                              'normalwork':total_normal_working_days,
                              'late':late,
                              'extra_day':extra_day,
                              'overtime':overtime,
                              'overtime_holiday':sundayworking,
                              })
                #print "value----------->",value
            if summary.absence_ids:
                absent=0
                reason=0
                for abs_line in summary.absence_ids:
                    if abs_line.type == 'with_reason': 
                        reason+=1
                    else: 
                        absent+=1
                value.update({'absentday':absent,'leaveday':reason})
            if summary.spt_lines:
                sptnum=0
                for spt in summary.spt_lines:
                    if spt.spt_id and spt.spt_id.id:
                        sptnum+=1
                value.update({'ondutyday':sptnum})
                
            ###
            if summary.absence_reason_ids:
                print "absence_reason_ids------------------>>"
                allowance_day = 0
                for absence_reason in summary.absence_reason_ids:
                    if absence_reason.reason.allowance == True:
                        allowance_day += 1
                allowance_day = allowance_day + workdays
                
                print "allowance_day", allowance_day
                
                value.update({'allowance_day':allowance_day})
                print "allowance_day22222", allowance_day
                #raise Warning(_('The number of remaining leaves is not sufficient for this leave type.\n'
                 #               'Please verify also the leaves waiting for validation.'))
                
            ###
            result.update({summary.id:value})
        return result
    
    def _ondutytrip(self, cr, uid, ids, field_names, arg=None, context=None):
        print "_ondutytrip"
        result = {}
        total_days = 0
        for val in self.browse(cr, uid, ids, context=None):
            duty_id="select id from duty_trip where date_start >= '%s' and date_end <= '%s' and state='paid'"%(val.start_date,val.end_date)
            cr.execute(duty_id)
            duty_id = ids = map(lambda x: x[0], cr.fetchall())
            print "duty_id", duty_id
            
        for duty in self.pool.get('duty.trip').browse(cr, uid, duty_id, context=None):
            print "duty---------_>>", duty
            total_days += duty.total_days
        result[val.id] = { 'ondutytrip' : total_days}
        return result
    
        
    _columns = {
        'name':fields.char("Attendance Summary name",size=128,required=True),
        'employee_id' : fields.many2one('hr.employee',"Employee",required=True),
        'start_date' : fields.date('Start Date',required=True),
        'end_date' : fields.date('End Date',required=True),
        'summary_lines':fields.one2many('hr.attendance.summary.lines','summary_id','Attendance Summary Lines'),
        'absence_ids':fields.one2many('hr.absence.summary.lines','summary_id',"Absence lines"),
        'absence_reason_ids':fields.one2many('hr.absence.reason.summary.lines','summary_id',"Absence lines"),
        'spt_lines':fields.one2many('hr.spt.summary','summary_id',"On Duty Days"),
        'workdays': fields.function(_get_summary, method=True, type='integer',size=20,store=True, multi='wsum', string='Total Working Days'),
        'normalwork': fields.function(_get_summary, method=True, type='integer',size=20,store=True, multi='wsum', string='Total Normal Working Days'),
        'late': fields.function(_get_summary, method=True, type='integer',size=20,store=True, multi='wsum', string='Total Late Day'),
        'overtime': fields.function(_get_summary, method=True, type='integer',size=20,store=True, multi='wsum', string='Total Overtime Day'),
        'overtime_holiday': fields.function(_get_summary, method=True, type='integer',size=20,store=True, multi='wsum', string='Overtime in holiday'),
        'extraday': fields.function(_get_summary, method=True, type='integer',size=20,store=True, multi='wsum', string='Total Extra Day'),
        'absentday': fields.function(_get_summary, method=True, type='integer',size=20,store=True, multi='wsum', string='Total Absents Day'),
        'leaveday': fields.function(_get_summary, method=True, type='integer',size=20,store=True, multi='wsum', string='Total Leaves Day'),
        'ondutyday': fields.function(_get_summary, method=True, type='integer',size=20,store=True, multi='wsum', string='Total Working Trip Day'),
        'allowance_day': fields.function(_get_summary, method=True, type='integer',size=20,store=True, multi='wsum', string='Total Allowance Day'),
        'ondutytrip': fields.function(_ondutytrip, method=True, type='integer',size=20,store=False, multi='wsum', string='Total Working Trip Day'),
        
        'half_day_leaves':fields.one2many('hr.holidays','summary_id',"Halfday Leaves"),
                }
    
    
    
hr_attendance_summary()

class hr_attendance_summary_lines(osv.osv):
    _name = "hr.attendance.summary.lines"
      
    def _get_attendances(self, cr, uid, ids, field_names, arg=None, context=None):
        result = {}
        if not ids: return result
        for idx in ids:
            sl=self.browse(cr,uid,idx)
            attendance_ids=self.pool.get('hr.attendance.summary').get_login_logout(cr,uid,sl.summary_id.employee_id.id,sl.name)
            attx=self.pool.get('hr.attendance').browse(cr,uid,attendance_ids)
            if len(attendance_ids)%2==1:
                attendance_ids.pop(len(attendance_ids)-1)
            result.update({idx:tuple(attendance_ids)})
        return result

    def onchange_name(self, cr, uid, ids, name,employee_id, context=None):
        res={'value':{}}
        if name and employee_id:
            attendance_ids=self.pool.get('hr.attendance').search(cr,uid,[('employee_id','=',employee_id),('name','>=',name+" 00:00:00"),('name','<=',name+" 23:59:59")])
            if attendance_ids:
                res['value'].update({'attendance_ids':attendance_ids})
        return res
    
    _columns = {
        'summary_id' : fields.many2one('hr.attendance.summary',"Employee"),
        'name' : fields.date('Date',required=True),
        'attendance_ids':fields.function(_get_attendances, method=True, type='one2many', relation='hr.attendance', string='Employee Attendance'),
        'sign_in':fields.datetime('Sign In'),
        'sign_out':fields.datetime('Sign Out'),
        'worktime':fields.char('Worktime',size=10),
        'late_time':fields.char('Late Time',size=10),
        'overtime':fields.char('Overtime',size=10),
        'extra_day':fields.char('Holiday Overtime',size=10),
        'longshift':fields.char('Longshift',size=10),
                }
hr_attendance_summary_lines()

class hr_absence_reason_summary_lines(osv.osv):
    _name = 'hr.absence.reason.summary.lines'
    
    _columns = {
            'name'          : fields.char('Name',size=300,readonly=False),
            'summary_id'    : fields.many2one('hr.attendance.summary', 'Summary ID'),
            'date'          : fields.date('date'),
            'reason'        : fields.many2one('absence.reason', 'Reason'),
                }
    
hr_absence_reason_summary_lines()

class hr_absence_summary_lines(osv.osv):
    _name="hr.absence.summary.lines"
    _columns = {
        'name':fields.date("Date"),
        'type':fields.selection([('with_reason','With Reason'),('no_reason','Absent')],'Type'),
        'summary_id':fields.many2one('hr.attendance.summary',"Summary ID"),
        'leave_id':fields.many2one('hr.holidays',"Leave ID"),
        'description':fields.text('Description'),
                }
    def write(self, cr, uid, ids, vals, context=None):
        hol_stat=self.pool.get('hr.holidays.status').search(cr,uid,[('name','like','Annual Leave')])
        if hol_stat:
            context.update({'holiday_status_id':hol_stat[0]})
        res = super(hr_absence_summary_lines, self).write(cr, uid, ids, vals, context=context)
        return res
    
    def create(self, cr, uid, vals, context=None):
        print "KKKKKKKKKKKKKKKKKKK"
        hol_stat=self.pool.get('hr.holidays.status').search(cr,uid,[('name','like','Annual Leave')])
        print "MMMMMMMMMMMMMM", hol_stat[0]
        if hol_stat:
            context.update({'holiday_status_id':hol_stat[0]})
        res = super(hr_absence_summary_lines, self).create(cr, uid, vals, context=context)
        return res
    
hr_absence_summary_lines()

class hr_spt_summary(osv.osv):
    _name = "hr.spt.summary"
    _columns = {
        'name':fields.date("Date"),
        'summary_id':fields.many2one('hr.attendance.summary',"Summary ID"),
        'spt_id':fields.many2one('hr.spt',"SPT"),
        'description':fields.text('Description'),
                }
hr_spt_summary()

class hr_attendance(osv.osv):
    _inherit = "hr.attendance"
    
    def _day_compute(self, cr, uid, ids, fieldnames, args, context=None):
        res = dict.fromkeys(ids, '')
        for obj in self.browse(cr, uid, ids, context=context):
            add_hour    = datetime.datetime.strptime(obj.name,"%Y-%m-%d %H:%M:%S")+timedelta(hours=7)
            res[obj.id] = time.strftime('%Y-%m-%d', time.strptime(str(add_hour), '%Y-%m-%d %H:%M:%S'))
            #t2          = datetime.datetime.strptime(obj.name,"%Y-%m-%d %H:%M:%S")+timedelta(hours=7)
        return res
    
    def _altern_si_so(self, cr, uid, ids, context=None):
        """ Alternance sign_in/sign_out check.
            Previous (if exists) must be of opposite action.
            Next (if exists) must be of opposite action.
        """
        for att in self.browse(cr, uid, ids, context=context):
            # search and browse for first previous and first next records
            prev_att_ids = self.search(cr, uid, [('employee_id', '=', att.employee_id.id), ('name', '<', att.name), ('action', 'in', ('sign_in', 'sign_out'))], limit=1, order='name DESC')
            next_add_ids = self.search(cr, uid, [('employee_id', '=', att.employee_id.id), ('name', '>', att.name), ('action', 'in', ('sign_in', 'sign_out'))], limit=1, order='name ASC')
            prev_atts = self.browse(cr, uid, prev_att_ids, context=context)
            next_atts = self.browse(cr, uid, next_add_ids, context=context)
            # check for alternance, return False if at least one condition is not satisfied
            if prev_atts and prev_atts[0].action == att.action: # previous exists and is same action
                return False
            if next_atts and next_atts[0].action == att.action: # next exists and is same action
                return True
            if (not prev_atts) and (not next_atts) and att.action != 'sign_in': # first attendance must be sign_in
                return False
        return True
    
    _columns = {
        'summary_line_id':fields.many2one('hr.attendance.summary.lines','Summary Line ID'),
        'day': fields.function(_day_compute, type='char', string='Day', store=True, select=1, size=32),
        'id_import'     : fields.many2one('attendance.import', 'ID Import', ondelete='cascade'),
                }
hr_attendance()

class hr_holidays(osv.osv):
    _inherit="hr.holidays"
    _columns={
        'summary_id':fields.many2one('hr.attendance.summary','Attendance Summary'),
              }
hr_holidays()