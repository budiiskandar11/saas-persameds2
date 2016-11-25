# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Budi Iskandar - Databit (budiiskandar@databit.co.id)
#    Copyright 2014 Databit Solusi Indonesia
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
    'name'      : 'Employee Enhancement Data for Abacus',
    'version'   : '0.1',
    'author'    : 'DATABIT',
    'category'  : 'Human Resource Management',
    'depends'   : ['hr','hr_contract','dos_hr_contract'],
    'description': """
    Menambahkan Employee Number
    """,
    'website'   : 'http://www.databit.co.id/',
    'data'      : [],
    'tests'     : [],
    "update_xml": [
                    "res_partner_view.xml",
                    "hr_employee_number_view.xml",
                    "hr_personal_info_view.xml",
                    "hr_ptkp_view.xml",
                    "hr_education_view.xml",
                    # "job_view.xml",
                    "hr_resign_view.xml",
                    "report/hr_report_view.xml"
                    ],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
    'application': False,
}