{
    "name" : "Holiday ABACUS",
    "version" : "1.0",
    "depends" : ["hr","base","hr_holidays"],
    "author" : "DATABIT",
    "description": """This module is aimed to input holidays in a year.
    """,
    "website" : "http://www.databit.co.id",
    "category" : "Custom/Human Resources",
    "init_xml" : [],
    "demo_xml" : [],
    'test': [],
    "update_xml" : [
       "hr_holidays_view.xml",
       "report_view.xml",
       "views/bit_document.xml",
       "bit_payment_view.xml",
       "security/base_security.xml",
       "hr_employee_view.xml",
    ],
    "active": False,
    "installable": True,
}