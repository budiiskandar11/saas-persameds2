# -*- coding: utf-8 -*-
#Copyright (c) Vincent Cardon <vincent.cardon@tranquil-it-systems.fr>
# Denis Cardon <denis.cardon@tranquilitsystems.com> and Emmanuel RICHARD.
#Ingenieur fondateur
#Tranquil IT Systems
from __future__ import with_statement
from osv import osv, fields
import pooler
import tools
from tools.translate import _
from report.render import render
from report.interface import report_int
import addons
import tempfile
import os
import netsvc
from pdf_ext import fill_pdf

class external_pdf(render):

    def __init__(self, pdf):
        render.__init__(self)
        self.pdf = pdf
        self.output_type='pdf'

    def _render(self):
        return self.pdf


class report_custom(report_int):

    def create(self, cr, uid, ids, datas, context=None):
        form_name = datas['form']['name']+'.pdf'
        
        pool = pooler.get_pool(cr.dbname)
        emp_obj = pool.get('hr.employee').browse(cr,uid,ids[0],context)
        result = {}
        partner = emp_obj.company_id.partner_id
        
        emp_name            = emp_obj.name
        emp_name            = emp_name.split(" ")
        name_length         = len(emp_name)
        firstname           = emp_name[0]
        midname             = ""
        lastname            = ""
        wife_husband_birth  = ""
        son1_birthday       = ""
        son2_birthday       = ""
        son3_birthday       = ""
        
        if name_length==2:
            midname =""
            lastname=emp_name[1]
        elif name_length==3:
            midname = emp_name[1]
            lastname= emp_name[2]
        elif name_length==4:
            midname = emp_name[1]+" "+emp_name[2]
            lastname= emp_name[3]
        
        birthday    = emp_obj.birthday
        birthday    = birthday.split("-")
        
        if emp_obj.country_id.name=="Indonesia":
            country=""
        else:
            country=emp_obj.country_id.name
        
        ktp=emp_obj.ktp
        if emp_obj.ktp:
            ktp=ktp.replace(".","")
            ktp=ktp.replace("-","")
        
        npwp=emp_obj.npwp
        if npwp:
            npwp=npwp.replace(".","")
            npwp=npwp.replace("-","")
        else:
            npwp=""
        
        family              = emp_obj.family_id
        wife_husband        = ['wife','istri','husband','suami']
        son                 = ['son','daughter','putra','putri','anak']
        wife_husband_name   = ""
        son1_name           = ""
        son2_name           = ""
        son3_name           = ""
        if len(family)!=0:
            for family in family:
                if family.relation:
                    if family.relation.name.lower() in wife_husband:
                        wife_husband_name   = family.name
                        wife_husband_birth  = family.birthday.split("-")
                    elif family.relation.name.lower() in son:
                        son_name            = family.name
                        if son1_name=="":
                            son1_name       = son_name
                            son1_birthday   = family.birthday.split("-")
                        elif son2_name=="":
                            son2_name=son_name
                            son2_birthday   = family.birthday.split("-")
                        elif son3_name=="":
                            son3_name=son_name
                            son3_birthday   = family.birthday.split("-")
        
        if wife_husband_birth=="":
            wife_husband_birth=["","",""]
        if son1_birthday=="":
            son1_birthday=["","",""]
        if son2_birthday=="":
            son2_birthday=["","",""]
        if son3_birthday=="":
            son3_birthday=["","",""]
        
        title=partner.title
        if title:
            title=title.name
        else:
            title=""

        phone=partner.phone
        if phone:
            phone=phone.replace("(","")
            phone=phone.replace("+","")
            phone=phone.replace(")","")
            phone=phone.split("-")
            phonearea=phone[0]
            if phone[0][0]!='0':
                phonearea='0'+phonearea[2:]
        else:
            phone=""
        
        fax=partner.address[0].fax
        if fax:
            fax=fax.replace("(","")
            fax=fax.replace("+","")
            fax=fax.replace(")","")
            fax=fax.split("-")
            faxarea=fax[0]
            if fax[0][0]!='0':
                faxarea='0'+faxarea[2:]
        else:
            fax=""
        
        result['com_name']                      = emp_obj.company_id.name
        result['com_npwp']                      = npwp
        result['com_phone1_area']               = phonearea
        result['com_phone1_number']             = phone[1]
        result['com_zip']                       = partner.address[0].zip
        result['com_badan_hukum']               = title
        result['emp_first_name']                = firstname
        result['emp_mid_name']                  = midname
        result['emp_last_name']                 = lastname
        result['emp_nama']                      = firstname+" "+midname+" "+lastname
        result['emp_jabatan']                   = emp_obj.job_id.name
        if emp_obj.department_id:
            result['emp_unit_bag_usaha']            = emp_obj.department_id.name
        result['emp_no_induk']                  = emp_obj.nik
        result['emp_tanggal_lahir']             = birthday[2]
        result['emp_bulan_lahir']               = birthday[1]
        result['emp_tahun_lahir']               = birthday[0]
        result['emp_kewarganegaraan']           = country
        result['emp_no_identitas']              = ktp
        result['emp_npwp']                      = npwp
        result['emp_email_address']             = emp_obj.work_email
        if emp_obj.mobile_phone:
            if len(emp_obj.mobile_phone)>5:
                result['emp_mobile_area']       = emp_obj.mobile_phone[:4]
                result['emp_mobile_number']     = emp_obj.mobile_phone[4:]
                result['emp_phone']             = emp_obj.mobile_phone
        result['com_phone_area']                = phonearea
        result['com_phone_number']              = phone[1]
        result['com_phone']                     = phonearea+phone[1]
        result['com_phone_ext']                 = emp_obj.extension
        result['emp_nama_pasangan']             = wife_husband_name
        result['emp_tgl_lahir_pasangan']        = wife_husband_birth[2]
        result['emp_bln_lahir_pasangan']        = wife_husband_birth[1]
        result['emp_thn_lahir_pasangan']        = wife_husband_birth[0]
        result['emp_nama_anak1']                = son1_name
        result['emp_tgl_lahir_anak1']           = son1_birthday[2]
        result['emp_bln_lahir_anak1']           = son1_birthday[1]
        result['emp_thn_lahir_anak']            = son1_birthday[0]
        result['emp_nama_anak2']                = son2_name
        result['emp_tgl_lahir_anak2']           = son2_birthday[2]
        result['emp_bln_lahir_anak2']           = son2_birthday[1]
        result['emp_thn_lahir_anak2']           = son2_birthday[0]
        result['emp_nama_anak3']                = son3_name
        result['emp_tgl_lahir_anak3']           = son3_birthday[2]
        result['emp_bln_lahir_anak3']           = son3_birthday[1]
        result['emp_thn_lahir_anak3']           = son3_birthday[0]
        if partner.address:
            result['com_contact_name']          = partner.address[0].name
            result['com_contact_function']      = partner.address[0].function
#            result['com_contact_phone_area']    = phonearea 
            result['com_contact_phone_number']  = phone[1]
#            result['com_contact_fax_area']      = faxarea
            result['com_contact_fax_number']    = fax[1]
            result['com_contact_email']         = partner.address[0].email
            result['com_address1']              = partner.address[0].street
            result['com_address2']              = partner.address[0].street2
            result['com_address']               = partner.address[0].street
            result['com_city']                  = partner.address[0].city
            result['com_kabupaten']             = partner.address[0].state_id
            result['com_fax_area']              = faxarea
            result['com_fax_number']            = fax[1]
        else:
            raise osv.except_osv(_('No Form Available !'), _('No Form Available!'))
        
        try:
            tmp_file = tempfile.mkstemp(".pdf")[1]
            try:
                fill_pdf(addons.get_module_resource('hr_jamsostek','report','pdf', form_name), tmp_file, result)
                with open(tmp_file, "r") as ofile:
                    self.obj = external_pdf(ofile.read())
            finally:
                try:
                    os.remove(tmp_file)
                except:
                    pass # nothing to do
            self.obj.render()
            return (self.obj.pdf, 'pdf')
        except Exception:
            raise osv.except_osv(_('pdf not created !'), _('Please check if package pdftk is installed!'))

report_custom('report.jamsostek.f1.report.print')

class jamsostek_form_report(osv.osv_memory):
    _name = 'form.jamsostek.report'
    _description = 'Form Jamsostek Report'

    _columns = {
         'name': fields.selection([('f1','Form F1'),
                                  ('f1a','Form F1A'),
                                  ('f1b','Form F1B'),
                                  ('f2a','Form F2A'),
                                  ('f3','Form F3'),
                                  ('f3b','Form F3B'),
                                  ('f3c','Form F3C'),
                                  ('f4','Form F4'),
                                  ('f5','Form F5'),
                                  ('f61a','Form F61A'),
                                  ('f6c2','Form F6C2'),
                                  ('fjakons','Form FJakons')],'Form',required=True),
    }

    def print_form_jamsostek_report(self, cr, uid, ids, context=None):
        active_ids = context.get('active_ids',[])
        data = {}
        data['form'] = {}
        data['ids'] = active_ids
        data['form']['name'] = self.browse(cr, uid, ids)[0].name
        print self.browse(cr, uid, ids)[0].name
        return { 'type': 'ir.actions.report.xml', 'report_name': 'jamsostek.f1.report.print', 'datas': data}

jamsostek_form_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
