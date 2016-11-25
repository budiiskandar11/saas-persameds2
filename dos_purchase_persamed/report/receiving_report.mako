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
				font-size:11px;
				text-align: justify;
    			text-justify: inter-word;
				line-height:15px;
				page-break-inside:auto;
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
			.border_right
			{
				border-right: 1px solid black;
			}
			.border_top_bottom
			{
				border-top: 1px solid lightGrey;
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
			.font16px
			{
				font-size: 16px;
			}
			.font10px
			{
				font-size: 10px;
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
         	
         	table.tr {
                page-break-inside:avoid; page-break-after:auto;
                page-break-before: always;
  				}
			
		</style>
	</head>
	%for o in objects:
	 <body style="border:0; margin: 0;" onload="subst()"> 
		<table cellpadding="3" width="100%" class="one font12px ">
            <tr>
            	<td></td>
            	<td colspan="9" class="hmid font16px">RECEIVING REPORT</td>
            	<td>Report : PMR150A </td>
            </tr>
            <tr>
            	<td class="border_bottom"></td>
            	<td colspan="9" class=" border_bottom hmid font16px"></td>
            	<td class="border_bottom">Version : 1</td>
            </tr>
            <tr>
            	<td>Nomor</td>
            	<td>: ${o.name or '/'}
            </tr
            <tr>
            	<td>Supplier
            	</td>
            	<td>: ${o.partner_id.name}
            	</td>
            	<td>
            	</td>
            	<td>Purchasing Officer : ${o.move_lines[0].purchase_id.validator.name or ''}
            	</td>
            	<td>
            	</td>
            	<td>Delivery No : ${o.supplier_dn or ''}
            	</td>
            </tr>
            <tr>
            	<td>PO Number
            	</td>
            	<td>: ${o.origin or '/'}
            	</td>
            	<td>
            	</td>
            	<td>Delivery Date : ${o.date_done or 'not received'}
            	</td>
            	<td>
            	</td>
            	<td>Supplier Docket
            	</td>
            </tr>
        	<tr>
        		<td><br/></td>
        	</tr>
        </table>
        <table  class="font12px one" style=" width: 100%; padding:30px 5px 5px 5px;">
				<tr class="border_bottom title-table">
					<th class="hmid" style="width: 2%; padding:5px;"> ItemNo</th>
					<th class="hleft" style="width: 20%">Name-
														Description/ <br/>
														Part Number</th>
					<th class="hleft" style="width: 10%">Stock Code<br/>
														PR Location</th>
					<th class="hleft" style="width: 7%;">UoP/UoI<br/>
														Conv.Fact</th>
					<th class="hleft" style="width: 7%">T.Order<br/>
													   To Come</th>
					<th class="hright" style="width: 10%">Qty Receive</th>
					<th class="hright" style="width: 10%">Qty Remaining</th>
					<th class="hleft" style="width: 5%">New Location</th>
					<th class="hleft" style="width: 10%">Dues Out<br/>
														Reserv./SOH</th>
					<th class="hleft" style="width: 10%">Requestor<br/>
														Qty Req.</th>
					
					<th class="hleft" style="width: 5%">Distrik<br/>
														NonMIMS</th>
					
				</tr>
				<% set i=0%>
				%for x in o.move_lines :
					<% set i=i+1%>
				<tr class="font12px">
					<td class="hmid" style="width: 2%; padding:5px;">${i}</td>
					<td class="hleft" style="width: 20%">${x.product_id.name}<br/>
														${x.part_no_product}</td>
											
					<td class="hleft" style="width: 10%">${x.product_id.stock_code.name or '/'}<br/>
														${o.distrik_id.name}</td>
					
					<td class="hleft" style="width: 7%;">${x.product_uom.name}<br/>
														</td>
					
					<td class="hleft" style="width: 7%">${x.purchase_line_id.product_qty}<br/>
													   ${x.product_uom_qty}</td>
					<td class="hright" style="width: 10%">${x.product_uom_qty}</td>
					<td class="hright" style="width: 10%">${x.purchase_line_id.product_qty-x.product_uom_qty}</td>
					<td class="hleft" style="width: 5%"></td>
					<td class="hleft" style="width: 10%"><br/>
														</td>
					<td class="hleft" style="width: 10%">${x.purchase_id.request_by.name}<br/>
														${x.purchase_line_id.product_qty}</td>
					
					<td class="hleft" style="width: 5%">${o.distrik_id.name}<br/>
														NA</td>
					
				</tr>
				%endfor
				<tr>
					<td colspan="11" class="border_top"><br/><br/></td>
				</tr>
			</table>	
      		<table cellpadding="8" border="1px solid" class="font12px one" >
      			<tr>
      				<td class="hmid"></td>
      				<td>Init</td>
      				<td>Storeman</td>
      				<td>Date</td>
      				<td>Discrepancy Report Notation</td>
      				<td></td>
      				<td>Init</td>
      				<td>Warehouse GL</td>
      				<td>Date</td>
      				<td>Discrepancy Report Notation</td>
      			</tr>
      			<tr>
      				<td class="hmid">Check By</td>
      				<td></td>
      				<td></td>
      				<td></td>
      				<td></td>
      				<td class="hmid">Q/C By</td>
      				<td></td>
      				<td></td>
      				<td></td>
      				<td></td>
      			</tr>
      			<tr>
      				<td class="hmid">Bin By</td>
      				<td></td>
      				<td></td>
      				<td></td>
      				<td></td>
      				<td class="hmid">Receive By</td>
      				<td></td>
      				<td></td>
      				<td></td>
      				<td></td>
      			</tr>
      			<tr>
      				<td class="hmid">Deliver To</td>
      				<td></td>
      				<td></td>
      				<td></td>
      				<td></td>
      				<td class="hmid">Sign Off</td>
      				<td></td>
      				<td></td>
      				<td></td>
      				<td></td>
      			</tr>
      		</table>
      
      %endfor 	
       </body>
   </html>
  