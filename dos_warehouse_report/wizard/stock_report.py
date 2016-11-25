import time
from openerp import pooler
from openerp.osv import fields, osv

class stock_report(osv.osv_memory):
    _name = "stock.report"
    
    _columns = {
            'start_date'        : fields.date('Start Date'),
            'end_date'          : fields.date('End Date'),
            'location'          : fields.many2one('stock.location','Location'),
            'type'              : fields.many2one('stock.picking.type','Picking Type'),
            'move_type'       : fields.selection([('internal','Internal'),
                                                  ('customer','Delivery Order'),
                                                  ('supplier','Incoming Shipment'),
                                                  ('all','All')
                                                  ],'Move Type')
                }
    _defaults = {
           'move_type' : 'all',
           
                 }
    
    
    
    def print_stock_list(self,cr,uid,ids,context=None):
        print "print_advance_payment_list------------>>", ids
        res = {}
        if context is None:
            context = {}
        
        data = {}
        data['ids'] = context.get('active_ids', [])
        data['model'] = context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(cr, uid, ids, ['start_date',  'end_date','move_type'], context=context)[0]
        #data['form'].update(self.read(cr, uid, ids, ['date_from_cmp',  'debit_credit', 'date_to_cmp',  'fiscalyear_id_cmp', 'period_from_cmp', 'period_to_cmp',  'filter_cmp', 'account_report_id', 'enable_filter', 'label_filter','target_move'], context=context)[0])
        print 'FINISH*******'
        return { 
                'type': 'ir.actions.report.xml',
                'report_name': 'stock.report.pdf',
                'datas': data,
            }
    
stock_report()