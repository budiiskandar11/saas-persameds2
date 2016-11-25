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

class account_check(osv.osv):
    
    def _compute_check(self, cr, uid, ids, name, args, context=None):
        if context is None:
            return {}
        res= {}
        for ch in self.browse(cr, uid, ids, context=context):#[0].check_id:
            res[ch.id] = {
                'total_check': 0.0
            }
            if ch.check_id:
                for lch in ch.check_id:
                    res[ch.id]['total_check'] += lch.amount
            res[ch.id]['total_check'] = res[ch.id]['total_check']
        return res
    
    def _compute_check2(self, cr, uid, ids, name, args, context=None):
        if context is None:
            return {}
        res={}
        for ch in self.browse(cr, uid,ids,{'state':'hold'}):#[0].check_id:
            res[ch.id] = {
                'total_check2': 0.0
            }
            if ch.check_id:
                for lch in ch.check_id:
                    res[ch.id]['total_check2'] += lch.amount
            res[ch.id]['total_check2'] = res[ch.id]['total_check2']
        return res

    _name ="account.check"
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _columns = {
        "name":fields.char ("Giro Receive No", size=24, required=True),
        "dates": fields.date("Receive Date"),
        "user_id": fields.many2one("res.users","Receive by"),
        "partner_id": fields.many2one("res.partner", "Partner"),
        "bank_id": fields.many2one("res.bank", "Bank"),                
        "check_id": fields.one2many("account.check.line","check_id","List check"),
        "voucher_id": fields.many2one("account.voucher","Transaction Number"),
        "memo": fields.text("Memo"),
        "branch": fields.char("Branch", size=64),
        "qty": fields.float("Qty (Pcs)"),
        "type": fields.selection([("check", "Cheque"), ("giro", "Giro")], "Type", readonly=True, select=1),
        "state": fields.selection([("draft", "Draft"), ("confirm", "Confirm"), ("used", "Used"),("cancel", "Canceled")], "State", readonly=True, required=True, select=1),
        'total_check': fields.function(_compute_check, method=True, multi='dc', type='float', string='Total', store=True),
        'total_check2': fields.function(_compute_check2, method=True, multi='dc', type='float', string='Residual Cheque', store=False),
    }
    _defaults = {
        "type": lambda self, cr, uid, context: context.get("type", "check"),
        "dates": lambda * a: time.strftime("%Y-%m-%d"),
        "state":"draft",
        'name': '/',
    }
    
    def set_to_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'draft'})
        return True
    
    def cancel_check(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'cancel'})
        return True
    
    def confirm_check(self, cr, uid, ids, context=None):
        for check in self.browse(cr, uid, ids):
            self.write(cr, uid, ids, {'state':'confirm','name':self.pool.get('ir.sequence').get(cr, uid, check.type)})
        return True
    
    def onchange_voucher_id(self, cr, uid, ids, voucher_id, context=None):
        partner_id = False
        if voucher_id:
            partner_id = self.pool.get('account.voucher').browse(cr, uid, voucher_id, context=context).partner_id.id
        return {'value': {'partner_id': partner_id}}
   
account_check()


class account_check_line(osv.osv):
    _name = "account.check.line"
    _description = 'List Cheque'
    _columns = {
        'check_id': fields.many2one('account.check', 'Giro Number',),       
        "name": fields.char("Giro No", size=64, required=True, readonly=True, states={"hold":[("readonly", False)]}, select=2),
        "voucher": fields.char('Number Payment', size=32, required=False, readonly=True, states={"hold":[("readonly", False)]}),
        "type": fields.related('check_id','type',type='char', string='Type', store=True),
        "type_voucher": fields.selection([("receipt", "Receipt"), ("payment", "Payment")], "Type Voucher", required=False, readonly=True, states={"hold":[("readonly", False)]}, select=1),
        "method": fields.selection([("paper", "Paper"), ("elec", "Electronic")], "Method", required=False, readonly=True, states={"hold":[("readonly", False)]}, select=1),
        "date": fields.date("Giro Date", required=False, readonly=True, states={"hold":[("readonly", False)]}, select=2),
        "date_end": fields.date("Giro End Date", required=True, readonly=True, states={"hold":[("readonly", False)]}, select=2),
        #"voucher_id": fields.many2one("account.voucher", "Payment", required=True, readonly=True, states={"hold":[("readonly", False)]}, select=1),
        #"partner_id": fields.many2one("res.partner", "Partner", required=True, readonly=True, states={"hold":[("readonly", False)]}, select=1),
        "amount": fields.float("Amount", required=True, readonly=True, states={"hold":[("readonly", False)]}, select=2),
        "bank_id": fields.many2one("res.bank", "Bank", required=False, readonly=True, states={"hold":[("readonly", False)]}, select=2),
        "branch": fields.char("Branch", size=64, readonly=True, states={"hold":[("readonly", False)]}, select=2),
        "state": fields.selection([("hold", "Hold"), ("released", "Released"), ("paid", "Paid"), ("end", "Canceled")], "State", readonly=True, required=True, select=1),
        #"vouch_id": fields.many2one("account.voucher", "Voucher", required=False, readonly=True, states={"hold":[("readonly", False)]}, select=2),
    }

    _defaults = {
        "type_voucher": lambda self, cr, uid, context: context.get("type_voucher", "payment"),
        "method": lambda * a: "paper",
        "state": lambda * a: "hold",
        "date": lambda * a: time.strftime("%Y-%m-%d"),
    }
    def button_released(self, cr, uid, ids, context={}):
        for chk in self.browse(cr, uid, ids):
            chk.write({"state":"released"})
        return True

    def button_cancel(self, cr, uid, ids, context={}):
        for chk in self.browse(cr, uid, ids):
            chk.write({"state":"end"})
        return True

    def button_paid(self, cr, uid, ids, context={}):
        for chk in self.browse(cr, uid, ids):
            chk.write({"state":"paid"})
        return True

    def onchange_method(self, cr, uid, ids, method):
        vals = {
            "name": method == "elec" and "1" or "",
        }
        return {"value": vals}
account_check_line()


