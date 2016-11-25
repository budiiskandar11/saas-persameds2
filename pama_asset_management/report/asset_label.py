# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2011 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2011 ChriCar Beteiligungs- und Beratungs- GmbH (<http://www.camptocamp.com>).
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
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import tempfile
import base64
from PIL import Image
import io, StringIO


import logging

try:
    import qrcode
    qr_mod = True
except:
    qr_mod = False

class asset_inherit(osv.osv):
    _inherit = "account.asset.asset"
    
    def _asset_qrcode(self, cr, uid, ids, name, args, context=None):
        _logger = logging.getLogger(__name__)

        res = {}
        min_size = 50
        size = min_size, min_size
        for ass in self.browse(cr, uid, ids, context=context):
            if ass.state == 'open' and qr_mod == True:
                number  = ass.asset_number
                name    = ass.name
                category = ass.category_id.name
                partner = ass.company_id.name
                value = str(ass.purchase_value)
                date = ass.purchase_date
                book = str(ass.value_residual)
                display = _('Code Ini Untuk Mengontrol Asset')

                lf ='\n'
                qr_string = lf.join([partner,category,number,name,date,value,book,display])
                _logger.debug('FGF QR string %s', qr_string)
                
               
                
                if len(qr_string) > 331:
                    raise osv.except_osv (_('Error'), _('QR string "%s" length %s exceeds 331 bytes') % (qr_string, len(qr_string)))
                #qr = qrencode.encode_scaled(qr_string,min_size,2)
                #f = tempfile.TemporaryFile(mode="r+")
                #qrCode = qr[2]
                #qrCode.save(f,'png')
                #f.seek(0)
                #qr_pic = base64.encodestring(f.read())            
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_M,
                    box_size=20,
                    border=4,
                )
                qr.add_data(qr_string)
                qr.make(fit=True)

                qr_pic = qr.make_image()
                _logger.debug('FGF QR pic %s', qr_pic)
                f = tempfile.TemporaryFile(mode="r+")
                qr_pic.save(f,'png')
                f.seek(0)
                qr_pic1 = base64.encodestring(f.read())            

                res[ass.id] = qr_pic1
            else:
                print ">>>>>>>>>>>>>>>>>>>", "kesini"
                res[ass.id] = False
        return res
    
    _columns = {
                'asset_qr_code' : fields.function(_asset_qrcode, method=True, string='QR Code', type='binary'),
                }
asset_inherit()
