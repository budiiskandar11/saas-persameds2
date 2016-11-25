from openerp.osv import fields, osv

class res_company(osv.osv):
    _inherit = 'res.company'

   

    _columns =  {
            'employee_id'	: fields.many2one('hr.employee','Employee'),
    }

   
res_company()