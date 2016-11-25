import time
from lxml import etree

from openerp.osv import fields, osv
from openerp.tools.translate import _

class contract_revision (osv.osv_memory):
    _name = 'contract.revision'
    
    _columns = {
            'name'          : fields.char('Contract Reference', size=128),
            'date_start'    : fields.date('Start Date',),
            'date_end'      : fields.date('End Date',),
            'wage'          : fields.float('Basic Salary'),
            'struct_id'     : fields.many2one('hr.payroll.structure', 'Salary Structure'),
            'type'          : fields.selection([('kenaikan', 'Kenaikan Grade'), 
                                               ('demosi', 'Demosi'),
                                               ('pengangkatan', 'Pengangkatan Tetap'),
                                               ('promosi', 'Promosi'),
                                               ('phk', 'PHK'),
                                               ], 'Renewal Option'),
                }
    
    def create_new_contract(self, cr, uid, ids, wizz, context=None):
        renewal_val = {}
        
        contract_obj = self.pool.get('hr.contract')
        for val in contract_obj.browse(cr, uid, context.get('active_ids'), context=context):
            print ">>>>>>>>>>", val.id
        
        if wizz['type'] in ('kenaikan','demosi','pengangkatan','promosi'):
            renewal_val = {
                    'name'          : wizz['name'],
                    'employee_id'   : val.employee_id.id,
                    'type_id'       : val.type_id.id,
                    'renewal_type'  : wizz['type'],
                    'job_id'        : val.job_id.id,
                    'prev_contract' : val.id,
                    'date_start'    : wizz['date_start'],
                    'date_end'      : wizz['date_end'],
                    'struct_id'     : wizz['struct_id'],
                    'wage'          : wizz['wage'],
                    'employee_status' : val.employee_status, 
                    'ptkp_id'       : val.ptkp_id.id,
                       }
            contract_obj.create(cr, uid, renewal_val, context=None)
            
        elif wizz['type'] in ('phk'):
            contract_obj.write(cr, uid, [val.id], {'employee_status' : 'terminate'})
        
        #raise osv.except_osv(_('Bad date'), _('End date could not be earlier than start date'))
        return True
    
    def confirm_renewal_contract(self, cr, uid, ids, context=None):
        wizz = {}
        for wizz in self.browse(cr, uid, ids, context=None):
            print "------------------->>", wizz.name
            
        wizz = {
            'name'          : wizz.name,
            'type'          : wizz.type,
            'date_start'    : wizz.date_start,
            'date_end'      : wizz.date_end,
            'struct_id'     : wizz.struct_id.id,
            'wage'          : wizz.wage,
                }
            
        #raise osv.except_osv(_('Bad date'), _('End date could not be earlier than start date'))
        return self.create_new_contract(cr, uid, ids, wizz, context)

contract_revision()