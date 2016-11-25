
from openerp.osv import fields, osv



class stock_picking(osv.osv):
    _inherit = "stock.picking"
    
    _columns = {
       #'move_lines': fields.one2many('stock.move', 'picking_id', 'Internal Moves', states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, copy=True),
        'pack_operation_ids': fields.one2many('stock.pack.operation', 'picking_id', states={'done': [('readonly', False)], 'cancel': [('readonly', True)]}, string='Related Packing Operations'),
        'is_install' : fields.boolean('Need Installation ?'),
        'install_created' : fields.boolean('From Inst. Created'),   
    }
    _defaults = {
                 'install_created':False,
                 }

    def create_installation(self,cr,uid,ids,context=None):
        print "kdkkdkdkdkkdkd.......kesini"
        move_obj = self.pool.get('stock.move')
        picking_obj = self.pool.get('stock.picking')
        install_obj = self.pool.get('installation')
        result={}
        context = dict(context or {})
        vals = {}
        for move in self.browse(cr, uid, ids) :
            if move.is_install == True :
                for line in move.pack_operation_ids :
#                 if line.to_install == True :
           
                    vals = {
                        'customer_id': move.partner_id.id or '',
                        'product_id': line.product_id.id or '',
                        'sale_ref'  : move.group_id.name or '', 
                        'move_ref'  : line.picking_id.name or False,
                        'default_code': line.product_id.default_code or False,
                        'lot_number' : line.lot_id.id or False,
                        'brand_id': line.product_id.product_brand_id.id or False,
                        'man_country' :line.product_id.product_country.id or False,
                    }
             
       
                inst_id = install_obj.create(cr, uid, vals, context=context)
        #asset_number = asset_obj.browse(cr, uid, asset_id, context=None).asset_number
        self.write(cr, uid, ids, {'install_created' : True}, context=None)       
       
        return True

class stock_move(osv.osv):
    _inherit = 'stock.move'
    _columns ={
               'to_install' : fields.boolean('To Install ?'),
               }
    
class stock_pack_operation(osv.osv):
    _inherit = 'stock.pack.operation'
    _columns ={
               'to_install' : fields.boolean('To Install ?'),
               }