import time
from lxml import etree

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp.tools import float_compare
from openerp.report import report_sxw
import openerp

class account_voucher(osv.osv):
    _inherit="account.voucher"
    _columns = {
        'invoice_name': fields.related('line_ids','name',type='char',string='Invoice',readonly=True),
    }