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

import time
from datetime import tzinfo, timedelta, datetime
from dateutil.relativedelta import relativedelta
from openerp.report import report_sxw
from openerp.addons.account.report.common_report_header import common_report_header
from openerp.tools.translate import _
from openerp.osv import osv




class report_account_common_inh(report_sxw.rml_parse, common_report_header):

    def __init__(self, cr, uid, name, context=None):
        super(report_account_common_inh, self).__init__(cr, uid, name, context=context)
        self.localcontext.update( {
            'time': time,
            'get_fiscalyear': self._get_fiscalyear,
            'get_account': self._get_account,
            'get_start_period': self.get_start_period,
            'get_end_period': self.get_end_period,
            'get_filter': self._get_filter,
            'get_start_date':self._get_start_date,
            'get_end_date':self._get_end_date,
            'get_target_move': self._get_target_move,
            'get_title_string_pl':self.get_title_string_pl,
            'get_dates_string_pl':self.get_dates_string_pl,
            'get_main_year_pl':self.get_main_year_pl,
            'get_comp_year_pl':self.get_comp_year_pl,
            'get_lines_report': self.get_lines_report,
            'get_dates_string':self.get_dates_string,
            'get_title_string':self.get_title_string,
            'get_main_year_bs':self.get_main_year_bs,
            'get_comp_year_bs':self.get_comp_year_bs,
            'get_chart_account_name':self.chart_account_name_bs,
            'get_lines_report_balance_sheet': self.get_lines_report_balance_sheet,
        })
        self.context = context
    #For Profit and Loss Report    
    def get_lines_report(self, data):        
        return self.pool.get('account.account').get_lines_report(self.cr, self.uid, data)
        
    def get_main_year_pl(self, data):
        from_date = data['form']['date_from']        
        return 'Year '+ (datetime.strptime(from_date, '%Y-%m-%d')).strftime('%Y')        
        
    def get_comp_year_pl(self, data):
        from_date = data['form']['date_from']  
        from_date = (datetime.strptime(from_date, '%Y-%m-%d')).date() + relativedelta(years=-1)
        from_date = str(from_date)
        return 'Year '+ (datetime.strptime(from_date, '%Y-%m-%d')).strftime('%Y')
        
    def get_lines_report_balance_sheet(self, data):
        return self.pool.get('account.account').get_lines_balance_sheet(self.cr, self.uid, data)
        
    def get_title_string(self,data):
        return self.pool.get('account.account').title_bs
        
    def chart_account_name_bs(self):
        return self.pool.get('account.account').chart_account_name_bs
        
    def get_main_year_bs(self, data):
        from_date = data['form']['date_from']        
        return 'Year '+ (datetime.strptime(from_date, '%Y-%m-%d')).strftime('%Y')        
        
    def get_comp_year_bs(self, data):
        from_date = data['form']['date_from']  
        from_date = (datetime.strptime(from_date, '%Y-%m-%d')).date() + relativedelta(years=-1)
        from_date = str(from_date)
        return 'Year '+ (datetime.strptime(from_date, '%Y-%m-%d')).strftime('%Y')
        
    def get_title_string_pl(self,data):
        return self.pool.get('account.account').title_pl
        
    def get_dates_string_pl(self, data):
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
                 
                ret = str((datetime.strptime(start, '%Y-%m-%d')).strftime('%B %d, %Y')) + ' - ' + str((datetime.strptime(end, '%Y-%m-%d')).strftime('%B %d, %Y'))
                return ret
        return False
        
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
                 
                ret = 'As of ' + str((datetime.strptime(end, '%Y-%m-%d')).strftime('%B %d, %Y'))
                return ret
        return False
        

class report_financial(osv.AbstractModel):
    _name = 'report.account.report_financial'
    _inherit = 'report.abstract_report'
    _template = 'account.report_financial'
    _wrapped_report_class = report_account_common_inh
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
