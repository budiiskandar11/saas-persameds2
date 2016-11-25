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

class asset_extra(osv.osv):
    _name = "asset.extra"
    
    _columns = {
        'name': fields.char('Asset Extra Comptable Name', required=True, readonly=True, states={'draft':[('readonly',False)]}),
        'code': fields.char('Reference', size=32, readonly=True, states={'draft':[('readonly',False)]}),
        'asset_desc'       : fields.char("Description", size=512,  readonly=True, states={'draft':[('readonly',False)]}),
        'purchase_value': fields.float('Purchase Value', required=True, readonly=True, states={'draft':[('readonly',False)]}),
        'currency_id': fields.many2one('res.currency','Currency',required=False, readonly=True, states={'draft':[('readonly',False)]}),
        'company_id': fields.many2one('res.company', 'Company', required=True, readonly=True, states={'draft':[('readonly',False)]}),
        'note': fields.text('Note'),
        'purchase_date': fields.date('Purchase Date', required=True, readonly=True, states={'draft':[('readonly',False)]}),
        'state': fields.selection([('draft','Draft'),
                                   ('open','Running'),
                                   ('approve', "Waiting Approval"),
                                   ('close','Close'),
                                   ], 'Status', required=True, copy=False,
                                  help="When an asset is created, the status is 'Draft'.\n" \
                                       "If the asset is confirmed, the status goes in 'Running' and the depreciation lines can be posted in the accounting.\n" \
                                       "You can manually close an asset when the depreciation is over. If the last line of depreciation is posted, the asset automatically goes in that status."),
        'active': fields.boolean('Active'),
        'partner_id': fields.many2one('res.partner', 'Partner', readonly=True, states={'draft':[('readonly',False)]}),
        'group_id': fields.many2one('asset.extra.group', 'Asset Group', change_default=True, readonly=True, states={'draft':[('readonly',False)]}),
        'asset_class_id': fields.many2one('account.asset.class', 'Asset Class', change_default=True, readonly=True, states={'draft':[('readonly',False)]}),
        'purchase_date1': fields.date('Purchase Date', required=True, readonly=True, states={'draft':[('readonly',False)]}),
        'image': fields.binary("Image",
            help="This field holds the image used as image for the Asset, limited to 1024x1024px."),
        'asset_number': fields.char('Asset Number', required=True,copy=False, readonly=True, states={'draft':[('readonly',False)]}),
        'location': fields.char('Location',  readonly=True, states={'draft':[('readonly',False)]}),
        'user_id': fields.many2one('res.users', 'Responsible ', readonly=True, states={'draft':[('readonly',False)]}),
        'asset_location_id'    : fields.many2one('asset.location','Location'),
        'employee_id': fields.many2one("hr.employee", "PIC Asset", required=False, readonly=True, states={"draft": [("readonly", False)]}),
        'department_id' : fields.many2one("hr.department", "Department"),
        'distrik_id' : fields.many2one("hr.distrik", "Distrik"),
        'active'     : fields.boolean('Active'),    
        'log_asset_ids' : fields.one2many('asset.extra.log','asset_extra_id','Log'),
        'close_reason': fields.text("To Close Reasons", required=False, states={"approve": [("required", True)]}),
        'date_last_check' : fields.date('Last Check'),
        'origin' : fields.char("Source Document", size=128),
    }  
    
    _defaults = {
                 'purchase_date1': lambda obj, cr, uid, context: time.strftime('%Y-%m-%d'),
                 'asset_number': lambda obj, cr, uid, context: '/',  
                 'user_id': lambda obj, cr, uid, context: uid,
                 'active' : True,
                 'state': 'draft',
                 'company_id': lambda self, cr, uid, context: self.pool.get('res.company')._company_default_get(cr, uid, 'asset.extra',context=context),
                 } 
    
    def onchange_company_id(self, cr, uid, ids, company_id=False, context=None):
        val = {}
        if company_id:
            company = self.pool.get('res.company').browse(cr, uid, company_id, context=context)
            if company.currency_id.company_id and company.currency_id.company_id.id != company_id:
                val['currency_id'] = False
            else:
                val['currency_id'] = company.currency_id.id
        return {'value': val}
    
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
      
#     def create(self, cr, uid, vals, context=None):
#         if context is None:
#             context = {}
#         if vals.get('asset_number', '/') == '/':
#             vals['asset_number'] = self.pool.get('ir.sequence').get(cr, uid, 'asset.extra') or '/'
#         new_id = super(asset_extra, self).create(cr, uid, vals, context)
#         return new_id
    
    def validate(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        return self.write(cr, uid, ids, {
            'state':'open', 'asset_number':self.pool.get('ir.sequence').get(cr, uid, 'asset.extra') or '/'
        }, context)
        
    def set_to_close(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'approve'}, context=context)
    
    def appr_to_close(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'close'}, context=context)

    def set_to_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)
    
    

asset_extra()
    
class asset_extra_log(osv.osv):
    _name ="asset.extra.log"
    _description = "Log Asset Extra Comptable"
    _columns    = {
                   'date'   : fields.date("Date"),
                   'asset_extra_id': fields.many2one('asset.extra', "Asset Extra Compt"),
                   'employee_id' : fields.many2one('hr.employee',"Check By"),
                   'note'        : fields.char('Description', size=256),
                   'condition'   : fields.selection([('Baik',"Baik"),
                                                     ('Rusak',"Rusak"),
                                                     ], "Condition"),
                   
                   
                   }
    _defaults = {
                 'date': lambda obj, cr, uid, context: time.strftime('%Y-%m-%d'),
                
                 
                 } 

asset_extra_log()

class asset_extra_group(osv.osv):
    _name ="asset.extra.group"
    _description = "Asset Extra Group"
    _columns    = {
                   'code'   : fields.char("code", size=12),
                   'name': fields.char('Group Name',size=64),
                   'asset_id' : fields.one2many("asset.extra", "group_id", "Assets"),
                  # 'asset_extra_id' : fields.one2many('asset.extra','asset_group_id',"Assets"),
                   
                   
                   
                   }


asset_extra_group()
    