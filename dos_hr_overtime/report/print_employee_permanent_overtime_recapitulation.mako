<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
	<head
		<style>
			.break { page-break-after: always; }
			.holiday { color:red; }
			body
			{
			border-collapse:collapse;
			border: white solid thin;
			min-height:6in;
			}
		
			table
			{
			padding:10px;
			border-collapse:collapse;
			border: white solid thin;
			}
			
			table.data
			{
			padding:10px;
			border-collapse:collapse;
			border: black solid thin;
			width:100%;
			}
			
			th
			{
			padding:5px;
			border-collapse:collapse;
			border: black solid thin;
			}
			
			.bold
			{
			font-weight:bold;
			}
			
			.padded
			{
			padding:8px;
			}
			
			.ttd
			{
			text-align:center;
			padding-bottom:80px;
			width:50%
			}
			
			.nama
			{
			padding-top:80px;
			text-align:center;
			width:50%;
			font-weight:bold;
			}
			
			.center
			{
			text-align:center;
			vertical-align:center;
			}
			
			.sum
			{
			background-color:black;
			color:white;
			font-weight:bold;
			}
			
			.total
			{
			border-top:black solid thin;
			}
			
		</style>
	</head>
	<body>
		%for o in get_object(data):
			<% setLang('en_ID' or 'en_US') %>
			<table width="100%">
				<tr>
					<td class="center bold">REKAPITULASI JAM & UPAH LEMBUR KARYAWAN</td>
				</tr>
				<tr>
					<td class="center bold">BUMI SIAK PUSAKO</td>
				</tr>
				<tr>
					<td class="center bold">BULAN ${get_periode(o.date).upper()}</b></td>
				</tr>
				<tr>
					<td class="bold"><br/>Beban Anggaran Dept. SDM & Umum<br/></td>
				</tr>
				<tr>
					<td><br/>
						<table class="data">
							<tr>
								<th rowspan="2" colspan="1">No.</th>
								<th rowspan="2" colspan="1">NIK</th>
								<th rowspan="2" colspan="1">Nama</th>
								<th rowspan="1" colspan="2">Jumlah Jam Lembur</th>
								<th rowspan="2" colspan="1">Gaji</th>
								<th rowspan="2" colspan="1">Tarif Upah Lembur</th>
								<th rowspan="2" colspan="1">Jumlah Upah Lembur</th>
								<th rowspan="2" colspan="1">Potongan PPh 21</th>
								<th rowspan="2" colspan="1">Jumlah yang Dibayarkan</th>
							</tr>
							<tr>
								<th rowspan="1" colspan="1">Aktual</th>
								<th rowspan="1" colspan="1">Hitungan</th>
							</tr>
					<% nomor=1 %>
					
					<% sum_sum_dur_total		= 0.0 		%>
					<% sum_sum_paid_hol_tot		= 0.0 		%>
					<% sum_before_pph			= 0.0		%>
					<% sum_pph 					= 0.0		%>
					<% sum_paid 				= 0.0		%>
					
					%for e in o.permanent:
						%if nomor%2==0:
							<tr bgcolor="#E6F3F2">
						%else:
							<tr>
						%endif
						<% sum_dur_x15		= 0.0 %>
						<% sum_dur_x2		= 0.0 %>
						<% sum_dur_hol_x2	= 0.0 %>
						<% sum_dur_hol_x3	= 0.0 %>
						<% sum_dur_hol_x4	= 0.0 %>
						<% sum_dur_total 	= 0.0 %>
						<% sum_paid_x15		= 0.0 %>
						<% sum_paid_x2		= 0.0 %>
						<% sum_paid_hol_x2	= 0.0 %>
						<% sum_paid_hol_x3	= 0.0 %>
						<% sum_paid_hol_x4	= 0.0 %>
						<% sum_paid_hol_tot = 0.0 %>
						%if len(get_overtime(e.id, o.date))>0:
							<% ot=get_overtime(e.id, o.date)[0] %>
							%for ot in ot.line_ids:
								%if is_holiday(ot.time_start)==True:
									<% dur_x15 = 0.0 %>
									<% dur_x2 = 0.0 %>
									%if ot.duration<=7:
										<% dur_hol_x2 = ot.duration %>
									%else:
										<% dur_hol_x2 = 7.0 %>
									%endif
									
									%if ot.duration<=7:
										<% dur_hol_x3 = 0.0 %>
									%else:
										<% dur_hol_x3 = 1.0 %>
									%endif
									
									%if ot.duration<=8:
										<% dur_hol_x4 = 0.0 %>
									%else:
										<% dur_hol_x4 = ot.duration - 8 %>
									%endif
									
									<% dur_total = ot.duration %>
									
									<% paid_x15 = 0.0 %>
									
									<% paid_x2 = 0.0 %>
									
									<% paid_hol_x2 = dur_hol_x2 * 2 %>
									
									<% paid_hol_x3 = dur_hol_x3 * 3 %>
									
									<% paid_hol_x4 = dur_hol_x4 * 4 %>
									
									<% paid_hol_tot = paid_hol_x2+paid_hol_x3+paid_hol_x4 %>
									
								%else:
									<% dur_x15 = 1.0 %>
									
									<% dur_x2 = ot.duration-1%>
									
									<% dur_hol_x2 = 0.0 %>
									
									<% dur_hol_x3 = 0.0 %>
									
									<% dur_hol_x4 = 0.0 %>
									
									<% dur_total = ot.duration %>
									
									<% paid_x15 = dur_x15 * 1.5 %>
									
									<% paid_x2 = dur_x2 * 2 %>
									
									<% paid_hol_x2 = 0.0 %>
							
									<% paid_hol_x3 = 0.0 %>
							
									<% paid_hol_x4 = 0.0 %>
							
									<% paid_hol_tot = paid_x15 + paid_x2 %>
								%endif
								<% sum_dur_x15		+= dur_x15 		%>
								<% sum_dur_x2		+= dur_x2 		%>
								<% sum_dur_hol_x2	+= dur_hol_x2 	%>
								<% sum_dur_hol_x3	+= dur_hol_x3 	%>
								<% sum_dur_hol_x4	+= dur_hol_x4 	%>
								<% sum_dur_total	+= dur_total 	%>
								<% sum_paid_x15		+= paid_x15 	%>
								<% sum_paid_x2		+= paid_x2 		%>
								<% sum_paid_hol_x2	+= paid_hol_x2 	%>
								<% sum_paid_hol_x3	+= paid_hol_x3 	%>
								<% sum_paid_hol_x4	+= paid_hol_x4  %>
								<% sum_paid_hol_tot	+= paid_hol_tot %>
							%endfor
						%endif
								<td class="center padded">${nomor}</td>
								<td class="center padded">${e.nik or "-"}</td>
								<td>${e.name.title()}</td>
								<td class="center padded">${sum_dur_total}</td>
								<td class="center padded">${sum_paid_hol_tot}</td>
								%if get_contract(e.id, o.date)==False:
									<td class="center padded">Rp ${formatLang(0.0,digits=get_digits(dp='Sale Price'))}</td>
									<% basic = 0 %>
								%else:
									<td class="center padded">Rp ${formatLang(round(get_contract(e.id, o.date).basic),digits=get_digits(dp='Sale Price'))}</td>
									<% basic = round(get_contract(e.id, o.date).basic) %>
								%endif
								<td class="center padded">Rp ${formatLang(round(basic/173),digits=get_digits(dp='Sale Price'))}</td>
								<% per_hour = round(basic/173) %>
								<td class="center padded">Rp ${formatLang(round(per_hour*sum_paid_hol_tot),digits=get_digits(dp='Sale Price'))}</td>
								<% before_pph = round(per_hour*sum_paid_hol_tot) %>
								<td class="center padded">Rp ${formatLang(round(before_pph*0.15),digits=get_digits(dp='Sale Price'))}</td>
								<% pph = round(before_pph*0.15) %>
								<td class="center padded">Rp ${formatLang(before_pph-pph,digits=get_digits(dp='Sale Price'))}</td>
								<% paid = before_pph-pph %>
							</tr>
							
						<% sum_sum_dur_total		+= sum_dur_total 		%>
						<% sum_sum_paid_hol_tot		+= sum_paid_hol_tot 	%>
						<% sum_before_pph			+= before_pph 			%>
						<% sum_pph					+= pph 					%>
						<% sum_paid					+= paid					%>
						
						<% nomor+=1 %>
					%endfor
							<tr>
								<td class="center padded bold total" colspan="3">Jumlah</td>
								<td class="center padded sum">${sum_sum_dur_total}</td>
								<td class="center padded sum">${sum_sum_paid_hol_tot}</td>
								<td class="center padded sum">X</td>
								<td class="center padded sum">X</td>
								<td class="center padded sum">Rp ${formatLang(sum_before_pph,digits=get_digits(dp='Sale Price'))}</td>
								<td class="center padded sum">Rp ${formatLang(sum_pph,digits=get_digits(dp='Sale Price'))}</td>
								<td class="center padded sum">Rp ${formatLang(sum_paid,digits=get_digits(dp='Sale Price'))}</td>
							</tr>
						</table>
					</td>
				</tr>
				<tr>
					<td class="center"><br/><br/><br/>Pekanbaru, ${get_current_date()}</td>
				</tr>
				<tr>
					<td class="center">BUMI SIAK PUSAKO</td>
				</tr>
				<tr>
					<td class="center">Disetujui Oleh,</td>
				</tr>
				<tr>
					<td class="nama"><u>${get_dept().manager_id.name.upper() or ""}</u></td>
				</tr>
				<tr>
					<td class="center">Manajer ${get_dept().name.upper() or "SDM & Umum}</td>
				</tr>
			</table>
		%endfor
	</body>
</html>