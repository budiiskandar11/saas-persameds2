<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
	<head>
	 <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>
	 <script>
            function subst() {
            var vars={};
            var x=document.location.search.substring(1).split('&');
            for(var i in x) {var z=x[i].split('=',2);vars[z[0]] = unescape(z[1]);}
            var x=['frompage','topage','page','webpage','section','subsection','subsubsection'];
            for(var i in x) {
            var y = document.getElementsByClassName(x[i]);
            for(var j=0; j<y.length; ++j) y[j].textContent = vars[x[i]];
                }
            }
        </script>
		<style>
			.vtop
			{
				vertical-align: top;
			}

			.vbottom
			{
				vertical-align: bottom;
			}
		
			.hright
			{
				text-align: right;
				padding-right: 3px;
			}
			.hleft
			{
				text-align: left;
			}
			.hmid
			{
				text-align: center;
			}
			.content
			{
				font-size: 12px;
			}
			.border_grey
			{
				border: 1px solid lightGrey;
			}
			.border_black
			{
				border: 1px solid black;
			}
			.space
			{
				min-height: 25px;
			}
			.note
			{
				width: 500px;
				padding: 5px;
				float:right;
				min-width: 100px;
				border:1px solid black;
			}
			.padding
			{
				padding: 5px;
			}
			.paddingtop
			{
				padding-top: 10px;
			}
			.paddingright
			{
				padding-right: 10px;
			}
			th
			{
				font-size: 12px;
				border-bottom: 1px solid black;
			}
			.border_bottom_grey
			{
				border-bottom: 1px solid lightGrey;
			}
			.background_color
			{
				background-color: lightGrey
			}
			.border_top
			{
				border-top: 1px solid black;
			}
			.border_bottom
			{
				border-bottom: 1px solid black;
			}
			.border_bottom_thin
			{
				
				border-bottom: 0.5px solid black
				
			}
			.border_right
			{
				border-right: 1px solid black;
			}
			.border_top_bottom
			{
				border-top: 1px solid black;
				border-bottom: 1px solid black;
			}
			.border_left_right
			{
				border-right: 1px solid black;
				border-left: 1px solid black;
			}
			.fright
			{
				float: right; 
			}
			.fleft
			{
				float: left; 
			}
			.font12px
			{
				font-size: 12px;
			}
			.font11px
			{
				font-size: 11px;
			}
			.font14px
			{
				font-size: 14px;
			}
			.font16px
			{
				font-size: 16px;
			}
			
			.font22px
			{
				font-size: 22px;
			}
			.font30px
			{
				font-size: 30px;
			}
			.title 
			{
				font-size: 22px;
				text-align: center;
				padding: 5px;
			}
			.title-table 
			{
				font-size: 12px;
				text-align:center;
				padding-top:20px;
			}
			.title-form 
			{
				font-size: 22px;
				text-align:center;
				padding-top:20px;
				padding-bottom:10px;
			}
			
         	table.one 
         	{border-collapse:collapse;}
			
		</style>
	</head>
	%for o in objects:
	
	<!-- ini untuk Delivery Order -->
	
		%if o.picking_type_id.code == 'outgoing'
	 	<body style="border:0; margin: 0;" onload="subst()">
	 	<tr>
        			<td colspan="3"><br/></td>
        		</tr>
        <table cellpadding="3" class="header one font12px" style="width:100%; border:1px solid black;">
        		
	           <tr>
	                <td class="font16px hmid" style="width:60%; lenght:auto; " rowspan="2">${helper.barcode(o.name)|safe}</td>
	                <td style="width:20%;" class="font11px hleft border_top_bottom border_left_right">Date</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">${time.strftime('%d %b %Y', time.strptime(o.date,'%Y-%m-%d %H:%M:%S'))}</td>
	            </tr> 
	              	
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">Origin</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">${o.origin or ""}</td>
	            </tr>
	            <tr> 
	            	<td class="font16px hmid" style="width:60%;" rowspan="2">Delivey Order No ${o.name or '/'}</td>  
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">From</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">${o.picking_type_id.warehouse_id.name or ''}</td>
	            </tr>
	            <tr>   
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">Page</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">${o.origin or ""}</td>
	            </tr>
	            
	           <tr>
	                
	                <td style="width:60%; background-color: #d3d3d3;" class="font11px hmid border_top_bottom border_left_right">SHIP TO</td>
	                
	                <td colspan="2" style="width:40%; background-color: #d3d3d3;" class="font11px hmid border_top_bottom border_left_right"></td>
	            </tr> 
	            <tr>
	                <td class="hleft font12px border_left_right" rowspan="6"><b>${o.partner_id.name}</b> </br> 
	                											${o.partner_id.street or ''} ${o.partner_id.street2 or ''} </br> 
	                											${o.partner_id.city or ''} ${o.partner_id.state_id.name or ''} </br> 
	                											${o.partner_id.country_id.name or ''} ${o.partner_id.zip or ''} 
	                											
	                											</td>
	                <td class="hleft font11px border_left_right" style="width:10%;">Packs</td>
	                <td class="hleft font11px border_left_right"> Pack</td>  
	            </tr>
	            <tr>   
	                <td style="width:10%;" class="hleft font11px border_left_right border_top_bottom">Products</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom"> Unit</td>
	            </tr>
	            <tr>   
	                <td style="width:10%;" class="hleft font11px border_left_right border_top_bottom">Vehicle No</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom"></td>
	            </tr>
	            <tr>   
	                <td style="width:10%;" class="hleft font11px border_left_right border_top_bottom">Driver Name</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom"></td>
	            </tr>
	            
	            
          </table>
          <tr>
        			<td colspan="3"><br/></td>
        		</tr>
           	<table  class="font11px one" style=" width: 100%; padding:30px 5px 5px 5px;">
            	<tr>
            		<td colspan="7"class="font14px"><b>Shipping Details</b></td>
            	</tr>
				<tr class="border_bottom  border_top title-table">
					<th class="hmid" style="width: 2%; padding:5px;">No</th>
					<th class="hmid" style="width: 10%">Item Code</th>
					<th class="hmid" style="width: 35%;">Description</th>
					<th class="hmid" style="width: 10%">Serial Number</th>
					<th class="hmid" style="width: 10%">Qty</th>
					<th class="hmid" style="width: 5%">Check</th>
					<th class="hmid" style="width: 20%">Notes</th>
					
				</tr>
				<% set i=0 %>
				%if o.state == 'done'
					%for line in o.pack_operation_ids :
					<% set i=i+1%>
					<tr class="border_bottom_thin">
						<td class="hleft" style="width: 2%; padding:5px;">${i}</td>
						<td class="hleft" style="width: 10%">${line.product_id.default_code}</td>
						<td class="hleft" style="width: 35%;">${line.product_id.name}<br/>
						${line.product_desc|safe}</td>
						<td class="hleft" style="width: 10%">${line.lot_id.name or ''}</td>
						<td class="hmid" style="width: 10%">${line.product_qty or '0'} ${line.product_uom_id.name or ''}</td>
						<td class="hleft" style="width: 5%"></td>
						<td class="hleft" style="width: 20%"></td>
						
					</tr>
					%endfor
				%else
					%for line in o.move_lines :
					<% set i=i+1%>
					<tr class="border_bottom_thin">
						<td class="hmid" style="width: 2%; padding:5px;">${i}</td>
						<td class="hmid" style="width: 10%">${line.product_id.default_code}</td>
						<td class="hleft" style="width: 35%;">${line.product_id.name}<br/>
						${line.product_desc|safe}</td>
						<td class="hmid" style="width: 10%"></td>
						<td class="hmid" style="width: 10%">${line.product_qty or '0'} ${line.product_uom.name or ''}</td>
						<td class="hmid" style="width: 5%"></td>
						<td class="hmid" style="width: 20%">Ready To Deliver</td>
						
					</tr>
					%endfor
				%endif
				
				
				
			</table>
       		 <table class="font12px hmid" style=" width: 100%; border:1px; ">
       			<tr>
			  		<br/>
			  		<br/>
			  	</tr>
			  	
       			<tr>
       				<td></td>
       				<td>Issued By
       				</td>
       				<td></td>
       				<td>Received By
       				</td>
       				<td></td>
       				<td>Acquitted By
       				</td>
       				<td></td>
       			</tr>
       			<tr>
       				<td><br/><br/><br/>
       				</td>
       				<td>
       				</td>
       				<td>
       				</td>
       			</tr>
       			
       		</table>
       	</body>
       	
       <!-- ini untuk Intenal Move -->
       
       %elif o.picking_type_id.code == 'internal'
       	<body style="border:0; margin: 0;" onload="subst()">
	 	<tr>
        	<td colspan="3"><br/></td>
       	</tr>
        <table cellpadding="3" class="header one font12px" style="width:100%; border:1px solid black;">
        		
	           <tr>
	                <td class="font22px hmid" style="width:60%;" rowspan="3">Internal Shipping No ${o.name or '/'}</td>
	                <td style="width:20%;" class="font11px hleft border_top_bottom border_left_right">Date</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">${time.strftime('%d %b %Y', time.strptime(o.date,'%Y-%m-%d %H:%M:%S'))}</td>
	            </tr> 
	              
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">Origin</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">${o.origin or ""}</td>
	            </tr>
	           
	            <tr>   
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">Page</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">${o.origin or ""}</td>
	            </tr>
	            
	           <tr>
	                
	                <td style="width:60%; background-color: #d3d3d3;" class="font11px hmid border_top_bottom border_left_right">SHIP To</td>
	                
	                <td colspan="2" style="width:40%; background-color: #d3d3d3;" class="font11px hmid border_top_bottom border_left_right"></td>
	            </tr> 
	            <tr>
	                <td class="hleft font12px border_left_right" rowspan="4">From : ${o.picking_type_id.default_location_src_id.name} <br/>
	                											 To	  : ${o.picking_type_id.default_location_dest_id.name}
	                </td>
	                <td class="hleft font11px border_left_right" style="width:10%;">Packs</td>
	                <td class="hleft font11px border_left_right"> Pack</td>  
	            </tr>
	            <tr>   
	                <td style="width:10%;" class="hleft font11px border_left_right border_top_bottom">Products</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom"> Unit</td>
	            </tr>
	            <tr>   
	                <td style="width:10%;" class="hleft font11px border_left_right border_top_bottom">Vehicle No</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom"></td>
	            </tr>
	            <tr>   
	                <td style="width:10%;" class="hleft font11px border_left_right border_top_bottom">Driver Name</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom"></td>
	            </tr>
	            
	            
          </table>
          <tr>
        			<td colspan="3"><br/></td>
        		</tr>
           	<table  class="font11px one" style=" width: 100%; padding:30px 5px 5px 5px;">
            	<tr>
            		<td colspan="7"class="font14px"><b>Shipping Details</b></td>
            	</tr>
				<tr class="border_bottom  border_top title-table">
					<th class="hmid" style="width: 2%; padding:5px;">No</th>
					<th class="hmid" style="width: 10%">Item Code</th>
					<th class="hmid" style="width: 35%;">Description</th>
					<th class="hmid" style="width: 10%">Serial Number</th>
					<th class="hmid" style="width: 10%">Qty</th>
					<th class="hmid" style="width: 5%">Check</th>
					<th class="hmid" style="width: 20%">Notes</th>
					
				</tr>
				<% set i=0 %>
				%if o.state == 'done'
					%for line in o.pack_operation_ids :
					<% set i=i+1%>
					<tr class="border_bottom_thin">
						<td class="hleft" style="width: 2%; padding:5px;">${i}</td>
						<td class="hleft" style="width: 10%">${line.product_id.default_code}</td>
						<td class="hleft" style="width: 35%;">${line.product_id.name}<br/><span/>
															  ${line.product_desc|safe or ''}
															  
						</td>
						<td class="hleft" style="width: 10%">${line.lot_id.name or ''}</td>
						<td class="hmid" style="width: 10%">${line.product_qty or '0'} ${line.product_uom_id.name or ''}</td>
						<td class="hleft" style="width: 5%"></td>
						<td class="hleft" style="width: 20%"></td>
						
					</tr>
					%endfor
				%else
					%for line in o.move_lines :
					<% set i=i+1%>
					<tr class="border_bottom_thin">
						<td class="hmid" style="width: 2%; padding:5px;">${i}</td>
						<td class="hmid" style="width: 10%">${line.product_id.default_code}</td>
						<td class="hleft" style="width: 35%;">${line.product_id.name}<br/>
						${line.product_desc|safe}</td>
						<td class="hmid" style="width: 10%"></td>
						<td class="hmid" style="width: 10%">${line.product_qty or '0'} ${line.product_uom.name or ''}</td>
						<td class="hmid" style="width: 5%"></td>
						<td class="hmid" style="width: 20%">Ready To Deliver</td>
						
					</tr>
					%endfor
				%endif
				
				
			</table>
       		 <table class="font12px hmid" style=" width: 100%; border:1px; ">
       			<tr>
			  		<br/>
			  		<br/>
			  	</tr>
			  	
       			<tr>
       				<td></td>
       				<td>Issued By
       				</td>
       				<td></td>
       				<td>Received By
       				</td>
       				<td></td>
       				<td>Acquitted By
       				</td>
       				<td></td>
       			</tr>
       			<tr>
       				<td><br/><br/><br/>
       				</td>
       				<td>
       				</td>
       				<td>
       				</td>
       			</tr>
       			<tr>
       				<td></td>
       				<td class="hleft border_top">Name
       				</td>
       				<td></td>
       				<td class="hleft border_top">Name
       				</td>
       				<td></td>
       				<td class="hleft border_top">Name
       				</td>
       				<td></td>
       			</tr>
       			<tr>
       				<td></td>
       				<td class="hleft">Date
       				</td>
       				<td></td>
       				<td class="hleft">Date
       				</td>
       				<td></td>
       				<td class="hleft">Date
       				</td>
       				<td></td>
       			</tr>
       		</table>
       	</body>
       	
       	<!-- ini untuk incoming -->
       	%else 
       	<body style="border:0; margin: 0;" onload="subst()">
	 	<tr>
        	<td colspan="3"><br/></td>
       	</tr>
        <table cellpadding="3" class="header one font12px" style="width:100%; border:1px solid black;">
        		
	           <tr>
	                <td class="font22px hmid" style="width:60%;" rowspan="4">Incoming Shipment No ${o.name or '/'}</td>
	                <td style="width:20%;" class="font11px hleft border_top_bottom border_left_right">Date</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">${time.strftime('%d %b %Y', time.strptime(o.date,'%Y-%m-%d %H:%M:%S'))}</td>
	            </tr> 
	              
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">Origin</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">${o.origin or ""}</td>
	            </tr>
	            <tr>   
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">To</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">${o.picking_type_id.warehouse_id.name or ''}</td>
	            </tr>
	            <tr>   
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">Page</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom">${o.origin or ""}</td>
	            </tr>
	            
	           <tr>
	                
	                <td style="width:60%; background-color: #d3d3d3;" class="font11px hmid border_top_bottom border_left_right">SHIP FROM</td>
	                
	                <td colspan="2" style="width:40%; background-color: #d3d3d3;" class="font11px hmid border_top_bottom border_left_right"></td>
	            </tr> 
	            <tr>
	                <td class="hleft font12px border_left_right" rowspan="6"><b>${o.partner_id.name}</b> </br> 
	                											${o.partner_id.street or ''} ${o.partner_id.street2 or ''} </br> 
	                											${o.partner_id.city or ''} ${o.partner_id.state_id.name or ''} </br> 
	                											${o.partner_id.country_id.name or ''} ${o.partner_id.zip or ''} 
	                											
	                											</td>
	                <td class="hleft font11px border_left_right" style="width:10%;">Packs</td>
	                <td class="hleft font11px border_left_right"> Pack</td>  
	            </tr>
	            <tr>   
	                <td style="width:10%;" class="hleft font11px border_left_right border_top_bottom">Products</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom"> Unit</td>
	            </tr>
	            <tr>   
	                <td style="width:10%;" class="hleft font11px border_left_right border_top_bottom">Vehicle No</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom"></td>
	            </tr>
	            <tr>   
	                <td style="width:10%;" class="hleft font11px border_left_right border_top_bottom">Driver Name</td>
	                <td style="width:20%;" class="hleft font11px border_left_right border_top_bottom"></td>
	            </tr>
	            
	            
          </table>
          <tr>
        			<td colspan="3"><br/></td>
        		</tr>
           	<table  class="font11px one" style=" width: 100%; padding:30px 5px 5px 5px;">
            	<tr>
            		<td colspan="7"class="font14px"><b>Shipping Details</b></td>
            	</tr>
				<tr class="border_bottom  border_top title-table">
					<th class="hmid" style="width: 2%; padding:5px;">No</th>
					<th class="hmid" style="width: 10%">Item Code</th>
					<th class="hmid" style="width: 35%;">Description</th>
					<th class="hmid" style="width: 10%">Serial Number</th>
					<th class="hmid" style="width: 10%">Qty</th>
					<th class="hmid" style="width: 5%">Check</th>
					<th class="hmid" style="width: 20%">Notes</th>
					
				</tr>
				<% set i=0 %>
				%if o.state == 'done'
					%for line in o.pack_operation_ids :
					<% set i=i+1%>
					<tr class="border_bottom_thin">
						<td class="hleft" style="width: 2%; padding:5px;">${i}</td>
						<td class="hleft" style="width: 10%">${line.product_id.default_code}</td>
						<td class="hleft" style="width: 35%;">${line.product_id.name}<br/>
						${line.product_desc|safe}</td>
						<td class="hleft" style="width: 10%">${line.lot_id.name or ''}</td>
						<td class="hmid" style="width: 10%">${line.product_qty or '0'} ${line.product_uom_id.name or ''}</td>
						<td class="hleft" style="width: 5%"></td>
						<td class="hleft" style="width: 20%"></td>
						
					</tr>
					%endfor
				%else
					%for line in o.move_lines :
					<% set i=i+1%>
					<tr class="border_bottom_thin">
						<td class="hmid" style="width: 2%; padding:5px;">${i}</td>
						<td class="hmid" style="width: 10%">${line.product_id.default_code}</td>
						<td class="hleft" style="width: 35%;">${line.product_id.name}<br/>
						${line.product_desc|safe}</td>
						<td class="hmid" style="width: 10%"></td>
						<td class="hmid" style="width: 10%">${line.product_qty or '0'} ${line.product_uom.name or ''}</td>
						<td class="hmid" style="width: 5%"></td>
						<td class="hmid" style="width: 20%">Ready To Receive</td>
						
					</tr>
					%endfor
				%endif
				
				
			</table>
       		 <table class="font12px hmid" style=" width: 100%; border:1px; ">
       			<tr>
			  		<br/>
			  		<br/>
			  	</tr>
			  	
       			<tr>
       				<td></td>
       				<td>Issued By
       				</td>
       				<td></td>
       				<td>Received By
       				</td>
       				<td></td>
       				<td>Acquitted By
       				</td>
       				<td></td>
       			</tr>
       			<tr>
       				<td><br/><br/><br/>
       				</td>
       				<td>
       				</td>
       				<td>
       				</td>
       			</tr>
       			<tr>
       				<td></td>
       				<td class="hleft border_top">Name
       				</td>
       				<td></td>
       				<td class="hleft border_top">Name
       				</td>
       				<td></td>
       				<td class="hleft border_top">Name
       				</td>
       				<td></td>
       			</tr>
       			<tr>
       				<td></td>
       				<td class="hleft">Date
       				</td>
       				<td></td>
       				<td class="hleft">Date
       				</td>
       				<td></td>
       				<td class="hleft">Date
       				</td>
       				<td></td>
       			</tr>
       		</table>
       	</body>
       	
       	%endif
       %endfor
   </html>	