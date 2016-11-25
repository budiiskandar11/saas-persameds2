
<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
<style>
div
	{
	min-height:1290px;
	height:1290px;
	margin-top:20px;
	margin-bottom:20px;
	position:relative;
	}
table
	{
	font-size:12px;
	}
td
	{
	padding:4px;
	}
#page_note
	{
	border:1px solid #000;
	right:0px;
	position:relative;
	font-size:12px;
	margin-right:0px;
	}
table .header
	{
	display:none;
	}
.main
	{
	width:23.7cm;
	margin:0 auto;
	}
.main td
	{
	border:1px solid #000;
	}
td .pajak
	{
	border:0px;
	}
.partner td
	{
	border:0px;
	}
.lines
	{
	border-collapse:collapse;
	width:23.7cm;
	}
.inv_line td
	{
	border-top:0px;
	border-bottom:0px;
	}
.inv_cell
	{
	text-align:right;
	}
	
</style>
</head>
<body>

%for x in objects:
	%for i in (1,2,3):
		<div style="clear:both">
			
			
			<table width="895px" cellpadding="0">
				<tr>
					<td width="537px" ></td>
					<td width="358px" >
						<table id="page_note" right="0" width="358px">
							<tr>
								<td width="20%" valign="top">Lembar ${i} : </td>
								<td width="80%">
								%if i==1:
									Untuk Pembeli BKP / Penerima JKP sebagai bukti Pajak Masukan
								%elif i==2:
									Untuk Pengusaha Kena Pajak yang menerbitkan Faktur Pajak Standar sebagai  bukti Pajak Keluaran
								%else:
									Untuk Pembukuan</br>
								%endif
								</td>
							</tr>	
						</table>
					</td>
				</tr>
			</table>
			<br>
			<br>
			<center style="width:23.7cm;"><h3>FAKTUR PAJAK</h3></center>
			<br>
			
			
			%for o in objects:
				
				<table class="main" cellspacing="0">
					<tr>
						<td colspan="3">Kode dan Nomor Seri Faktur Pajak : 
							
							${o.nomor_faktur_id.name}
						</td>
					</tr>
					<tr>
						<td colspan="3">Pengusaha Kena Pajak</td>
					</tr>
					<tr>
						<td colspan="3">
							<table class="partner" border="0">
								<tr>
									<td>Nama</td>
									<td>:</td>
									<td>${(o.company_id and o.company_id.name) or ''}</td>
								</tr>
								<tr>
									<td>Alamat</td>
									<td>:</td>
									<td>${o.company_id.street or ''} ${o.company_id.street2 or ''}<br> ${o.company_id.city or ''} - ${o.company_id.country_id.name or ''}</td>
								</tr>
								<tr>
									<td>NPWP</td>
									<td>:</td>
									<td>${(o.company_id and o.company_id.npwp) or ''}</td>
								</tr>
							</table>
						</td>
					</tr>
					<tr>
						<td colspan='3'>Pembeli Barang Kena Pajak/Penerima Jasa Kena Pajak</td>
					</tr>
					<tr>
						<td colspan='3'>
							<table class="partner" border="0">
								<tr>
									<td>Nama</td>
									<td>:</td>
									<td>${(o.partner_id and o.partner_id.title and o.partner_id.title.name) or ''} ${(o.partner_id and o.partner_id.name) or ''}</td>
								</tr>
								<tr>
									<td>Alamat</td>
									<td>:</td>
									<td>${o.partner_id.street or ''} ${o.partner_id.street2 or ''}<br> ${o.partner_id.city or ''} - ${o.partner_id.country_id.name or ''}</td>
								</tr>
								<tr>
									<td>NPWP</td>
									<td>:</td>
									<td></td>
								</tr>
							</table>
						</td>
					</tr>
					
						<tr>
							<td style='width:40px'>No.Urut</td>
					        <td align="center">Nama Barang Kena Pajak / Jasa Kena Pajak</td>
					        <td align="center" width="30%">Harga Jual /Penggantian /Uang Muka /Termin *)</td>
						</tr>
						
        
        
						%for invoice_line in o.invoice_line:
							%if invoice_line.product_id.type != 'service':
								<tr class='inv_line'>
									<td align='right'>${n}</td>
									<td>${invoice_line.name or ""}</td>
									<td align='right' width="30%">${formatLang(invoice_line.price_subtotal)}</td>
								</tr>
							
							%endif
							
						
						%endfor
						
						<tr class="inv_line"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr class="inv_line"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr class="inv_line"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr class="inv_line"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr class="inv_line"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr class="inv_line"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr class="inv_line"><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
						<tr>
							<td colspan='2'>
								Harga Jual /Penggantian /Uang Muka /Termin *)
							</td>
							<td align='right'></td>
						</tr>
						<tr>
							<td colspan='2'>Dikurangi potongan harga</td>
							<td align='right'>0</td>
						</tr>
						<tr>
							<td colspan='2'>Dikurangi Uang Muka yang sudah diterima</td>
							<td align='right'>0</td>
						</tr>
						<tr>
							<td colspan='2'>Dasar Pengenaan Pajak</td>
							<td colspan='2' align='right'></td>
						</tr>
						<tr>
							<td colspan='2'>PPN = 10% X Dasar Pengenaan Pajak</td>
							<td align='right'></td>
						</tr>
					
					<tr>
						<td colspan='5'>
							<table width="100%" border="0px" cellspacing='0'>
								<tr>
									<td colspan='4' class='pajak'>Tarif Penjualan Atas Barang Mewah</td>
									<td width="30%" style="text-align:left; border: 0;">${o.company_id.partner_id.city or ""}, ${time.strftime('%d %B %Y', time.strptime( o.date_invoice,'%Y-%m-%d'))}</td>
								</tr>
								<tr>
									<td>Tarif</td>
									<td>DPP</td>
									<td>PPn</td>
								</tr>
								<tr>
									<td>........... </td>
									<td>Rp </td>
									<td>Rp </td>
									<td rowspan='4' class='pajak'></td>
								</tr>
								<tr>
									<td>........... </td>
									<td>Rp </td>
									<td>Rp</td>
									<td style="border: 0";></td>
								</tr>
								<tr>
									<td>........... %</td>
									<td>Rp </td>
									<td>Rp</td>
									<td style="border: 0";></td>
								</tr>
								<tr>
									<td>........... </td>
									<td>Rp </td>
									<td>Rp</td>
									<td rowspan="2" width="30%" style="text-align:left; border: 0;">
										<span style="border-bottom: 1px solid;">Nama : </span>
										<p style="margin-top: 0;">
											Jabatan : 
										</p>
									</td>
								</tr>
								<tr>
									<td colspan='2'>Jumlah</td>
									<td></td>
									<td style="border: 0; margin-top: -10px;"></td>
								</tr>
							</table>
						</td>
					</tr>
				</table>
			%endfor
			<font size='0.5' style='margin-left:14px'>*) Coret yang tidak perlu</font>
		</div>
	%endfor
%endfor
</body>
</html>
