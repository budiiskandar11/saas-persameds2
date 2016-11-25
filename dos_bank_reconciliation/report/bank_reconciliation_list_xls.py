# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2014 Noviat nv/sa (www.noviat.com). All rights reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import xlwt
import time
from datetime import datetime
from openerp.osv import orm
from openerp.report import report_sxw
from openerp.addons.report_xls.report_xls import report_xls
from openerp.addons.report_xls.utils import rowcol_to_cell, _render
from openerp.tools.translate import translate, _
from openerp import pooler
import logging
_logger = logging.getLogger(__name__)

_ir_translation_name = 'bank.reconciliation.list.xls'


class bank_reconciliation_xls_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(bank_reconciliation_xls_parser, self).__init__(cr, uid, name, context=context)
        recon_obj = self.pool.get('bank.reconciliation')
        
        self.localcontext.update({
            'get_data':self.get_data,
            'datetime': datetime,
            '_': self._,
            })
        self.context = context
    
    def get_data(self,):
        cr, uid = self.cr, self.uid
        db_pool = pooler.get_pool(self.cr.dbname)
        #budget_pool = db_pool.get('budget.item')
        #peri_pool = db_pool.get('account.period')
        
        recon = self.pool.get('bank.reconciliation').browse(self.cr, self.uid, self.ids)
        return recon
        
        
    def _(self, src):
        lang = self.context.get('lang', 'en_US')
        
        print "translate(self.cr, _ir_translation_name, 'report', lang, src) or src", translate(self.cr, _ir_translation_name, 'report', lang, src) or src
        return translate(self.cr, _ir_translation_name, 'report', lang, src) or src


class bank_reconciliation_xls(report_xls):

    def generate_xls_report(self, _p, _xs, data, objects, wb):
        data = _p.get_data()[0]
        report_name = _("Laporan Kas")
        
        ws = wb.add_sheet(report_name[:31])
        ws.show_grid = 0
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1
        
        # Length Coloum
        
        ws.col(1).width = len("ABC")*1280# Source No.
        ws.col(2).width = len("ABCDEF")*2048# Description
        ws.col(3).width = len("ABC")*1280# Increase
        ws.col(4).width = len("AB")*128
        ws.col(5).width = len("ABC")*1280# Decrease
        ws.col(6).width = len("AB")*128
        ws.col(7).width = len("ABC")*1280# Balance
        ###############
        
        row_pos = 0
        row = 0
        col = 0
        
        
        # Style
        
        title       = xlwt.easyxf('font: height 240, name Arial, colour_index black, bold on; align: vert centre, horiz centre;')
        header      = xlwt.easyxf('font: colour_index black, bold on; align: vert centre, horiz centre; borders: right thin, left thin, top thin, bottom thin')
        bold        = xlwt.easyxf('font: bold on;')
        normal      = xlwt.easyxf(num_format_str='#,##0.00;(#,##0.00)')
        total_label = xlwt.easyxf('font: colour_index black, bold on; align: vert centre;')
        total_inc   = xlwt.easyxf('font: colour_index black, bold on; borders: top thin; border: top thin', num_format_str='#,##0.00;(#,##0.00)')
        footer      = xlwt.easyxf('font: colour_index black, bold on; align: vert centre; border: top thin')
        
        tabel_ttd   = xlwt.easyxf('font: colour_index black; align: vert centre,horiz centre;')
        tabel_ttd_under_line = xlwt.easyxf('font: colour_index black, underline on; align: vert centre,horiz centre;')
        #######
        
        
        # Set Header Company
        
        ws.write_merge(row, row,0, 7, data.company_id.name, title)
        ws.write_merge(row+1, row+1,0, 7,"Laporan " + data.journal_id.name, title)
        ws.write_merge(row+2, row+2,0, 7,"From " + data.start_date + " To " + data.end_date, title)
        
        #ws.write(row, 2, data.company_id.name, title)
        #ws.write(row+1, 2, "Laporan " + data.journal_id.name, title)
        #ws.write(row+2, 2, "From " + data.start_date + " To " + data.end_date, title)
        
        # Set Header Coloum
        ws.write(row+4, 0, "Date", header)
        ws.write(row+4, 1, "Source No.", header)
        ws.write(row+4, 2, "Description", header)
        #ws.write(row+4, 3, "Increase", )
        ws.write_merge(row+4, row+4, 3, 4,"Increase", header)
        #ws.write(row+4, 5, "Decrease", header)
        ws.write_merge(row+4, row+4, 5, 6,"Decrease", header)
        ws.write(row+4, 7, "Balance", header)
        
        ####Last Balance####
        #ws.write_merge(row, row,0, 7, data.company_id.name, title)
        
        ws.write_merge(5, 5, 0, 5, "Last Balance", footer)
        ws.write(5, 7, data.beginning_balance, total_inc)
        ####################
        row = 6
        # Set Line
        cell_increase_start      = xlwt.Utils.rowcol_to_cell(row,3)
        cell_decrease_start      = xlwt.Utils.rowcol_to_cell(row,5)
        for line in data.mutation_reconciliation:
            #if line.bank_recon_id:
            ws.write(row, 0, line.date, normal)
            ws.write(row, 1, line.move_line_id.move_id.name, normal)
            ws.write(row, 2, line.name, normal)
            ws.write(row, 3, line.debit, normal)
            ws.write(row, 5, line.credit, normal)
            #ws.write(row, 7, line.balance, normal)
            ####
            cell_balance    = xlwt.Utils.rowcol_to_cell(row-1,7)
            cell_debit      = xlwt.Utils.rowcol_to_cell(row,3)
            cell_credit     = xlwt.Utils.rowcol_to_cell(row,5)
            formula_balance = "%s + %s - %s"%(cell_balance,cell_debit,cell_credit)
            ws.write(row, 7, xlwt.Formula(formula_balance), normal)
            ####
            row += 1
        cell_increase_end      = xlwt.Utils.rowcol_to_cell(row-1,3)
        cell_decrease_end      = xlwt.Utils.rowcol_to_cell(row-1,5)
        
        # Set Total
        
        formula_increase          = "SUM(%s:%s)"%(cell_increase_start,cell_increase_end)
        formula_decrease          = "SUM(%s:%s)"%(cell_decrease_start,cell_decrease_end)
        
        ws.write_merge(row, row, 0, 1,"Total of "+data.journal_id.name, total_label)
        ws.write(row,3,xlwt.Formula(formula_increase), total_inc)
        ws.write(row,5,xlwt.Formula(formula_decrease), total_inc)
        row += 1
        ws.write_merge(row, row,0, 7,"", footer)
       
        ######Kolom TTD#####
        row+=2
        ws.write_merge(row, row, 0,1,"Disetujui : ", tabel_ttd)
        ws.write(row,2,"Diketahui oleh:", tabel_ttd)
        ws.write_merge(row, row, 3,5,"Diperiksa oleh:", tabel_ttd)
        ws.write_merge(row, row, 6,7,"Dibuat oleh :", tabel_ttd)
        
        row+=1
        row2 = row+4
        ws.write_merge(row, row2, 0,1,"", tabel_ttd)
        ws.write_merge(row, row2, 2,2,"", tabel_ttd)
        ws.write_merge(row, row2, 3,5,"", tabel_ttd)
        ws.write_merge(row, row2, 6,7,"", tabel_ttd)
        
        
        row+=5
        print "22222222222222", row
        ws.write_merge(row, row, 0,1, "", tabel_ttd_under_line)
        ws.write(row,2,"", tabel_ttd_under_line)
        ws.write_merge(row, row, 3,5,data.check_by.name or '', tabel_ttd_under_line)
        ws.write_merge(row, row, 6,7,data.user_id.name or '', tabel_ttd_under_line)
        
        row+=1
        ws.write_merge(row, row, 0,1, "Direktur", tabel_ttd)
        ws.write(row,2,"FA Dept. Head", tabel_ttd)
        ws.write_merge(row, row, 3,5,"Treasury Sec Head", tabel_ttd)
        ws.write_merge(row, row, 6,7,"Cashier", tabel_ttd)
        ####################
        
bank_reconciliation_xls('report.bank.reconciliation.list.xls',
    'bank.reconciliation',
    parser=bank_reconciliation_xls_parser)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
