import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta

from openerp import netsvc
from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.tools.safe_eval import safe_eval as eval
import pytz

class import_attendance_confirm(osv.osv_memory):
    """
    This wizard will confirm the all the selected draft invoices
    """

    _name = "import.attendance.confirm"
    _description = "Confirm Attendances"
    
    def create_attendance(self, cr, uid, ids, employee_id, date, action, record, context=None):
        attendance_obj = self.pool.get('hr.attendance')
        print "date?????", date, datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - timedelta(hours=7)
        val = {
               'employee_id'    : employee_id,
               'name'           : datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - timedelta(hours=7),
               'action'         : action,
               'id_import'      : record.id
               }
        
        attendance_obj.create(cr, uid, val, context=None)
        return True
    
    def create_absence(self, cr, uid, ids, name, employee_id, date, reason, record, context=None):
        absence_obj = self.pool.get('hr.absence')
        
        val = {
               'name'           : name,
               'employee_id'    : employee_id,
               'date'           : date,
               'reason'         : reason,
               'id_import'      : record.id
               }
        
        absence_obj.create(cr, uid, val, context=None)
        return True
    
    def attendance_confirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        active_ids = context.get('active_ids', []) or []

        proxy = self.pool['attendance.import']
        for record in proxy.browse(cr, uid, active_ids, context=context):
            print "#################################", record.nama_peg.name, record.id
            
            if record.state not in ('draft'):
                raise osv.except_osv(_('Warning!'), _("Selected attendances with state draft."))
            
            name            = record.name
            date            = datetime.strptime(record.tanggal, '%m/%d/%y')
            employee_id     = record.nama_peg.id
            sign_in_date    = record.date_sign_in
            sign_out_date   = record.date_sign_out
            reason          = record.reason.id
            
            #date = datetime.datetime.strptime(i.date,"%Y-%m-%d").strftime('%Y-%m-%d')
            #date = datetime.datetime.strptime(date,"%Y-%m-%d")
            #print "date----------------->>", date, date.strftime("%u")
            
            print "Date-----.>", date
            
            if str(date.strftime("%u")) == '6' or str(date.strftime("%u")) == '7':
                True
            elif self.pool.get('hr.holiday.year').search(cr,uid,[('date','=',date)]):
                print "MASUUUUUUUUKK", date
                True
            elif sign_in_date and sign_out_date:
                ###Sign In###
                self.create_attendance(cr, uid, ids, employee_id, sign_in_date, 'sign_in', record, context)
                ###Sign Out###
                self.create_attendance(cr, uid, ids, employee_id, sign_out_date, 'sign_out', record, context)
            elif not sign_in_date and not sign_out_date and reason:
                self.create_absence(cr, uid, ids, name, employee_id, date, reason, record,context)
            elif not sign_in_date and not sign_out_date and not reason:
                raise osv.except_osv(_('Warning!'), _("Attandance for %s in date : %s not have any sign in or sign out and not reason") % (record.nama_peg.name, str(date)))               
            else:
                reason_search = self.pool.get('absence.reason').search(cr, uid, [('asdefault','=',True)])
                if not reason_search:
                    raise osv.except_osv(_('Warning!'), _("Please define Absence Reason default"))
                for i in self.pool.get('absence.reason').browse(cr, uid, reason_search):
                    reason = i.id
                
                self.create_absence(cr, uid, ids, name, employee_id, date, reason, record,context)
            record.write({'state' : 'confirm'})
            
        return {'type': 'ir.actions.act_window_close'}