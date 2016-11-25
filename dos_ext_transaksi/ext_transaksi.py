from mx import DateTime
from lxml import etree

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import openerp.addons.decimal_precision as dp
from openerp import netsvc

from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import api

class ext_transaksi(osv.osv):
    _name = "ext.transaksi"
    _description = "Extra Transaksi"
    
    _columns = {
            'name' : fields.char('Description', 128, required=True, readonly=True, states={'draft':[('readonly',False)]}),
            'ext_line' : fields.one2many('ext.transaksi.line', 'ext_transaksi_id','Lines', required=True, readonly=True, states={'draft':[('readonly',False)]}),
            'journal_id': fields.many2one('account.journal', 'Journal', required=True, readonly=True, states={'draft':[('readonly',False)]}),
            'ref': fields.char('Reference', size=64, readonly=True, states={'draft':[('readonly',False)]}),
            'date': fields.date('Transaction Date', required=True, readonly=True, states={'draft':[('readonly',False)]}),
            'state':fields.selection([('draft','Draft'), ('confirm','Confirm'), ('posted','Posted')], 'State', readonly=True),
            'move_id':fields.many2one('account.move', 'Account Entry',readonly=True, states={'draft':[('readonly',False)]}),
            'move_ids': fields.related('move_id','line_id', type='one2many', relation='account.move.line', string='Journal Items',readonly=True, states={'draft':[('readonly',False)]}),
            'currency_id':fields.many2one('res.currency', 'Currency', readonly=True, states={'draft':[('readonly',False)]}),
            'force_period': fields.many2one('account.period','Force Period', required=False, readonly=True, states={'draft':[('readonly',False),('required',True)]}),
            'number': fields.char('Number', size=32, readonly=True, states={'draft':[('readonly',False)]}),
            'company_id': fields.many2one('res.company', 'Company', required=True, change_default=True, readonly=True, states={'draft':[('readonly',False)]}),
            'distrik_id' : fields.many2one('hr.distrik',"Distrik", readonly=True, states={'draft':[('readonly',False)]}),
            'type'      : fields.selection([('general','General'),
                                            ('asset','Asset'),
                                            ],'Tipe',  readonly=True, states={'draft':[('readonly',False)]}),
           'registered' : fields.boolean('Registered',readonly=True),
            #'department_id': fields.many2one('hr.department','Department', readonly=True, states={'draft':[('readonly',False)]})
            #'move_ids': fields.related('move_id','line_id', type='one2many', relation='account.move.line', string='Journal Items', readonly=True),    
                }
    
    _defaults = {
            'state' : 'draft',
            'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'ext.transaksi', context=c),
            #'currency_id': 12
            'type'  : 'general',
                 }
    _order = "id desc"
    
    def notification_remainder(self, cr, uid, ids, context=None):
        print "AAAAAAAAAAAA"
        self.pool.get('notification.remainder').notification_remainder(cr,uid,ids,context=None)
        return True
    
    def auto_balance(self, cr, uid, ids, move_id, context=None):
        
        move_pool = self.pool.get('account.move')
        move_line_pool = self.pool.get('account.move.line')
        sum_debit   = 0.0
        sum_credit  = 0.0
        move = move_pool.browse(cr, uid, move_id, context=None)
        for line in move.line_id:
            sum_debit   += line.debit
            sum_credit  += line.credit
        
        print "sum_debit", sum_debit, sum_credit
        
        
        sum_debit   = 0.0
        sum_credit  = 0.0
        move = move_pool.browse(cr, uid, move_id, context=None)
        for line in move.line_id:
            sum_debit   += line.debit
            sum_credit  += line.credit
            
            print line.debit, line.credit
        
        diff = sum_debit - sum_credit
        print "sum_debit", sum_debit, sum_credit
        print "Selisih=============", diff
        
        if abs(diff) < 0.1:
            if diff > 0:
                print "EDIT CREDIT"
                move_line_search = move_line_pool.search(cr, uid, [('move_id','=', move_id), ('credit','<>',0.0)])
                move_line_balance = move_line_pool.browse(cr, uid, move_line_search)[0]
                
                balance_update = move_line_balance.credit + abs(diff)
                
                print "move_line_balance.credit + diff", balance_update
                move_line_pool.write(cr, uid, move_line_balance.id, {'credit' : balance_update})
            
            else:
                print "EDIT DEBIT"
                move_line_search = move_line_pool.search(cr, uid, [('move_id','=', move_id), ('debit','<>',0.0)])
                move_line_balance = move_line_pool.browse(cr, uid, move_line_search)[0]
                
                balance_update = move_line_balance.debit + abs(diff)
                print "move_line_balance.credit + diff", balance_update
                
                move_line_pool.write(cr, uid, move_line_balance.id, {'debit' : balance_update,})
        return True
    
    def confirm_action(self, cr, uid, ids, context=None):
        for val in self.browse(cr,uid,ids,context=None):
            company_currency    = val.company_id.currency_id.id
            transaction_currency= val.currency_id.id
            
            if company_currency <> transaction_currency:
                for line in val.ext_line:
                    if line.amount_currency == 0.0:
                        raise osv.except_osv(_('Error !'), _('Please define input amount currency in %s !') % val.currency_id.name)
            
        return self.write(cr, uid, ids, {'state':'confirm'}, context=None)
    
    def asset_register(self, cr, uid, ids, context=None):
        #context = context or {}
        asset_obj = self.pool.get('asset.register')
        move = self.browse(cr,uid,ids, context=None)
          
        for line in move.ext_line:
            if line.debit > 0.0 :
                vals = {
                            'name': line.name,
    #                         'asset_desc': line.name,
                             'origin': move.number or False,
                             'purchase_value': line.debit,
    #                         'partner_id': line..partner_id.id,
                             'purchase_date' : move.date,
    #                         'employee_id' :line.order_id.employee_id.id,
    #                         'department_id':line.order_id.department_id.id,
                            'distrik_id':move.distrik_id.id,
                             'currency_id': move.currency_id.id,
                              'cip_account_id' : line.account_id.id,
                              'send_asset' : 'no', 
                              
                        }
                asset_id = asset_obj.create(cr, uid, vals, context=context)
                self.write(cr, uid, ids, {'registered': True})     
        return True
        
    def posted_action(self, cr, uid, ids, context=None):
        if not context:
            context={}
        account_obj = self.pool.get('account.account')
        move_pool = self.pool.get('account.move')
        move_line_pool = self.pool.get('account.move.line')
        seq_obj = self.pool.get('ir.sequence')
        currency_obj = self.pool.get('res.currency')
        for ext_pay in self.browse(cr, uid, ids, context=context):
            #print "Name===============>>",ext_pay.name
            if ext_pay.number:
                name = ext_pay.number
            elif ext_pay.journal_id.sequence_id:
                name = seq_obj.get_id(cr, uid, ext_pay.journal_id.sequence_id.id)
            else:
                raise osv.except_osv(_('Error !'), _('Please define a sequence on the journal !'))
            #seq = seq_obj.get_id(cr, uid, ext_pay.journal_id.sequence_id.id)
            move = {
                'name': name,
                'journal_id': ext_pay.journal_id.id,
                'narration': ext_pay.ref,
                'date': ext_pay.date,
                'ref': ext_pay.name,
                'period_id': ext_pay.force_period.id,
                ###
                ###By Pass Close Period###
                'force_period_allow' : True
                ###
                }
            move_id = move_pool.create(cr, uid, move)
            #print "LINES :::::", ext_pay.ext_line
            #acc = account_obj.browse(cr, uid, account_id, context=context)
            balance = 0.0
            company_currency = ext_pay.company_id.currency_id.id
            for ext_pay_line in ext_pay.ext_line:
                acc = account_obj.browse(cr, uid, ext_pay_line.account_id.id, context=context)
                debit = currency_obj.compute(cr, uid, ext_pay.currency_id.id, company_currency, ext_pay_line.debit, context={'date': ext_pay.date})
                credit = currency_obj.compute(cr, uid, ext_pay.currency_id.id, company_currency, ext_pay_line.credit, context={'date': ext_pay.date})
                
                print "XXXXXXXXXXXXXXXXXX", company_currency <> ext_pay.currency_id.id and ext_pay_line.debit or -ext_pay_line.credit or 0.0
                
                move_line = {
                    'name'              : ext_pay_line.name or '/',
                    'debit'             : ext_pay_line.debit,
                    'credit'            : ext_pay_line.credit,
                    'account_id'        : ext_pay_line.account_id.id,
                    'move_id'           : move_id,
                    'journal_id'        : ext_pay.journal_id.id,
                    'period_id'         : ext_pay.force_period.id,
                    'analytic_account_id': ext_pay_line.analytic_account_id.id,
                    'partner_id'        : ext_pay_line.partner_id.id,
                    'currency_id'       : company_currency <> ext_pay.currency_id.id and ext_pay.currency_id.id or False,
                    #'program_budget_id' : ext_pay_line.program_budget_id.id or False,
                    'amount_currency'   : ext_pay_line.amount_currency,#company_currency <> ext_pay.currency_id.id and ext_pay_line.debit or company_currency <> ext_pay.currency_id.id and -ext_pay_line.credit or 0.0,
                    'date'              : ext_pay.date,
                    ###
                    'force_period_allow' : True,
                    ###
                    }
                balance += ext_pay_line.amount_currency
                #print "1",move_line
                move_line_pool.create(cr, uid, move_line)
            
            if balance != 0.0:
                raise osv.except_osv(_('Error !'), _('Amount Currency not Balance !'))
            
            #self.auto_balance(cr, uid, ids, move_id, context)    
            
            move_pool.post(cr, uid, [move_id], context={})
            self.write(cr, uid, ids, {
                'state': 'posted',
            })
        return self.write(cr, uid, ids, {'state':'posted','move_id':move_id, 'number':name}, context=context)
    
    
#    def cancel_transaction(self, cr, uid, ids, context=None):
#        print "cancel ids",ids
#        move_pool = self.pool.get('account.move')
#        move_pool_obj = self.pool.get('account.move.line')
#        obj_account_analytic_line = self.pool.get('account.analytic.line')
#        id=self.browse(cr,uid,ids,context=context)[0]
#        move_id=id.move_id.id
#        
#        print "move_id", move_id
#        move_pool_search = move_pool_obj.search(cr, uid, [('move_id','=',move_id)])
#        move_pool_browse = move_pool_obj.browse(cr, uid, move_pool_search)
#        
#        
#        for line in move_pool_browse:
#            print "line.id", line.id
#            analytic_line_search = obj_account_analytic_line.search(cr, uid, [('move_id','=',line.id)])
#            #print "analytic_line_id", analytic_line_id
#            analytic_line_browse = obj_account_analytic_line.browse(cr, uid, analytic_line_search)
#            #print "analytic_line_id", analytic_line_id
#            for analytic_line_id in analytic_line_browse:
#                if analytic_line_id:
#                    print "MASUKKKKKKKKKKKKKKKKKk", analytic_line_id.id
#                    obj_account_analytic_line.unlink(cr, uid, [analytic_line_id.id])
#        
#        #print "move_id",move_id
#        move_pool.write(cr,uid,[move_id],{'state':'draft'})
#        #move_pool.unlink(cr,uid,[move_id])
#        
#        
#        return self.write(cr, uid, ids, {'state':'draft'}, context=context)
#    
    
    def cancel_transaction(self, cr, uid, ids, context=None):
        
        reconcile_pool = self.pool.get('account.move.reconcile')
        move_pool = self.pool.get('account.move')
        move_pool_line = self.pool.get('account.move.line')
        analytic_line_pool = self.pool.get('account.analytic.line')
        
        for voucher in self.browse(cr, uid, ids, context=context):
            recs = []
            for line in voucher.move_ids:
                print "voucher.move_id.id", line.id
                analytic_line_search = analytic_line_pool.search(cr, uid, [('move_id','=',line.id)])
                move_pool_line.write(cr, uid, [line.id], {'analytic_account_id': ''})
                if analytic_line_search:
                    analytic_line_browse = analytic_line_pool.browse(cr, uid, analytic_line_search)
                    for line_analytic in analytic_line_browse:
                        recs.append(line_analytic.id)
                print "recs", recs, "line.move_id", line.move_id.id
                #analytic_line_pool.unlink(cr, uid, recs)
                #move_pool_line.write(cr, uid, [voucher.move_id.id], {'account_analytic_id': ''})
                move_pool.button_cancel(cr, uid, [line.move_id.id])
                move_pool.unlink(cr, uid, [line.move_id.id])
        res = {
            'state':'draft',
        }
        self.write(cr, uid, ids, res)
        return True    
    
ext_transaksi()

class ext_transaksi_line(osv.osv):
    _name = "ext.transaksi.line"
    _description = "Extra Transaksi"
    
    _columns = {
        'name'                  : fields.char('Description', 128,required=True),
        'reference'             : fields.char('Reference', 128,required=False),
        'ext_transaksi_id'      : fields.many2one('ext.transaksi', 'Extra Payment ID'),
        'debit'                 : fields.float('Debit'),
        'credit'                : fields.float('Credit'),
        'account_id'            : fields.many2one('account.account', 'Account', domain="[('type','!=','view')]", required=True),
        'department_id'         : fields.many2one('hr.department','Department',),
        'analytic_account_id'   : fields.many2one('account.analytic.account', 'Analytic Account'),
        'partner_id'            : fields.many2one('res.partner', string="Partner", help='The Ordering Partner'),
        'amount_currency'       : fields.float('Amount Currency', help="The amount expressed in an optional other currency if it is a multi-currency entry.", digits_compute=dp.get_precision('Account')),
        #'program_id': fields.many2one('program.program', 'Program'),
        #'program_budget_id': fields.many2one('program.budget', 'Program Budget'),
        
        #'currency_id': fields.many2one('res.currency', 'Currency', help="The optional other currency if it is a multi-currency entry."),
    }
    
    def onchange_program_budget(self,cr,uid,ids,program):
        res={}
        if program:
            program=self.pool.get('program.budget').browse(cr,uid,program)
            res['value'] = {'analytic_account_id':program.budget_line_id and program.budget_line_id.analytic_account_id and program.budget_line_id.analytic_account_id.id or False}
        return res
    
    def onchange_debit(self, cr, uid, ids, debit, credit):
        result= {}
        if debit:
            result['value'] = {
                'debit': debit,
                'credit': 0,
            }
        else:
            result['value'] = {
                'debit': 0,
                'credit': 0,
            }
        return result
    
    def onchange_credit(self, cr, uid, ids, debit, credit):
        result= {}
        if credit:
            result['value'] = {
                'debit': 0,
                'credit': credit,
            }
        else:
            result['value'] = {
                'debit': 0,
                'credit': 0,
            }
        return result
        
    
#    def onchange_currency(self, cr, uid, ids, account_id, amount, currency_id, date=False, journal=False, context=None):
#        if context is None:
#            context = {}
#        account_obj = self.pool.get('account.account')
#        journal_obj = self.pool.get('account.journal')
#        currency_obj = self.pool.get('res.currency')
#        if (not currency_id) or (not account_id):
#            return {}
#        result = {}
#        acc = account_obj.browse(cr, uid, account_id, context=context)
#        v = currency_obj.compute(cr, uid, currency_id, acc.company_id.currency_id.id, amount, context=context)
#        result['value'] = {
#            'debit': v > 0 and v or 0.0,
#            'credit': v < 0 and -v or 0.0,
#            'ammount_currency': v < 0 and -v or 0.0,
#        }
#        return result
    
ext_transaksi_line()