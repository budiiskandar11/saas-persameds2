
from datetime import datetime, timedelta
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
from openerp import workflow
from datetime import date, timedelta as td


class duty_trip(osv.osv):
    _name           = "duty.trip"
    _description    = "Perjalanan Dinas"
    
    
    def _total_days(self, cr, uid, ids, field_name, arg, context=None):
        print "_total_days"
        res = {}
        day={
             'Monday':0,
             'Tuesday':1,
             'Wednesday':2,
             'Thursday':3,
             'Friday':4,
             'Saturday':5,
             'Sunday':6,
             }
        for val in self.browse(cr, uid, ids, context=None):
            emp_data=self.pool.get('hr.employee').browse(cr,uid,val.employee_id.id)
            contract_id=self.pool.get('hr.payslip').get_contract(cr,uid,emp_data,val.date_start,val.date_end,context)
            if not contract_id:
                warning={
                    "title": ("No Contract Found !"),
                    'message':("You should define a contract for employee : %s!"%(emp_data.resource_id.name))
                    }
            d1 = datetime.strptime(val.date_start, '%Y-%m-%d').date()
            d2 = datetime.strptime(val.date_end, '%Y-%m-%d').date()
            
            delta = d2 - d1
            total = 0
            for i in range(delta.days + 1):
                print d1 + td(days=i)
                t1 = d1 + td(days=i)
                t1day=day[t1.strftime("%A")]
                
                contract=self.pool.get('hr.contract').browse(cr,uid,contract_id)[0]
                contractdaycheck=self.pool.get('resource.calendar.attendance').search(cr,uid,[('calendar_id','=',contract.working_hours.id),('dayofweek','=',str(t1day))])
                if contractdaycheck:
                    total += 1
        res[val.id] = { 'total_days' : total}
        return res
    
    def _total_idr(self, cr, uid, ids, field_name, arg, context=None):
        print "_total_idr"
        cur_obj = self.pool.get('res.currency')
        res = {}
        if context is None:
            context = {}
        total = 0.0
        for val in self.browse(cr, uid, ids, context=context):
            for line in val.duty_list:
                if line.currency_id.name == 'IDR':
                    total += line.tot_amount
            print "total", total
        res[val.id] = { 'tot_amount_idr' : total}
        return res
    
    def _total_usd(self, cr, uid, ids, field_name, arg, context=None):
        print "_total_idr"
        cur_obj = self.pool.get('res.currency')
        res = {}
        if context is None:
            context = {}
        total = 0.0
        
        for val in self.browse(cr, uid, ids, context=context):
            for line in val.duty_list:
                if line.currency_id.name == 'USD':
                    total += line.tot_amount
            print "total", total
        res[val.id] = { 'tot_amount_usd' : total}
        return res
    
    
    def onchange_employee_id(self, cr, uid, ids, part, context=None):
        if not part:
            return {'value': {'depart_id': False, 'job_id': False}}

        part = self.pool.get('hr.employee').browse(cr, uid, part, context=context)
        
        val = {
            'depart_id': part.department_id.id,
            'job_id': part.job_id.id,
            
        }
       
        return {'value': val}
    
  
        
        
    def approve(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {
            'state':'approve'
        }, context)
        
    def paid(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {
            'state':'paid'
        }, context)
    
    def settle(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {
            'state':'settle'
        }, context)
        
    def done(self, cr, uid, ids, context={}):
        return self.write(cr, uid, ids, {
            'state':'done'
        }, context)    

    def cancel(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)
    
    def propose_payment(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'wait_pay'}, context=context)

    def set_to_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)
        return True;
    
    
    
    
    _columns        = {
                       'name'           : fields.char('Name', size=64),
                       'no_number'      : fields.char('Number', size=64),
                       'employee_id'    : fields.many2one('hr.employee','Responsible'),
                       'depart_id'      : fields.related('employee_id', 'department_id', string='Department', type='many2one', relation='hr.department', readonly=True, store=True),
                       'job_id'         : fields.related('employee_id', 'job_id', string='Job Title', type='many2one', relation='hr.job', readonly=True, store=True),          
                       'user_id'        : fields.many2one('res.users', "Create By"),
                       'date_start'     : fields.date('Start Date'),
                       'date_create'     : fields.date('Date Create'),
                       'date_end'       : fields.date('End Date'),
                       'total_days'       : fields.function(_total_days, string='Total Days' ,type='integer', multi = "all", method=True),
                       'departure'      : fields.char("Departure", size=64),
                       'destination'    : fields.char("Destination", size=64),
                       'departure_local'      : fields.many2one("res.kabupaten","Departure", size=64),
                       'destination_local'      : fields.many2one("res.kabupaten","Destination", size=64),
                       
                       'route'          : fields.char('Route', size=64),
                                                      
                       'employee'       : fields.many2many('hr.employee','hr_duty_rel','employee_id','duty_id'),
                       'description'    : fields.text('Purposes', size= 256),
                       'flight_ids'     : fields.one2many('flight.list', 'duty_id', 'Flight List'),
                       'hotel_ids'      : fields.one2many('hotel.list', 'duty_id', 'Hotel List'),
                       'duty_list'      : fields.one2many('duty.list','duty_id','Duty List'),
                       'category_id'    : fields.many2one('duty.category',"Category"),
                       'type'           : fields.selection([('domestik','Domestic'),('int','International')],'Type'),
                       'state'          : fields.selection([
                                          ('draft','Draft'),
                                          ('confirm','Confirm'),
                                          ('approve','Approve'),
                                           ('wait_pay','Payment Propose'),
                                          ('paid','Paid'),
                                          ('settle','Settle'),
                                          ('done','Done')
                                            ],'State'),
                       'tot_amount_idr'      : fields.function(_total_idr, string='Total IDR' ,type='float', multi = "all IDR", method=True),
                       'tot_amount_usd'      : fields.function(_total_usd, string='Total USD' ,type='float', multi = "all USD", method=True),
                       'voucher_no'          : fields.char("Voucher No", size=64),
                       'voucher_date'        : fields.date("Payment Date"),
                       
                       
                       
                       
                       
                       }
    _defaults       = {
                      'state'       :'draft',
                      'user_id': lambda s, cr, uid, c: uid,
                      'type'        : 'domestik',
                      'date_create' : lambda *a:time.strftime('%Y-%m-%d'),
                      }
    def confirm(self, cr, uid, ids, context={}):
        print "SEqueNCE",self.pool.get('ir.sequence').get(cr, uid, 'duty.trip.order')
        return self.write(cr, uid, ids, {
            'state':'confirm',
            'name'   : self.pool.get('ir.sequence').get(cr, uid, 'duty.trip.order'),
        }, context)
duty_trip()

class duty_category(osv.osv):
    _name           = "duty.category"
    _columns        = {
                       'name'      : fields.char('Name', size=64),
                       'code'      : fields.char('Code', size=12),
                      }

duty_category()


class duty_list(osv.osv):
    _name           = "duty.list"
    
    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        print "XXXXXXXXXX"
        cur_obj = self.pool.get('res.currency')
        res = {}
        if context is None:
            context = {}
        sub_total = 0.0
        for line in self.browse(cr, uid, ids, context=context):
            sub_total = line.qty * line.amount
            print "sub_total", sub_total
        res[line.id] = { 'tot_amount' : sub_total}
        return res
    
    
    
   
    _columns        = {
                      'name'            : fields.char('Describe'),
                      'amount'          : fields.float('Unit Price'),
                      'tot_amount'      : fields.function(_amount_line, string='Subtotal' ,type='float', multi = "all", method=True),
                      'qty'             : fields.float('Qty'),
                      'duty_id'         : fields.many2one('duty.trip','Duty Trip'),
                      'currency_id'    : fields.many2one('res.currency','Currency'),
                      }
    
    
    
    
    
duty_list()

class flight_list(osv.osv):
    _name           = "flight.list"
    _columns        = {
                      'flight_num'      :fields.char("Flight No", size=64),
                       'flight_dep'      :fields.char("Departure City", size=64),
                       'flight_arr'      :fields.char("Arrival City", size=64),
                       'flight_date'      :fields.date("Flight Date", size=64),
                       'flight_time'      :fields.float("Flight Time", size=64),
                       'arrival_time'      :fields.float("Arrival Time", size=64),
                       'arrival_date'      :fields.date("Arrival Date", size=64),
                       'duty_id'         : fields.many2one('duty.trip','Duty Trip'),
                      }
flight_list()

class hotel_list(osv.osv):
    _name           = "hotel.list"
    _columns        = {
                      'hotel_name'          :fields.char("Hotel Name", size=64),
                      'check_in_date'       :fields.date("Check In Date"),
                      'check_out_date'      :fields.date("Check Out Date"),
                      'note'                :fields.text("Note"),
                      'duty_id'         : fields.many2one('duty.trip','Duty Trip'),
                      }
hotel_list()

