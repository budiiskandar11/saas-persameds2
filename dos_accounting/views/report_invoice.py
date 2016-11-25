from openerp.addons.report_webkit.webkit_report import webkit_report_extender
from openerp import SUPERUSER_ID

import openerp
import time
from openerp.report import render,report_sxw
from openerp.report.interface import report_int
import openerp.tools as tools
from openerp.report import render
from lxml import etree

import time, os

from openerp.addons.dos_amount2text_idr import amount_to_text_id
import itertools
from lxml import etree

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp
from openerp.osv import osv,fields


    
class account_invoice(osv.osv):
      _inherit = "account.invoice"
      
      @api.multi
      def amount_to_text_id(self, amount, currency='IDR'):
          return amount_to_text_id(amount, currency="Rupiah")


account_invoice()