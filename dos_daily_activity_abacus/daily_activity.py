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

class daily_activity_category(osv.osv):
    _name = 'daily.activity.category'
    
    _columns = {
            'code'      : fields.char('Code',size=256),
            'job_id' : fields.many2one('hr.job', 'Job Position'),
            'name'      : fields.char('Category Name',size=256),
                }
    
daily_activity_category()


class daily_activity(osv.osv):
    _name       = 'daily.activity.report'
    
    def _line_count(self, cr, uid, ids, field_name, arg, context):
        res = {}
        count = 0.0
        for val in self.browse(cr, uid, ids):            
            for line in val.daily_lines:
                count += 1
            for line in val.daily_lines2: 
                count += 1
            res[val.id] = count
        return res
    
    def _line_count_time(self, cr, uid, ids, field_name, arg, context):
        res = {}
        count = 0.0
        for val in self.browse(cr, uid, ids):            
            for line in val.daily_lines:
                time = line.time_end - line.time_start 
                count += time
                
            for line in val.daily_lines2:
                time = line.time_end - line.time_start 
                count += time
            
            res[val.id] = count
        return res
    
    def _get_task_list_todo(self, cr, uid, ids, field_names, arg=None, context=None):
        result  = {}
        data    = []
        if not ids: return result
        
        #cr.execute('''SELECT pl.slip_id, pl.id FROM hr_payslip_line AS pl \
        #            LEFT JOIN hr_salary_rule_category AS sh on (pl.category_id = sh.id) \
        #            WHERE pl.slip_id in %s \
        #            GROUP BY pl.slip_id, pl.sequence, pl.id ORDER BY pl.sequence''',(tuple(ids),))
        
        daily = self.browse(cr, uid, ids, context)
        for e in daily:
            cr.execute('SELECT id FROM task_delegate WHERE employee_id = %s', (e.employee_id.id,))
            delegate_id = tuple(map(lambda x: x[0], cr.fetchall()))
            
            if not delegate_id:
                return result
            
        cr.execute('SELECT id, name, deadline, note, state FROM task_list WHERE task_delegate_id in %s and state not in %s', (delegate_id, ("done", "cancel"),))
        
        res = cr.fetchall()
        for r in res:
            print "r[0]????????????????????????", r[0]
            
            data.append(int(r[0]))
            
        
        result[e.id] = data
            
            
        print "result>>>>>>>>>>>>>>>>>>>", result
        return result
    
    _columns    = {
                    'name'          : fields.char('Summary',size=256,required=True),
                    'date'          : fields.date('Date'),
                    'employee_id'   : fields.many2one('hr.employee','Employee',readonly=False),
                    'department_id' : fields.related('employee_id', 'department_id', string='Unit', type='many2one', relation='hr.department', readonly=True),
                    'daily_lines'   : fields.one2many('daily.activity.line','daily_id','Daily Report Lines'),
                    'daily_lines2'  : fields.one2many('daily.activity.line','daily_id2','Daily Report Lines'),
                    #'task_list_todo': fields.one2many('task.list.todo','daily_id','Daily Report Lines'),
                    
                    'task_list_todo': fields.function(_get_task_list_todo, method=True, 
                                                        type='one2many', relation='task.list', string='Daily Report LinesXXX'),
                    
                    #'activity_number'   : fields.function()
                    'activity_number': fields.function(_line_count, method=True, string='Activity Number', type='integer', ),
                    'activity_time' : fields.function(_line_count_time, method=True, string='Activity Time', type='float', ),
                    'job_id' : fields.many2one('hr.job', 'Job Position'),
                    
                   }
    
    def onchange_employee_id(self, cr, uid, ids, employee_id, context=None):
        res     = {}
        job_id  = False
        if employee_id:
            print "employee_id----------->>", employee_id
            for val in self.pool.get('hr.employee').browse(cr, uid, [employee_id], context=None):
                print "VAL------------->>", val.id
                print "NAME------------->>", val.name
                job_id = val.job_id.id or False
            
                res = {'job_id' : job_id}
        return {'value' : res}
    
    _defaults   =   {
                     'employee_id'   : lambda self, cr, uid, c: self.pool.get('hr.employee')._employee_default_get(cr, uid, 'daily.activity', context=c),
                     #'employee_id'      : lambda self, cr, uid, context: uid,
                     'date'         : lambda *a: time.strftime('%Y-%m-%d'),
                     }
daily_activity()

class task_list_todo(osv.osv):
    _name= 'task.list.todo'
    
    _columns = {
            'name'              : fields.char('Task Description', size=256,),
            'daily_id'          : fields.many2one('daily.activity.report','Daily Report'),
            'deadline'          : fields.date('Deadline'),
            'state'             : fields.selection([('draft', 'On Progress'), ('done', 'Done'), ('cancel', 'Cancelled')],'State'),
            'note'              : fields.text('Notes'),
                }
    
    _defaults = {
            'state'         : 'draft',
                 }
    
task_list_todo()

class daily_activity_line(osv.osv):
    _name       = 'daily.activity.line'
    
    def _get_date(self, cr, uid, ids, field_name, arg, context):
        res = {}
        date = False
        for val in self.browse(cr, uid, ids):
            if val.daily_id:
                date = val.daily_id.date
            elif val.daily_id2:
                date = val.daily_id2.date
            
            res[val.id] = date
        return res
    
    _columns    = {
                    'task_list_id'  : fields.many2one('task.list','Task Delegated','Task List', ondelete='cascade'),
                    'category_id'  : fields.many2one('daily.activity.category','DAR Category'),
                    'name'      : fields.char('Description Task',size=256,required=True),
                    'date'      : fields.function(_get_date, method=True, string='Date', type='date', ),
                    'date_start': fields.datetime('Time Start'),
                    'date_end'  : fields.datetime('Time End'),
                    'time_start': fields.float('Start'),
                    'time_end'  : fields.float('End'),
                    'activity'  : fields.char('Activity', size= 256),
                    'result'    : fields.char('Result', size= 256),
                    'follow_up' : fields.char('Follow_Up', size= 256), 
                    'note'      : fields.text('Note'),
                    'state'     : fields.selection([('draft', 'On Progress'), ('done', 'Done'), ('cancel', 'Cancelled')],'State'),
                    'daily_id'  : fields.many2one('daily.activity.report','Daily Report'),
                    'daily_id2'  : fields.many2one('daily.activity.report','Daily Report'),
                    'task_line_id'      : fields.many2one('task.list','Task Line'),
                   }
    _defaults   =   {
                     'state'         : 'draft',
                     'date_start'    : lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
                     }
    
    def task_done(self, cr, uid, ids, context=None):
        task_list_obj = self.pool.get('task.list')
        for val in self.browse(cr, uid, ids, context=None):
            if val.task_list_id:
                task_list_obj.write(cr, uid,val.task_list_id.id, {'state' : 'done'})
            self.write(cr, uid,ids, {'state' : 'done'})
        return True
    
    def task_cancel(self, cr, uid, ids, context=None):
        task_list_obj = self.pool.get('task.list')
        for val in self.browse(cr, uid, ids, context=None):
            if val.task_list_id:
                task_list_obj.write(cr, uid,val.task_list_id.id, {'state' : 'draft'})
            self.write(cr, uid,ids, {'state' : 'draft'})
        return True
    
daily_activity_line()