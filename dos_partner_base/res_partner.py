# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

import datetime
from lxml import etree
import math
import pytz
import re

import openerp
from openerp import SUPERUSER_ID
from openerp import pooler, tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.tools.yaml_import import is_comment
from openerp import tools, api

class res_partner(osv.osv):
    _inherit    = 'res.partner'
    _description= 'Partner Inherit'
    _columns    = {
                   'code'               : fields.char('Code Customer',size=16),
                   'birthday'           : fields.datetime('Birthday'),
                   #'area_id'            : fields.many2one('res.branch','Area'),
                   'hobby'              : fields.char('Hobby'),
                   'wife'               : fields.char('Wife'),
                   'fav_book'           : fields.char('Favorite Books'),
                   'fav_food'           : fields.char('Favorite Foods'),
				   #'competitor_product' : fields.one2many('product.competitor','competitor_product_id',' ',),
                   'group_id'           : fields.many2one('res.partner','Group/Holding'),
                   'kode_status'        : fields.char('kode status', size=1),
          'npwp'	    : fields.char('NPWP', size=64),
          'street_npwp'    : fields.char('Street'),
          'street2_npwp'   : fields.char('Street2'),
          'city_npwp'      : fields.char('City'),
          'state_id_npwp'  : fields.many2one('res.country.state','State'),
          'zip_npwp'       : fields.char('ZIP'),
				   ### company profile ###
 				   'akta_pendirian_id'  : fields.char('No Akta Pendirian', size=64),
                    'akta_file'      : fields.binary('AKTA Attachment'),
 				   'siup_id'	: fields.char('No SIUP', size=64),
                    'siup_file' : fields.binary('SIUP Attachment'),
                    'pkp'       : fields.boolean("PKP"),
 				   'tdp_id'		: fields.char('No TDP', size=64),
                    'tdp_file'  : fields.binary('TDP Attachment'),
                    'other_file': fields.binary('Other Attachment'),
				   'business_sector'	: fields.many2one('business.sector',' Business Sector'),
        		   'type'               : fields.selection([('default', 'Default'), ('invoice', 'Invoice'),
                                                            ('delivery', 'Shipping'), ('contact', 'Contact'),
                                                            ('other', 'Other')], 'Address Type',
        			                                     help="Used to select automatically the right address according to the context in sales and purchases documents."),
			        'street'            : fields.char('Street', size=128),
			        'street2'           : fields.char('Street2', size=128),
			        'zip'               : fields.char('Zip', change_default=True, size=24),
			        'city'              : fields.char('City', size=128),
                    'user_id_2'         : fields.many2one('res.users','Salesperson 2'),
                    'user_id_3'         : fields.many2one('res.users','Salesperson 3'), 
			        'state_id'          : fields.many2one("res.country.state", 'State'),
			        'country_id'        : fields.many2one('res.country', 'Country'),
                   

			        'country'           : fields.related('country_id', type='many2one', relation='res.country', string='Country',
			                                  deprecated="This field will be removed as of OpenERP 7.1, use country_id instead"),
                    'investor_country'  : fields.many2one('res.country','Country of Investor'),
                   
                    'legal_ids'          : fields.one2many('company.legal','partner_id', "Legal"),
                    
                    
                ####
                    'contact_name1'      : fields.char('Name', size=64),
                    'street_contact1'    : fields.char('Street'),
                    'street2_contact1'   : fields.char('Street2'),
                    'city_contact1'      : fields.char('City'),
                    'state_id_contact1'  : fields.many2one('res.country.state','State'),
                    'zip_contact1'       : fields.char('ZIP'),
                    'country_id_contact1': fields.many2one('res.country', 'Country'),
                    
                    'contact_name2'      : fields.char('Name', size=64),
                    'street_contact2'    : fields.char('Street'),
                    'street2_contact2'   : fields.char('Street2'),
                    'city_contact2'      : fields.char('City'),
                    'state_id_contact2'  : fields.many2one('res.country.state','State'),
                    'zip_contact2'       : fields.char('ZIP'),
                    'country_id_contact2': fields.many2one('res.country', 'Country'),
                   }


      

    _defaults   = {
                   #'is_company' : True,
                   'user_id'    : lambda self, cr, uid, context: uid,
                   'code'       : '/',
                   #'section_id' : lambda self,cr,uid,c: self.pool.get('res.users').browse(cr, uid, uid, c).default_section_id.id,
                   }
    
    
    def create(self, cr, uid, vals, context=None):
        if vals.get('is_company',True)==True :
           if vals.get('parent_id',False)==False :  
              vals['code'] = self.pool.get('ir.sequence').get(cr, uid, 'res.partner') or '/'
        else :
                vals['code'] = '/'
        order =  super(res_partner, self).create(cr, uid, vals, context=context)
        return order
    
    @api.multi
    def write(self, vals):
        # res.partner must only allow to set the company_id of a partner if it
        # is the same as the company of all users that inherit from this partner
        # (this is to allow the code from res_users to write to the partner!) or
        # if setting the company_id to False (this is compatible with any user
        # company)
        if vals.get('website'):
            vals['website'] = self._clean_website(vals['website'])
        if vals.get('company_id'):
            company = self.env['res.company'].browse(vals['company_id'])
            for partner in self:
                if partner.user_ids:
                    companies = set(user.company_id for user in partner.user_ids)
                    if len(companies) > 1 or company not in companies:
                        raise osv.except_osv(_("Warning"),_("You can not change the company as the partner/user has multiple user linked with different companies."))
        
        
        for partner in self:
            ####
            if partner.is_company==True and partner.code == '/':
                code = self.env['ir.sequence'].get('res.partner') or '/'
                vals.update({'code': code})
            ####
        
        
        result = super(res_partner, self).write(vals)
        for partner in self:
            self._fields_sync(partner, vals)
        return result

    def onchange_sales_team(self, cr, uid, ids, sales, context=None):
        if sales:
            team = self.pool.get('res.partner').browse(cr, uid, address, context=context)
            return {'value': {'street': address.street,'street2' : address.street2,
            'city' : address.city,'state_id' : address.state_id.id,'zip' : address.zip,
            'country_id' : address.country_id.id, 'type' :address.type, 'partner_phone' : address.mobile, 'sales_id' : address.user_id.id,}}
        return {'value': {}}

    _sql_constraints = [
        ('npwp_uniq', 'unique(npwp)', 'The npwp of the customer must be unique!'),
    ]


res_partner()

class company_legal(osv.osv):
    _name = "company.legal"
    _columns = {

            'number' : fields.char('Number', size=24),
            'name'              : fields.char('Description', size=64),
            'date_release'                 : fields.date('Date Release'),
            'date_end'      : fields.date('Valid Until'),
            'file'                   : fields.binary('Attachment'),
            'note'                  : fields.char('Notes'),
            'partner_id'    : fields.many2one('res.partner','partner'),
            'lembaga_penerbit' : fields.char('Lembaga Penerbit'),
    }
company_legal()

class business_sector(osv.osv):
    _name = "business.sector"
    _columns = {
            'code'	: fields.char('Code', size=64),
            'name'	: fields.char('Name', size=64),
            'customer_ids': fields.one2many('res.partner','business_sector','Customer')
    }
business_sector()

class res_partner_bank(osv.osv):
    '''Bank Accounts'''
    _inherit    = "res.partner.bank"
    _columns = {
            #'currency_id' : fields.many2one('res.currency', 'Currency'),
                }
    
    def _prepare_name_get(self, cr, uid, bank_dicts, context=None):
        """ Format the name of a res.partner.bank.
            This function is designed to be inherited to add replacement fields.
            :param bank_dicts: a list of res.partner.bank dicts, as returned by the method read()
            :return: [(id, name), ...], as returned by the method name_get()
        """
        # prepare a mapping {code: format_layout} for all bank types
        bank_type_obj = self.pool.get('res.partner.bank.type')
        bank_types = bank_type_obj.browse(cr, uid, bank_type_obj.search(cr, uid, []), context=context)
        bank_code_format = dict((bt.code, bt.format_layout) for bt in bank_types)

        res = []
        for data in bank_dicts:
            name = data['acc_number']
            if data['state'] and bank_code_format.get(data['state']):
                try:
                    if not data.get('bank_name'):
                        data['bank_name'] = _('BANK')
                    data = dict((k, v or '') for (k, v) in data.iteritems())
                    name = bank_code_format[data['state']] % data
                    ##########################
                    if data['owner_name']:
                        name = name + ' ('+data['owner_name']+')'
                    ##########################
                    
                except Exception:
                    raise osv.except_osv(_("Formating Error"), _("Invalid Bank Account Type Name format."))
            
            res.append((data.get('id', False), name))
        return res

    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        bank_dicts = self.read(cr, uid, ids, self.fields_get_keys(cr, uid, context=context), context=context)
        return self._prepare_name_get(cr, uid, bank_dicts, context=context)
    
res_partner_bank()

