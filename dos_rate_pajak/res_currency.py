from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from openerp import api, fields as fields2
import datetime

class res_currency_tax_rate(osv.osv):
    _name = "res.currency.tax.rate"
    _description = "Currency Tax Rate"

    _columns = {
        'name': fields.datetime('Date', required=True, select=True),
        'rate': fields.float('Rate', digits=(12,6), help='The rate of the currency to the currency of rate 1'),
        'currency_id': fields.many2one('res.currency', 'Currency', readonly=True),
        #'currency_rate_type_id': fields.many2one('res.currency.rate.type', 'Currency Rate Type', help="Allow you to define your own currency rate types, like 'Average' or 'Year to Date'. Leave empty if you simply want to use the normal 'spot' rate type"),
        'kp_men': fields.char('Keputusan Menteri'),
    }
    _defaults = {
        'name': lambda *a: time.strftime('%Y-%m-%d'),
    }
    _order = "name desc"
    
res_currency_tax_rate()

class res_currency(osv.osv):
    _inherit = 'res.currency'
    _description = 'res currency'
  
    
    
    @api.v8
    def round_tax(self, amount):
        """ Return `amount` rounded according to currency `self`. """
        #return float_round(amount, precision_rounding=self.rounding)
        return round(amount)

    @api.v7
    def round_tax(self, cr, uid, currency, amount):
        """Return ``amount`` rounded  according to ``currency``'s
           rounding rules.

           :param Record currency: currency for which we are rounding
           :param float amount: the amount to round
           :return: rounded float
        """
        #return float_round(amount, precision_rounding=currency.rounding)
        return round(amount)
    
#     def _get_conversion_rate(self, cr, uid, from_currency, to_currency, context=None):
#         if context is None:
#             context = {}
#         ctx = context.copy()
#         from_currency = self.browse(cr, uid, from_currency.id, context=ctx)
#         to_currency = self.browse(cr, uid, to_currency.id, context=ctx)
#         
#         ###
#         cr.execute('select id from res_currency where base = TRUE')
#         company_currency = cr.fetchone()[0]
#         
#         #print "ctx----->>", company_currency,from_currency,to_currency,ctx['date']
#         if ctx['date'] and from_currency.id <> company_currency:
#             rate_check = False
#             cr.execute('SELECT name FROM res_currency_rate WHERE currency_id = %s AND name = %s',(from_currency.id, ctx['date']))
#             rate_check = cr.fetchone()
#             if not rate_check:
#                 raise osv.except_osv(_('BI Rate'), _('No rate found \n Please Contact your Accounting Staff'))
#         ###
#         if from_currency.rate == 0 or to_currency.rate == 0:
#             date = context.get('date', time.strftime('%Y-%m-%d'))
#             if from_currency.rate == 0:
#                 currency_symbol = from_currency.symbol
#             else:
#                 currency_symbol = to_currency.symbol
#             raise osv.except_osv(_('Error'), _('No rate found \n' \
#                     'for the currency: %s \n' \
#                     'at the date: %s') % (currency_symbol, date))
#         print "to_currency.rate/from_currency.rate", to_currency.rate, "====", from_currency.rate, to_currency.rate/from_currency.rate
#         #return to_currency.rate/from_currency.rate
#         return from_currency.rate / to_currency.rate
    
    def _get_conversion_rate(self, cr, uid, from_currency, to_currency, context=None):
        if context is None:
            context = {}
        ctx = context.copy()
        from_currency = self.browse(cr, uid, from_currency.id, context=ctx)
        to_currency = self.browse(cr, uid, to_currency.id, context=ctx)

        if from_currency.rate == 0 or to_currency.rate == 0:
            date = context.get('date', time.strftime('%Y-%m-%d'))
            if from_currency.rate == 0:
                currency_symbol = from_currency.symbol
            else:
                currency_symbol = to_currency.symbol
            raise osv.except_osv(_('Error'), _('No rate found \n' \
                    'for the currency: %s \n' \
                    'at the date: %s') % (currency_symbol, date))
        return from_currency.rate/to_currency.rate
        #return to_currency.rate/from_currency.rate
    
    
    def _compute(self, cr, uid, from_currency, to_currency, from_amount, round=True, context=None):
        print "XXXXXXXXXXXXXXXXXX777"
        if (to_currency.id == from_currency.id):
            if round:
                return self.round(cr, uid, to_currency, from_amount)
            else:
                return from_amount
        else:
            ######
            try:
                rate = context.get('force_rate')
            except:
                rate = False
                
            print ">>>>>>>>>>>>>", from_amount, rate
                
            ######
            if not rate:
                print "HHHHHHHHHHHHHHHHHHHHHHH***"
                rate = self._get_conversion_rate(cr, uid, from_currency, to_currency, context=context)
            if round:
                return self.round(cr, uid, to_currency, from_amount * rate)
            else:
                return from_amount * rate
    
    def _current_tax_rate(self, cr, uid, ids, name, arg, context=None):
        return self._get_current_tax_rate(cr, uid, ids, context=context)
    
    def _current_tax_rate_silent(self, cr, uid, ids, name, arg, context=None):
        return self._get_current_tax_rate(cr, uid, ids, raise_on_no_rate=False, context=context)
    
    def _get_current_tax_rate(self, cr, uid, ids, raise_on_no_rate=True, context=None):
        print "xxxxxxxxxxxxxxxxxxxxbudi", raise_on_no_rate, context
        if context is None:
            context = {}
        res = {}
        
        date = context.get('date') or time.strftime('%Y-%m-%d')
        
        for id in ids:
            base = self.pool.get('res.currency').browse(cr, uid, [id], context=None)[0].base
            if raise_on_no_rate and base == False:
                #####Check Date Tax Rate####
                cr.execute('SELECT name FROM res_currency_tax_rate '
                           'WHERE currency_id = %s '
                             'AND name <= %s '
                           'ORDER BY name desc LIMIT 1',
                           (id, date))
                 
                if cr.rowcount:
                    rate_tax_date = cr.fetchone()[0]
                    date            = datetime.datetime.strptime(date , '%Y-%m-%d').date()
                    rate_tax_date   = datetime.datetime.strptime(rate_tax_date, '%Y-%m-%d %H:%M:%S').date()
                    delta = (date - rate_tax_date).days
                    print "delta****************88", delta
                    ###Alert Dimatikan sementara###
                    #if delta > 6:
                    #    raise osv.except_osv(_('Error!'),_("Your Invalid Tax Rate"))
                 
                ############################
             
            cr.execute('SELECT rate FROM res_currency_tax_rate '
                       'WHERE currency_id = %s '
                         'AND name <= %s '
                       'ORDER BY name desc LIMIT 1',
                       (id, date))
            if cr.rowcount:
                res[id] = cr.fetchone()[0]
            elif not raise_on_no_rate:
                res[id] = 0
            else:
                currency = self.browse(cr, uid, id, context=context)
                raise osv.except_osv(_('Error!'),_("No currency rate associated for currency '%s' for the given period" % (currency.name)))
        return res
    
    def _get_conversion_tax_rate(self, cr, uid, from_currency, to_currency, context=None):
        print "###_get_conversion_tax_rate###"
        if context is None:
            context = {}
        ctx = context.copy()
        
        from_currency = self.browse(cr, uid, from_currency.id, context=ctx)
        to_currency = self.browse(cr, uid, to_currency.id, context=ctx)
        
        ###
        cr.execute('select id from res_currency where base = TRUE')
        company_currency = cr.fetchone()[0]
        
        #print "BBBBBBBBBBBBB", ctx['date'] and from_currency.id <> company_currency
        
        
        print "ctx----->>", company_currency,from_currency,to_currency,ctx['date']
        
        if ctx['date'] and from_currency.id <> company_currency:
            rate_check = False
            cr.execute('SELECT name FROM res_currency_tax_rate '
                           'WHERE currency_id = %s '
                             'AND name <= %s '
                           'ORDER BY name desc LIMIT 1',
                           (from_currency.id, ctx['date']))
            
            print "rate_check---->>", rate_check
            
            if cr.rowcount:
                rate_tax_date = cr.fetchone()[0]
                date            = datetime.datetime.strptime(ctx['date'] , '%Y-%m-%d').date()
                rate_tax_date   = datetime.datetime.strptime(rate_tax_date, '%Y-%m-%d %H:%M:%S').date()
                delta = (date - rate_tax_date).days
                
                print "delta------>>", delta
                
                if delta > 6:
                    raise osv.except_osv(_('Tax Rate'), _('No rate found \n Please Contact your Accounting Staff'))
        ###
        
        if from_currency.tax_rate == 0 or to_currency.tax_rate == 0:
            date = context.get('date', time.strftime('%Y-%m-%d'))
            
            if from_currency.tax_rate == 0:
                currency_symbol = from_currency.symbol
            else:
                currency_symbol = to_currency.symbol
            raise osv.except_osv(_('Error'), _('No rate found \n' \
                    'for the currency: %s \n' \
                    'at the date: %s') % (currency_symbol, date))
        return from_currency.tax_rate/to_currency.tax_rate

    def _compute_tax(self, cr, uid, from_currency, to_currency, from_amount, round=True, context=None):
        if (to_currency.id == from_currency.id):
            print "AAAAAAAAAAAAAAAA"
            if round:
                return self.round(cr, uid, to_currency, from_amount)
            else:
                return from_amount
        else:
            print "BBBBBBBBBBBBBBB"
            rate = self._get_conversion_tax_rate(cr, uid, from_currency, to_currency, context=context)
            print "rate------------>>", rate
            if round:
                ####
                return self.round_tax(cr, uid, to_currency, from_amount * rate)
                ####
            else:
                return from_amount * rate

    @api.v7
    def compute_tax(self, cr, uid, from_currency_id, to_currency_id, from_amount,
                round=True, context=None):
        context = context or {}
        if not from_currency_id:
            from_currency_id = to_currency_id
        if not to_currency_id:
            to_currency_id = from_currency_id
        xc = self.browse(cr, uid, [from_currency_id,to_currency_id], context=context)
        from_currency = (xc[0].id == from_currency_id and xc[0]) or xc[1]
        to_currency = (xc[0].id == to_currency_id and xc[0]) or xc[1]
        return self._compute_tax(cr, uid, from_currency, to_currency, from_amount, round, context)
    
    @api.v8
    def compute_tax(self, from_amount, to_currency, round=True):
        print "compute_tax--------------------->>", self.name, from_amount, to_currency, round
        """ Convert `from_amount` from currency `self` to `to_currency`. """
        assert self, "compute from unknown currency"
        assert to_currency, "compute to unknown currency"
        # apply conversion rate
        if self == to_currency:
            to_amount = from_amount
        else:
            to_amount = from_amount * self._get_conversion_tax_rate(self, to_currency)
        # apply rounding
        
        print "#################@@@@@@@@@@@@@@", round, to_currency.round_tax(to_amount), to_amount
        ####
        print "TTTTTTTTTTTT", to_currency.round_tax(to_currency.round(to_amount)) if round else to_amount
        return to_currency.round_tax(to_currency.round(to_amount)) if round else to_amount
        ####
        
    def computerate(self, cr, uid, from_currency_id, to_currency_id, from_amount, round=True, currency_rate_type_from=False, currency_rate_type_to=False, context=None):
        if not context:
            context = {}
        if not from_currency_id:
            from_currency_id = to_currency_id
        if not to_currency_id:
            to_currency_id = from_currency_id
        xc = self.browse(cr, uid, [from_currency_id,to_currency_id], context=context)
        from_currency = (xc[0].id == from_currency_id and xc[0]) or xc[1]
        to_currency = (xc[0].id == to_currency_id and xc[0]) or xc[1]
        if (to_currency_id == from_currency_id) and (currency_rate_type_from == currency_rate_type_to):
            if round:
                return self.round(cr, uid, to_currency, from_amount)
            else:
                return from_amount
        else:
            context.update({'currency_rate_type_from': currency_rate_type_from, 'currency_rate_type_to': currency_rate_type_to})
#             rate = self._get_conversion_rate(cr, uid, from_currency, to_currency, context=context)
            from_currency = self.pool.get('res.currency.tax.rate').search(cr, uid, [('currency_id','=',from_currency_id)], context=context)
            from_currency1 = self.pool.get('res.currency.tax.rate').browse(cr, uid, from_currency, context=context)
            rate = {}
            i = 0;
            for f in from_currency1:
#                 print f.name
                if context['date'] == f.name:
#                     print "]]]]]]]]]]]]]]]]True",f.name,"[[[[[[[[[[[[[[[[[[",f.rate
                    rate[i] = f.rate
                    i+=1
#                     return from_amount * f.rate
                else:
                    if context['date'] > f.name:
#                         print "]]]]]]]]]]]]]]]]",f.name,"[[[[[[[[[[[[[[[[[[",f.rate
#                         return from_amount * f.rate
                        rate[i] = f.rate
                        i+=1
    
            if rate.has_key(0):          
                if round:
    #                 print "=========",from_amount / rate[0]
                    return self.round(cr, uid, to_currency, from_amount / rate[0])
                else:
    #                 print "=========",from_amount / rate[0]
                    return from_amount / rate[0]
            else:
                raise osv.except_osv(_('Warning!'), _('Please Insert Rate Pajak'))
                
    
    _columns = {
        'rate_tax_ids'  : fields.one2many('res.currency.tax.rate', 'currency_id', string='Res Currency'),
        'tax_rate'      : fields.function(_current_tax_rate, string='Current Tax Rate', digits=(12,6),
            help='The rate of the currency to the currency of rate 1.'),
        'tax_rate_silent': fields.function(_current_tax_rate_silent, string='Current Tax Rate', digits=(12,6),
            help='The rate of the currency to the currency of rate 1 (0 if no rate defined).'),
        'visible': fields.boolean('Visible'),
    }

res_currency()