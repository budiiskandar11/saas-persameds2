{
    "name" : "Training",
    "version" : "1.0",
    "depends" : ["hr","base", "account","dos_hr_indonesia"],
    "author" : "Databit",
    "description": """This module is aimed to handle Training form for each employees.
    """,
    "website" : "http://databit.co.id",
    "category" : "Custom/Human Resources",
    "init_xml" : [],
    "demo_xml" : [],
    'test': [],
    "update_xml" : [
       "hr_training_view.xml",
       "data/dos_training_data.xml"
    ],
    "active": False,
    "installable": True,
}