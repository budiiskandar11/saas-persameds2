function openerp_account_cfs(instance) {

    var module = instance.website_account;
    var _t     = instance.web._t;
    var QWeb   = instance.web.qweb;


module.cashflowstatementWidget = instance.web.Widget.extend({
        template: 'cashflowstatementWidget',
        events: {
        'click #btnprint':'printit',
        'click #btnexport':'exportit',
        'click #btnsubmit': 'get_data',
        },
        init: function(parent, params){
            this._super(parent,params);
            var self = this;
            self.companies = [];
            self.income_details = [];
            self.expense_details = [];
            },
        
        start: function(){
            window.document.title = 'Statement of Cash Flows - Odoo';   
            this._super();
            var self = this;
            this.title="Statement of Cash Flows";
            $('.js_pick_quit').click(function(){ 
            		return new instance.web.Model("ir.model.data").get_func("search_read")([['name', '=', 'action_account_form']], ['res_id']).pipe(function(res) {
            		window.location = '/web#action=' + res[0]['res_id'];
                	}); 
                	});
            this.$("#datepicker_from").datepicker({
		changeMonth: true,
		changeYear: true,
		dateFormat:"mm/dd/yy"
		});
	    this.$("#datepicker_to").datepicker({
		changeMonth: true,
		changeYear: true,
		dateFormat:"mm/dd/yy"
		});		
	    this.$("#daterange").daterangepicker({
     	 	datepickerOptions : {
         	numberOfMonths : 2,
         	initialText : 'Select Date Range...',
         	rangeSplitter : '-',
         	dateFormat: "yy-mm-dd",
         	'showDropDowns':true
     		}
 	    }); 	    
 	    
 	    // Getter
		var dateFormat = $( "#daterange" ).datepicker( "option", "dateFormat" );
 
	    // Setter
		$( "#daterange" ).datepicker( "option", "dateFormat", "yy-mm-dd" );
				
            var deferred_promises = [];            
            /*deferred_promises.push(new instance.web.Model('account.account')
            .query(['name', 'id'])
            .filter([['parent_id', '=', false]])
            .all()
            .then(function (results) {
                _(results).each(function (item) {
                    self.$('#chart_account_id').append('<option class="js_loc_option" value='+item['id']+'>'+item['name']+'</option>');
                });
            })
            );*/  
            deferred_promises.push(new instance.web.Model('account.account')
            .call("get_user_chart_accounts", ({'data':{}}))
            .then(function(results) {
                _(results).each(function (item) {
                    if(item['select'] == true)
                        self.$('#chart_account_id').append('<option class="js_loc_option" value='+item['id']+' selected="selected">'+item['code'] + ' '+item['name']+'</option>');
                    else
                        self.$('#chart_account_id').append('<option class="js_loc_option" value='+item['id']+'>'+item['code'] + ' '+item['name']+'</option>');
                });
            })
            ); 
	    deferred_promises.push(new instance.web.Model('account.period')
            .query(['name', 'id'])
            //.filter([['parent_id', '=', false]])
            .all()
            .then(function (results) {
                _(results).each(function (item) {
                    self.$('#periodfrom').append('<option class="js_loc_option" value='+item['id']+'>'+item['name']+'</option>');
                    self.$('#periodto').append('<option class="js_loc_option" value='+item['id']+'>'+item['name']+'</option>');
                });
            })
            );            
            deferred_promises.push(new instance.web.Model('account.account')
            .call("get_user_company", ({'data':{}}))
            .then(function(results) {
                    self.$('#companyid').html(results['name']);
            })
            );
            return $.when.apply($, deferred_promises).then(function(){
                
               stopsplash(100);
                });
               
        }, 
        quit: function(){
            return new instance.web.Model("ir.model.data").get_func("search_read")([['name', '=', 'action_account_form']], ['res_id']).pipe(function(res) {
                    window.location = '/web#action=' + res[0]['res_id'];
                });
        }, 
        get_title: function(){
        var self = this; 
        self.$(".oe_loading").hide();        
            return "Statement of Cash Flows";
        },
        get_filter_string:function(){
            var self = this;alert(self.$('#daterange').html());
            var daterange = self.$('#daterange').val();
            date_from = false;
            date_to = false;
            if (daterange.trim()!='')
            {
                date_from = daterange['start'];
                date_to = daterange['end'];
	    }
	    return date_from + ' - ' + date_to
        },
        get_company:function(){
           new instance.web.Model("account.account").get_func("get_user_company")([['name', '!=', '']], ['name']).then(function(res) {
                    return res[0]['name']
                    
                });
        },
        load_companies: function(){
            var self = this;
            var locations = [];
            new instance.web.Model("res.company").get_func("search_read")([['name', '!=', '']], ['name']).then(function(res) {
                    for(var i = 0; i < res.length; i++){
                    self.companies.push({name: res[i]['name'], id: res[i]['id'],});
                    }
                    
                });
        },
        get_companies: function(){
        var self = this;
        self.$('#chart_account_id').val();
            
            self.load_companies();
            return self.companies;
        },
        validate_data: function(){
        var self = this;
        from_date = self.$('#datepicker_from').val();
        to_date = self.$('#datepicker_to').val();
        if(eval(from_date)!=undefined && eval(to_date)!=undefined)
        {
        from = new Date(from_date);
        to = new Date(to_date);
        if(to<from)
        {
          alert('From Date should be Less than/ Equal to To Date');
          return false;
        }
        else
        {
          return true;
        }
        }
        from_period = self.$('#periodfrom').val();
        to_period = self.$('#periodto').val();
        if(eval(from_period)!=undefined && eval(to_period)!=undefined)
        {
        from = eval(from_period);
        to = eval(to_period);
        if(to<from)
        {
          alert('"Period From" should be Less than/ Equal to "Period To"');
          return false;
        }
        else
        {
          return true;
        }
        }
        },
        get_childs:function(parent,childs){
        var ret='<ul>';
        for (i = 0; i < childs.length; i++) {
          ret+='<li id='+childs[i]['id']+'><a><table><tr><td STYLE="width:80%;text-decoration:none;">'+childs[i]['name']+'</td><td style="text-align:right;padding-right: 10px;">'+childs[i]['balance']+'</td></tr></table></a></li></ul>'
        }
        ret+='</ul>';
        },
        
        show_hide_filters: function(){
            var self = this;
            var filter = self.$('#filter_select').val();
            if(filter.trim()=='filter_date')
            {
                self.$('#daterangetd3').removeClass('hidediv');
                self.$('#daterangetd2').removeClass('hidediv');
                self.$('#daterangetd1').removeClass('hidediv');
            }
            else
            {
                self.$('#daterangetd3').addClass('hidediv');
                self.$('#daterangetd2').addClass('hidediv');
                self.$('#daterangetd1').addClass('hidediv');   
                self.$('#daterange').daterangepicker("clearRange");         
            }
            if(filter.trim()=='filter_period')
            {
                self.$('#periodfromtd3').removeClass('hidediv');
                self.$('#periodfromtd2').removeClass('hidediv');
                self.$('#periodfromtd1').removeClass('hidediv');
                self.$('#periodtotd3').removeClass('hidediv');
                self.$('#periodtotd2').removeClass('hidediv');
                self.$('#periodtotd1').removeClass('hidediv');
            }
            else
            {
                self.$('#periodfromtd3').addClass('hidediv');
                self.$('#periodfromtd2').addClass('hidediv');
                self.$('#periodfromtd1').addClass('hidediv');  
                self.$('#periodtotd3').addClass('hidediv');
                self.$('#periodtotd2').addClass('hidediv');
                self.$('#periodtotd1').addClass('hidediv');   
                self.$('#periodfrom').val("-1");
                self.$('#periodto').val("-1");       
            }
        },
        
        printit: function(){
                startsplash();
                var self = this;
                var company = self.$('#companyid').text(); 
                var title = self.$('#titleid').text(); 
                var filter = self.$('#filterid').text(); 
                var filter_str = self.$('#filterid').text(); 
                var maindata = self.$('#maintd').html();
                from_date = self.$('#datepicker_from').val();
		to_date = self.$('#datepicker_to').val();
		var chart_account_id = eval(self.$('#chart_account_id').val());
		self.$('#filter_select').val("filter_date");
		var period_from = eval(self.$('#periodfrom').val());
		var period_to = eval(self.$('#periodto').val());
		var filter = self.$('#filter_select').val();
		var daterange = self.$('#daterange').val();
		var target_move = self.$('#targetmove_select').val();
		//var display_account_id = self.$('#display_account_select').val();
        	//var display_account_name = self.$('#display_account_select option:selected').text();
		var date_from = false;
		var date_to = false;
		var date_str = '';
		if (daterange.trim()!='')
		{
		    date_from = new Date(daterange.substring(10, 20));
		    date_to = new Date(daterange.substring(29, 39));
		    date_str = date_from.toLocaleFormat('%d %B %Y') + ' - ' + date_to.toLocaleFormat('%d %B %Y');
		    from_dt = date_from.toLocaleFormat('%m-%d-%Y');
		    to_dt = date_to.toLocaleFormat('%m-%d-%Y');
		}
                self.model_account = new instance.web.Model("account.account");
        	return self.model_account
                    .call("print_report_pdf_cfs", ({'data':{'form': {'chart_account_id': chart_account_id, 'fiscalyear_id': 1, 'date_from': from_dt, 'period_to': false, 'journal_ids': [], 'used_context': {'chart_account_id': chart_account_id, 'fiscalyear': 1, 'date_from': from_dt, 'date_to': to_dt, 'state': target_move, 'journal_ids': false}, 'date_to': to_dt, 'filter': 'filter_date', 'target_move': target_move, 'filter_string':date_str, 'title':title, 'company':company, 'filter_str':filter_str, 'from_print':true}}}))
                    .then(function(action){
                                stopsplash(1000);
                                return self.do_action(action);
                           });
        },
        
        exportit: function(){
                startsplash();
                var self = this;
                var company = self.$('#companyid').text(); 
                var title = self.$('#titleid').text(); 
                var filter = self.$('#filterid').text(); 
                var filter_str = self.$('#filterid').text(); 
                var maindata = self.$('#maintd').html();
                from_date = self.$('#datepicker_from').val();
		to_date = self.$('#datepicker_to').val();
		var chart_account_id = eval(self.$('#chart_account_id').val());
		self.$('#filter_select').val("filter_date");
		var period_from = eval(self.$('#periodfrom').val());
		var period_to = eval(self.$('#periodto').val());
		var filter = self.$('#filter_select').val();
		var daterange = self.$('#daterange').val();
		var target_move = self.$('#targetmove_select').val();
		//var display_account_id = self.$('#display_account_select').val();
        	//var display_account_name = self.$('#display_account_select option:selected').text();
		var date_from = false;
		var date_to = false;
		var date_str = '';
		if (daterange.trim()!='')
		{
		    date_from = new Date(daterange.substring(10, 20));
		    date_to = new Date(daterange.substring(29, 39));
		    date_str = date_from.toLocaleFormat('%d %B %Y') + ' - ' + date_to.toLocaleFormat('%d %B %Y');
		    from_dt = date_from.toLocaleFormat('%m-%d-%Y');
		    to_dt = date_to.toLocaleFormat('%m-%d-%Y');
		}
                self.model_account = new instance.web.Model("cashflow.statement.xls");
        	return self.model_account
                    .call("xls_export", ({'data':{'form': {'chart_account_id': chart_account_id, 'fiscalyear_id': 1, 'date_from': from_dt, 'period_to': false, 'journal_ids': [], 'used_context': {'chart_account_id': chart_account_id, 'fiscalyear': 1, 'date_from': from_dt, 'date_to': to_dt, 'state': target_move, 'journal_ids': false}, 'date_to': to_dt, 'filter': 'filter_date', 'target_move': target_move, 'filter_string':date_str, 'title':title, 'company':company, 'filter_str':filter_str, 'from_print':true}}}))                    
                    .then(function(action){
                                stopsplash(1000);
                                return self.do_action(action);
                           });
        },
        
        get_data: function(){
        startsplash();
        var self = this;
        self.$('#maintd').empty();
        from_date = self.$('#datepicker_from').val();
        to_date = self.$('#datepicker_to').val();
        var chart_account_id = eval(self.$('#chart_account_id').val());        
        var chart_account_name = self.$('#chart_account_id option:selected').text();
        //var display_account_id = self.$('#display_account_select').val();
        //var display_account_name = self.$('#display_account_select option:selected').text();
        self.$('#filter_select').val("filter_date");
        var period_from = eval(self.$('#periodfrom').val());
        var period_to = eval(self.$('#periodto').val());
        var filter = self.$('#filter_select').val();
        var daterange = self.$('#daterange').val();
        var target_move = self.$('#targetmove_select').val();
        var date_from = false;
        var date_to = false;
        var date_str = '';
        if (daterange.trim()!='')
        {
            date_from = new Date(daterange.substring(10, 20));
            date_to = new Date(daterange.substring(29, 39));
            date_str = date_from.toLocaleFormat('%B %d, %Y') + ' through ' + date_to.toLocaleFormat('%B %d, %Y');
            from_dt = date_from.toLocaleFormat('%m-%d-%Y');
	    to_dt = date_to.toLocaleFormat('%m-%d-%Y');
        }
        
        if(self.$('#filter_select').val()=='-1')
        {
          alert('Please Select the Filter by');
          return;
        }
        else if(self.$('#daterange').val().trim()=='' && filter=='filter_date')
        {
          alert('Please Select the Date Range');
          return;
        }
        else if((self.$('#periodfrom').val()=='-1' || self.$('#periodto').val()=='-1') && filter=='filter_period')
        {
          alert('Please Select the Periods');
          return;
        }
        else if(self.$('#targetmove_select').val()=='-1')
        {
          alert('Please Select the "Target Moves"');
          return;
        }        
        /*else if(eval(from_date)==undefined)
        {
          alert('Please Select the Date From');
          return;          
        }
        else if(eval(to_date)==undefined)
        {
          alert('Please Select the Date To');
          return;          
        }*/
        else {
        valid = self.validate_data();
        if(valid==false)
          return;
        }
        self.$('#filterid').text(date_str);
        
        self.$('#tblheader').removeClass('hidediv');
        self.$('#companyid').removeClass('hidediv'); 
        self.$('#titleid').removeClass('hidediv'); 
        self.$('#filterid').removeClass('hidediv'); 
        self.$('#btnprint').removeClass('hidediv'); 
        self.$('#btnexport').removeClass('hidediv'); 
        self.$('#tblTitles').removeClass('hidediv'); 
        
        
        self.lines = "";
        self.model_account = new instance.web.Model("account.account");
        self.model_account
                    .call("get_lines_cashflow_statement", ({'data':{'form': {'chart_account_id': chart_account_id, 'fiscalyear_id': 1, 'date_from': from_dt, 'period_to': false, 'journal_ids': [], 'used_context': {'chart_account_id': chart_account_id, 'fiscalyear': 1, 'date_from': from_dt, 'date_to': to_dt, 'state': target_move, 'journal_ids': false}, 'date_to': to_dt, 'filter': 'filter_date', 'target_move': target_move, 'from_load':true}}}))
                    .then(function(results) {
                        _(results).each(function (item) {
                        {//if(item['type']!='report' && item['parent_name'] !=chart_account_name)
                        {
                        var content = '<ul><li id='+item['id']+'><a><table id='+item['id']+'_'+item['has_childs']+' class="datatbl" ><tr><td valign=top STYLE="text-decoration:none;">'+(item['bold']==true ? '<b style="color:RoyalBlue">'+(item['name']!='Cash Flow' ? item['name'] : '&nbsp;')+'</b></td><td valign=top style="width:150px;text-align:right;padding-right: 10px;border-top: 1px solid black;border-bottom: 1px solid black;">'+(item['has_childs']==false ? '<b style="color:RoyalBlue">'+(item['name']!='Adjustments to reconcile Net Income' && item['name']!='to net cash provided by operations:' ? (item['balance']).toFixed(2):'')+'</b>':'')+'</td></tr><tr><td height=25></td><td></td><td></td><td></td></tr></table></a></li></ul>':(item['has_childs']==true ? '<b style="color:RoyalBlue">'+(item['name']!='Cash Flow' ? item['name'] : '&nbsp;')+'</b></td><td></td><td></td><td></td>':(item['name']!='Cash Flow' ? item['name'] : '&nbsp;')+'</td><td style="width:150px;text-align:right;padding-right: 10px;">'+(item['name']!='Adjustments to reconcile Net Income' && item['name']!='to net cash provided by operations:' ? (item['balance']).toFixed(2):'')+'</td>')+'</tr></table></a></li></ul>')
                        if(self.$('#'+item['parent_id']+'').html()!=undefined){
                          self.$('#'+item['parent_id']+'').append(content);
                        }
                        else
                        {
                          self.$('#maintd').append(content);
                          //if(item['child_ids']!=undefined && item['child_ids'].length>0){
                          //self.$('#'+item['id']+'').append(self.get_childs(item['id'],item['child_ids']));
                          //}
                        }
                        }                        
                        }
                    });
                    $( '.tree li' ).each( function() {
						if( $( this ).children( 'ul' ).length > 0 ) {
								$( this ).addClass( 'parent' );     
						}
				});
				
				$( '.tree li.parent > a' ).click( function( ) {
						$( this ).parent().toggleClass( 'active' );
						$( this ).parent().children( 'ul' ).slideToggle( 'fast' );
				});
				
				$( '.tree li' ).each( function() {
						$( this ).toggleClass( 'active' );
						$( this ).children( 'ul' ).slideToggle( 'fast' );
				});
				$( '.datatbl tr td' ).each( function() {
						$( this ).click( function(){
						splt = $( this ).parent().parent().parent().attr('id').split('_');
						acc_id = splt[0];
						flg_childs = splt[1];
						if(flg_childs == 'false' && (acc_id%1==0)){
						return new instance.web.Model("ir.model.data").get_func("search_read")([['name', '=', 'action_move_line_select']], ['res_id']).pipe(function(res) {
            					window.open('/web#page=0&limit=80&view_type=list&model=account.move.line&action='+res[0]['res_id']+'&active_id='+acc_id,'_blank');
                				}); 
                				}
						});
					});
                 stopsplash(500);
                 });
		 
        },
            
    });
    openerp.web.client_actions.add('website_account.cashflow_statement', 'instance.website_account.cashflowstatementWidget');
}
