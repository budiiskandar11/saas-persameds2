from openerp.osv import fields, osv

class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'date_terms_signed' : fields.datetime('Date Terms Signed', help='Date on witch the sales conditions/terms are signed'),
        'print_terms' : fields.boolean('Print Terms', help='If true the sales conditions/terms will be printed on the documents'),
    }

    _defaults = {
        'print_terms' : True,
    }
res_partner()

# vim:sts=4:et
