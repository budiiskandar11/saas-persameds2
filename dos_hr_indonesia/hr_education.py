
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools.safe_eval import safe_eval as eval
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta


class hr_education (osv.osv):
    _name = 'hr.education'
    _description= 'Education Background List of Employee'

    #Check whether the course title and the course description are not the same
    _columns = {
                'edu_from'          : fields.char("Start (year)", size=4,  help="Education start"),
                'edu_to'            : fields.char("Finish (year)", size=4, help="Education finish"),
                'type'          : fields.selection([('formal','Formal'),
                                                ('informal','Informal')],'Type'),
                'name'          : fields.char('Edu Name', size=64, required=False, help="Education name (ie. School/University Name)"),
                'subject'       : fields.char('Subject', size=64, required=False, help="Education subject"),
                'notes'         : fields.text('Notes'),
                'res_id'        : fields.integer('Resource ID', select=1, readonly=True),
                'employee'      : fields.many2one('hr.employee','Employee'),
                'passed'        : fields.selection([('yes','Lulus'),
                                                ('no','Tidak lulus'),
                                                ('move','Pindah')], 'Status'),
                'degree'        : fields.char('Degree',size=16),
                'certificate'   : fields.binary('Attachment'),
                'no_certificate'   : fields.char('Certificate No', size=16),
               
                }
    
    _order = "name desc,create_date desc"

hr_education()

class hr_employee(osv.osv):
    """ HR Employee """
    _inherit = "hr.employee"
    _columns = {
                'education_id': fields.one2many('hr.education', 'res_id', 'Education background', required=True ),
                'latest_edu'     : fields.char('Latest Education', size=32),
                'degree'        : fields.selection ([
                                                     ('sma',"SMA"),
                                                     ('smk',"SMK"),
                                                     ('d1', "D1"),
                                                     ('d3', "D3"),
                                                     ('p2',"S1"),
                                                     ('s2',"S2"),
                                                     ('s3',"S3")
                                                     ],"Degree"),
                #'message_ids': fields.one2many('mailgate.message', 'res_id', 'Messages', domain=[('model','=',_name)]),
                }

hr_employee()
