# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
from openerp.tools import amount_to_text_en
from openerp.addons.dos_amount2text_idr import amount_to_text_id

class konversi(osv.osv):
    _inherit   = "account.invoice"
    
    def _amount_in_words(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            val = 0.0 
            res[order.id] = {
                'amount_words_invoice': '0.0',
            }
            val = order.amount_total
            cur = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.currency_id
            test = cur_obj.round(cr, uid, cur, val)            
            res[order.id] = amount_to_text_id.amount_to_text(test,'id', currency=cur.name)
        return res
    
    _columns    = {
       'amount_string'  : fields.function(_amount_in_words, string='In Words', type="char", store=True, help="The amount in words"),
   }
    
konversi()