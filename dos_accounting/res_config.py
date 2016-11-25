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

from openerp.osv import fields, osv
from openerp.tools.translate import _

class dos_config_settings(osv.osv_memory):
    _inherit = 'dos.config.settings'
    _columns = {
        'sale_account_additional_discount_id': fields.many2one('account.account', 'Account Additional Discount', required=False),
        'purchase_account_additional_discount_id': fields.many2one('account.account', 'Account Additional Discount', required=False),
    }

    def get_default_additional_discount(self, cr, uid, fields, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)   
        return {'sale_account_additional_discount_id': user.company_id and user.company_id.sale_account_additional_discount_id.id, 'purchase_account_additional_discount_id': user.company_id and user.company_id.purchase_account_additional_discount_id.id}

    def set_default_additional_discount(self, cr, uid, ids, context=None):
        company_obj = self.pool.get('res.company')
        config = self.browse(cr, uid, ids[0], context)
        return company_obj.write(cr, uid, [config.company_id.id], {'sale_account_additional_discount_id': config.sale_account_additional_discount_id.id, 'purchase_account_additional_discount_id': config.purchase_account_additional_discount_id.id})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
