# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2016 Databit Solusi Indonesia
#    (http://wwww.databit.co.id)
#    
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

import psycopg2
import tempfile
import base64
from PIL import Image
import io, StringIO
from reportlab.graphics.barcode import createBarcodeDrawing
from dateutil.relativedelta import relativedelta

import logging


class installation(osv.osv):
    _name = "installation"
    _description ="Form Installation"
    
    def _asset_barcode(self, cr, uid, ids, name, args, context=None):
        _logger = logging.getLogger(__name__)
        
        res = {}
        for ass in self.browse(cr, uid, ids, context=context):
            if ass.state != 'draft':
                number  = ass.warranty_no
        
                barcode = createBarcodeDrawing('Code128', value=str(number), width=300, height=30, humanreadable=True)
                image_data = barcode.asString('png')
                label = base64.encodestring(image_data)
                
                res[ass.id] = label
            else :
                #print ">>>>>>><<<<<>><><><><><><>", "kesini"
                res[ass.id] = False 
        return res
    
    
    _columns = {
              'name'         : fields.char('Name', readonly=True),
              'user_id'      : fields.many2one('res.users', 'Responsible ', readonly=True, states={'draft':[('readonly',False)]}),
              'date_create'   : fields.datetime('Create Date', readonly=True, states={"draft": [("readonly", False)]}),
              'customer_id'     : fields.many2one('res.partner','Sold To', readonly=True, states={"draft": [("readonly", False)]}),
              'partner_id'     : fields.many2one('res.partner','Install To', readonly=True, states={"draft": [("readonly", False)]}),
              'contact_id'    : fields.many2one('res.partner', 'Contact Name', readonly=True, states={"draft": [("readonly", False)]}),
              'contact2_id'    : fields.many2one('res.partner', 'Contact Name', readonly=True, states={"draft": [("readonly", False)]}),
              'responsible_id' : fields.many2one('hr.employee','Install By', readonly=True, states={"draft": [("readonly", False)]}),
              'so_id'        : fields.many2one('sale.order','Sales No', readonly=True, states={"draft": [("readonly", False)]}),
              'do_id'        : fields.many2one('stock.picking','DO No', readonly=True, states={"draft": [("readonly", False)]}),
              'date_install'    : fields.datetime('Installation Date', readonly=True, states={"draft": [("readonly", False)]}),
              'date_finish'     : fields.datetime('Finish Date'),
              'product_id'      : fields.many2one('product.product','Unit',readonly=True, states={"draft": [("readonly", False)]}),
              'unit_id'         : fields.many2one('sale.order.line','Unit', readonly=True, states={"draft": [("readonly", False)]}),
              'cost_ids'        : fields.one2many('installation.cost','installation_id','Costs'),
              'task_ids'        : fields.one2many('installation.task','installation_id','Tasks'),
              'state'           : fields.selection([('draft','Draft'),
                                                    ('confirm','Confirm'),
                                                    ('progress','Progress'),
                                                    ('done','Done'),
                                                    ('cancel','Cancel')
                                                    ],'State'),
                'sale_ref'      : fields.char('Sale No', readonly=True, states={"draft": [("readonly", False)]}),
                'move_ref'      : fields.char('DO No',readonly=True, states={"draft": [("readonly", False)]}),
                'default_code'      : fields.char('Type',readonly=True, states={"draft": [("readonly", False)]}),
                'lot_number'      : fields.many2one('stock.production.lot','Serial Number',readonly=True, states={"draft": [("readonly", False)]}),
                'brand_id'      : fields.many2one('product.brand','Brand',readonly=True, states={"draft": [("readonly", False)]}),
                'man_country'      : fields.many2one('res.country','Country Origin',readonly=True, states={"draft": [("readonly", False)]}),
                'notes'             : fields.text('Notes'),
                'company_id': fields.many2one('res.company', 'Company', required=True, readonly=True, states={'draft':[('readonly',False)]}),
                'phone1'    : fields.char('Phone / Fax',readonly=True, states={"draft": [("readonly", False)]}),
                'phone2'    : fields.char('Phone / Fax',readonly=True, states={"draft": [("readonly", False)]}),
                'email1'    : fields.char('Email',readonly=True, states={"draft": [("readonly", False)]}),
                'email2'    : fields.char('Email',readonly=True, states={"draft": [("readonly", False)]}),
                'contact1'    : fields.char('Contact Person',readonly=True, states={"draft": [("readonly", False)]}),
                'contact2'    : fields.char('Contact Person',readonly=True, states={"draft": [("readonly", False)]}),
                'warranty_no'   : fields.char('Warranty Number'),
                'valid_date'    : fields.date('Warranty Valid Until'),
                'war_barcode' : fields.function(_asset_barcode, method=True, string='barcode', type='binary'),
                }
    
    
    _defaults = {
                 'name'  : '/',
                 'date_create'  : fields.datetime.now,
                 'user_id'      : lambda obj, cr, uid, context: uid,
                 'state'        : 'draft',
                 'company_id': lambda self, cr, uid, context: self.pool.get('res.company')._company_default_get(cr, uid, 'installation',context=context),
                 
                 }
    
    
    
    def onchange_date(self, cr, uid, ids,date_finish):
        
        result = {'value':{'valid_date':False}}
        
        if date_finish :
            date = datetime.strptime(date_finish,'%Y-%m-%d %H:%M:%S')
            valid_date = datetime.date(date) + relativedelta(years=1)
            print "dddddddddd",valid_date
            result['value']={'valid_date':valid_date}
        
            
        return result

    def onchange_product(self, cr, uid, ids, product_id):
        
        for onchange in self.pool.get('product.product').browse(cr, uid, [product_id], context=None):
            print '1111111'
            code = onchange.default_code
            brand = onchange.product_brand_id.id
            con = onchange.product_country.id
            return {'value':{'man_country': con,
                             'default_code': code,
                             'brand_id' : brand,
                             
                             }}
        
    
    def action_confirm(self, cr, uid, vals,context=None):
        if context is None:
             context = {}
        
        for ins in self.browse(cr, uid, vals, context=None):
             if ins.name =='/':
                code = ins.default_code or ""
                bulan = time.strftime('%m', time.strptime( ins.date_create,'%Y-%m-%d %H:%M:%S'))
                tahun = time.strftime('%y', time.strptime( ins.date_create,'%Y-%m-%d %H:%M:%S'))
                print "kkkkkkkkkkkkkkkkkkk", bulan
                name = self.pool.get('ir.sequence').get(cr, uid, 'installation') or '/'
                name = name + '_BA-INST/'+ code+'/PMS/'+ bulan + '/' + tahun
             else :
                name = ins.name
        return self.write(cr, uid, vals, {'state': 'confirm', 'name': name}, context=context)
    
    def progress(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'progress'}, context=context)
    
    def done(self, cr, uid, ids, context=None):
        for ins in self.browse(cr, uid, ids, context=None):
            code = ins.default_code or ""
            tanggal = time.strftime('%d', time.strptime( ins.date_finish,'%Y-%m-%d %H:%M:%S'))
            bulan = time.strftime('%m', time.strptime( ins.date_finish,'%Y-%m-%d %H:%M:%S'))
            tahun = time.strftime('%y', time.strptime( ins.date_finish,'%Y-%m-%d %H:%M:%S'))
            name = 'PS'+code+tanggal+ bulan+tahun
        return self.write(cr, uid, ids, {'state': 'done','warranty_no': name}, context=context)
    
    def cancel(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)
    
    def set_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)
    
    def unlink(self, cr, uid, ids, context=None):
        context = context or {}
        for move in self.browse(cr, uid, ids, context=context):
            if move.state not in ('draft', 'cancel'):
                raise osv.except_osv(_('User Error!'), _('You can only delete installation on draft state'))
        return True
    
    def print_bast(self, cr, uid, ids, context=None):
        assert len(ids) == 1
        return self.pool['report'].get_action(cr, uid, ids, 'report_installation', context=context)
    def print_war(self, cr, uid, ids, context=None):
        assert len(ids) == 1
        return self.pool['report'].get_action(cr, uid, ids, 'report_warranty', context=context)
    
    
installation()

class installation_task(osv.osv):
    _name ='installation.task'
    _description = "Installation Task"
    _columns = {
                'installation_id' : fields.many2one('installation','Installation No'),
                'name'            : fields.char('Work Task', size=256, required=True),
                'description'     : fields.text('Description'),
                'result'          : fields.selection([('working','Working Properly'),
                                                      ('fix','Fixed Need'),
                                                      ('broken','Broken'),
                                                      ('skip','Skips'),
                                                      ]
                                                     ,'Result'),
                'next_action'          : fields.char('Next Action', size=256),
                
                
                }



installation_task()


class installation_cost(osv.osv):
    _name ='installation.cost'
    _description = "Installation Cost"
    _columns = {
                'installation_id' : fields.many2one('installation','Installation No'),
                'type'            : fields.many2one('installation.cost.type','Cost Type'),
                'description'     : fields.char('Description', size=128),
                'employee_id'     : fields.many2one('hr.employee','Employee'),
                'amount'          : fields.float('amount'),
                
                
                }



installation_cost()

class installation_cost_type(osv.osv):
    _name       =   'installation.cost.type'
    _columns    = {
                   'name'   : fields.char('Name', required=True),
                   'code'   : fields.char('Code'),
                   'account_id' : fields.many2one('account.account','Account Code'),
                   
                   }
    
    
installation_cost_type()
