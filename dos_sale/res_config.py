# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
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
import datetime
from dateutil.relativedelta import relativedelta

import openerp
from openerp import SUPERUSER_ID
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools.translate import _
from openerp.osv import fields, osv

class sale_config_settings(osv.osv_memory):
    _inherit = 'sale.config.settings'

    _columns = {
        'sale_discount_limit': fields.float('Limit discount to require a manager approval', required=False,
             help="Discount after which validation of sale order line required."),
        'company_id' : fields.many2one('res.company',"Company"),
        
    }
    
    _default = {
                'company_id' : lambda s,cr,u,c: s.pool.get('res.users').browse(cr,u,u).company_id.id, 
                }



    def get_default_discount_limit(self, cr, uid, fields, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)   
        return {'sale_discount_limit': user.company_id and user.company_id.sale_discount_limit}

    def set_default_discount_limit(self, cr, uid, ids, context=None):
        company_obj = self.pool.get('res.company')
        config = self.browse(cr, uid, ids[0], context)
        return company_obj.write(cr, uid, [config.company_id.id], {'sale_discount_limit': config.sale_discount_limit})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
