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

class account_asset_asset(osv.osv):
    _inherit = "account.asset.asset"
    
    def name_get(self, cr, uid, ids, context=None):
        print "name_get----------->>"
        res = []
        
        for val in self.browse(cr, uid, ids, context=context):
            name = val.name
            if val.asset_number and val.asset_number != "/":
                name = val.asset_number +" - "+ val.name
#             name = line.location_id.name + ' > ' + line.location_dest_id.name
#             if line.product_id.code:
#                 name = line.product_id.code + ': ' + name
#             if line.picking_id.origin:
#                 name = line.picking_id.origin + '/ ' + name
            res.append((val.id, name))
        return res
    
    def _compute_board_undone_tax_dotation_nb(self, cr, uid, asset, depreciation_date, total_days, context=None):
        undone_dotation_number = asset.tax_method_number
        if asset.method_time == 'end':
            end_date = datetime.strptime(asset.method_end, '%Y-%m-%d')
            undone_dotation_number = 0
            while depreciation_date <= end_date:
                depreciation_date = (datetime(depreciation_date.year, depreciation_date.month, depreciation_date.day) + relativedelta(months=+asset.method_period))
                undone_dotation_number += 1
        if asset.prorata:
            undone_dotation_number += 1
        return undone_dotation_number
    
    def _tax_amount_residual(self, cr, uid, ids, name, args, context=None):
        res={}
        for asset in self.browse(cr, uid, ids, context):
            amount=0
            posted_tax_dep_line=self.pool['account.asset.tax.depreciation.line'].search(cr, uid, [('move_check', '=', True), ('asset_id', '=', asset.id)])
            for tax_dep_line in self.pool['account.asset.tax.depreciation.line'].browse(cr, uid, posted_tax_dep_line, context):
                 amount +=  tax_dep_line.amount 
            company_currency = asset.company_id.currency_id.id
            current_currency = asset.currency_id.id
            #amount = self.pool['res.currency'].compute(cr, uid, company_currency, current_currency, res.get(asset.id, 0.0), context=context)
            res[asset.id] = asset.purchase_value - amount - asset.salvage_value
        for id in ids:
            res.setdefault(id, 0.0)
        return res

    def first_validate(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        return self.write(cr, uid, ids, {
            'state':'fa_validate'
        }, context)
    
#     def _amount_usd_residual(self, cr, uid, ids, name, args, context=None):
#         cr.execute("""SELECT
#                 l.asset_id as id, SUM(usd_amount) AS amount
#             FROM
#                 account_move_line l
#             WHERE
#                 l.asset_id IN %s GROUP BY l.asset_id """, (tuple(ids),))
#         res=dict(cr.fetchall())
#         for asset in self.browse(cr, uid, ids, context):
#             amount = res.get(asset.id, 0.0) or 0.0
#             
#             print ">>>>>>>>>>", amount
#             
#             res[asset.id] = asset.purchase_value_usd - amount
#         for id in ids:
#             res.setdefault(id, 0.0)
#         return res
    
    
    _columns = {
        'category_id': fields.many2one('account.asset.category', 'Asset Group', required=True, change_default=True, readonly=True, states={'draft':[('readonly',False)]}),
        'asset_group_id': fields.many2one('account.asset.group', 'Asset Categories', change_default=True, readonly=True, states={'draft':[('readonly',False)]}),
        'asset_class_id': fields.many2one('account.asset.class', 'Asset Class', change_default=True, readonly=True, states={'draft':[('readonly',False)]}),
        'purchase_date1': fields.date('Purchase Date', required=True, readonly=True, states={'draft':[('readonly',False)]}),
        
        'image': fields.binary("Image",
            help="This field holds the image used as image for the Asset, limited to 1024x1024px."),
        'asset_number': fields.char('Asset Number', required=True,copy=False, readonly=True, states={'draft':[('readonly',False)]}),
        'location': fields.char('Location',  readonly=True, states={'draft':[('readonly',False)]}),
        'user_id': fields.many2one('res.users', 'Responsible ', readonly=True, states={'draft':[('readonly',False)]}),
        'user_id': fields.many2one('res.users', 'Responsible ', readonly=True, states={'draft':[('readonly',False)]}),
        #tax depreciation method
        'tax_method_progress_factor': fields.float('Degressive Factor', readonly=True, states={'draft':[('readonly',False)]}),
        
        'tax_dep_method': fields.selection([('linear','Linear'),('degressive','Degressive')], 'Tax Depreciations Computation Method', required=True, readonly=True, states={'draft':[('readonly',False)]}, help="Choose the method to use to compute the amount of depreciation lines.\n"\
            "  * Linear: Calculated on basis of: Gross Value / Number of Depreciations\n" \
            "  * Degressive: Calculated on basis of: Residual Value * Degressive Factor"),
        
        'tax_value_residual': fields.function(_tax_amount_residual, method=True, digits_compute=dp.get_precision('Account'), string='Tax Residual Value'),
        
       'tax_depreciation_line_ids': fields.one2many('account.asset.tax.depreciation.line', 'asset_id', 'Depreciation Lines', readonly=True, states={'draft':[('readonly',False)],'open':[('readonly',False)]}),
       'state': fields.selection([('draft','Draft'),('fa_validate','Waiting FA Validate'),('open','Running'),('close','Close')], 'Status', required=True, copy=False,
                                  help="When an asset is created, the status is 'Draft'.\n" \
                                       "If the asset is confirmed, the status goes in 'Running' and the depreciation lines can be posted in the accounting.\n" \
                                       "You can manually close an asset when the depreciation is over. If the last line of depreciation is posted, the asset automatically goes in that status."),
        
        'tax_asset_category' : fields.many2one('account.asset.tax.category', 'Asset Tax Category'),
        'tax_method_number' : fields.integer('Tax Number of Depreciation', required=True),
        'tax_method_period' : fields.integer('Tax Period of Depreciation', required=True),
        'tax_asset_group'   : fields.char("Asset Group", size=16),
        'is_masterlist'     : fields.boolean("Is Asset Masterlist ?", help="Please Check if Asset is a Masterlist Assets"),
        'is_leasing'        : fields.boolean("Is Leasing Assets?", help="Please Check if Asset is a Masterlist Assets"),
        'leasing_no'        : fields.float("Leasing Period"),
        'asset_location_id'    : fields.many2one('asset.location','Location'),
        'asset_desc'       : fields.char("Description", size=512,  readonly=True, states={'draft':[('readonly',False)]}),
        'employee_id': fields.many2one("hr.employee", "PIC Asset", required=False, readonly=True, states={"draft": [("readonly", False)]}),
        'department_id' : fields.many2one("hr.department", "Department",  readonly=True, states={"draft": [("readonly", False)]}),
        #'distrik_id' : fields.many2one("hr.distrik", "Distrik", readonly=True, states={"draft": [("readonly", False)]}),
        ###
        'serial_number': fields.char("Serial Number", size=64),
        'brand'        : fields.char("Brand", size=128),
        'asset_reg_id'  : fields.many2one('asset.register', 'Asset Register ID'),
       # 'asset_distrik_id':fields.related('asset_reg_id', 'asset_distrik_id', type='many2one', relation='hr.distrik', string='Asset District', readonly=True),
        #'asset_distrik_id': fields.related("check_registered", "bank_id", relation='res.bank', type="many2one", readonly=True, string="Bank"),
        ###
        ###
        #'field1'    : fields.char('Field 1', size=128),
        'field1':fields.related('asset_reg_id', 'field1', type='char', string='Field 1'),
        'field2':fields.related('asset_reg_id', 'field2', type='char', string='Field 2'),
        'field3':fields.related('asset_reg_id', 'field3', type='char', string='Field 3'),
        'field4':fields.related('asset_reg_id', 'field4', type='char', string='Field 4'),
        'field5':fields.related('asset_reg_id', 'field5', type='char', string='Field 5'),
        'field6':fields.related('asset_reg_id', 'field6', type='char', string='Field 6'),
        'field7':fields.related('asset_reg_id', 'field7', type='char', string='Field 7'),
        'field8':fields.related('asset_reg_id', 'field8', type='char', string='Field 8'),
        'field9':fields.related('asset_reg_id', 'field9', type='char', string='Field 9'),
        ###
        
        ###
        #'purchase_value_usd' : fields.float('Gross Value USD'),
        #'value_residual_usd': fields.function(_amount_usd_residual, method=True, digits_compute=dp.get_precision('Account'), string='Residual USD Value'),
        ###
        
    }  
    
    _defaults = {
                 'purchase_date1': lambda obj, cr, uid, context: time.strftime('%Y-%m-%d'),
                 'asset_number': lambda obj, cr, uid, context: '/',  
                 'user_id': lambda obj, cr, uid, context: uid,
                 'tax_dep_method': 'degressive',
                 'tax_method_number': 5.0,
                 'tax_method_period' : 12.0
                 } 
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('asset_number', '/') == '/':
            pfx = self.pool.get('account.asset.class').browse(cr, uid, [vals.get('asset_class_id')], context=None)[0].code or ""
            
            print "XXXXXXXXXXXXXX", vals.get('asset_class_id'), pfx
            vals['asset_number'] = self.pool.get('ir.sequence').get(cr, uid, 'account.asset.asset') or '/'
            vals['asset_number'] = pfx + vals['asset_number']
            #raise (_('Error'), _('Not implemented'))
        new_id = super(account_asset_asset, self).create(cr, uid, vals, context)
        return new_id
    
    def onchange_petty_cash(self, cr, uid, ids, petty_request_id):
        print "XXXXXXXXXXXXXXXXX", petty_request_id
        res = {'value':{}}
        dst_journal_id  = False
        dst_amount      = 0.0
        
        cash_req_obj = self.pool.get('petty.cash.request')
        
        if petty_request_id:
            for val in cash_req_obj.browse(cr,uid,[petty_request_id],context=None):
                dst_journal_id  = val.petty_journal_id.id
                dst_amount      = val.amount_request
        res['value']['dst_journal_id']  = dst_journal_id
        res['value']['dst_amount']      = dst_amount
        
        print "res>>>>>>>>>>>>>>>>", res
        
        return res

    
    def onchange_parent_asset(self,cr,uid,ids,parent_id):
        res = {'value':{}}
        asset_obj = self.pool.get('account.asset.asset')
        
        if parent_id:
            for val in asset_obj.browse(cr,uid,[parent_id],context=None):
                res['value']['purchase_date'] = val.purchase_date
        
        return res
    
    def depreciation_sync(self, cr, uid, ids, context=None):
        for asset in self.browse(cr, uid, ids, context=None):
            if asset.state != 'open':
                raise (_('Error'), _('This Asset must in state Running'))
            
            if not asset.parent_id:
                raise (_('Error'), _('Parent asset not define'))
            
            cr.execute("select max(depreciation_date) from account_asset_depreciation_line where move_check = True and asset_id = %s" % (asset.parent_id.id,))
            last_depreciation_date = cr.fetchone()[0]
            
            cr.execute("select id from account_asset_depreciation_line where move_check = False and asset_id = %s and depreciation_date <= %s" , (asset.id, last_depreciation_date))
            to_depreciate_ids = map(lambda x: x[0], cr.fetchall())
            
            for depre in to_depreciate_ids:
                print "Derpe", depre
                self.pool.get('account.asset.depreciation.line').create_move(cr, uid, depre, context={'date_now':time.strftime('%Y-%m-%d')})
            
        return True
    
    def _compute_board_tax_amount(self, cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=None):
        #by default amount = 0
        amount = 0
        if i == undone_dotation_number:
            amount = residual_amount
        else:
            if asset.tax_dep_method == 'linear':
                amount = amount_to_depr / (undone_dotation_number - len(posted_depreciation_line_ids))
                if asset.prorata:
                    amount = amount_to_depr / asset.method_number
                    days = total_days - float(depreciation_date.strftime('%j'))
                    if i == 1:
                        amount = (amount_to_depr / asset.method_number) / total_days * days
                    elif i == undone_dotation_number:
                        amount = (amount_to_depr / asset.method_number) / total_days * (total_days - days)
            elif asset.tax_dep_method == 'degressive':
                amount = residual_amount * asset.tax_method_progress_factor
                if asset.prorata:
                    days = total_days - float(depreciation_date.strftime('%j'))
                    if i == 1:
                        amount = (residual_amount * asset.tax_method_progress_factor) / total_days * days
                    elif i == undone_dotation_number:
                        amount = (residual_amount * asset.tax_method_progress_factor) / total_days * (total_days - days)
        return amount
    
    def compute_tax_depreciation_board(self, cr, uid, ids, context=None):
        print ">>>>>>>>>>>>>>>>>>>>>"
        depreciation_lin_obj = self.pool.get('account.asset.tax.depreciation.line')
        currency_obj = self.pool.get('res.currency')
        for asset in self.browse(cr, uid, ids, context=context):
            if asset.value_residual == 0.0:
                continue
            posted_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_check', '=', True)],order='depreciation_date desc')
            old_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id)])
            if old_depreciation_line_ids:
                depreciation_lin_obj.unlink(cr, uid, old_depreciation_line_ids, context=context)

            amount_to_depr = residual_amount = asset.value_residual
            
            depreciation_date = datetime.strptime(self._get_last_depreciation_date(cr, uid, [asset.id], context)[asset.id], '%Y-%m-%d')
            ####TAMABHAN BARU###########
            day = depreciation_date.day
            month = depreciation_date.month
            year = depreciation_date.year
            total_days = (year % 4) and 365 or 366
            
            days_current_month = calendar.mdays[datetime(year, month, day).month]
            depreciation_date = datetime(depreciation_date.year, depreciation_date.month, days_current_month)
            #####################
            #####################################
#             if asset.prorata:
#                 depreciation_date = datetime.strptime(self._get_last_depreciation_date(cr, uid, [asset.id], context)[asset.id], '%Y-%m-%d')
#             else:
#                 # depreciation_date = 1st January of purchase year
#                 purchase_date = datetime.strptime(asset.purchase_date, '%Y-%m-%d')
#                 #if we already have some previous validated entries, starting date isn't 1st January but last entry + method period
#                 if (len(posted_depreciation_line_ids)>0):
#                     last_depreciation_date = datetime.strptime(depreciation_lin_obj.browse(cr,uid,posted_depreciation_line_ids[0],context=context).depreciation_date, '%Y-%m-%d')
#                     depreciation_date = (last_depreciation_date+relativedelta(months=+asset.method_period))
#                 else:
#                     depreciation_date = datetime(purchase_date.year, 1, 1)
            ####################################
                    
            day = depreciation_date.day
            month = depreciation_date.month
            year = depreciation_date.year
            
            
            ###################
            print "month--------->>", month
            print "year--------->>", year
            
            start_year = year
            end_year = (datetime(year, month, day) + relativedelta(months=asset.tax_method_number-1)).year
            print "end_year>>>>>>>>>>>>", start_year, end_year
            
            for setyear in range(start_year, end_year+1):
                print "iiiiiiii", setyear
            
            
            total_days = (year % 4) and 365 or 366
            
            month_of_current_year   =  12-month+1
            month_of_last_year      =  month-1
            year_old                = 0
            amount                  = 0.0
            
            
            ##First Year###
            amount = ((month_of_current_year/12.0)*asset.tax_method_progress_factor * asset.tax_value_residual) / month_of_current_year
            
            print "amount*********************", asset.tax_value_residual, amount
            ###################
            
            undone_dotation_number = self._compute_board_undone_tax_dotation_nb(cr, uid, asset, depreciation_date, total_days, context=context)
            
            print "undone_dotation_number>>>>>>>>>>>", len(posted_depreciation_line_ids), undone_dotation_number
            
            for x in range(len(posted_depreciation_line_ids), undone_dotation_number):
                i = x + 1
                #amount = self._compute_board_tax_amount(cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=context)
                
                #####################
                if depreciation_date.year != start_year:
                    if depreciation_date.year != year_old:
                        year_old = depreciation_date.year
                        #if depreciation_date.year == start_year:
                        #    amount = (((month_of_current_year/12)*asset.tax_method_progress_factor * residual_amount) / 12)
#                         if depreciation_date.year == end_year:
#                             print "CCCCCCCCCCCCCCCCCCCCCCCCCCCC", i
#                             amount = ((residual_amount) / month_of_last_year)
#                         else:
#                             amount = ((asset.tax_method_progress_factor * residual_amount) / 12.0)
                        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", i
                        
                            
                        amount = ((asset.tax_method_progress_factor * residual_amount) / 12.0)
                #######Bulan Akhir####
                if i == asset.tax_method_number:
                    amount = residual_amount
                ######################
                print "amount------------->>", amount
                #####################
                residual_amount -= amount
                vals = {
                     'amount': amount,
                     'asset_id': asset.id,
                     'sequence': i,
                     'name': str(asset.id) +'/' + str(i),
                     'remaining_value': residual_amount,
                     'depreciated_value': (asset.purchase_value - asset.salvage_value) - (residual_amount + amount),
                     'depreciation_date': depreciation_date.strftime('%Y-%m-%d'),#depreciation_date.strftime('%Y-%m-25'),
                }
                depreciation_lin_obj.create(cr, uid, vals, context=context)
                # Considering Depr. Period as months
                #depreciation_date = (datetime(year, month, day) + relativedelta(months=+asset.method_period))
                
                depreciation_date = (datetime(year, month, day) + relativedelta(months=+asset.tax_method_period))
                depreciation_date = datetime(depreciation_date.year, depreciation_date.month, calendar.mdays[depreciation_date.month])
                
                
                day = depreciation_date.day
                month = depreciation_date.month
                year = depreciation_date.year
        return True
            
    def compute_depreciation_board_anoop(self, cr, uid, ids, context=None):
        depreciation_lin_obj = self.pool.get('account.asset.depreciation.line')
        tax_depreciation_lin_obj = self.pool.get('account.asset.tax.depreciation.line')
        currency_obj = self.pool.get('res.currency')
        for asset in self.browse(cr, uid, ids, context=context):
            if asset.value_residual == 0.0:
                continue
            posted_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_check', '=', True)],order='depreciation_date desc')
            old_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_id', '=', False)])
            
            if old_depreciation_line_ids:
                depreciation_lin_obj.unlink(cr, uid, old_depreciation_line_ids, context=context)
            
            old_tax_depreciation_line_ids = tax_depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_check', '=', False)])
            if old_tax_depreciation_line_ids:
                tax_depreciation_lin_obj.unlink(cr, uid, old_tax_depreciation_line_ids, context=context)
            
            
            amount_to_depr = residual_amount = asset.value_residual
            tax_amount_to_depr = tax_residual_amount = asset.tax_value_residual
                
            if asset.prorata:
                depreciation_date = datetime.strptime(self._get_last_depreciation_date(cr, uid, [asset.id], context)[asset.id], '%Y-%m-%d')
            else:
                # depreciation_date = 1st January of purchase year
                purchase_date = datetime.strptime(asset.purchase_date, '%Y-%m-%d')
                #if we already have some previous validated entries, starting date isn't 1st January but last entry + method period
                if (len(posted_depreciation_line_ids)>0):
                    last_depreciation_date = datetime.strptime(depreciation_lin_obj.browse(cr,uid,posted_depreciation_line_ids[0],context=context).depreciation_date, '%Y-%m-%d')
                    depreciation_date = (last_depreciation_date+relativedelta(months=+asset.method_period))
                else:
                    depreciation_date = datetime(purchase_date.year, 1, 1)
            day = depreciation_date.day
            month = depreciation_date.month
            year = depreciation_date.year
            total_days = (year % 4) and 365 or 366

            undone_dotation_number = self._compute_board_undone_dotation_nb(cr, uid, asset, depreciation_date, total_days, context=context)
            for x in range(len(posted_depreciation_line_ids), undone_dotation_number):
                i = x + 1
                amount = self._compute_board_amount(cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=context)
                residual_amount -= amount
                vals = {
                     'amount': amount,
                     'asset_id': asset.id,
                     'sequence': i,
                     'name': str(asset.id) +'/' + str(i),
                     'remaining_value': residual_amount,
                     'depreciated_value': (asset.purchase_value - asset.salvage_value) - (residual_amount + amount),
                     'depreciation_date': depreciation_date.strftime('%Y-%m-%d'),
                }
                dep_line_id=depreciation_lin_obj.create(cr, uid, vals, context=context)
                
                 #tax depreciation line creation
                tax_amount = self._compute_board_tax_amount(cr, uid, asset, i, tax_residual_amount, tax_amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=context)
                tax_residual_amount -= tax_amount
                vals = {
                     'amount': tax_amount,
                     'asset_id': asset.id,
                     'sequence': i,
                     'name': str(asset.id) +'/' + str(i),
                     'remaining_value': tax_residual_amount,
                     'depreciated_value': (asset.purchase_value - asset.salvage_value) - (tax_residual_amount + tax_amount),
                     'depreciation_date': depreciation_date.strftime('%Y-%m-%d'),
                     'account_asset_depreciation_line': dep_line_id,
                     
                }
                tax_depreciation_lin_obj.create(cr, uid, vals, context=context)
                
                # Considering Depr. Period as months
                depreciation_date = (datetime(year, month, day) + relativedelta(months=+asset.method_period))
                day = depreciation_date.day
                month = depreciation_date.month
                year = depreciation_date.year
        return True
    
    def compute_depreciation_board(self, cr, uid, ids, context=None):
        depreciation_lin_obj = self.pool.get('account.asset.depreciation.line')
        for asset in self.browse(cr, uid, ids, context=context):
            if asset.value_residual == 0.0:
                continue
            posted_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_check', '=', True)])
            old_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_id', '=', False)])
            if old_depreciation_line_ids:
                depreciation_lin_obj.unlink(cr, uid, old_depreciation_line_ids, context=context)
            
            amount_to_depr = residual_amount = asset.value_residual

            depreciation_date = datetime.strptime(self._get_last_depreciation_date(cr, uid, [asset.id], context)[asset.id], '%Y-%m-%d')
            day = depreciation_date.day
            month = depreciation_date.month
            year = depreciation_date.year
            total_days = (year % 4) and 365 or 366
            
            days_current_month = calendar.mdays[datetime(year, month, day).month]
            depreciation_date = datetime(depreciation_date.year, depreciation_date.month, days_current_month)
#            
            undone_dotation_number = self._compute_board_undone_dotation_nb(cr, uid, asset, depreciation_date, total_days, context=context)
            for x in range(len(posted_depreciation_line_ids), undone_dotation_number):
                i = x + 1
                amount = self._compute_board_amount(cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=context)
                residual_amount -= amount
                vals = {
                     'amount': amount,
                     'asset_id': asset.id,
                     'sequence': i,
                     'name': str(asset.id) +'/' + str(i),
#                      'name': asset.code + ':' + str(i),
                     'remaining_value': residual_amount,
                     'depreciated_value': (asset.purchase_value - asset.salvage_value) - (residual_amount + amount),
                     'depreciation_date': depreciation_date.strftime('%Y-%m-%d'),
                     ###
                     #'amount_usd': asset.purchase_value_usd/asset.method_number,
                }
                depreciation_lin_obj.create(cr, uid, vals, context=context)
                # Considering Depr. Period as months
#                 days_current_month = calendar.mdays[datetime(year, month, day).month]
#                 depreciation_date = (datetime(year, month, days_current_month) + relativedelta(months= +asset.method_period))
                depreciation_date = (datetime(year, month, day) + relativedelta(months=+asset.method_period))
                depreciation_date = datetime(depreciation_date.year, depreciation_date.month, calendar.mdays[depreciation_date.month])
                
#                 
                day = depreciation_date.day
                month = depreciation_date.month
                year = depreciation_date.year
        return True
    
    
    
    
    
    
   
    
    def onchange_tax_category(self, cr, uid, ids, tax_asset_category, context=None):
        if not tax_asset_category:
            return {'value': {
                              'tax_asset_group' : False,
                              'tax_method_number': False,
                              'tax_method_period': False,
                              'tax_method_progress_factor': False,
                             
                              }}
        ass = self.pool.get('account.asset.tax.category').browse(cr, uid, tax_asset_category, context=context)
       
        if ass:
            tax_asset_group = ass.grup
            tax_method_number = ass.tax_method_number_cat
            tax_method_period = ass.tax_method_period_cat
            tax_method_progress_factor = ass.tax_method_progress_factor_cat
        return {'value': {
                              'tax_asset_group' : tax_asset_group,
                              'tax_method_number': tax_method_number,
                              'tax_method_period': tax_method_period,
                              'tax_method_progress_factor': tax_method_progress_factor,
                             
                              }}

class asset_location(osv.osv):
    _name = "asset.location"
    _columns = {
                'name'  : fields.char('Location'),
                'asset_area_id'  : fields.many2one('asset.area','Area'),
                }

class asset_area(osv.osv):
    _name = "asset.area"
    _columns = {
                'name'  : fields.char('Area'),
                'asset_gedung_id'  : fields.many2one('asset.gedung','Gedung'),
                }
    
class asset_gedung(osv.osv):
    _name = "asset.gedung"
    _columns = {
                'name'  : fields.char('Gedung'),
                }
         
class account_asset_depreciation_line(osv.osv):
    _inherit = 'account.asset.depreciation.line'

    def unlink(self, cr, uid, ids, context=None):
        for asset_line in self.browse(cr, uid, ids, context=context):
               tax_line_ids= self.pool.get('account.asset.tax.depreciation.line').search(cr,uid,[ ('account_asset_depreciation_line', '=', asset_line.id)], context=context)
               if tax_line_ids :
                   self.pool.get('account.asset.tax.depreciation.line').unlink(cr, uid, tax_line_ids, context=context)
        return super(account_asset_depreciation_line, self).unlink(cr, uid, ids, context=context)
    
    _columns = {
            'amount_usd': fields.float('Current USD', digits_compute=dp.get_precision('Account'), required=False),
                }
    
    def create_move(self, cr, uid, ids, context=None):
        print "$############create_move", context
        
        context = dict(context or {})
        can_close = False
        asset_obj = self.pool.get('account.asset.asset')
        period_obj = self.pool.get('account.period')
        move_obj = self.pool.get('account.move')
        move_line_obj = self.pool.get('account.move.line')
        currency_obj = self.pool.get('res.currency')
        created_move_ids = []
        asset_ids = []
        for line in self.browse(cr, uid, ids, context=context):
            depreciation_date = context.get('date_now') or context.get('depreciation_date') or line.depreciation_date or time.strftime('%Y-%m-%d')
            period_ids = period_obj.find(cr, uid, depreciation_date, context=context)
            company_currency = line.asset_id.company_id.currency_id.id
            current_currency = line.asset_id.currency_id.id
            context.update({'date': depreciation_date})
            amount = currency_obj.compute(cr, uid, current_currency, company_currency, line.amount, context=context)
            sign = (line.asset_id.category_id.journal_id.type == 'purchase' and 1) or -1
            seq = line.name
            reference = line.asset_id.name
            asset_name = "Depreciation ke " + seq +" " + reference
            move_vals = {
                'name': '/',
                'date': depreciation_date,
                'ref': reference,
                'period_id': period_ids and period_ids[0] or False,
                'journal_id': line.asset_id.category_id.journal_id.id,
                }
            move_id = move_obj.create(cr, uid, move_vals, context=context)
            journal_id = line.asset_id.category_id.journal_id.id
            partner_id = line.asset_id.partner_id.id
            move_line_obj.create(cr, uid, {
                'name': asset_name,
                'ref': reference,
                'move_id': move_id,
                'account_id': line.asset_id.category_id.account_depreciation_id.id,
                'debit': 0.0,
                'credit': amount,
                'period_id': period_ids and period_ids[0] or False,
                'journal_id': journal_id,
                'partner_id': partner_id,
                'currency_id': company_currency != current_currency and  current_currency or False,
                'amount_currency': company_currency != current_currency and - sign * line.amount or 0.0,
                'date': depreciation_date,
                ###
               # 'usd_amount':-line.amount_usd,
                #'district': line.asset_id.asset_distrik_id.id,
            })
            move_line_obj.create(cr, uid, {
                'name': asset_name,
                'ref': reference,
                'move_id': move_id,
                'account_id': line.asset_id.category_id.account_expense_depreciation_id.id,
                'credit': 0.0,
                'debit': amount,
                'period_id': period_ids and period_ids[0] or False,
                'journal_id': journal_id,
                'partner_id': partner_id,
                'currency_id': company_currency != current_currency and  current_currency or False,
                'amount_currency': company_currency != current_currency and sign * line.amount or 0.0,
                'analytic_account_id': line.asset_id.category_id.account_analytic_id.id,
                'date': depreciation_date,
                'asset_id': line.asset_id.id,
                ###
               # 'usd_amount':line.amount_usd,
                #'district': line.asset_id.asset_distrik_id.id,
            })
            self.write(cr, uid, line.id, {'move_id': move_id}, context=context)
            created_move_ids.append(move_id)
            asset_ids.append(line.asset_id.id)
        # we re-evaluate the assets to determine whether we can close them
        for asset in asset_obj.browse(cr, uid, list(set(asset_ids)), context=context):
            if currency_obj.is_zero(cr, uid, asset.currency_id, asset.value_residual):
                asset.write({'state': 'close'})
        return created_move_ids
    
class account_asset_tax_depreciation_line(osv.osv):
    _name = 'account.asset.tax.depreciation.line'
    _description = 'Asset Tax depreciation line'

  

    _columns = {
        'name': fields.char('Depreciation Name', required=True, select=1),
        'sequence': fields.integer('Sequence', required=True),
        'asset_id': fields.many2one('account.asset.asset', 'Asset', required=True, ondelete='cascade'),
        'parent_state': fields.related('asset_id', 'state', type='char', string='State of Asset'),
        'amount': fields.float('Current Depreciation', digits_compute=dp.get_precision('Account'), required=True),
        'remaining_value': fields.float('Next Period Depreciation', digits_compute=dp.get_precision('Account'),required=True),
        'depreciated_value': fields.float('Amount Already Depreciated', required=True),
        'depreciation_date': fields.date('Depreciation Date', select=1),
        'account_asset_depreciation_line': fields.many2one('account.asset.depreciation.line', 'Depreciation line Entry'),
        'move_check': fields.related('account_asset_depreciation_line', 'move_check', type='boolean',  string='Posted', readonly=True),
        
    } 

    
class account_asset_tax_category(osv.osv):
    _name = 'account.asset.tax.category'
    _description = 'Asset Tax Category'

  

    _columns = {
        'name': fields.char('Depreciation Name', required= True, select=1),
        'sequence': fields.integer('Sequence'),
        'grup' : fields.selection([('Bangunan','Bangunan'),('Bukan Bangunan','Bukan Bangunan')], 'Group', required=True, copy=False,
                                  help="Kelompok Bangunan atau bukan bangunan'.\n"
                                      ),
        'tax_method_number_cat' : fields.integer('Tax Number of Depreciation'),
        'tax_method_period_cat' : fields.integer('Tax Period of Depreciation'),
        'tax_method_progress_factor_cat': fields.float('Degressive Factor'),
        
        'tax_dep_method_cat': fields.selection([('linear','Linear'),('degressive','Degressive')], 'Tax Depreciations Computation Method', required= True)
           
        
    } 