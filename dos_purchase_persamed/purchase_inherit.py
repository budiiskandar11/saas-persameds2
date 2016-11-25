import pytz
from openerp import SUPERUSER_ID, workflow
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import attrgetter
from openerp.tools.safe_eval import safe_eval as eval
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.osv.orm import browse_record_list, browse_record, browse_null
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
import time

class purchase_order(osv.osv):
    _inherit = 'purchase.order'

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
                'disc_total' : 0.0,
                'add_amount': 0.0,
                'gross_total': 0.0,
            }
            val = val1 = add_amount = val2 = val4 = 0.0
            
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
               val1 += line.price_subtotal
               val2 += line.price_unit * line.product_qty
               val4 += (line.price_unit * ((line.diskon or 0.0) / 100.0)) * line.product_qty 
               for c in self.pool.get('account.tax').compute_all(cr, uid, line.taxes_id, line.price_unit * (1-(line.diskon or 0.0)/100.0), line.product_qty, line.product_id, order.partner_id)['taxes']:
                    val += c.get('amount', 0.0)
            if order.add_amount:
               add_amount = order.add_amount
            print ">>>>>>>>>>>>><<<",   add_amount  
            res[order.id]['gross_total']=cur_obj.round(cr, uid, cur, val2) 
            res[order.id]['add_amount']=cur_obj.round(cr, uid, cur, add_amount) 
            res[order.id]['disc_total']=cur_obj.round(cr, uid, cur, val4)  
            res[order.id]['amount_tax']=cur_obj.round(cr, uid, cur, val)
            res[order.id]['amount_untaxed']=cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_total']=res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']+ res[order.id]['add_amount']
        return res
    
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('purchase.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()



    _columns = {
        'freight_metode'        : fields.selection([('Air Freight','Air Freight'),
                                                    ('Sea Freight','Sea Freight'),
                                                    ('Vehicle','Vehicle'),
                                                    ]
                                                   ,'Shipping Via'),
        'add_amount' : fields.float('Additional'),
        'add_reason' : fields.char('Desc', size=64),
        'gross_total' : fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Gross Total',
            store={
                'purchase.order.line': (_get_order, None, 10),}, multi="sums", help="The amount without tax", track_visibility='always'),
        'disc_total' : fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total Discount',
            store={
                'purchase.order.line': (_get_order, None, 10),}, multi="sums", help="The amount without tax", track_visibility='always'),
        'amount_untaxed': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Untaxed Amount',
            store={
                'purchase.order.line': (_get_order, None, 10),
            }, multi="sums", help="The amount without tax", track_visibility='always'),
        'amount_tax': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Taxes',
            store={
                'purchase.order.line': (_get_order, None, 10),
            }, multi="sums", help="The tax amount"),
        'amount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total',
            store={
                'purchase.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','add_amount'], 10),   
                'purchase.order.line': (_get_order, None, 10),
            },multi="sums", help="The amount"),
        'port_id'   : fields.many2one('shipping.port','Port'),
        'inco'  : fields.boolean('Incoterm ?'),
        'shipping_int' : fields.char('Shipping Instruction', size=256),    
                
                }
    _defaults ={
                'freight_metode' : 'Vehicle',
                }
  
    def button_dummy(self, cr, uid, ids, context=None):
        return True
    
    def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
        """Collects require data from purchase order line that is used to create invoice line
        for that purchase order line
        :param account_id: Expense account of the product of PO line if any.
        :param browse_record order_line: Purchase order line browse record
        :return: Value for fields of invoice lines.
        :rtype: dict
        """
        
        
        return {
            'name': order_line.name,
            'account_id': account_id,
            'price_unit': order_line.price_unit or 0.0,
            'quantity': order_line.product_qty,
            'product_id': order_line.product_id.id or False,
            'uos_id': order_line.product_uom.id or False,
            'discount': order_line.diskon or 0.0,
            'invoice_line_tax_id': [(6, 0, [x.id for x in order_line.taxes_id])],
            'account_analytic_id': order_line.account_analytic_id.id or False,
            'purchase_line_id': order_line.id,
        }
    
    def action_invoice_create(self, cr, uid, ids, context=None):
        """Generates invoice for given ids of purchase orders and links that invoice ID to purchase order.
        :param ids: list of ids of purchase orders.
        :return: ID of created invoice.
        :rtype: int
        """
        context = dict(context or {})
        property_obj = self.pool.get('ir.property')
        inv_obj = self.pool.get('account.invoice')
        inv_line_obj = self.pool.get('account.invoice.line')

        res = False
        uid_company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
        for order in self.browse(cr, uid, ids, context=context):
            context.pop('force_company', None)
            if order.company_id.id != uid_company_id:
                #if the company of the document is different than the current user company, force the company in the context
                #then re-do a browse to read the property fields for the good company.
                context['force_company'] = order.company_id.id
                order = self.browse(cr, uid, order.id, context=context)
            
            # generate invoice line correspond to PO line and link that to created invoice (inv_id) and PO line
            inv_lines = []
            for po_line in order.order_line:
                if po_line.state == 'cancel':
                    continue
                acc_id = self._choose_account_from_po_line(cr, uid, po_line, context=context)
                inv_line_data = self._prepare_inv_line(cr, uid, acc_id, po_line, context=context)
                inv_line_id = inv_line_obj.create(cr, uid, inv_line_data, context=context)
                inv_lines.append(inv_line_id)
                po_line.write({'invoice_lines': [(4, inv_line_id)]})

            
            # get invoice data and create invoice
            inv_data = self._prepare_invoice(cr, uid, order, inv_lines, context=context)
            inv_id = inv_obj.create(cr, uid, inv_data, context=context)

            # compute the invoice
            inv_obj.button_compute(cr, uid, [inv_id], context=context, set_total=True)

            # tambahan untuk add ammount
            inv_add = {}
            if order.add_amount > 0 :
               acc_id = property_obj.get(cr, uid, 'property_account_expense_categ', 'product.category', context=context).id
               print ">>>>>>>>>>>>>>", acc_id
               inv_add = {
                            'name': order.add_reason or 'Additional Cost',
                            'account_id': acc_id,
                            'price_unit': order.add_amount or 0.0,
                            'quantity': 1, 
                            'invoice_id' : inv_id
                            #'product_id': order_line.product_id.id or False,
                            #'uos_id': order_line.product_uom.id or False,
                            #'discount': order_line.diskon or 0.0,
                            #'invoice_line_tax_id': [(6, 0, [x.id for x in order_line.taxes_id])],
                            #'account_analytic_id': order_line.account_analytic_id.id or False,
                            #'purchase_line_id': order_line.id, 
                          } 
               inv_line_obj.create(cr, uid, inv_add, context=context)
            
            # Link this new invoice to related purchase order
            order.write({'invoice_ids': [(4, inv_id)]})
            res = inv_id
        return res
  
purchase_order()

class purchase_order_lines(osv.osv):
    _inherit = 'purchase.order.line'
    
    def _amount_line(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        disc = subtot= 0.0
        for line in self.browse(cr, uid, ids, context=context):
            taxes = tax_obj.compute_all(cr, uid, line.taxes_id, line.price_unit, line.product_qty, line.product_id, line.order_id.partner_id)
            cur = line.order_id.pricelist_id.currency_id
            disc = line.price_unit * ((line.diskon or 0.0) / 100.0) * line.product_qty
            subtot = taxes['total'] - disc
            res[line.id] = cur_obj.round(cr, uid, cur, subtot)
        return res
    
    
    _columns = {
                'diskon'    : fields.float('Disc'),
                'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
                }
purchase_order_lines()

class shipping_port(osv.osv):
    _name = "shipping.port"
    _columns = {
                'name'  : fields.char('Port'),
                'code'  : fields.char('Code'),
                
                }

