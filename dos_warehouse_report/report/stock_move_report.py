
from openerp import pooler
import time
from openerp import pooler
# import datetime, dateutil.parser

import time

from openerp.report import report_sxw
#from openerp.addons.account.report.common_report_header import common_report_header
from openerp.tools.translate import _
from openerp.osv import osv

from openerp.report import report_sxw
from openerp.tools.translate import _
from openerp.osv import osv
from openerp.addons.dos_amount2text_idr import amount_to_text_id
from openerp.addons.report_webkit import webkit_report
from openerp.addons.report_webkit.report_helper import WebKitHelper
from openerp.addons.report_webkit.webkit_report import webkit_report_extender
from openerp import SUPERUSER_ID



class DosWebkitParser5(report_sxw.rml_parse):
    print "kesini ngga y -----------------------------------------"
    def __init__(self, cr, uid, name, context):
        super(DosWebkitParser5, self).__init__(cr, uid, name, context=context)
        self.line_no = 0
        self.localcontext.update({
#             'time': time,
            #'get_data' : self._get_data,
            'get_stock_data':self._get_stock_data,
            'convert':self.convert,
        })
        
    def _get_data(self,data):
        
        #location_id  = data['form']['location'][0]
        picking_type  = data['form']['type'][0]
        print " ----------------->",picking_type.name
        date_start  = dateutil.parser.parse(data['form']['start_date'])
        date_stop   = dateutil.parser.parse(data['form']['end_date'])
        
        result_date_start   = date_start.strftime('%d-%b-%y')
        result_date_end     = date_stop.strftime('%d-%b-%y')
        
        result_date = {
                   # 'location'       : location_id or '',
                    'type'      : picking_type,
                    'result_date_start'   : result_date_start,
                    'result_date_end'     : result_date_end,
                  }
        return result_date
    
    def _get_stock_data(self,data):
        print "xxxxxxxxxx_get_stock_data",data
        #picking_type  = data['form']['type'][0]
        start = data['form']['start_date']
        end = data['form']['end_date']
        cr, uid= self.cr, self.uid
        db_pool = pooler.get_pool(self.cr.dbname)
        
        move_type = data['form']['move_type']
       
        res = []
        results = []
        if move_type == 'internal' :
            picking = db_pool.get('stock.picking.type').search(cr,uid,[('code','=','internal')])
        if move_type == 'supplier' :
            picking = db_pool.get('stock.picking.type').search(cr,uid,[('code','=','incoming')])
        if move_type == 'customer' :
            picking = db_pool.get('stock.picking.type').search(cr,uid,[('code','=','outgoing')])
        if move_type == 'all' :
            picking = db_pool.get('stock.picking.type').search(cr,uid,[('code','in',('incoming','outgoing'))])
          
        print "picking Type====================",picking
#         
        search = db_pool.get('stock.move').search(cr, uid, [('picking_type_id','in',picking),
                                                            ('date','>=',start),
                                                            ('date','<=',end),
                                                            ('state','=','done')
                                                             
                                                            ])
       
        results = db_pool.get('stock.move').browse(cr, uid, search)
        return results
        
    def convert(self, amount, cur):
        amt_id = amount_to_text_id.amount_to_text(amount, 'id', cur)
        return amt_id

#   
    
webkit_report.WebKitParser(
    'report.stock.report.pdf',
    'stock.report',
    'addons/dos_warehouse_report/report/stock_report.mako',
    parser=DosWebkitParser5)
    
    