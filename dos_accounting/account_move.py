import time
from datetime import datetime

from openerp import workflow
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp import tools
from openerp.report import report_sxw
import openerp

class account_move_line(osv.osv):
    _inherit = "account.move.line"

    def _update_journal_check(self, cr, uid, journal_id, period_id, context=None):
        journal_obj = self.pool.get('account.journal')
        period_obj = self.pool.get('account.period')
        jour_period_obj = self.pool.get('account.journal.period')
        cr.execute('SELECT state FROM account_journal_period WHERE journal_id = %s AND period_id = %s', (journal_id, period_id))
        result = cr.fetchall()
        journal = journal_obj.browse(cr, uid, journal_id, context=context)
        period = period_obj.browse(cr, uid, period_id, context=context)
        for (state,) in result:
            if state == 'done':
                ###
                print "UID---------->>", uid
                force_period_allow = self.pool.get('res.users').browse(cr, uid, [uid], context=None)[0].force_period
                if force_period_allow == False:
                    raise osv.except_osv(_('Error!'), _('You can not add/modify entries in a closed period %s of journal %s.') % (period.name, journal.name))
                ###
        if not result:
            jour_period_obj.create(cr, uid, {
                'name': (journal.code or journal.name)+':'+(period.name or ''),
                'journal_id': journal.id,
                'period_id': period.id
            })
        return True
    
    _columns = {}
    
account_move_line()