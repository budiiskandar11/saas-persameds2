from openerp.osv import osv,fields
from datetime import date
from datetime import datetime
import time
from openerp import tools

class holiday_year(osv.osv):
    _name       = "hr.holiday.year"
    _columns    = {
                   'name'       : fields.char('Holiday Name', size=128, required=True),
                   'year'       : fields.char('Year',size=4,readonly=True),
                   'month'      : fields.char('Month',size=16, readonly=True),
                   'date'       : fields.date('Date', required=True),
                   'note'       : fields.text('Description'),
                   'delay'      : fields.float('Duration'),
                   }
    _defaults = {
                 'delay':1.0,
                 }
    def create(self,cr,uid,vals,context=None):
        ttyme = datetime.fromtimestamp(time.mktime(time.strptime(vals['date'],"%Y-%m-%d")))
        vals['month']   = tools.ustr(ttyme.strftime('%B'))
        vals['year']    = tools.ustr(ttyme.strftime('%Y'))
        ids  =super(holiday_year,self).create(cr,uid,vals)
        return ids
    
    def write(self,cr,uid,ids,vals,context=None):
        date_key = "date"
        if date_key in vals.keys():
            ttyme = datetime.fromtimestamp(time.mktime(time.strptime(vals['date'],"%Y-%m-%d")))
            vals['month']   = tools.ustr(ttyme.strftime('%B'))
            vals['year']    = tools.ustr(ttyme.strftime('%Y'))
        write= super(holiday_year,self).write(cr,uid,ids,vals)
        return write
holiday_year()