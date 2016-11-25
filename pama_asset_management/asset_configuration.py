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

from datetime import date,datetime,timedelta
import time
from dateutil import relativedelta
from openerp import models, fields, api, _



class account_asset_group(models.Model):
    _name = 'account.asset.group'
    _description = 'Asset group'

    name = fields.Char("Name", required=True)
    code = fields.Char('Code', select=1)
    
        
class account_asset_class(models.Model):
    _name = 'account.asset.class'
    _description = 'Asset Class'

    name = fields.Char("Name", required=True)
    code = fields.Char('Code',  select=1)
    
        


    
    


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: