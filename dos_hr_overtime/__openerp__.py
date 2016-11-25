{
    "name" : "Overtime Submission",
    "version" : "1.0",
    "depends" : ["hr","hr_attendance","dos_hr_holiday_year"],
    "author" : "Databit",
    "description": """This module is aimed to handle overtime submission.
    """,
    "website" : "http://www.databit.co.id",
    "category" : "Custom/Human Resources",
    "init_xml" : [],
    "demo_xml" : [],
    'test': [],
    "update_xml" : [
        "hr_overtime_view.xml",
        "hr_employee_level.xml",
        "report/print_overtime_recapitulation_view.xml",
        "report_view.xml",
        "views/overtime_form.xml",
    ],
    "active": False,
    "installable": True,
}