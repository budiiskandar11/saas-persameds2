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

from openerp import fields, models, api, _

class account_asset_category(models.Model):
    _inherit = "account.asset.category"

    account_disposal_id             = fields.Many2one('account.account', required=True,string='Disposal Account', )
    account_gainloss_disposal_id    = fields.Many2one('account.account', required=True,string='Disposal Gain/ Loss Account', )
    account_transit_id              = fields.Many2one('account.account', required=True,string='Transit Account', )


class account_asset_asset(models.Model):
    _inherit = "account.asset.asset"
    
    asset_disposal = fields.Boolean(string='Asset Disposal', readonly=True,)
    
    