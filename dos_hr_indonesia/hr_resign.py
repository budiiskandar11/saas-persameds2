# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014, Databit Solusi Indonesia
#    Author : Budi Iskandar (budiiskandar@databit.co.id)
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

class hr_resign(osv.osv):
    _name = "hr.resign"
    _columns = {
                 
                'user_id'           : fields.many2one('res.users', 'Created By'),
                'date'              : fields.date('Date'),
                'employee_id'       : fields.many2one('hr.employee', 'Employee'),
                'contract_id'       : fields.many2one('hr.contract', 'Contract/SPK Reference'),
                'reason'            : fields.text('Reason'),
                'attach'            : fields.binary('Attachment'),
                'state'             : fields.selection([
                                            ('draft','Draft'),
                                            ('confirm','Confirm'),
                                            ('approve','Approve'),
                                            ('verify','Verified'),
                                            ],'State'),
                'name'              : fields.char('Name'),
                'date_confirm'      : fields.date('Confirm Date', readonly=True, select=True),
                'date_approval'     : fields.date('Approval Date', readonly=True, select=True),
                'date_verified'     : fields.date('Approval Date', readonly=True, select=True),
                'new_contract_id'   : fields.many2one('hr.contract','New Contract/SPK'),
                'asset_return'      : fields.boolean ('Fix Asset Return',helps='Centang Jika Karyawan sudah mengembalikan Fix Asset'),
                'bpjs_nonactive'    : fields.boolean ('BPJS NonActive'),
                'department_id'     : fields.related('employee_id', 'department_id', string='Department', type='many2one', relation='hr.department', readonly=True, store=True),
                'job_id'            : fields.related('employee_id', 'job_id', string='Job Title', type='many2one', relation='hr.job', readonly=True, store=True),
               
                
              }
    _defaults = {
    			'user_id' :lambda self, cr, uid, context=None: uid,
                'state'     : 'draft',
    }
 
    
    def action_wait_approval(self, cr, uid, ids, context=None):
        for o in self.browse(cr, uid, ids):
            #noprod = self.test_no_product(cr, uid, o, context)
            employee_obj = self.pool.get('hr.employee')
            if (o.state == 'draft'):
                self.write(cr, uid, [o.id], {'state': 'confirm', 'date_confirm': fields.date.context_today(self, cr, uid, context=context)})
            elif (o.state == 'confirm'):
                
                date = time.strftime('%Y-%m-%d') or False
                if o.contract_id:
                    val = {
                        'name'              : '/',
                        'type_id'           : o.contract_id.type_id.id or False,
                        'employee_id'       : o.employee_id.id or False,
                        'employee_status'   : 'resign',
                        'wage'              : o.contract_id.wage or 0.0,
                        'struct_id'         : o.contract_id.struct_id.id or False,
                        'date_start'        : o.contract_id.date_start or False,
                        'date_end'          : date,
                    }
                    new_id = self.pool.get('hr.contract').create(cr,uid,val)
                    self.write(cr,uid,[o.id],{'new_contract_id':new_id})
                self.write(cr, uid, [o.id], {'state': 'approve', 'date_approval': fields.date.context_today(self, cr, uid, context=context)})
            elif (o.state == 'approve'):
                self.write(cr, uid, [o.id], {'state': 'verify', 'date_verified': fields.date.context_today(self, cr, uid, context=context)})
                
                employee_obj.write(cr,uid,[o.employee_id.id],{'state_id':'resign'})
                
        return True        
    
hr_resign()