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
			#border_bottom_grey
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
			
			.list_table1{
			width:100%;
			font-size:11px;
			border-left:1px solid black;
			border-top:1px solid black;
        	border-bottom:1px solid black;
        	border-right:1px solid black;
		}
			
         	table.one 
         	{border-collapse:collapse;}
			
			#watermark {
			  color: #d0d0d0;
			  text-align:center;
			  font-size: 80pt;
			  -webkit-transform: rotate(-45deg);
			  position: fixed;
			  width: 500px;
			  height: 500px;
			  margin: 0;
			  z-index: -1;
			  left:130px;
			  top:150px;
				}
		
		</style>
</head>
<body>
	%for o in objects :
		%if o.type =='payment':
			<table class="list_table1" width="100%" cellpadding="2px" border="0">
			<tr>
				<td></td>
				<td>
			<table cellspacing="0" cellpadding="1px" width="100%" class="font12px" border="0">
		 		<tr>
		 			<td rowspan="3" width="10%"><span style="tadv-align:right;font-size:24">${helper.embed_company_logo(width=100, height=40)|safe}</span></td>
		 			<td width="70%" style="font-size:16px;">${o.company_id.name}</td>
		 			<td width="20%" style="font-size:11px;color:white;">Form No. : ${o.name or ''}</td>
		 		</tr>
		 		<tr>
		 			<td style="font-size:12px;">${o.create_uid.name}</td>
		 			<td rowspan="2" style="font-size:30px;text-align:center"><b>PV</b></td>
		 		</tr>
		 		<tr>
		 			<td>&nbsp;</td>
		 		</tr>
		 	</table>
			<table width="100%" class="font10px one" cellpadding="2px" border="0">
				<tr>
					<td colspan="3" class="font14px"><b>PAYMENT VOUCHER (${o.number})</b></td>
					<td>&nbsp;</td>
				</tr>
				<tr>
					<td  width="20%">PAID TO</td>
					<td>: ${o.partner_id.name}</td>
					<td  width="10%">NO.</td>
					<td>: ${o.payment_voucher_order_number}</td>
				</tr>
				<tr>
					<td width="20%">AMOUNT</td>
					%if o.amount > 0
					<td>: ${o.company_id.currency_id.symbol} ${formatLang(o.amount) or formatLang(0)}</td>
					%else
					<td>: ${o.company_id.currency_id.symbol} ${formatLang(o.amount) or formatLang(0)}</td>
					%endif
					<td>DATE</td>
					<td>: ${time.strftime('%d/%m/%Y', time.strptime( o.date,'%Y-%m-%d'))}</td>
				</tr>
				<tr>
					<td width="20%">BANK</td>
					<td>: </td>
					<td></td>
					<td></td>
				</tr>
				<tr>
					<td></td>
					<td></td>
					<td></td>
					<td><br/></td>
				</tr>
			</table>
			<table  cellpadding="2px" width="100%" class="font10px one" border="0">
				<tr bgcolor="#d3d3d3">
					<th width="20%" padding-top="1px" class="border_top_bottom border_left_right hmid">ACCOUNT CODE</th>
					<th width="50%" padding-top="1px" class="border_top_bottom border_left_right hmid">PARTICULAR</th>
					<th width="30%" padding-top="1px" class="border_top_bottom border_left_right hmid">AMOUNT</th>
				</tr>
				%for x in o.line_dr_ids :
					%if x.amount > 0.0:
						<tr>
							<td width="20%" class=" border_left_right hmid">${x.account_id.code}</td>
							<td width="50%" class=" border_left_right hleft">${x.move_line_id.invoice and x.move_line_id.invoice.invoice_line[0].name or x.move_line_id.ref or ''}</td>
							<td width="30%" class=" border_left_right hright">${o.company_id.currency_id.symbol} ${formatLang(x.amount) or ''}</td>
						</tr>
					%endif
				%endfor
				
				%for y in o.line_cr_ids :
					%if y.amount > 0.0:
						<tr>
							<td width="20%" class=" border_left_right hmid">${y.account_id.code}</td>
							<td width="50%" class=" border_left_right hleft">${y.move_line_id.invoice and y.move_line_id.invoice.invoice_line[0].name or y.move_line_id.name or ''}</td>
							<td width="30%" class=" border_left_right hright">${o.company_id.currency_id.symbol} ${formatLang(y.amount*-1) or ''}</td>
						</tr>
					%endif
				%endfor
				
				<tr>
					<td height="10px" class=" border_left_right hmid">&nbsp;</td>
					<td class=" border_left_right hmid">&nbsp;</td>
					<td class=" border_left_right hright">&nbsp;</td>
				</tr>
				<tr>
					<td width="20%" class="border_bottom border_left_right hmid"></td>
					<td width="50%" class="border_bottom border_left_right hright"><b>TOTAL</b></td>
					<td width="30%" class="border_bottom border_left_right hright"><b>${o.company_id.currency_id.symbol} ${formatLang(o.amount) or formatLang(0)}</b></td>
				</tr>
				<tr>
					<td ></td>
					<td ></td>
					<td >
						<br/>
						
					</td>
				</tr>
				
				%if o.journal_id.type == 'cash':
					<%set label_bank_cash = 'CASH'%>
				%else:
					<%set label_bank_cash = 'BANK'%>
				%endif
				
				<tr>
					<td height="1px" width="20%" >PAYMENT USING</td>
					<td >: ${label_bank_cash}</td>
					<td ></td>
				</tr>
				<tr>
					<td width="20%" >${label_bank_cash}</td>
					<td >: ${o.journal_id.name}</td>
					<td >
						
					</td>
				</tr>
				<tr>
					<td >DATE</td>
					<td >: ${time.strftime('%d/%m/%Y', time.strptime( o.date,'%Y-%m-%d'))}</td>
					<td >
						
					</td>
				</tr>
				<tr>
					<td >AMOUNT</td>
					<td >: ${o.company_id.currency_id.symbol} ${formatLang(o.amount) or formatLang(0)}</td>
					<td >
						
					</td>
				</tr>
				<tr>
					<td ></td>
					<td ></td>
					<td >
						<br/>
					</td>
				</tr>
			
			</table>
			<table cellpadding="2px"  width="100%" class="font12px one" border="0">
				<tr>
					<td width="20" class="hmid">RECEIVED BY :</td>
					<td width="20"></td>
					<td width="20" class="hmid">CHECKED BY :</td>
					<td width="20"></td>
					<td width="20" class="hmid">REQUEST BY :</td>
				</tr>
				<tr>
					<td>
						<br/>
						<br/>
						<br/>
						<br/>
						
					</td>
				</tr>
				<tr>
					<td class="border_bottom"></td>
					<td></td>
					<td class="border_bottom"></td>
					<td></td>
					<td class="border_bottom"></td>
				</tr>
				<tr>
					<td>&nbsp;</td>
				</tr>
			</table>
				</td>
				<td></td>
			</tr>
			</table>
		%else :
			<table class="list_table1" width="100%" cellpadding="2px" border="0">
			<tr>
				<td></td>
				<td>
			<table cellspacing="0" cellpadding="1px" width="100%" class="font12px" border="0">
		 		<tr>
		 			<td rowspan="3" width="10%"><span style="tadv-align:right;font-size:24">${helper.embed_company_logo(width=100, height=40)|safe}</span></td>
		 			<td width="70%" style="font-size:16px;">${o.company_id.name}</td>
		 			<td width="20%" style="font-size:11px;color:white;">Form No. : ${o.name or ''}</td>
		 		</tr>
		 		<tr>
		 			<td style="font-size:12px;">${o.create_uid.name}</td>
		 			<td rowspan="2" style="font-size:30px;text-align:center"><b>KUITANSI</b></td>
		 		</tr>
		 		<tr>
		 			<td>&nbsp;</td>
		 		</tr>
		 	</table>
			<table width="100%" class="font10px one" cellpadding="2px" border="0">
				<tr>
					<td colspan="3" class="font14px"><b>RECEIVE VOUCHER (${o.number})</b></td>
					<td>&nbsp;</td>
				</tr>
				<tr>
					<td  width="20%">RECEIVE FROM</td>
					<td>: ${o.partner_id.name}</td>
					<td  width="10%">NO.</td>
					<td>: ${o.payment_voucher_order_number}</td>
				</tr>
				<tr>
					<td width="20%">AMOUNT</td>
					%if o.amount > 0
					<td>: ${o.company_id.currency_id.symbol} ${formatLang(o.amount) or formatLang(0)}</td>
					%else
					<td>: ${o.company_id.currency_id.symbol} ${formatLang(o.amount) or formatLang(0)}</td>
					%endif
					<td>DATE</td>
					<td>: ${time.strftime('%d/%m/%Y', time.strptime( o.date,'%Y-%m-%d'))}</td>
				</tr>
				
			</table>
			<table  cellpadding="2px" width="100%" class="font10px one" border="0">
				<tr bgcolor="#d3d3d3">
					<th width="20%" padding-top="1px" class="border_top_bottom border_left_right hmid">ACCOUNT CODE</th>
					<th width="50%" padding-top="1px" class="border_top_bottom border_left_right hmid">PARTICULAR</th>
					<th width="30%" padding-top="1px" class="border_top_bottom border_left_right hmid">AMOUNT</th>
				</tr>
				%for x in o.line_cr_ids :
					%if x.amount > 0.0:
						<tr>
							<td width="20%" class=" border_left_right hmid">${x.account_id.code}</td>
							<td width="50%" class=" border_left_right hleft">${x.move_line_id.invoice and x.move_line_id.invoice.invoice_line[0].name or x.move_line_id.ref or ''}</td>
							<td width="30%" class=" border_left_right hright">${o.company_id.currency_id.symbol} ${formatLang(x.amount) or ''}</td>
						</tr>
					%endif
				%endfor
				
				%for y in o.line_dr_ids :
					%if y.amount > 0.0:
						<tr>
							<td width="20%" class=" border_left_right hmid">${y.account_id.code}</td>
							<td width="50%" class=" border_left_right hleft">${y.move_line_id.invoice and y.move_line_id.invoice.invoice_line[0].name or y.move_line_id.name or ''}</td>
							<td width="30%" class=" border_left_right hright">${o.company_id.currency_id.symbol} ${formatLang(y.amount*-1) or ''}</td>
						</tr>
					%endif
				%endfor
				
				<tr>
					<td height="10px" class=" border_left_right hmid">&nbsp;</td>
					<td class=" border_left_right hmid">&nbsp;</td>
					<td class=" border_left_right hright">&nbsp;</td>
				</tr>
				<tr>
					<td width="20%" class="border_bottom border_left_right hmid"></td>
					<td width="50%" class="border_bottom border_left_right hright"><b>TOTAL</b></td>
					<td width="30%" class="border_bottom border_left_right hright"><b>${o.company_id.currency_id.symbol} ${formatLang(o.amount) or formatLang(0)}</b></td>
				</tr>
				<tr>
					<td ></td>
					<td ></td>
					<td >
						<br/>
						
					</td>
				</tr>
				
				%if o.journal_id.type == 'cash':
					<%set label_bank_cash = 'CASH'%>
				%else:
					<%set label_bank_cash = 'BANK'%>
				%endif
				
				<tr>
					<td height="1px" width="20%" >PAYMENT USING</td>
					<td >: ${label_bank_cash}</td>
					<td ></td>
				</tr>
				<tr>
					<td >DATE</td>
					<td >: ${time.strftime('%d/%m/%Y', time.strptime( o.date,'%Y-%m-%d'))}</td>
					<td >
						
					</td>
				</tr>
				<tr>
					<td >IN WORDS</td>
					<td >: ${convert(o.amount,o.currency_id.name)}</td>
					<td >
						
					</td>
				</tr>
				<tr>
					<td ></td>
					<td ></td>
					<td >
						<br/>
					</td>
				</tr>
			
			</table>
			<table cellpadding="2px"  width="100%" class="font12px one" border="0">
				<tr>
					<td width="20" class="hmid">RECEIVED BY :</td>
					<td width="20"></td>
					<td width="20" class="hmid">CHECKED BY :</td>
					
					
				</tr>
				<tr>
					<td>
						<br/>
						<br/>
						<br/>
						<br/>
						
					</td>
				</tr>
				<tr>
					<td class="border_bottom"></td>
					<td></td>
					<td class="border_bottom"></td>
					
					
				</tr>
				<tr>
					<td>&nbsp;</td>
				</tr>
			</table>
				</td>
				<td></td>
			</tr>
			</table>
		
		
		%endif
	
	%endfor
	
	
	
</body>
</html>