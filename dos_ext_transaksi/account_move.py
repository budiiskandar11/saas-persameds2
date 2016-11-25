import time
from datetime import datetime

from openerp import workflow
from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp import tools
from openerp.report import report_sxw
import openerp

class account_move(osv.osv):
    _inherit = 'account.move'
    
    _columns = {
            'force_period_allow' : fields.boolean('Force Period Allow'),
                }
    
    def validate(self, cr, uid, ids, context=None):
        if context and ('__last_update' in context):
            del context['__last_update']

        valid_moves = [] #Maintains a list of moves which can be responsible to create analytic entries
        obj_analytic_line = self.pool.get('account.analytic.line')
        obj_move_line = self.pool.get('account.move.line')
        obj_precision = self.pool.get('decimal.precision')
        prec = obj_precision.precision_get(cr, uid, 'Account')
        for move in self.browse(cr, uid, ids, context):
            journal = move.journal_id
            amount = 0
            line_ids = []
            line_draft_ids = []
            company_id = None
            # makes sure we don't use outdated period
            ###
            if move.force_period_allow == True:
                context.update({'force_period_allow': True})
            #else:
            #    print "@@@@@@@@@@@@@@@@@@@", context
            #    context.update({'force_period_allow': False})
            ###
            obj_move_line._update_journal_check(cr, uid, journal.id, move.period_id.id, context=context)
            for line in move.line_id:
                amount += line.debit - line.credit
                line_ids.append(line.id)
                if line.state=='draft':
                    line_draft_ids.append(line.id)

                if not company_id:
                    company_id = line.account_id.company_id.id
                if not company_id == line.account_id.company_id.id:
                    raise osv.except_osv(_('Error!'), _("Cannot create moves for different companies."))

                if line.account_id.currency_id and line.currency_id:
                    if line.account_id.currency_id.id != line.currency_id.id and (line.account_id.currency_id.id != line.account_id.company_id.currency_id.id):
                        raise osv.except_osv(_('Error!'), _("""Cannot create move with currency different from ..""") % (line.account_id.code, line.account_id.name))

            if round(abs(amount), prec) < 10 ** (-max(5, prec)):
                # If the move is balanced
                # Add to the list of valid moves
                # (analytic lines will be created later for valid moves)
                valid_moves.append(move)

                # Check whether the move lines are confirmed

                if not line_draft_ids:
                    continue
                # Update the move lines (set them as valid)

                obj_move_line.write(cr, uid, line_draft_ids, {
                    'state': 'valid'
                }, context, check=False)

                account = {}
                account2 = {}

                if journal.type in ('purchase','sale'):
                    for line in move.line_id:
                        code = amount = 0
                        key = (line.account_id.id, line.tax_code_id.id)
                        if key in account2:
                            code = account2[key][0]
                            amount = account2[key][1] * (line.debit + line.credit)
                        elif line.account_id.id in account:
                            code = account[line.account_id.id][0]
                            amount = account[line.account_id.id][1] * (line.debit + line.credit)
                        if (code or amount) and not (line.tax_code_id or line.tax_amount):
                            obj_move_line.write(cr, uid, [line.id], {
                                'tax_code_id': code,
                                'tax_amount': amount
                            }, context, check=False)
            elif journal.centralisation:
                # If the move is not balanced, it must be centralised...

                # Add to the list of valid moves
                # (analytic lines will be created later for valid moves)
                valid_moves.append(move)

                #
                # Update the move lines (set them as valid)
                #
                self._centralise(cr, uid, move, 'debit', context=context)
                self._centralise(cr, uid, move, 'credit', context=context)
                obj_move_line.write(cr, uid, line_draft_ids, {
                    'state': 'valid'
                }, context, check=False)
            else:
                # We can't validate it (it's unbalanced)
                # Setting the lines as draft
                not_draft_line_ids = list(set(line_ids) - set(line_draft_ids))
                if not_draft_line_ids:
                    obj_move_line.write(cr, uid, not_draft_line_ids, {
                        'state': 'draft'
                    }, context, check=False)
        # Create analytic lines for the valid moves
        for record in valid_moves:
            obj_move_line.create_analytic_lines(cr, uid, [line.id for line in record.line_id], context)

        valid_moves = [move.id for move in valid_moves]
        return len(valid_moves) > 0 and valid_moves or False
    
account_move()

class account_move_line(osv.osv):
    _inherit = "account.move.line"
    
    def _update_check(self, cr, uid, ids, context=None):
        done = {}
        for line in self.browse(cr, uid, ids, context=context):
            err_msg = _('Move name (id): %s (%s)') % (line.move_id.name, str(line.move_id.id))
            if line.move_id.state <> 'draft' and (not line.journal_id.entry_posted):
                raise osv.except_osv(_('Error!'), _('You cannot do this modification on a confirmed entry. You can just change some non legal fields or you must unconfirm the journal entry first.\n%s.') % err_msg)
            if line.reconcile_id:
                raise osv.except_osv(_('Error!'), _('You cannot do this modification on a reconciled entry. You can just change some non legal fields or you must unreconcile first.\n%s.') % err_msg)
            t = (line.journal_id.id, line.period_id.id)
            if t not in done:
                ####Update Context force_period_allow####
                print "line.move_id--------_>>", line.move_id
                if line.force_period_allow == True:
                    context.update({'force_period_allow': True})
                else:
                    context.update({'force_period_allow': False})
                #########################################
                self._update_journal_check(cr, uid, line.journal_id.id, line.period_id.id, context)
                done[t] = True
        return True
    
    _columns = {
            'force_period_allow' : fields.boolean('Force Period Allow'),
                }
    
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
                
                try:
                    force_period_allow = context['force_period_allow']
                except:
                    force_period_allow = False
                    
                print "force_period_allow---------", force_period_allow
                ########Cek silisih Hari post & end period#############
                now         = time.strftime('%Y-%m-%d')
                now         = datetime.strptime(now, '%Y-%m-%d')
                
                end_period  = period.date_stop
                end_period  = datetime.strptime(end_period, '%Y-%m-%d')
                
                delta = (now - end_period).days
                #print "period--------------_>>", period.name, type(period.date_stop), period.date_stop, type(now), now, delta
                #######################################################
                
                if force_period_allow == False or force_period_allow == True and delta > 5:
                    raise osv.except_osv(_('Error!'), _('You can not add/modify entries in a closed period %s of journal %s.') % (period.name, journal.name))
                ###
        if not result:
            jour_period_obj.create(cr, uid, {
                'name': (journal.code or journal.name)+':'+(period.name or ''),
                'journal_id': journal.id,
                'period_id': period.id
            })
        return True
    
    def create(self, cr, uid, vals, context=None, check=True):
        account_obj = self.pool.get('account.account')
        tax_obj = self.pool.get('account.tax')
        move_obj = self.pool.get('account.move')
        cur_obj = self.pool.get('res.currency')
        journal_obj = self.pool.get('account.journal')
        context = dict(context or {})
        if vals.get('move_id', False):
            move = self.pool.get('account.move').browse(cr, uid, vals['move_id'], context=context)
            if move.company_id:
                vals['company_id'] = move.company_id.id
            if move.date and not vals.get('date'):
                vals['date'] = move.date
        if ('account_id' in vals) and not account_obj.read(cr, uid, [vals['account_id']], ['active'])[0]['active']:
            raise osv.except_osv(_('Bad Account!'), _('You cannot use an inactive account.'))
        if 'journal_id' in vals and vals['journal_id']:
            context['journal_id'] = vals['journal_id']
        if 'period_id' in vals and vals['period_id']:
            context['period_id'] = vals['period_id']
        if ('journal_id' not in context) and ('move_id' in vals) and vals['move_id']:
            m = move_obj.browse(cr, uid, vals['move_id'])
            context['journal_id'] = m.journal_id.id
            context['period_id'] = m.period_id.id
        #we need to treat the case where a value is given in the context for period_id as a string
        if 'period_id' in context and not isinstance(context.get('period_id', ''), (int, long)):
            period_candidate_ids = self.pool.get('account.period').name_search(cr, uid, name=context.get('period_id',''))
            if len(period_candidate_ids) != 1:
                raise osv.except_osv(_('Error!'), _('No period found or more than one period found for the given date.'))
            context['period_id'] = period_candidate_ids[0][0]
        if not context.get('journal_id', False) and context.get('search_default_journal_id', False):
            context['journal_id'] = context.get('search_default_journal_id')
        ####
        print "vals--------", vals
        try:
            if vals['force_period_allow']:
                context.update({'force_period_allow': True})
        except:
            context.update({'force_period_allow': False})
        ####
        self._update_journal_check(cr, uid, context['journal_id'], context['period_id'], context)
        move_id = vals.get('move_id', False)
        journal = journal_obj.browse(cr, uid, context['journal_id'], context=context)
        vals['journal_id'] = vals.get('journal_id') or context.get('journal_id')
        vals['period_id'] = vals.get('period_id') or context.get('period_id')
        vals['date'] = vals.get('date') or context.get('date')
        if not move_id:
            if journal.centralisation:
                #Check for centralisation
                res = self._check_moves(cr, uid, context)
                if res:
                    vals['move_id'] = res[0]
            if not vals.get('move_id', False):
                if journal.sequence_id:
                    #name = self.pool.get('ir.sequence').next_by_id(cr, uid, journal.sequence_id.id)
                    v = {
                        'date': vals.get('date', time.strftime('%Y-%m-%d')),
                        'period_id': context['period_id'],
                        'journal_id': context['journal_id']
                    }
                    if vals.get('ref', ''):
                        v.update({'ref': vals['ref']})
                    move_id = move_obj.create(cr, uid, v, context)
                    vals['move_id'] = move_id
                else:
                    raise osv.except_osv(_('No Piece Number!'), _('Cannot create an automatic sequence for this piece.\nPut a sequence in the journal definition for automatic numbering or create a sequence manually for this piece.'))
        ok = not (journal.type_control_ids or journal.account_control_ids)
        if ('account_id' in vals):
            account = account_obj.browse(cr, uid, vals['account_id'], context=context)
            if journal.type_control_ids:
                type = account.user_type
                for t in journal.type_control_ids:
                    if type.code == t.code:
                        ok = True
                        break
            if journal.account_control_ids and not ok:
                for a in journal.account_control_ids:
                    if a.id == vals['account_id']:
                        ok = True
                        break
            # Automatically convert in the account's secondary currency if there is one and
            # the provided values were not already multi-currency
            if account.currency_id and 'amount_currency' not in vals and account.currency_id.id != account.company_id.currency_id.id:
                vals['currency_id'] = account.currency_id.id
                ctx = {}
                if 'date' in vals:
                    ctx['date'] = vals['date']
                vals['amount_currency'] = cur_obj.compute(cr, uid, account.company_id.currency_id.id,
                    account.currency_id.id, vals.get('debit', 0.0)-vals.get('credit', 0.0), context=ctx)
        if not ok:
            raise osv.except_osv(_('Bad Account!'), _('You cannot use this general account in this journal, check the tab \'Entry Controls\' on the related journal.'))

        result = super(account_move_line, self).create(cr, uid, vals, context=context)
        # CREATE Taxes
        if vals.get('account_tax_id', False):
            tax_id = tax_obj.browse(cr, uid, vals['account_tax_id'])
            total = vals['debit'] - vals['credit']
            base_code = 'base_code_id'
            tax_code = 'tax_code_id'
            account_id = 'account_collected_id'
            base_sign = 'base_sign'
            tax_sign = 'tax_sign'
            if journal.type in ('purchase_refund', 'sale_refund') or (journal.type in ('cash', 'bank') and total < 0):
                base_code = 'ref_base_code_id'
                tax_code = 'ref_tax_code_id'
                account_id = 'account_paid_id'
                base_sign = 'ref_base_sign'
                tax_sign = 'ref_tax_sign'
            base_adjusted = False
            for tax in tax_obj.compute_all(cr, uid, [tax_id], total, 1.00, force_excluded=False).get('taxes'):
                #create the base movement
                if base_adjusted == False:
                    base_adjusted = True
                    if tax_id.price_include:
                        total = tax['price_unit']
                    newvals = {
                        'tax_code_id': tax[base_code],
                        'tax_amount': tax[base_sign] * abs(total),
                    }
                    if tax_id.price_include:
                        if tax['price_unit'] < 0:
                            newvals['credit'] = abs(tax['price_unit'])
                        else:
                            newvals['debit'] = tax['price_unit']
                    self.write(cr, uid, [result], newvals, context=context)
                else:
                    data = {
                        'move_id': vals['move_id'],
                        'name': tools.ustr(vals['name'] or '') + ' ' + tools.ustr(tax['name'] or ''),
                        'date': vals['date'],
                        'partner_id': vals.get('partner_id', False),
                        'ref': vals.get('ref', False),
                        'statement_id': vals.get('statement_id', False),
                        'account_tax_id': False,
                        'tax_code_id': tax[base_code],
                        'tax_amount': tax[base_sign] * abs(total),
                        'account_id': vals['account_id'],
                        'credit': 0.0,
                        'debit': 0.0,
                    }
                    self.create(cr, uid, data, context)
                #create the Tax movement
                if not tax['amount'] and not tax[tax_code]:
                    continue
                data = {
                    'move_id': vals['move_id'],
                    'name': tools.ustr(vals['name'] or '') + ' ' + tools.ustr(tax['name'] or ''),
                    'date': vals['date'],
                    'partner_id': vals.get('partner_id',False),
                    'ref': vals.get('ref',False),
                    'statement_id': vals.get('statement_id', False),
                    'account_tax_id': False,
                    'tax_code_id': tax[tax_code],
                    'tax_amount': tax[tax_sign] * abs(tax['amount']),
                    'account_id': tax[account_id] or vals['account_id'],
                    'credit': tax['amount']<0 and -tax['amount'] or 0.0,
                    'debit': tax['amount']>0 and tax['amount'] or 0.0,
                }
                self.create(cr, uid, data, context)
            del vals['account_tax_id']

        recompute = journal.env.recompute and context.get('recompute', True)
        if check and not context.get('novalidate') and (recompute or journal.entry_posted):
            tmp = move_obj.validate(cr, uid, [vals['move_id']], context)
            if journal.entry_posted and tmp:
                move_obj.button_validate(cr,uid, [vals['move_id']], context)
        return result
    
account_move_line()