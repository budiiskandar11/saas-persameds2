from openerp.osv import osv,fields
from openerp.addons import decimal_precision as dp
from openerp.tools.translate import _
import datetime
from datetime import date
from openerp import tools
import time


class hr_dplk(osv.osv):
    _name = "hr.dplk"
    _description = "DPLK"
   
    def compute(self, cr, uid, ids, context=None):
        for val in self.browse(cr, uid, ids, context=None):
            ##Write THP##
            contract_wage = val.contract_id.wage
        self.write(cr, uid, ids, {'contract_wage': contract_wage})
   
    def _calculate(self, cr, uid, ids, field_names, arg, context=None):
        res = {}
        jht_amount      = 0
        jpk_amount      = 0
        jkk_amount      = 0
        jk_amount       = 0
        tk_lhk_amount   = 0
        
        dplk_by_employee    = 0.0
        dplk_by_company     = 0.0
        dplk_amount         = 0.0
        
        married         =['married','sudah menikah','menikah','berkeluarga']
            
        for rs in self.browse(cr, uid, ids, context=context):
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
            
            total_umr = 0.0
            if rs.dplk:
                dplk_amount     = (rs.contract_wage)*0.1
                dplk_by_employee= (rs.contract_wage)*0.025
                dplk_by_company = (rs.contract_wage)*0.075
                
                
            ###########
            
            #print "jht_amount+jpk_amount+jkk_amount+jk_amount+tk_lhk_amount", jht_amount+jpk_amount+jkk_amount+jk_amount+tk_lhk_amount
            
            record = {
                      'dplk_by_employee' : dplk_by_employee,
                      'dplk_by_company' : dplk_by_company,
                      'total'           : dplk_amount,
                      #'contract_wage'   : (contract.wage),
                      #'kelas'           : kelas,
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
        if employee_id:
            employee = self.pool.get('hr.employee').browse(cr, uid, employee_id, context=context)
            
            #contract_ids = self.pool.get('hr.contract').search(cr, uid, [('employee_id','=',employee_id),('date_start','<=',period.date_start),'|',('date_end','>=',period.date_start),('date_end','=',False)])
            #if not contract_ids:
            #    raise osv.except_osv(_('No Valid Contract Found!'), _('No valid contract found for this employee!\nPlease create contract for this employee first.'))
            #contract = self.pool.get('hr.contract').browse(cr, uid, contract_ids)[0]
            
            res['jnumber']      = employee.insurance_id or False
            #res['contract_id']  = contract.id or False
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
                'jnumber'       : fields.char('DPLK Number',size=32,required=True,readonly=True, states={'draft':[('readonly',False)]}),
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
                'dplk'           : fields.boolean('DPLK',help='Check this box for JHT',required=False,readonly=True,states={'draft':[('readonly',False)]}),
                
                'tax_type'      : fields.selection([('k1','K1'),
                                                    ('k2','K2'),
                                                    ('k3','K3')],'Tax Type'),
                'bank_account'  : fields.char('Bank Account',size=32),
                'note'          : fields.text('Notes'),
                'period_id'     : fields.many2one('account.period','Period',readonly=True,states={'draft':[('readonly',False)]}),
                'contract_wage' : fields.float(string='Take Home Pay', digits_compute=dp.get_precision('Account'), readonly=True),
                
                'dplk_by_employee'    : fields.function(_calculate, method=True, store=False, multi='dc', string='JPK by Employee', digits_compute=dp.get_precision('Account')),
                'dplk_by_company'     : fields.function(_calculate, method=True, store=False, multi='dc', string='JPK by Company', digits_compute=dp.get_precision('Account')),
                
                'total'         : fields.function(_calculate, method=True, store=False, multi='dc', string='Total', digits_compute=dp.get_precision('Account')),
                'employee_number'   : fields.char("NIK", size=64, readonly=True,states={'draft':[('readonly',False)]}),
                'state'         : fields.selection([('draft','Draft'),('registered','Registered')],'State',readonly=True),
                'date_from'  : fields.date('Date From', required=True),
                'date_to'    : fields.date('Date To', required=True),
                
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
hr_dplk()