# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2013 Noviat nv/sa (www.noviat.com). All rights reserved.
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

from openerp.osv import orm
import xlwt
from openerp.addons.website_account.report_xls import report_xls
from openerp.addons.website_account.utils import rowcol_to_cell
from openerp.tools.translate import _
# import logging
# _logger = logging.getLogger(__name__)

class cashflow_statement_xls(orm.TransientModel):
    _name = 'cashflow.statement.xls'

    def xls_export(self, cr, uid, data, context=None):
        #return self.check_report(cr, uid, ids, context=context)
        fiscalyear_id = self.pool.get('account.account').get_fiscal_year(cr, uid, data['form']['chart_account_id'])
        data['form']['fiscalyear_id'] = fiscalyear_id
        data['form']['used_context']['fiscalyear'] = fiscalyear_id
        ret = {'type': 'ir.actions.report.xml', 'datas': {'model': 'ir.ui.menu', 'ids': [], 'form': {'chart_account_id': data['form']['chart_account_id'], 'period_to': False, 'fiscalyear_id': data['form']['fiscalyear_id'], 'periods': [], 'date_from': data['form']['date_from'], 'used_context': {'lang': 'en_US', 'state': data['form']['target_move'], 'chart_account_id': data['form']['chart_account_id'], 'fiscalyear': data['form']['fiscalyear_id']}, 'period_from': False, 'date_to': data['form']['date_to'], 'filter': data['form']['filter'], 'target_move': data['form']['target_move']}, 'title':data['form']['title'], 'company': data['form']['company'], 'filter_str':data['form']['filter_str']}, 'report_name': 'account.account_report_cashflow_statement_xls'}
        
        return ret
        
class account_cashflow_statement_xls(report_xls):
    column_sizes = []

    def generate_xls_report(self, _p, _xs, data, objects, wb):
        formula_dict_debit = {}
        formula_dict_credit = {}
        formula_dict = {}
        self.column_sizes = []
        ws = wb.add_sheet('Cashflow Statement')
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1
        row_pos = 0
	records = self.pool.get('account.account').get_lines_cashflow_statement(self.cr, self.uid, data)
	max_level = self.pool.get('account.account').max_level_cfs + 1  # Index starts with 0 but levels starts with 1, -3 to avoid 3 empty Rows
        # set print header/footer
        ws.header_str = data['title']
        ws.footer_str = self.xls_footers['standard']
        # Title
        cell_style = xlwt.easyxf(_xs['xls_title'])
        
        cell_format = _xs['bold'] + _xs['borders_all']
        cell_style = xlwt.easyxf(cell_format)
        cell_style_center = xlwt.easyxf(cell_format + _xs['center'])
        c_specs = [
            ('company', max_level, 0, 'text', data['company'], None, cell_style_center),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)
        c_specs = [
            ('title', max_level, 0, 'text', data['title'], None, cell_style_center),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)
        c_specs = [
            ('filter_str', max_level, 0, 'text', data['filter_str'], None, cell_style_center),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)

        # write empty row to define column sizes
	
        self.column_sizes.extend([5] * (max_level-2))
        self.column_sizes.append(45)
        self.column_sizes.append(25)
        c_sizes = self.column_sizes
        c_specs = [('empty%s' % i, 1, c_sizes[i], 'text', None)
                   for i in range(0, len(c_sizes))]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, set_column_size=True,set_row_height=False)
	
        # Column Header Row
        cell_format = _xs['bold'] + _xs['fill_blue'] + \
            _xs['borders_all'] + _xs['wrap'] + _xs['top']
        cell_style = xlwt.easyxf(cell_format)
        cell_style_right = xlwt.easyxf(cell_format + _xs['right'])
        cell_style_center = xlwt.easyxf(cell_format + _xs['center'])
        c_specs = [
            ('account', max_level-1, 0, 'text', _('Account'), None, cell_style_center),
        ]        
        c_specs += [
                         ('balance', 1, 0, 'text',
                         _('Balance'), None, cell_style_right)]        
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)
        ws.set_horz_split_pos(row_pos)
	
        last_child_consol_ids = []

        # cell styles for account data
        view_cell_format = _xs['bold'] + _xs['borders_all']
        view_cell_style = xlwt.easyxf(view_cell_format)
        view_cell_style_center = xlwt.easyxf(view_cell_format + _xs['center'])
        view_cell_style_decimal = xlwt.easyxf(
            view_cell_format + _xs['right'],
            num_format_str=report_xls.decimal_format)
        view_cell_style.font.colour_index = xlwt.Style.colour_map['dark_blue_ega']           
        view_cell_style_center.font.colour_index = xlwt.Style.colour_map['dark_blue_ega']           
        view_cell_style_decimal.font.colour_index = xlwt.Style.colour_map['dark_blue_ega']           
        view_cell_style_pct = xlwt.easyxf(
            view_cell_format + _xs['center'], num_format_str='0')
        regular_cell_format = _xs['borders_all']
        regular_cell_style = xlwt.easyxf(regular_cell_format)
        regular_cell_style_center = xlwt.easyxf(
            regular_cell_format + _xs['center'])
        regular_cell_style_decimal = xlwt.easyxf(
            regular_cell_format + _xs['right'],
            num_format_str=report_xls.decimal_format)
        regular_cell_style_pct = xlwt.easyxf(
            regular_cell_format + _xs['center'], num_format_str='0')
        tall_style = xlwt.easyxf('font:height 720;' + view_cell_format)    	
	
        
        for current_account in records:

            if current_account['has_childs'] or current_account.has_key('bold'):
                cell_style = view_cell_style
                cell_style_center = view_cell_style_center
                cell_style_decimal = view_cell_style_decimal
                cell_style_pct = view_cell_style_pct
            else:
                cell_style = regular_cell_style
                cell_style_center = regular_cell_style_center
                cell_style_decimal = regular_cell_style_decimal
                cell_style_pct = regular_cell_style_pct		
	    
	    balance = current_account['balance']
	    
	    """-3 to avoid 3 empty Rows"""
            c_specs = [
                ('account', 1, 0, 'text', current_account['name']!='Cash Flow' and current_account['name'], None, None, None, current_account['level']-1, max_level-1),
            ]              
            if current_account['has_childs']:
                c_specs +=[
                ('balance', 1, 0, 'text', None, None, None),
                ]
            else:
                if not current_account.has_key('bold'): # or current_account['name'][:5] == 'Total' """ Give this condition also if any issue in Formulas or to avoid Formulas"""
                    if current_account.has_key('hide_bal'):
                        balance = None
                        c_specs +=[
                            ('balance', 1, 0, 'text', None, None, None),
                        ]
                    else:
                        c_specs +=[
                            ('balance', 1, 0, 'number', balance, None, cell_style_decimal,None, None, None, None),
                        ]
                elif current_account.has_key('bold'):
                    current = None
                    if isinstance(current_account['id'], float) and formula_dict.has_key(current_account['id']-0.5):
                        formula_dict[current_account['id']-0.5] += ',5)'
                        current = formula_dict[current_account['id']-0.5]
                    elif isinstance(current_account['id'], (long,int)) and formula_dict.has_key(current_account['id']):
                        formula_dict[current_account['id']] += ',5)'    
                        current = formula_dict[current_account['id']]
                    c_specs +=[
                        ('balance', 1, 0, 'number', None, current, cell_style_decimal,None, None, None, True),
                    ]    
                    
                    
             
            t_cell = rowcol_to_cell(row_pos, max_level-1)            
                
            if formula_dict.has_key(current_account['parent_id']):
                formula_dict[current_account['parent_id']] += ' + ' + t_cell
            else:
                formula_dict[current_account['parent_id']] = 'Round(' + t_cell
            row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
            if row_data[1][2][8]==True:
                row_pos = self.xls_write_row(
                ws, row_pos, row_data, row_style=cell_style, set_row_height=True)
            else:    
                row_pos = self.xls_write_row(
                ws, row_pos, row_data, row_style=cell_style)
                
account_cashflow_statement_xls('report.account.account_report_cashflow_statement_xls',
                  'account.account')




