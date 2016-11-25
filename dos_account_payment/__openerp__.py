# -*- coding: utf-8 -*-
##############################################################################
#
#    account_optimization module for OpenERP, Account Optimizations
#    Copyright (C) 2011 Thamini S.à.R.L (<http://www.thamini.com) Xavier ALT
#
#    This file is a part of account_optimization
#
#    account_optimization is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    account_optimization is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Account Payment Administration",
    "version": "1.0",
    "author": "DATABIT",
    'complexity': "easy",
    "category": "Account Voucher",
    "description": """
    
    This module aim to make payment administration such as:
    * Cash
    * Non Payment Administration
    * Transfer
    * Check
    * Giro
    * Credit Card
    * Debit Card
    Form Kwitansi/Receipt at Customer Payment / Supplier Payment
    Form Print Voucher at Customer Payment / Supplier Payment
    Form Print Cheque at Customer Payment / Supplier Payment
    """,
    "website" : "http://www.databit.co.id",
    "images" : [],
    'depends': ['base',
                'account',
                'account_voucher',
                'purchase',
#                 'dos_amount2text_idr',
                'report_webkit'],
    'init_xml': [
    ],
    'demo_xml': [
    ],
    'update_xml': [
         "report/report_view.xml",
#         "template_mako.xml",
        "report/qweb_cheque.xml",
        "check_sequence.xml",
#         "security/ir.model.access.csv",
        "account_check_view.xml",
        "account_voucher.xml",
        "letter_credit_view.xml",
    ],
    "init_xml": [],
    "demo_xml" : [],
    'test': [],
    'installable': True,
    #'application': True,
    'auto_install': False,
    'certificate': '',
    "css": [],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: