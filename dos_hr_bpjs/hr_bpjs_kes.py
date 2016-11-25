from openerp.osv import osv,fields
from openerp.addons import decimal_precision as dp
from openerp.tools.translate import _
import datetime
from datetime import date
from openerp import tools
import time


class hr_bpjs_kes(osv.osv):
    _name = "hr.bpjs.kes"
    _description = "BPJS Kesehatan"
    
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
            jpk_amount =0.0
            jpk_by_employee = 0.0
            jpk_by_company = 0.0
            jkk_amount = 0.0
            jk_amount = 0.0
            
            premi_karyawan      = 0.0 
            premi_perusahaan    = 0.0
            kelas = 0
            
            total_umr = 0.0
            if rs.jht:
                jht_amount      = (rs.contract_wage)*0.057
                jht_by_employee = (rs.contract_wage)*0.02
                jht_by_company  = (rs.contract_wage)*0.037

            if rs.jpk:
                premi_perusahaan    = 0.0
                premi_karyawan      = 0.0
                
                total_umr = (rs.contract_wage)
                #if total_umr <= 2700000:
                #    premi_perusahaan    = 2700000 * 0.04 #Premi Perusahaan
                #    premi_karyawan      = 2700000 * 0.005 #Premi Karyawan
                #elif total_umr > 2700000:
                #    premi_perusahaan    = 4725000 * 0.04 #Premi Perusahaan
                #    premi_karyawan      = 4725000 * 0.005 #Premi Karyawan
                
                premi_perusahaan    = total_umr * 0.04 #Premi Perusahaan
                premi_karyawan      = total_umr * 0.005 #Premi Karyawan
                
                if total_umr > 4725000:
                    premi_perusahaan    = 4725000 * 0.04 #Premi Perusahaan
                    premi_karyawan      = 4725000 * 0.005 #Premi Karyawan
                
                jpk_amount = premi_perusahaan + premi_karyawan 
                
                ###Cek Status dimatikan###
#                 if rs.name.marital:
#                     ####################
#                     if rs.name.marital == 'married':
#                         total_umr = (contract.wage+contract.advantages_gross + allowance_daily_amount)
#                         premi_perusahaan    = total_umr * 0.04 #Premi Perusahaan
#                         premi_karyawan      = total_umr * 0.005 #Premi Karyawan
#                         
#                         if total_umr > 4725000:
#                             premi_perusahaan    = 4725000 * 0.04 #Premi Perusahaan
#                             premi_karyawan      = 4725000 * 0.005 #Premi Karyawan
#                         
#                         jpk_amount = premi_perusahaan + premi_karyawan 
#                 else:
#                     raise osv.except_osv(_('No Marital Status Found!'), _('No marital status found for this employee!'))
            
            if rs.jkk:
                jkk_amount=(rs.contract_wage)*0.008
                
            if rs.jk:
                jk_amount=(rs.contract_wage)*0.003
            
            
            ###Class###
            if total_umr <> 0.0:
                if total_umr > 3543750:
                    kelas = 1
                else:
                    kelas = 2
            ###########
            
            print "jht_amount+jpk_amount+jkk_amount+jk_amount+tk_lhk_amount", jht_amount+jpk_amount+jkk_amount+jk_amount+tk_lhk_amount
            
            record = {
                      'jht_amount'      : jht_amount,
                      'jht_by_employee' : jht_by_employee,
                      'jht_by_company'  : jht_by_company,
                      'jpk_by_employee' : premi_karyawan, 
                      'jpk_by_company'  : premi_perusahaan,
                      'jkk_amount'      : jkk_amount,
                      'jk_amount'       : jk_amount,
                      'tk_lhk_amount'   : tk_lhk_amount,
                      'total'           : jht_amount+jpk_amount+jkk_amount+jk_amount+tk_lhk_amount,
                      #'contract_wage'   : (contract.wage+contract.advantages_gross + allowance_daily_amount),
                      'kelas'           : kelas,
                      }
            res[rs.id] = record
        return res
    
    def _get_info(self, cr, uid, ids, field_names, arg, context=None):
        res= {}
        for jsostek in self.browse(cr,uid,ids,context):
            emp_id      = jsostek.name.id
            contract_id = self.pool.get('hr.contract').search(cr,uid,[('employee_id','=',emp_id),'|',('date_end','>=',time.strftime("%Y-%m-%d")),('date_end','=',False)])
            if not contract_id:
                raise osv.except_osv(_('No Valid Contract Found!'), _('No valid contract found for this employee!\nPlease create contract for %s first')%(jsostek.name.name,))
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
        if employee_id:
            employee = self.pool.get('hr.employee').browse(cr, uid, employee_id, context=context)
            
            contract_ids = self.pool.get('hr.contract').search(cr, uid, [('employee_id','=',employee_id),('date_start','<=',current_date),'|',('date_end','>=',current_date),('date_end','=',False)])
            if not contract_ids:
                raise osv.except_osv(_('No Valid Contract Found!'), _('No valid contract found for this employee!\nPlease create contract for %s first.')%(employee.name))
            contract = self.pool.get('hr.contract').browse(cr, uid, contract_ids)[0]
            print "contract", contract
            res['jnumber']      = employee.insurance_id or False
            res['contract_id']  = contract.id or False
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
                'department_id' : fields.function(_get_info,method=True,type="many2one",string="Department",obj="hr.department",store=True,multi='dc'),
                #'section_id'    : fields.function(_get_info,method=True,type="many2one",string="Section",obj="hr.section",store=True,multi='dc'),
                'job_id'        : fields.function(_get_info,method=True,type="many2one",string="Job",obj="hr.job",store=True,multi='dc'),
                'current_job_level_id': fields.function(_get_info,method=True,type="many2one",string="Current Job Level",obj="hr.department",store=True,multi='dc'),
                'emp_status'    : fields.char('Employee Status',size=64,readonly=True,states={'draft':[('readonly',False)]}),
                'reg_date'      : fields.date('Registered Date',readonly=True,states={'draft':[('readonly',False)]}),
                'branch_office' : fields.many2one('res.partner','Jamsostek Branch Office'),
                'jht'           : fields.boolean('Jaminan Hari Tua (JHT)',help='Check this box for JHT',required=False,readonly=True,states={'draft':[('readonly',False)]}),
                'jpk'           : fields.boolean('Jaminan Kesehatan',help='Check this box for JPK',readonly=True,states={'draft':[('readonly',False)]}),
                'jkk'           : fields.boolean('Jaminan Kecelakaan Kerja (JKK)',help='Check this box for JKK',states={'draft':[('readonly',False)]}),
                'jk'            : fields.boolean('Jaminan Kematian (JKM)',help='Check this box for JK',readonly=True,states={'draft':[('readonly',False)]}),
                'tk_lhk'        : fields.boolean('Luar Hubungan Kerja',help='Check this box for TK-LHK',readonly=True,states={'draft':[('readonly',False)]}),
                'tax_type'      : fields.selection([('k1','K1'),
                                                    ('k2','K2'),
                                                    ('k3','K3')],'Tax Type'),
                'bank_account'  : fields.char('Bank Account',size=32),
                'note'          : fields.text('Notes'),
                'period_id'     : fields.many2one('account.period','Period',readonly=True,states={'draft':[('readonly',False)]}),
                'contract_wage' : fields.float(string='Take Home Pay', digits_compute=dp.get_precision('Account'), readonly=True),
                'jht_amount'    : fields.function(_calculate, method=True, store=False, multi='dc', string='JHT Amount', digits_compute=dp.get_precision('Account')),
                'jht_by_employee'    : fields.function(_calculate, method=True, store=False, multi='dc', string='JHT by Employee', digits_compute=dp.get_precision('Account')),
                'jht_by_company'     : fields.function(_calculate, method=True, store=False, multi='dc', string='JHT by Company', digits_compute=dp.get_precision('Account')),
                'jpk_by_employee'    : fields.function(_calculate, method=True, store=False, multi='dc', string='JPK by Employee', digits_compute=dp.get_precision('Account')),
                'jpk_by_company'     : fields.function(_calculate, method=True, store=False, multi='dc', string='JPK by Company', digits_compute=dp.get_precision('Account')),
                'jkk_amount'    : fields.function(_calculate, method=True, store=False, multi='dc', string='JKK Amount', digits_compute=dp.get_precision('Account')),
                'jk_amount'     : fields.function(_calculate, method=True, store=False, multi='dc', string='JK Amount', digits_compute=dp.get_precision('Account')),
                'tk_lhk_amount' : fields.function(_calculate, method=True, store=False, multi='dc', string='TK-LHK Amount', digits_compute=dp.get_precision('Account')),
                'total'         : fields.function(_calculate, method=True, store=False, multi='dc', string='Total', digits_compute=dp.get_precision('Account')),
                'kelas'         : fields.function(_calculate, method=True, store=False, multi='dc', string='Class', type='integer'),
                'state'         : fields.selection([('draft','Draft'),('registered','Registered')],'State',readonly=True),
                'employee_number'   : fields.char("NIK", size=64, readonly=True,states={'draft':[('readonly',False)]}),
                'date_from'  : fields.date('Date From', required=True),
                'date_to'    : fields.date('Date To', required=True),
                'allowance_daily_amount' : fields.function(_allowance_daily_amount, method=True, type='float', string='Allowances Daily Amount', digits_compute=dp.get_precision('Payroll'),),
                }
    _defaults ={
                'state'         : 'draft',
                }
    
    def register(self,cr,uid,ids,context=None):
        self.compute(cr, uid, ids, context)
        self.write(cr,uid,ids,{'state':'registered'})
        return True
    
    def cancel(self,cr,uid,ids,context=None):
        self.write(cr,uid,ids,{'state':'draft'})
        return True
hr_bpjs_kes()