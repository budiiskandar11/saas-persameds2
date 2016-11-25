from openerp.osv import fields,osv

class hr_employee_level(osv.osv):
    _name = "hr.employee.level"
    _columns = {
        'name':fields.char("Level Name",size=32,required=True),
        "parent_id":fields.many2one("hr.employee.level","Parent Level"),
        "description":fields.text("Description"),
                }
hr_employee_level()

class hr_employee(osv.osv):
    _inherit="hr.employee"
    _columns = {
        'level_id':fields.many2one("hr.employee.level","Level ID"),
        }
hr_employee()