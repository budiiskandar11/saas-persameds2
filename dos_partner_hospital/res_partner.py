# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

import datetime
from lxml import etree
import math
import pytz
import re

import openerp
from openerp import SUPERUSER_ID
from openerp import pooler, tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.tools.yaml_import import is_comment
from openerp import tools, api

class res_partner(osv.osv):
    _inherit    = 'res.partner'
    _description= 'Partner Inherit'
    _columns    = {
                   'hospital'               : fields.boolean('hospital',size=16),
                   'class'           : fields.selection([('a','A'),
                                                         ('b','B'),
                                                         ('c','C'),
                                                         ('d','D'),
                                                         ('other','Other')
                                                         ],'Class'),
                   'owner'               : fields.selection([('pemda','Pemerintah Daerah'),
                                                         ('swasta','Swasta'),
                                                         ('organisasi','Organisasi'),
                                                         ('angkatan','Angkatan'),
                                                         ('polisi','Polisi'),
                                                         ('kementrian','Kementrian'),
                                                         ('bumn','BUMN')
                                                         ],'Penyelenggara'),
                   
                   }
    _defaults ={
                'is_company' : True,
                }