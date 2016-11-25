<html>
	<head>
		<style>
			
			body {
			font-family:helvetica;
			font-size:12px;
			
			}
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
				padding-top: 5px;
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
			thead { display: table-header-group }
			tfoot { display: table-row-group }
			tr { page-break-inside: avoid }
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
				font-family:helvetica;
			}
			.font8px
			{
				font-size: 8px;
				font-family:helvetica;
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
	</head>
	% for o in objects:
	<body style="border:0; margin: 0;" onload="subst()">
	
        <table width="100%" class="one font12px" cellpading="3">
        	
        	%if o.state == 'draft'
			<tr>
				<td colspan="2" class="font22px hmid" width="100%"><u>DRAFT SURAT PENAWARAN</u></td>
			</tr>
			%elif o.state == 'cancel'
			<tr>
				<td colspan="2" class="font22px hmid" width="100%"><u>SURAT PENAWARAN</u></td>
			</tr>
			%elif o.state == 'quot_approval'
			<tr>
				<td colspan="2" class="font22px hmid" width="100%"><u>DRAFT SURAT PENAWARAN (To Confirm) </u></td>
			</tr>
			%elif o.state == 'quot'
			<tr>
				<td colspan="2" class="font22px hmid" width="100%"><u>SURAT PENAWARAN</u></td>
			</tr>
			%elif o.state == 'sent'
			<tr>
				<td colspan="2" class="font22px hmid" width="100%"><u>SURAT PENAWARAN</u></td>
			</tr>
			%else
			<tr>
				<td colspan="2" class="font22px hmid" width="100%"><u>SALES ORDER</u></td>
			</tr>
			%endif
			<tr>
				<td colspan="2"class="hmid" width="100%">Nomor : ${o.name}</td>
			</tr>
			<tr>
				<td colspan="2"><br/></td>
				
			</tr>
			<tr>
				<td colspan="2" class="hleft" width="100%">Jakarta, ${time.strftime('%d %b %Y', time.strptime( o.date_order,'%Y-%m-%d %H:%M:%S'))}</td>
			</tr>
			<tr>
				<td width="11%" class="hleft">Kepada Yth :</td>
			</tr>
			<tr>
				<td></td>
				<td class=""><b>${o.partner_id.name}<b/></td>
			</tr>
			<tr>
				<td></td>
				<td class="">${o.partner_id.street}</td>
				
			</tr>
			<tr>
				<td></td>
				<td class="">${o.partner_id.street2 or ''}</td>
				
			</tr>
			<tr>
				<td></td>
				<td class="">${o.partner_id.state or ''} ${o.partner_id.city or ''} ${o.partner_id.country_id.name or ''}</td>
				
			</tr>
			<tr>
				<td>UP: </td>
				<td class=""><b>${o.contact or ''}</b></td>
				
			</tr>
			<tr>
				<td>CC: </td>
				<td class=""><b>${o.contact2 or ''}</b></td>
				
			</tr>
			<tr>
				<td><br/></td>
				
			</tr>
			<tr>
				<td  colspan="2" class="perjanjian">Dengan Hormat,</td>
			</tr>
			<tr>
				<td><br/></td>
				
			</tr>
			<tr>
				<td   colspan="2" class="perjanjian">Kami dari PT Persada Medika Solusindo selaku Sole Agent
				dan Distributor Alat Kesehatan, dengan ini bermaksud mengajukan surat penawaran harga untuk product sebagai berikut :</td>
			</tr>
			
        </table>
        <br/>
		
		<table width="100%" class="one font10px" cellpading="3">
			<tr>
				<th class="border_bottom hleft font10px" colspan="7">Details</th>
			</tr>
			<tr>
				<th width="3%" rowspan="1" class="hmid">No.</th>
				<th width="30%" rowspan="1"  colspan="1" class="hleft">Produk </th>
				<th width="15%" rowspan="1" class="hleft">Merk/Tipe/Negara Asal</th>
				<th width="10%" rowspan="1" class="hmid">Qty</th>
				<th width="15%" colspan="1">Harga Satuan</th>
				<th width="10%" rowspan="1">PPN 10%</th>
				<th width="20%" rowspan="1">Harga Nett</th>
				
			</tr>
			<!-- <tr>
				<th width="8%" class="hmid" >Satuan</th>
				<th width="8%" class="hmid" >Disc (%)</th>
				
				
			</tr> -->
			
			<% set i=0 %>
			<% set n=0 %>
			<% set y=0 %>
			%if o.paket == 'reg' :
				%for line in o.order_line:
					<% set y=y+1 %>
						<tr style="page-break-inside:avoid; page-break-after:auto; ">	
							<td class="vtop font10px" width="3%">${y}</td>
							<td class="vtop paddingtop font10px" colspan="1" width="35%">${line.product_id.name or ''}<br/>
																		${line.product_id.description|safe or ''}
							</td>
							
							<td class=" vtop paddingtop font10px" width="15%">Merek   : ${line.product_id.product_brand_id.name or ''}</br>
											Model   : ${line.product_id.default_code}</br>
											Origin : ${line.product_id.product_country.name or ''}
							</td>
							<td class="vtop hmid paddingtop font10px" width="10%">${line.product_uom_qty} ${line.product_uom.name}</td>
							<td class=" vtop hright paddingtop font10px" width="15%">${formatLang(line.price_unit) or formatLang('0')}</td>
							<!-- <td class="vtop hmid paddingtop font10px" width="6%">${line.discount or 0.0}</td> -->
							
							%if line.tax_id :
								<td class="vtop hmid paddingtop font10px" width="10%">${formatLang((line.price_unit*(1-(line.discount/100)))*0.10) or formatLang(0)}</td>

								<td  class="vtop hright paddingtop font10px" width="20%">${formatLang((line.price_subtotal)+((line.price_unit*(1-(line.discount/100)))*0.10)) or formatLang('0')}</td>
							%else :
									<td class="vtop hmid paddingtop font10px" width="10%"></td>
									<td  class="vtop hright paddingtop font10px" width="20%">${formatLang(line.price_subtotal) or formatLang('0')}</td>
							%endif
						</tr>
					
				%endfor
			%else :
			
				%for line in o.order_line:
				
				%if line.main_unit :
				<% set n=n+1%>
				<tr style="page-break-inside:avoid; page-break-after:auto; ">
					
					<td class="vtop font10px" width="5%"> Paket ${n}</td>
					
					<td class="vtop paddingtop font10px" colspan="2" width="47%">${line.product_id.name or ''}<br/>
																${line.product_id.description|safe or ''}
					</td>
					
					<td class=" vtop paddingtop font10px" width="15%">Merek   : ${line.product_id.product_brand_id.name or ''}</br>
									Model   : ${line.product_id.default_code}</br>
									Origin : ${line.product_id.product_country.name or ''}
					</td>
					<td class="vtop hmid paddingtop font10px" width="10%">${line.product_uom_qty} ${line.product_uom.name}</td>
					<td class=" vtop hright paddingtop font10px" width="7%">${formatLang(line.price_unit) or formatLang('0')}</td>
					<!-- <td class="vtop hmid paddingtop font10px" width="5%">${line.discount or 0.0}</td> -->
					
					%if line.tax_id :
							<td class="vtop hmid paddingtop font10px" width="10%">${formatLang((line.price_unit*(1-(line.discount/100)))*0.10) or formatLang(0)}</td>
							<td  class="vtop hright paddingtop font10px" width="15%">${formatLang((line.price_subtotal)+((line.price_unit*(1-(line.discount/100)))*0.10)) or formatLang('0')}</td>
					%else :
							<td class="vtop hmid paddingtop font10px" width="10%"></td>
							<td  class="vtop hright paddingtop font10px" width="15%">${formatLang(line.price_subtotal) or formatLang('0')}</td>
					%endif
				</tr>
				%else:
				<tr style="page-break-inside:avoid; page-break-after:auto; ">
					
					<td class="vtop font10px" width="5%"></td>
					<td class="vtop paddingtop font10px" colspan="2" width="47%">${line.product_id.name or ''}<br/>
																${line.product_id.description|safe or ''}
					</td>
					
					<td class=" vtop paddingtop font10px" width="15%">Merek   : ${line.product_id.product_brand_id.name or ''}</br>
									Model   : ${line.product_id.default_code}</br>
									Origin : ${line.product_id.product_country.name or ''}
					</td>
					<td class="vtop hmid paddingtop font10px" width="10%">${line.product_uom_qty} ${line.product_uom.name}</td>
					<td class=" vtop hright paddingtop font10px" width="7%">${formatLang(line.price_unit) or formatLang('0')}</td>
					<!-- <td class="vtop hmid paddingtop font10px" width="8%">${line.discount or 0.0}</td>
					 -->
					%if line.tax_id :
							<td class="vtop hmid paddingtop font10px" width="10%">${formatLang((line.price_unit*(1-(line.discount/100)))*0.10) or formatLang(0)}</td>
							<td  class="vtop hright paddingtop font10px" width="15%">${formatLang((line.price_subtotal)+((line.price_unit*(1-(line.discount/100)))*0.10)) or formatLang('0')}</td>
					%else :
							<td class="vtop hmid paddingtop font10px" width="10%"></td>
							<td  class="vtop hright paddingtop font10px" width="15%">${formatLang(line.price_subtotal) or formatLang('0')}</td>
					%endif
					
				</tr>
				%endif
				%endfor
			%endif
			<tr>
				<td colspan="8" class="border_top">
				</td>
			</tr>
			</table>
			<table width="100%" class="one font12px" cellpading="10px" style="page-break-inside:avoid; page-break-after:auto; padding:5px">
			<tr style="page-break-inside:avoid; page-break-after:auto; ">
				<td width="56%"></td>
				<td style="padding-top:5px" width="20%" class="hright">Total :</td>
				<td style="padding-top:5px" width="13%" class="hright">${formatLang(o.gross_total)}</td>
			</tr>
			<tr>
				<td ></td>
				<td  style="padding-top:5px" class="hright">Discount :</td>
				<td style="padding-top:5px" class="hright"> ${formatLang(o.discount_total-o.order_line|sum(attribute='disc_amount'))}</td>
			</tr>
			<tr>
				<td ></td>
				<td style="padding-top:5px"  class="hright">Disc. Tambahan :</td>
				<td style="padding-top:5px" class="hright"> ${formatLang(o.order_line|sum(attribute='disc_amount'))}</td>
			</tr>
			<tr>
				<td ></td>
				<td style="padding-top:5px" class="hright">Gross Total :</td>
				<td style="padding-top:5px" class="hright border_top">${formatLang(o.amount_untaxed) or formatLang('0')}</td>
			</tr>
			<tr>
				<td ></td>
				<td style="padding-top:5px" class="hright">PPN 10% :</td>
				<td style="padding-top:5px"  class="hright">${formatLang(o.amount_tax) or formatLang('0')}</td>
			</tr>
			<tr>
				<td ></td>
				<td style="padding-top:5px"  class="hright border_top">Net Total :</td>
				<td style="padding-top:5px"  class="hright border_top">${formatLang(o.amount_total) or formatLang('0')}</td>
			</tr>
			
		</table>
		
		<table width="100%" class="content one font11px" cellpading="3px" style="page-break-inside:avoid; page-break-after:auto;">
			<tr >
				<td class="hleft"><b>Kondisi penawaran : </b></td> 
			</tr>
			<tr>
				<td class="font11px" style="color: solid black"> ${o.ketentuan|safe or '-'}
				</td>
			</tr>
		</table>
		<table class="content" width="100%" style="page-break-inside:avoid; ">
		<tr >
				<td class="content padding"></br></td>
			</tr>	
			<tr>
				<td class="perjanjian">Demikian Surat Penawaran ini kami buat. Atas perhatian dan kerjasamanya kami ucapkan terima kasih.</td>
			</tr>
			<tr>
				<td class="perjanjian">Hormat Kami,</td>
			</tr>
			<tr>
				<td class="perjanjian">${helper.embed_image('png',o.user_id.signature_pic,175,100)|safe}</td>
			</tr>
			<tr>
				<td class="perjanjian">${o.user_id.name}</td>
			</tr>
			
		</table>
		<p class="content">
			Jika penawaran ini disetujui, silahkan isi form dibawah ini dan kembalikan ke ${o.company_id.name or '-'} melalui FAX ${o.company_id.fax or '-'} atau email ke sales@persameds.com.
		</p>
		
		<table style="page-break-inside:avoid; " class="content" border="0px" cellspacing="0px" width="100%">
			<tr >
				<td class="content padding"></br></td>
			</tr>
			<tr >
				<td class="content padding"><b>Form Konfirmasi Order</b></td>
			</tr>
			<tr>
				<td class="content padding">
					Dengan ditandatanganinya form ini, kami menyetujui penawaran yang diajukan <br/><br/>
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
		
		
    % endfor
	
	</body>
</html>