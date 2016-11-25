# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2013 BroadTech IT Solutions.
#    (http://wwww.broadtech-innovations.com)
#    contact@boradtech-innovations.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
import datetime


class purchase_request(osv.osv):
    _name = 'purchase.request'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
            }
            val = val1 = 0.0
            cur = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.currency_id
            for line in order.order_line:
                val1 += line.price_subtotal
                for c in self.pool.get('account.tax').compute_all(cr, uid, line.taxes_id, line.price_unit, line.product_qty, line.product_id, order.partner_id)['taxes']:
                    val += c.get('amount', 0.0)
            res[order.id]['amount_tax']=cur_obj.round(cr, uid, cur, val)
            res[order.id]['amount_untaxed']=cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_total']=res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
        return res
    
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('purchase.request.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()
    
    
    STATE_SELECTION = [
        ('draft', 'Draft'),
        #('sent', 'RFQ'),
        #('bid', 'Bid Received'),
        ('confirmed', 'Waiting Validate'),
        ('approved', 'Validated'),
        #('except_picking', 'Shipping Exception'),
        #('except_invoice', 'Invoice Exception'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ]
    
    READONLY_STATES = {
        'confirmed': [('readonly', True)],
        'approved': [('readonly', True)],
        'done': [('readonly', True)]
    }
    
    _columns = {
        'name': fields.char('Order Reference', required=True, select=True, copy=False,
                            help="Unique number of the purchase request, "
                                 "computed automatically when the purchase request is created."),        
        'type'          : fields.selection([#('general',"General"),
                                            #('asset',"Asset"),
                                            #('asset_extra', "Low Value Assets"),
                                            #('import',"Import Transaction"),
                                            ('prepayment',"Prepayment (DP)"),
                                            ],"Type Request", required=True, readonly=True,states={'draft': [('readonly', False)]}),
        'partner_id':fields.many2one('res.partner', 'Supplier', required=True, states=READONLY_STATES,
            change_default=True, track_visibility='always'),
        'partner_ref': fields.char('Supplier Reference', states={'confirmed':[('readonly',True)],
                                                                 'approved':[('readonly',True)],
                                                                 'done':[('readonly',True)]},
                                   copy=False,
                                   help="Reference of the sales request or bid sent by your supplier. "
                                        "It's mainly used to do the matching when you receive the "
                                        "products as this reference is usually written on the "
                                        "delivery order sent by your supplier."),
        'create_date': fields.datetime('Creation Date', readonly=True, select=True, help="Date on which supplier prepayment is created."),
        'date_order':fields.datetime('Date Create', required=True, states={'confirmed':[('readonly',True)],
                                  'approved':[('readonly',True)]},
                                 select=True, help="Depicts the date where the Quotation should be validated and converted into a Purchase Request, by default it's the creation date.",
                                 copy=False),
        'date_due' : fields.date('Due Date'),
        'state': fields.selection(STATE_SELECTION, 'Status', readonly=True,
                                  help="The status of the purchase request or the quotation request. "
                                       "A request for quotation is a purchase request in a 'Draft' status. "
                                       "Then the order has to be confirmed by the user, the status switch "
                                       "to 'Confirmed'. Then the supplier must confirm the order to change "
                                       "the status to 'Approved'. When the purchase request is paid and "
                                       "received, the status becomes 'Done'. If a cancel action occurs in "
                                       "the invoice or in the receipt of goods, the status becomes "
                                       "in exception.",
                                  select=True, copy=False),
        'order_line': fields.one2many('purchase.request.line', 'order_id', 'Order Lines',
                                      states={'approved':[('readonly',True)],
                                              'done':[('readonly',True)]},
                                      copy=True),
        'invoice_ids': fields.many2many('account.invoice', 'payment_req_invoice_rel', 'payment_req_line_id',
                                        'payment_req_id', 'Invoices', copy=False,
                                        help="Invoices generated for a purchase request"),
        'amount_untaxed': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Untaxed Amount',
            store={
                'purchase.request.line': (_get_order, None, 10),
            }, multi="sums", help="The amount without tax", track_visibility='always'),
        'amount_tax': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Taxes',
            store={
                'purchase.request.line': (_get_order, None, 10),
            }, multi="sums", help="The tax amount"),
        'amount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total',
            store={
                'purchase.request.line': (_get_order, None, 10),
            }, multi="sums", help="The total amount"),
        'user_id'   : fields.many2one('res.users', "Created by",readonly=True, states={'draft': [('readonly', False)]}, index=True,
                       help="Creator"),
#         'employee_id': fields.many2one('hr.employee', "Responsible", readonly=True,states={'draft': [('readonly', False)]}, index=True,
#                        help="Employee who responsible for this transaction"),
        'company_id': fields.many2one('res.company', 'Company', required=True, select=1),
#         'department_id' : fields.many2one('hr.department','Department', readonly=True,states={'draft': [('readonly', False)]}, index=True,),
        'notes'         : fields.text('Notes', readonly=True,states={'draft': [('readonly', False)]}),
        'propose'       : fields.text('Propose', readonly=True,states={'draft': [('readonly', False)]}),
        'bank_id'       : fields.many2one('res.partner.bank', "Beneficiary Account", readonly=True,states={'draft': [('readonly', False)]}, index=True,),
        'npwp'          : fields.char('NPWP No', size=64, readonly=True,states={'draft': [('readonly', False)]}, index=True),
        'fiscal_position': fields.many2one('account.fiscal.position', 'Fiscal Position',readonly=True, states={'draft': [('readonly', False)]}, help="Default setting tax for this supplier, for example : if this supplier has PKP, then VAT is a must"),
        'payment_term_id'  : fields.many2one('account.payment.term', string='Payment Terms',
                                    readonly=True, states={'draft': [('readonly', False)]},
                        help="If you use payment terms, the due date will be computed automatically at the generation "
                             "of accounting entries. If you keep the payment term and the due date empty, it means direct payment. "
                             "The payment term may compute several due dates, for example 50% now, 50% in one month."),
        'supplier_name'          : fields.char('Supplier Name', size=64,readonly=True, states={'draft': [('readonly', False)]}, index=True),
        #'purchase_id' : fields.many2one('purchase.order', 'Purchase Order'),
        'prepayment_status'          : fields.boolean("Prepayment Status", readonly=True),
        #'asset_category': fields.many2one('account.asset.category',"Asset Category",readonly=True, states={'draft': [('readonly', False)]}),
        #'asset_group'  : fields.many2one('asset.group', "Asset Group",readonly=True,states={'draft': [('readonly', False)]}),
        #'reg_asset'    : fields.boolean("Asset Registered",readonly=True,),               
        #'asset_extra_group': fields.many2one("asset.extra.group", "Group", readonly=True,states={'draft': [('readonly', False)]}),
        'currency_id': fields.many2one('res.currency','Currency',required=False, readonly=True, states={'draft':[('readonly',False)]}),
        #'pettycash_id': fields.many2one('ext.payment','Petty Cash for use', readonly=True, states={'draft':[('readonly',False)]}),
         
    }
    
    
    def _get_type(self, cr, uid, context=None):
        if context is None:
            context = {}
        return context.get('type', 'prepayment')


    _defaults = {
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid, 'purchase.request', context=c),
        'date_order': fields.datetime.now,
        'create_date': fields.datetime.now,
        'state': 'draft',
        'type': _get_type,
        'user_id': lambda s, cr, uid, c: uid,
        'name': lambda obj, cr, uid, context: '/',
    }
    
    def button_dummy(self, cr, uid, ids, context=None):
        return True
    
    def action_to_draft(self, cr, uid, ids, context=None):
        return self.write(cr,uid,ids,{'state':'draft'})
    
    def action_confirmed(self, cr, uid, ids, context=None):
        for val in self.browse(cr, uid, ids, context=None):
            name = val.name
            if val.name == '/':
                name = self.pool.get('ir.sequence').get(cr, uid, 'purchase.request.prepayment')
            self.write(cr, uid, ids, {'name': name, 'state':'confirmed'})
        return True
    
    def action_cancel(self, cr, uid, ids, context=None):
        for val in self.browse(cr, uid, ids, context=None):
            if val.invoice_ids and val.invoice_ids[0].state != 'draft':
                raise osv.except_osv(_('Error!'), _('Can not cancel if invoice on progress')) 
            if val.invoice_ids:
                self.pool.get('account.invoice').unlink(cr, uid, [val.invoice_ids[0].id])    
        return self.write(cr,uid,ids,{'state':'cancel'})
    
    def action_validate(self, cr, uid, ids, context=None):
        return self.action_invoice_create(cr, uid, ids, context=context)
    
#     def onchange_employee_id(self, cr, uid, ids, employee_id, context=None):
#         dept_id = False
#         if not employee_id:
#             return {'value': {'department_id': False}}
#         emp_obj = self.pool.get('hr.employee').browse(cr, uid, employee_id, context=context)
#         if emp_obj.department_id:
#             dept_id = emp_obj.department_id.id
#         return {'value': {'department_id': dept_id, 'order_line':False}}
    
    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        company_id = self.pool.get('res.users')._get_company(cr, uid, context=context)
        if not partner_id:
            return {'value': {'bank_id': False, 'npwp': False, 'payment_term_id':False}}
        p = self.pool.get('res.partner').browse(cr, uid, partner_id, context=None)
        fp = self.pool['account.fiscal.position'].get_fiscal_position(cr, uid, company_id, partner_id, context=context)
        bank_id = False
        npwp = False
        payment_term = False
        
        if p.npwp:
            npwp = p.npwp
        if p.property_supplier_payment_term:
            payment_term = p.property_supplier_payment_term.id or False
        if p.bank_ids :
            bank_id = p.bank_ids and p.bank_ids[0].id or False
            
        return {'value': {'npwp': npwp, 
                          'payment_term_id': payment_term,
                          'bank_id': bank_id,
                          'fiscal_position': fp or p.property_account_position and p.property_account_position.id,
                          }
                }
    
#     def create(self, cr, uid, vals, context=None):
#         if vals.get('name','/')=='/':
#             vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'purchase.request') or '/'
#         context = dict(context or {}, mail_create_nolog=True)
#         order =  super(purchase_request, self).create(cr, uid, vals, context=context)
#         return order
    
    def view_invoice(self, cr, uid, ids, context=None):
        '''
        This function returns an action that display existing invoices of given sales order ids. It can either be a in a list or in a form view, if there is only one invoice to show.
        '''
        context = dict(context or {})
        mod_obj = self.pool.get('ir.model.data')
        wizard_obj = self.pool.get('purchase.order.line_invoice')
        #compute the number of invoices to display
        inv_ids = []
        for po in self.browse(cr, uid, ids, context=context):
#             if po.invoice_method == 'manual':
            if not po.invoice_ids:
                context.update({'active_ids' :  [line.id for line in po.order_line if line.state != 'cancel']})
                wizard_obj.makeInvoices(cr, uid, [], context=context)

        for po in self.browse(cr, uid, ids, context=context):
            inv_ids+= [invoice.id for invoice in po.invoice_ids]
        res = mod_obj.get_object_reference(cr, uid, 'account', 'invoice_supplier_form')
        res_id = res and res[1] or False

        return {
            'name': _('Supplier Invoices'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [res_id],
            'res_model': 'account.invoice',
            'context': "{'type':'in_invoice', 'journal_type': 'purchase'}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': inv_ids and inv_ids[0] or False,
        }

    
    def _choose_account_from_po_line(self, cr, uid, po_line, context=None):
        fiscal_obj = self.pool.get('account.fiscal.position')
        property_obj = self.pool.get('ir.property')
        if po_line.account_id:
            acc_id = po_line.account_id.id
        elif po_line.product_id:
            acc_id = po_line.product_id.property_account_expense.id
            if not acc_id:
                acc_id = po_line.product_id.categ_id.property_account_expense_categ.id
            if not acc_id:
                raise osv.except_osv(_('Error!'), _('Define an expense account for this product: "%s" (id:%d).') % (po_line.product_id.name, po_line.product_id.id,))
        else:
            acc_id = property_obj.get(cr, uid, 'property_account_expense_categ', 'product.category', context=context).id
        fpos = False
        return fiscal_obj.map_account(cr, uid, fpos, acc_id)
    
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
            'invoice_line_tax_id': [(6, 0, [x.id for x in order_line.taxes_id])],
            ###
            'account_analytic_id' : order_line.order_id.type != 'prepayment' and order_line.analytic_account_id.id or False,
            ###
        }

    def _prepare_invoice(self, cr, uid, order, line_ids, context=None):
        """Prepare the dict of values to create the new invoice for a
           purchase order. This method may be overridden to implement custom
           invoice generation (making sure to call super() to establish
           a clean extension chain).

           :param browse_record order: purchase.order record to invoice
           :param list(int) line_ids: list of invoice line IDs that must be
                                      attached to the invoice
           :return: dict of value to create() the invoice
        """
        journal_ids = self.pool['account.journal'].search(
                            cr, uid, [('type', '=', 'purchase'),
                                      ('company_id', '=', order.company_id.id)],
                            limit=1)
        if not journal_ids:
            raise osv.except_osv(
                _('Error!'),
                _('Define purchase journal for this company: "%s" (id:%d).') % \
                    (order.company_id.name, order.company_id.id))
        return {
            'name': order.partner_ref or order.name,
            'reference': order.partner_ref or order.name,
            'account_id': order.partner_id.property_account_payable.id,
            'type': 'in_invoice',
            'partner_id': order.partner_id.id,
            'currency_id': order.currency_id.id,
            #'currency_id': self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.currency_id.id,
            'journal_id' : len(journal_ids) and journal_ids[0] or False,
            'invoice_line': [(6, 0, line_ids)],
            'npwp_no': order.npwp,
            'fiscal_position': order.fiscal_position.id or False,
            'payment_term': order.payment_term_id.id or False,
            'partner_bank_id': order.bank_id.id or False,
            'comment'   : order.propose,
            'purchase_request_id' : order.id,
            'origin' : order.name or False,
            ###
            #'employee_id' : order.employee_id.id or False,
            ### 
        }
    #===========================================================================
    # ini kalo depends ke module budget
    #===========================================================================
#===============================================================================
#     def action_budget_opex_virtual(self, cr, uid, ids, context=None):
#         budget_virtual_obj = self.pool.get('budget.virtual')
#         cur_obj = self.pool.get('res.currency')
#         for noi in self.browse(cr, uid, ids, context=None):
#             transaction_currency_id = noi.currency_id.id
#             company_currency_id     = noi.company_id.currency_id.id            
#             for line in noi.order_line:
#                 total_tax = 0.0
#                 if line.analytic_account_id:
#                     amount = line.price_subtotal or 0.0
#                     if line.taxes_id:
#                         for c in self.pool.get('account.tax').compute_all(cr, uid, line.taxes_id, line.price_unit, line.product_qty)['taxes']:
#                             total_tax += c.get('amount', 0.0)                     
#                         amount = amount + total_tax
#                     vals = {
#                         'noi_id'                : noi.id,
#                         'name'                  : line.name or "",
#                         'analytic_account_id'   : line.analytic_account_id.id,
#                         'date'                  : datetime.datetime.strptime(noi.date_order, '%Y-%m-%d %H:%M:%S').date(),
#                         'amount'                : transaction_currency_id<>company_currency_id and cur_obj.compute(cr, uid, transaction_currency_id, company_currency_id, amount, 
#                                         context={'date': datetime.datetime.strptime(noi.date_order, '%Y-%m-%d %H:%M:%S').date() or time.strftime('%Y-%m-%d')}, round=False) or amount,
#                         }
#                     budget_virtual_obj.create(cr, uid, vals, context=None)
#         return True
#     
#     def action_invoice_create(self, cr, uid, ids, context=None):
#         """Generates invoice for given ids of purchase orders and links that invoice ID to purchase order.
#         :param ids: list of ids of purchase orders.
#         :return: ID of created invoice.
#         :rtype: int
#         """
#         context = dict(context or {})
#         
#         inv_obj = self.pool.get('account.invoice')
#         inv_line_obj = self.pool.get('account.invoice.line')
#         cur_obj = self.pool.get('res.currency')
#         
#         res = False
#         uid_company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
#         for order in self.browse(cr, uid, ids, context=context):
#             ######Check Budget Capex##########
#             transaction_currency_id = order.currency_id.id
#             company_currency_id     = order.company_id.currency_id.id
#             
#             department_id   = order.department_id.id
#             date            = datetime.datetime.strptime(order.date_order, '%Y-%m-%d %H:%M:%S').date()
#             
#             budget_version_obj  = self.pool.get('budget.version')
#             version_search      = budget_version_obj.search(cr, uid, [('date_start','<=',date),('date_stop','>=',date)])
#             if version_search:
#                 version_id      = budget_version_obj.browse(cr, uid, version_search)[0].id            
#                 cr.execute("""select analytic_account_id, sum(product_qty*price_unit) from purchase_request_line 
#                                 where order_id = %s group by analytic_account_id""",(order.id,))                 
#                 noi_budget_line = cr.fetchall()
#                 
#                 if noi_budget_line:
#                     for line in noi_budget_line:
#                         account_analytic_id = line[0]
#                         amount_request      = line[1]
#                         print "amount_request>>>>>>>>>>>>>>>>>1111111111", amount_request
#                         amount_request = transaction_currency_id<>company_currency_id and cur_obj.compute(cr, uid, transaction_currency_id, company_currency_id, amount_request, 
#                                             context={'date': datetime.datetime.strptime(order.date_order, '%Y-%m-%d %H:%M:%S').date() or time.strftime('%Y-%m-%d')}) or amount_request,
#                         amount_request  = amount_request[0]
#                         print "amount_request>>>>>>>>>>>>>>>>>", amount_request
#                         if account_analytic_id:
#                             budget_line_search = self.pool.get('budget.line').search(cr, uid, [
#                                                                        ('analytic_account_id','=',account_analytic_id),
#                                                                        ('budget_version_id','=',version_id)
#                                                                        ])
#                             budget_opex = self.pool.get('budget.line').browse(cr, uid, budget_line_search)
#                             remain_budget = sum([l['analytic_virtual_diff_amount'] for l in budget_opex])
#                             
#                             if remain_budget < amount_request:
#                                 raise osv.except_osv(_('Budget Over!'), _('Your Budget Remain is %s') % (remain_budget))
#                         
#             ##################################
#             self.pool.get('purchase.request.line').write(cr, uid, [line.id for line in order.order_line if line.state != 'cancel'], {'state': 'done'}, context=context)
#             context.pop('force_company', None)
#             order = self.browse(cr, uid, order.id, context=context)
#             ####Cek Amount DP####
#             if order.type == 'prepayment' and order.purchase_id:
#                 amount_po  = order.purchase_id.amount_total
#                 amount_noi = order.amount_total
#                 if amount_noi >= amount_po:
#                     raise osv.except_osv(_('Over Amount!'), _('You can not request Prepayment more than %s') % amount_po)
#                 
#                 self.pool.get('purchase.order').write(cr, uid, [order.purchase_id.id], {'prepayment_id' : order.id,
#                                                                                         'dp_status'     :'created'
#                                                                                         })
#                     #raise osv.except_osv(_('User Error!'),_('You cannot delete a not draft transfer "%s"') % trans.name)
#             # generate invoice line correspond to PO line and link that to created invoice (inv_id) and PO line
#             inv_lines = []
#             for po_line in order.order_line:
#                 if po_line.state == 'cancel':
#                     continue
#                 acc_id = self._choose_account_from_po_line(cr, uid, po_line, context=context)
#                 inv_line_data = self._prepare_inv_line(cr, uid, acc_id, po_line, context=context)
#                 inv_line_id = inv_line_obj.create(cr, uid, inv_line_data, context=context)
#                 inv_lines.append(inv_line_id)
#                 po_line.write({'invoice_lines': [(4, inv_line_id)]})
# 
#             # get invoice data and create invoice
#             inv_data = self._prepare_invoice(cr, uid, order, inv_lines, context=context)
#             inv_id = inv_obj.create(cr, uid, inv_data, context=context)
# 
#             # compute the invoice
#             inv_obj.button_compute(cr, uid, [inv_id], context=context, set_total=True)
# 
#             # Link this new invoice to related purchase order
#             order.write({'invoice_ids': [(4, inv_id)]})
#             self.write(cr, uid, ids, {'state': 'done'}, context=context)
#             res = inv_id
#             
#             ####Hit Virtual Budget
#             self.action_budget_opex_virtual(cr, uid, ids, context=None)
#             ######################
#         return res
#===============================================================================
    
    #---create Assets and Low Value Assets by Budi----
    
#     def action_number_asset(self, cr, uid, ids, context=None):
#         #result = super(purchase_request, self).action_number(cr, uid, ids, *args, **kargs)
#         result={}
#         context = dict(context or {})
#         for inv in self.browse(cr, uid, ids):
#             self.pool.get('purchase.request.line').asset_create(cr, uid, inv.order_line)
#             self.write(cr, uid, ids, {'reg_asset': True}, context=context)
#         return result
    def action_invoice_create(self, cr, uid, ids, context=None):
        """Generates invoice for given ids of purchase orders and links that invoice ID to purchase order.
        :param ids: list of ids of purchase orders.
        :return: ID of created invoice.
        :rtype: int
        """
        context = dict(context or {})
        
        inv_obj = self.pool.get('account.invoice')
        inv_line_obj = self.pool.get('account.invoice.line')
        cur_obj = self.pool.get('res.currency')        
        res = False
        uid_company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
        for order in self.browse(cr, uid, ids, context=context):
            ######Check Budget Capex##########
            ##################################
            self.pool.get('purchase.request.line').write(cr, uid, [line.id for line in order.order_line if line.state != 'cancel'], {'state': 'done'}, context=context)
            context.pop('force_company', None)
            order = self.browse(cr, uid, order.id, context=context)
            ####Cek Amount DP kalo pake PO####
#             if order.type == 'prepayment' and order.purchase_id:
#                 amount_po  = order.purchase_id.amount_total
#                 amount_noi = order.amount_total
#                 if amount_noi >= amount_po:
#                     raise osv.except_osv(_('Over Amount!'), _('You can not request Prepayment more than %s') % amount_po)                
#                 self.pool.get('purchase.order').write(cr, uid, [order.purchase_id.id], {'prepayment_id' : order.id,
#                                                                                         'dp_status'     :'created'
#                                                                                         })
                    #raise osv.except_osv(_('User Error!'),_('You cannot delete a not draft transfer "%s"') % trans.name)
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
            # Link this new invoice to related purchase order
            order.write({'invoice_ids': [(4, inv_id)]})
            self.write(cr, uid, ids, {'state': 'done'}, context=context)
            res = inv_id            
            ####Hit Virtual Budget
            ######################
        return res
    
#     def action_register_asset(self, cr, uid, ids, context=None):
#         #result = super(purchase_request, self).action_number(cr, uid, ids, *args, **kargs)
#         result={}
#         context = dict(context or {})
#         for inv in self.browse(cr, uid, ids):
#             self.pool.get('purchase.request.line').asset_register(cr, uid, inv.order_line)
#             self.write(cr, uid, ids, {'reg_asset': True}, context=context)
#         return result
    
    
class purchase_request_line(osv.osv):
    _name = 'purchase.request.line'
    
    def _amount_line(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        for line in self.browse(cr, uid, ids, context=context):
            taxes = tax_obj.compute_all(cr, uid, line.taxes_id, line.price_unit, line.product_qty, line.product_id, line.order_id.partner_id)
            cur = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.currency_id
            res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
        return res
    
    def _get_uom_id(self, cr, uid, context=None):
        try:
            proxy = self.pool.get('ir.model.data')
            result = proxy.get_object_reference(cr, uid, 'product', 'product_uom_unit')
            return result[1]
        except Exception, ex:
            return False
    
    _columns = {
        'order_id': fields.many2one('purchase.request', 'Order Reference', select=True, required=True, ondelete='cascade'),
        'name': fields.text('Description', required=True),
        'date_planned': fields.date('Scheduled Date', required=False, select=True),
        'product_id': fields.many2one('product.product', 'Product', change_default=True),
        'price_unit': fields.float('Unit Price', required=True, digits_compute= dp.get_precision('Product Price')),
        'product_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure'), required=True),
        'taxes_id': fields.many2many('account.tax', 'purchase_request_taxe', 'ord_id', 'tax_id', 'Taxes'),
        'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
        'product_uom': fields.many2one('product.uom', 'Unit of Measure', required=True),
        'account_id': fields.many2one('account.account', 'Account', change_default=True),
        #'analytic_account_id' : fields.many2one('account.analytic.account', 'Analytic Account'),
        'state': fields.selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')],
                                  'Status', required=True, readonly=True, copy=False,
                                  help=' * The \'Draft\' status is set automatically when purchase request in draft status. \
                                       \n* The \'Confirmed\' status is set automatically as confirm when purchase request in confirm status. \
                                       \n* The \'Done\' status is set automatically when purchase request is set as done. \
                                       \n* The \'Cancelled\' status is set automatically when user cancel purchase request.'),
        #'invoice_lines': fields.many2many('account.invoice.line', 'purchase_request_line_invoice_rel',
        #                                  'order_line_id', 'invoice_id', 'Invoice Lines',
        #                                  readonly=True, copy=False),
        
    }
    
    _defaults = {
        'product_uom' : _get_uom_id,
        'product_qty': lambda *a: 1.0,
        'state': lambda *args: 'draft',
        #'invoiced': lambda *a: 0,
    }
    
    #=====================ini buat onchange budget==============================
    # def onchange_account_id(self, cr, uid, ids, account_id, department_id, context=None):
    #     analytic_account_id = False
    #     if not account_id or not department_id:
    #         return {'value': {'analytic_account_id': False}}
    #     aa_obj = self.pool.get('account.analytic.account')
    #     aa_search = aa_obj.search(cr,uid,[('budget_expense','=',account_id),('department_id','=',department_id)])
    #     if aa_search:
    #         for aa in aa_obj.browse(cr,uid,aa_search,context=None):
    #             analytic_account_id = aa.id
    #     
    #     return {'value': {'analytic_account_id': analytic_account_id}}
    #===========================================================================
    
    def onchange_product_uom(self, cr, uid, ids, product_id, qty, uom_id,
            partner_id, date_order=False, date_planned=False,
            name=False, price_unit=False, state='draft', context=None):
        """
        onchange handler of product_uom.
        """
        if context is None:
            context = {}
        if not uom_id:
            return {'value': {'price_unit': price_unit or 0.0, 'name': name or '', 'product_uom' : uom_id or False}}
        context = dict(context, purchase_uom_check=True)
        return self.onchange_product_id(cr, uid, ids, product_id, qty, uom_id,
            partner_id, date_order=date_order, date_planned=date_planned,
            name=name, price_unit=price_unit, state=state, context=context)
        
    def _get_date_planned(self, cr, uid, supplier_info, date_order_str, context=None):
        """Return the datetime value to use as Schedule Date (``date_planned``) for
           PO Lines that correspond to the given product.supplierinfo,
           when ordered at `date_order_str`.

           :param browse_record | False supplier_info: product.supplierinfo, used to
               determine delivery delay (if False, default delay = 0)
           :param str date_order_str: date of order field, as a string in
               DEFAULT_SERVER_DATETIME_FORMAT
           :rtype: datetime
           :return: desired Schedule Date for the PO line
        """
        supplier_delay = int(supplier_info.delay) if supplier_info else 0
        return datetime.strptime(date_order_str, DEFAULT_SERVER_DATETIME_FORMAT) + relativedelta(days=supplier_delay)
    
    def onchange_product_id(self, cr, uid, ids, product_id, qty, uom_id,
            partner_id, date_order=False, date_planned=False,
            name=False, price_unit=False, state='draft', context=None):
        """
        onchange handler of product_id.
        """
        if context is None:
            context = {}
        
        account_id = False
        analytic_account_id = False
        ############    
        if product_id:
            product = self.pool.get('product.product').browse(cr,uid,[product_id],context=None)[0]
            account_id = product.property_account_expense.id or product.categ_id.property_account_expense_categ.id or False 
        
        ############
        
        res = {'value': {'price_unit': price_unit or 0.0, 
                         'name': name or '', 'product_uom' : uom_id or False, 
                         'account_id':account_id or False,
                         }}
        if not product_id:
            return res

        product_product = self.pool.get('product.product')
        product_uom = self.pool.get('product.uom')
        res_partner = self.pool.get('res.partner')
        product_pricelist = self.pool.get('product.pricelist')
        account_fiscal_position = self.pool.get('account.fiscal.position')
        account_tax = self.pool.get('account.tax')

        # - check for the presence of partner_id and pricelist_id
        #if not partner_id:
        #    raise osv.except_osv(_('No Partner!'), _('Select a partner in purchase order to choose a product.'))
        #if not pricelist_id:
        #    raise osv.except_osv(_('No Pricelist !'), _('Select a price list in the purchase order form before choosing a product.'))

        # - determine name and notes based on product in partner lang.
        context_partner = context.copy()
        if partner_id:
            lang = res_partner.browse(cr, uid, partner_id).lang
            context_partner.update( {'lang': lang, 'partner_id': partner_id} )
        product = product_product.browse(cr, uid, product_id, context=context_partner)
        #call name_get() with partner in the context to eventually match name and description in the seller_ids field
        if not name or not uom_id:
            # The 'or not uom_id' part of the above condition can be removed in master. See commit message of the rev. introducing this line.
            dummy, name = product_product.name_get(cr, uid, product_id, context=context_partner)[0]
            if product.description_purchase:
                name += '\n' + product.description_purchase
            res['value'].update({'name': name})

        # - set a domain on product_uom
        res['domain'] = {'product_uom': [('category_id','=',product.uom_id.category_id.id)]}

        # - check that uom and product uom belong to the same category
        product_uom_po_id = product.uom_po_id.id
        if not uom_id:
            uom_id = product_uom_po_id

        if product.uom_id.category_id.id != product_uom.browse(cr, uid, uom_id, context=context).category_id.id:
            if context.get('purchase_uom_check') and self._check_product_uom_group(cr, uid, context=context):
                res['warning'] = {'title': _('Warning!'), 
                                  'message': _('Selected Unit of Measure does not belong to the same category as the product Unit of Measure.')}
            uom_id = product_uom_po_id

        res['value'].update({'product_uom': uom_id})

        # - determine product_qty and date_planned based on seller info
        if not date_order:
            date_order = fields.datetime.now()


        supplierinfo = False
        precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Product Unit of Measure')
        for supplier in product.seller_ids:
            if partner_id and (supplier.name.id == partner_id):
                supplierinfo = supplier
                if supplierinfo.product_uom.id != uom_id:
                    res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier only sells this product by %s') % supplierinfo.product_uom.name }
                min_qty = product_uom._compute_qty(cr, uid, supplierinfo.product_uom.id, supplierinfo.min_qty, to_uom_id=uom_id)
                if float_compare(min_qty , qty, precision_digits=precision) == 1: # If the supplier quantity is greater than entered from user, set minimal.
                    if qty:
                        res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier has a minimal quantity set to %s %s, you should not purchase less.') % (supplierinfo.min_qty, supplierinfo.product_uom.name)}
                    qty = min_qty
        #dt = self._get_date_planned(cr, uid, supplierinfo, date_order, context=context).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        qty = qty or 1.0
        #res['value'].update({'date_planned': date_planned or dt})
        if qty:
            res['value'].update({'product_qty': qty})

        price = price_unit
        if price_unit is False or price_unit is None:
            # - determine price_unit and taxes_id
#             if pricelist_id:
#                 date_order_str = datetime.strptime(date_order, DEFAULT_SERVER_DATETIME_FORMAT).strftime(DEFAULT_SERVER_DATE_FORMAT)
#                 price = product_pricelist.price_get(cr, uid, [pricelist_id],
#                         product.id, qty or 1.0, partner_id or False, {'uom': uom_id, 'date': date_order_str})[pricelist_id]
#             else:
            price = product.standard_price

#         taxes = account_tax.browse(cr, uid, map(lambda x: x.id, product.supplier_taxes_id))
#         fpos = fiscal_position_id and account_fiscal_position.browse(cr, uid, fiscal_position_id, context=context) or False
#         taxes_ids = account_fiscal_position.map_tax(cr, uid, fpos, taxes)
        taxes_ids = product.supplier_taxes_id
        res['value'].update({'price_unit': price, 'taxes_id': taxes_ids})

        return res

    product_id_change = onchange_product_id
    product_uom_change = onchange_product_uom
    
#     def asset_create(self, cr, uid, lines, context=None):
#         context = context or {}
#         asset_obj = self.pool.get('account.asset.asset')
#         for line in lines:
#             if line:
#                 vals = {
#                     'name': line.name,
#                     'code': line.order_id.name or False,
#                     'category_id': line.order_id.asset_category.id,
#                     'purchase_value': line.price_subtotal,
#                     #'period_id': line.order_id.period_id.id,
#                     'partner_id': line.order_id.partner_id.id,
#                     #'company_id': line.order_id.company_id.id,
#                     #'currency_id': line.order_id.currency_id.id,
#                     'purchase_date' : line.order_id.date_order,
#                 }
#                 changed_vals = asset_obj.onchange_category_id(cr, uid, [], vals['category_id'], context=context)
#                 vals.update(changed_vals['value'])
#                 asset_id = asset_obj.create(cr, uid, vals, context=context)
# #                 if line.asset_category_id.open_asset:
# #                     asset_obj.validate(cr, uid, [asset_id], context=context)
#         return True
#     
#     def asset_register(self, cr, uid, lines, context=None):
#         context = context or {}
#         asset_obj = self.pool.get('asset.register')
#         for line in lines:
#             i = line.product_qty 
#             z = int(i)           
#             for i in range(0,z):
#                 x = i + 1
#                 if line :
#                     vals = {
#                         'name': line.name + '/' + str(x),
#                         'asset_desc': line.name,
#                         'origin': line.order_id.name or False,
#                         'purchase_value': line.price_unit,
#                         'partner_id': line.order_id.partner_id.id,
#                         'purchase_date' : line.order_id.date_order,
#                         'employee_id' :line.order_id.employee_id.id,
#                         'department_id':line.order_id.department_id.id,
#                         'distrik_id':line.order_id.distrik_id.id,
#                         'currency_id': line.order_id.currency_id.id,
#                         'type': 'extra',
#                     }
#                 
#                 asset_id = asset_obj.create(cr, uid, vals, context=context)
#                  
#         return True
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
