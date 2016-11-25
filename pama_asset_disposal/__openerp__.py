# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2015 BroadTech IT Solutions Pvt Ltd.
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

{
    'name': 'Asset Disposal For Pama',
    'version': '1.01',
    'depends': ['pama_asset_management'],
    'author': 'BroadTech IT Solutions Pvt Ltd',
    'description': """
Financial and accounting asset disposal.
==========================================

This Module manages asset disposal.

    """,
    'website': 'www.broadtech-innovations.com',
    'category': 'Accounting & Finance',
    'sequence': 33,
    'demo': [ ],
    'test': [ ],
    'data': [
        'security/ir.model.access.csv',
        'views/asset_disposal_view.xml',
        'views/asset_accountant_view.xml',
        'asset_disposal_sequence.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

