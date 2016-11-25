<html>
	<head>
		<style>
			
			body {
			font-family:helvetica;
			font-size:12px;
			padding: 5px;
			
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
			.border_bottom_dot
			{
				border-bottom: dotted 1px;
			}
			.border_right
			{
				border-right: 1px solid black;
			}
			
			.border_left
			{
				border-left: 1px solid black;
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
			.kotak {
				border-right: 1px solid black;
				border-left: 1px solid black;
				border-top: 1px solid black;
				border-bottom: 1px solid black;
				padding-top:5px; 
				padding-bottom:5px;
				padding-left:2px;
			}
			
			
         	table.one 
         	{border-collapse:collapse;}
			
		</style>
	</head>
	% for o in objects:
	<body style="border:0; margin: 0;" onload="subst()">
	
	      
        <table width="100%" class="one font10px" cellpadding="2px">
        	<tr>
        		<td colspan="4" class="font22px hmid" ><b>KARTU GARANSI* / <i>WARRANTY CARD</i></b></td>
        	</tr>
        	<tr>
        		<td colspan="2" class="font14px" >NOMOR KARTU GARANSI : <b>${o.warranty_no}</b></td>
        		<td  colspan="2" height="10px"><img src="data:image/png;base64,{${ o.war_barcode }}"/></td>
        	</tr>
        	<tr>
        		<td class="border_left_right border_top" colspan="2"><b>INFORMASI PRODUK</b></td>
        		<td class="border_left border_top"></td>
        		<td class="border_right border_top"></td>
        	</tr>
        	<tr>
        		<td class="border_left" width="20%">NAMA PRODUK</td>
        		<td class="border_right border_bottom_dot" width="30%">${o.product_id.name or ''}</td>
        		<td class="border_left" width="27%">NOMOR SERI</td>
        		<td class="border_right border_bottom_dot" width="23%">${o.lot_number.name or ''}</td>
        	</tr>
        	<tr>
        		<td class="border_left">MEREK/TIPE</td>
        		<td class="border_right border_bottom_dot">${o.brand_id.name or ''}/${o.default_code or ''}</td>
        		<td class="border_left">TANGGAL INSTALASI</td>
        		<td class="border_right border_bottom_dot">${time.strftime('%d %B %Y', time.strptime( o.date_install,'%Y-%m-%d %H:%M:%S'))}</td>
        	</tr>
        	<tr>
        		<td class="border_left">PABRIK</td>
        		<td class="border_right border_bottom_dot">${o.man_country.name}</td>
        		<td class="border_left"></td>
        		<td class="border_right"></td>
        	</tr>
        	<tr>
        		<td class="border_left">NEGARA ASAL</td>
        		<td class="border_right border_bottom_dot">${o.man_country.name}</td>
        		<td class="border_left">BERLAKU SD</td>
        		<td class="border_right">${time.strftime('%d %B %Y', time.strptime( o.date_finish,'%Y-%m-%d %H:%M:%S'))}</td>
        	</tr>
        	<tr>
        		<td class="border_left_right border_top" colspan="2"><b>INFORMASI PELANGGAN</b></td>
        		<td class="border_left_right border_top_bottom hmid"><b>SOLE AGENT</b></td>
        		<td class="border_left_right border_top_bottom hmid"><b>CAP/STEMPEL SOLE AGENT</b></td>
        	</tr>
        	<tr>
        		<td class="border_left">NAMA CUSTOMER</td>
        		%if o.customer_id.parent_id :
        		<td class="border_right border_bottom_dot">${o.customer_id.parent_id.name or ''}-${o.customer_id.name or ''}</td>
        		%else :
        		<td class="border_right border_bottom_dot">${o.customer_id.name or ''}</td>
        		%endif
        		<td class="border_left_right">PT PERSADA MEDIKA SOLUSINDO</td>
        		<td class="border_left_right"></td>
        	</tr>
        	<tr>
        		<td class="border_left">NO CUSTOMER</td>
        		<td class="border_right border_bottom_dot">${o.customer_id.parent_id.code or o.customer_id.code or ''} </td>
        		<td class="border_left_right border_bottom" rowspan="4">${o.company_id.street or ''} ${o.company_id.street2 or ''}<br/>
        													${o.company_id.city or ''} ${o.company_id.state_id.name or ''} ${o.company_id.zip or ''}<br/>
        													Phone/Fax : ${o.company_id.phone or ''}<br/>
        													website : ${o.company_id.website or ''}
        		</td>
        		<td class="border_left_right"></td>
        	</tr>
        	<tr>
        		<td class="border_left">ALAMAT</td>
        		<td class="border_right">${o.customer_id.street or ''} ${o.customer_id.street2 or ''} </td>
        		
        		<td class="border_left_right"></td>
        	</tr>
        	<tr>
        		<td class="border_left"></td>
        		<td class="border_right border_bottom_dot">${o.customer_id.city or ''} ${o.customer_id.state_id.name or ''} ${o.customer_id.zip or ''}</td>
        		
        		<td class="border_left_right"></td>
        	</tr>
        	<tr>
        		<td class="border_left border_bottom">NO TELP</td>
        		<td class="border_right border_bottom">${o.phone1 or ''}</td>
        		
        		<td class="border_left_right border_bottom"></td>
        	</tr>
        	<tr>
				<td colspan="3" hleft" width="100%"  style="padding-top:3px; padding-bottom:10px;">
				<b><i>*Garansi diberikan 1 tahun sesuai dengan aturan garansi pabrik</b></i>
				</td>
			</tr>
        	
		</table>
		<table width="100%" class="one font10px" cellpadding="1px">
			<tr>
				<td class="border_bottom_dot"><i>untuk pelanggan</i></td>
			</tr>
			<tr>
				<td><i>untuk penjual</i></td>
			</tr>
		</table>
		<table width="100%" class="one font10px" cellpadding="2px">
        	<tr>
        		<td colspan="4" class="font22px hmid" ><b>KARTU GARANSI* / <i>WARRANTY CARD</i></b></td>
        	</tr>
        	<tr>
        		<td colspan="2" class="font14px" >NOMOR KARTU GARANSI : <b>${o.warranty_no}</b></td>
        		<td  colspan="2" height="10px"><img src="data:image/png;base64,{${ o.war_barcode }}"/></td>
        	</tr>
        	<tr>
        		<td class="border_left_right border_top" colspan="2"><b>INFORMASI PRODUK</b></td>
        		<td class="border_left border_top"></td>
        		<td class="border_right border_top"></td>
        	</tr>
        	<tr>
        		<td class="border_left" width="20%">NAMA PRODUK</td>
        		<td class="border_right border_bottom_dot" width="30%">${o.product_id.name or ''}</td>
        		<td class="border_left" width="27%">NOMOR SERI</td>
        		<td class="border_right border_bottom_dot" width="23%">${o.lot_number.name or ''}</td>
        	</tr>
        	<tr>
        		<td class="border_left">MEREK/TIPE</td>
        		<td class="border_right border_bottom_dot">${o.brand_id.name or ''}/${o.default_code or ''}</td>
        		<td class="border_left">TANGGAL INSTALASI</td>
        		<td class="border_right border_bottom_dot">${time.strftime('%d %B %Y', time.strptime( o.date_install,'%Y-%m-%d %H:%M:%S'))}</td>
        	</tr>
        	<tr>
        		<td class="border_left">PABRIK</td>
        		<td class="border_right border_bottom_dot">${o.man_country.name}</td>
        		<td class="border_left"></td>
        		<td class="border_right"></td>
        	</tr>
        	<tr>
        		<td class="border_left">NEGARA ASAL</td>
        		<td class="border_right border_bottom_dot">${o.man_country.name}</td>
        		<td class="border_left">BERLAKU SD</td>
        		<td class="border_right">${time.strftime('%d %B %Y', time.strptime( o.date_finish,'%Y-%m-%d %H:%M:%S'))}</td>
        	</tr>
        	<tr>
        		<td class="border_left_right border_top" colspan="2"><b>INFORMASI PELANGGAN</b></td>
        		<td class="border_left_right border_top_bottom hmid"><b>SOLE AGENT</b></td>
        		<td class="border_left_right border_top_bottom hmid"><b>CAP/STEMPEL SOLE AGENT</b></td>
        	</tr>
        	<tr>
        		<td class="border_left">NAMA CUSTOMER</td>
        		%if o.customer_id.parent_id :
        		<td class="border_right border_bottom_dot">${o.customer_id.parent_id.name or ''}-${o.customer_id.name or ''}</td>
        		%else :
        		<td class="border_right border_bottom_dot">${o.customer_id.name or ''}</td>
        		%endif
        		<td class="border_left_right">PT PERSADA MEDIKA SOLUSINDO</td>
        		<td class="border_left_right"></td>
        	</tr>
        	<tr>
        		<td class="border_left">NO CUSTOMER</td>
        		<td class="border_right border_bottom_dot">${o.customer_id.parent_id.code or o.customer_id.code or ''} </td>
        		<td class="border_left_right border_bottom" rowspan="4">${o.company_id.street or ''} ${o.company_id.street2 or ''}<br/>
        													${o.company_id.city or ''} ${o.company_id.state_id.name or ''} ${o.company_id.zip or ''}<br/>
        													Phone/Fax : ${o.company_id.phone or ''}<br/>
        													website : ${o.company_id.website or ''}
        		</td>
        		<td class="border_left_right"></td>
        	</tr>
        	<tr>
        		<td class="border_left">ALAMAT</td>
        		<td class="border_right">${o.customer_id.street or ''} ${o.customer_id.street2 or ''} </td>
        		
        		<td class="border_left_right"></td>
        	</tr>
        	<tr>
        		<td class="border_left"></td>
        		<td class="border_right border_bottom_dot">${o.customer_id.city or ''} ${o.customer_id.state_id.name or ''} ${o.customer_id.zip or ''}</td>
        		
        		<td class="border_left_right"></td>
        	</tr>
        	<tr>
        		<td class="border_left border_bottom">NO TELP</td>
        		<td class="border_right border_bottom">${o.phone1 or ''}</td>
        		
        		<td class="border_left_right border_bottom"></td>
        	</tr>
        	<tr>
				<td colspan="3" hleft" width="100%"  style="padding-top:3px; padding-bottom:10px;">
				<b><i>*Garansi diberikan 1 tahun sesuai dengan aturan garansi pabrik</b></i>
				</td>
			</tr>
        	
		</table>
		%if o.partner_id:
		<table width="100%" class="one font10px" cellpadding="1px">
			<tr>
				<td class="border_bottom_dot"></td>
			</tr>
			<tr>
				<td><i>untuk pengguna</i></td>
			</tr>
		</table>
		<table width="100%" class="one font10px" cellpadding="2px">
        	<tr>
        		<td colspan="4" class="font22px hmid" ><b>KARTU GARANSI* / <i>WARRANTY CARD</i></b></td>
        	</tr>
        	<tr>
        		<td colspan="2" class="font14px" >NOMOR KARTU GARANSI : <b>${o.warranty_no}</b></td>
        		<td  colspan="2" height="10px"><img src="data:image/png;base64,{${ o.war_barcode }}"/></td>
        	</tr>
        	<tr>
        		<td class="border_left_right border_top" colspan="2"><b>INFORMASI PRODUK</b></td>
        		<td class="border_left border_top"></td>
        		<td class="border_right border_top"></td>
        	</tr>
        	<tr>
        		<td class="border_left" width="20%">NAMA PRODUK</td>
        		<td class="border_right border_bottom_dot" width="30%">${o.product_id.name or ''}</td>
        		<td class="border_left" width="27%">NOMOR SERI</td>
        		<td class="border_right border_bottom_dot" width="23%">${o.lot_number.name or ''}</td>
        	</tr>
        	<tr>
        		<td class="border_left">MEREK/TIPE</td>
        		<td class="border_right border_bottom_dot">${o.brand_id.name or ''}/${o.default_code or ''}</td>
        		<td class="border_left">TANGGAL INSTALASI</td>
        		<td class="border_right border_bottom_dot">${time.strftime('%d %B %Y', time.strptime( o.date_install,'%Y-%m-%d %H:%M:%S'))}</td>
        	</tr>
        	<tr>
        		<td class="border_left">PABRIK</td>
        		<td class="border_right border_bottom_dot">${o.man_country.name}</td>
        		<td class="border_left"></td>
        		<td class="border_right"></td>
        	</tr>
        	<tr>
        		<td class="border_left">NEGARA ASAL</td>
        		<td class="border_right border_bottom_dot">${o.man_country.name}</td>
        		<td class="border_left">BERLAKU SD</td>
        		<td class="border_right">${time.strftime('%d %B %Y', time.strptime( o.date_finish,'%Y-%m-%d %H:%M:%S'))}</td>
        	</tr>
        	<tr>
        		<td class="border_left_right border_top" colspan="2"><b>INFORMASI PELANGGAN</b></td>
        		<td class="border_left_right border_top_bottom hmid"><b>SOLE AGENT</b></td>
        		<td class="border_left_right border_top_bottom hmid"><b>CAP/STEMPEL SOLE AGENT</b></td>
        	</tr>
        	<tr>
        		<td class="border_left">NAMA CUSTOMER</td>
        		%if o.customer_id.parent_id :
        		<td class="border_right border_bottom_dot">${o.customer_id.parent_id.name or ''}-${o.customer_id.name or ''}</td>
        		%else :
        		<td class="border_right border_bottom_dot">${o.customer_id.name or ''}</td>
        		%endif
        		<td class="border_left_right">PT PERSADA MEDIKA SOLUSINDO</td>
        		<td class="border_left_right"></td>
        	</tr>
        	<tr>
        		<td class="border_left">NO CUSTOMER</td>
        		<td class="border_right border_bottom_dot">${o.customer_id.parent_id.code or o.customer_id.code or ''} </td>
        		<td class="border_left_right border_bottom" rowspan="4">${o.company_id.street or ''} ${o.company_id.street2 or ''}<br/>
        													${o.company_id.city or ''} ${o.company_id.state_id.name or ''} ${o.company_id.zip or ''}<br/>
        													Phone/Fax : ${o.company_id.phone or ''}<br/>
        													website : ${o.company_id.website or ''}
        		</td>
        		<td class="border_left_right"></td>
        	</tr>
        	<tr>
        		<td class="border_left">ALAMAT</td>
        		<td class="border_right">${o.customer_id.street or ''} ${o.customer_id.street2 or ''} </td>
        		
        		<td class="border_left_right"></td>
        	</tr>
        	<tr>
        		<td class="border_left"></td>
        		<td class="border_right border_bottom_dot">${o.customer_id.city or ''} ${o.customer_id.state_id.name or ''} ${o.customer_id.zip or ''}</td>
        		
        		<td class="border_left_right"></td>
        	</tr>
        	<tr>
        		<td class="border_left border_bottom">NO TELP</td>
        		<td class="border_right border_bottom">${o.phone1 or ''}</td>
        		
        		<td class="border_left_right border_bottom"></td>
        	</tr>
        	<tr>
				<td colspan="3" hleft" width="100%"  style="padding-top:3px; padding-bottom:10px;">
				<b><i>*Garansi diberikan 1 tahun sesuai dengan aturan garansi pabrik</b></i>
				</td>
			</tr>
        	
		</table>
		%endif
		
    % endfor
	
	</body>
</html>