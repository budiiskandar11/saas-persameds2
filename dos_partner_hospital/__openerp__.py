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
    "name" : "Hospital List",
    "version" : "0.1",
    'category': 'Custom Modules/Tools',
    "depends" : ['base',],
    "author" : "Databit",
    "website" : "http://www.databit.co.id",
    "description": """
        Daftar Rumah Sakit di Indonesia 
    """,
    "init_xml"      : [],
    "demo_xml"      : [],
    "data"          : [
                    
                    'partner_inherit_view.xml',
                    #'data/res.partner.csv',
                    
                    ],
    "installable"   : True,
}