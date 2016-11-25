from openerp.osv import fields, osv

class res_company(osv.osv):
    _inherit = 'res.company'

   

    _columns =  {
            'npp' 			: fields.char('NPP', size= 16),
    }

   
res_company()