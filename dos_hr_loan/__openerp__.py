{
    "name": "Loan Management",
    "version": "1.0",
    "depends": ['base','hr','dos_hr_indonesia'],
    "author": "Databit",
    "category": "Accounting & Finance",
    "description": """
        Pinjaman Karyawan
    """,
    "init_xml": [],
    'update_xml': [
        'loan_management_view.xml',
        'loan_management_workflow.xml',
        #'user_view.xml'
    ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
