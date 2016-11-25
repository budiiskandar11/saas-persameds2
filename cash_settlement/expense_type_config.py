
import time
from lxml import etree
from openerp import SUPERUSER_ID, netsvc, api
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class expense_type(osv.osv):
    _name  = 'expense.type'
    _description = 'Tipe advance related dengan account'
    _columns    = {
                   'name'   : fields.char('Name', required =True),
                   'code'   : fields.char('Code'),
                   'account_id' : fields.many2one('account.account', 'Account Advance', required=True)
                   
                   }
    
expense_type()