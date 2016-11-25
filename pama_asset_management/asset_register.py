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
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class asset_register(osv.osv):
    _name = "asset.register"
    
    _columns = {
        'name': fields.char('Asset Register Name', required=True, readonly=True, states={'draft':[('readonly',False)]}),
        'code': fields.char('Reference', size=32, readonly=True, states={'draft':[('readonly',False)]}),
        'purchase_value': fields.float('Purchase Value', required=True, readonly=True, states={'draft':[('readonly',False)]}),
        'currency_id': fields.many2one('res.currency','Currency',required=False, readonly=True, states={'draft':[('readonly',False)]}),
        'company_id': fields.many2one('res.company', 'Company', required=True, readonly=True, states={'draft':[('readonly',False)]}),
        'note': fields.text('Note'),
        'image': fields.binary("Image",
            help="This field holds the image used as image for the Asset, limited to 1024x1024px."),
        'asset_group_id' : fields.many2one('account.asset.category', 'Asset Group',readonly=True, states={'draft':[('readonly',False)]}),
        'asset_category': fields.many2one('account.asset.group', 'Asset Category', change_default=True, readonly=True, states={'draft':[('readonly',False)]}),
        'asset_class_id': fields.many2one('account.asset.class', 'Asset Class', change_default=True, readonly=True, states={'draft':[('readonly',False)]}),
        'asset_number': fields.char('Asset Number', required=True,copy=False, readonly=True, states={'draft':[('readonly',False)]}),
        'user_id': fields.many2one('res.users', 'Responsible ', readonly=True),
        'asset_location_id'    : fields.many2one('asset.location','Location',readonly=True, states={'draft':[('readonly',False)]} ),
        ###
        'serial_number': fields.char("Serial Number", size=64),
        'brand'        : fields.char("Brand", size=128),
        ###
        'employee_id': fields.many2one("hr.employee", "PIC Asset", required=False, readonly=True, states={"draft": [("readonly", False)]}),
        'department_id' : fields.many2one("hr.department", "Department",  readonly=True, states={"draft": [("readonly", False)]}),
        'distrik_id' : fields.many2one("hr.distrik", "Distrik", readonly=True, states={"draft": [("readonly", False)]}),
        'asset_distrik_id' : fields.many2one("hr.distrik", "Asset District", readonly=True, states={"draft": [("readonly", False)]}),
        
        'active'     : fields.boolean('Active'),
        'purchase_date1': fields.date('Purchase Date', required=True, readonly=True, states={'draft':[('readonly',False)]}),
        'purchase_date': fields.date('Purchase Date', required=True, readonly=True, states={'draft':[('readonly',False)]}),
        'asset_desc'       : fields.char("Description", size=512,  readonly=True, states={'draft':[('readonly',False)]}),
        'origin' : fields.char("Source Document", size=128, readonly=True, states={'draft':[('readonly',False)]}),
        'partner_id' : fields.many2one("res.partner", "Partner" , readonly=True, states={'draft':[('readonly',False)]}),
        'state': fields.selection([('draft','Draft'),
                                   ('register','Registered'),
                                   ], 'Status', required=True, copy=False,),
                
        'type': fields.selection([('fixasset','Fix Asset'),
                                   ('extra','Extra'),
                                   ], 'Status', copy=False,),
        'asset_id'     : fields.many2one("account.asset.asset", "Fix Asset" , readonly=True), 
        ###
        'stock_move_id'     : fields.many2one("stock.move", "Stock Move" , readonly=True), 
        'stock_move_line'   : fields.many2many('stock.move', 'asset_reg_move_rel', 'asset_reg_id', 'stock_move_id', 'Stock Move Line'),
        ###
        
        'cip_account_id' : fields.many2one("account.account", "CIP Account"),
        'serial_number': fields.char("Serial Number", size=64),
        'brand'        : fields.char("Brand", size=128),
        
        ###
        'note'     : fields.text('Notes'),
        'field1'    : fields.char('Field 1', size=128),
        'field2'    : fields.char('Field 2', size=128),
        'field3'    : fields.char('Field 3', size=128),
        'field4'    : fields.char('Field 4', size=128),
        'field5'    : fields.char('Field 5', size=128),
        'field6'    : fields.char('Field 6', size=128),
        'field7'    : fields.char('Field 7', size=128),
        'field8'    : fields.char('Field 8', size=128),
        'field9'    : fields.char('Field 9', size=128),
        ###
        
        ###Budget###
        'budget_asset_item_id'  : fields.many2one('budget.asset.item', 'Budget Asset item'),
        ############
        ############
        'purchase_value_usd': fields.float('Purchase Value USD', required=False, readonly=True, states={'draft':[('readonly',False)]}),
        
        'currency_usd_id': fields.many2one('res.currency','Currency USD',required=False, readonly=True, states={'draft':[('readonly',False)]}),
        ############
    }
    
    _defaults = {
                 'purchase_date1': lambda obj, cr, uid, context: time.strftime('%Y-%m-%d'),
                 'asset_number': lambda obj, cr, uid, context: '/',  
                 'user_id': lambda obj, cr, uid, context: uid,
                 'active' : True,
                 'state': 'draft',
                 'company_id': lambda self, cr, uid, context: self.pool.get('res.company')._company_default_get(cr, uid, 'asset.extra',context=context),
                 } 
    
    def onchange_employee_id (self, cr, uid, ids, employee_id):
        depart={}
        distrik={}
        
        for onchange in self.pool.get('hr.employee').browse(cr, uid, [employee_id], context=None):
            print '1111111'
                
        depart = onchange.department_id
        distrik = onchange.distrik_id
            
        return {'value':{
                             'department_id': depart,
                             'distrik_id' : distrik,
                             
                             }}
        
    def asset_extra_create(self, cr, uid, ids, context=None):
        asset = self.pool.get('asset.register')
        asset_obj = self.pool.get('asset.extra')
        result={}
        context = dict(context or {})
        vals = {}
        for inv in self.browse(cr, uid, ids) :
            #if inv.send_asset == 'yes' and inv.asset_transfer_status != 'done': 
            #    raise osv.except_osv(_('Invalid Action!'), _('You Can not Confirm Asset when asset not sent'))
            
            vals = {
                        'name': inv.name or '/',
                        'asset_desc': inv.asset_desc,
                        'code': inv.name or False,
                        'purchase_value': inv.purchase_value,
                       'partner_id': inv.partner_id.id,
                        'purchase_date' : inv.purchase_date,
                        'employee_id' :inv.employee_id.id,
                         'department_id':inv.department_id.id,
                         'distrik_id':inv.distrik_id.id,
                         'currency_id': inv.currency_id.id ,
                        'category_id': inv.asset_group_id.id,
                        'asset_group_id' : inv.asset_category.id,
                        'asset_class_id' : inv.asset_class_id.id,
                        'asset_location_id' : inv.asset_location_id.id,
                        'image': inv.image,
                        'serial_number':inv.serial_number,
                        'brand':inv.brand,
                    }
             
       
        asset_id = asset_obj.create(cr, uid, vals, context=context)
        asset_number = asset_obj.browse(cr, uid, asset_id, context=None).asset_number
        self.write(cr, uid, ids, {'state' : 'register', 'asset_number' : asset_number}, context=None)       
        return True
        
    def asset_create(self, cr, uid, ids, context=None):
        asset = self.pool.get('asset.register')
        asset_obj = self.pool.get('account.asset.asset')
        result={}
        context = dict(context or {})
        vals = {}
        for inv in self.browse(cr, uid, ids) :
            #if inv.send_asset == 'yes' and inv.asset_transfer_status != 'done': 
            #    raise osv.except_osv(_('Invalid Action!'), _('You Can not Confirm Asset when asset not sent'))
            
            vals = {
                        'name': inv.name or '/',
                        'asset_desc': inv.asset_desc,
                        'code': inv.name or False,
                        'purchase_value': inv.purchase_value,
                       'partner_id': inv.partner_id.id,
                        'purchase_date' : inv.purchase_date,
                        'employee_id' :inv.employee_id.id,
                         'department_id':inv.department_id.id,
                         'distrik_id':inv.distrik_id.id,
                         'currency_id': inv.currency_id.id ,
                        'category_id': inv.asset_group_id.id,
                        'asset_group_id' : inv.asset_category.id,
                        'asset_class_id' : inv.asset_class_id.id,
                        'asset_location_id' : inv.asset_location_id.id,
                        'image': inv.image,
                        'serial_number':inv.serial_number,
                        'brand':inv.brand,
                        'purchase_value_usd'    : inv.purchase_value_usd or 0.0,
                        'asset_reg_id': inv.id,
                    }
             
       
        asset_id = asset_obj.create(cr, uid, vals, context=context)
        
        #####CIP to Asset#######
        move_pool = self.pool.get('account.move')
        move_line_pool = self.pool.get('account.move.line')
        period_pool = self.pool.get('account.period')
        period_id = period_pool.find(cr, uid, time.strftime('%Y-%m-%d'), context=None)[0]
        move = {
                'name'          : inv.name,
                'journal_id'    : inv.asset_group_id.journal_id.id,
                'narration'     : inv.name,
                'date'          : time.strftime('%Y-%m-%d'),
                'ref'           : inv.name,
                'period_id'     : period_id,
                'district'      : inv.send_asset == 'yes' and inv.dest_distrik_id.id or inv.distrik_id.id
                ###
                }
        move_id = move_pool.create(cr, uid, move)
        
        move_line = {
                    'name'              : inv.name or "/",
                    'debit'             : inv.purchase_value or 0.0,
                    'credit'            : 0.0,
                    'account_id'        : inv.asset_group_id.account_asset_id.id,
                    'move_id'           : move_id,
                    'journal_id'        : inv.asset_group_id.journal_id.id,
                    'period_id'         : period_id,
                    #'analytic_account_id': ext_pay_line.analytic_account_id.id,
                    #'partner_id'        : ext_pay_line.partner_id.id,
                    #'currency_id'       : company_currency <> ext_pay.currency_id.id and ext_pay.currency_id.id or False,
                    #'program_budget_id' : ext_pay_line.program_budget_id.id or False,
                    #'amount_currency'   : ext_pay_line.amount_currency,#company_currency <> ext_pay.currency_id.id and ext_pay_line.debit or company_currency <> ext_pay.currency_id.id and -ext_pay_line.credit or 0.0,
                    #'usd_amount'    : inv.purchase_value_usd or 0.0,
                    'date'          : time.strftime('%Y-%m-%d'),
                    'district'      : inv.send_asset == 'yes' and inv.dest_distrik_id.id or inv.distrik_id.id,
                    }
        move_line_pool.create(cr, uid, move_line)
        move_line = {
                    'name'              : inv.name or "/",
                    'debit'             : 0.0,
                    'credit'            : inv.purchase_value or 0.0,
                    'account_id'        : inv.cip_account_id.id,
                    'move_id'           : move_id,
                    'journal_id'        : inv.asset_group_id.journal_id.id,
                    'period_id'         : period_id,
                    #'analytic_account_id': ext_pay_line.analytic_account_id.id,
                    #'partner_id'        : ext_pay_line.partner_id.id,
                    #'currency_id'       : company_currency <> ext_pay.currency_id.id and ext_pay.currency_id.id or False,
                    #'program_budget_id' : ext_pay_line.program_budget_id.id or False,
                    #'amount_currency'   : ext_pay_line.amount_currency,#company_currency <> ext_pay.currency_id.id and ext_pay_line.debit or company_currency <> ext_pay.currency_id.id and -ext_pay_line.credit or 0.0,
                    #'usd_amount'    : -inv.purchase_value_usd or 0.0,
                    'date'          : time.strftime('%Y-%m-%d'),
                    'district'      : inv.send_asset == 'yes' and inv.dest_distrik_id.id or inv.distrik_id.id,
                    }
        move_line_pool.create(cr, uid, move_line)
        ########################
        
        asset = asset_obj.browse(cr, uid, asset_id, context=None)
        self.write(cr, uid, ids, {'state' : 'register', 'asset_id':asset.id, 'asset_number' : asset.asset_number}, context=None)       
        return True
    
    
    def check_asset_register_merge(self, cr, uid, ids, context=None):
        print "len(ids)------>>", len(ids)
        
        for asset_reg in self.browse(cr, uid, ids, context=None):
            if asset_reg.state != 'draft':
                raise osv.except_osv(_('Invalid Action!'), _('You Can not merge if state not in Draft'))
        return True
    
    def copy_split(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        if context is None:
            context = {}
            
        asset_register_id   = context['asset_register_id']
        amount_value        = context['amount_value']
        
        print "asset_register_id", id, asset_register_id, "amount_value", amount_value 
            
        default.update({'note' : "Split Asset Register", 'state': 'draft', 'purchase_value':amount_value})
        
        print "HHHHHHHHHHHHHHHHHHHH"
        
        return super(asset_register, self).copy(cr, uid, asset_register_id, default, context=context)
    
    def copy_merge(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        if context is None:
            context = {}
        default.update({'note' : "Merge Asset Register", 'state': 'draft'})
        return super(asset_register, self).copy(cr, uid, id, default, context=context)
        
    def asset_register_merge(self, cr, uid, ids, context=None):
        asset_reg_obj          = self.pool.get('asset.register')
        
        print "IDS----------->>", ids
       
        new_asset_register = asset_reg_obj.copy_merge(cr, uid, ids[0], None, context=None)
        print "new_new_asset_register--------->>", new_asset_register
        merge_purchase_value = 0.0
        origin = ""
        ###Update INvoice ids Purchase Order###
        move_ids = []
        for asset_reg in asset_reg_obj.browse(cr, uid, ids, context=None):
            origin = asset_reg.origin +" + "+ origin
            merge_purchase_value += asset_reg.purchase_value
            move_ids.append(asset_reg.stock_move_id)
            ###Delete Invoice Old###
            if asset_reg.state != 'draft':
                raise osv.except_osv(_('Invalid Action!'), _('You Can not Delete This record'))
            asset_reg.unlink()
        self.write(cr, uid, [new_asset_register], {
                                                   'origin'             : origin,
                                                   'stock_move_line'    : [(6, 0, [x.id for x in move_ids])],
                                                   'purchase_value'     : merge_purchase_value,
                                                   }, context=None)
        return True

    
asset_register()
