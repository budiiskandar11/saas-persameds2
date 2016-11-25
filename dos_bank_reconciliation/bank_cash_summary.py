import time
from openerp import pooler
from openerp.osv import fields, osv

class wizz_cash_bank_summary(osv.osv_memory):
    _name = "wizz.cash.bank.summary"
    _columns = {
            'company_id'    : fields.many2one('res.company', 'Company', required=True),
            'fiscalyear_id' : fields.many2one('account.fiscalyear', 'Fiscal Year'),
            'start_date'    : fields.date('Start Date'),
            'end_date'      : fields.date('End Date'),
            'district_id'   : fields.many2one('hr.distrik', 'District'),
            #'journal_id'    : fields.many2one('account.journal', 'Cash/Bank'),
                }
    _defaults = {
            'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'wizz.cash.bank.summary', context=c),
                 } 
    
    def create_cash_bank_report(self, cr, uid, ids, context=None):
        print "create_cash_bank_report----------MASUK", ids
        res = {}
        if context is None:
            context = {}
        datas = {'ids': ids}#context.get('active_ids', [])}
        datas['model'] = 'wizz.cash.bank.summary'
        datas['form'] = self.read(cr, uid, ids)[0]
        #period_ids = self.pool.get('account.period').search(cr, uid, [('fiscalyear_id','=',datas['form']['fiscalyear_id'][0])])
        #period = self.pool.get('account.period').browse(cr, uid, period_ids)
#         i=1
#         for p in period:
#             res[str(i)] = {
#                 'id': p.id,
#                 'name': p.name,
#                 'date': time.strftime('%b-%y', time.strptime(p.date_start,'%Y-%m-%d')),
#                 'start': p.date_start,
#                 'end': p.date_stop,
#             }
#             i+=1
#         datas['form'].update(res)
        print "datas>>>>>>>>>>>>>>>>>>>)))", datas
        
        return { 
            'type': 'ir.actions.report.xml',
            'report_name': 'cash.bank.summary.xls',
            'datas': datas,
                }
    
wizz_cash_bank_summary()