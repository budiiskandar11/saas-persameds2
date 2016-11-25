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

class hr_benefit(osv.osv):
    _name = 'hr.benefit'
    
    _columns = {
            'name'                  : fields.char('Description',size=128,),
            'type'                  : fields.selection([('bonus','Bonus'),
                                                       ('benefit',"Benefit"),
                                                       ('thr','THR'),
                                                       ('spp','SPP'),
                                                       ('insentif','Insentif'),
                                                       ('gaji13','Gaji Ke-13'),
                                                       ('reward','Reward Kinerja'),
                                                       ('uniform','Tunjangan Uniform'),
                                                       ],"Type"),
            'create_date'           : fields.date('Create Date',required=True),
            'effective_period'      : fields.many2one('account.period', 'Effective Period'),
            'employee_id'           : fields.many2one('hr.employee', 'Employee'),
            'percentage'            : fields.float('Percentage %'),
            'amount'                : fields.float('Amount'),
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
    
hr_benefit()