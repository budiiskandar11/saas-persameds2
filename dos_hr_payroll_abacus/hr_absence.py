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

class hr_absence(osv.osv):
    _name = "hr.absence"
    
    _columns = {
            'name'          : fields.char('Name',size=300,readonly=False),
            'employee_id'   : fields.many2one('hr.employee', 'Employee'),
            'date'          : fields.date('date'),
            'reason'        : fields.many2one('absence.reason', 'Reason'),
            'id_import'     : fields.many2one('attendance.import', 'ID Import', ondelete='cascade'),
                }
    
hr_absence()