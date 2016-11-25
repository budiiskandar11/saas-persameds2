import time

from openerp.osv import fields, osv
from openerp.tools.translate import _

class asset_register_merge(osv.osv_memory):
    _name = "asset.register.merge"
    _description = "Asset Register Merge"
    
    _columns = {
                }
    
    def merge_asset_register(self, cr, uid, ids, context=None):
       
        asset_reg_obj = self.pool.get('asset.register')
        mod_obj =self.pool.get('ir.model.data')
        if context is None:
            context = {}
            
        print "context.get('active_ids',[])*****************8", context
        #raise osv.except_osv(_('Error!'), _('XXXXXXXX123'))
        asset_reg_obj.check_asset_register_merge(cr, uid, context.get('active_ids',[]), context)
        allorders = asset_reg_obj.asset_register_merge(cr, uid, context.get('active_ids',[]), context)
        
        return True
        return {
            'domain': "[('id','in', [" + ','.join(map(str, allorders.keys())) + "])]",
            'name': _('Asset Register'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'asset.register',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'search_view_id': id['res_id']
        }
    
asset_register_merge()
    
    