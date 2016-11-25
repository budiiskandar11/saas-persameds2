{
    "name"          : "Rate Pajak",
    "version"       : "1.0",
    'depends'       : [
                    'base',
                    ],
    "author"        : "Databit Solusi Indonesia",
    "description"   : """Rate Pajak Indonesia""",
    "website"       : "https://www.databit.co.id/",
    'category'      : 'UKM PACKAGE,SME PACKAGE,ENTERPRICE PACKAGE',
    "init_xml"      : [],
    "demo_xml"      : [],
    'test'          : [],
    "data"          : [
#                         'security/ir.model.access.csv',
                        "res_currency_view.xml",
                       ],
    'installable': True,
    'auto_install': False,
}