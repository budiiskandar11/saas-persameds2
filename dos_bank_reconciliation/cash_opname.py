import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time

import openerp
from openerp import SUPERUSER_ID
from openerp import pooler, tools
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round

import openerp.addons.decimal_precision as dp


class bank_reconciliation_cash(osv.osv):
    _inherit = 'bank.reconciliation'
    
    def _refresh_record2(self, cr, uid, context=None):
        res = []
        curr = [50, 100, 200, 500, 1000,]
        curr2 = [1000, 2000, 5000, 10000, 20000, 50000, 100000]
        for rs in curr:
            dct = {
                'name': rs,
                'qty': 0.0,
                'type':'logam',
            }
            res.append(dct)  
        for rs2 in curr2 :
            dct2 = {
                 'name': rs2,
                 'qty': 0.0,
                 'type':'kertas',
             }
            res.append(dct2)
        return res
    
    
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        non_cash = 0.0
        bal = 0.0
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'total_uang_kertas': 0.0,
                'total_kertas_rusak': 0.0,
                'total_logam': 0.0,
                'total_cash' : 0.0,
                'total_non_cash' : 0.0,
                'grand_total' : 0.0,
            }
            
            non_cash = order.eviden + order.bulat + order.bon_sementara
            bal = order.ending_balance
            
            val1 = val2 = val3 = 0.0
            for line in order.cash_ids:
                if line.type == 'logam' :
                    val1 += line.sub_total_bagus
                if line.type == 'kertas' :
                    val2 += line.sub_total_bagus
                    val3 += line.sub_total_rusak
                
            cur = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.currency_id
            res[order.id]['total_uang_kertas'] = cur_obj.round(cr, uid, cur, val2)
            res[order.id]['total_kertas_rusak'] = cur_obj.round(cr, uid, cur, val3)
            res[order.id]['total_logam'] = cur_obj.round(cr, uid, cur, val1)
            res[order.id]['total_cash'] = res[order.id]['total_uang_kertas']+res[order.id]['total_kertas_rusak']+res[order.id]['total_logam']
            res[order.id]['total_non_cash'] = cur_obj.round(cr, uid, cur, non_cash)
            res[order.id]['grand_total'] = res[order.id]['total_non_cash']+res[order.id]['total_cash']
            res[order.id]['selisih'] = res[order.id]['grand_total']-cur_obj.round(cr, uid, cur, bal)
        return res
    
    
    _columns = {
                'cash_ids' : fields.one2many('cash.tunai.opname','bank_recon_id','Cash Opname'),
                'total_uang_kertas' : fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total Uang Kertas',multi='sums', help="The total amount."),
                'total_kertas_rusak': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total Uang Kertas Rusak',multi='sums', help="The total amount."),
                'total_logam'       : fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total Uang Logam',multi='sums', help="The total amount."),
                'total_cash'        : fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total Cash',multi='sums', help="The total amount."),
                'date_opname'       : fields.date('Checking Date'),
                'check_by'          : fields.many2one('hr.employee',"Check By"),
                'total_non_cash'    : fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total Non Cash',multi='sums', help="The total amount."),
                'eviden'            : fields.float('Eviden Dalam Proses'),
                'bulat'             : fields.float('Selisih Pembulatan'),
                'bon_sementara'     : fields.float('Bon Sementara'),
                'selisih'           : fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Selisih',multi='sums', help="The total amount."),
                'grand_total'       : fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Grand Total',multi='sums', help="The total amount."),
                'user_id'           : fields.many2one('res.users','Create By'),
                }
    
    
    _defaults = {
                'cash_ids' : _refresh_record2,
                'eviden'            : 0.0,
                'bulat'             : 0.0,
                'bon_sementara'     : 0.0,
                'user_id': lambda s, cr, uid, c: uid,
                }
   

bank_reconciliation_cash()

class cash_tunai_opname(osv.osv):
    _name   = "cash.tunai.opname"
    _description = "Cash Opname"
    
    def _amount_line1(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        
        for line in self.browse(cr, uid, ids, context=context):
            
            res[line.id] = line.name * line.qty_bagus
        return res
    
    def _amount_line2(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        
        for line in self.browse(cr, uid, ids, context=context):
            
            res[line.id] = line.name * line.qty_rusak
        return res

    
    
    
    _columns = {
                'name'          : fields.float('Pecahan',),
                'bank_recon_id': fields.many2one('bank.reconciliation','Bank Reconciliation'),
                'type'          : fields.selection([('logam',"Uang Logam"),
                                            ('kertas',"Uang Kertas"),
                                            ],"Tipe Uang", required=True,
                                           ),
                'qty_bagus'           : fields.float('Qty'),
                'sub_total_bagus': fields.function(_amount_line1, string='Sub Total', type='float', digits_compute=dp.get_precision('Account')),
                'qty_rusak'             : fields.float('Qty Rusak',),
                'sub_total_rusak': fields.function(_amount_line2, string='Sub Total', type='float', digits_compute=dp.get_precision('Account')),
                }
               
cash_tunai_opname()