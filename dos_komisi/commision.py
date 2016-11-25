from openerp.osv import fields, osv
import datetime
from openerp.tools.translate import _

class sale_commision(osv.osv):
    _name ="sale.commision"
    _description ="Sales Komisi"
    _columns = {
                'name' : fields.char('Number'),
                'date' : fields.date('Date Create'),
                'create_by' : fields.many2one('res.users','Create by'),
                'start_date' : fields.date('Start Date'),
                'end_date' : fields.date('End Date'),
                'sales_person' : fields.many2one('res.users','Sales Person'),
                 'lines_ids' : fields.one2many('commision.lines','commision_id','List Sales'),
                
                }


class commision_lines(osv.osv):
    _name ="commision.lines"
    _description = "Commision Lines"
    _columns = {
               'commision_id' : fields.many2one('sale.commision','ID'),
               'invoice_id' : fields.many2one('account.invoice','Invoice No'),
               'partner_id' : fields.many2one('res.partner','Customer'),
               'date'       : fields.date('Invoice Date'),
               'reference'  : fields.char('Sale No'),
               'total_amount': fields.float('Total Invoice'),
               'total_payment': fields.float('Total Payment'),
                }