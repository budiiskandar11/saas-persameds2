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
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools.safe_eval import safe_eval as eval

class hr_employee(osv.osv):
    _inherit = "hr.employee"
    
    
    def _current_working_age(self, cr, uid, ids, field_name, arg, context):
        res = {}
        today = date = datetime.now()
        yow = today
        for employee in self.browse(cr, uid, ids):            
            #if employee.yow:
            if employee.date_in and employee.date_out==False:
                yow = datetime.strptime(employee.date_in, '%Y-%m-%d')
                res[employee.id] = relativedelta (today, yow).years
            elif employee.date_in and employee.date_out:
                date_in = datetime.strptime(employee.date_in, '%Y-%m-%d')
                date_out = datetime.strptime(employee.date_out, '%Y-%m-%d')
                diff = date_out - date_in
                print date_in, date_out,diff.days
#                 print "DIFF",employee.date_out - employee.date_in
#                 date1 = relativedelta(datetime.strptime(employee.date_in, '%Y-%m-%d')).years
#                 date2 = relativedelta(datetime.strptime(employee.date_out, '%Y-%m-%d')).years
#                 print "=========>>>>",relativedelta(date2 - date1)
                res[employee.id] = diff.days/365
        return res
    
    
    _columns = {
                 
                'nik'           : fields.char('NIK', size=20, help="Nomor Karyawan"),
                'grade'         : fields.many2one('hr.grade',"Grade"),
                'level'         : fields.many2one('hr.position.level',"Level" ),
                'state_id'         : fields.selection([
                                                    ('new','Draft'),
                                                    ('draft', 'PKWT'), 
                                                    ('active', 'Tetap'), 
                                                    ('resign', 'Resigned'),
                                                    ('terminate', 'Terminated'),
                                                    ('pension', 'Pension'),
                                   ], 'State'),
                'date_in'          : fields.date('Date Hired'),
                'pengangkatan_date': fields.date('Tanggal Pengangkatan'),
                'date_out'         : fields.date('Date Resigned'),
                'year_work'         : fields.function(_current_working_age, method=True, string='Period of Work (year)', type='integer', store=True),

                'types'         : fields.selection([
                                                    ('employee', 'Employee'), 
                                                    ('commisioner', 'Commissioner'),
                                                    ('director', 'Director'),], 'Type', help='Employee State'),
              }
    _sql_constraints = [
        ('nik_uniq', 'unique (nik)', 'NIK must be unique per employee !')
                        ]
    
    _defaults = {
               'types'  : 'employee',   
               'state_id'  : 'new',
               
               }
    
    def modify(self,cr,uid,ids,context=None):
        self.write(cr,uid,ids,{'state_id':'new'})
        return True 
    
hr_employee()


class hr_grade(osv.osv):
    _name = "hr.grade"
    _columns = {
                 
                'name'          : fields.char("Code", size=4),
                'description'           : fields.char('Name',size=16),
              }
hr_grade()

class hr_level(osv.osv):
    _name = "hr.position.level"
    _columns = {
                 
                'name'          : fields.char("Level", size=64),
                'description'   : fields.char('Description',size=16),
              }
hr_grade()



## HR Contract ##
# 
# class hr_employee_contract(osv.osv):
#     _inherit = "hr.contract"
#     _columns = {
#                 'state'         : fields.selection([
#                                                     ('draft', 'Draft'), 
#                                                     ('propose', 'Proposed'), 
#                                                     ('confirm', 'Confirmed'),
#                                                     ('run', 'Running'),
#                                                     ('stop', 'Cancelled'),
#                                    ], 'State', help='Contract State'),
#                 
#                 }
# 
# 
#     _defaults ={  
#                'state'  : 'draft'
#                
#                }
# hr_employee_contract()


