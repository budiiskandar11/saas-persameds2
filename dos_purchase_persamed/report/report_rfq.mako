 <!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
	<head>
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
			.perjanjian
			{
				font-size:10px;
				text-align: justify;
    			text-justify: inter-word;
				line-height:12px;
				page-break-inside:avoid; page-break-after:auto;
			}
			th
			{
				font-size: 12px;
				border-bottom: 1px solid black;
				border-left : 1px solid black;
				border-right : 1px solid black;
				border-top : 1px solid black;
				background-color: lightGrey
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
			.font10px
			{
				font-size: 10px;
			}
			.font8px
			{
				font-size: 8px;
			}
			.font14px
			{
				font-size: 14px;
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
        </style>
    </head>
     %for o in objects  : 
    <body style="border:0; margin: 0;" onload="subst()">
      
       
	      <table cellpadding="3" class="header one" style="width:100%">
	           <tr>
	                <td class="font22px hmid" style="width:60%;" rowspan="2">REQUEST FOR QUOTATION</td>
	                <td style="width:10%; background-color: #d3d3d3;" class="font12px hmid border_top_bottom border_left_right">Number</td>
	                <td style="width:10%;"></td>
	                <td style="width:10%; background-color: #d3d3d3;" class="font12px hmid border_top_bottom border_left_right">Date</td>
	            </tr> 
	            <tr>
	                <td class="hmid font12px border_left_right border_top_bottom">${o.name or '/'}</td>
	                <td style="width:10%;"></td>
	                <td class="hmid font12px border_left_right border_top_bottom">${time.strftime('%d %b %Y', time.strptime(o.date_order,'%Y-%m-%d %H:%M:%S'))}</td>
	            </tr> 
	            <tr>
	                <td class="hmid font12px"></td>
	                <td style="width:10%;"></td>
	                <td class="hmid font12px"></br>
	                							
	                
	                </td> 
	           </tr> 
	              
          </table>
          <table cellpadding="3" class="header one" style="padding-top:30px ; width:100%">
	           <tr>
	                
	                <td style="width:45%; background-color: #d3d3d3;" class="font12px hmid border_top_bottom border_left_right">Supplier</td>
	                <td style="width:10%;"></td>
	                <td style="width:45%; background-color: #d3d3d3;" class="font12px hmid border_top_bottom border_left_right">Ship To</td>
	            </tr> 
	            <tr>
	                <td class="hleft font12px border_left_right"><b>${o.partner_id.name}</b> </br> 
	                											${o.partner_id.street or ''} ${o.partner_id.street2 or ''} 
	                											${o.partner_id.city or ''} ${o.partner_id.state_id.name or ''} 
	                											${o.partner_id.country_id.name or ''} ${o.partner_id.zip or ''} 
	                											
	                											</td>
	                <td style="width:10%;"></td>
	                <td class="hleft font12px border_left_right"><b>${o.picking_type_id.warehouse_id.partner_id.name or ''} </b></br>
	                						   ${o.picking_type_id.warehouse_id.partner_id.street or ''}, ${o.picking_type_id.warehouse_id.partner_id.street2 or ''} </br>
	                						   ${o.picking_type_id.warehouse_id.partner_id.city or ''} ${o.picking_type_id.warehouse_id.partner_id.state_id.name or ''}</br>
	                						   ${o.picking_type_id.warehouse_id.partner_id.country_id.name or ''} ${o.picking_type_id.warehouse_id.partner_id.zip or ''}	
	                </td>
	                
	            </tr> 
	             <tr>
	                
	                <td class="font12px border_left_right"></td>
	                <td style="width:10%;"></td>
	                <td style="width:45%; background-color: #d3d3d3;" class="font12px hmid border_left_right border_top_bottom">Shipping Via</td>
	            </tr> 
	            <tr>
	                <td class="font12px border_left_right"></td>
	                <td style="width:10%;"></td>
	                <td class="hleft font12px border_left_right">${o.freight_metode or ''}</td> 
	             </tr>
	              <tr>
	                
	                <td style="width:45%; background-color: #d3d3d3;" class="font12px hmid border_top_bottom border_left_right">Currency</td>
	                <td style="width:10%;"></td>
	                <td style="width:45%; background-color: #d3d3d3;" class="font12px hmid border_left_right border_top_bottom">Incoterm</td>
	            </tr> 
	            <tr>
	                <td class="hleft font12px  border_left_right border_bottom">${o.currency_id.name}</td> 
	                <td style="width:10%;"></td>
	                <td class="hleft font12px border_left_right border_bottom">${o.incoterm_id.code or ''}-${o.incoterm_id.name or ''}</td> 
	             </tr>
	            
	           
	           <tr>
	                <td class="hmid font12px"></td>
	                <td style="width:10%;"></td>
	                <td class="hmid font12px"></br>
	                							
	                
	                </td> 
	           </tr> 
          </table>
          <table class=" font12px one" cellpadding="3" style="width:100%">
          				<tr>
          					<td colspan="5" class="font12px"> <b>Details</b> </td>
          				</tr>
          				<tr>
          					<th width="5%">No</th>
          					<th width="30%">Product</th>
          					<th width="30%">Spesification</th>
          					<th width="10%">Expected Date</th>
          					<th width="10%">Qty</th>
          					
          				</tr>
          				<%set i=0 %>
          				%for m in o.order_line :
          				<%set i=i+1 %>
          				<tr>
          					<td class="border_left_right">${i}</td>
          					<td class="border_left_right">${m.product_id.default_code or ''}-${m.product_id.name or ''}</td>
          					<td class="border_left_right hmid">${m.name or ''}</td>
          					<td class="border_left_right hmid">${m.date_planned}</td>
          					<td class="border_left_right hmid">${m.product_qty or '0'} ${m.product_uom.name or ''}</td>
          					
          				</tr>
          				%endfor
          				<tr>
          					<td class="border_left_right border_bottom hmid"></td>
          					<td class="border_left_right border_bottom hmid"></td>
          					<td class="border_left_right border_bottom hmid"></td>
          					<td class="border_left_right border_bottom hmid"></td>
          					<td class="border_left_right border_bottom hmid"></td>
          					
          				</tr>
          			</table>
          			
          <table class=" font12px" cellpadding="3" style="width:100%; padding-top:40px">
          	<tr>
          		<td>Please submit your quotation and send it via email to scm@persameds.com </td>
          	</tr>
          	<tr>
          		<td>Authorized By</td>
          	</tr>
          	<tr>
          		<td></br></br></br></td>
          	</tr>
          	<tr>
          		<td>${o.create_uid.name}</td>
          	</tr>
          	
          </table>
        
          
          
          
      %endfor
       
       </body>
   </html>