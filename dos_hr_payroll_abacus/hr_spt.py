from openerp.osv import fields,osv

class hr_spt(osv.osv):
    _name = "hr.spt"
    _columns = {
        'name':fields.char('Task Name',size=64,required=True),
        'department_id':fields.many2one('hr.department','Department'),
#         'source_id':fields.many2one('res.partner.address','From'),
        'partner_id':fields.many2one('res.partner',"Partner"),
#         'destination_id':fields.many2one('res.partner.address',"Destination"),
        'date_from':fields.date("Start Date", required=True),
        'date_to':fields.date("End Date",required=True),
        'spt_lines':fields.one2many('hr.spt.lines','spt_id',"Assigned Employee"),
        'state':fields.selection([('draft',"Draft"),("cancel","Cancelled"),("approved","Approved")],"State",readonly=True)
        }
    _defaults = {
        'state':'draft'
                 }
    
    def button_proposed(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'approved'},context)
    
    def button_draft(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'draft'},context)
    
    def button_cancel(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'cancel'},context)

hr_spt()

class hr_spt_lines(osv.osv):
    _name = "hr.spt.lines"
    _columns = {
        'spt_id':fields.many2one('hr.spt',"SPT Number"),
        'employee_id':fields.many2one('hr.employee',"Employee",required=True),
        'description':fields.text("Description"),
                }

hr_spt_lines()

