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
import time
from datetime import tzinfo, timedelta, datetime
from dateutil.relativedelta import relativedelta
from openerp.report import report_sxw
from openerp.addons.account.report.common_report_header import common_report_header
from openerp.tools.translate import _
from openerp.osv import osv
# import logging
# _logger = logging.getLogger(__name__)


class profit_loss_xls(orm.TransientModel):
    _name = 'profit.loss.xls'

    def xls_export(self, cr, uid, data, context=None):
        #return self.check_report(cr, uid, ids, context=context)
        fiscalyear_id = self.pool.get('account.account').get_fiscal_year(cr, uid, data['form']['chart_account_id'])
        data['form']['fiscalyear_id'] = fiscalyear_id
        data['form']['used_context']['fiscalyear'] = fiscalyear_id
        if data['form']['report_type'] == 'standard':
            ret = {'type': 'ir.actions.report.xml', 'datas': {'model': 'ir.ui.menu', 'ids': [], 'form': {'chart_account_id': data['form']['chart_account_id'], 'period_to': False, 'fiscalyear_id': data['form']['fiscalyear_id'], 'periods': [], 'date_from': data['form']['date_from'], 'used_context': {'lang': 'en_US', 'state': data['form']['target_move'], 'chart_account_id': data['form']['chart_account_id'], 'fiscalyear': data['form']['fiscalyear_id']}, 'period_from': False, 'date_to': data['form']['date_to'], 'filter': data['form']['filter'], 'target_move': data['form']['target_move'], 'account_report_id':data['form']['account_report_id'], 'debit_credit':data['form']['debit_credit'], 'enable_filter':data['form']['enable_filter'], 'target_move': data['form']['target_move'], 'report_type':data['form']['report_type']}, 'title':data['form']['title'], 'company': data['form']['company'], 'filter_str':data['form']['filter_str']}, 'report_name': 'account.account_report_profit_loss_xls'}
        elif data['form']['report_type'] == 'prevyear':    
            ret = {'type': 'ir.actions.report.xml', 'datas': {'model': 'ir.ui.menu', 'ids': [], 'form': {'chart_account_id': data['form']['chart_account_id'], 'period_to': False, 'fiscalyear_id': data['form']['fiscalyear_id'], 'periods': [], 'date_from': data['form']['date_from'], 'used_context': {'lang': 'en_US', 'state': data['form']['target_move'], 'chart_account_id': data['form']['chart_account_id'], 'fiscalyear': data['form']['fiscalyear_id']}, 'comparison_context': {'fiscalyear': data['form']['comparison_context']['fiscalyear'], 'journal_ids':data['form']['comparison_context']['journal_ids'],'date_from': data['form']['comparison_context']['date_from'], 'date_to': data['form']['comparison_context']['date_to'], 'state': data['form']['comparison_context']['state'], 'chart_account_id':data['form']['comparison_context']['chart_account_id']}, 'period_from': False, 'date_to': data['form']['date_to'], 'filter': data['form']['filter'], 'target_move': data['form']['target_move'], 'account_report_id':data['form']['account_report_id'], 'debit_credit':data['form']['debit_credit'], 'enable_filter':data['form']['enable_filter'], 'target_move': data['form']['target_move'], 'fiscalyear_id_cmp':data['form']['fiscalyear_id_cmp'],'filter_cmp':data['form']['filter_cmp'], 'date_from_cmp':data['form']['date_from_cmp'], 'date_to_cmp':data['form']['date_to_cmp'], 'report_type':data['form']['report_type']}, 'title':data['form']['title'], 'company': data['form']['company'], 'filter_str':data['form']['filter_str']}, 'report_name': 'account.account_report_profit_loss_xls'}
        return ret
        
class account_profit_loss_xls(report_xls):
    column_sizes = []
    
    def generate_xls_report(self, _p, _xs, data, objects, wb):
        if data['form']['report_type'] == 'standard':
            self.generate_xls_report_stn(_p, _xs, data, objects, wb)
        elif data['form']['report_type'] == 'prevyear':  
	    self.generate_xls_report_prev(_p, _xs, data, objects, wb)
	    
	    
    def generate_xls_report_stn(self, _p, _xs, data, objects, wb):
        #print 'vvvvvvvvvvvvvvvvvvvvv', data
        formula_dict = {}
        ws = wb.add_sheet('Income Statement')
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1
        row_pos = 0
        self.column_sizes = []
	records = self.pool.get('account.account').get_lines_report(self.cr, self.uid, data)
	max_level = self.pool.get('account.account').max_level + 1 -2 # For Index 0 (+1), -2 To avoid 2 empty rows
        # set print header/footer
        ws.header_str = data['title']
        ws.footer_str = self.xls_footers['standard']

        # Title
        cell_style = xlwt.easyxf(_xs['xls_title'])
        
        cell_format = _xs['bold'] + _xs['borders_all']
        cell_style = xlwt.easyxf(cell_format)
        cell_style_center = xlwt.easyxf(cell_format + _xs['center'])
        c_specs = [
            ('company', max_level+1, 0, 'text', data['company'], None, cell_style_center),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)
        c_specs = [
            ('title', max_level+1, 0, 'text', data['title'], None, cell_style_center),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)
        c_specs = [
            ('filter_str', max_level+1, 0, 'text', data['filter_str'], None, cell_style_center),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)

        # write empty row to define column sizes
	
        self.column_sizes.extend([5] * (max_level-1))
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
            ('account', max_level, 0, 'text', _('Account'), None, cell_style_center),
        ]        
        c_specs += [('balance', 1, 0, 'text',
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
            
        style_percent = xlwt.easyxf(num_format_str='0.00%')    
        view_cell_style.font.colour_index = xlwt.Style.colour_map['dark_blue_ega']           
        view_cell_style_center.font.colour_index = xlwt.Style.colour_map['dark_blue_ega']           
        view_cell_style_decimal.font.colour_index = xlwt.Style.colour_map['dark_blue_ega']           
        style_percent.font.colour_index = xlwt.Style.colour_map['dark_blue_ega']                   
	
        
        for current_account in records:
            
            if current_account['type']=='report' or current_account['level']==0:
                continue

            if current_account['level'] <= 3 or current_account['name'][:5] == 'Total' or current_account['has_childs']:
                cell_style = view_cell_style
                cell_style_center = view_cell_style_center
                cell_style_decimal = view_cell_style_decimal
                cell_style_pct = view_cell_style_pct
            else:
                cell_style = regular_cell_style
                cell_style_center = regular_cell_style_center
                cell_style_decimal = regular_cell_style_decimal
                cell_style_pct = regular_cell_style_pct
		
	    balance = current_account['name']=='Net Income' and current_account['balance'] or current_account['balance'] # or abs(current_account['balance'])   """ To bring the Formulas in Excel we avoided the abs vals
	    """ -2 To avoid 2 empty rows"""
            c_specs = [
                ('account', 1, 0, 'text', current_account['name'], None, None, None, (current_account['level']>0 and current_account['level'] -2  or 0), max_level),                
            ]              
            if current_account['has_childs']:
                c_specs +=[
                ('balance', 1, 0, 'text', None, None, None),
                ]
            else:
                if current_account['name'][:5] != 'Total': # or current_account['name'][:5] == 'Total' """ Give this condition also if any issue in Formulas or to avoid Formulas"""
                    c_specs +=[
                        ('balance', 1, 0, 'number', balance, None, cell_style_decimal),
                    ]
                elif current_account['name'][:5] == 'Total':
                    formula_dict[current_account['id']-0.5] += ',5)'
                    c_specs +=[
                        ('balance', 1, 0, 'number', None, formula_dict[current_account['id']-0.5], cell_style_decimal),
                    ]
            t_cell = rowcol_to_cell(row_pos, max_level)
            if formula_dict.has_key(current_account['parent_id']):
                formula_dict[current_account['parent_id']] += (current_account['user_type'] and (current_account['user_type'].lower().strip()=='expenseSS' and ' - ' or ' + ') or ' + ') + t_cell
            else:
                formula_dict[current_account['parent_id']] = 'ROUND('+(current_account['user_type'] and (current_account['user_type'].lower().strip()=='expenseSS' and ' - ' or '') or '') + t_cell
                    
                    
            row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
            if row_data[0][2][4][:5]=='Total':
                row_pos = self.xls_write_row(
                ws, row_pos, row_data, row_style=cell_style, set_row_height=True)
            else:    
                row_pos = self.xls_write_row(
                ws, row_pos, row_data, row_style=cell_style)

    def generate_xls_report_prev(self, _p, _xs, data, objects, wb):
        #print 'bbbbbbbbbbbbbbbbbbbbbbbbbbbb', data
        formula_dict = {}
        formula_dict_prev = {}
        ws = wb.add_sheet('Income Statement')
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1
        row_pos = 0
        self.column_sizes = []
	records = self.pool.get('account.account').get_lines_report(self.cr, self.uid, data)
	max_level = self.pool.get('account.account').max_level + 4 -2 # For Index 0 (+1), -2 To avoid 2 empty rows
        # set print header/footer
        ws.header_str = data['title']
        ws.footer_str = self.xls_footers['standard']
	#print 'hhhhhhhhhhhhhhhhhhhhhhhhh', max_level
        # Title
        cell_style = xlwt.easyxf(_xs['xls_title'])
        
        cell_format = _xs['bold'] + _xs['borders_all']
        cell_style = xlwt.easyxf(cell_format)
        cell_style_center = xlwt.easyxf(cell_format + _xs['center'])
        c_specs = [
            ('company', max_level+1, 0, 'text', data['company'], None, cell_style_center),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)
        c_specs = [
            ('title', max_level+1, 0, 'text', data['title'], None, cell_style_center),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)
        c_specs = [
            ('filter_str', max_level+1, 0, 'text', data['filter_str'], None, cell_style_center),
        ]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, row_style=cell_style)

        # write empty row to define column sizes
	
        self.column_sizes.extend([5] * (max_level-4))
        self.column_sizes.append(45)
        self.column_sizes.append(25)
        self.column_sizes.append(25)
        self.column_sizes.append(25)
        self.column_sizes.append(25)
        c_sizes = self.column_sizes
        c_specs = [('empty%s' % i, 1, c_sizes[i], 'text', None)
                   for i in range(0, len(c_sizes))]
        row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
        row_pos = self.xls_write_row(
            ws, row_pos, row_data, set_column_size=True,set_row_height=False)
	        
        from_date = data['form']['date_from']        
        curr_lbl = 'Year '+ (datetime.strptime(from_date, '%m-%d-%Y')).strftime('%Y')        
        
        from_date = data['form']['date_from_cmp']
        comp_lbl = 'Year '+ (datetime.strptime(from_date, '%Y-%m-%d')).strftime('%Y')

        # Column Header Row
        cell_format = _xs['bold'] + _xs['fill_blue'] + \
            _xs['borders_all'] + _xs['wrap'] + _xs['top']
        cell_style = xlwt.easyxf(cell_format)
        cell_style_right = xlwt.easyxf(cell_format + _xs['right'])
        cell_style_center = xlwt.easyxf(cell_format + _xs['center'])
        c_specs = [
            ('account', max_level-3, 0, 'text', _('Account'), None, cell_style_center),
        ]        
        c_specs += [('balance', 1, 0, 'text',
                         _(curr_lbl), None, cell_style_right),
                    ('balance_cmp', 1, 0, 'text',
                         _(comp_lbl), None, cell_style_right),
                    ('cur_change', 1, 0, 'text',
                         _('$ Change'), None, cell_style_right),
                    ('per_change', 1, 0, 'text',
                         _('% Change'), None, cell_style_right)]        
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
	style_percent_bold = xlwt.easyxf(_xs['bold'], num_format_str='0.00%')  
	style_percent = xlwt.easyxf(num_format_str='0.00%')  
        view_cell_style.font.colour_index = xlwt.Style.colour_map['dark_blue_ega']           
        view_cell_style_center.font.colour_index = xlwt.Style.colour_map['dark_blue_ega']           
        view_cell_style_decimal.font.colour_index = xlwt.Style.colour_map['dark_blue_ega']           
        style_percent.font.colour_index = xlwt.Style.colour_map['dark_blue_ega']                   
        for current_account in records:
            
            if current_account['type']=='report' or current_account['level']==0:
                continue

            if current_account['level'] <= 3 or current_account['name'][:5] == 'Total' or current_account['has_childs']:
                cell_style = view_cell_style
                cell_style_center = view_cell_style_center
                cell_style_decimal = view_cell_style_decimal
                cell_style_pct = view_cell_style_pct
                cell_style_percent = style_percent_bold
            else:
                cell_style = regular_cell_style
                cell_style_center = regular_cell_style_center
                cell_style_decimal = regular_cell_style_decimal
                cell_style_pct = regular_cell_style_pct
                cell_style_percent = style_percent
		
	    balance = current_account['name']=='Net Income' and current_account['balance'] or current_account['balance'] # or abs(current_account['balance'])   """ To bring the Formulas in Excel we avoided the abs vals
	    balance_cmp = current_account['balance_cmp']
	    cur_change = current_account['cur_change']
	    per_change = current_account['per_change']
	    
	    """ -2 To avoid 2 empty rows"""
            c_specs = [
                ('account', 1, 0, 'text', current_account['name'], None, None, None, (current_account['level']>0 and current_account['level'] -2  or 0), max_level-3),                
            ]              
            t_cell = rowcol_to_cell(row_pos, max_level-3)
            t_cell_prev = rowcol_to_cell(row_pos, max_level-2)
            if current_account['has_childs']:
                c_specs +=[
                ('balance', 1, 0, 'text', None, None, None),
                ('balance_cmp', 1, 0, 'text', None, None, None),
                ('cur_change', 1, 0, 'text', None, None, None),
                ('per_change', 1, 0, 'text', None, None, None),
                ]
            else:
                if current_account['name'][:5] != 'Total': # or current_account['name'][:5] == 'Total' """ Give this condition also if any issue in Formulas or to avoid Formulas"""
                    c_specs +=[
                        ('balance', 1, 0, 'number', balance, None, cell_style_decimal),
                        ('balance_cmp', 1, 0, 'number', balance_cmp, None, cell_style_decimal),
                        ('cur_change', 1, 0, 'number', None, 'ROUND(('+t_cell +'-'+ t_cell_prev+'),5)', cell_style_decimal),
                        ('per_change', 1, 0, 'text', None, 'ROUND(IF('+t_cell +'=0, IF('+t_cell_prev +'=0, 0, SIGN(-'+t_cell_prev +')), IF('+t_cell_prev +'=0, SIGN('+t_cell +'), ('+t_cell +'-'+t_cell_prev +')/ABS('+t_cell_prev +'))),5)', cell_style_percent),
                    ]
                elif current_account['name'][:5] == 'Total':
                    formula_dict[current_account['id']-0.5] += ',5)'
                    formula_dict_prev[current_account['id']-0.5] += ',5)'
                    c_specs +=[
                        ('balance', 1, 0, 'number', None, formula_dict[current_account['id']-0.5], cell_style_decimal),
                        ('balance_cmp', 1, 0, 'number', None, formula_dict_prev[current_account['id']-0.5], cell_style_decimal),
                        ('cur_change', 1, 0, 'number', None, 'ROUND(('+t_cell +'-'+ t_cell_prev+'),5)', cell_style_decimal),
                        ('per_change', 1, 0, 'text', None, 'ROUND(IF('+t_cell +'=0, IF('+t_cell_prev +'=0, 0, SIGN(-'+t_cell_prev +')), IF('+t_cell_prev +'=0, SIGN('+t_cell +'), ('+t_cell +'-'+t_cell_prev +')/ABS('+t_cell_prev +'))),5)', cell_style_percent),
                    ]
            
            
            if formula_dict.has_key(current_account['parent_id']):
                formula_dict[current_account['parent_id']] += (current_account['user_type'] and (current_account['user_type'].lower().strip()=='expenseSS' and ' - ' or ' + ') or ' + ') + t_cell
            else:
                formula_dict[current_account['parent_id']] = 'ROUND('+(current_account['user_type'] and (current_account['user_type'].lower().strip()=='expenseSS' and ' - ' or '') or '') + t_cell
                
            if formula_dict_prev.has_key(current_account['parent_id']):
                formula_dict_prev[current_account['parent_id']] += (current_account['user_type'] and (current_account['user_type'].lower().strip()=='expenseSS' and ' - ' or ' + ') or ' + ') + t_cell_prev
            else:
                formula_dict_prev[current_account['parent_id']] = 'ROUND('+(current_account['user_type'] and (current_account['user_type'].lower().strip()=='expenseSS' and ' - ' or '') or '') + t_cell_prev    
                    
                    
            row_data = self.xls_row_template(c_specs, [x[0] for x in c_specs])
            if row_data[0][2][4][:5]=='Total':
                row_pos = self.xls_write_row(
                ws, row_pos, row_data, row_style=cell_style, set_row_height=True)
            else:    
                row_pos = self.xls_write_row(
                ws, row_pos, row_data, row_style=cell_style)

account_profit_loss_xls('report.account.account_report_profit_loss_xls',
                  'account.account')
