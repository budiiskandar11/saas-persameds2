# -*- encoding: utf-8 -*-
import os
from openerp.osv import fields, osv
import xmlrpclib
import cStringIO as StringIO
import tempfile
from openerp.report.render import render
import openerp.tools
import openerp.addons

jy_serv=xmlrpclib.ServerProxy("http://localhost:9000/")

class external_pdf(render):

    def __init__(self, pdf):
        render.__init__(self)
        self.pdf = pdf
        self.output_type='pdf'

    def _render(self):
        return self.pdf

def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('utf-8')

def decode_vals(vals): #need to format for str and unicode object-
    dc={}
    for k,v in vals.items():
        k,v = unicode(k),safe_unicode(v) # key and value must the same type str,str
        dc[k]=v
    return dc

def pdf_fill1(orig_pdf,vals):
    vals=decode_vals(vals)
    orig_pdf_abs=os.path.join(os.getcwd(),orig_pdf)
    tmp=os.tempnam()
    print 'filling pdf',orig_pdf,vals

    jy_serv.pdf_fill(orig_pdf_abs,tmp,vals)
    pdf=file(tmp).read()
    os.unlink(tmp)
    return pdf


def pdf_fill(orig_pdf,vals):
    #vals = decode_vals(vals)
    orig_pdf_abs = os.path.join(os.getcwd(),orig_pdf)
    tmp = tempfile.mkstemp(".pdf")[1]
    print "========="
    print 'orig_pdf = ',orig_pdf
    print "========="
    print 'vals = ',vals
    print "========="
    print 'orig_pdf_abs = ',orig_pdf_abs
    print "========="
    tools.pdf_utils.fill_pdf(addons.get_module_resource('ad_account_indonesia','report','pdf','spt_masa_ppn_1111a.pdf'), tmp, vals)
    #tools.pdf_utils.fill_pdf(orig_pdf, tmp, vals)
    print 'rrrrrrrrrrrrrrrrrrr'

    try:
        tools.pdf_utils.fill_pdf(orig_pdf, tmp, vals)
        with open(tmp, "r") as ofile:
            self.obj = external_pdf(ofile.read())
    finally:
        try:
            os.remove(tmp_file)
        except:
            pass # nothing to do
    print "========="
    print "aaaaa"
    print "========="
    
    self.obj.render()
    pdf = self.obj.pdf
    return pdf

def pdf_merge(pdf1,pdf2):
    try:
        tmp1 = tempfile.mkstemp(".pdf")[1]
        tmp2 = tempfile.mkstemp(".pdf")[1]
        tmp3 = tempfile.mkstemp(".pdf")[1]

        file(tmp1,"w").write(pdf1)
        file(tmp2,"w").write(pdf2)

        cmd = "pdftk %s %s cat output %s"%(tmp1,tmp2,tmp3)
        os.system(cmd)
        pdf3=file(tmp3).read()
        os.unlink(tmp1)
        os.unlink(tmp2)
        os.unlink(tmp3)
        return pdf3
    except:
        raise Exception("Failed to merge PDF files")
    
