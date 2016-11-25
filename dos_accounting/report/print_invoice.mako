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
	<body>
		<table width="100%" border="0">
			<tr valign="top">
				<td colspan="3" class="vtop">
					<span class="font22px"><b>Commercial</b><br/>
					<span class="font30px"><b>Tax Invoice</b><br/></span>				
				</td>
				<td rowspan="7" class="hright vtop">	
					${helper.embed_image('jpg',o.company_id.logo, width=110, height=auto)}<br/>			
					<span class="font12px">${o.company_id.street or '-'}<br/>
					${o.company_id.city or '-'} ${o.company_id.zip or '-'}<br/>
					${o.company_id.state_id and o.company_id.state_id.name or '-'}<br/><br/>
					Tel: ${o.company_id.phone or '-'} (Aust)<br/>
					Tel: +61 8 8125 4744 (Int'l)<br/>
					Fax: ${o.company_id.fax or '-'}<br/><br/>
					${o.company_id.email or '-'}<br/>
					${o.company_id.website or '-'}<br/>
					<b>A.B.N. ${o.company_id.abn or '-'}</b><br/>
					</span>
				</td>
			</tr>			
			<tr>
				<td>&nbsp;&nbsp;</td>
				<td>&nbsp;&nbsp;</td>
				<td>&nbsp;&nbsp;</td>
			</tr>
			<tr>
				<td width="12%">
					<b>Date:</b>
				</td>
				<td><b>${o.date_invoice or ''}</b><br/></td>
				<td>
					<table width="100%">
						<tr>
							<td>&nbsp;</td>
						</tr>
					</table>	
				</td>
			</tr>
			<tr>
				<td>
					<b>Invoice&nbsp;&nbsp;#</b>
				</td>
				<td><b>${o.number or ''}</b><br/></td>
				<td>					
					<table width="100%">
						<tr>
							<td>&nbsp;</td>
						</tr>
					</table>	
				</td>
			</tr>
			<tr>
				<td>&nbsp;&nbsp;</td>
				<td>&nbsp;&nbsp;</td>
				<td>&nbsp;&nbsp;</td>
			</tr>
			<tr>
				<td>&nbsp;&nbsp;</td>
				<td>&nbsp;&nbsp;</td>
				<td>&nbsp;&nbsp;</td>
			</tr>
			<tr>
				<td align="left" valign="bottom">&nbsp;</td>
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
				<td class="hleft vtop">
					<b>Ship To:</b><br/>
					<span class="font12px">${o.partner_id and o.partner_id.name or ''}<br/>
					${o.street or ''}<br/>
					${o.city or ''}
					${o.state_id and o.state_id.name or ''}
					${o.zip or ''}<br/>
					${o.country_id.name or ''}<br/><br/>
					%if o.phone:
					<b>Phone No.</b> ${o.phone or ''}
					%endif
					<br/>
					</span>
				</td>
			</tr>
		</table>
		--
		<table cellpadding="5px" width="100%">
			<tr>
				<td align="center"><b><span class="font12px">Service Provider</span></b></td>
				<td align="center"><b><span class="font12px">Order No.</span></b></td>
				<td align="center"><b><span class="font12px">Ship Via</span></b></td>
			</tr>
			<tr>
				<td align="center" style="border:1px solid black;"><span class="font12px">${ o.user_id and o.user_id.name or ''}</span></td>
				<td align="center" style="border:1px solid black;"><span class="font12px">${ o.name or ''}</span></td>
				<td align="center" style="border:1px solid black;"><span class="font12px">${ o.out_courier_id and o.out_courier_id.name or ''}</span></td>
			</tr>
		</table>
		<table cellpadding="5px" width="100%" style="border:1px solid black;">
			<tr>
				<td align="left" width="35%"><span class="font12px"><b>Equipment</b>:&nbsp;${o.equipment_type_id and o.equipment_type_id.name or ''}</span></td>
				<td align="left" width="20%"><span class="font12px"><b>Make</b>:&nbsp;${o.manufacturer_id and o.manufacturer_id.name or ''}</span></td>
				<td align="left" width="20%"><span class="font12px"><b>Model</b>:&nbsp;${o.model_id and o.model_id.name or ''}</span></td>
				<td align="left" width="25%"><span class="font12px"><b>Serial</b>:&nbsp;${o.serial_number or ''}</span></td>
			</tr>
		</table>	
		<table border="1px" cellspacing="0px" cellpadding="5px" width="100%">
			<tr class="font12px">
				<th width="5%">QTY.</th>
				<th width="42%">DESCRIPTION</th>
				<th width="15%">PRICE</th>
				<th width="5%">DISC.</th>
				<th width="15%">EXTENDED</th>
				<th width="8%">TAX (GST)</th>
			</tr>
			<% rate = 0.0 %>
			%for l in o.invoice_line:
			<tr class='inv_line'>
				<td>${ formatLang(l.quantity) or formatLang(0)}</td>
				<td>${ l.name or ''}</td>
				<td align="right">${ o.currency_id.symbol or ''}${ formatLang(l.price_unit) or formatLang(0)}</td>
				<td align="right">${ formatLang(l.discount) or 0.0}</td>
				<td align="right">${ o.currency_id.symbol or ''}${ formatLang(l.price_subtotal) or formatLang(0)}</td>
				<td align="center">
				%if l.invoice_line_tax_id:
					%for t in l.invoice_line_tax_id:
						<% rate = 100.0*t.amount %>
						${ t.name }
					%endfor
				%else:
					'N-T'
				%endif
				</td>
			</tr>
			%endfor
			${blank_line(9,nourut([line for line in o.invoice_line], l)) or ''}
			<tr>
				<td width="60%" colspan="2" rowspan="3">
					<table width="100%" height="100%" cellpadding="5px" cellspacing="0px" border="0">
						<tr align="left" valign="top" class="font12px">
							<td valign="top">
								<span>Comment:</span><br/>
								<span valign="top">${ o.comment or ''}</span><br/><br/>
								<hr/>
								<span valign="bottom" class="font12px">Customer ABN:</span>
							</td>
						</tr>
					</table>
				</td>				
				<td width="40%" colspan="4">
					<table width="100%" height="100%">
						<tr class="font12px">
							<td>Sale Amount</td>
							<td align="right">${ o.currency_id.symbol or ''}${ formatLang(o.amount_untaxed) or formatLang(0)}</td>
						</tr>
						<tr class="font12px">
							<td>Freight</td>
							<td align="right">${ o.currency_id.symbol or ''}${ formatLang(o.amount_freight) or formatLang(0)}</td>
						</tr>
						<tr class="font12px">
							<td>TAX (GST)</td>
							<td align="right">${ o.currency_id.symbol or ''}${ formatLang(o.amount_tax) or formatLang(0)}</td>
						</tr>
						<tr class="font12px">
							<td><b>TOTAL</b></td>
							<td align="right"><b>${ o.currency_id.symbol or ''}${ formatLang(o.amount_total) or formatLang(0)}</b></td>
						</tr>
						<tr class="font12px">
							<td><b>PAID TO DATE</b></td>
							<td align="right"><b>${ o.currency_id.symbol or ''}${ o.state in ('open','proforma','proforma2') and formatLang(o.amount_total-o.residual) or formatLang(0)}</b></td>
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
				<td width="51%" align="left" valign="top">
					<table class="font12px" width="100%" style="border-top:1px solid black;border-bottom:1px solid black;border-left:1px solid black;border-right:1px solid black;" align="right">
						<tr>
							<td><b><u>Bank Payment info:</u></b></td>
							<td><i>Please remit directly to:</i></td>
						</tr>
						<tr>
							<td>Bank:</td>
							<td>Bankwest</td>
						</tr>
						<tr>
							<td>Account Name:</td>
							<td>ProbeLogic Pty Ltd</td>
						</tr>
						<tr>
							<td>BSB:</td>
							<td>306-054</td>
						</tr>
						<tr>
							<td>Account No:</td>
							<td>0442318</td>
						</tr>
					</table>
				</td>
				<td width="49%" align="right" valign="top">
					<table cellpadding="5px" width="98%" style="border-top:1px solid black;border-bottom:1px solid black;border-left:1px solid black;border-right:1px solid black;" align="right">
						<tr>
							<td><b>BALANCE:</b></td>
							<td align="right"><b>${ o.currency_id.name or ''}${ o.currency_id.symbol or ''}${ formatLang(o.residual) or formatLang(0)}</b></td>
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
				<td align="center" class="font12px"><b>TERMS ${o.payment_term and o.payment_term.name or '14 DAYS'} FROM INVOICE DATE<br/>
								${ 'STATEMENTS NOT ISSUED - PLEASE PAY ON INVOICE'}</b></td>
			</tr>
		</table>
	</body>
	%endfor
</html>