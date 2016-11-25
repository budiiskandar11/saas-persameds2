import time
from openerp import pooler
from openerp.osv import fields, osv

class wizz_cash_bank_summary(osv.osv_memory):
    _name = "wizz.payroll.summary"
    _columns = {
            'company_id'    : fields.many2one('res.company', 'Company', required=True),
            'fiscalyear_id' : fields.many2one('account.fiscalyear', 'Fiscal Year'),
            'bank_id'       : fields.many2one('res.bank', 'Bank'),
            'start_date'    : fields.date('Start Date'),
            'end_date'      : fields.date('End Date'),
                }
    _defaults = {
            'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'wizz.cash.bank.summary', context=c),
                 } 
    
    def create_report(self, cr, uid, ids, context=None):
        print "create_report----------MASUK", ids
        res = {}
        if context is None:
            context = {}
        datas = {'ids': ids}#context.get('active_ids', [])}
        datas['model'] = 'wizz.payroll.summary'
        datas['form'] = self.read(cr, uid, ids)[0]
        print "datas>>>>>>>>>>>>>>>>>>>)))", datas
        
        return { 
            'type': 'ir.actions.report.xml',
            'report_name': 'payroll.summary.bii.xls',
            'datas': datas,
                }
    
wizz_cash_bank_summary()