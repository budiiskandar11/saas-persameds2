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
		
			<table class="list_table1" width="100%" cellpadding="2px" border="0">
			<tr>
				<td></td>
				<td>
			<table cellspacing="0" cellpadding="1px" width="100%" class="font12px" border="0">
		 		<tr>
		 			<td rowspan="2" width="10%" style="padding-right:5px"><span style="tadv-align:right;font-size:24; padding-right: 5px">${helper.embed_company_logo(width=100, height=40)|safe}</span></td>
		 			<td  rowspan="2" width="70%" style="font-size:12px;">
		 				<b>${o.company_id.name} </b><br/>
		 				${o.company_id.street or ''} ${o.company_id.street2 or ''}  ${o.company_id.city or ''}
										 ${o.company_id.state or ''}  ${o.company_id.country or ''}  ${o.company_id.zip or ''}<br/>
						Phone : ${o.company_id.phone or ''}


		 			</td>
		 			<td width="20%" style="font-size:24px;">KUITANSI</td>
		 		</tr>
		 		<!-- <tr>
		 			<td style="font-size:12px;">${o.create_uid.name}</td>
		 			<td rowspan="2" style="font-size:30px;text-align:center"><b>KUITANSI</b></td>
		 		</tr> -->
		 		<tr>
		 			<td class="font10px"><b>NOMOR : ${o.number}</b></td>
					
		 		</tr>
		 	</table>
		 	<br/> <br/>
			<table width="100%" class="font12px one" cellpadding="2px" border="0">
				
				<tr>
					<td  width="30%">SUDAH DITERIMA DARI</td>
					<td width="2%">:</td>
					<td  style="border-bottom: dotted 1px black"><b>${o.partner_id.name}</b></td>

					<!-- <td  width="10%">NO.</td>
					<td style="border-bottom: dotted 1px black">: ${o.payment_voucher_order_number}</td> -->
				</tr>
				<tr>
					<td >TERBILANG</td>
					<td width="2%">:</td>
					<td style="border-bottom: dotted 1px black">${convert(o.amount,o.currency_id.name)|title}</td>
					
				</tr>
				
				
				<tr>
					<td >UNTUK PEMBAYARAN</td>
					<td width="2%">:</td>
					<td style="border-bottom: dotted 1px black">${o.name or 'Pembelian barang'}</td>
					
				</tr>
				<tr>
					<td ></td>
					<td width="2%">:</td>
					<td style="border-bottom: dotted 1px black"></td>
					
				</tr>
				<tr>
					<td ></td>
					<td width="2%">:</td>
					<td style="border-bottom: dotted 1px black"></td>
					
				</tr>
			</table>
			<br/>
			<table cellpadding="2px"  width="100%" class="font12px one" border="0">
				<tr>
					
					%if o.amount > 0
					<td width="30%" rowspan="2" class="hmid" style="border:1px solid black; padding:5px; font-size:18px;">${o.company_id.currency_id.symbol} ${formatLang(o.amount) or formatLang(0)}</td>
					%else
					<td width="30%" rowspan="2" class="hmid" style="border:1px solid black; padding:5px; font-size:18px;">${o.company_id.currency_id.symbol} ${formatLang(o.amount) or formatLang(0)}</td>
					%endif
					<td  rowspan="2" width="30%"></td>
					<td width="30%" class="hmid" >Jakarta, ${time.strftime('%d %B %Y', time.strptime( o.date,'%Y-%m-%d'))}</td>

				</tr>
				<tr>
					<td class="hmid">Diterima Oleh :</td>
				</tr>
				
			</table>
			
			<table cellpadding="2px"  width="100%" class="font12px one" border="0">
				<tr>
					<td colspan="2" width="30%">Catatan :</td>
					
					<td width="30%" class="hmid"></td>
					<td width="30%" class="hmid"></td>
					
				</tr>
				<tr>
					<td width="2%" class="font10px vtop">1.</td>
					<td colspan="2" width="30%" class="font10px">Mohon pembayaran dilakukan dengan transfer ke rekening bank berikut :<br/>
									<b>Bank Mandiri Cab. Citra Grand Cibubur<br/>
									Rekening : 900-003-080-796-1<br/>
									Atas Nama : Surono</b>
					</td>
					
					<td width="30%" class="hmid"></td>
					
				</tr>
				<tr>
					<td width="2%" class="font10px vtop">2.</td>
					<td colspan="2" width="30%" class="font10px">Pembayaran dianggap sah setelah uang diterima di rekening kami
					</td>
					
					<td width="30%" class="hmid"></td>
					
				</tr>
				<tr>
					<td colspan="3"></td>
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
		
	%endfor
	
	
	
</body>
</html>