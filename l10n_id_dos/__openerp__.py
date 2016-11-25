#!/usr/bin/python
# -*- coding: utf-8 -*-
##############################################################################
#
#   Alam Dewata Utama, PT    
#   Copyright (C) 2010-2013 ADSOft (<http://www.adsoft.co.id>). 
#   All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name"          : "Indonesian - Accounting",
    "version"       : "1.0",
    "author"        : "DATABIT - OpenERP Partner Indonesia",
    "category"      : "Localization/Account Charts",
    'complexity'    : "easy",    
    "description"   : """
Chart of Account for Indonesia by databit
=========================================

Indonesian accounting chart and localization Indonesia by databit    
    """,
    "website"       : "http://www.databit.co.id",
    'images'        : [],
    "init_xml"      : [],
    "depends"       : ["account","account_chart"],
    "update_xml"    : ["coa_indonesia.xml"],
    "demo_xml"      : [],
    'test'          : [],
    "active"        : False,
    "installable"   : True,
    'auto_install'  : False,    
    'certificate'   : '',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: