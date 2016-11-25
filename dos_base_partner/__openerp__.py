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
    "name" : "Partner Custom Databit",
    "version" : "0.1",
    'category': 'Custom Modules/Tools',
    "depends" : ['base',],
    "author" : "Databit",
    "website" : "http://www.databit.co.id",
    "description": """
        - Terdapat Penambahan Field 
            * Birthday
            * Hobi
            * Wife
            * Favorit Book
            * Favorit Food
    """,
    "init_xml"      : [],
    "demo_xml"      : [],
    "data"          : [
                    'security/ir.model.access.csv',
                    'res_partner_view.xml',
                    'partner_sequence.xml',
                    'res_kabupaten.xml',
                    "data/res.country.state.csv",
                    "data/res.kabupaten.csv",
                    "data/res.kecamatan.csv",
                    
                    ],
    "installable"   : True,
}
