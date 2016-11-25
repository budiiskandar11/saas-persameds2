#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################################################################
#
#   PT Databit Solusi Indonesia
#   Copyright (C) 2010-2016 Databit (<http://www.databit.co.id>). 
#   All Rights Reserved
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

import time
from lxml import etree
from openerp import SUPERUSER_ID, netsvc, api
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _


class reimburstment(osv.osv):
    _name ='reimburstment'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'For Reiburstment Expense'
    
    def _amount_tot(self, cr, uid, ids, field_name, args, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                
                'amount_total': 0.0,
            }
            val1 =0.0
            for line in order.line_ids:
                val1 += line.subtotal
                
            cur = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.currency_id
            res[order.id]['amount_total'] = cur_obj.round(cr, uid, cur, val1)
            
        return res
    
    def _get_period(self, cr, uid, context=None):
        if context is None: context = {}
        if context.get('period_id', False):
            return context.get('period_id')
#         if context.get('invoice_id', False):
#             company_id = self.pool.get('account.invoice').browse(cr, uid, context['invoice_id'], context=context).company_id.id
#             context.update({'company_id': company_id})
        periods = self.pool.get('account.period').find(cr, uid, context=context)
        return periods and periods[0] or False
    
    _columns = {
                
                'name'      : fields.char('No'),
                'create_uid'    : fields.many2one('res.users','Create By', readonly=True),
                'date_create'   : fields.datetime('Date Create', readonly=True),
                'employee_id': fields.many2one("hr.employee", "Employee", readonly=True, states={"draft": [("readonly", False)]}),
                'state': fields.selection([
                    ('draft', 'Draft'),
                    ('confirm', 'Waiting Approval'),
                    ('approve', 'Waiting Payment'),
                    ('posted', 'Paid'),
                    ('cancel', 'Cancelled')
                    ], 'State', readonly=True, size=32,
                    help=' * The \'Draft\' state is used when a user is encoding a new and unconfirmed Voucher. \
                                \n* The \'Pro-forma\' when voucher is in Pro-forma state,voucher does not have an voucher number. \
                                \n* The \'Posted\' state is used when user create voucher,a voucher number is generated and voucher entries are created in account \
                                \n* The \'Cancelled\' state is used when user cancel voucher.'),
                'memo': fields.char('Memo', size=256, required=True ,readonly=True, states={'draft': [('readonly', False)]}),
                'date_start'    : fields.date('Date Start', readonly=True, states={'draft':[('readonly',False)]}),
                'date_end'      : fields.date('Date End', readonly=True, states={'draft':[('readonly',False)]}),
                'department_id' : fields.many2one('hr.department','Departement', readonly=True, states={'draft':[('readonly',False)]}),
                'amount_total'  : fields.function(_amount_tot, type='float', multi = "all", method=True, string='Total', digits_compute= dp.get_precision('Account')),
                'line_ids'      : fields.one2many('reimburstment.line','reimburstment_id','Reimburst Lines' ,readonly=True, states={'draft':[('readonly',False)]}),
                'date_payment'  : fields.date('Payment Date', readonly=True, states={'approve':[('readonly',False)]}),
                'journal_id': fields.many2one('account.journal', 'Bank/ Cash Payment', required=False, readonly=True, states={'approve': [('readonly', False)]}),
                'period_id': fields.many2one('account.period', 'Period', required=False,),
                'move_id':fields.many2one('account.move', 'Account Entry'),
                'currency_id': fields.many2one('res.currency', 'Currency', readonly=True, states={'draft': [('readonly', False)]}),
                }
    
    _defaults = {
                 'create_uid' : lambda obj, cr, uid, context: uid,
                 'date_create' : fields.datetime.now,
                 'state'        :'draft',
                 'period_id': _get_period,
                 'currency_id': lambda self, cr, uid, context: self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.currency_id.id,
                 }
    
    def onchange_employee_id(self, cr, uid, ids, employee_id):
        department_id={}
        
        for emp in self.pool.get('hr.employee').browse(cr, uid, [employee_id], context=None):
        
            department_id = emp.department_id
            
        return {'value':{ 'department_id' : department_id,}}
    
    def propose(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'confirm',
                                         'name': self.pool.get('ir.sequence').get(cr, uid, 'reimburstment')}
                                         , context=context)
    
    def cancel(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)
    
    def approve(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'approve'}, context=context)
    
    def create_payment(self, cr, uid, ids, context=None):
        self.action_move_line_create2(cr, uid, ids, context=context)
        self.write(cr, uid, ids, {'state': 'posted'}, context=context)
        return True
    
    def action_move_line_create2(self, cr, uid, ids, context=None):
        
        move_pool = self.pool.get('account.move')
        move_line_pool = self.pool.get('account.move.line')
        currency_pool = self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        seq_obj = self.pool.get('ir.sequence')
        amount_currency = 0.0
        
        for inv in self.browse(cr, uid, ids, context=context):
#             if inv.move_id:
#                 continue
#             context_multi_currency = context.copy()
#             context_multi_currency.update({'date': inv.date})
# 
#             if inv.number:
#                 name = inv.number
            if inv.journal_id.sequence_id:
                name = seq_obj.get_id(cr, uid, inv.journal_id.sequence_id.id)
            else:
                raise osv.except_osv(_('Error !'), _('Please define a sequence on the journal !'))
#             if not inv.reference:
#                 ref = name.replace('/','')
#             else:
#                 ref = inv.reference
            print ">>>>>>>>>>>>>>>>", name
            
            move = {
                'name': name,
                'journal_id': inv.journal_id.id,
                'narration': inv.memo,
                'date': inv.date_payment,
                'ref': inv.memo,
                'period_id': inv.period_id and inv.period_id.id or False
            }
            move_id = move_pool.create(cr, uid, move)
            self.write(cr, uid, ids, {'move_id': move_id}, context=context)
#             #create the first line manually
            company_currency = inv.journal_id.company_id.currency_id.id
            #current_currency = inv.currency_id.id
            debit = 0.0
            credit = 0.0
            move_line_debit={}
            
            
            move_line_credit = {
                        'name': 'Pembayaran Reimburs No' + inv.name or '/',
                        'debit': 0.0,
                        'credit': inv.amount_total or 0.0,
                        'account_id': inv.journal_id.default_credit_account_id.id,
                        'move_id': move_id,
                        'journal_id': inv.journal_id.id,
                        'period_id': inv.period_id and inv.period_id.id or False,
                        #'analytic_account_id': ext_pay_line.analytic_account_id.id,
                        #'partner_id': inv.partner_id.id,
#                         'currency_id': company_currency <> currency and currency or False,
#                         'amount_currency': company_currency <> currency and line.amount or 0.0,
                        'date': inv.date_payment,
                        ###
                        'bank_recon_id' : True,
                        ###
                                }
            move_line_pool.create(cr, uid, move_line_credit)
            
             
#             
            for line in inv.line_ids :
                move_line_debit = {
                        'name': line.name,
                        'debit': line.subtotal or 0.0,
                        'credit': 0.0,
                        'account_id': line.tipe_id.account_id.id,
                        'move_id': move_id,
                        'journal_id': inv.journal_id.id,
                        'period_id': inv.period_id and inv.period_id.id or False,
                        #'analytic_account_id': ext_pay_line.analytic_account_id.id,
                        #'partner_id': inv.partner_id.id,
#                         'currency_id': company_currency <> currency and currency or False,
#                         'amount_currency': company_currency <> currency and line.amount or 0.0,
                        'date': line.date,
                                }
                
                move_line_id = move_line_pool.create(cr, uid, move_line_debit)      
            
        return True    



reimburstment()

class reimburstment_line(osv.osv):
    _name           = 'reimburstment.line'
    _description    = 'Line Reimburstment'
    
    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        if context is None:
            context = {}
        sub_total = 0.0
        for line in self.browse(cr, uid, ids, context=context):
            sub_total = line.qty * line.unit_price
            
            res[line.id] = { 'subtotal' : sub_total}
            #print "xxxx.....>>>>>>>>>>>>", res
        return res
    
    _columns        = {
                       'name'   : fields.char('Description', required=True),
                       'tipe_id': fields.many2one('reimburstment.expense.type','Tipe'),
                       'date'   : fields.date('Date'),
                       'qty'    : fields.float('Qty'),
                       'unit_price' :fields.float('Unit Price'),
                       'subtotal'   :fields.function(_amount_line, type='float', multi = "all", method=True, string='Subtotal', digits_compute= dp.get_precision('Account')),
                       'reimburstment_id' : fields.many2one('reimburstment','Reimburstment ID'),
                       'receipt'    : fields.boolean('Kuitansi'),
                       'alasan'     : fields.char('Reasons'),
                       } 
    _defaults   = {
                   'receipt' : False,
                   }

reimburstment_line

class reimburstment_expense_type(osv.osv):
    _name  = 'reimburstment.expense.type'
    _description = 'Tipe advance related dengan account'
    _columns    = {
                   'name'   : fields.char('Name', required =True),
                   'code'   : fields.char('Code'),
                   'account_id' : fields.many2one('account.account', 'Account Advance', required=True)
                   
                   }
    
reimburstment_expense_type()
    
    
