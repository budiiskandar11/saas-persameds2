import datetime
import time
from lxml import etree
import math
import pytz
import re

import openerp
from openerp import SUPERUSER_ID
from openerp import pooler, tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.tools.yaml_import import is_comment

class task_delegate(osv.osv):
    _name= 'task.delegate'
    
    _columns = {
            'name'          : fields.char('Subject', size=128,),
            'created_by'    : fields.many2one('res.users', 'Created by'),
            'department_created_by'    : fields.many2one('hr.department', 'Department'),
            'employee_id'   : fields.many2one('hr.employee', 'Delegate to'),
            'delegate_date' : fields.date('Delegate Date'),
            'department_id' : fields.related('employee_id', 'department_id', string='Unit', type='many2one', relation='hr.department', readonly=True),
            'task_list'     : fields.one2many('task.list','task_delegate_id', 'Task List'),
            'state'         : fields.selection([('draft', 'New Task'),('confirm', 'Task Delegated'), 
                                                ('done', 'Done'), ('cancel', 'Cancelled')],'State'),
            'note'          : fields.text('Notes'),
            'company_id'    : fields.many2one('res.company', 'Company', readonly=True),
                }
    
    def create_task_list(self, cr, uid, ids, daily_id):
        print ">>>>create_task_list>>>>>>>>>>>>>>."
        todo_object = self.pool.get('task.list.todo')
        
        for assign in self.browse(cr, uid, ids, context=None):
            for assign_line in assign.task_list:
                todo_line = {
                        'name'      : assign_line.name,
                        'deadline'  : assign_line.deadline,
                        'note'      : assign_line.note,
                        'daily_id'  : daily_id,
                        'state'     : 'draft',
                            }
                todo_object.create(cr, uid, todo_line)
        return True
    
    def assign_task(self, cr, uid, ids, context=None):
        dar_object = self.pool.get('daily.activity.report')
        dar_line_object = self.pool.get('daily.activity.line')
        
        for assign in self.browse(cr, uid, ids, context=None): 
###Create Task in DAR####
#             dar_val = {
#                     'name'          : assign.name,
#                     'employee_id'   : assign.employee_id.id,
#                     'date'          : assign.delegate_date,
#                     'state'         : 'draft',
#                        }
#             daily_id = dar_object.create(cr, uid, dar_val)
#             for assign_line in assign.task_list:
#                 dar_val_line = {
#                             'name'          : assign_line.name,
#                             'daily_id'      : daily_id,
#                             #'task_line_id'  : assign_line.id,
#                             'state'         : 'draft',
#                                 }
#                 dar_line_object.create(cr, uid, dar_val_line)
                
            template_id = self.pool.get('email.template').search(cr, uid, [('model_id','=','task.delegate')])[0]
            if template_id:
                print "XXXXXXXXXXXXX", template_id, ids[0]    
                self.pool.get('email.template').send_mail(cr, uid, template_id, ids[0],True, context=context)
            
            #self.create_task_list(cr, uid, ids, daily_id)
            self.write(cr, uid, ids, {'state' : 'confirm'})
        return True
    
    def cancel_task(self, cr, uid, ids, context=None):
        for assign in self.browse(cr, uid, ids, context=None): 
            self.write(cr, uid, ids, {'state' : 'cancel'})
        return True
    
    def set_to_draft(self, cr, uid, ids, context=None):
        for assign in self.browse(cr, uid, ids, context=None): 
            self.write(cr, uid, ids, {'state' : 'draft'})
        return True
    
    def onchange_created_by(self, cr, uid, ids, created_by):
        print "XXXXXXXXXXXX", created_by
        val = {}
        employee_obj = self.pool.get('hr.employee')
        
        
        employee_search = employee_obj.search(cr, uid, [('user_id','=',created_by)])
        print "employee_search", employee_search
        department_created_by = employee_obj.browse(cr, uid, employee_search)[0].department_id.id
        
        print "department_created_by", department_created_by
        
        val = {
               'department_created_by'  : department_created_by
               }
        
        return {'value' : val}
    
    _defaults = {
            'created_by'    : lambda self, cr, uid, context: uid,
            'state'         : 'draft',
            'delegate_date' : lambda *a:time.strftime('%Y-%m-%d'),
            'company_id'    : lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'hr.employee', context=c),
                 }
task_delegate()

class task_list(osv.osv):
    _name= 'task.list'
    
    _columns = {
            'category_id'       : fields.many2one('daily.activity.category','DAR Category'),
            'name'              : fields.char('Task Description', size=256,),
            'employee_id'       : fields.related('task_delegate_id', 'employee_id', string='Employee', type='many2one', relation='hr.employee', readonly=True, store=True),
            'task_delegate_id'  : fields.many2one('task.delegate', 'Task Delegate'),
            'deadline'          : fields.date('Deadline'),
            'state'             : fields.selection([('draft', 'On Progress'), ('done', 'Done'), ('cancel', 'Cancelled')],'State'),
            'note'              : fields.text('Notes'),
            'daily_lines'       : fields.one2many('daily.activity.line','task_list_id','Daily Report Lines'),
                }
    
    _defaults = {
            'state'         : 'draft',
                 }
    
task_list()