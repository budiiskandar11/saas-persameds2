from openerp.osv import fields, osv

class term_term(osv.osv):
    _name = "term.term"
    _description = "Terms and conditions"

    _columns = {
        'name' : fields.char('Name', size=64, required=True ),
        'pdf': fields.binary('PDF File', help="The PDF file to attach to the report", required=True),
        'mode': fields.selection([('begin','Before report'),('end','After report'),('duplex','Every other page')], string="Insertion mode", required=True),
        'term_rule_ids' : fields.one2many('term.rule','term_id','Uses',help='reports where the term is used')
    }
term_term()

class term_rule(osv.osv):
    _name = 'term.rule'
    _description = 'Rules to define where the linked term is to be used.'

    _columns = {
        'sequence': fields.integer('Sequence'),
        'term_id' : fields.many2one('term.term','Term', required=True),
        'company_id' : fields.many2one('res.company','Company'),
        'report_id' : fields.many2one('ir.actions.report.xml', 'Report', required=True),
        'report_name': fields.related('report_id','report_name', type="char", string='Report Name', readonly=True),
        'condition' : fields.char('Condition', size=128, help='condition on when to print the therm'),
    }

    _defaults = {
        'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'term.rule', context=c),
    }
term_rule()

class report_xml(osv.osv):
    _inherit = 'ir.actions.report.xml'

    _columns = {
        'term_rule_ids' : fields.one2many('term.rule','report_id',help='List of possible terms to be added.')
    }
report_xml()

class res_company(osv.osv):
    _inherit = 'res.company'

    _columns = {
        'term_rule_ids' : fields.one2many('term.rule','company_id',help='List of terms for this company.')
    }
res_company()

# vim:sts=4:et
