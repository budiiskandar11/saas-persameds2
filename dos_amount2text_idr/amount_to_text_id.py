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

#-------------------------------------------------------------
#ENGLISH
#-------------------------------------------------------------
from openerp.tools.translate import _

to_19_en = ( 'Zero',  'One',   'Two',  'Three', 'Four',   'Five',   'Six',
          'Seven', 'Eight', 'Nine', 'Ten',   'Eleven', 'Twelve', 'Thirteen',
          'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen' )
tens_en  = ( 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety')
denom_en = ( '',
          'Thousand',     'Million',         'Billion',       'Trillion',       'Quadrillion',
          'Quintillion',  'Sextillion',      'Septillion',    'Octillion',      'Nonillion',
          'Decillion',    'Undecillion',     'Duodecillion',  'Tredecillion',   'Quattuordecillion',
          'Sexdecillion', 'Septendecillion', 'Octodecillion', 'Novemdecillion', 'Vigintillion' )

to_19_id = ( 'nol',  'satu',   'dua',  'tiga', 'empat',   'lima',   'enam',
          'tujuh', 'delapan', 'sembilan', 'sepuluh',   'sebelas', 'dua belas', 'tiga belas',
          'empat belas', 'lima belas', 'enam belas', 'tujuh belas', 'delapan belas', 'sembilan belas' )
tens_id  = ( 'dua puluh', 'tiga puluh', 'empat puluh', 'lima puluh', 'enam puluh', 'tujuh puluh', 'delapan puluh', 'sembilan puluh')
denom_id = ( '', 'ribu',
	  'juta', 'miliar', 'biliun', 'triliun',       'quadriliun',
          'ribu',     'juta',         'billion',       'trillion',       'quadrillion',
          'Quintillion',  'Sextillion',      'Septillion',    'Octillion',      'Nonillion',
          'Decillion',    'Undecillion',     'Duodecillion',  'Tredecillion',   'Quattuordecillion',
          'Sexdecillion', 'Septendecillion', 'Octodecillion', 'Novemdecillion', 'Vigintillion' )

to_19 = ( 'nol',  'satu',   'dua',  'tiga', 'empat',   'lima',   'enam',
          'tujuh', 'delapan', 'sembilan', 'sepuluh',   'sebelas', 'dua belas', 'tiga belas',
          'empat belas', 'lima belas', 'enam belas', 'tujuh belas', 'delapan belas', 'sembilan belas' )
tens  = ( 'dua puluh', 'tiga puluh', 'empat puluh', 'lima puluh', 'enam puluh', 'tujuh puluh', 'delapan puluh', 'sembilan puluh')
denom = ( '', 'ribu',
	  'juta', 'miliar', 'biliun', 'triliun',       'quadriliun',
          'ribu',     'juta',         'billion',       'trillion',       'quadrillion',
          'Quintillion',  'Sextillion',      'Septillion',    'Octillion',      'Nonillion',
          'Decillion',    'Undecillion',     'Duodecillion',  'Tredecillion',   'Quattuordecillion',
          'Sexdecillion', 'Septendecillion', 'Octodecillion', 'Novemdecillion', 'Vigintillion' )

# convert a value < 100 to English.
def _convert_nn(val):
    if val < 20:
        return to_19[val]
    for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens)):
        if dval + 10 > val:
            if val % 10:
                return dcap + ' ' + to_19[val % 10]
            return dcap

# convert a value < 1000 to english, special cased because it is the level that kicks 
# off the < 100 special case.  The rest are more general.  This also allows you to
# get strings in the form of 'forty-five hundred' if called directly.
def _convert_nnn(val):
    word = ''
    (mod, rem) = (val % 100, val // 100)
    if rem == 1:
        word = 'seratus'
        if mod > 0:
            word = word + ' '    
    elif rem > 1:
        word = to_19[rem] + ' ratus'
        if mod > 0:
            word = word + ' '
    if mod > 0:
        word = word + _convert_nn(mod)
    return word

def english_number(val):
    if val < 100:
        return _convert_nn(val)
    if val < 1000:
        return _convert_nnn(val)
    for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom))):
        if dval > val:
	    mod = 1000 ** didx
            l = val // mod
            r = val - (l * mod)
            ret = _convert_nnn(l) + ' ' + denom[didx]
            if r > 0:
                ret = ret + ' ' + english_number(r)
	    if val < 2000:
	        ret = ret.replace("satu ribu","seribu")
	    return ret

def amount_to_text(number, currency):
    number = '%.2f' % number
    units_name = ' ' + cur_name(currency) + ' '
    list = str(number).split('.')
    start_word = english_number(int(list[0]))
    end_word = english_number(int(list[1]))
    cents_number = int(list[1])
    cents_name = (cents_number > 1) and 'sen' or 'sen'
    final_result_sen = start_word + units_name + end_word +' '+cents_name
    final_result = start_word + units_name
    if end_word == 'nol':
	   final_result = final_result
    else:
	   final_result = final_result_sen
    
    return final_result[:1].upper()+final_result[1:].lower()

def cur_name(cur="idr"):
    #print cur
    cur = cur.lower()
    if cur=="all":
        return "Leke"
    if cur=="usd":
        return "Dollars"
    if cur=="afn":
        return "Afghanis"
    if cur=="ars":
        return "Pesos"
    if cur=="awg":
        return "Guilders (also called Florins)"
    if cur=="aud":
        return "Dollars"
    if cur=="azn":
        return "New Manats"
    if cur=="bsd":
        return "Dollars"
    if cur=="bbd":
        return "Dollars"
    if cur=="byr":
        return "Rubles"
    if cur=="bzd":
        return "Dollars"
    if cur=="bmd":
        return "Dollars"
    if cur=="bob":
        return "Bolivianos"
    if cur=="bam":
        return "Convertible Marka"
    if cur=="bwp":
        return "Pulas"
    if cur=="bgn":
        return "Leva"
    if cur=="brl":
        return "Reais"
    if cur=="gbp":
        return "Pounds"
    if cur=="bnd":
        return "Dollars"
    if cur=="khr":
        return "Riels"
    if cur=="cad":
        return "Dollars"
    if cur=="kyd":
        return "Dollars"
    if cur=="clp":
        return "Pesos"
    if cur=="cny":
        return "Yuan Renminbi"
    if cur=="cop":
        return "Pesos"
    if cur=="crc":
        return "Colón"
    if cur=="hrk":
        return "Kuna"
    if cur=="cup":
        return "Pesos"
    if cur=="czk":
        return "Koruny"
    if cur=="dkk":
        return "Kroner"
    if cur=="dop":
        return "Pesos"
    if cur=="xcd":
        return "Dollars"
    if cur=="egp":
        return "Pounds"
    if cur=="svc":
        return "Colones"
    if cur=="gbp":
        return "Pounds"
    if cur=="eek":
        return "Krooni"
    if cur=="fkp":
        return "Pounds"
    if cur=="fjd":
        return "Dollars"
    if cur=="ghc":
        return "Cedis"
    if cur=="gip":
        return "Pounds"
    if cur=="gtq":
        return "Quetzales"
    if cur=="ggp":
        return "Pounds"
    if cur=="gyd":
        return "Dollars"
    if cur=="hnl":
        return "Lempiras"
    if cur=="hkd":
        return "Dollars"
    if cur=="huf":
        return "Forint"
    if cur=="isk":
        return "Kronur"
    if cur=="inr":
        return "Rupees"
    if cur=="idr":
        return "Rupiah"
    if cur=="irr":
        return "Rials"
    if cur=="imp":
        return "Pounds"
    if cur=="ils":
        return "New Shekels"
    if cur=="jmd":
        return "Dollars"
    if cur=="jpy":
        return "Yen"
    if cur=="jep":
        return "Pounds"
    if cur=="kzt":
        return "Tenge"
    if cur=="kpw":
        return "Won"
    if cur=="krw":
        return "Won"
    if cur=="kgs":
        return "Soms"
    if cur=="lak":
        return "Kips"
    if cur=="lvl":
        return "Lati"
    if cur=="lbp":
        return "Pounds"
    if cur=="lrd":
        return "Dollars"
    if cur=="chf":
        return "Switzerland Francs"
    if cur=="ltl":
        return "Litai"
    if cur=="mkd":
        return "Denars"
    if cur=="myr":
        return "Ringgits"
    if cur=="mur":
        return "Rupees"
    if cur=="mxn":
        return "Pesos"
    if cur=="mnt":
        return "Tugriks"
    if cur=="mzn":
        return "Meticais"
    if cur=="nad":
        return "Dollars"
    if cur=="npr":
        return "Rupees"
    if cur=="ang":
        return "Guilders (also called Florins)"
    if cur=="nzd":
        return "Dollars"
    if cur=="nio":
        return "Cordobas"
    if cur=="ngn":
        return "Nairas"
    if cur=="kpw":
        return "Won"
    if cur=="nok":
        return "Krone"
    if cur=="omr":
        return "Rials"
    if cur=="pkr":
        return "Rupees"
    if cur=="pab":
        return "Balboa"
    if cur=="pyg":
        return "Guarani"
    if cur=="pen":
        return "Nuevos Soles"
    if cur=="php":
        return "Pesos"
    if cur=="pln":
        return "Zlotych"
    if cur=="qar":
        return "Rials"
    if cur=="ron":
        return "New Lei"
    if cur=="rub":
        return "Rubles"
    if cur=="shp":
        return "Pounds"
    if cur=="sar":
        return "Riyals"
    if cur=="rsd":
        return "Dinars"
    if cur=="scr":
        return "Rupees"
    if cur=="sgd":
        return "Dollars"
    if cur=="sbd":
        return "Dollars"
    if cur=="sos":
        return "Shillings"
    if cur=="zar":
        return "Rand"
    if cur=="krw":
        return "Won"
    if cur=="lkr":
        return "Rupees"
    if cur=="sek":
        return "Kronor"
    if cur=="chf":
        return "Francs"
    if cur=="srd":
        return "Dollars"
    if cur=="syp":
        return "Pounds"
    if cur=="twd":
        return "New Dollars"
    if cur=="thb":
        return "Baht"
    if cur=="ttd":
        return "Dollars"
    if cur=="try":
        return "Lira"
    if cur=="trl":
        return "Liras"
    if cur=="tvd":
        return "Dollars"
    if cur=="uah":
        return "Hryvnia"
    if cur=="gbp":
        return "Pounds"
    if cur=="usd":
        return "Dollars"
    if cur=="uyu":
        return "Pesos"
    if cur=="uzs":
        return "Sums"
    if cur=="eur":
        return "Euro"
    if cur=="vef":
        return "Bolivares Fuertes"
    if cur=="vnd":
        return "Dong"
    if cur=="yer":
        return "Rials"
    if cur=="zwd":
        return "Zimbabwe Dollars"

#-------------------------------------------------------------
# Generic functions
#-------------------------------------------------------------

_translate_funcs = {'id' : amount_to_text}
    
#TODO: we should use the country AND language (ex: septante VS soixante dix)
#TODO: we should use en by default, but the translation func is yet to be implemented
def amount_to_text(nbr, lang='id', currency='idr'):
    """
    Converts an integer to its textual representation, using the language set in the context if any.
    Example:
        1654: thousands six cent cinquante-quatre.
    """
#    import netsvc
#    if nbr > 10000000:
#        netsvc.Logger().notifyChannel('translate', netsvc.LOG_WARNING, _("Number too large '%d', can not translate it"))
#        return str(nbr)
    
    if not _translate_funcs.has_key(lang):
        #netsvc.Logger().notifyChannel('translate', netsvc.LOG_WARNING, _("tidak ditemukan fungsi terjemahan mata uang: '%s'" % (lang,)))
        #TODO: (default should be en) same as above
        lang = 'id'
    return _translate_funcs[lang](abs(nbr), currency)

if __name__=='__main__':
    from sys import argv
    
    lang = 'id'
    if len(argv) < 2:
        for i in range(1,200):
            print i, ">>", int_to_text(i, lang)
        for i in range(200,999999,139):
            print i, ">>", int_to_text(i, lang)
    else:
        print int_to_text(int(argv[1]), lang)

