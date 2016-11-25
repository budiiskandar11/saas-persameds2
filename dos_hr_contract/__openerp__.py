{
    "name"          : "Human Resources for Contract Management",
    "version"       : "1.0",
    "depends"       : ["hr","base","hr_contract","hr_payroll"],
    "author"        : "DATABIT",
    "description"   : """
Description
===========

This module consists of so many features related to Human Resources module, e.g:

- Employee's Contracts

""",
    "website"       : "http://databit.co.id",
    "category"      : "Human Resources",
    "init_xml"      : [],
    "demo_xml"      : [],
    'test'          : [],
    "data"          : [
                       ],
    "update_xml"    : [
                       'wizard/contract_revision_view.xml',
                       'hr_contract_view.xml',
                        "views/pkwt_doc.xml",
                        "views/exit_interview.xml",
                        "report_view.xml",
                        "res_company_view.xml",

                       ],
    "active"        : False,
    "installable"   : True,
}