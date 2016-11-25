## -*- coding: utf-8 -*-
<!DOCTYPE html SYSTEM
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <style type="text/css">
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
				font-size: 10px;
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
			.font10px
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
            
            .overflow_ellipsis {
                text-overflow: ellipsis;
                overflow: hidden;
                white-space: nowrap;
            }

            .open_invoice_previous_line {
                font-style: italic;
            }

            .percent_line {
                font-style: italic;
            }

            .amount {
                text-align:right;
            }

            .classif_title {
                text-align:right;
            }

            
            .total{
               font-weight:bold;
            }
            ${css}
        </style>
    </head>

   
    <body>
   
    	
       <table cellpadding="3" border="1" class="one font10px" style="width:100%; page-break-before: always; page-break-after: always;">
       		<tr>
       			<td colspan="10">Laporan Stock PT Persada Medica Solusindo</td>
       		</tr>
       		<tr>
       			<td colspan="3">Type</td>
       			<td colspan="7">:</td>
       		</tr>
       		<tr>
       			<td colspan="3">Date</td>
       			<td colspan="7">:</td>
       		</tr>
       		
       		<tr>
      			<th rowspan="2" width="2%">No.</th>
      			<th width="5% class="hleft">Code</th>
      			<th width="5%"></th>
      			<th width="7%"></th>
      			<th width="5%"></th>
      			<th width="20%"></th>
      			<th width="7%" colspan="3">Qty</th>
      			
      		</tr>
      		<tr>
      			
      			<th width="5%"></th>
      			<th width="5%" class="hleft">Picking Type</th>
      			<th width="7%" class="hleft">Tanggal</th>
      			<th width="5%" class="hleft">Ref</th>
      			<th width="20%" class="hleft">Deliver From/To</th>
      			<th width="7%" class="hmid">Qty In</th>
      			<th width="7%" class="hmid">Qty Out</th>
      			<th width="7%" class="hmid">Balance</th>
      			
      			
      		</tr>
      		<% set i=0 %>
      		 
	      		 %for line in get_stock_data(data)|groupby('name'):
	      		 
					<% set i = i+1%>
					 <tr style="page-break-inside:avoid; page-break-after:auto;">
					 	<td class="border_bottom" width="2%">${i}</td>
		       			<td class="border_bottom" colspan="3">${line.grouper}</td>
		       			<td class="border_bottom"></td>
		       			<td class="border_bottom"></td>
		       			<td class="border_bottom"></td>
		       			<td class="border_bottom"></td>
		       			<td class="border_bottom">${line.list|sum(attribute='product_uom_qty')}</td>
		       			
		       		</tr>  
	      		 		%for move in line.list|groupby('picking_type_id.name') :
	      		 		 <tr style="page-break-inside:avoid; page-break-after:auto;">
						 	<td></td>
						 	<td></td>
			       			<td class="border_bottom" colspan="2" width="5%">${move.grouper}</td>
			       			<td class="border_bottom"></td>
			       			<td class="border_bottom"></td>
			       			<td class="border_bottom" ></td>
			       			%if move.grouper == 'Delivery Orders' :
			       			<td class="border_bottom hright" width="7%">XXX${move.list|sum(attribute='product_uom_qty')}</td>
			       			%endif
			       			<td class="border_bottom"></td>
		       			 </tr>
		       				%for stock in move.list|sort():	
				       		<tr style="page-break-inside:avoid; page-break-after:auto;">
				       			<td></td>
				       			<td></td>
				       			<td></td>
				       			
				       			<td>${time.strftime('%d %B %Y', time.strptime(stock.date,'%Y-%m-%d %H:%M:%S'))}</td>
				       			<td>${stock.picking_id.name}</td>
				       			<td>${stock.picking_id.partner_id.name}</td>
				       			%if stock.picking_type_id.name == 'Delivery Orders' :
				       			<td class="hright">${stock.product_uom_qty}</td>
				       			<td class="border_bottom"></td>
				       			%elif stock.picking_type_id.name == 'Receipts' :
				       			<td class="border_bottom"></td>
				       			<td class="hright">${stock.product_uom_qty}</td>
				       			%endif
				       			<td class="border_bottom"></td>
				       		</tr>
			       			%endfor
		       			%endfor
	      		%endfor
	      	
      
       </table>
       
      
 	
       
        
       
    </body>
</html>