
import itertools
from lxml import etree
from openerp.osv import fields, osv
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp

class company(osv.osv):
    _inherit = "res.company"
    _columns = {
        'npwp':fields.char('NPWP',size=64),
        'kode_transaksi': fields.char('kode transaksi', size=2),
        'kode_status': fields.char('kode status', size=1),
        'kode_cabang': fields.char('kode cabang', size=3),
        }
company()

class res_partner(osv.osv):
    _inherit = 'res.partner'
    _description = 'res partner'
    
    def onchange_npwp(self, cr, uid, ids, npwp, context=None):
        res = {}
        vals = {}
        if npwp == False:
            return res
        elif len(npwp)==20:
            return {"value":npwp}
        elif len(npwp)==15:
            formatted_npwp = npwp[:2]+'.'+npwp[2:5]+'.'+npwp[5:8]+'.'+npwp[8:9]+'-'+npwp[9:12]+'.'+npwp[12:15]
            vals={
                  "npwp" : formatted_npwp
            }
            return {"value":vals}
        else:
            warning = {
                'title': _('Warning'),
                'message': _('Wrong Format must 15 digit'),
            }
            return {'warning': warning, 'value' : {'npwp' : False}}
        return res
    
    
    _columns = {
        'npwp': fields.char('NPWP', size=128),
        'kawasan': fields.selection([('yes','YES'),('no','NO')], 'Kawasan', help=''),
        'kode_transaksi': fields.char('kode transaksi', size=2),
#         'kode_status': fields.char('kode status', size=1),
    }
    
    _defaults = {
                 }
res_partner()