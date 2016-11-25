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
# 
# import time
# from openerp.report import report_sxw
# from openerp.osv import fields, osv
# from openerp.report.render import render
# #from ad_num2word_id import num2word
# #import pooler
# from report_tools import pdf_fill,pdf_merge
# from openerp.tools.translate import _
from openerp.addons.report_webkit.webkit_report import webkit_report_extender
from openerp import SUPERUSER_ID

@webkit_report_extender("dos_accounting.faktur.pajak.form")
def extend_demo(pool, cr, uid, localcontext, context):
    admin = pool.get("res.users").browse(cr, uid, SUPERUSER_ID, context)
    
#     def get_taxes(pool, cr, uid, data, context):
#         taxes = ''
#         if len(data.tax_id)==1:
#             taxes+=data.tax_id[0].name
#         else:
#             taxes+="%s; %s" % (data.tax_id[0].name, data.tax_id[1].name)
#         return taxes
#     
    localcontext.update({
        "admin_name": admin.name,
        
    })    

# class faktur(report_sxw.rml_parse):
#     
#     def __init__(self, cr, uid, name, context):
#         print "ssssssssssssssssssssssssssssss"
#         super(faktur, self).__init__(cr, uid, name, context=context)        
#         #======================================================================= 
#         invoice = self.pool.get('account.invoice').browse(cr, uid, context['active_ids'])[0]
#         if invoice.state != 'open' and invoice.type != 'out_invoice':
#             raise osv.except_osv(_('You can not print Faktur Pajak Form !'), _('Faktur Pajak must be for Customer or State must be Open'))
#         #=======================================================================
#         self.line_no = 0
#         self.localcontext.update({
#             'time': time,
#             'alamat': self.alamat_npwp,
#             'convert':self.convert,
#             'nourut': self.no_urut,
#             'get_ppn': self.get_ppn,
#             'line_no':self._line_no,
#             'blank_line':self._blank_line,
#             'get_internal':self._get_internal,
#             'sum_tax':self._sum_tax,
#             'get_curr2':self.get_curr,
#             'get_invoice':self._get_invoice,
#             'get_curr':self._get_used_currency,
#             'get_rate_tax': self._get_rate_tax,
#             'get_rate_kpmen': self._get_rate_kpmen,
#         })
#     
#     def _get_rate_tax(self,data):
#         print '>>>>>>data>>>>>>>>',data,'<<<<dataid<<<',data['id']
#         val = {}
#         inv = self.pool.get('account.invoice').browse(self.cr,self.uid,data['id'])        
#         if inv.currency_tax_id.name == 'IDR':
#             print '>>>>>>>>>currency tax name>>>>>>>>',inv.currency_tax_id.name
#             n = 0
#             for cur_tax in inv.currency_tax_id.rate_tax_ids:
#                 print '>>>>>>> tgl nih <<<<<<<<',cur_tax.name
#                 if inv.date_invoice == cur_tax.name: 
#                     val[n] = cur_tax.rate
#                     print 'rate valas :',val[n]
#                     n+=1
#                 else:
#                     if inv.date_invoice > cur_tax.name:
#                         val[n] = cur_tax.rate
#                         print 'rate valas beda tgl:',val[n]
#                         n+=1
#         print '>>>>>>',val
#         return val
#     
#     def _get_rate_kpmen(self,data):
#         val = {}
#         inv = self.pool.get('account.invoice').browse(self.cr,self.uid,data['id'])        
#         if inv.currency_tax_id.name == 'IDR':
#             n = 0
#             for cur_tax in inv.currency_tax_id.rate_tax_ids:
#                 if inv.date_invoice == cur_tax.name: 
#                     val[n] = cur_tax.kp_men
#                     print 'rate valas :',val[n]
#                     n+=1
#                 else:
#                     if inv.date_invoice > cur_tax.name:
#                         val[n] = cur_tax.kp_men
#                         print 'rate valas beda tgl:',val[n]
#                         n+=1
#         return val
#   
#     def _get_used_currency(self,inv_id):
#         invdata=self.pool.get('account.invoice').browse(self.cr,self.uid,inv_id)
#         curr=self.pool.get('res.currency')
#         #print "invoice====================>",inv_id
#         if invdata.company_id.currency_id != invdata.currency_id:
#             query_rate="select rate from res_currency_rate where name=(select max(name) from res_currency_rate where currency_id="+str(invdata.currency_id.id)+" and name <= '"+str(invdata.date_invoice)+"' ) and currency_id="+str(invdata.currency_id.id)
#             #print "***",query_rate
#             self.cr.execute(query_rate)
#             rate=map(lambda x: x[0], self.cr.fetchall())
#             #print "======",curr.round(self.cr,self.uid,invdata.currency_id,1/rate[0])
#             return curr.round(self.cr,self.uid,invdata.currency_id,1/rate[0])
#         else:
#             #print "======1"
#             return 1
#     
#     def _get_curr(self,data):
#         #print "========>",data['id']
#         ai_data=self.pool.get('account.invoice').browse(self.cr,self.uid,data['id'])
#         print  ai_data.currency_id.name
#         return ai_data.currency_id.name
#     
#     def _sum_tax(self,tax_id):
#         taxtotal=0.00
#         taxtotal=sum([lt.amount or 0 for lt in tax_id])
#         return taxtotal
# 
#     def convert(self, amount_total, cur):
#         #amt_id = amount_to_text_id.amount_to_text(amount_total, 'id', cur)
#         amt_id = num2word.num2word_id(amount_total,"id").decode('utf-8')
#         return amt_id
#     
#     def no_urut(self, list, value):
#         return list.index(value) + 1
#     
#     def get_ppn(self, akun):
#         ppn = akun.amount_untaxed*0.1
#         return ppn
# 
#     def _blank_line(self, nlines, row, type):
#         #print nlines,row
#         res = ""
#         if type=="IDR":
#             if row > 15:
#                 for i in range(nlines+1):
#                     res = res + ('<tr class="inv_line"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>')
#             else:
#                 for i in range(nlines - row):
#                     res = res + ('<tr class="inv_line"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>')
#         else:
#             if row > 15:
#                 for i in range(nlines+1):
#                     res = res + ('<tr class="inv_line"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>')
#             else:
#                 for i in range(nlines - row):
#                     res = res + ('<tr class="inv_line"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>')
# 
#         return res
# 
#     def _line_no(self):
#         self.line_no = self.line_no + 1
#         return self.line_no
#     
#     def _get_internal(self,numb):
#         if numb:
#             faktur_number_uniq = '00000000'+numb[1:]
#             faktur_number_uniq = faktur_number_uniq[-8:]
#             return faktur_number_uniq
#         else:
#             return '.....'
#     
#     def alamat_npwp(self, partner_id, type):
#         address_id = self.pool.get('res.partner').search(self.cr, self.uid, [('partner_id','=',partner_id), ('type','=',type)])
#         if address_id:
#             address = self.pool.get('res.partner').browse(self.cr, self.uid, address_id)[0]
#             partner_address = ''
#             partner_address += address.street and address.street +', ' or ''
#             partner_address += address.street2 and address.street2 +', ' or ''
#             partner_address += address.city and address.city +', ' or ''
#             partner_address += address.zip and address.zip +', ' or ''
#             partner_address += address.country_id.name and address.country_id.name or ''
#             return  partner_address.upper()
#         else:
#             return False
#         
#     def _get_invoice(self,data):
#         #print "Data",data," - id ",data['id']
#         
# #        warning = {
# #            'title': _('Warning!'),
# #            'message': _('You selected an Unit of Measure which is not compatible with the product.')
# #        }
# #        return {'warning': warning}
#         inv_id=[data['id']]
#         inv_data=self.pool.get('account.invoice').browse(self.cr,self.uid,inv_id)
#         if inv_data:
#             return inv_data
#         else: 
#             return False
#         
#     def get_curr(self,data):
#         #print "========>",data['id']
#         ai_data=self.pool.get('account.invoice').browse(self.cr,self.uid,data['id'])
#         return ai_data.currency_id.name
#            
#report_sxw.report_sxw('report.faktur.pajak.valas.form', 'account.invoice', 'addons/dos_accounting/report/faktur_pajak_valas.mako', parser=faktur,header=False)
#report_sxw.report_sxw('report.faktur.pajak.form', 'account.invoice', 'addons/dos_accounting/report/faktur_pajak.mako', parser=faktur,header=False)      
#report_sxw.report_sxw('report.faktur.pajak', 'account.invoice', 'addons/ad_faktur_pajak/report/faktur_pajak_report.rml',parser=faktur, header=False)
#report_sxw.report_sxw('report.faktur.pajak.usd', 'account.invoice', 'addons/ad_faktur_pajak/report/faktur_pajak_report_usd.rml',parser=faktur, header=False)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


