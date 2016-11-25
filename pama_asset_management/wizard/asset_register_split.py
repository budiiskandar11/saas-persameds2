
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class asset_register_split_wiz(osv.osv_memory):
    _name = "asset.register.split.wiz"
    _description = "Asset Split"
    _columns = {
        'asset_register_id'   : fields.many2one('asset.register', 'Asset Register',),
        'original_value'      : fields.float('Amount Value', required=True,),  
        'asset_split_line'    : fields.one2many('asset.register.split.line.wiz', 'asset_register_id', 'Asset split Line'),
                }
    
    def split_asset_register(self, cr, uid, ids, context=None):
        asset_reg_obj = self.pool.get('asset.register')
        mod_obj =self.pool.get('ir.model.data')
        if context is None:
            context = {}
        
        for wiz in self.browse(cr, uid, ids, context=None):
            asset_register_id = wiz.asset_register_id.id
            print ">>>>>>>>>>>>>xx", asset_register_id
            for line in wiz.asset_split_line:
                amount_value = line.amount_value
                asset_reg_obj.copy_split(cr, uid, [asset_register_id], None, context={'asset_register_id':asset_register_id,'amount_value':amount_value})
            
            asset_reg_obj.unlink(cr, uid, asset_register_id)
            
        return True
    
    def default_get(self, cr, uid, fields, context=None):
        if context is None: context = {}
        res = super(asset_register_split_wiz, self).default_get(cr, uid, fields, context=context)
        asset_ids = context.get('active_ids', [])
        active_model = context.get('active_model')

        if not asset_ids or len(asset_ids) != 1:
            # Partial Picking Processing may only be done for one picking at a time
            return res
        assert active_model in ('asset.register'), 'Bad context propagation'
        asset_id, = asset_ids
        asset = self.pool.get('asset.register').browse(cr, uid, asset_id, context=context)
        items = []
        
        for asset in asset:
            asset_register_id   = asset.id
            original_value      = asset.purchase_value
            item = {
                'name'          : asset.name,
                'asset_class_id': asset.asset_class_id.id,
                'amount_value'  : asset.purchase_value
                    }
            if asset.name:
                items.append(item)
        res.update(asset_register_id=asset_register_id,original_value=original_value, asset_split_line=items)
        return res
    
asset_register_split_wiz()

class asset_register_split_line_wiz(osv.osv_memory):
    _name = "asset.register.split.line.wiz"
    _description = "Asset Split Line"
    _columns = {
        'asset_register_id' : fields.many2one('asset.register.split.wiz', 'Asset Class',),
        'name'              : fields.char('Asset Desctription', size=264),
        'asset_class_id'    : fields.many2one('account.asset.class', 'Asset Class',),
        'amount_value'      : fields.float('Amount Value', required=True,),  
                }
    
asset_register_split_line_wiz()
