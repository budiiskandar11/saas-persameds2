<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
	<head>
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
			<table  class="font12px one perjanjian" style=" width: 100%; padding:30px 10px 5px 5px;">
				
				
				<% set i=0%>
				<% set comp_cur = o.currency_id.id%>
					%for x in o.order_line :
					<% set i=i+1%>
					
				<tr class="tr">
					<td class="hmid" style="width: 2%; padding:8px;">${i}</td>
					<td class="hleft" style="width: 35%">${x.product_id.name or ''}/ 
							${x.name}</td>
					<td class="hright" style="width: 12%;">${x.product_qty} 
							${x.product_uom.name}</td>
					<td class="hright" style="width: 3%">${o.currency_id.symbol}</td>
					<td class="hright" style="width: 10%">${formatLang(x.price_unit) or formatLang(0)}</td>
					<td class="hright" style="width: 10%">%</td>
					<td class="hright" style="width: 3%">${o.currency_id.symbol}</td>
					<td class="hright" style="width: 15%">${formatLang(x.price_subtotal) or formatLang(0)}</td>
					
				</tr>
				%endfor	
				<tr>
					<td colspan="8" class="border_bottom"><br></br></td>
				</tr>
			<tr>
				<td colspan="4"></td>
				<td colspan="2" class="hright">Total :</td>
				<td> ${o.currency_id.symbol}</td>
				<td class="hright">${formatLang(o.amount_untaxed) or formatLang(0)}</td>
			</tr>
			<tr>
				<td colspan="4"></td>
				<td colspan="2" class="hright">Discount :</td>
				<td> ${o.currency_id.symbol}</td>
				<td class="hright"> ${formatLang(0)}</td>
			</tr>
			<tr>
				<td colspan="4"></td>
				<td colspan="2" class="hright">Gross Total :</td>
				<td class="hleft border_top"> ${o.currency_id.symbol}</td>
				<td class="hright border_top">${formatLang(o.amount_untaxed) or formatLang('0')}</td>
			</tr>
			%if o.amount_tax > 0
			<tr>
				<td colspan="4"></td>
				<td colspan="2" class="hright">PPN 10% :</td>
				<td> ${o.currency_id.symbol}</td>
				<td class="hright">${formatLang(o.amount_tax) or formatLang('0')}</td>
			</tr>
			%endif
			<tr>
				<td colspan="4"></td>
				<td colspan="2" class="hright">${o.add_reason or ''} :</td>
				<td> ${o.currency_id.symbol}</td>
				<td class="hright">${formatLang(o.add_amount) or formatLang('0')}</td>
			</tr>
			<tr>
				<td colspan="4"></td>
				<td colspan="2" class="hright border_top font14px">Net Total :</td>
				<td class="hleft border_top"> ${o.currency_id.symbol}</td>
				<td class="hright border_top">${formatLang(o.amount_total) or formatLang('0')}</td>
			</tr>	
			</table>
			<table class="font12px one perjanjian" width="100%">
				<tr>
					<td width="10%">Notes</td>
					<td>
						: ${o.notes or ''}
					</td>
				</tr>
			</table>
        	
				
				
		
       
       %endfor 	
       </body>
   </html>
  