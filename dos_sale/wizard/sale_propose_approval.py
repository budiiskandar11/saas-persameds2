##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class sale_propose_approval(osv.osv_memory):
    _name = "sale.propose.approval"
    _description = "Sales Propose Approval"

    _columns = {
        'qtty': fields.integer('Quantity', readonly=True),
        'limit_disc': fields.float('Limit Disc %', digits=(16, 2), readonly=True),
    }
    
    def _get_advance_product(self, cr, uid, context=None):
        sale_obj = self.pool.get('sale.order')
        sale_ids = context.get('active_ids', [])
        config_obj = self.pool.get('res.company')
        config_sale_ids = config_obj.search(cr, uid, [])
        get_limit_disc = 0.0
        if config_sale_ids:
            config = config_obj.browse(cr, uid, config_sale_ids[0])
            get_limit_disc = config.sale_discount_limit
            
        for order in sale_obj.browse(cr, uid, sale_ids):
            count_line = 0.0
            if order.order_line:
                for line in order.order_line:
                    if line.discount > get_limit_disc:
                        count_line+=1
            return count_line
    
    def _get_limit_disc(self, cr, uid, context=None):
        config_obj = self.pool.get('res.company')
        config_sale_ids = config_obj.search(cr, uid, [])
        get_limit_disc = 0.0
        if config_sale_ids:
            config = config_obj.browse(cr, uid, config_sale_ids[0])
            get_limit_disc = config.sale_discount_limit
        return get_limit_disc
    
    _defaults = {
        'qtty': _get_advance_product,
        'limit_disc': _get_limit_disc,
    }

    def propose_approve(self, cr, uid, ids, context=None):
        """ propose approval to manager """
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        sale_obj = self.pool.get('sale.order')
        sale_ids = context.get('active_ids', [])
        sale_obj.signal_workflow(cr, uid, sale_ids, 'quot_approval')
        sale_obj.write(cr, uid, sale_ids, {'state': 'quot_approval'}, context=context)
        return {'type': 'ir.actions.act_window_close'}
    
    def bypass_approve(self, cr, uid, ids, context=None):
        """ by pass approval by manager """
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        sale_obj = self.pool.get('sale.order')
        sale_ids = context.get('active_ids', [])
        sale_obj.signal_workflow(cr, uid, sale_ids, 'quot_confirm')
        for order in sale_obj.browse(cr, uid, sale_ids):
            name=order.name  
            if  not order.quo_ref :
                name = self.pool.get('ir.sequence').get(cr, uid, 'sale.order', context=context) or '/' 
                sale_obj.write(cr, uid, sale_ids, {'name': name}, context=context)
        sale_obj.write(cr, uid, sale_ids, {'state': 'quot'}, context=context)
        return {'type': 'ir.actions.act_window_close'}
        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
