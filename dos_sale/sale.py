from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import openerp.addons.decimal_precision as dp
from openerp import workflow

class sale_order(osv.Model):
    _inherit    = "sale.order"
    
    def _amount_all_wrapper(self, cr, uid, ids, field_name, arg, context=None):
        """ Wrapper because of direct method passing as parameter for function fields """
        return self._amount_all(cr, uid, ids, field_name, arg, context=context)
    
    def _amount_line_tax(self, cr, uid, line, context=None):
        val = 0.0
        line_obj = self.pool['sale.order.line']
        price = line_obj._calc_line_base_price(cr, uid, line, context=context)
        qty = line_obj._calc_line_quantity(cr, uid, line, context=context)
        for c in self.pool['account.tax'].compute_all(
                cr, uid, line.tax_id, price, qty, line.product_id,
                line.order_id.partner_id)['taxes']:
            val += c.get('amount', 0.0)
        return val
    
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'gross_total': 0.0,
                'discount_total': 0.0,
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
            }
            val = val1 = val3 = 0.0
            total_disc = 0.0
            disc = 0.0
            disc_amt = 0.0
            net_untaxed = 0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                val3 += line.price_unit * line.product_uom_qty
                disc += (line.price_unit * ((line.discount or 0.0) / 100.0)) * line.product_uom_qty
                disc_amt += line.disc_amount
                total_disc = disc + disc_amt
                net_untaxed += line.price_subtotal
                val += self._amount_line_tax(cr, uid, line, context=context)
                
            #==========================discount global==========================
            if order.amount_add_disc:
                if order.add_disc_type == 'percent':
                    total_disc = total_disc + (val3 * (order.amount_add_disc / 100.0))
                else:
                    total_disc = total_disc + order.amount_add_disc
                net_untaxed = val3 - total_disc
                
            res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val)
            res[order.id]['gross_total'] = cur_obj.round(cr, uid, cur, val3)
            res[order.id]['discount_total'] = cur_obj.round(cr, uid, cur, total_disc)
            res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, net_untaxed)
            res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
        return res

    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()

    _columns    = {
             'name': fields.char('Order Reference', required=True, copy=False,
             readonly=False, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, select=True),#additional discount
            'add_disc_type': fields.selection([('fix','Fix Amount'),('percent','Percentage (%)')], 'Type Discount', states={'confirmed': [('readonly', True)], 'approved': [('readonly', True)], 'done': [('readonly', True)]}),
            'amount_add_disc':fields.float('Additional Discount', digits_compute=dp.get_precision('Account'), states={'confirmed': [('readonly', True)], 'approved': [('readonly', True)], 'done': [('readonly', True)]}),      
            'date_valid': fields.date('Valid Date', required=False, readonly=True, select=True),
            'state': fields.selection([
                    ('draft', 'Draft'),
                    ('quot_approval', 'Waiting Approval'),
                    ('quot', 'Quotation'),
                    ('sent', 'Quotation Sent'),
                    ('waiting_date', 'Waiting Schedule'),
                    ('manual', 'Sale to Invoice'),
                    ('progress', 'Sales Order'),
                    ('invoice_except', 'Invoice Exception'),
                    ('shipping_except', 'Shipping Exception'),
                    ('cancel', 'Cancelled'),
                    ('done', 'Done'),
                    ], 'Status', readonly=True, track_visibility='onchange',
                    help="Gives the status of the quotation or sales order. \nThe exception status is automatically set when a cancel operation occurs in the processing of a document linked to the sales order. \nThe 'Waiting Schedule' status is set when the invoice is confirmed but waiting for the scheduler to run on the order date.", select=True),
                
            'gross_total': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Total',
                store={
                    'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','amount_add_disc'], 10),
                    'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty','disc_amount'], 10),
                },
                multi='sums', help="The amount gross total.", track_visibility='always'),
            'discount_total': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Total Disc',
                store={
                    'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','amount_add_disc'], 10),
                    'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty','disc_amount'], 10),
                },
                multi='sums', help="The amount discount total.", track_visibility='always'),
            'amount_untaxed': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Untaxed Amount',
                store={
                    'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','amount_add_disc'], 10),
                    'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty','disc_amount'], 10),
                },
                multi='sums', help="The amount without tax.", track_visibility='always'),
            'amount_tax': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Taxes',
                store={
                    'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','amount_add_disc'], 10),
                    'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty','disc_amount'], 10),
                },
                multi='sums', help="The tax amount."),
            'amount_total': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Net Total',
                store={
                    'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','amount_add_disc'], 10),
                    'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty','disc_amount'], 10),
                },
                multi='sums', help="The total amount."),
            'ketentuan'         : fields.text('Ketentuan Lain-Lain'),
            'contact'           : fields.char('Contact (Up:)'),
            'contact2'           : fields.char('Contact (Cc:)'),
            'quo_ref'           : fields.many2one('sale.order','Quotation Ref', readonly=True),
            'reason'              : fields.char('Reason'),
            'conf_date'        : fields.date('Order Confirmation Date'),
            'paket'             : fields.selection([('reg','Regular'),
                                                    ('paket','Paket')],'Paket ?')
       }
    
    _defaults = {
                 'ketentuan' : lambda self, cr, uid, context: self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.ketentuan,
                 'paket'    :'reg',
                 }
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('name', '/') == '/':
             vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'sale.quot', context=context) or '/'
        if vals.get('partner_id') and any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id', 'fiscal_position']):
            defaults = self.onchange_partner_id(cr, uid, [], vals['partner_id'], context=context)['value']
            if not vals.get('fiscal_position') and vals.get('partner_shipping_id'):
                delivery_onchange = self.onchange_delivery_id(cr, uid, [], vals.get('company_id'), None, vals['partner_id'], vals.get('partner_shipping_id'), context=context)
                defaults.update(delivery_onchange['value'])
            vals = dict(defaults, **vals)
        ctx = dict(context or {}, mail_create_nolog=True)
        new_id = super(sale_order, self).create(cr, uid, vals, context=ctx)
        self.message_post(cr, uid, [new_id], body=_("Quotation created"), context=ctx)
        return new_id
    
    def action_confirm_quot(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        config_obj = self.pool.get('sale.config.settings')
        company_obj = self.pool.get('res.company')
        company_sale_ids = company_obj.search(cr, uid, [])
        mod_obj = self.pool.get('ir.model.data')
        config_sale_ids = config_obj.search(cr, uid, [])
        
          
        if company_sale_ids:
            configs = company_obj.browse(cr, uid, company_sale_ids[0])
        for order in self.browse(cr, uid, ids):
            if order.order_line:
                for line in order.order_line:
                    if line.discount > configs.sale_discount_limit:
                        res = mod_obj.get_object_reference(cr, uid, 'dos_sale', 'view_sale_propose_approval_disc')
                        res_id = res and res[1] or False,
                
                        return {
                            'name': _('Propose Approval to Manager'),
                            'view_type': 'form',
                            'view_mode': 'form',
                            'view_id': [res_id],
                            'res_model': 'sale.propose.approval',
                            'context': "{}",
                            'type': 'ir.actions.act_window',
                            'nodestroy': True,
                            'target': 'new',
                            #'res_id': new_inv_ids and new_inv_ids[0] or False,
                        }
            name=order.name           
            if  not order.quo_ref :
                name = self.pool.get('ir.sequence').get(cr, uid, 'sale.order', context=context) or '/' 
               
            self.signal_workflow(cr, uid, ids, 'quot_confirm')
            #self.write(cr, uid, ids, {'state': 'quot'}, context=context)
            self.write(cr, uid, ids, {'state': 'quot','name' : name}, context=context)
        return True
    
    def quo_revision(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res         = {}
        data        = self.browse(cr, uid, ids)
        data_name   = data.name
        ref_name    = "/Rev"
        rev_ids     = False
        versi       = 0
        sale_order_line = self.pool.get('sale.order.line')
        if not data.quo_ref:
            for revision in self.browse(cr, uid, ids):
                print "-------",revision.name, ref_name, versi
                if revision.name:
                    from_name = revision.name
                else:
                    from_name = 'Quot'
                #         add_disc_type
#         amount_add_disc
                vals = {
                    'name'                  : from_name + ref_name + str(versi+1),
                    'partner_id'            : revision.partner_id.id,
                    'partner_invoice_id'    : revision.partner_invoice_id.id,
                    'partner_shipping_id'   : revision.partner_shipping_id.id,
                    'add_disc_type'         : revision.add_disc_type or '',
                    'amount_add_disc'       : revision.amount_add_disc or 0.0,
                    #'product_template_id'   : revision.product_template_id.id,
                    #'prod_attribute_id'     : revision.prod_attribute_id.id,
                    #'value_id'              : revision.value_id.id,
                    'quo_ref'               : revision.id,
                    'contact'               : revision.contact,
                    'contact2'              : revision.contact2,
                    'date_order'            : revision.date_order,
                    #'quotation_type'        : revision.quotation_type,
                    'state'                 : 'draft'
                }
                rev_ids = self.create(cr, uid ,vals)
            for line in revision.order_line:
                tax_ids=[]
                for tax in line.tax_id:
                    tax_ids.append(tax.id)
                sale_data = self.search(cr, uid, [('order_line','=',revision.id)])
                line_vals = {
                        'order_id': rev_ids,
                        'product_id': line.product_id.id,
                        'name': line.name,
                        'product_uom_qty': line.product_uom_qty,
                        'price_unit': line.price_unit,
                        'tax_id': [[6, False, tax_ids]],
                        'price_subtotal': line.price_subtotal,
                        'discount': line.discount,
                        #'main_sale_line': line.main_sale_line,
                        'sequence': line.sequence,
                        #'product_categ_id': line.product_categ_id and line.product_categ_id.id or False
                }
                sale_order_line.create(cr, uid, line_vals,context=context)
        else:
            for revision in self.browse(cr, uid, ids):
                versi   = int(data_name[len(data_name) -1:]) + 1
                vals = {
                    'name'                  : data_name[:len(data_name)-1] + str(versi),
                    'partner_id'            : revision.partner_id.id,
                    'partner_invoice_id'    : revision.partner_invoice_id.id,
                    'partner_shipping_id'   : revision.partner_shipping_id.id,
                    'add_disc_type'         : revision.add_disc_type or '',
                    'amount_add_disc'       : revision.amount_add_disc or 0.0,
                    #'product_template_id'   : revision.product_template_id.id,
                    #'prod_attribute_id'     : revision.prod_attribute_id.id,
                    #'value_id'             : revision.value_id.id,
                    'quo_ref'               : revision.id,
                    'contact'               : revision.contact,
                    'contact2'              : revision.contact2,
                    'date_order'            : revision.date_order,
                    #'quotation_type'        : revision.quotation_type,
                    'state'                 : 'draft'
                }
                rev_ids = self.create(cr, uid ,vals)
            for line in revision.order_line:
                tax_ids=[]
                for tax in line.tax_id:
                    tax_ids.append(tax.id)
                sale_data = self.search(cr, uid, [('order_line','=',revision.id)])
                line_vals = {
                        'order_id'      : rev_ids,
                        'product_id'    : line.product_id.id,
                        'name'          : line.name,
                        'product_uom_qty'   : line.product_uom_qty,
                        'price_unit'        : line.price_unit,
                        'tax_id'            : [[6, False, tax_ids]],
                        'price_subtotal'    : line.price_subtotal,
                         'discount': line.discount,
                        #'main_sale_line': line.main_sale_line,
                        'sequence': line.sequence,
                        #'product_categ_id': line.product_categ_id and line.product_categ_id.id or False
                }
                sale_order_line.create(cr, uid, line_vals,context=context)
        
        if rev_ids:
            self.signal_workflow(cr, uid, ids, 'cancel')
            return {
                'name'      : _("Quotation Revision"),
                'view_type' : 'form',
                'view_mode' : 'form',
                'res_model' : 'sale.order',
                'res_id'    : rev_ids,
                'nodestroy' : False,
                'type'      : 'ir.actions.act_window',
                'target'    : 'blank',
                'context'   : context
                }
        else:
            return False
   
    def action_approve_quot(self, cr, uid, ids, context=None):
        
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        for order in self.browse(cr, uid, ids):
            self.pool.get('sale.order.line').write(cr, uid, [line.id for line in order.order_line if line.state != 'cancel'], {'state': 'quot'}, context=context)
            name=order.name  
            if  not order.quo_ref :
                name = self.pool.get('ir.sequence').get(cr, uid, 'sale.order', context=context) or '/' 
           # print"VVVCVVCVCVVCVCVCVCVCVCVCVCVC", name
            self.signal_workflow(cr, uid, ids, 'quot_confirm')
        
            self.write(cr, uid, ids, {'state': 'quot','name' : name}, context=context)
        return True
    
    def print_quotation_test(self, cr, uid, ids, context=None):
        #super(sale_order, self).print_quotation(cr, uid, ids, context=context
        '''
        This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        #super(sale_order, self).signal_quotation_sent(cr, uid, ids, context=context)
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        self.pool.get('sale.order').signal_quotation_sent(cr, uid, ids)
        return self.pool['report'].get_action(cr, uid, ids, 'dos_new_quotation_report', context=context)
    
    def print_quotation(self, cr, uid, ids, context=None):
        '''
        This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        self.signal_workflow(cr, uid, ids, 'quotation_sent')
        return self.pool['report'].get_action(cr, uid, ids, 'dos_new_quotation_report', context=context)
       
#     def print_quotation(self, cr, uid, ids, context=None):
#         '''
#         This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
#         '''
#         assert len(ids) == 1, 'This option should only be used for a single id at a time'
#         wf_service = netsvc.LocalService("workflow")
#         wf_service.trg_validate(uid, 'sale.order', ids[0], 'quotation_sent', cr)
#         datas = {
#                  'model': 'sale.order',
#                  'ids': ids,
#                  'form': self.read(cr, uid, ids[0], context=context),
#         }
#         return {'type': 'ir.actions.report.xml', 'report_name': 'dos.new.quotation', 'datas': datas, 'nodestroy': True}
sale_order()

class sale_order_line(osv.Model):
    _inherit    = "sale.order.line"
    
    def _calc_line_base_price(self, cr, uid, line, context=None):
        
        return (line.price_unit * (1 - (line.discount or 0.0) / 100.0)-line.disc_amount)
    
    def _calc_line_quantity(self, cr, uid, line, context=None):
        return line.product_uom_qty
    
    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):  
            price = self._calc_line_base_price(cr, uid, line, context=context)
            qty = self._calc_line_quantity(cr, uid, line, context=context)
            taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, qty,
                                        line.product_id,
                                        line.order_id.partner_id)
            cur = line.order_id.pricelist_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
        return res
    
    _columns    = {
                   'main_unit': fields.boolean('Main'),
                   'state': fields.selection(
                [('cancel', 'Cancelled'),('draft', 'Draft'),('quot', 'Quotation'),('confirmed', 'Confirmed'),('exception', 'Exception'),('done', 'Done')],
                'Status', required=True, readonly=True, copy=False,
                help='* The \'Draft\' status is set when the related sales order in draft status. \
                    \n* The \'Confirmed\' status is set when the related sales order is confirmed. \
                    \n* The \'Exception\' status is set when the related sales order is set as exception. \
                    \n* The \'Done\' status is set when the sales order line has been picked. \
                    \n* The \'Cancelled\' status is set when a user cancel the sales order related.'),
                   'disc_amount' : fields.float('Disc. Amt'),
                   'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
                   'num'    : fields.char('Seq'),
            }
    
    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        invoice_line = super(sale_order_line, self)._prepare_order_line_invoice_line(cr, uid, line,account_id=False, context=context)
#         add_disc_type
#         amount_add_disc
#         gross_total
#         ketentuan
#         contact_id
#         quo_ref
        invoice_line['disc_amount'] = line.disc_amount or 0.0
       
        return invoice_line
    
sale_order_line()    
