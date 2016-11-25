import time
from openerp.report import report_sxw
from report.render import render
from osv import osv
import pooler
from openerp.addons.dos_amount2text_idr import amount_to_text_id

class report_webkit_html(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_webkit_html, self).__init__(cr, uid, name, context=context)
        self.line_no = 0
        self.localcontext.update({
            'time': time,
            'convert':self.convert,
            'nourut': self.no_urut,
            'blank_line':self.blank_line,
            'total_amount':self.total_amount,
        })
    
    def convert(self, amount, cur):
        amt_id = amount_to_text_id.amount_to_text(amount, 'id', cur)
        return amt_id
    
    def total_amount(self, ext_lines):
        print 'ext_lines',ext_lines
        total = 0.0
        for ext in ext_lines:
            if ext.credit:
                total+=ext.credit
        return total#{'quantity':total}
    
    def no_urut(self, list, value):
        return list.index(value) + 1
    
    def blank_line(self, nlines):
        #row = len(nlines)
        row = nlines
        res = ""
        if row < 8:
            for i in range(8 - row):
                res = res + ('A<br/>')
                #res = res + ('<tr> <td>&nbsp;</td> <td>&nbsp;</td> <td>&nbsp;</td> <td colspan="2">&nbsp;</td></tr>')
        return res
        
report_sxw.report_sxw('report.webkit.extra.transaksi',
                       'ext.transaksi', 
                       'addons/dos_ext_transaksi/report/report_webkit_html.mako',
                       parser=report_webkit_html,header=False)
report_sxw.report_sxw('report.webkit.account.move',
                       'account.move', 
                       'addons/dos_ext_transaksi/report/account_move_html.mako',
                       parser=report_webkit_html,header=False)
#RML
report_sxw.report_sxw(
    'report.new.general.journal',
    'ext.transaksi',
    'addons/dos_ext_transaksi/report/report_new_general_journal.rml', header=False,
    parser=report_webkit_html
)

