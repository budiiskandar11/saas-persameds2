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
			.border_top
			{
				border-top: 1px solid black;
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
		</style>
	</head>
	<body>
	% for o in objects:
        <table width="100%" border="0">
        	<tr>
				<td width="35%">&nbsp;</td>
				<td width="30%" align="center" class="vbottom">&nbsp;</td>
				<td width="35%" rowspan="3" align="right">${helper.embed_company_logo()|safe}<br/>
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
				<td class="hleft vtop">&nbsp;</td>
				<td valign="top" class="hleft">
					<h2>
						${ o.state == 'draft' and 'DRAFT' or o.state == 'quot' and 'QUOTATION' or 'SALE ORDER'}
					</h2>
				</td>
			</tr>
			<tr>
				<td class="hleft vtop">
					<b>Date:</b> ${o.date_order}<br/><br/>
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
				<td>
				<br/><br/>
				<b>Shipping Address:</b><br/>
						<span class="font12px">${o.partner_shipping_id and o.partner_shipping_id.name or ''}<br/>
						${o.partner_shipping_id and o.partner_shipping_id.street or ''}<br/>
						${o.partner_shipping_id and o.partner_shipping_id.city or ''}
						${o.partner_shipping_id and o.partner_shipping_id.state_id.name or ''}
						${o.partner_shipping_id and o.partner_shipping_id.zip or ''}<br/>
						${o.partner_shipping_id and o.partner_shipping_id.country_id.name or ''}<br/><br/>
						<b>Phone No.</b> ${o.partner_shipping_id and o.partner_shipping_id.phone or ''}<br/>	
						<b>&nbsp;</b><br/>
						</span>
				</td>
			</tr>
        </table>
        <br/>
		<table width="100%">
			<tr>
				<td colspan="2" width="50%"><b>
				% if o.state == 'draft':	
					Draft Reference No: 
				% elif o.state == 'quot':						
					Quotation Reference No: 
				% else:	
					Sale Order Reference No: 
				%endif
				
				 &nbsp;&nbsp;&nbsp;&nbsp; ${o.name}</b></td>
				<td class="hmid" colspan="2" width="50%"><b>Valid To: &nbsp;&nbsp;&nbsp;&nbsp; ${o.valid_date or "N/A"}</b></td>
			</tr>
		</table>
		<br/>
		<table width="100%">
			<tr>
				<th colspan="6" class="content hleft">Details</th>
			</tr>
			<tr>
				<th width="8%" class="hleft">Qty</th>
				<th width="50%" class="hleft">Description</th>
				<th width="15%" class="hleft">Unit Price</th>
				<th width="5%">Disc.</th>
				<th width="7%">Tax</th>
				<th width="15%">Price</th>
			</tr>
			%for line in o.order_line:
			<tr>
				<td class="content border_bottom_grey hleft">${formatLang(line.product_uom_qty)}</td>
				<td class="content border_bottom_grey">${line.name}</td>
				<td class="content border_bottom_grey paddingright"> ${formatLang(line.price_unit)}</td>
				<td class="content border_bottom_grey hright">${ formatLang(line.discount) or 0.0 }</td>
				<td class="content border_bottom_grey hright">
				%for t in line.tax_id:
					${t.name}
				%endfor
				</td>
				<td class="content border_bottom_grey hright"> ${formatLang(line.price_subtotal)}</td>
			</tr>
			%endfor
			<tr>
				<td colspan="3">&nbsp;</td>
				<td class="content" colspan="2"> Total :</td>
				<td class="content border_top hright"> ${o.company_id.currency_id.name or 'Rp'} ${formatLang(o.gross_total)}</td>
			</tr>
			<tr>
				<td colspan="3">&nbsp;</td>
				<td class="content" colspan="2">Discount :</td>
				<td class="content hright"> ${o.company_id.currency_id.name or 'Rp'} ${formatLang(o.discount_total)}</td>
			</tr>
			<tr>
				<td colspan="3">&nbsp;</td>
				<td class="content" colspan="2">Untaxed :</td>
				<td class="content border_top hright"> ${o.company_id.currency_id.name or 'Rp'} ${formatLang(o.amount_untaxed)}</td>
			</tr>
			<tr>
				<td colspan="3">&nbsp;</td>
				<td class="content" colspan="2">Taxes :</td>
				<td class="content hright"> ${o.company_id.currency_id.name or 'Rp'} ${formatLang(o.amount_tax)}</td>
			</tr>
		</table>
		<table class="fright">
			<tr>
				<td width=50%>&nbsp;</td>
				<td class="padding"><b>NET TOTAL :&nbsp;&nbsp;  ${o.company_id.currency_id.name or 'Rp'} ${formatLang(o.amount_total)}</b></td>
			</tr>
		</table>
		<table class="content padding border_black fright" width="75%">
			<tr>
				<td class="content vtop hright paddingright"><b>Terms and Condition :</b></td>
				<td class="content">* Terms of Payment : ${o.payment_term.name or '-'}.
				<br/>* Prices are inclusive of VAT.
				<br/>* Payment is required prior to goods being dispatched.
				</td>
			</tr>
			<tr>
				<td class="content vtop hright paddingright"><b>Notes :</b></td> 
				<td class="content"> ${o.note or '-'}.
				
				</td>
			</tr>
		</table>
		<br /><br /><br /><br /><br /><br/>
		<p>
			<b style="font-size:12px">Quotation Acceptance - <b>FAX TO: ${o.company_id.fax or '-'} / EMAIL TO: ${o.company_id.email or '-'}</b></b>
		</p>
		<table  class="content border_grey" border="1px" cellspacing="0px" width="100%">
			<tr>
				<td class="content padding">
					I hereby accept this proposal and authorize ProbeLogic to proceed with the above mentioned purchase.<br/><br/>
					<table width="100%" cellpadding="10px">
						<tr>
							<td width="25%">Purchase Order #</td>
							<td width="25%">_____________________________</td>
							<td width="10%">Date</td>
							<td width="40%">______________________________</td>
						</tr>
						<tr>
							<td width="25%">Signed</td>
							<td width="25%">_____________________________</td>
							<td width="10%">Name</td>
							<td width="40%">______________________________</td>
						</tr>
					</table>
				</td>
			</tr>
		</table>
		</br><br /><br /><br /><br />
		<p class="content">
			If you select to accept this quotation, please complete the above and return to ${o.company_id.name or '-'} by FAX or email.
		</p>
		
    % endfor
	<!--
	% for o in objects:
		<table width="100%" border="0">
			<tr>
				<td width="35%">&nbsp;</td>
				<td width="30%" align="center" class="vbottom"><h2>QUOTATION</h2></td>
				<td width="35%" align="right">${helper.embed_image('jpg',o.company_id.logo, width=110, height=auto)}</td>
			</tr>
			<tr>
				<td class="hleft vtop">
					<b>Date:</b> ${o.date_order}<br/><br/>
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
					<span class="font12px">${o.partner_id and o.partner_id.name or ''}
					</span>
				</td>
				<td class="hright vtop content">	
					<span class="font12px">${o.company_id.street or '-'}<br/>
					${o.company_id.city or '-'} ${o.company_id.zip or '-'}<br/>
					${o.company_id.state_id and o.company_id.state_id.name or '-'}<br/><br/>
					Tel: ${o.company_id.phone or '-'}<br/>
					Fax: ${o.company_id.fax or '-'}<br/><br/>
					${o.company_id.email or '-'}<br/>
					${o.company_id.website or '-'}<br/>
					</span>
				</td>
			</tr>
		</table>
		<br/>
		<table width="100%">
			<tr>
				<td colspan="2" width="50%"><b>Quotation Reference No: &nbsp;&nbsp;&nbsp;&nbsp; ${o.name}</b></td>
				<td class="hmid" colspan="2" width="50%"><b>Valid To: &nbsp;&nbsp;&nbsp;&nbsp; ${o.valid_date or "N/A"}</b></td>
			</tr>
		</table>
		<br/>
		<hr class="border_top"/>
		<table width="100%">
			<tr>
				<th colspan="6" class="content hleft">Details</th>
			</tr>
			<tr>
				<th width="8%" class="hleft">Qty</th>
				<th width="50%" class="hleft">Description</th>
				<th width="15%" class="hleft">Unit Price</th>
				<th width="5%">Disc.</th>
				<th width="7%">Tax</th>
				<th width="15%">Price</th>
			</tr>
			%for line in o.order_line:
			<tr>
				<td class="content border_bottom_grey hleft">${formatLang(line.product_uom_qty)}</td>
				<td class="content border_bottom_grey">${line.name}</td>
				<td class="content border_bottom_grey paddingright">${formatLang(line.price_unit)}</td>
				<td class="content border_bottom_grey hright">${ formatLang(line.discount) or 0.0 }</td>
				<td class="content border_bottom_grey hright">
				%for t in line.tax_id:
					${t.name}
				%endfor
				</td>
				<td class="content border_bottom_grey hright">${formatLang(line.price_subtotal)}</td>
			</tr>
			%endfor
			<tr>
				<td colspan="3">&nbsp;</td>
				<td class="content" colspan="2">Total Amount :</td>
				<td class="content border_top hright">${formatLang(o.amount_untaxed)}</td>
			</tr>
			<tr>
				<td colspan="3">&nbsp;</td>
				<td class="content" colspan="2">Total Discount :</td>
				<td class="content border_top hright">${formatLang(o.amount_untaxed)}</td>
			</tr>
			<tr>
				<td colspan="3">&nbsp;</td>
				<td class="content" colspan="2">Net Total :</td>
				<td class="content border_top hright">${formatLang(o.amount_untaxed)}</td>
			</tr>
			<tr>
				<td colspan="3">&nbsp;</td>
				<td class="content" colspan="2">Taxes :</td>
				<td class="content hright">${formatLang(o.amount_tax)}</td>
			</tr>
		</table>
		<table class="fright">
			<tr>
				<td width=50%>&nbsp;</td>
				<td class="border_black padding"><b>GRAND TOTAL :&nbsp;&nbsp; ${formatLang(o.amount_total)}</b></td>
			</tr>
		</table>
		<table class="content padding border_black fright" width="75%">
			<tr>
				<td class="content vtop hright paddingright"><b>Terms and Agreement :</b></td>
				<td class="content"><b>* Terms of Payment :
				<br/>* Prices are inclusive of VAT
				<br/>* Payment is required prior to goods being dispatched.</b>
				</td>
			</tr>
		</table>
		
		
	% endfor
	-->
	</body>
</html>