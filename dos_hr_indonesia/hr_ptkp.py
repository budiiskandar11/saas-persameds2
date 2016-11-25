# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools.safe_eval import safe_eval as eval



class hr_ptkp(osv.osv):
    _name		= "hr.ptkp"
    _columns    = {
                   'name' : fields.char('Code'),
                   'describe' : fields.char('Describe'),
                   'amount' : fields.float('Amount'),
                   }
hr_ptkp()

class hr_contract(osv.osv):
    
    def onchange_ptkp_amount(self, cr, uid, ids, ptkp, context=None):
        res = {}
        if ptkp:
            # if ptkp == 'TK':
            #     return {'value': {'amount_ptkp': categ.ptkp_id.amount}}
            # elif ptkp == 'K0':
            #     return {'value': {'amount_ptkp': categ.ptkp_id.amount}}
            # elif ptkp == 'K1':
            #     return {'value': {'amount_ptkp': categ.ptkp_id.amount}}
            # elif ptkp == 'K2':
            #     return {'value': {'amount_ptkp': categ.ptkp_id.amount}}
            # elif ptkp == 'K3':
            #     return {'value': {'amount_ptkp': categ.ptkp_id.amount}}
            # print "RESULT ===", self.pool.get('sale.order').browse(cr,uid,ids,context=context)
            hr_ptkp = self.pool.get('hr.ptkp').browse(cr,uid,ptkp,context=context)
            amount = hr_ptkp.amount
            return {'value':{'amount_ptkp':amount}}

            return res
            print "RESSSSSSSSSS = ",res


    _inherit = "hr.contract"
    _columns = {
                # 'category_ptkp':fields.selection([('tk','TK'),('k0','K0'),('k1','K1'),('k2','K2'),('k3','K3')],'PTKP',),
                'ptkp_id':fields.many2one('hr.ptkp','PTKP'),
                #'amount_ptkp':fields.float('Amount PTKP'),
                'amount_ptkp' : fields.related('ptkp_id', 'amount', type='float', string='Amount PTKP', readonly=True),
                }
hr_contract()
