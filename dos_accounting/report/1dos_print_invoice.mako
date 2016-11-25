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
			.border_left_right
			{
				border-top: 1px solid black;
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
			.font22px
			{
				font-size: 18px;
			}
			.font30px
			{
				font-size: 30px;
			}
			
			
		</style>
	</head>
	%for o in objects:
	<body>
		<table width="100%" border="0">
			<tr valign="top">
				<td colspan="3" class="vtop">
					<span class="font22px"><b>Commercial</b><br/>
					<span class="font30px"><b>Tax Invoice</b><br/></span>				
				</td>
				<td rowspan="7" class="hright vtop">	
					${helper.embed_company_logo()|safe}<br/>			
					<span class="font12px">${o.company_id.street or '-'}<br/>
					${o.company_id.city or '-'} ${o.company_id.zip or '-'}<br/>
					${o.company_id.state_id and o.company_id.state_id.name or '-'}<br/>
					Tel: ${o.company_id.phone or '-'}<br/>
					Fax: ${o.company_id.fax or '-'}<br/>
					${o.company_id.email or '-'}<br/>
					${o.company_id.website or '-'}<br/>
					</span>
				</td>
			</tr>			
			<tr>
				<td>&nbsp;&nbsp;</td>
				<td>&nbsp;&nbsp;</td>
				<td>&nbsp;&nbsp;</td>
			</tr>
			<tr>
				<td>
					<b>Date&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: ${o.date_invoice or ''}</b>
				</td>
			</tr>
			<tr>
				<td>
					<b>Invoice &nbsp;&nbsp; #${o.number or 'Draft'}</b>
				</td>
			</tr>
			<tr>
				<td>&nbsp;&nbsp;</td>
				
			</tr>
			<tr>
				<td class="hleft vtop">

				<b>Billing Address:</b><br/>
				<span class="font12px">${o.partner_id and o.partner_id.name or ''}<br/>
				${o.partner_id and o.partner_id.street or ''}<br/>
				${o.partner_id and o.partner_id.city or ''}
				${o.partner_id and o.partner_id.state_id.name or ''}
				${o.partner_id and o.partner_id.zip or ''}<br/>
				${o.partner_id and o.partner_id.country_id.name or ''}<br/><br/>
				<b>Phone No.</b> ${o.partner_id and o.partner_id.phone or ''}<br/>	
				<b>&nbsp;</b><br/>
				</span>				

					
				</td>
				
			</tr>
		</table>
		<table cellpadding="2px" width="100%" style="border:1px solid black;">
			<tr >
				<td align="left"><b><span class="font12px border_bottom_grey">Responsible :</span></b></td>
				<td align="left"><b><span class="font12px border_bottom_grey">Order No. :</span></b></td>
				<td align="left"><b><span class="font12px border_bottom_grey">Reference :</span></b></td>
				
				
			</tr>
			<tr>
				
				<td align="left" ><span class="font12px">${ o.user_id and o.user_id.name or ''}</span></td>
				<td align="left" ><span class="font12px">${ o.origin or ''}</span></td>
				<td align="left" ><span class="font12px">${ o.name or ''}</span></td>
				
			</tr>
		</table>
		<table>
			<tr>
				<td></td>
			</tr>
		</table>
		
		<table cellpadding="5px" width="100%" style="border:1px solid black;">
			
			<tr>
				<th width="8%" class="hleft background_color" >Qty</th>
				<th width="50%" class="hleft background_color">Description</th>
				<th width="15%" class="hleft background_color">Unit Price</th>
				<th width="5%" class="background_color">Disc.</th>
				<th width="7%" class="background_color">Tax</th>
				<th width="15%" class="background_color">Price</th>
			</tr>
			
			%for l in o.invoice_line:
			<tr>
				<td class="content border_bottom_grey hleft">${ formatLang(l.quantity) or formatLang(0)}</td>
				<td class="content border_bottom_grey hleft">${ l.name or ''}</td>
				<td class="content border_bottom_grey hright">${ o.currency_id.symbol or ''} ${ formatLang(l.price_unit) or formatLang(0)}</td>
				<td class="content border_bottom_grey hleft">${ formatLang(l.discount) or 0.0}</td>
				<td class="content border_bottom_grey hleft">
				%for t in l.tax_id:
					${t.name}
				%endfor
				</td>
				<td class="content border_bottom_grey hright">${ o.currency_id.symbol or ''} ${ formatLang(l.price_subtotal) or formatLang(0)}</td>
			%endfor
			</tr>
			
			<tr >
				<td width="60%" colspan="2" rowspan="3" border="0">
					<table width="100%" height="100%" cellpadding="5px" cellspacing="0px" border="0">
						<tr align="left" valign="top" class="font12px">
							<td valign="top">
								<span>Comment:</span><br/>
								<span valign="top"><i>${ o.comment or ''}</i></span><br/><br/>
								<hr/>
								<span valign="bottom" class="font12px">Customer ABN:</span>
							</td>
						</tr>
					</table>
				</td>				
								
				<td width="40%" colspan="4">
					<table width="100%" height="100%">
						<tr class="font12px">
							<td>Total</td>
							<td class="border_top hright">${ o.currency_id.symbol or ''} ${ formatLang(o.gross_total)}</td>
						</tr>
						<tr class="font12px">
							<td>Discount</td>
							<td align="right">${ o.currency_id.symbol or ''} ${ formatLang(o.discount_total)}</td>
						</tr>
						<tr class="font12px" >
							<td >Total Untaxed Amount</td>
							<td class="border_top hright" align="right">${ o.currency_id.symbol or ''} ${ formatLang(o.amount_untaxed)}</td>
						</tr>
						
						<tr class="font12px">
							<td>Tax</td>
							<td align="right">${ o.currency_id.symbol or ''} ${ formatLang(o.amount_tax)}</td>
						</tr>
						<tr class="font12px">
							<td class="border_top hleft"><b>NET TOTAL</b></td>
							<td class="border_top hright"><b>${ o.currency_id.symbol or ''} ${ formatLang(o.amount_total) }</b></td>
						</tr>
						<tr class="font12px">
							<td><b>PAID TO DATE</b></td>
							<td align="right"><b>${ o.currency_id.symbol or ''}${ o.state in ('open','proforma','proforma2') and formatLang(o.amount_total-o.residual) or formatLang(0)}</b></td>
						</tr>
						<tr class="border_left_right">
							<td class="font22px"><b>BALANCE:</b></td>
							<td class="font22px"align="right"><b>${ o.currency_id.symbol or ''} ${ formatLang(o.residual) or formatLang(0)}</b></td>
						</tr>
					</table>
				</td>
			</tr>
		</table>
		<table>
			<tr>
				<td></td>
			</tr>
		</table>
		<table width="100%">
			<tr>
				<td width="50%" align="left" valign="top">
					<table class="font12px" width="100%" style="border-top:1px solid black;border-bottom:1px solid black;border-left:1px solid black;border-right:1px solid black;" align="right">
						
						<tr>
							<td><b><u>Payment Details </u></b></td>
							<td><i>Please remit directly to:</i></td>
						</tr>
						<tr>
							<td>&nbsp&nbsp&nbsp Bank </td>
							<td>: Bankwest</td>
						</tr>
						<tr>
							<td>&nbsp&nbsp&nbsp Account Name</td>
							<td>: PT Databit Solusi Indonesia</td>
						</tr>
						<tr>
							<td>&nbsp&nbsp&nbsp Account No</td>
							<td>: 0442318</td>
						</tr>
					</table>
				</td>
				
					<td width="50%" align="left" valign="top">
					<table class="font12px" width="100%" style="border-top:1px solid black;border-bottom:1px solid black;border-left:1px solid black;border-right:1px solid black;" align="right">
						<tr>
							<td><b><u>Other Information</u></b></td>
							<td></td>
						</tr>
						<tr>
							<td>&nbsp&nbsp&nbsp Payment Terms</td>
							<td>: ${o.payment_term and o.payment_term.name or '14 DAYS'} </td>
						</tr>
						<tr>
							<td>&nbsp&nbsp&nbsp Company NPWP No</td>
							<td>: 122.099.009.990990</td>
						</tr>
						<tr>
							<td>&nbsp&nbsp&nbsp Company NPWP Name</td>
							<td>: PT Databit Solusi Indonesia</td>
						</tr>
						
					</table>
				</td>
			</tr>
		</table>
		<table width="100%">
			<tr>
				<td>&nbsp;</td>
			</tr>
		</table>	
		<table width="100%" valign="bottom">
			<tr>
				<td align="center" class="font12px">
								${ 'STATEMENTS NOT ISSUED - PLEASE PAY ON INVOICE'}</b></td>
			</tr>
		</table>
	</body>
	%endfor
	
</html>