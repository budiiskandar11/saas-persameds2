import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time

import openerp
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round
from openerp.tools.safe_eval import safe_eval as eval

import openerp.addons.decimal_precision as dp

class account_journal(osv.osv):
    _inherit = "account.journal"
    
    _columns = {
            #'distrik_id'            : fields.many2one('hr.distrik', "District"),
            'stock_mit_account'     : fields.many2one('account.account', "Transit Account"),
    }

account_journal()