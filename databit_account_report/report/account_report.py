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

from openerp.addons.databit_account_report import JasperDataParser
from openerp.addons.jasper_reports import jasper_report
from datetime import datetime

from openerp.osv import fields, osv


class jasper_account_report(JasperDataParser.JasperDataParser):
        
    def __init__(self, cr, uid, ids, data, context):
        super(jasper_account_report, self).__init__(cr, uid, ids, data, context)
        self.sheet_names=[]
        
    def generate_data_source(self, cr, uid, ids, data, context):
        return 'records'

    
    def generate_parameters(self, cr, uid, ids, data, context):
        if data['report_type']=='xls':
            return {'IS_IGNORE_PAGINATION':True}
        return {}

    def generate_properties(self, cr, uid, ids, data, context):
        return {
            'net.sf.jasperreports.export.xls.one.page.per.sheet':'true',
            'net.sf.jasperreports.export.xls.sheet.names.all': '/'.join(self.sheet_names),
            'net.sf.jasperreports.export.ignore.page.margins':'true',
            'net.sf.jasperreports.export.xls.remove.empty.space.between.rows':'true'
            }
        
    def generate_records(self, cr, uid, ids, data, context):
        result = []
        coa = data['form']['chart_account_id']
        coa = coa and self.pool.get('account.account').browse(cr, uid, coa, context=context).name or False
        
        fiscalyear = data['form']['fiscalyear_id']
        fiscalyear = fiscalyear and self.pool.get('account.fiscalyear').browse(cr, uid, fiscalyear, context=context).name or False
        filter = 'No Filters'
        if data['form']['filter'] == 'filter_no':
            filter = 'No Filters'
        if data['form']['filter'] == 'filter_date':
            filter = 'Date'
        if data['form']['filter'] == 'filter_period':
            filter = 'Periods'
            
        target_move = 'All Entries'
        if data['form']['target_move'] == 'posted':
            target_move = 'All Posted Entries'
        if data['form']['target_move'] == 'all':
            target_move = 'All Entries'
        
        lines = []
        account_obj = self.pool.get('account.account')
        currency_obj = self.pool.get('res.currency')
        ids2 = self.pool.get('account.financial.report')._get_children_by_order(self.cr, self.uid, [data['form']['account_report_id'][0]], context=data['form']['used_context'])
        for report in self.pool.get('account.financial.report').browse(self.cr, self.uid, ids2, context=data['form']['used_context']):
            vals = {
                'coa': coa,
                'fiscalyear': fiscalyear,
                'filter': filter,
                'target_move': target_move,
                'label_comp': data['form']['label_filter'],
                'name': report.name,
                'balance': report.balance * report.sign or 0.0,
                'type': 'report',
                'level': bool(report.style_overwrite) and report.style_overwrite or report.level,
                'account_type': report.type =='sum' and 'view' or False, #used to underline the financial report balances
            }
            if data['form']['debit_credit']:
                vals['debit'] = report.debit
                vals['credit'] = report.credit
            if data['form']['enable_filter']:
                vals['balance_cmp'] = self.pool.get('account.financial.report').browse(self.cr, self.uid, report.id, context=data['form']['comparison_context']).balance * report.sign or 0.0
            lines.append(vals)
            account_ids = []
            if report.display_detail == 'no_detail':
                #the rest of the loop is used to display the details of the financial report, so it's not needed here.
                continue
            if report.type == 'accounts' and report.account_ids:
                account_ids = account_obj._get_children_and_consol(self.cr, self.uid, [x.id for x in report.account_ids])
            elif report.type == 'account_type' and report.account_type_ids:
                account_ids = account_obj.search(self.cr, self.uid, [('user_type','in', [x.id for x in report.account_type_ids])])
            if account_ids:
                for account in account_obj.browse(self.cr, self.uid, account_ids, context=data['form']['used_context']):
                    #if there are accounts to display, we add them to the lines with a level equals to their level in
                    #the COA + 1 (to avoid having them with a too low level that would conflicts with the level of data
                    #financial reports for Assets, liabilities...)
                    if report.display_detail == 'detail_flat' and account.type == 'view':
                        continue
                    flag = False
                    vals = {
                        'coa': coa,
                        'fiscalyear': fiscalyear,
                        'filter': filter,
                        'target_move': target_move,
                        'label_comp': data['form']['label_filter'],
                        'name': account.code + ' ' + account.name,
                        'balance':  account.balance != 0 and account.balance * report.sign or account.balance or 0.0,
                        'type': 'account',
                        'level': report.display_detail == 'detail_with_hierarchy' and min(account.level + 1,6) or 6, #account.level + 1
                        'account_type': account.type,
                    }
                    if data['form']['debit_credit']:
                        vals['debit'] = account.debit
                        vals['credit'] = account.credit
                    if not currency_obj.is_zero(self.cr, self.uid, account.company_id.currency_id, vals['balance']):
                        flag = True
                    if data['form']['enable_filter']:
                        vals['balance_cmp'] = account_obj.browse(self.cr, self.uid, account.id, context=data['form']['comparison_context']).balance * report.sign or 0.0
                        if not currency_obj.is_zero(self.cr, self.uid, account.company_id.currency_id, vals['balance_cmp']):
                            flag = True
                    if flag:
                        lines.append(vals)
        self.sheet_names.append('Account Report')
        return lines
    

jasper_report.report_jasper('report.jasper_account_report', 'account.financial.report', parser=jasper_account_report)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: