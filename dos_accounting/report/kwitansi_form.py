import time
from openerp.report import report_sxw
from openerp.osv import fields, osv
from openerp.report.render import render
#from ad_num2word_id import num2word
#import pooler
from report_tools import pdf_fill,pdf_merge
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
#from ad_amount2text_idr import amount_to_text_id
from openerp.tools import amount_to_text_en 


class kwitansi_form(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context):
        super(kwitansi_form, self).__init__(cr, uid, name, context=context)
        #if self.pool.get('sale.order').browse(cr, uid, context['active_ids'])[0].state <> 'approved':
        #    raise osv.except_osv(_('Can not Print PO Form !'), _('You can not Print PO Form If State not Approved'))
#        
       # self.line_no = 0
        self.localcontext.update({
            'get_object':self._get_object,
            'counter':self.counter,
#            'time': time,
#            'convert':self.convert,
#            'get_company_address': self._get_company_address,
#            #'angka':self.angka,
##            'alamat': self.alamat_npwp,
#            'convert':self.convert,
#            'charge':self.charge,
##            'nourut': self.no_urut,
##            'get_ppn': self.get_ppn,
#            'line_no':self._line_no,
#            'blank_line':self.blank_line,
#            'blank_line_rfq':self.blank_line_rfq,
#            'get_grand_total':self.get_grand_total,
#            'get_internal':self._get_internal,
#            'sum_tax':self._sum_tax,
#            'get_curr2':self.get_curr,
#            'get_invoice':self._get_invoice,
#            'get_curr':self._get_used_currency,
        }) 
        
    def _get_object(self,data):
        obj_data=self.pool.get(data['model']).browse(self.cr,self.uid,[data['id']])
#        seq=obj_data[0].print_seq
#        seq+=1
#        obj_data[0].write({'print_seq':seq})
        return obj_data
    
    def counter(self,data):
        pc=data.print_counter
        id=data.id
#         if data.print_counter :
#             query= "UPDATE downpayment SET print_counter = 'printed'"#(print_counter + 1) where id='"+str(id)+"'"
#         else:
#             query= "UPDATE downpayment SET print_counter = ''"#'1' where id='"+str(id)+"'"
        query= "UPDATE downpayment SET print_counter = 'printed' where id='"+str(id)+"'"
        self.cr.execute(query)

report_sxw.report_sxw('report.faktur_pajak.form', 'account.invoice', 'ad_kwitansi_form/report/faktur_pajak.mako', parser=kwitansi_form,header=False)