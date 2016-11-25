{
    "name": "Extra Transaksi",
    "version": "1.0",
    "depends": ['base','account','hr'],
    "author": "DATABIT",
    "category": "",
    "description": """
       Extra Transaksi
    """,
    "init_xml": [],
    'update_xml': [
            'security/ir.model.access.csv',
            "ext_transaksi_view.xml",
                   
    ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
