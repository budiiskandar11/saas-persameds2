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
from .. import duty_trip
from openerp.addons.decimal_precision import decimal_precision as dp


class hr_report(osv.Model):
    _name = "duty.report"
    _description = "Duty Trip Statistics"
    _auto = False
    _rec_name = 'date_create'
    _order = 'date_create desc'

    _columns = {
        'user_id': fields.many2one('res.users', 'User', readonly=True),
        'company_id': fields.many2one('res.company', 'Company', readonly=True),
        'date_create': fields.datetime('Create Date', readonly=True),
        'type'           : fields.selection([('domestik','Domestic'),('int','International')],'Type'),
        'category_id'    : fields.many2one('duty.category',"Category"),
        'employee_id'    : fields.many2one('hr.employee','Responsible'),
        'idr_total': fields.float('Total Cost IDR', readonly=True),
        #'usd_total': fields.float('Total Cost USD', readonly=True),
        #'stage_id': fields.many2one ('hr.recruitment.stage', 'Stage'),
        #'type_id': fields.many2one('hr.recruitment.degree', 'Degree'),
        'depart_id': fields.many2one('hr.department','Department',readonly=True),
       'user_id'        : fields.many2one('res.users', "Create By"),
        }
    
    def init(self, cr):
        tools.drop_view_if_exists(cr,self._table)
        cr.execute("""
            create or replace view duty_report as (
                 select
                     min(s.id) as id,
                     s.create_date as date_create,
                     s.depart_id,
                     s.user_id,
                     s.type,
                     s.category_id,
                     s.employee_id
                   
                 from duty_trip s
                    
                 group by
                     s.create_date,
                     s.depart_id,
                     s.type,
                     s.category_id,
                     s.employee_id,
                     s.user_id
            )
        """)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:


