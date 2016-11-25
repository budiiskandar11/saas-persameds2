{
    "name"          : "Human Resources for Duty Trip",
    "version"       : "1.0",
    "depends"       : ["hr","base","dos_base"],
    "author"        : "DATABIT",
    "description"   : """
Description
===========

This module consists of so many features related to Human Resources module, e.g:

- Employee's Duty Trip

""",
    "website"       : "http://databit.co.id",
    "category"      : "Human Resources",
    "init_xml"      : [],
    "demo_xml"      : [],
    'test'          : [],
    "data"          : [
                       ],
    "update_xml"    : [
                       "duty_trip_view.xml",
                       "report_view.xml",
                       "views/pa_template.xml",
                       "views/sppd_template.xml",
                       "duty_trip_sequence.xml",
                       "report/duty_trip_report_view.xml",
                       ],
    "active"        : False,
    "installable"   : True,
}