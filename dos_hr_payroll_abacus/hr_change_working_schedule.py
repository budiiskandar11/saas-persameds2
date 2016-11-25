from openerp.osv import fields,osv
from datetime import date

class hr_substitute_working_schedule(osv.osv):
    _name = "hr.substitute.working.schedule"
    _columns = {
        'name':fields.many2one('hr.employee',"Employee",required=True),
        'substitution':fields.boolean("Substitution",help="Checked if the schedule is substituted with other Employee"),
        'contract_id':fields.many2one('hr.contract',"Active Contract",required=True),
        'substitution_date':fields.date('Substitution Date',required=True),
        'substituen_id':fields.many2one('hr.employee',"Substituent Employee"),
        'substituen_contract_id':fields.many2one('hr.contract',"Active Contract"),
        'hour_from' : fields.float('Work from', size=8,  help="Working time will start from", select=True),
        'hour_to' : fields.float("Work to", size=8, help="Working time will end at"),
        'propose_id' : fields.many2one('hr.employee',"Proposed by",required=True),
        'state':fields.selection([('cancel','Cancelled'),('draft','Draft'),('proposed','Proposed'),('approved',"Approved")],"State",readonly=True),
                }
    _defaults={
        'state':'draft',
        
               }
    
    def button_proposed(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'proposed'},context)
    
    def button_cancel(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'cancel'},context)
    
    def button_draft(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'draft'},context)
    
    def button_approved(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'approved'},context)
    
    def onchange_substitution(self,cr,uid,ids,substitution=False,substituen_id=False,substituen_contract_id=False,hour_from=False,hour_to=False,context=None):
        value={
               'substitution':substitution,
               'substituen_id':substituen_id,
               'substituen_contract_id':substituen_contract_id,
               'hour_from':hour_from,
               'hour_to':hour_to,
               }
        if not context:
            context={}
        if substitution:
            value.update({'hour_from':False,'hour_to':False})
        else:
            value.update({'substituen_id':False,'substituen_contract_id':False})
        return {'value':value}
    
    def onchange_name(self,cr,uid,ids,emp_id,context=None):
        if not context:
            context={}
        value={'contract_id':False}
        if emp_id:
            emp_data=self.pool.get('hr.employee').browse(cr,uid,emp_id,context=context)
            start_date=date.today()
            contract_id=self.pool.get('hr.payslip').get_contract(cr,uid,emp_data,start_date,False,context)
            if contract_id:
                value.update({'contract_id':contract_id[0]})
        return {'value':value}
    
    def onchange_substituen(self,cr,uid,ids,emp_id,context=None):
        if not context:
            context={}
        value={'substituen_contract_id':False}
        if emp_id:
            emp_data=self.pool.get('hr.employee').browse(cr,uid,emp_id,context=context)
            start_date=date.today()
            contract_id=self.pool.get('hr.payslip').get_contract(cr,uid,emp_data,start_date,False,context)
            if contract_id:
                value.update({'substituen_contract_id':contract_id[0]})
        return {'value':value}
        
hr_substitute_working_schedule()