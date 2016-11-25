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


class res_religion(osv.osv):
    
    _name = "res.religion"
    _description= 'Description of religion'

    _columns = {
        'name' : fields.char('Religion', size=20, required = True, help="Religion name"),
        }

    _sql_constraints = [
        ('unique_name', 'unique (name)', 'Religion name must be unique !')
    ]

    def copy(self, cr, uid, id, default={}, context=None):
        previous_name = self.browse(cr, uid, id, context=context)
        if not default:
            default = {}
        default = default.copy()
        default['name'] = (previous_name['name'] or '') + '(copy)'
        print default['name']
        return super(res_religion, self).copy(cr, uid, id, default, context=context)

res_religion()


class hr_personal_info(osv.osv):
    _inherit = "hr.employee"
    
    def _current_employee_age(self, cr, uid, ids, field_name, arg, context):
        res = {}
        today = date = datetime.now()
        dob = today
        for employee in self.browse(cr, uid, ids):            
            if employee.birthday:
                dob = datetime.strptime(employee.birthday, '%Y-%m-%d')
                res[employee.id] = relativedelta (today, dob).years
        return res
    
    
    
    
    _columns = {
                 'no_ktp'        : fields.char('No.KTP', size=20, help="Nomor Kartu Tanda Penduduk"),
                 'date_valid'    : fields.date('KTP Validity Date'),
                 'ktp_street': fields.char('Street', size=128),
                 'ktp_street2': fields.char('Street2', size=128),
                 'ktp_rt': fields.char('Street2', size=4),
                 'ktp_rw': fields.char('Street2', size=4),
                 'ktp_kel': fields.char('Street2', size=128),
                 'ktp_zip': fields.char('Zip', change_default=True, size=24),
                 'ktp_city': fields.char('City', size=128),
                 'ktp_state_id': fields.many2one("res.country.state", 'State'),
                 'ktp_country_id': fields.many2one('res.country', 'Country'),
                 'religion_id'    : fields.many2one('res.religion', 'Religion', help='Employee religion'),
                 'blood_type'        : fields.selection([('a','A'),
                                                        ('b','B'),
                                                        ('ab','AB'),
                                                        ('o','O')], 'Blood Type'),
                'marriage_date'     : fields.date('Marriage Date'),
                 'emergency_contact' : fields.char('Emergency contact', size=64),
                 'emergency_relation' : fields.char('Relation', size=64),
                 'emergency_phone' : fields.char('Emergency phone', size=64),
                    'npwp' : fields.char('NPWP No', size=20, required=False, help="Indonesian Tax Registration Number e.g 01.855.081.4-005.000"),
                 'family_ids' : fields.one2many('hr.family','employee_id','Family Member'),
                 'job_exp_ids': fields.one2many('hr.job_experience','employee_id','Job Experience'),
                 'age' : fields.function(_current_employee_age, method=True, string='Age', type='integer', store=True),
                 'sim': fields.char('SIM', size=32, help="Surat Ijin Mengemudi"),
                 'sim_type': fields.selection([('a','A'),
                                              ('b1','B1'),
                                              ('b2','B2'),
                                              ('c','C'),
                                              ('d','D')],'Type'),
                 'sim_expire': fields.date('Expire Date'),
                 'email'      : fields.char('Email'),
                 }
    
    def onchange_format_npwp(self, cr, uid, ids, npwp):

        if len(npwp) == 0:
            return True

        warning = {
            "title": _("Bad NPWP format !"),
            "message": _("The NPWP format should be like this '01.855.081.4-005.000' or '018550814005000'")
        }

        if len(npwp) not in (15,20):
            return {'warning': warning}

        if len(npwp)==15:
            try:
                int(npwp)
            except:
                return {'warning': warning}
        
        if len(npwp)==20:
            try:
                int(npwp[:2])
                int(npwp[3:6])
                int(npwp[7:10])
                int(npwp[11:12])
                int(npwp[13:16])
                int(npwp[-3:])
            except:
                return {'warning': warning}

        vals = {}
        if len(npwp)==15:
            formatted_npwp = npwp[:2]+"."+npwp[2:5]+"."+npwp[5:8]+"."+npwp[8:9]+"-"+npwp[9:12]+"."+npwp[12:15]
            vals={
                "npwp" : formatted_npwp
            }
            return {"value": vals}

        return {"value": vals}

    def _check_npwp(self,cr,uid,ids,context=None):
        """npwp = self.browse(cr, uid, ids[0], context=context).npwp
        if not npwp:
            return True

        if len(npwp) not in (15,20):
            return False

        if len(npwp)==15:
            try:
                int(npwp)
            except:
                return False
        
        if len(npwp)==20:
            try:
                int(npwp[:2])
                int(npwp[3:6])
                int(npwp[7:10])
                int(npwp[11:12])
                int(npwp[13:16])
                int(npwp[-3:])
            except:
                return False
        
        if npwp[2:3] not in '.':
            return False
        if npwp[6:7] not in '.':
            return False
        if npwp[10:11] not in '.':
            return False
        if npwp[12:13] not in '-':
            return False
        if npwp[16:17] not in '.':
            return False"""
        return True
    
    _constraints = [
        (_check_npwp, _("Bad NPWP format ! \nThe NPWP format should be like this '01.855.081.4-005.000' or '018550814005000'"), ['npwp'])
        ]
    
hr_personal_info()

class hr_family(osv.osv):
    _name = 'hr.family'
    _columns = {
        'name'          : fields.char('Nama'),
        'birthday'      : fields.date('Tanggal Lahir'),
        'status'        : fields.selection([
            ('ayah','Suami'),
            ('ibu','Istri'),
            ('anak','Anak')
            ],'Status'),
        'notes'         : fields.text('Notes'),
        'employee_id'   : fields.many2one('hr.employee','Employee'),
    }
hr_family()

class hr_job_experience(osv.osv):
    _name = 'hr.job_experience'
    _columns = {
        'company_name'  : fields.char('Company Name'),
        'title'         : fields.char('Title'),
        'location'      : fields.char('Location'),
        'date_from'     : fields.date('Date From'),
        'date_to'       : fields.date('Date To'),
        'current_work'  : fields.boolean('I Currently Workhere'),
        'employee_id'   : fields.many2one('hr.employee','Employee'),
    }
hr_job_experience()

