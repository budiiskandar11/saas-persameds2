# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    Copyright (c) 2009 Zikzakmedia S.L. (http://zikzakmedia.com) All Rights Reserved.
#                       Jordi Esteve <jesteve@zikzakmedia.com>
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

import xlwt
from datetime import datetime
from openerp.report import report_sxw
from openerp.addons.report_xls.report_xls import report_xls
from openerp.addons.report_xls.utils import rowcol_to_cell
#from openerp.addons.account.report.account_financial_report \
#    import report_account_common
from openerp.addons.account_financial_report_webkit_xls.report.account_financial_report import report_account_common


from openerp.tools.translate import _
from openerp import pooler
import time

class balance_sheet_xls(report_xls):
    def generate_xls_report(self, _p, _xs, data, objects, wb):
        
        lines = _p.get_lines(data)
        
        #line = _p.get_line(data['fiscalyear_id']['date_start'], data['start_date'], data['end_date'])
        
        cr, uid = self.cr, self.uid
        db_pool = pooler.get_pool(self.cr.dbname)
        account_pool = db_pool.get('account.account')
#         company_currency_id = data['company_id']['currency_id']['id']
#         print "company_currency_id>>>>>>>>>>>>>>", company_currency_id
        print "data['id']---------->>", data
        print "data['id']---------->>", data['form']['id']
        
        ####
        account_pool = db_pool.get('accounting.report')
        for wizz in account_pool.browse(cr,uid,data['form']['id']):
            print "Company-------->>", wizz.company_id.name
        
        ####
        
        report_name = _(wizz.account_report_id.name)
        
        ws = wb.add_sheet(report_name[:31])
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1
        row_pos = 0
        
        ##########
        ws.col(0).width = len("ABCD")*100
        ws.col(1).width = len("ABCDEF")*1000
        ws.col(2).width = len("ABCDEF")*1500
        ws.col(3).width = len("ABCDEF")*1000
        ws.col(4).width = len("ABCDEF")*1000
        ws.col(5).width = len("ABCD")*1000
        ws.col(6).width = len("ABCD")*1000
        ws.col(7).width = len("ABCDEF")*1000
        ws.col(8).width = len("ABCD")*100
        ##########
        ##Style
        title          = xlwt.easyxf('font: height 200, name Arial, colour_index black, bold on; align: horiz left;')
        title_l         = xlwt.easyxf('font: height 200, name Arial, colour_index black, bold on; align: horiz left; borders: top thin, bottom thin')
        title_c         = xlwt.easyxf('font: height 200, name Arial, colour_index black, bold on; align: horiz centre; borders: top thin, bottom thin')
        header_tbl      = xlwt.easyxf('font: height 200, name Arial, colour_index black; align: horiz centre, vert centre; pattern: pattern solid, fore_color gray25;')
        number          = xlwt.easyxf(num_format_str='#,##0.00;(#,##0.00)')
        view_line       = xlwt.easyxf('font: height 200, name Arial, colour_index black, bold on; align: horiz left;')
        normal_line     = xlwt.easyxf('font: height 200, name Arial, colour_index black; align: horiz left;')
        
        view_line_number       = xlwt.easyxf('font: height 200, name Arial, colour_index black, bold on; align: horiz right;', num_format_str='#,##0.00;(#,##0.00)')
        normal_line_number     = xlwt.easyxf('font: height 200, name Arial, colour_index black; align: horiz right;', num_format_str='#,##0.00;(#,##0.00)')
        
        
        borderkiri      = xlwt.easyxf('borders: left thin')
        borderkanan     = xlwt.easyxf('borders: right thin')
        borderatas      = xlwt.easyxf('borders: top thin')
        borderbawah     = xlwt.easyxf('borders: bottom thin')
        ##########
        
        ws.write(1,1, wizz.account_report_id.name+" "+wizz.company_id.name, title)
        
        #####Filter by #####
        ws.write(3,1, "Chart of Accounts:", normal_line)
        ws.write(4,1, wizz.chart_account_id.name, normal_line)
        
        ws.write(3,2, "Fiscal Year:", normal_line)
        ws.write(4,2, wizz.fiscalyear_id.name, normal_line)
        
        ws.write(3,3, "Filter By:", normal_line)
        ws.write(4,3, wizz.filter, normal_line)
        
        ws.write(3,4, "Target Moves:", normal_line)
        ws.write(4,4, wizz.target_move, normal_line)
        ####################
        
        ws.write(8,1, "Code", title_l)
        ws.write(8,2, "Name", title_c)
        ws.write(8,3, "Balance", title_c)
        ###Comparison###
        if wizz.enable_filter:
            ws.write(8,4, wizz.label_filter, title_c)
        ################
        #print "Lines--------------->>", lines
        row = 9
        for line in lines:
            try:
                account_code = line['account_code']
                account_name = line['account_name']
            except:
                account_code = ''
                account_name = line['name']
            
            ###Style###
            if line['account_type'] == 'view':
                name    = view_line
                balance = view_line_number
            else:
                name    = normal_line
                balance = normal_line_number
            ###########
            
            if account_code == '':
                ws.write_merge(row,row,1,2, account_name, name)
                ws.write(row,3, line['balance'], balance)
            else:
                ws.write(row,1, account_code, name)
                ws.write(row,2, " "*line['level']+account_name, name)
                ws.write(row,3, line['balance'], balance)
                
            ###Comparison###
            if wizz.enable_filter:
                ws.write(row,4, line['balance_cmp'], balance)
            ################
            row+=1
        
        
        
        
        
        pass

balance_sheet_xls('report.balance.sheet.xls',
                   'accounting.report',
                   parser=report_account_common)
