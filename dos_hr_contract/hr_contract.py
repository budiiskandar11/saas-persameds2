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
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

class hr_contract(osv.osv):
	_inherit = 'hr.contract'
	_columns = {
		'employee_status' : fields.selection([
			('ojt','OJT'),
			('active','Tetap'),
			('resign','Resigned'),
			('terminate','Terminated'),
			('pension','Pension')
			],'Type'),
		'state' : fields.selection([
			('draft','Draft'),
			('confirm','Confirm'),
			('approve','Approve')
			],'State'),
		'date_confirm': fields.date('Confirm Date', readonly=True, select=True),
        'date_approval': fields.date('Approval Date', readonly=True, select=True),
        
        'renewal_type'	: fields.selection([('kenaikan', 'Kenaikan Grade'), 
                                               ('demosi', 'Demosi'),
                                               ('pengangkatan', 'Pengangkatan Tetap'),
                                               ('promosi', 'Promosi'),
                                               ('phk', 'PHK'),
                                               ], 'Renewal Type'),
        'prev_contract' : fields.many2one('hr.contract','Previous Contract'),
        
		}

	_defaults = {
		'state' : 'draft',
	}

	def action_wait_approval(self, cr, uid, ids, context=None):
	        for o in self.browse(cr, uid, ids):
	            #noprod = self.test_no_product(cr, uid, o, context)
	            if (o.state == 'draft'):
	                self.write(cr, uid, [o.id], {'state': 'confirm', 'date_confirm': fields.date.context_today(self, cr, uid, context=context)})
	            elif (o.state == 'confirm'):
	            	employee = self.pool.get('hr.employee')
	            	if (o.employee_status == 'ojt'):
	            		employee.write(cr,uid,[o.employee_id.id],{'state_id':'draft'})
	            	elif (o.employee_status == 'active'):
	            		employee.write(cr,uid,[o.employee_id.id],{'state_id':'active'})
	            	elif (o.employee_status == 'resign'):
	            		employee.write(cr,uid,[o.employee_id.id],{'state_id':'resign'})
	            	elif (o.employee_status == 'terminate'):
	            		employee.write(cr,uid,[o.employee_id.id],{'state_id':'terminate'})
	            	elif (o.employee_status == 'pension'):
	            		employee.write(cr,uid,[o.employee_id.id],{'state_id':'pension'})
	                self.write(cr, uid, [o.id], {'state': 'approve', 'date_approval': fields.date.context_today(self, cr, uid, context=context)})
	        return True

	def modify(self, cr, uid, ids, context=None):
		res = {}
		if context==None:
			context = context
		self.write(cr, uid, ids, {'state':'draft'})
		return True


hr_contract()