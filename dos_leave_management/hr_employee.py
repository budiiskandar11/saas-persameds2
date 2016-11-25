import datetime
import math
import time
from operator import attrgetter

from openerp.exceptions import Warning
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import workflow

class hr_employee(osv.osv):
    _inherit = 'hr.employee'
    
    _columns = {
            'leave_job_approval': fields.many2one('hr.job', "Leave Need Approval", select=True,),
                }
    
hr_employee()