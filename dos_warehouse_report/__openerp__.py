#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2009 ADSOFT - OpenERP Partner Indonesia
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name" : "Warehouse Report Template",
    "version" : "0.1",
    'category': 'Custom Modules/Tools',
    "depends" : ['base','report_webkit', 'stock'],
    "author" : "Databit",
    "website" : "http://www.databit.co.id",
    "description": """
       Report Surat Jalan
    """,
    "init_xml"      : [],
    "demo_xml"      : [],
    "data"          : [
                       'report/report_stock_format_paper.xml',
                       'report/stock_report.mako',
                       'report/stock_report_view.xml',
                    'wizard/stock_report.xml',
                    'report/warehouse_header_footer.xml',
                    'report/wr_header_form.xml',
                    'stock_view.xml',
                    ],
    "installable"   : True,
}
