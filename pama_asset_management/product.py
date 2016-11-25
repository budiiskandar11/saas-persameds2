from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools.safe_eval import safe_eval as eval
import openerp.addons.decimal_precision as dp
from openerp.tools.float_utils import float_round
from openerp.exceptions import except_orm

class product_template(osv.osv):
    _inherit = 'product.template'
    
    _columns = {
            'tobe_asset'        : fields.selection([('yes', 'Asset'), ('no', 'Stock'), ('cost', 'Direct Cost')], 'Asset/Stock/Cost',),
            'asset_group_id'    : fields.many2one('account.asset.category', 'Asset Group', ),
            'asset_category_id' : fields.many2one('account.asset.group', 'Asset Categories', ),
            'asset_class_id'    : fields.many2one('account.asset.class', 'Asset Class', ),
                }
    
    _defaults = {
            'tobe_asset' : 'no',
                 }

product_template()