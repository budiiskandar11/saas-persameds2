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

		<% set hari = {'Sunday':'Minggu','Monday':'Senin','Tuesday':'Selasa','Wednesday':'Rabu','Thursday':'Kamis','Friday':'Jumat','Saturday': 'Sabtu'} %>
        
        <table width="100%" class="one font12px" cellpading="10">
        	
        	
			<tr>
				<td colspan="3" class="font22px hmid" width="100%">BERITA ACARA INSTALASI ALAT</td>
			</tr>
			<tr>
				<td colspan="3" style="padding-top:5px; padding-bottom:25px;" class="font14px hmid" width="100%">Nomor : ${o.name or False}</td>
			</tr>
<<<<<<< HEAD
			<!-- <tr>
				<td colspan="3" class="hleft" width="100%">Pada hari ini ${hari[time.strftime('%A', time.strptime( o.date_install,'%Y-%m-%d %H:%M:%S'))]}, tanggal ${time.strftime('%d', time.strptime( o.date_install,'%Y-%m-%d %H:%M:%S'))},
				bulan ${time.strftime('%B', time.strptime( o.date_install,'%Y-%m-%d %H:%M:%S'))}, tahun ${time.strftime('%Y', time.strptime( o.date_install,'%Y-%m-%d %H:%M:%S'))}, telah dilakukan instalasi alat sebagai berikut :
=======
			<tr>
				<td colspan="3" class="hleft" width="100%">Pada hari ini ________________, tanggal ________________,
				bulan __________________, tahun ________, telah dilakukan instalasi alat sebagai berikut :
>>>>>>> 40d4e20e391f7bd6df4e853c81e153835364f25a
				</td>
			</tr> -->
			<tr>
				<td colspan="3" class="hleft" width="100%">Pada hari ini ____________, tanggal ________________,
				bulan ___________________, tahun ______________, telah dilakukan instalasi alat sebagai berikut :
				</td>
			</tr>
		
			<tr>
				<td width="5%"></td>
				<td style="padding-top:10px; padding-bottom:5px;" colspan="2" class="font14px"><b>DATA PRODUK</b></td>
			</tr>
			<tr>
				<td width="5%"></td>
				<td width="30%" class="kotak">Nama Alat / Product</td>
				<td width="60%" class="kotak"> ${o.product_id.name}</td>
			</tr>
			<tr>
				<td width="5%"></td>
				<td width="30%" class="kotak">Merek / Tipe</td>
				<td width="60%" class="kotak"> ${o.brand_id.name or ''} / ${o.default_code or ''}</td>
			</tr>
			<tr>
				<td width="5%"></td>
				<td width="30%" class="kotak">Negara Asal</td>
				<td width="60%" class="kotak"> ${o.man_country.name or ''}</td>
			</tr>
			<tr>
				<td width="5%"></td>
				<td width="30%" class="kotak">Nomor Seri</td>
				<td width="60%" class="kotak"> ${o.lot_number.name}</td>
			</tr>
			<tr>
				<td width="5%"></td>
				<td colspan="2" style="padding-top:10px; padding-bottom:5px;" class="font14px"><b>DATA CUSTOMER</b></td>
			</tr>
			<tr>
				<td width="5%"></td>
				<td width="30%" class="kotak">Nama Pelanggan</td>
				 %if o.customer_id.parent_id :
				<td width="60%" class="kotak">	${o.customer_id.parent_id.name or ''}</td>
				%else :
				<td width="60%" class="kotak">	${o.customer_id.name or ''}</td>
				%endif
			</tr>
			<tr>
				<td width="5%"></td>
				<td width="30%" class="kotak">Alamat</td>
				<td width="60%" class="kotak">${o.customer_id.street}<br/>
												${o.customer_id.street2}<br/>
												${o.customer_id.city or ''} <br/> ${o.customer_id.state_id.name or ''} ${o.customer_id.zip or ''}
				</td>
			</tr>
			<tr>
				<td width="5%"></td>
				<td width="30%" class="kotak">No. Telp / Fax</td>
				<td width="60%" class="kotak"> ${o.phone1 or ''}</td>
			</tr>
			<tr>
				<td width="5%"></td>
				<td width="30%" class="kotak">Kontak</td>
				<td width="60%" class="kotak"> ${o.contact1 or ''}</td>
			</tr>
			<tr>
				<td width="5%"></td>
				<td width="30%" class="kotak">Nama User *</td>
				%if o.partner_id.parent_id :
				<td width="60%" class="kotak">	${o.partner_id.parent_id.name or ''} - ${o.partner_id.name or ''} </td>
				%else :
				<td width="60%" class="kotak">	${o.partner_id.name or ''}</td>
				%endif
			</tr>
			<tr>
				<td width="5%"></td>
				<td width="30%" class="kotak">Alamat User *</td>
				<td width="60%" class="kotak">${o.partner_id.street or ''}<br/>
												${o.partner_id.street2 or ''}<br/>
												${o.partner_id.city or ''} <br/> ${o.partner_id.state_id.name or ''} ${o.partner_id.zip or ''}
				</td>
			</tr>
			<tr>
				<td width="5%"></td>
				<td width="30%" class="kotak">No. Telp / Fax *</td>
				<td width="60%" class="kotak">${o.phone2 or ''}</td>
			</tr>
			
			<tr>
				<td width="5%"></td>
				<td colspan="2" class="font10px hleft" width="100%"  style="padding-top:5px; padding-bottom:3px;"><i>* Diisi apabila Nama Pelanggan dan User/Pengguna berbeda</i></td>
			</tr>
			<tr>
				<td colspan="3" hleft" width="100%"  style="padding-top:15px; padding-bottom:10px;">
				Demikian Berita Acara Instalasi Alat ini telah dibuat, untuk dipergunakan sebagaimana mestinya.
				</td>
			</tr>
			<tr>
				%if o.partner_id :
				<td colspan="3" hleft" width="100%"  style="padding-top:15px; padding-bottom:20px;">
				${o.partner_id.city or 'Jakarta'}, ____________________
				</td>
				%else:
				<td colspan="3" hleft" width="100%"  style="padding-top:15px; padding-bottom:20px;">
				${o.customer_id.city or 'Jakarta'}, _____________________
				</td>
				%endif
			</tr>
		</table>
		<table width="100%" class="one font12px"  border="1px" cellpading="300px">
			<tr >
				<td style="width:32%; padding-top:5px;">Sole Agent : <br/>
					<b>${o.company_id.name}</b>
				</td>
				 %if o.customer_id.parent_id :
				<td style="width:32%; padding-top:5px;">Pelanggan : <br/>
					<b>${o.customer_id.parent_id.name or ''} - ${o.customer_id.name or ''}</b>
				</td>
				%else :
				<td style="width:32%; padding-top:5px;">Pelanggan : <br/>
					<b>${o.customer_id.name or ''}</b>
				</td>
				%endif
				
				<td style="width:32%; padding-top:5px; ">Pengguna : <br/>
					<b>${o.partner_id.name or ''}</b>
				</td>
			</tr>
			<tr>
				<td style="width:32%; padding-top:5px; "><br/><br/><br/><br/><br/><br/><br/><b>${o.responsible_id.name or 'Nama :'}</b></td>
				<td style="width:32%; padding-top:5px; "><br/><br/><br/><br/><br/><br/><br/><b>${o.contact1 or 'Nama :'}</td>
				<td style="width:32%; padding-top:5px; "><br/><br/><br/><br/><br/><br/><br/><b>${o.contact2 or 'Nama :'}</td>
			</tr>
			<tr>
				<td style="width:32%; padding-top:5px; ">
					Technical Manager
				</td>
				<td style="width:32%; padding-top:5px; "></td>
				<td style="width:32%; padding-top:5px; "></td>
			</tr>
			
		
		</table>
		
		
    % endfor
	
	</body>
</html>
