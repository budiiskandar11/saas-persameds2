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
import pytz

class bpjs_generate(osv.osv_memory):
    _name = 'bpjs.generate'
    
    _columns = {
            'name'       : fields.char('Desciptions',size=32, required=True),
            'date_from'  : fields.date('Date From', required=True),
            'date_to'    : fields.date('Date To', required=True),
                }
    
    def bpjs_generate(self, cr, uid, ids, context=None):
        for wiz in self.browse(cr, uid, ids, context=None):
            print "OOOOOOOOOOOOOOOOOOOOOOOO", wiz.date_from
            date_from = wiz.date_from
            date_to = wiz.date_to
        
        
        bpjs_register_obj   = self.pool.get('hr.bpjs.register')
        bpjs_tk_obj         = self.pool.get('hr.bpjs.tk')
        bpjs_kes_obj        = self.pool.get('hr.bpjs.kes')
        bpjs_dplk_obj       = self.pool.get('hr.dplk')
        
        bpjs_search = bpjs_register_obj.search(cr, uid, [('state','=','registered')])
        
        for val in bpjs_register_obj.browse(cr, uid, bpjs_search):
            print "Nama Karyawan------>>", val.name.name
            if val.bpjs_tk_member == True :
                data = {
                        'jnumber'       : val.bpjs_tk_number,
                        'contract_id'   : val.contract_id.id,
                        'name'          : val.name.id,
                        'date_from'     : date_from,
                        'date_to'       : date_to,
                        'reg_date'      : val.reg_date,
                        'jht'           : val.jht,
                        'jkk'           : val.jkk,
                        'jk'            : val.jk,
                        }
                bpjs_tk_obj.create(cr, uid, data, context=None)
                
            if val.bpjs_kes_member == True :
                data = {
                        'jnumber'       : val.bpjs_kes_number, 
                        'contract_id'   : val.contract_id.id,
                        'name'          : val.name.id,
                        'date_from'     : date_from,
                        'date_to'       : date_to,
                        'reg_date'      : val.reg_date,
                        'jpk'           : val.jpk,
                        }
                bpjs_kes_obj.create(cr, uid, data, context=None)
                
            if val.dplk_member == True :
                data = {
                        'jnumber'       : val.dplk_number, 
                        'contract_id'   : val.contract_id.id,
                        'name'          : val.name.id,
                        'date_from'     : date_from,
                        'date_to'       : date_to,
                        'reg_date'      : val.reg_date,
                        'dplk'          : val.dplk,
                        }
                bpjs_dplk_obj.create(cr, uid, data, context=None)
        
        return True

bpjs_generate()