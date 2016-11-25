from openerp.addons.report_webkit.webkit_report import webkit_report_extender
from openerp import SUPERUSER_ID
import time
from openerp import models, fields, api, _
from openerp.report import report_sxw
from openerp.addons.dos_amount2text_idr import amount_to_text_id
from openerp.tools import amount_to_text


@webkit_report_extender("dos_accounting.report_payment_request")
def extend_demo(pool, cr, uid, localcontext, context):
    admin = pool.get("res.users").browse(cr, uid, SUPERUSER_ID, context)
      
  
    localcontext.update({
        "admin_name": admin.name,
        "convert" : convert,
    })
    
def convert(self, amount_total, cur):
        amt_id = dos.amount2text_idr.amount_to_text(self, cr, uid, 'id', cur)
        return amt_id


