##############################################################################
#
#    Copyright (C) 2009 Almacom (Thailand) Ltd.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields
import time

class letter_credit(osv.osv):
    _name = "letter.credit"
    _description = "Letter Credit"
    _columns = {
                'name'          : fields.char('Name'),
                'partner_id'    : fields.many2one('res.partner','Partner'),
                'currency_id'   : fields.many2one('res.currency','Currency'),
                'bank_name'     : fields.char('Bank Name'),
                'purchase_id'   : fields.many2one('purchase.order','Purchase'),
#                 'date_create'   : fields.date('Date'),
                'date_paid'     : fields.date('Date Paid'),
                'amount'        : fields.float('Amount'),
                'user_id'       : fields.many2one('res.users','Responsible'),
                'company_id'    : fields.many2one('res.company','Company'),
                'note'          : fields.text('Notes'),
                'state'         : fields.selection([('cancelled','Cancelled'),
                                                    ('draft','Draft'),
                                                    ('proposed','Proposed'),
                                                    ('paid','Paid')],'State',readonly=True),
                'create_date'   : fields.date('Create Date'),
                'voucher_id'    : fields.many2one('account.voucher','Voucher'),
                }
    _defaults = {
                'user_id'          : lambda self,cr,uid,context: uid,
                'state'            : 'draft',
                 }
    
    def button_draft(self,cr,uid,ids,context):
        self.write(cr,uid,ids,{'state':'draft'})
        return True
    
    def button_proposed(self,cr,uid,ids,context):
        self.write(cr,uid,ids,{'state':'proposed'})
        return True
        
    def button_cancel(self,cr,uid,ids,context):
        self.write(cr,uid,ids,{'state':'cancelled'})
        return True
letter_credit()