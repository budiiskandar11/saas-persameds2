from openerp.osv import fields, osv
import datetime
from openerp.tools.translate import _

class training_type(osv.osv):
    _name = "training.type"
    _columns = {
                'name'      : fields.char('Name',size=64,required=True),
                'desc'      : fields.text('Description'),
                }
training_type()

class training_predicate(osv.osv):
    _name = "training.predicate"
    _columns = {
                'name'      : fields.char('Name',size=64,required=True),
                'desc'      : fields.text('Description'),
                }
training_predicate()

class hr_training(osv.osv):
    _inherit = ['mail.thread']
    _name = "hr.training"
    _description= 'Training History of Employee'


    def _get_currency(self, cr, uid, context=None):
        user = self.pool.get('res.users').browse(cr, uid, [uid], context=context)[0]
        return user.company_id.currency_id.id

    def _diffday(self, cr, uid, ids, field_names, arg, context=None):
        res={}
        for rs in self.browse(cr, uid, ids, context=context):
            if rs.date_start:
                start   = str(rs.date_start).split('-')
                start   = datetime.date(int(start[0]), int(start[1]), int(start[2]))
                if rs.date_end:
                    end = str(rs.date_end).split('-')
                    end = datetime.date(int(end[0]), int(end[1]), int(end[2]))
                    diff = end - start
                    diffDay = diff.days + 1
                    if diffDay<0:
                        raise osv.except_osv(_('Bad date'), _('End date could not be earlier than start date'))
                    record = {
                           'duration' : diffDay
                           }
            res[rs.id] = record
        return res
        
    _columns = {
                'name'          : fields.char('Training Title',size=256,required=True,track_visibility='always'),
                'provider'      : fields.many2one('res.partner','Training Provider', required=True, domain="[('supplier','=','True')]",track_visibility='onchange'),
                'street'        : fields.char('Street', size=128),
                'street2'       : fields.char('Street2', size=128),
                'zip'           : fields.char('Zip', change_default=True, size=24),
                'city'          : fields.char('City', size=128),
                'state_id'      : fields.many2one("res.country.state", 'State'),
                'country_id'    : fields.many2one('res.country', 'Country'),
                'location'      : fields.char('Training Location',size=128),
                'location_type' : fields.selection([('domestic','Dalam Negeri'),
                                                    ('overseas','Luar Negeri')], 'Location Category'),
                'pengusul'      : fields.many2one('hr.employee','Name',required=True),
                'job_id'        : fields.many2one('hr.job','Function'),
                'department'    : fields.many2one('hr.department','Department',required=True),
                'purpose'       : fields.text('Training Purpose'),
                'date_start'    : fields.date('Start',required=True),
                'date_end'      : fields.date('End',required=True),
                'duration'      : fields.function(_diffday, method=True, store=True, multi='dc', string='Duration (days)',help="Duration (days)"),
                'type'          : fields.many2one('training.type','Training Type'),
                'employee'      : fields.many2many('hr.employee','employee_training_rel','employee_id','training_id','Employee List',track_visibility='onchange',
                                                   states={'done': [('readonly', True)], 'approved': [('readonly', True)]}),
                'state'         : fields.selection([('draft','Draft'),
                                                ('proposed','Proposed'),
                                                ('approved','Approved'),
                                                ('done','Done')],'State',readonly=True),
                'lines'         : fields.one2many('hr.training.lines','submission','Lines'),
                'currency_id'   : fields.many2one('res.currency', 'Currency'),
                'company_id': fields.many2one('res.company', 'Company', required=True),
                'cost'          : fields.float('Cost',track_visibility='onchange'),
                'product_id'    : fields.many2one('product.product','Product',states={'done': [('readonly', True)], 'approved': [('readonly', True)]}),
                'account_id'    : fields.many2one('account.account','Account',states={'done': [('readonly', True)], 'approved': [('readonly', True)]}),
                'journal_id'    : fields.many2one('account.journal','Journal',states={'done': [('readonly', True)], 'approved': [('readonly', True)]}),
                }
    _defaults = {
                 'state':'draft',
                 'company_id': lambda s, cr, uid, c: s.pool.get('res.company')._company_default_get(cr, uid, 'hr.employee', context=c),
                 'currency_id': _get_currency,
                 }
    
    _track = {
                'state': {
                    'dos_hr_training.training_proposed': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'proposed',
                    'dos_hr_training.training_approved': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'approved',
                    'dos_hr_training.training_done': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'done',
                },
              }
    def onchange_dateGo(self,cr,uid,ids,start,end):
        if start:
            start   = str(start).split('-')
            start   = datetime.date(int(start[0]), int(start[1]), int(start[2]))
            if end:
                end     = str(end).split('-')
                end     = datetime.date(int(end[0]), int(end[1]), int(end[2]))
                diff = end - start
                val = {'duration' : diff.days+1}
                return {'value':val}
        return start
    
    def onchange_dateReturn(self,cr,uid,ids,start,end):
        val = {}
        if end:
            end     = str(end).split('-')
            end     = datetime.date(int(end[0]), int(end[1]), int(end[2]))
            if start:
                start   = str(start).split('-')
                start   = datetime.date(int(start[0]), int(start[1]), int(start[2]))
                diff = end - start
                val = {'duration' : diff.days+1}
                return {'value':val}
            else:
                val = {'duration' : 0}
        return {'value':val}
    
    def onchange_provider(self,cr,uid,ids,data,context=None):
        val={}
        if data:
            partner=self.pool.get('res.partner').browse(cr,uid,data)
            val={
                 'street'   : partner.street,
                 'street2'  : partner.street2,
                 'city'     : partner.city,
                 'state_id' : partner.state_id and partner.state_id.id or False,
                 'zip'      : partner.zip,
                 'country_id':partner.country_id and partner.country_id.id or False
                 }
        return{'value':val}
        
    def onchange_proposer(self,cr,uid,ids,data,context=None):
        val={}
        if data:
            proposer=self.pool.get('hr.employee').browse(cr,uid,data)
            val['job_id']=proposer['job_id']['id']
            val['department']=proposer['department_id']['id']
        return {'value':val}
    
    def onchange_peserta(self,cr,uid,ids,data,context=None):
        val={}
        if data:
            proposer=self.pool.get('hr.employee').browse(cr,uid,data)
            val['state']=proposer['state_id']['id']
            val['job_id']=proposer['job_id']['id']
            val['department']=proposer['department_id']['id']
        return {'value':val}
    
    def button_proposed(self, cr, uid, ids, context={}):
        for chk in self.browse(cr, uid, ids):
            chk.write({"state":"proposed"})
        return True
    
    def button_approved(self, cr, uid, ids, context={}):
        res=True
        for tr in self.browse(cr, uid, ids):
            qty = len(tr.employee)
            tr.write({"state":"approved"})
        
#        inv  = {
#                'name': tr.name,
#                'account_id': tr.account_id,
#                'type': 'in_invoice',
#                'partner_id': tr.provider,
#                'address_invoice_id': exp.employee_id.address_home_id.id,
#                'address_contact_id': exp.employee_id.address_home_id.id,
#                'origin': exp.name,
#                'invoice_line': lines,
#                'currency_id': exp.currency_id.id,
#                'payment_term': payment_term_id,
#                'fiscal_position': exp.employee_id.address_home_id.partner_id.property_account_position.id
#                }
        
        return res
    
    def button_draft(self, cr, uid, ids, context={}):
        for chk in self.browse(cr, uid, ids):
            chk.write({"state":"draft"})
        return True
    
    def button_cancel(self, cr, uid, ids, context={}):
        for chk in self.browse(cr, uid, ids):
            chk.write({"state":"cancelled"})
        return True
    
    def button_done(self, cr, uid, ids, context={}):
        for chk in self.browse(cr, uid, ids):
            chk.write({"state":"done"})
            data = self.pool.get('hr.training').browse(cr,uid,ids[0])
            for employee in data['employee']:
                values = {
                          'name'        : data.name,
                          'employee'    : employee.id,
                          'submission'  : ids[0],
                          'provider'    : data.provider.id,
                          'location_type'    : data.location_type.id,
                          'date_start'  : data.date_start,
                          'date_end'    : data.date_end,
                          'duration'    : data.duration,
                          'type'        : data.type.id,
                          'cost'        : data.cost,
                          }
                self.pool.get('hr.training.lines').create(cr,uid,values)
        return True
hr_training()

class hr_training_lines(osv.osv):
    _name = "hr.training.lines"
    def _count_duration(self,cr,uid,ids,field,arg,context):
        trainings=self.browse(cr,uid,ids,context=context)
        result = {}
        for training in trainings :
#            start=False
            
            if training.date_end:
                if training.date_start:
#                    start   = training.date_start.split('-')
#                    start   = datetime.date(int(start[0]), int(start[1]), int(start[2]))
                    start=datetime.datetime.strptime(training.date_start, '%Y-%m-%d')
                    end=datetime.datetime.strptime(training.date_end, '%Y-%m-%d')
                    duration=end-start
                    if duration.days<0:
                        raise osv.except_osv(_('Bad date'), _('End date could not be earlier than start date'))
                        result[training.id]=duration.days+1
            else:
                result[training.id]=0
             
        #print "4==========>",result
        return result
        
    _columns = {
                'name'          : fields.char('Title',size=256,required=True),
                'certificate'   : fields.binary('Certificate'),
                'submission'    : fields.many2one('hr.training','Submission',readonly=True,help="If you find this field empty, the training submission maybe has been deleted, or this record is created manually."),
                'employee'      : fields.many2one('hr.employee','Employee'),
                'provider'      : fields.many2one('res.partner','Training Provider'),
                'location'      : fields.char('Location',size=128),
                'location_type' : fields.selection([('domestic','Dalam Negeri'),
                                                    ('overseas','Luar Negeri')], 'Location type'),
                'date_start'    : fields.date('Start'),
                'date_end'      : fields.date('End'),
                #'duration'      : fields.integer('Duration (days)',store=True, readonly=True),
                'duration'      :fields.function(_count_duration,method=True,type='integer',string='Duration (days)',help="Training Duration",store=True),
                'currency_id'      : fields.many2one('res.currency','Currency'),
                'cost'          : fields.integer('Cost'),
                'predicate'     : fields.many2one('training.predicate','Training Predicate'),
                'certification' : fields.selection([('certified','Certified'),
                                                    ('non_certified','Non Certified')],
                                                   'Certification'),
                'category'      : fields.selection([('after','After recruited'),
                                                    ('before','Before recruited')],
                                                   'Before/After'),
                'type'          : fields.many2one('training.type','Type'),
                }
    
    def create(self,cr,uid,vals,context=None):
        end=vals['date_end']
        start=vals['date_start']
        if 'duration' not in vals.keys():
            if end:
                end     = vals['date_end'].split('-')
                end     = datetime.date(int(end[0]), int(end[1]), int(end[2]))
                if start:
                    start   = vals['date_start'].split('-')
                    start   = datetime.date(int(start[0]), int(start[1]), int(start[2]))
        
                    duration=end-start
                    if duration.days<0:
                        raise osv.except_osv(_('Bad date'), _('End date could not be earlier than start date'))
                        vals['duration']=duration.days+1
            else:
                vals['duration']=0
        ids=super(hr_training_lines,self).create(cr,uid,vals,context)
        return ids
    
    def write(self,cr,uid,ids,vals,context=None):
        print 'vals238451e3',vals
        end=vals['date_end']
        start=vals['date_start']
        if 'duration' not in vals.keys():
            if end:
                end     = vals['date_end'].split('-')
                end     = datetime.date(int(end[0]), int(end[1]), int(end[2]))
                if start:
                    start   = vals['date_start'].split('-')
                    start   = datetime.date(int(start[0]), int(start[1]), int(start[2]))
        
                    duration=end-start
                    if duration.days<0:
                        raise osv.except_osv(_('Bad date'), _('End date could not be earlier than start date'))
                        vals['duration']=duration.days+1
            else:
                vals['duration']=0
        write=super(hr_training_lines,self).write(cr,uid,ids,vals,context)
        return write
    
    def onchange_provider(self,cr,uid,ids,data,context=None):
        val={}
        if data:
            partner=self.pool.get('res.partner').browse(cr,uid,data)
            address=partner['address'][0]['street']
            val['location']=address
        return{'value':val}
        
    def onchange_dateGo(self,cr,uid,ids,start,end):
        if start:
            start   = str(start).split('-')
            start   = datetime.date(int(start[0]), int(start[1]), int(start[2]))
            if end:
                end     = str(end).split('-')
                end     = datetime.date(int(end[0]), int(end[1]), int(end[2]))
                diff = end - start
                val = {'duration' : diff.days+1}
                return {'value':val}
        return start
  
    def onchange_dateReturn(self,cr,uid,ids,start,end):
        val = {'duration' : 0}
        if end:
            end     = str(end).split('-')
            end     = datetime.date(int(end[0]), int(end[1]), int(end[2]))
            if start:
                start   = str(start).split('-')
                start   = datetime.date(int(start[0]), int(start[1]), int(start[2]))
                diff = end - start
                val = {'duration' : diff.days+1}
                return {'value':val}
            else:
                val = {'duration' : 0}
        return {'value':val}
hr_training_lines()

class hr_employee(osv.osv):
    _inherit = "hr.employee"
    _columns = {
                
                'training_line' : fields.one2many('hr.training.lines','employee','Training Lines'),
                }
hr_employee()