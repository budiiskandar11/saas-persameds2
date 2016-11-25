from openerp.report import report_sxw
from datetime import date
from datetime import datetime
import time
from openerp.tools.translate import _

class training_proposal(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context):
        super(training_proposal, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                                  'get_object'      : self._get_object,
                                  'get_start'       : self._get_start,
                                  'get_end'         : self._get_end,
                                  'get_current_date': self._get_current_date,
                                  })
        
    def _get_object(self,data):
        obj_data=self.pool.get(data['model']).browse(self.cr,self.uid,[data['id']])
        return obj_data
    
    def _get_start(self, start):
        ttyme = datetime.fromtimestamp(time.mktime(time.strptime(start,"%Y-%m-%d")))
        start = tools.ustr(ttyme.strftime('%e %B %Y'))
        return start
    
    def _get_end(self, end):
        ttyme = datetime.fromtimestamp(time.mktime(time.strptime(end,"%Y-%m-%d")))
        end = tools.ustr(ttyme.strftime('%e %B %Y'))
        return end
    
    def _get_current_date(self):
        current = time.strftime('%Y-%m-%d')
        ttyme = datetime.fromtimestamp(time.mktime(time.strptime(current,"%Y-%m-%d")))
        current = tools.ustr(ttyme.strftime('%e %B %Y'))
        return current
    
report_sxw.report_sxw('report.print.training.proposal', 'hr.training', 'ad_hr_training/report/print_training_proposal.mako', parser=training_proposal)
