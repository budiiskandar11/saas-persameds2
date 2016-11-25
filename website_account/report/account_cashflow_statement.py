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

from openerp.osv import osv
from openerp.report import report_sxw
from datetime import tzinfo, timedelta, datetime
from openerp.addons.account.report.common_report_header import common_report_header
from openerp.tools.translate import _


class account_cashflow_statement_inh(report_sxw.rml_parse, common_report_header):
    _name = 'report.account.account.cashflow.statement'
    def __init__(self, cr, uid, name, context=None):
        super(account_cashflow_statement_inh, self).__init__(cr, uid, name, context=context)
        self.sum_debit = 0.00
        self.sum_credit = 0.00
        self.date_lst = []
        self.date_lst_string = ''
        self.result_acc = []
        self.localcontext.update({
            'time': time,
            'get_title': self.get_title,
            'get_filter_str': self.get_filter_str,
            'get_lines_report_cashflow_statement': self.get_lines_report_cashflow_statement,
            'get_dates_string':self.get_dates_string,
        })
        self.context = context
     
    def get_title(self):
        return self.pool.get('account.account').title_cfs
    
    def get_filter_str(self):    
        return self.pool.get('account.account').filter_str_cfs
        
    def get_lines_report_cashflow_statement(self, data):
        datas = self.pool.get('account.account').get_lines_cashflow_statement(self.cr, self.uid, data)
        return datas

        
    def get_dates_string(self, data):
        if data['form'].has_key('filter_string') and data['form']['filter_string']:
            return data['form']['filter_string']
        else:
            if data['form']['filter'] == 'filter_period':
                start = self.get_start_period(data)
                end = self.get_end_period(data)
                return str(start) + ' - ' + str(end)
            elif data['form']['filter'] == 'filter_date':
                start = self._get_start_date(data)
                end = self._get_end_date(data)
                 
                ret = str((datetime.strptime(start, '%Y-%m-%d')).strftime('%d %B %Y')) + ' - ' + str((datetime.strptime(end, '%Y-%m-%d')).strftime('%d %B %Y'))
                return ret
        return False

    def _get_account(self, data):
        if data['model']=='account.account':
            return self.pool.get('account.account').browse(self.cr, self.uid, data['form']['id']).company_id.name
        return super(account_balance ,self)._get_account(data)

    


class report_cashflow_statement(osv.AbstractModel):
    _name = 'report.website_account.report_cashflow_statement'
    _inherit = 'report.abstract_report'
    _template = 'website_account.report_cashflow_statement'
    _wrapped_report_class = account_cashflow_statement_inh

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
