import time
import datetime
from datetime import date

from datetime import timedelta
from dateutil import relativedelta

from openerp import api, tools
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

from openerp.tools.safe_eval import safe_eval as eval

class hr_employee(osv.osv):
    _inherit = 'hr.employee'
    
    _columns = {
            'insurance_id' : fields.char('Insurance Number', size=64),
                }
hr_employee()

class hr_bpjstk_run(osv.osv):
    _name = 'hr.bpjstk.run'
    _description = 'BPJS TK Batches'
    
    
    _columns = {
        'name': fields.char('Name', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        #'name' : fields.many2one('account.period',"Periode"),
        'bpjstk_ids': fields.many2many('hr.bpjs.tk', 'bpjstk_rel','bpjs_tk_id', 'bpjs_run_id', required=False),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('close', 'Close'),
        ], 'Status', select=True, readonly=True, copy=False),
        'date_start': fields.date('Date From', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'date_end': fields.date('Date To', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'credit_note': fields.boolean('Credit Note', readonly=True, states={'draft': [('readonly', False)]}, help="If its checked, indicates that all payslips generated from here are refund payslips."),
        'user_id' : fields.many2one('res.users', "Created By"),
        'date_create' : fields.date('Date Created'),
        'period_id'   : fields.many2one('account.period', "Period"),
        'total_empl'    : fields.float("Total Employee"),
        'total_jkm'    : fields.float("Total JKM"),
        'total_iuran_employee' : fields.float("Total Iuran"),
        'total_jht_com'   : fields.float("Total JHT by Company"),
        'total_wages'           : fields.float("Total Wages"),
        'total_jkk'             : fields.float("Total JKK"),
        'total_jht_emp'             : fields.float("Total JHT by Employee"),
        'company_id'    : fields.many2one('res.company',"Company"),
        'npp' : fields.related('company_id', 'npp', string='NPP', type='char', relation='res.company', readonly=True, store=True),
    }
    _defaults = {
        'state': 'draft',
         'user_id': lambda s, cr, uid, c: uid,
         'date_create' : lambda *a:time.strftime('%Y-%m-%d'),
        'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'hr.employee', context=c),
        'name'  : 'BPJS Ketenagakerjaan Monthly Report', 
        'date_start': lambda *a: time.strftime('%Y-%m-01'),
        'date_end': lambda *a: str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10],
    }

    def draft_bpjstk_run(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

    def close_bpjstk_run(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'close'}, context=context)


hr_bpjstk_run()





class hr_contract(osv.osv):
    _inherit = 'hr.contract'
    
    def _calculate_salary(self, cr, uid, ids, field_names, arg, context=None):
        vals = {}
        allowance   = 0.0
        thp         = 0.0
        
        rule_categ_obj  = self.pool.get('hr.salary.rule.category')
        rule_obj        = self.pool.get('hr.salary.rule')
        
        alw_rule_categ  = rule_categ_obj.search(cr, uid, [('code','=','ALW')])
        
        alw_rule        = rule_obj.search(cr, uid, [('category_id','in',tuple(alw_rule_categ))])
        
        ###Uang Makan###
        uang_makan      = 22 * 40000
        ###Uang Transport###
        uang_transport  = 22 * 50000
        
        for contract in self.browse(cr, uid, ids, context=context):
            if not contract.struct_id:
                vals[contract.id] = {'advantages_gross':0.0,}
                continue
            for rule_id in contract.struct_id.rule_ids:
                if rule_id.id in tuple(alw_rule):
                    allowance += rule_id.amount_fix

            vals[contract.id] = {
                'advantages_gross'  : allowance,
                'thp'               : contract.wage + allowance + uang_makan + uang_transport + contract.fasilitas_jabatan,
            }
        return vals
    
    _columns = {
            'advantages_gross'  : fields.function(_calculate_salary, method=True, multi='dc', type='float', string='Allowances', digits=(14,2)),
            'thp'               : fields.function(_calculate_salary, method=True, multi='dc', type='float', string='Take Homepay', digits=(14,2)),
                }
    
hr_contract()

class hr_bpjs_tk(osv.osv):
    _name = "hr.bpjs.tk"
    _description = "BPJS Ketenagakerjaan"
    
    def compute(self, cr, uid, ids, context=None):
        for val in self.browse(cr, uid, ids, context=None):
            ##Write THP##
            contract_wage = val.contract_id.thp
        self.write(cr, uid, ids, {'contract_wage': contract_wage})
    
    def _allowance_daily_amount(self, cr, uid, ids, name, args, context):
        if not ids: return {}
        
        attendance_obj          = self.pool.get('hr.attendance')
        allowance_day           = 0
        attendance_day          = 0
        absence_allowance_day   = 0
        res = {}
        for val in self.browse(cr, uid, ids, context=context):
            if val.date_from:
                cr.execute("select count(id) from hr_attendance where day <= %s and day >= %s and employee_id = %s and action = %s", (val.date_to, val.date_from, val.name.id, "sign_in"))
                attendance_day = cr.fetchone()[0]
                
                ###Filter Reason Allowance###
                cr.execute("select id from absence_reason where allowance = True")
                reason_allowance = tuple(map(lambda x: x[0], cr.fetchall()))
                
                print "reason_allowance---------->>", reason_allowance
                
                ###
                cr.execute("select count(id) from hr_absence where date <= %s and date >= %s and employee_id = %s and reason in %s", (val.date_to, val.date_from, val.name.id, reason_allowance))
                absence_allowance_day = cr.fetchone()[0]
            
            print "allowance_day---------->>", allowance_day
            print "absence_day", absence_allowance_day
            
            ###Khusus Potongan diasumsikan selama 22 Hari###
            #total_days = attendance_day + absence_allowance_day
            total_days = 22
            
            ###Uang Makan###
            uang_makan          = total_days * 40000
            ###Uang Transportasi###
            uang_transportasi   = total_days * 50000
            
            res[val.id] = uang_makan + uang_transportasi 
        return res
    
    def _calculate(self, cr, uid, ids, field_names, arg, context=None):
        res = {}
        jht_amount      = 0
        jpk_amount      = 0
        jkk_amount      = 0
        jk_amount       = 0
        tk_lhk_amount   = 0
        married         =['married','sudah menikah','menikah','berkeluarga']
            
        for rs in self.browse(cr, uid, ids, context=context):
            allowance_daily_amount = rs.allowance_daily_amount
            contract_ids    = self.pool.get('hr.contract').search(cr,uid,[('employee_id','=',rs.name.id)])
            #print "contract_ids",contract_ids,rs.contract_id.name
            if len(contract_ids)==0:
                raise osv.except_osv(_('No Contract Found!'), _('No contract found for this employee!\nPlease create contract for this employee first.'))
            else:
                #contract        =self.pool.get('hr.contract').browse(cr,uid,contract_ids[0])
                contract        = self.browse(cr, uid, ids[0]).contract_id
            jht_amount = 0.0
            jht_by_employee = 0.0
            jht_by_company = 0.0
            jpk_amount = 0.0
            jkk_amount = 0.0
            jk_amount = 0.0
            if rs.jht:
                jht_amount      = (contract.wage+contract.advantages_gross + allowance_daily_amount)*0.057
                jht_by_employee = (contract.wage+contract.advantages_gross + allowance_daily_amount)*0.02
                jht_by_company  = (contract.wage+contract.advantages_gross + allowance_daily_amount)*0.037
            
            if rs.jkk:
                jkk_amount=(contract.wage+contract.advantages_gross + allowance_daily_amount)*0.0024
                
            if rs.jk:
                jk_amount=(contract.wage+contract.advantages_gross + allowance_daily_amount)*0.003
            
            print "jht_amount+jpk_amount+jkk_amount+jk_amount+tk_lhk_amount", jht_amount+jpk_amount+jkk_amount+jk_amount+tk_lhk_amount
            
            record = {
                      'jht_amount'      : jht_amount,
                      'jht_by_employee' : jht_by_employee,
                      'jht_by_company'  : jht_by_company,
                      'jpk_amount'      : jpk_amount,
                      'jkk_amount'      : jkk_amount,
                      'jk_amount'       : jk_amount,
                      'tk_lhk_amount'   : tk_lhk_amount,
                      'total'           : jht_amount+jpk_amount+jkk_amount+jk_amount+tk_lhk_amount,
                      'total_by_employee' : jht_by_employee,
                      'total_by_company' : jht_by_company + jk_amount + jkk_amount,
                      #'contract_wage'   : (contract.wage+contract.advantages_gross + allowance_daily_amount),
                      }
            res[rs.id] = record
        return res
    
    def _get_info(self, cr, uid, ids, field_names, arg, context=None):
        res= {}
        for jsostek in self.browse(cr,uid,ids,context):
            emp_id      = jsostek.name.id
            contract_id = self.pool.get('hr.contract').search(cr,uid,[('employee_id','=',emp_id),'|',('date_end','>=',time.strftime("%Y-%m-%d")),('date_end','=',False)])
            if not contract_id:
                raise osv.except_osv(_('No Valid Contract Found!'), _('No valid contract found for this employee!\nPlease create contract for this employee first.'))
            else:
                contract_id = contract_id[0]
            department_id        = jsostek.name.department_id.id
            #section_id           = jsostek.name.section.id
            job_id               = jsostek.name.job_id.id
            #current_job_level_id = jsostek.name.current_job_level.id
            record={
                    #'contract_id':contract_id or False,
                    'department_id':department_id or False,
                    #'section_id':section_id or False,
                    'job_id':job_id,
                    #'current_job_level_id':current_job_level_id,
                    }
            res[jsostek.id]=record
            #self.write(cr, uid, ids, {'contract_id': contract_id})
        return res
    
    def onchange_employee_id(self, cr, uid, ids, employee_id, context=None):
        res = {}
       
        current_date = datetime.date.today()
        employee_obj  = self.pool.get('hr.employee')
       
        contract_ids = self.pool.get('hr.contract').search(cr, uid, [('employee_id','=',employee_id),('date_start','<=',current_date),'|',('date_end','>=',current_date),('date_end','=',False)])
        if not contract_ids:
            raise osv.except_osv(_('No Valid Contract Found!'), _('No valid contract found for this employee!\nPlease create contract for this employee first.'))
        contract = self.pool.get('hr.contract').browse(cr, uid, contract_ids)[0]
        
        if employee_id:
            emp = employee_obj.browse(cr, uid, employee_id, context=context)
            department_id        = emp.department_id.id
            #section_id           = emp.section.id
            job_id               = emp.job_id.id
            nik                  = emp.nik
            dob                 = emp.dob or False
            status               = emp.state_id
            current_job_level_id = emp.level and emp.level.id or False
            
            res = {
                'contract_id': contract.id or False,
                'department_id': department_id or False,
                'employee_number': nik or False,
                'job_id': job_id,
                'dob'   : dob,
                'emp_status' : status, 
                'current_job_level_id': current_job_level_id,
                  }
        return {'value': res}   
           
           


    
    def onchange_period(self, cr, uid, ids, employee_id, period_id, context=None):
        res = {}
        period_obj  = self.pool.get('account.period')
        employee_obj  = self.pool.get('hr.employee')
        period      = period_obj.browse(cr, uid, period_id)
        contract_ids = self.pool.get('hr.contract').search(cr, uid, [('employee_id','=',employee_id),('date_start','<=',period.date_start),'|',('date_end','>=',period.date_start),('date_end','=',False)])
        if not contract_ids:
            raise osv.except_osv(_('No Valid Contract Found!'), _('No valid contract found for this employee!\nPlease create contract for this employee first.'))
        contract = self.pool.get('hr.contract').browse(cr, uid, contract_ids)[0]
        #jsostek = self.browse(cr, uid, ids)[0]
        if employee_id:
            emp = employee_obj.browse(cr, uid, employee_id)
            department_id        = emp.department_id.id
            #section_id           = emp.section.id
            job_id               = emp.job_id.id
            current_job_level_id = emp.level and emp.level.id or False
        res = {
            'contract_id': contract.id or False,
            'department_id': department_id or False,
            #'section_id': section_id or False,
            'job_id': job_id,
            'current_job_level_id': current_job_level_id,
        }
        return {'value': res}
    
    _columns = {
                'jnumber'       : fields.char('BPJS Number',size=32,required=True,readonly=True, states={'draft':[('readonly',False)]}),
                'name'          : fields.many2one('hr.employee','Employee Name',required=True,readonly=True,states={'draft':[('readonly',False)]}),
                #'contract_id'   : fields.function(_get_info,method=True,string="Contract",type="many2one",obj="hr.contract",store=True,multi='dc'),
                'contract_id'   : fields.many2one('hr.contract', 'Contract',readonly=True,states={'draft':[('readonly',False)]}),
                'department_id' : fields.many2one('hr.department', 'Department' , readonly=True,states={'draft':[('readonly',False)]}),
              
                'job_id'        : fields.many2one('hr.job', 'Job Title', readonly=True,states={'draft':[('readonly',False)]}),
                'current_job_level_id': fields.char("Level", size=32, readonly=True,states={'draft':[('readonly',False)]}),
                'emp_status'    : fields.char('Employee Status',size=64,readonly=True,states={'draft':[('readonly',False)]}),
                'reg_date'      : fields.date('Registered Date',readonly=True,states={'draft':[('readonly',False)]}),
                'branch_office' : fields.many2one('res.partner','Jamsostek Branch Office'),
                'jht'           : fields.boolean('Jaminan Hari Tua (JHT)',help='Check this box for JHT',required=True,readonly=True,states={'draft':[('readonly',False)]}),
                'jpk'           : fields.boolean('Jaminan Pemeliharaan Kesehatan (JPK)',help='Check this box for JPK',readonly=True,states={'draft':[('readonly',False)]}),
                'jkk'           : fields.boolean('Jaminan Kecelakaan Kerja (JKK)',help='Check this box for JKK',states={'draft':[('readonly',False)]}),
                'jk'            : fields.boolean('Jaminan Kematian (JKM)',help='Check this box for JK',readonly=True,states={'draft':[('readonly',False)]}),
                'tk_lhk'        : fields.boolean('Luar Hubungan Kerja',help='Check this box for TK-LHK',readonly=True,states={'draft':[('readonly',False)]}),
                'tax_type'      : fields.selection([('k1','K1'),
                                                    ('k2','K2'),
                                                    ('k3','K3')],'Tax Type'),
                'bank_account'  : fields.char('Bank Account',size=32),
                'note'          : fields.text('Notes'),
                'period_id'     : fields.many2one('account.period','Period',readonly=True,states={'draft':[('readonly',False)]}),
                #'contract_wage' : fields.function(_calculate, method=True, store=False, multi='dc', string='Take Home Pay', digits_compute=dp.get_precision('Account')),
                'contract_wage' : fields.float(string='Take Home Pay', digits_compute=dp.get_precision('Account')),
                'jht_amount'    : fields.function(_calculate, method=True, store=False, multi='dc', string='JHT Amount', digits_compute=dp.get_precision('Account')),
                'jht_by_employee'    : fields.function(_calculate, method=True, store=False, multi='dc', string='JHT By Employee', digits_compute=dp.get_precision('Account')),
                'jht_by_company'    : fields.function(_calculate, method=True, store=False, multi='dc', string='JHT By Company', digits_compute=dp.get_precision('Account')),
                'jpk_amount'    : fields.function(_calculate, method=True, store=False, multi='dc', string='JPK Amount', digits_compute=dp.get_precision('Account')),
                'jkk_amount'    : fields.function(_calculate, method=True, store=False, multi='dc', string='JKK Amount', digits_compute=dp.get_precision('Account')),
                'jk_amount'     : fields.function(_calculate, method=True, store=False, multi='dc', string='JK Amount', digits_compute=dp.get_precision('Account')),
                'tk_lhk_amount' : fields.function(_calculate, method=True, store=False, multi='dc', string='TK-LHK Amount', digits_compute=dp.get_precision('Account')),
                'total_by_employee' : fields.function(_calculate, method=True, store=False, multi='dc', string='Total by Employee', digits_compute=dp.get_precision('Account')),
                'total_by_company' : fields.function(_calculate, method=True, store=False, multi='dc', string='Total by Company', digits_compute=dp.get_precision('Account')),
                'total'         : fields.function(_calculate, method=True, store=False, multi='dc', string='Total', digits_compute=dp.get_precision('Account')),
                
                'state'         : fields.selection([('draft','Draft'),('registered','Active'),('non_active','Non Active')],'State',readonly=True),
                'employee_number'   : fields.char("NIK", size=64, readonly=True,states={'draft':[('readonly',False)]}),
                'bpjs_run_id': fields.many2one('hr.bpjs.tk', 'BPJS TK Batches', readonly=True, states={'draft': [('readonly', False)]}, copy=False),
                'dob'         : fields.date('Date of Birth'),
                'date_from'  : fields.date('Date From', required=True),
                'date_to'    : fields.date('Date To', required=True),
                
                'allowance_daily_amount' : fields.function(_allowance_daily_amount, method=True, type='float', string='Allowances Daily Amount', digits_compute=dp.get_precision('Payroll'),),
                }
    _defaults ={
                'state'         : 'draft',
                }
    
    def register(self,cr,uid,ids,context=None):
        self.write(cr,uid,ids,{'state':'registered'})
        return True
    
    def non_active(self,cr,uid,ids,context=None):
        self.write(cr,uid,ids,{'state':'non_active'})
        return True
    
    def modify(self,cr,uid,ids,context=None):
        self.write(cr,uid,ids,{'state':'draft'})
        return True
    
    def cancel(self,cr,uid,ids,context=None):
        self.write(cr,uid,ids,{'state':'draft'})
        return True
hr_bpjs_tk()