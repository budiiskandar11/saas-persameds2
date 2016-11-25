try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from pyPdf import PdfFileWriter, PdfFileReader
import time
import base64
import logging

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools.safe_eval import safe_eval as eval
from openerp.report import report_sxw
from openerp import pooler


# We store the original function
#openerp_create_single_pdf = report_sxw.create_single_pdf

def create_single_pdf(self, cr, uid, ids, data, report_xml, context=None):
    log = logging.getLogger('agaplan_terms_and_conditions')

    res = openerp_create_single_pdf(self, cr, uid, ids, data, report_xml, context)
    if report_xml.report_type != 'pdf':
        return res

    pool = pooler.get_pool(cr.dbname)

    # Check conditions to add or not
    rule_obj = pool.get('term.rule')
    rule_ids = rule_obj.search(cr, uid, [
        ('report_name','=',report_xml.report_name),
    ])

    if not len(rule_ids):
        # No conditions should be added, return regular result
        return res

    valid_rules = []
    for rule in rule_obj.browse(cr, uid, rule_ids, context=context):
        log.debug("Checking rule %s for report %s",
                rule.term_id.name, report_xml.report_name)

        if rule.company_id:
            model_obj = pool.get( data['model'] ).browse(cr, uid, ids[0], context=context)
            if hasattr(model_obj, 'company_id'):
                if rule.company_id.id != model_obj.company_id.id:
                    log.debug("Company id's did not match !")
                    continue
                else:
                    log.debug("Company id's matched !")

        if rule.condition:
            env = {
                'object': pool.get( data['model'] ).browse(cr, uid, ids[0], context=context),
                'report': report_xml,
                'data': data,
                'date': time.strftime('%Y-%m-%d'),
                'time': time,
                'context': context,
            }
            # User has specified a condition, check it and return res when not met
            if not safe_eval(rule.condition, env):
                log.debug("Term condition not met !") 
                continue
            else:
                log.debug("Term condition met !")

        valid_rules += [ rule ]

    output = PdfFileWriter()
    reader = PdfFileReader( StringIO(res[0]) )

    for rule in valid_rules:
        if rule.term_id.mode == 'begin':
            att = PdfFileReader( StringIO(base64.decodestring(rule.term_id.pdf)) )
            [ output.addPage(page) for page in att.pages ]

    for page in reader.pages:
        output.addPage( page )
        for rule in valid_rules:
            if rule.term_id.mode == 'duplex':
                att = PdfFileReader( StringIO(base64.decodestring(rule.term_id.pdf)) )
                [ output.addPage(page) for page in att.pages ]

    for rule in valid_rules:
        if rule.term_id.mode == 'end':
            att = PdfFileReader( StringIO(base64.decodestring(rule.term_id.pdf)) )
            [ output.addPage(page) for page in att.pages ]

    buf = StringIO()
    output.write(buf)
    return (buf.getvalue(), report_xml.report_type)

report_sxw.create_single_pdf = create_single_pdf

# vim:sts=4:et
