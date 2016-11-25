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
    'name': 'Assets Management For Pama',
    'version': '1.0',
    'depends': ['account_asset'],
    'author': 'Broadtech IT Solutions Pvt Ltd',
    'description': """
Financial and accounting asset management.
==========================================

This Module manages the assets owned by a company or an individual. It will keep 
track of depreciation's occurred on those assets. And it allows to create Move's 
of the depreciation lines.

    """,
    'website': 'www.broadtech-innovations.com',
    'category': 'Accounting & Finance',
    'sequence': 32,
    'demo': [ ],
    'test': [ ],
    'data': [
             'wizard/asset_register_split_view.xml',
            'wizard/asset_register_merge_view.xml',
             
#         'security/account_asset_security.xml',
         'security/ir.model.access.csv',
#         'wizard/account_asset_change_duration_view.xml',
#         'wizard/wizard_asset_compute_view.xml',
         'account_asset_view.xml',
         'account_asset_sequence_view.xml',
         'asset_extra_comptable_view.xml',
         'asset_register.xml',
         'product_view.xml',
         'report/report_view.xml',
         'report/account_asset_report_view_inherit.xml',
         
         
#         'report/account_asset_report_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

