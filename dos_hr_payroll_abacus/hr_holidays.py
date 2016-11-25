import datetime, time
from itertools import groupby
from operator import itemgetter

from openerp import netsvc
from openerp.osv import fields, osv
from openerp.tools.translate import _

from dateutil.relativedelta import relativedelta

#from dateutil import relativedelta
#from datetime import datetime,timedelta, date

#from datetime import datetime.datetime

def date_range(start, end):
    r = (end+datetime.timedelta(days=1)-start).days
    return [start+datetime.timedelta(days=i) for i in range(r)]

class hr_holidays(osv.osv):
    _inherit = "hr.holidays"
    
    def convert_timeformat(self,time_string):
        split_list = str(time_string).split('.')
        hour_part = split_list[0]
        mins_part = split_list[1]
        round_mins = int(round(float(mins_part) * 60,-2))
        converted_string = hour_part + ':' + str(round_mins)[0:2]
        return converted_string
    
    def onchange_date_from(self, cr, uid, ids, date_to, date_from,emp_id=None):
        result = {}
        if date_to and date_from:
            
            ####Reset to 00:00:00####
            date_from   = datetime.datetime.strptime(date_from,"%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d 00:00:00')
            date_to     = datetime.datetime.strptime(date_to,"%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d 00:00:00')
            
            end = datetime.datetime.strptime(date_to,"%Y-%m-%d %H:%M:%S")
            start = datetime.datetime.strptime(date_from,"%Y-%m-%d %H:%M:%S")
            
            dur = end - start
            dur = dur.days + 1
            
            print "Dur>>>>>>>>>>>>>>>>>>123", dur
            
            datelist = [ start + datetime.timedelta(days=x) for x in range(0,dur) ]
            libur = 0
            for date in datelist:
                print "AAAA", date
                print "xxxxx", date.strftime("%u")
                if date.strftime("%u")=="6" or date.strftime("%u")=="7":
                    libur = libur+1
                
            end1=start+datetime.timedelta(dur-1)
            print "selisih", (dur+1)-libur
            
            #########################
            
            #####Tanggal Merah#####
            holiday_year_obj    = self.pool.get('hr.holiday.year')
            holiday_year_search = holiday_year_obj.search(cr, uid, [('date','>=',date_from),('date','<=',date_to)])
            
            if holiday_year_search:
                for i in holiday_year_obj.browse(cr, uid, holiday_year_search):
                    date = datetime.datetime.strptime(i.date,"%Y-%m-%d").strftime('%Y-%m-%d')
                    date = datetime.datetime.strptime(date,"%Y-%m-%d")
                    print "date----------------->>", date, date.strftime("%u")
                    
                    if str(date.strftime("%u")) in ['1','2','3','4','5']:
                        print "date.strftime***************", date.strftime("%u")
                        libur = libur+1
            print "Libuurrrrrrrr", libur
            #######################
            
            if emp_id:
                emp_data=self.pool.get('hr.employee').browse(cr,uid,emp_id)
                contract_id=self.pool.get('hr.payslip').get_contract(cr,uid,emp_data,date_from,date_to,{})
                contract=self.pool.get('hr.contract').browse(cr,uid,contract_id)[0]
                #print "===============",contract
            diff_day = self._get_number_of_days(date_from, date_to)
            print "diff_day------------>>", diff_day
            dt_from=datetime.datetime.strptime(date_from,"%Y-%m-%d %H:%M:%S")
            dt_to=datetime.datetime.strptime(date_to,"%Y-%m-%d %H:%M:%S")
            late_diff=datetime.timedelta(seconds=0)
            for dd in date_range(dt_from, dt_to):
                if emp_id:
                    day={
                         'Monday':0,
                         'Tuesday':1,
                         'Wednesday':2,
                         'Thursday':3,
                         'Friday':4,
                         'Saturday':5,
                         'Sunday':6,
                         }
                    t2=datetime.datetime.strptime(date_to,"%Y-%m-%d %H:%M:%S")
                    t2dayofweek=day[t2.strftime("%A")]
                    querysignin="select min(hour_from) from resource_calendar_attendance where calendar_id=%s and dayofweek='%s'"%(contract.working_hours.id,t2dayofweek)
                    cr.execute(querysignin)
                    try:
                        res = dd.strftime("%Y-%m-%d")+" "+self.convert_timeformat(cr.fetchone()[0])+":00"
                    except:
                        res=False
                    if dd.strftime("%Y-%m-%d")==dt_to.strftime("%Y-%m-%d") and res:
                        late_diff=dt_to-datetime.datetime.strptime(res,"%Y-%m-%d %H:%M:%S")
                ####Leave Half Day####
                #if dd.strftime("%A")=="Saturday" or late_diff >= datetime.timedelta(hours=2):
                #    result['value'] = {
                #        'number_of_days_temp': round(diff_day)+0.5
                #    }
                #else:    
                #    result['value'] = {
                #        'number_of_days_temp': round(diff_day)+1
                #    }
                
                
                result['value'] = {
                        'number_of_days_temp': round(diff_day)+1 - libur,
                        'date_from' : date_from,
                        'date_to'   : date_to,  
                    }
                
            return result
        result['value'] = {
            'number_of_days_temp': 0,
            'date_from' : date_from,
            'date_to'   : date_to,
        }
        return result
    
hr_holidays