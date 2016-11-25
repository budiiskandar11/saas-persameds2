##############################################################################
#
#    Copyright (C) 2011 ADSOFT OpenERP Partner Indonesia
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

from openerp.osv import osv, fields

class res_country_state(osv.osv):
    _inherit = "res.country.state"
    _columns = {
        'name': fields.char('State/Province', size=64, required=True , translate=True),
        'kabupaten_line': fields.one2many('res.kabupaten', 'state_id', 'Kabupaten'),
    }
res_country_state()

class res_kabupaten(osv.osv):
    _name = "res.kabupaten"
    _description = "List Kabupaten"
    _columns = {
        'name': fields.char('Kabupaten', size=64, required=True , translate=True),
        'state_id': fields.many2one('res.country.state',"Name"),
        'kecamatan_line': fields.one2many('res.kecamatan', 'kabupaten_id', 'Kecamatan'),
    }
res_kabupaten()

class res_kecamatan(osv.osv):
    _name = "res.kecamatan"
    _description = "List Kecamatan"
    _columns = {
        'name': fields.char('Kecamatan', size=64, required=True , translate=True),
        'state_id': fields.many2one('res.country.state',"State/Province"),
        'kabupaten_id': fields.many2one('res.kabupaten',"Kabupaten"),
    }
res_kecamatan()
