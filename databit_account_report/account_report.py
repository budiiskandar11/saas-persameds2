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

class account_common_report(osv.osv_memory):
    _inherit = "accounting.report"

    def print_report(self, cr, uid, ids, context=None):
        data = {}
        data['ids'] = context.get('active_ids', [])
        data['model'] = context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(cr, uid, ids[0], context=context)
        for field in ['fiscalyear_id', 'chart_account_id', 'period_from', 'period_to', 'fiscalyear_id_cmp', 'period_from_cmp', 'period_to_cmp']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        used_context = self.pool.get('account.common.report')._build_contexts(cr, uid, ids, data, context=context)
        data['form']['periods'] = used_context.get('periods', False) and used_context['periods'] or []
        data['form']['used_context'] = dict(used_context, lang=context.get('lang', 'en_US'))
        
        comparison_context = self.pool.get('accounting.report')._build_comparison_context(cr, uid, ids, data, context=context)
        data['form']['comparison_context'] = comparison_context
        data['report_type'] = 'xls'
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'jasper_account_report',
            'jasper_output': 'xls',
            'datas': data,
            'nodestroy' : True
        }
        
account_common_report()