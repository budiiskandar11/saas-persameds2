
from openerp.osv import fields, osv



class stock_picking(osv.osv):
    _inherit = "stock.picking"
    
    def _total_pack(self, cr, uid, ids, name, args, context=None):
        res         = {}
        for pick in self.browse(cr, uid, ids, context=None):
            total_qty   = 0.0
            for line in pick.move_lines:
                total_qty += line.product_uom_qty
            res[pick.id] = total_qty
        return res
    
    _columns = {
        'date_transfered': fields.datetime('Date of Received', help="Date of Received by Customer", states={'done': [('readonly', True)], 'cancel': [('readonly', True)]}, copy=False),
        'carrier_tracking_ref' : fields.char(
                'Tracking Ref.',
                readonly=False,  # updated by wizard
                track_visibility='onchange',),
       'transport_mode' : fields.selection([('internal','Internal Transport'),
                                                    ('external','External Carrier'),
                                                   
                                                    ],
                                                string='Transport Mode',
                                                readonly=False,
                                                states={'draft': [('readonly', False)]}),
        'vehicle_no': fields.char('Vehicle No', size=64),
        'driver_name' : fields.char('Driver Name', size=64),
        'pack_no': fields.float('Qty Pack'),
        'total_item' : fields.function(_total_pack, method=True, type='float', string="Total Qty"),     
    }



class stock_move(osv.osv):
    _inherit = 'stock.move'
    _columns ={
               'product_desc' : fields.text('Description')
               }
    
    def onchange_product_id(self, cr, uid, ids, prod_id=False, loc_id=False, loc_dest_id=False, partner_id=False):
        """ On change of product id, if finds UoM, UoS, quantity and UoS quantity.
        @param prod_id: Changed Product id
        @param loc_id: Source location id
        @param loc_dest_id: Destination location id
        @param partner_id: Address id of partner
        @return: Dictionary of values
        """
        if not prod_id:
            return {}
        user = self.pool.get('res.users').browse(cr, uid, uid)
        lang = user and user.lang or False
        if partner_id:
            addr_rec = self.pool.get('res.partner').browse(cr, uid, partner_id)
            if addr_rec:
                lang = addr_rec and addr_rec.lang or False
        ctx = {'lang': lang}

        product = self.pool.get('product.product').browse(cr, uid, [prod_id], context=ctx)[0]
        uos_id = product.uos_id and product.uos_id.id or False
        result = {
            'name': product.partner_ref,
            'product_uom': product.uom_id.id,
            'product_uos': uos_id,
            'product_uom_qty': 1.00,
            'product_uos_qty': self.pool.get('stock.move').onchange_quantity(cr, uid, ids, prod_id, 1.00, product.uom_id.id, uos_id)['value']['product_uos_qty'],
            'product_desc' : product.description,
        }
        if loc_id:
            result['location_id'] = loc_id
        if loc_dest_id:
            result['location_dest_id'] = loc_dest_id
        return {'value': result}
    