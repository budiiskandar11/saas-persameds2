# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp import tools
from openerp.osv import fields, osv
from .. import hr_employee
from openerp.addons.decimal_precision import decimal_precision as dp


class hr_report(osv.Model):
    _name = "hr.report"
    _description = "Employee Statistics"
    _auto = False
    _rec_name = 'date_create'
    _order = 'date_create desc'

    _columns = {
        'user_id': fields.many2one('res.users', 'User', readonly=True),
        'company_id': fields.many2one('res.company', 'Company', readonly=True),
        'date_create': fields.datetime('Create Date', readonly=True),
        'gender': fields.selection([('male', 'Male'), ('female', 'Female')], 'Gender'),
        'degree'        : fields.selection ([
                                                     ('sma',"SMA"),
                                                     ('d3', "D3"),
                                                     ('p2',"S1"),
                                                     ('s2',"S2"),
                                                     ('s3',"S3")
                                                     ],"Degree"),
        'state_id'         : fields.selection([
                                                    ('draft', 'PKWT'), 
                                                    ('active', 'Tetap'), 
                                                    ('resign', 'Resigned'),
                                                    ('terminate', 'Terminated'),
                                                    ('pension', 'Pension'),
                                   ], 'State', help='Employee State'),
        'job_id': fields.many2one('hr.job', 'Applied Job',readonly=True),
        #'stage_id': fields.many2one ('hr.recruitment.stage', 'Stage'),
        #'type_id': fields.many2one('hr.recruitment.degree', 'Degree'),
        'department_id': fields.many2one('hr.department','Department',readonly=True),
        #'priority': fields.selection(hr_recruitment.AVAILABLE_PRIORITIES, 'Appreciation'),
        #'salary_prop' : fields.float("Salary Proposed", digits_compute=dp.get_precision('Account')),
        #'salary_prop_avg' : fields.float("Avg. Proposed Salary", group_operator="avg", digits_compute=dp.get_precision('Account')),
        #'salary_exp' : fields.float("Salary Expected", digits_compute=dp.get_precision('Account')),
        #'salary_exp_avg' : fields.float("Avg. Expected Salary", group_operator="avg", digits_compute=dp.get_precision('Account')),
        #'partner_id': fields.many2one('res.partner', 'Partner',readonly=True),
        #'available': fields.float("Availability"),
        #'delay_close': fields.float('Avg. Delay to Close', digits=(16,2), readonly=True, group_operator="avg",
        #                               help="Number of Days to close the project issue"),
        #'last_stage_id': fields.many2one ('hr.recruitment.stage', 'Last Stage'),
    }
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'hr_report')
        cr.execute("""
            create or replace view hr_report as (
                 select
                     min(s.id) as id,
                     s.create_date as date_create,
                     s.job_id,
                     s.gender,
                     s.degree,
                     s.state_id,
                     s.department_id
                 from hr_employee s
                 group by
                     s.create_date,
                     s.gender,
                     s.degree,
                     s.state_id,
                     s.job_id,
                     s.department_id
            )
        """)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


