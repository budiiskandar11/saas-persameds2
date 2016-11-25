import itertools
import logging
from functools import partial
from itertools import repeat

from lxml import etree
from lxml.builder import E

import openerp
from openerp import SUPERUSER_ID, models
from openerp import tools
import openerp.exceptions
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from openerp.http import request

_logger = logging.getLogger(__name__)

class res_users(osv.osv):
    _inherit = "res.users"
    
    _columns = {
            'force_period' : fields.boolean('Force Period Allow'),
                }
    
res_users()