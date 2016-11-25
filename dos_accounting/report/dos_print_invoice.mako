<html>
	<head>
		<style>
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
			.border_top_thin
			{
				border-top: 0.5px solid black
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
				
				<td style="width:50%" class="vtop hleft">
					<span class="font14px"><b>Date&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: ${o.date_invoice or ''}</b><br/>
					<span class="font14px"><b>Invoice No :&nbsp;&nbsp; #${o.number or 'Draft'}</b><br/></span>				
				</td>
				<td style="width:50%" class="hright">
					<span class="font22px"><b>Commercial</b><br/>
					<span class="font30px"><b>Tax Invoice</b><br/></span>				
				</td>
				
				
			</tr>			
			
	
			<tr>
				<td class="hleft vtop">

				<b>Billing Address:</b><br/>
				<span class="font12px">${o.partner_id and o.partner_id.name or ''}<br/>
				${o.partner_id and o.partner_id.street or ''}<br/>
				${o.partner_id and o.partner_id.street2 or ''}<br/>
				${o.partner_id and o.partner_id.city or ''}
				${o.partner_id and o.partner_id.state_id.name or ''}
				${o.partner_id and o.partner_id.zip or ''}<br/>
				${o.partner_id and o.partner_id.country_id.name or ''}<br/>
				 ${o.partner_id and o.partner_id.phone or ''}<br/>	
				<b>&nbsp;</b><br/>
				</span>	
				</td>
				
			</tr>
		</table>
		<table cellpadding="2px" width="100%" style="border:1px solid black;">
			<tr >
				<td align="left"><b><span class="font12px">Responsible : ${ o.user_id and o.user_id.name or ''}</span></b></td>
				<td align="left"><b><span class="font12px">Reference : ${ o.origin or ''}</span></b></td>	
			</tr>
			
			
		</table>
		
		
		<table cellpadding="3px" width="100%" class="one">
		<tr>
				<td><br/></td>
			</tr>
			<tr>
				<th colspan="6" class="hleft"><b>Invoice Details</b><br/></th>
			</tr>
			<tr>
				<th width="5%" class="hleft background_color">No</th>
				<th width="40%" class="hleft background_color">Description</th>
				<th width="10%" class="hleft background_color" >Qty</th>
				<th width="15%" class="hleft background_color">Unit Price (${ o.currency_id.symbol or ''})</th>
				<th width="10%" class="background_color">Disc.</th>
				<th width="20%" class="background_color">Price (${ o.currency_id.symbol or ''})</th>
			</tr>
			<% set i=0%>
			%for l in o.invoice_line:
			<% set i=i+1%>
			<tr>
				<td class=" font11px content border_bottom_thin hmid">${i}</td>
				<td class="font11px content border_bottom_thin hleft">${ l.name or ''}</td>
				<td class=" font11px content border_bottom_thin hleft">${ formatLang(l.quantity) or formatLang(0)}</td>
				
				<td class="font11px content border_bottom_thin hright">${ formatLang(l.price_unit) or formatLang(0)}</td>
				<td class="font11px content border_bottom_thin hmid">${ formatLang(l.discount) or 0.0}</td>
				
				<td class="font11px content border_bottom_thin hright">${ formatLang(l.price_subtotal) or formatLang(0)}</td>
			%endfor
			</tr>
			
			<tr >
				<td width="60%" colspan="2" rowspan="3" border="0" class="font11px content vtop">Comment:<br/>
								<span valign="top"><i>${ o.comment or ''}</i></span><br/><br/>
								
				</td>				
								
				<td width="40%" colspan="4">
					<table width="100%" height="100%">
						<tr class="font11px">
							<td>Total</td>
							<td class="hright">${ formatLang(o.gross_total)}</td>
						</tr>
						<tr class="font11px">
							<td>Discount</td>
							<td align="right">${ formatLang(o.discount_total)}</td>
						</tr>
						<tr class="font11px" >
							<td >Total Untaxed Amount</td>
							<td class="border_top hright" align="right">${ formatLang(o.amount_untaxed)}</td>
						</tr>
						
						<tr class="font11px">
							<td>Tax</td>
							<td align="right">${ formatLang(o.amount_tax)}</td>
						</tr>
						<tr class="font12px">
							<td class="border_top hleft"><b>NET TOTAL</b></td>
							<td class="border_top hright"><b>${ formatLang(o.amount_total) }</b></td>
						</tr>
						<tr class="font12px">
							<td><b>PAID TO DATE</b></td>
							<td align="right"><b>${ o.state in ('open','proforma','proforma2') and formatLang(o.amount_total-o.residual) or formatLang(0)}</b></td>
						</tr>
						<tr class="border_left_right border_bottom">
							<td class="font12px "><b>BALANCE:</b></td>
							<td class="font12px "align="right"><b>${ formatLang(o.residual) or formatLang(0)}</b></td>
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
		<table width="100%" style="page-break-inside: avoid">
			<tr>
				<td width="50%" align="left" valign="top">
					<table class="font12px one" width="100%" style="border-top:1px solid black;border-bottom:1px solid black;border-left:1px solid black;border-right:1px solid black;" align="right">
						
						<tr>
							<td colspan="3"><b><u>Payment Terms </u></b></td>
						</tr>
						<tr>
							<td style="width:10%" class="border_bottom">No</td>
							<td style="width:60%" class="border_bottom">Name</td>
							<td style="width:30%" class="border_bottom" >Amount (${ o.currency_id.symbol or ''})</td>
						</tr>
						<% set i=0%>
						%if o.payment_term :
							%for terms in o.payment_term.line_ids :
							<% set i=i+1 %>
							<tr>
									<td class="hleft">${i}</td>
									
									%if terms.value == 'procent':
										%if i == 1
											<td class="hleft">Payments DP ${terms.value_amount*100 or ''}%</td>
										%else
											<td class="hleft">Payments # ${i} ${terms.value_amount*100 or ''}%</td>
										%endif
										<td class="hright">${formatLang(terms.value_amount * o.amount_total)}</td>
										
									%elif terms.value == 'fixed':
										<td class="hleft">Payments # ${i}</td>
										<td class="hright">${formatLang(terms.value_amount)}</td>
									%else: 
										<td class="hleft">Payments # ${i}</td>
										<td class="hright">${formatLang((o.amount_total)-(terms|sum(attribute='value_amount')))}</td>
									%endif
							</tr>
							%endfor
						%else :
							<tr>
								<td class="hleft border_bottom">1</td>
								<td class="hleft border_bottom">Payments</td>
								<td class="hright border_bottom">${formatLang(o.amount_total)}</td>
							</tr>
						%endif
					</table>
				</td>
				
					<td width="50%" align="left" valign="top">
					<table class="font12px" width="100%" style="border-top:1px solid black;border-bottom:1px solid black;border-left:1px solid black;border-right:1px solid black;" align="right">
						<tr>
							<td colspan="2"><b><u> Information</u></b></td>
							
						</tr>
						<tr>
							<td>&nbsp&nbsp&nbsp Company NPWP No</td>
							<td>: 73.268.227.3-432.000</td>
						</tr>
						<tr>
							<td>&nbsp&nbsp&nbsp Company NPWP Name</td>
							<td>: PT Persada Medika Solusindo</td>
						</tr>
						<tr>
							<td><b><u>Payment Details </u></b></td>
							<td><i>Please remit directly to:</i></td>
						</tr>
						<tr>
							<td>&nbsp&nbsp&nbsp Bank </td>
							<td>: PT Bank Mandiri Tbk </td>
						</tr>
						<tr>
							<td>&nbsp&nbsp&nbsp Cabang </td>
							<td>: KCP Cibubur Citra Grand</td>
						</tr>
						%if o.amount_tax > 0
						<tr>
							<td>&nbsp&nbsp&nbsp Account Name</td>
							<td>: PT Persada Medika Solusindo</td>
						</tr>
						<tr>
							<td>&nbsp&nbsp&nbsp Account No</td>
							<td>: 167-000-141-887-9</td>
						</tr>
						%else
						<tr>
							<td>&nbsp&nbsp&nbsp Account Name</td>
							<td>: Surono</td>
						</tr>
						<tr>
							<td>&nbsp&nbsp&nbsp Account No</td>
							<td>: 900-003-080-796-1</td>
						</tr>
						%endif
						
					</table>
				</td>
			</tr>
			
		</table>
		<table width="100%" class="font12px">
		<tr>
			<td><br/></td>
		</tr>
			<tr>
				<td>Validate By</td>
			</tr>
		<tr>
			<td><br/><br/><br/></td>
		</tr>
		<tr>
		<td>${o.user_id.name or ''}</td>
		</tr>
		<tr>
		<td>Finance</td>
		</tr>
		</table>	
		<table width="100%" valign="bottom">
		<tr>
			<td><br/></td>
		</tr>
			<tr>
				<td align="center" class="font12px">
								${ 'STATEMENTS NOT ISSUED - PLEASE PAY ON INVOICE'}</b></td>
			</tr>
		</table>
	</body>
	%endfor
	
</html>
