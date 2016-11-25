import datetime
import math
import time
from operator import attrgetter

from openerp.exceptions import Warning
from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import workflow

class bit_payment(osv.osv):
    _name = 'bit.payment'
    
    _columns = {
            'name'                  : fields.char('Description',size=128,),
            'leave_id'              : fields.many2one('hr.holidays.propose', 'Holidays Doc'),
            'create_date'           : fields.date('Create Date',required=True),
            'effective_period'      : fields.many2one('account.period', 'Effective Period'),
            'employee_id'           : fields.many2one('hr.employee', 'Employee'),
            'percentage'            : fields.float('Percentage %'),
            'state'                 : fields.selection([('draft','Draft'),
                                                       ('confirm',"Confirm"),('cancel','Cancelled')],"State",readonly=True),
                }
    
    _defaults={
        'state'         : 'draft',
        'create_date'   : lambda *a:time.strftime('%Y-%m-%d'),
               }
    
    def confirm(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'confirm'},context)
    
    def cancel(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'cancel'},context)
    
    def set_to_draft(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'draft'},context)
    
bit_payment()