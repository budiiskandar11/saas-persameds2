import time
from report import report_sxw
from report.render import render
from osv import osv
import pooler
from ad_amount2text_idr import amount_to_text_id

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
        total = 0.0
        for ext in ext_lines:
            if ext.credit:
                total+=ext.credit
        return total#{'quantity':total}
    
    def no_urut(self, list, value):
        return list.index(value) + 1
    
    def blank_line(self, nlines):
        #print "xxx",nlines
        row = len(nlines)
        #print "qqq",row
        res = ""
        if row < 8:
            for i in range(8 - row):
                res = res + ('A<br/>')
                #res = res + ('<tr> <td>&nbsp;</td> <td colspan="2">&nbsp;</td> <td colspan="2">&nbsp;</td> </tr>')
        print res
        return res
        
report_sxw.report_sxw('report.webkit.cash.advance',
                       'cash.advance', 
                       'addons/ad_cash_settlement/report/cash_advance.mako',
                       parser=report_webkit_html)
