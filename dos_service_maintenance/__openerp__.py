# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2015 Broadtech IT Solutions Pvt Ltd.
#    (http://wwww.broadtech-innovations.com)
#    contact@broadtech-innovations.com
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
####################################################################

{
    'name': 'Installation and Service',
    'version': '1.0',
    'depends': ['sale', 'hr'],
    'author': 'Databit Solusi Indonesia',
    'description': """
This module create to record installation and Maintenance 

    """,
    'website': 'www.databit.co.id',
    'category': 'Installation and Service',
    'sequence': 32,
    'demo': [ ],
    'test': [ ],
    'data': [
             'report/persamed_header_footer.xml',
             'report/install_report.xml',
             'stock_view_inherit.xml',
            'installation_sequence.xml',
           'installation_view.xml',
         
            ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: