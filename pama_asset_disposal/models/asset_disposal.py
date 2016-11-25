# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2015 Broadtech IT Solutions Pvt Ltd.
#    (http://wwww.broadtech-innovations.com)
#    contact@broadtech-innovations.com
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

import time
from openerp import fields, models, api, _

class account_asset_disposal(models.Model):
    _name = "account.asset.disposal"
    _description = "Asset Disposal"
    
    @api.model
    def _default_currency(self):
        return  self.env.user.company_id.currency_id
    
    
    name = fields.Char(string='Name', default='/', required=True, readonly=True, states={'draft': [('readonly', False)]})
    date = fields.Date(string='Date', required=True, default=lambda self: time.strftime('%Y-%m-%d'), readonly=True, states={'draft': [('readonly', False)]})
    invoice_date = fields.Date(string='Invoice Date')
    responsible_id = fields.Many2one('res.users', string='Responsible',default=lambda self: self.env.user, readonly=True, states={'draft': [('readonly', False)]})
    asset_id = fields.Many2one('account.asset.asset', string='Asset',required=True, readonly=True, states={'draft': [('readonly', False)]}, domain="[('state','=','open')]")
    asset_responsible_id = fields.Many2one('res.users', string='Asset Responsible', readonly=True, states={'draft': [('readonly', False)]})
    
    purchase_value = fields.Float(string='Purchase Value', readonly=True, states={'draft': [('readonly', False)]})
    book_value = fields.Float(string='Book Value', readonly=True, states={'draft': [('readonly', False)]})
    depreciation_value = fields.Float(string='Depreciation Value', readonly=True, states={'draft': [('readonly', False)]})
    
    purchase_value_usd      = fields.Float(string='Purchase Value USD', readonly=True, states={'draft': [('readonly', False)]})
    book_value_usd          = fields.Float(string='Book Value USD', readonly=True, states={'draft': [('readonly', False)]})
    depreciation_value_usd  = fields.Float(string='Depreciation Value USD', readonly=True, states={'draft': [('readonly', False)]})
    
    type = fields.Selection([
            ('to_sale', 'To Sale'),
            ('to_destroy', 'To Destroy'),
            ('csr_activity', 'CSR Activity')
        ], string='Type',required=False, default=False)
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=False)
    price = fields.Float(string='Price', readonly=False)
    tax_ids = fields.Many2many('account.tax',
        'asset_disposal_tax', 'asset_disposal_id', 'tax_id',
        string='Taxes', domain=[('parent_id', '=', False)], readonly=False)
    reasons = fields.Char(string='Reasons', size=256, readonly=False)
    move_id = fields.Many2one('account.move', string='Disposal Entry', readonly=True, )
    invoice_id = fields.Many2one('account.invoice', string='Invoices', readonly=True, )
    currency_id = fields.Many2one('res.currency', string='Currency',
        required=True, readonly=True, states={'draft': [('readonly', False)]},
        default=_default_currency, track_visibility='always')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('propose', 'Proposed'),
            ('approved', 'Approved'),
            ('validate', 'Validate'),
            ('dispose', 'Dispose'),
            ('done', 'Done')
        ], string='Status', default='draft', readonly=True,)
    note = fields.Text('Notes')
    
    
    masterlist  = fields.Boolean(string='Is Masterlist', related='asset_id.is_masterlist')
    leasing     = fields.Boolean(string='Is Leasing', related='asset_id.is_leasing')

    @api.multi
    def asset_id_change(self, asset_id):
        """On change function for asset_id.
            asset_responsible_id, purchase_value, book_value and
            depreciation_value are changed on selecting an asset_id.
        """
        if not asset_id:
            return {'value': {'asset_responsible_id': False,
#                               'masterlist': False,
#                               'leasing': False,
                              'purchase_value': 0.00,
                              'book_value': 0.00,
                              'depreciation_value': 0.00,
                              
#                               'purchase_value_usd': 0.00,
#                               'book_value_usd': 0.00,
#                               'depreciation_value_usd': 0.00,
                              }}
        values = {}
        asset = self.env['account.asset.asset'].browse(asset_id)
        if asset:
            values['asset_responsible_id'] = asset.user_id and asset.user_id.id or False
#             values['masterlist'] = asset.is_masterlist
#             values['leasing'] = asset.is_leasing
            
            values['purchase_value'] = asset.purchase_value
            values['book_value'] = asset.value_residual
            values['depreciation_value'] = asset.purchase_value - asset.value_residual
            
#             values['purchase_value_usd']        = asset.purchase_value_usd
#             values['book_value_usd']            = asset.value_residual_usd
#             values['depreciation_value_usd']    = asset.purchase_value_usd - asset.value_residual_usd
        else:
            return {'value': {'asset_responsible_id': False,
                              'purchase_value'      : 0.00,
                              'book_value'          : 0.00,
                              'depreciation_value'  : 0.00,
                              
#                               'purchase_value_usd'      : 0.00,
#                               'book_value_usd'          : 0.00,
#                               'depreciation_value_usd'  : 0.00,
                              }}
        return {'value': values}
    
   
    
    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(self.env.cr, self.env.user.id, 'account.asset.disposal') or '/'
        new_id = super(account_asset_disposal, self).create(vals)
        return new_id
    
    @api.one
    def button_propose(self):
        self.state = 'propose'
    @api.one
    def button_approve(self):
        self.state = 'approved'
    @api.one
    def button_validate(self):
        self.state = 'validate'
    @api.one
    def button_dispose(self):
        self.state = 'dispose'
    @api.one
    def button_done(self):
        account_move = self.env['account.move']
        account_move_line = self.env['account.move.line']
        account_period = self.env['account.period']
        account_asset = self.env['account.asset.asset']
       # cr, uid = self.cr, self.uid
        period_ids = account_period.find(self.date)
        company_currency = self.asset_id.company_id.currency_id.id
        current_currency = self.asset_id.currency_id.id

        print "self.date--------------------->>", self.date
        

        move_vals = {
                'name': self.name,
                'date': self.date,
                'ref': self.asset_id.name,
                'period_id': period_ids and period_ids[0].id or False,
                'journal_id': self.asset_id.category_id.journal_id.id,
                }
            
        move_id = account_move.create(move_vals)
        journal_id = self.asset_id.category_id.journal_id.id
        
        account_move_line.create({
                'name': self.name,
                'ref': self.asset_id.name,
                'move_id': move_id.id,
                'account_id': self.asset_id.category_id.account_depreciation_id.id,
                'credit': 0.0,
                'debit': self.depreciation_value,
                'period_id': period_ids and period_ids[0].id or False,
                'journal_id': journal_id,
                #'partner_id': partner_id,
                'currency_id': company_currency != current_currency and  current_currency or False,
                'amount_currency': company_currency != current_currency and - sign * self.depreciation_value or 0.0,
                'usd_amount' : self.depreciation_value_usd,
                'date': self.date,
            })
        account_move_line.create({
                'name': self.name,
                'ref': self.asset_id.name,
                'move_id': move_id.id,
                'account_id': self.asset_id.category_id.account_disposal_id.id,
                'credit': 0.0,
                'debit': self.book_value,
                'period_id': period_ids and period_ids[0].id or False,
                'journal_id': journal_id,
                #'partner_id': partner_id,
                'currency_id': company_currency != current_currency and  current_currency or False,
                'amount_currency': company_currency != current_currency and - sign * self.book_value or 0.0,
                'usd_amount' : self.book_value_usd,
                'date': self.date,
            })
        
        account_move_line.create({
                'name': self.name,
                'ref': self.asset_id.name,
                'move_id': move_id.id,
                'account_id': self.asset_id.category_id.account_asset_id.id,
                'debit': 0.0,
                'credit': self.purchase_value,
                'period_id': period_ids and period_ids[0].id or False,
                'journal_id': journal_id,
                #'partner_id': partner_id,
                'currency_id': company_currency != current_currency and  current_currency or False,
                'amount_currency': company_currency != current_currency and - sign * self.purchase_value or 0.0,
                'usd_amount' : -self.purchase_value_usd,
                'date': self.date,
            })
        
        self.state = 'done'
        self.move_id=move_id.id
        self.asset_id.write({'asset_disposal':True})
        if self.type == 'to_sale' :
            self.create_invoice()
        self.asset_id.set_to_close()
        
   
    def create_invoice(self):
        print "################# create_invoice"
        inv_obj = self.env['account.invoice']
        inv_line_obj = self.env['account.invoice.line']
        tax_ids =[]
        for tax_id in self.tax_ids:
            tax_ids.append(tax_id.id)
            
        company_currency = self.asset_id.company_id.currency_id
        current_currency = self.currency_id
            
        inv_val = {
                'name': self.name,
                'origin': self.name,
                'type': 'out_invoice',
                'reference': False,
                'account_id': self.partner_id.property_account_receivable.id,
                'partner_id': self.partner_id.id,
                #'invoice_line': [(0, 0, inv_line_values)],
                'currency_id': self.currency_id.id,
                'comment': self.note,
                'payment_term': self.partner_id.property_payment_term.id,
                'fiscal_position': self.partner_id.property_account_position.id,
                'date_invoice' : self.invoice_date,
              #  'section_id': sale.section_id.id,
                   }
        
        inv_id=inv_obj.create(inv_val)
        
        company_currency = self.asset_id.company_id.currency_id.with_context(date=self.invoice_date)
        
        print "company_currency != current_currency", company_currency, current_currency
                
        disposal_inv_amount = company_currency != current_currency and \
                            company_currency.compute(self.book_value, current_currency) or self.book_value
        
        inv_line_values = {
                'name': self.name,
                'origin': self.name,
                'account_id': self.asset_id.category_id.account_disposal_id.id,
                #'price_unit': self.price,
                'price_unit': disposal_inv_amount,
                'quantity': 1.0,
                'discount': False,
                'invoice_id': inv_id.id,
              #  'uos_id': res.get('uos_id', False),
               # 'product_id': wizard.product_id.id,
                'invoice_line_tax_id': [(6, 0,tax_ids)]
              #  'account_analytic_id': sale.project_id.id or False,
            }
        
        print "######################", self.price, disposal_inv_amount
        
        gainloss_inv_amount = self.price - disposal_inv_amount
        inv_line_gain_values = {
                'name': "Gain or Loss - " + self.name,
                'origin': self.name,
                'account_id': self.asset_id.category_id.account_gainloss_disposal_id.id,
                'price_unit': gainloss_inv_amount,
                'quantity': 1.0,
                'discount': False,
                'invoice_id': inv_id.id,
              #  'uos_id': res.get('uos_id', False),
               # 'product_id': wizard.product_id.id,
                #'invoice_line_tax_id': [(6, 0,tax_ids)]
              #  'account_analytic_id': sale.project_id.id or False,
            }
        
        inv_line_id = inv_line_obj.create(inv_line_values)
        inv_line_gain_id = inv_line_obj.create(inv_line_gain_values)
        self.invoice_id = inv_id.id
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: