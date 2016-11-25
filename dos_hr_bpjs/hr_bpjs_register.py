import time
import datetime
from datetime import date

from datetime import timedelta
from dateutil import relativedelta

from openerp import api, tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

from openerp.tools.safe_eval import safe_eval as eval

class hr_bpjs_register(osv.osv):
    _name = 'hr.bpjs.register'
    
    _columns = {
            'name'              : fields.many2one('hr.employee','Employee Name',),
            'reg_date'          : fields.date('Registered Date',readonly=True,states={'draft':[('readonly',False)]}),
            
            'bpjs_tk_member'    : fields.boolean('BPJS Ketenagakerjaan Member'),
            'bpjs_tk_number'    : fields.char('BPJS TK Number',size=32,required=False,readonly=True, states={'draft':[('readonly',False)]}),
            'jht'               : fields.boolean('Jaminan Hari Tua (JHT)',help='Check this box for JHT',required=True,readonly=True,states={'draft':[('readonly',False)]}),
            'jkk'               : fields.boolean('Jaminan Kecelakaan Kerja (JKK)',help='Check this box for JKK',states={'draft':[('readonly',False)]}),
            'jk'                : fields.boolean('Jaminan Kematian (JKM)',help='Check this box for JK',readonly=True,states={'draft':[('readonly',False)]}),
            'jk_pensiun'        : fields.boolean('Dana Pensiun',help='Check this box for JK',readonly=True,states={'draft':[('readonly',False)]}),
            
            'bpjs_kes_member'   : fields.boolean('BPJS Kesehatan Member'),
            'bpjs_kes_number'   : fields.char('BPJS Kes Number',size=32,required=False,readonly=True, states={'draft':[('readonly',False)]}),
            'jpk'               : fields.boolean('Jaminan Kesehatan',help='Check this box for JPK',readonly=True,states={'draft':[('readonly',False)]}),
            
            'dplk_member'       : fields.boolean('DPLK Member'),
            'dplk_number'       : fields.char('BPJS Kes Number',size=32,required=False,readonly=True, states={'draft':[('readonly',False)]}),
            'dplk'              : fields.boolean('DPLK',help='Check this box for JK',readonly=True,states={'draft':[('readonly',False)]}),
            
            'contract_id'       : fields.many2one('hr.contract', 'Contract',readonly=True,states={'draft':[('readonly',False)]}),
            'state'             : fields.selection([('draft','Draft'),('registered','Registered'), ('non_active','Non Active')],'State',readonly=True),
                }
    
    _defaults ={
                'state'         : 'draft',
                }
    
    def register(self,cr,uid,ids,context=None):
        self.write(cr,uid,ids,{'state':'registered'})
        return True
    
    def non_active(self,cr,uid,ids,context=None):
        self.write(cr,uid,ids,{'state':'non_active'})
        return True
    
    def modify(self,cr,uid,ids,context=None):
        self.write(cr,uid,ids,{'state':'draft'})
        return True
    
    def cancel(self,cr,uid,ids,context=None):
        self.write(cr,uid,ids,{'state':'draft'})
        return True
    
hr_bpjs_register()