<html>
	<head>
		<style>
			
			body {
			font-family:helvetica;
			font-size:12;
			}
			.ht {
			font-family:helvetica;
			font-size:11;
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
	% for o in objects:
	<body onload="subst()">
      
        <table width="100%" class="one font12px" cellpading="5">
        	<tr>
				<td colspan="3">${helper.embed_company_logo(height="60px",width="auto")|safe}</td>
			</tr>
        	<tr>
        		<td>
        			<br/>
        		</td>
        	</tr>
        	
			<tr>
				<td colspan="3" class="font22px hmid" width="100%"><u>CONFIRMATION ORDER</u></td>
			</tr>
			
			<tr>
				<td colspan="3"class="hmid" width="100%">Nomor : ${o.name}</td>
			</tr>
			<tr>
				<td colspan="3"><br/></td>
				
			</tr>
			<tr>
				%if o.conf_date :
				<td colspan="3" class="hleft" width="100%">Jakarta, ${time.strftime('%d %b %Y', time.strptime( o.conf_date,'%Y-%m-%d'))}</td>
				%else : 
				<td colspan="3" class="hleft" width="100%">Jakarta, </td>
				%endif
			</tr>
			<tr>
				<td width="10%" class="hleft">Kepada Yth :</td>
				<td class="hleft"></td>
				<td class="hleft"></td>
			</tr>
			<tr>
				<td width="10%"></td>
				<td width="30%" class="hleft"><b>${o.partner_id.name}<b/></td>
				<td class="hleft"></td>
			</tr>
			<tr>
				<td width="10%"></td>
				<td class="hleft">${o.partner_id.street}</td>
				<td class="hleft"></td>
			</tr>
			<tr>
				<td width="10%"></td>
				<td class="hleft">${o.partner_id.street2 or ''}</td>
				<td class="hleft"></td>
			</tr>
			<tr>
				<td width="10%"></td>
				<td width="30%"class="hleft">${o.partner_id.state or ''} ${o.partner_id.city or ''} ${o.partner_id.country_id.name or ''}</td>
				<td class="hleft"></td>
			</tr>
			<tr>
				<td>Up: </td>
				<td class="hleft"><b>${o.contact or ''}</b></td>
				<td class="hleft"></td>
			</tr>
			<tr>
				<td>Cc: </td>
				<td class="hleft"><b>${o.contact2 or ''}</b></td>
				<td class="hleft"></td>
			</tr>
			<tr>
				<td><br/></td>
				<td class="hleft"></td>
				<td class="hleft"></td>
			</tr>
			<tr>
				<td  colspan="3" class="perjanjian">Dengan Hormat,</td>
			</tr>
			<tr>
				<td><br/></td>
				
			</tr>
			<tr>
				<td   colspan="3" class="perjanjian">Kami dari PT Persada Medika Solusindo selaku Sole Agent
				dan Distributor Alat Kesehatan, dengan ini bermaksud mengajukan surat konfirmasi order, 
				%if o.client_order_ref :
				berdasarkan PO No. <b>${o.client_order_ref or ''}</b>
				%endif
				dengan rincian sebagai berikut :</td>
			</tr>
			
        </table>
        <br/>
		
		<table width="100%" class="one font10px" cellpading="3">
			<tr>
				<th class="border_bottom hleft font10px" colspan="8">Details</th>
			</tr>
			<tr>
				<th width="3%" rowspan="2" class="h">No.</th>
				<th width="10%" rowspan="2" class="hleft">Produk </th>
				<th width="25%" rowspan="2" class="hleft">Deskripsi</th>
				<th width="15%" rowspan="2" class="hleft">Merk/Tipe/Negara Asal</th>
				<th width="10%" rowspan="2" class="hmid">Qty</th>
				<th width="25%" colspan="3">Harga (Rupiah)</th>
				
			</tr>
			<tr>
				<th width="6%" class="hmid" >Satuan</th>
				<th width="8%" class="hmid" >Discount</th>
				<th width="13%" class="hmid">Jumlah</th>
			</tr>
			
			<% set i=0 %>
			%for line in o.order_line:
			<% set i=i+1 %>
			%if line.main_unit == True
			<tr style="page-break-inside:avoid; page-break-after:always; padding-top:10px">
				<td class="font12px" width="3%"><b>${i}</b></td>
				<td class="font12px" width="10%"><b>${line.product_id.name or ''}</b></td>
				<td class="font12px" width="25%"><b>${line.product_id.description or ''}</b></td>
				<td  width="15%"><b>Merek   : ${line.product_id.product_brand_id.name or ''}</br>
								Model   : ${line.product_id.default_code}</br>
								Origin : ${line.product_id.product_country.name or ''}</b>
				</td>
				<td class="hmid font12px" width="10%"><b>${line.product_uom_qty} ${line.product_uom.name}</b></td>
				<td class="hright font12px" width="7%"><b>${formatLang(line.price_unit) or formatLang('0')}</b></td>
				<td class="hmid font12px" width="8%"><b>${line.discount}</b></td>
				<td  class="hright font12px" width="13%"><b>${formatLang(line.price_subtotal) or formatLang('0')}</b></td>
			</tr>
			%else
			<tr style="page-break-inside:avoid; page-break-after:auto; ">
				<td class="paddingtop" width="3%">${i}</td>
				<td class="paddingtop" width="10%">${line.product_id.name or ''}</td>
				<td class="paddingtop" width="25%">${line.product_id.description or ''}</td>
				<td class="paddingtop" width="15%">Merek   : ${line.product_id.product_brand_id.name or ''}</br>
								Model   : ${line.product_id.default_code}</br>
								Origin : ${line.product_id.product_country.name or ''}
				</td>
				<td class="hmid paddingtop" width="10%">${line.product_uom_qty} ${line.product_uom.name}</td>
				<td class="hright paddingtop" width="7%">${formatLang(line.price_unit) or formatLang('0')}</td>
				<td class="hmid paddingtop" width="8%">${line.discount}</td>
				<td  class="hright paddingtop" width="13%">${formatLang(line.price_subtotal) or formatLang('0')}</td>
			</tr>
			%endif 
			%endfor
			<tr>
				<td colspan="9" class="border_top">
				</td>
			</tr>
			<tr>
				<td colspan="5"></td>
				<td colspan="2" class="hright">Total :</td>
				<td class="hright">${formatLang(o.gross_total)}</td>
			</tr>
			<tr>
				<td colspan="5"></td>
				<td colspan="2" class="hright">Discount :</td>
				<td class="hright"> ${formatLang(o.discount_total)}</td>
			</tr>
			<tr>
				<td colspan="5"></td>
				<td colspan="2" class="hright">Gross Total :</td>
				<td class="hright border_top">${formatLang(o.amount_untaxed) or formatLang('0')}</td>
			</tr>
			<tr>
				<td colspan="5"></td>
				<td colspan="2" class="hright">PPN 10% :</td>
				<td class="hright">${formatLang(o.amount_tax) or formatLang('0')}</td>
			</tr>
			<tr>
				<td colspan="5"></td>
				<td colspan="2" class="hright border_top">Net Total :</td>
				<td class="hright border_top">${formatLang(o.amount_total) or formatLang('0')}</td>
			</tr>
			
		</table>
		
		<table class="content" width="100%">
			<tr >
				<td class="hleft"><b>Keterangan : </b></td> 
			</tr>
			<tr>
				<td class="ht" style="color: solid black"> ${o.ketentuan|safe or '-'}
				</td>
			</tr>
		</table>
		<table class="content" width="100%" style="page-break-inside:avoid; ">
		<tr >
				<td class="content padding"></br></td>
			</tr>	
			<tr>
				<td colspan="2" class="perjanjian">Demikian Surat Konfirmasi order ini kami buat. Atas perhatian dan kerjasamanya kami ucapkan terima kasih.</td>
			</tr>
			<tr >
				<td class="content padding"></br></td>
			</tr>
			
			<tr>
				<td width="50%" class="perjanjian">Hormat Kami,</td>
				<td width="50%" class="perjanjian">Menyetujui,</td>
			</tr>
			<tr>
				<td width="50%"  class="perjanjian">${o.company_id.name|upper}</td>
				<td width="50%" class="perjanjian">${o.partner_id.name|upper}</td>
			</tr>
			<tr>
				<td class="perjanjian">${helper.embed_image('png',o.user_id.signature_pic,175,100)|safe}</td>
				<td class="perjanjian"></td>
			</tr>
			<tr>
				<td class="perjanjian">${o.user_id.name}</td>
				<td class="perjanjian">${o.contact or ''}</td>
			</tr>
			
		</table>
		
		
		
    % endfor
	
	</body>
	
	</body>
</html>