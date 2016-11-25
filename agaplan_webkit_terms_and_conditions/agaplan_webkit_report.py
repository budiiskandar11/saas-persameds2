from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import pooler, tools
from openerp.tools.safe_eval import safe_eval as eval
from openerp.addons.report_webkit.webkit_report import webkit_report_extender

import time
import base64
import logging

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from pyPdf import PdfFileWriter, PdfFileReader
except ImportError:
    raise osv.except_osv(
        "agaplan_terms_and_conditions needs pyPdf",
        """To install the module "agaplan_terms_and_conditions" please ask your administrator to install the pyPdf package."""
    )

try:
    from openerp.addons.report_webkit.webkit_report import WebKitParser
except ImportError:
    raise osv.except_osv(
        "agaplan_webkit_terms_and_conditions needs to see the module report_webkit, is it not in your addons_path ?",
        """Please ask your administrator to put the 'report_webkit' module in the OpenERP addons_path"""
    )

_logger = logging.getLogger(__name__)

# We store the original function
webkit_create_single_pdf = WebKitParser.create_single_pdf

def create_single_pdf(self, cr, uid, ids, data, report_xml, context=None):
    log = logging.getLogger('agaplan_terms_and_conditions')

    res = webkit_create_single_pdf(self, cr, uid, ids, data, report_xml, context)
    if report_xml.report_type != 'webkit':
        log.warn("report_type was not what we expected (%s) thus we return regular result.", report_xml.report_type)
        return res

    pool = pooler.get_pool(cr.dbname)

    # Check conditions to add or not
    rule_obj = pool.get('term.rule')
    if not rule_obj:
        # Module is not installed
        return res

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
            model_obj = pool["ir.model.data"].browse(cr, uid, ids[0], context=context)
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
            map(output.addPage, att.pages)

    for page in reader.pages:
        output.addPage( page )
        for rule in valid_rules:
            if rule.term_id.mode == 'duplex':
                att = PdfFileReader( StringIO(base64.decodestring(rule.term_id.pdf)) )
                map(output.addPage, att.pages)

    for rule in valid_rules:
        if rule.term_id.mode == 'end':
            att = PdfFileReader( StringIO(base64.decodestring(rule.term_id.pdf)) )
            map(output.addPage, att.pages)

    buf = StringIO()
    output.write(buf)
    return (buf.getvalue(), res[1])

WebKitParser.create_single_pdf = create_single_pdf

# vim:sts=4:et
