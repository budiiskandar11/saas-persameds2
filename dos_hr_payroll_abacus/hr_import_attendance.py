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

class absence_reason(osv.osv):
    _name   = "absence.reason"
    
    _columns = {
            'name'          : fields.char('Name',size=32,readonly=False),
            'allowance'     : fields.boolean('Allowance'),
            'asdefault'     : fields.boolean('As Default'),
                }
    
absence_reason()

class attendance_import(osv.osv):
    _name   = "attendance.import"
    
    def _get_sign_in(self, cr, uid, ids, name, arg, context=None):
        """Read the shipping date from the related packings"""
        # TODO: would be better if it returned the date the picking was processed?
        res = {}
        for attn in self.browse(cr, uid, ids, context=context):
            if attn.masuk:
                if str(attn.masuk).find('.') > 0:
                    merge_date      = str(attn.tanggal) +' '+ str(attn.masuk).replace(".", ":") + ':00'
                else:
                    merge_date      = str(attn.tanggal) +' '+ str(attn.masuk) + ':00:00'
                
                print "merge_date---------->>", merge_date
                
                date_sign       = datetime.strptime(merge_date, '%m/%d/%y %H:%M:%S') - timedelta(hours=7)
                
                print "date_sign----->>", date_sign
                
                sign            = date_sign.strftime('%Y-%m-%d %H:%M:%S') 
                res[attn.id]    = sign
            else:
                res[attn.id] = False
        return res
    
    def _get_sign_out(self, cr, uid, ids, name, arg, context=None):
        """Read the shipping date from the related packings"""
        # TODO: would be better if it returned the date the picking was processed?
        res = {}
        for attn in self.browse(cr, uid, ids, context=context):
            if attn.keluar:
                if str(attn.keluar).find('.') > 0:
                    merge_date      = str(attn.tanggal) +' '+ str(attn.keluar).replace(".", ":") + ':00'
                else:
                    merge_date      = str(attn.tanggal) +' '+ str(attn.keluar) + ':00:00'
                ###JIKA Jam lebih dari 24:00:00#####
                if int(merge_date.split(" ")[1].split(":")[0]) >= 24:
                    merge_date      = str(attn.tanggal) +' '+ '23:59:00'
                ################################
                date_sign       = datetime.strptime(merge_date, '%m/%d/%y %H:%M:%S') - timedelta(hours=7)
                sign            = date_sign.strftime('%Y-%m-%d %H:%M:%S') 
                res[attn.id]    = sign
            else:
                res[attn.id] = False
        return res
    
    
    def _get_attn(self, cr, uid, ids, name, arg, context=None):
        """Read the shipping date from the related packings"""
        # TODO: would be better if it returned the date the picking was processed?
        res = {}
        for attn in self.browse(cr, uid, ids, context=context):
            if attn.tanggal:
                date_attn       = datetime.strptime(attn.tanggal, '%m/%d/%y')
                attendances     = date_attn.strftime('%Y-%m-%d') 
                res[attn.id]    = attendances
            print res
        return res
    
    _columns    = {
                    'name'          : fields.char('Name',size=300,readonly=False),
                    'no_peg'        : fields.char('Nomor Pegawai',size=300,readonly=False),
                    'no_akun'       : fields.integer('Nomor Akun'),
                    #'nama_peg'      : fields.char('Nama Pegawai',size=256),
                    'nama_peg'      : fields.many2one('hr.employee', 'Nama Pegawai'),
                    'auto_assign'   : fields.char('Auto Assign',size=32), 
                    'tanggal'       : fields.char('Tanggal'),
                    'jam_kerja'     : fields.char('Jam Kerja',size=32),
                    #****************************************************************#
                    'awal_tugas'    : fields.char('Awal Tugas',size=32),
                    'akhir_tugas'   : fields.char('Akhir Tugas',size=32),
                    'masuk'         : fields.char('Masuk',size=32),
                    'keluar'        : fields.char('Keluar',size=32),
                    'telat'         : fields.char('Telat',size=32),
                    'pulang_awal'   : fields.char('Pulang Awal',size=32),
                    'bolos'         : fields.boolean('Bolos'),
                    'waktu_lembur'  : fields.char('Waktu Lembur',size=32),
                    'waktu_kerja'   : fields.char('Waktu Kerja',size=32),
                    'status'        : fields.char('Status',size=32),
                    #****************************************************************#
                    'hrs_c_out'     : fields.boolean('Hrs C/Out'),
                    'departement'   : fields.char('Department',size=32),
                    'ndays'         : fields.integer('Ndays'),
                    'akhir_pekan'   : fields.integer('Akhir Pekan'),
                    'hari_libur'    : fields.integer('Hari Libur'),
                    'lama_hadir'    : fields.char('Lama Hadir',size=32),
                    'ndays_out'     : fields.float('Ndays Out'),
                    'lembur_weekday': fields.float('Lembur Akhir Pekan'),
                    'libur_lembur'  : fields.float('Libur Lembur'),
                    #****************************************************************#
                    'date_sign_in'  : fields.function(_get_sign_in, type='datetime',
                                                        store=False, string='Sign In Date',
                                                            help=""),
                    'date_sign_out' : fields.function(_get_sign_out, type='datetime',
                                                        store=False, string='Sign Out Date',
                                                            help=""),
                    'date_attn'     : fields.function(_get_attn, type='date',
                                                        store=False, string='Attn Date',
                                                            help=""),
                   'deskripsi'       : fields.char('Deskripsi',size=300,readonly=False), 
                   'reason'         : fields.many2one('absence.reason', 'Reason'),                     
                   'state'         : fields.selection([('draft', 'Draft'), ('confirm', 'Confirmed')], 'State'),
                }
    _defaults   = {
                    'state'     : 'draft',
                    #'name'      : '/'
                   }
attendance_import()