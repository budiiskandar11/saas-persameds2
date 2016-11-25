from openerp.addons.report_webkit.webkit_report import webkit_report_extender
from openerp import SUPERUSER_ID


@webkit_report_extender("dos_sale.dos_new_quotation_report")
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
        #'get_taxes': get_taxes,
    })
# class order(report_sxw.rml_parse):
#     def __init__(self, cr, uid, name, context=None):
#         super(order, self).__init__(cr, uid, name, context=context)
#         self.localcontext.update({
# #             'get_object'        : self._get_object,
#             'time'              : time, 
# #             'show_discount'     : self._show_discount,
# #             'get_contact'       : self._get_contact,
#             'get_taxes'         : self._get_taxes,
#         })
#     
# #     def _get_contact(self,data):
# #         if data.is_company:
# #             if data.child_ids:
# #                 contact = data.child_ids[0].name
# #                 return contact
# #             else:
# #                 return False
# #         else:
# #             return False
# #         
# #     def _get_object(self,data):
# #         obj_data=self.pool.get(data['model']).browse(self.cr,self.uid,[data['id']])
# #         return obj_data
# #     
# #     def _show_discount(self, uid, context=None):
# #         cr = self.cr
# #         try: 
# #             group_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sale', 'group_discount_per_so_line')[1]
# #         except:
# #             return False
# #         return group_id in [x.id for x in self.pool.get('res.users').browse(cr, uid, uid, context=context).groups_id]
# #     
#     def _get_taxes(self,data):
#         taxes = ''
#         if len(data.tax_id)==1:
#             taxes+=data.tax_id[0].name
#         else:
#             taxes+="%s; %s" % (data.tax_id[0].name, data.tax_id[1].name)
#         return taxes
# 
# report_sxw.report_sxw('report.dos.new.quotation','sale.order','dos_sale/report/dos_print_quotation.mako',parser=order)
