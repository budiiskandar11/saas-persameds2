{
    "name" : "BPJS",
    "version" : "1.0",
    "depends" : ["hr","hr_payroll",
                 "dos_hr_indonesia",
                 #"ad_hr_overtime"
                 ],
    "author" : "DATABIT",
    "description": """This module is aimed to handle BPJS form for each employees.
    """,
    "website" : "http://www.databit.co.id",
    "category" : "Custom/Human Resources",
    "init_xml" : [],
    "demo_xml" : [],
    'test': [],
    "update_xml" : [
                    "hr_contract_view.xml",
                    "hr_employee_view.xml",
                    "hr_bpjs_tk_view.xml",
                    "hr_bpjs_kes_view.xml",
                    "hr_dplk_view.xml",
                    "res_company_view.xml",
                    "hr_bpjs_register_view.xml",
                    "wizard/bpjs_generate_view.xml",
                    
       #"wizard/print_form_jamsostek_view.xml"
       
    ],
    "active": False,
    "installable": True,
}