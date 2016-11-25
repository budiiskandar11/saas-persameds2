import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta

from openerp import netsvc
from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.tools.safe_eval import safe_eval as eval

class hr_payslip_run(osv.osv):
    _inherit="hr.payslip.run"
    
    def close_payslip_run(self, cr, uid, ids, context=None):
        print "print payslip run"
        if not context:
            context={}
        move_pool = self.pool.get('account.move')
        period_pool = self.pool.get('account.period')
        timenow = time.strftime('%Y-%m-%d')
        batches=self.browse(cr,uid,ids)
        for batch in batches:
            if batch.slip_ids:
                line_ids = []
                debit_sum = 0.0
                credit_sum = 0.0
                partner_id = batch.partner_id.id
                if not batch.slip_ids[0].period_id:
                    search_periods = period_pool.find(cr, uid, batch.date_start, context=context)
                    period_id = search_periods[0]
                else:
                    period_id = batch.slip_ids[0].period_id.id
    
                name = _('Payslip Batch - %s') % (batch.name)
                move = {
                    'narration': name,
                    'date': timenow,
                    'ref': batch.name,
                    'journal_id': batch.slip_ids[0].journal_id.id,
                    'period_id': period_id,
                }
                debit_line ={}
                credit_line ={}
                debit_sum=0.0
                credit_sum=0.0
                for slip in batch.slip_ids:
                    if slip.line_ids:
                        for line in slip.line_ids:
                            debit_account_id = line.salary_rule_id.account_debit.id
                            credit_account_id = line.salary_rule_id.account_credit.id
                            #print "slip.credit_note",slip.credit_note
                            amt = slip.credit_note and -line.total or line.total
                            #print "========================================================================="
                            #print line.name," - ",amt, " - ",line.total," - D: ",line.salary_rule_id.account_debit.id," - -C: ",line.salary_rule_id.account_credit.id
                            #print "========================================================================="
                            if debit_account_id:
                                if not debit_line.has_key(debit_account_id):
                                    debit_line.update({debit_account_id:(0, 0, {
                                            'name': line.name,
                                            'date': timenow,
                                            'partner_id': partner_id,
                                            'account_id': debit_account_id,
                                            'journal_id': slip.journal_id.id,
                                            'period_id': period_id,
                                            'debit': amt > 0.0 and amt or 0.0,
                                            'credit': amt < 0.0 and -amt or 0.0,
                                            'analytic_account_id': line.salary_rule_id.analytic_account_id and line.salary_rule_id.analytic_account_id.id or False,
                                            'tax_code_id': line.salary_rule_id.account_tax_id and line.salary_rule_id.account_tax_id.id or False,
                                            'tax_amount': line.salary_rule_id.account_tax_id and amt or 0.0,
                                        })
                                        })
                                else:
                                    debit_line[debit_account_id][2]['debit'] += amt > 0.0 and amt or 0.0
                                    debit_line[debit_account_id][2]['credit'] += amt < 0.0 and -amt or 0.0
                            
                            if credit_account_id:
                                if not credit_line.has_key(credit_account_id):
                                    credit_line.update({credit_account_id: (0, 0, {
                                        'name': line.name,
                                        'date': timenow,
                                        'partner_id': partner_id,
                                        'account_id': credit_account_id,
                                        'journal_id': slip.journal_id.id,
                                        'period_id': period_id,
                                        'debit': amt < 0.0 and -amt or 0.0,
                                        'credit': amt > 0.0 and amt or 0.0,
                                        'analytic_account_id': line.salary_rule_id.analytic_account_id and line.salary_rule_id.analytic_account_id.id or False,
                                        'tax_code_id': line.salary_rule_id.account_tax_id and line.salary_rule_id.account_tax_id.id or False,
                                        'tax_amount': line.salary_rule_id.account_tax_id and amt or 0.0,
                                        })
                                    })
                                else:
                                    credit_line[credit_account_id][2]['debit'] += amt < 0.0 and -amt or 0.0
                                    credit_line[credit_account_id][2]['credit'] += amt > 0.0 and amt or 0.0
                        for cred_key in credit_line:
                            credit_sum += credit_line[cred_key][2]['credit'] - credit_line[cred_key][2]['debit']
                        for deb_key in debit_line:
                            debit_sum += debit_line[deb_key][2]['debit'] - debit_line[deb_key][2]['credit']
                for key in debit_line :
                    line_ids.append(debit_line[key])
                    
                for key in credit_line :
                    line_ids.append(credit_line[key])
                    
                if debit_sum > credit_sum:
                    acc_id = batch.slip_ids[0].journal_id.default_credit_account_id.id
                    if not acc_id:
                        raise osv.except_osv(_('Configuration Error!'),_('The Expense Journal "%s" has not properly configured the Credit Account!')%(slip.journal_id.name))
                    adjust_credit = (0, 0, {
                        'name': _('Adjustment Entry'),
                        'date': timenow,
                        'partner_id': partner_id,
                        'account_id': acc_id,
                        'journal_id': batch.slip_ids[0].journal_id.id,
                        'period_id': period_id,
                        'debit': 0.0,
                        'credit': debit_sum - credit_sum,
                    })
                    raise osv.except_osv(_('Difference in sum debit_sum > credit_sum!'),_('Debit Sum "%s" & Credit Sum "%s"')%(debit_sum,credit_sum))
                    line_ids.append(adjust_credit)
    
                elif debit_sum < credit_sum:
                    acc_id = batch.slip_ids[0].journal_id.default_debit_account_id.id
                    if not acc_id:
                        raise osv.except_osv(_('Configuration Error!'),_('The Expense Journal "%s" has not properly configured the Debit Account!')%(slip.journal_id.name))
                    adjust_debit = (0, 0, {
                        'name': _('Adjustment Entry'),
                        'date': timenow,
                        'partner_id': partner_id,
                        'account_id': acc_id,
                        'journal_id': batch.slip_ids[0].journal_id.id,
                        'period_id': period_id,
                        'debit': credit_sum - debit_sum,
                        'credit': 0.0,
                    })
                    raise osv.except_osv(_('Difference in sum debit_sum < credit_sum!'),_('Debit Sum "%s" & Credit Sum "%s"')%(debit_sum,credit_sum))
                    line_ids.append(adjust_debit)
                move.update({'line_id': line_ids})
#                print "moveeeeeeeeeee==========\n\n\r"
                all_slip_id=[x.id for x in batch.slip_ids]
#                print 'all_slip_id',all_slip_id
#                print "==========\n\n\r"
                move_id = move_pool.create(cr, uid, move, context=context)
                
                self.pool.get('hr.payslip').write(cr, uid, all_slip_id, {'move_id': move_id, 'period_id' : period_id, "state":'done'}, context=context)
                if slip.journal_id.entry_posted:
                    move_pool.post(cr, uid, [move_id], context=context)             
        return self.write(cr, uid, ids, {'move_id': move_id,'state': 'close'}, context=context)
    
hr_payslip_run()