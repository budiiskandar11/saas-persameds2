import time
from datetime import datetime
from openerp.osv import fields, osv
from openerp.tools.translate import _

class import_invoice_wiz(osv.osv_memory):
    _name = "import.invoice.wiz"
    
    
    
    _columns = {
            'invoice_wiz_ids': fields.many2many('account.invoice', 'sale_invoice_rel', 'wizard_id', 'sale_id', 'Duty Trip List'),
            'user_id': fields.many2one('res.users','Sales Person'),
            'date_start' : fields.date('Date Start'),
            'date_end' : fields.date('Date End'),
                }
    
    def default_get(self,cr, uid, fields, context={}):
         res = super(import_invoice_wiz,self).default_get(cr, uid, fields, context=context)
         if context is None:
            context = {}
         record_id = context and context.get('active_id', False) or False
         if not record_id:
            return res
         
         data = self.pool.get('sale.commision').browse(cr,uid, record_id,context=context)
         print "xxxxxxxxxxxx", data['sales_person'].name
         if 'sales_person' in fields :
             res.update({'user_id':data['sales_person'].id})
             print "xxxxxxxxxxxx", data['sales_person'].name
         return res
     
    _defaults = {
                 'user_id' : default_get,
                 
                 }
    
    
    
    def create_sale_items(self,cr,uid,ids,context={}):
        lines=[]
        for data in self.browse(cr,uid,ids,context):
            for inv in data.invoice_wiz_ids:
                vals={
                    'invoice_id':inv.id,
                    'partner_id':inv.partner_id.id,
                    'date': inv.date_invoice,
                    'reference' :inv.reference,
                    'total_amount' :inv.amount_total,
                    'total_residual' :inv.residual,
                }
                lines.append((0,0,vals))
            self.pool.get('sale.commision').write(cr,uid,context['active_id'],{'lines_ids':lines})
        return True