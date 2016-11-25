<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
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
			.border_top_bottom
			{
				border-top: 1px solid lightGrey;
				border-bottom: 1px solid black;
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
			.font10px
			{
				font-size: 10px;
			}
			.font14px
			{
				font-size: 14px;
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
		<div style="clear:both">
		
		
		
		<table class="paddingtop" cellpadding="2px" width="100%">
			<tr>
				<td align="center" class="font14px">BERITA ACARA PEMERIKSAAN UANG KAS</td>
			</tr>
		</table>
		<table cellpadding="2px" width="100%">
			<tr>
				<td align="left" class="font12px">Pada hari ini tanggal ${time.strftime('%d', time.strptime( o.date_opname,'%Y-%m-%d'))} Bulan ${time.strftime('%B', time.strptime( o.date_opname,'%Y-%m-%d'))} Tahun ${time.strftime('%Y', time.strptime( o.date_opname,'%Y-%m-%d'))} telah diadakan
				pemeriksaan dan penghitungan uang kash dengan hasil sebagai berikut :
				</td>
			</tr>
			
		</table>
		
		<table cellpadding="1px" class="font12px " width="100%">
			<tr>
				<td align="left" class="font12px "><b>I. Uang Tunai</b></td>
			</tr>
			<tr>
				<td class="hmid">1</td>
				<td class="hmid">Uang Kertas</td>
				<td class="hmid border_top_bottom"></td>
				<td class="hmid border_top_bottom">Pecahan</td>
				<td class="hmid border_top_bottom">Jumlah</td>
				<td class="hmid border_top_bottom" ></td>
				<td class="hmid border_top_bottom">Nilai Uang</td>
				<td class="hmid border_top_bottom"></td>
				<td class="hmid border_top_bottom"></td>
			</tr>
			%for l in o.cash_ids: 
				% if l.type == 'kertas':
				<tr>
					<td></td>
					<td></td>
					<td>${ o.currency_id.symbol or ''}</td>
					<td class="hright" >${ formatLang(l.name) or formatLang(0)}</td>
					<td class="hmid">${ l.qty_bagus or 0.0}</td>
					<td>${ o.currency_id.symbol or ''}</td>
					<td class="hright">${ formatLang(l.sub_total_bagus) or formatLang(0)}</td>
				    <td></td>
				    <td></td>
				</tr >	
				%endif
			 %endfor
			 <tr >
				<td></td>
				<td class="hright">Jumlah Uang tunai</td>
				<td ></td>
				<td></td>
				<td></td>
				<td></td>
				<td></td>
				<td class=" border_top_bottom">${ o.currency_id.symbol or ''}</td>
				<td class=" hright border_top_bottom">${ formatLang(o.total_uang_kertas) or formatLang(0)}</td>	
			</tr>	
		
			<tr>
				<td class="hmid">2</td>
				<td class="hleft">Uang Kertas Rusak</td>
				<td class="hmid border_top_bottom"></td>
				<td class="hmid border_top_bottom">Pecahan</td>
				<td class="hmid border_top_bottom">Jumlah</td>
				<td class="hmid border_top_bottom" ></td>
				<td class="hmid border_top_bottom">Nilai Uang</td>
				<td class="hmid "></td>
				<td class="hmid "></td>
			</tr>
			%for l in o.cash_ids: 
				% if l.type == 'kertas':
				<tr>
					<td></td>
					<td></td>
					<td>${ o.currency_id.symbol or ''}</td>
					<td class="hright" >${ formatLang(l.name) or formatLang(0)}</td>
					<td class="hmid">${ l.qty_bagus or 0.0}</td>
					<td>${ o.currency_id.symbol or ''}</td>
					<td class="hright">${ formatLang(l.sub_total_rusak) or formatLang(0)}</td>
				</tr >	
				%endif
			 %endfor
			 <tr >
				<td></td>
				<td class="hright">Jumlah Uang tunai</td>
				<td></td>
				<td></td>
				<td></td>
				<td></td>
				<td></td>
				<td class="border_top_bottom">${ o.currency_id.symbol or ''}</td>
				<td class="hright border_top_bottom">${ formatLang(o.total_kertas_rusak) or formatLang(0)}</td>	
			</tr>	
		
			<tr>
				<td class="hmid">3</td>
				<td class="hleft">Uang Logam</td>
				<td  class="hmid border_top_bottom"></td>
				<td class="hmid border_top_bottom">Pecahan</td>
				<td class="hmid border_top_bottom">Jumlah</td>
				<td class="hmid border_top_bottom" ></td>
				<td class="hmid border_top_bottom">Nilai Uang</td>
			</tr>
			%for l in o.cash_ids: 
				% if l.type == 'logam':
				<tr>
					<td></td>
					<td></td>
					<td>${ o.currency_id.symbol or ''}</td>
					<td class="hright" >${ formatLang(l.name) or formatLang(0)}</td>
					<td class="hmid">${ l.qty_bagus or 0.0}</td>
					<td>${ o.currency_id.symbol or ''}</td>
					<td class="hright">${ formatLang(l.sub_total_bagus) or formatLang(0)}</td>
				</tr >	
				%endif
			 %endfor
			 <tr >
				<td></td>
				<td class="hright">Jumlah Uang tunai</td>
				<td></td>
				<td></td>
				<td></td>
				<td></td>
				<td></td>
				<td class="border_top_bottom ">${ o.currency_id.symbol or ''}</td>
				<td class="hright border_top_bottom">${ formatLang(o.total_logam) or formatLang(0)}</td>	
			</tr>	
			<tr>
				<td></td>
				<td align="left" class="font12px">Jumlah Total Uang Tunai</td>
				<td></td>
				<td></td>
				<td></td>
				<td></td>
				<td></td>
				<td class="border_top_bottom">${ o.currency_id.symbol or ''}</td>
				<td class=" hright border_top_bottom">${ formatLang(o.total_cash) or formatLang(0)}</td>	
			
			</tr>
		
			<tr>
				<td align="left" class="font12px "><b>II. Uang Non Tunai<b></td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				
				<td  class="hmid ">Nilai Uang</td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
			</tr>
			
		
			<tr>
				
				<td class="hmid">1</td>
				<td class="hleft">Eviden Dalam Proses (Sesuai Lampiran)</td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td class="">${ o.currency_id.symbol or ''}</td>
				<td class="hright">${ formatLang(o.eviden) or formatLang(0)}</td>
				<td class="hright" ></td>
				<td class="hmid"></td>
				<td class="hmid"></td>
				
			</tr>
			<tr>
				
				<td class="hmid">2</td>
				<td class="hleft">Selisih Pembulatan</td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td class="">${ o.currency_id.symbol or ''}</td>
				<td class="hright">${ formatLang(o.bulat) or formatLang(0)}</td>
				<td class="hright" ></td>
				<td class="hmid"></td>
				<td class="hmid"></td>
				
			</tr>
			<tr>
				
				<td class="hmid">3</td>
				<td class="hleft">Bon Sementara (sesuai lampiran)</td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td class="">${ o.currency_id.symbol or ''}</td>
				<td class="hright">${ formatLang(o.bon_sementara) or formatLang(0)}</td>
				<td class="hright" ></td>
				<td class="hmid"></td>
				<td class="hmid"></td>
				
			</tr>
			<tr>
				
				
				<td class="hmid"></td>
				<td class="hleft">Jumlah Uang Non Tunai</td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td class="">${ o.currency_id.symbol or ''}</td>
				<td class="hright" >${ formatLang(o.total_non_cash) or formatLang(0)}</td>
				<td class="hright" ></td>
				
				
			</tr>
			<tr>
				
				
				<td class="hmid"></td>
				<td class="hleft">Jumlah Uang Kas Dihitung</td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td class="">${ o.currency_id.symbol or ''}</td>
				<td class="hright">${ formatLang(o.grand_total) or formatLang(0)}</td>
				<td class="hright" ></td>
				
				
			</tr>
			<tr>
				
				
				<td class="hmid"></td>
				<td class="hleft">Jumlah Uang Kas Odoo</td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td >${ o.currency_id.symbol or ''}</td>
				<td class="hright">${ formatLang(o.ending_balance) or formatLang(0)}</td>
				<td class="hright" ></td>
				
				
			</tr>
			<tr>
				
				
				<td class="hmid"></td>
				<td class="hleft">Selisih</td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td align="left" class="font12px "></td>
				<td class="border_top_bottom">${ o.currency_id.symbol or ''}</td>
				<td class="hright border_top_bottom">${ formatLang(o.selisih) or formatLang(0)}</td>
				<td class="hright" ></td>
				
				
			</tr>
		</table>
		<tr>&nbsp;&nbsp;</tr>
		<tr>&nbsp;&nbsp;</tr>
		<table cellpadding="1px" width="100%">
			<tr>
				<td align="left" class="font12px">Dengan ini saya menyatakan bahwa dana tersebut diatas telah  
				diperiksa dan dihitung di hadapan saya oleh <b>${ o.check_by.name or '#NA'} </b> selaku <b>${ o.check_by.job_id.name or '#NA'}</b> dan telah diserahkan kembali kepada
				saya dalam keadaan seperti semula</td>
			</tr>
			<tr>
				<td align="left" class="font12px">Tidak ada lagi dana lain yang dipercayana oleh perusahaan, PT Energia
				Prima Nusantara kepada saya yang belum saya beritahukan</td>
			</tr>
			
		</table>
		<table cellpadding="1px" width="100%"  class="font12px">
			<tr style="height=60px;">
				<td></td>
		     	<td></td>
		     	
		     	<td></td>
		     	<td></td>
		     	<td></td>
		     	<td></td>
		     	<td>Jakarta, ${time.strftime('%d-%m-%Y', time.strptime( o.date_opname,'%Y-%m-%d'))}</td>
			</tr>
			<tr>
				<td width="20%" align="center">Disetujui :</td>
				<td ></td>
		     	<td width="20%" align="center">Diketahui oleh:</td>
		     	<td></td>
		     	<td width="20%" align="center">Diperiksa oleh:</td>
		     	<td></td>
		     	<td width="20%" align="center">Dibuat oleh :</td>
		     	<td></td>
			</tr>
			<tr>
			   <td>
					   <br></br>
						<br></br>
						<br></br>
						<br></br>
						<br></br>
				</td>
				<td></td>
				<td></td>
				<td></td>
				<td align="center">	<br></br>
						<br></br>
						<br></br>
						<br></br>
						<br></br>
						${ o.check_by and o.check_by.name or '#NA'}
				</td>
				<td></td>
				<td align="center"> <br></br>
						<br></br>
						<br></br>
						<br></br>
						<br></br>
						${o.user_id.name}</td>
			</tr>
			
			<tr>
				<td width="20%" align="center" class="border_top">Direktur</td>
				<td width="5%"></td>
		     	<td width="20%"  align="center" class="border_top">FA Dept. Head</td>
		     	<td width="5%"></td>
		     	<td width="20%"  align="center" class="border_top">Treasury Sec Head</td>
		     	<td width="5%"></td>
		     	<td width="20%"  align="center" class="border_top">Cashier</td>
			</tr>
		</table>
		
		</div>
	</body>
	%endfor
	
</html>