{
    "name": "Terms and Conditions",
    "version": "0.1",
    "description": """
    Module that gives the possibility to add custom terms and conditions to reports
    """,
    "category": "Generic Modules/Base",
    "author": "Agaplan",
    "website": "http://www.agaplan.eu",
    "depends": [
        "base",
    ],
    "init": [],
    "update_xml": [
        'views/term_view.xml',
        'views/partner_view.xml',
        'security/ir.model.access.csv',
    ],
    "demo": [],
    "test": [],
    "installable": True,
}
# vim:sts=4:et
