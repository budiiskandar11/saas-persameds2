<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
	<head
		<style>
			.break
			{
			page-break-after: always;
			border: white solid thin;
			}
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
			
			.data
			{
			padding:10px;
			border-collapse:collapse;
			border: lightGrey solid thin;
			width:100%;
			text-align:center;
			background-color:black;
			color:white;
			font-weight:bold;
			}
			
			th
			{
			padding:5px;
			border-collapse:collapse;
			border: lightGrey solid thin;
			}
			
			.bold
			{
			font-weight:bold;
			}
			
			.padded
			{
			padding-top:8px;
			border: lightGrey solid thin;
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
			<% ecount=len(o.employee) %>
			<% tcounter=1 %>
			%for e in o.employee:
				%if tcounter==ecount:
					<table width="100%">
				%else:
					<table class="break" width="100%">
				%endif
						<tr>
							<td class="center"><h2>DAFTAR LEMBUR PEKERJA ${e.status.upper()} BUMI SIAK PUSAKO<h2></td>
						</tr>
						<tr>
							<td class="center">Periode: ${get_periode(o.date)}</td>
						</tr>
						<tr>
							<td class="center">NIK: <b>${e.nik or "-"}</b></b></td>
						</tr>
						<tr>
							<td class="center">Nama: <b>${e.name.upper()}</b></td>
						</tr>
						<tr>
							<td class="center">Anggaran: SDM & Umum</b></td>
						</tr>
						<tr>
							<td width="100%"><br/><br/><br/>
								<table  width="100%">
									<tr>
										<th rowspan="4" colspan="1">No.</th>
										<th rowspan="4" colspan="1">Tanggal</th>
										<th rowspan="2" colspan="2">Jam Kerja</th>
										<th rowspan="4" colspan="1">Jumlah</th>
										<th rowspan="1" colspan="12">Jumlah Jam Lembur</th>
									</tr>
									<tr>
										<th rowspan="1" colspan="6">Aktual</th>
										<th rowspan="1" colspan="6">Hitungan</th>
									</tr>
									<tr>
										<th rowspan="2" colspan="1">Mulai</th>
										<th rowspan="2" colspan="1">Selesai</th>
	
										<th rowspan="1" colspan="2">Hari Kerja</th>
										<th rowspan="1" colspan="3" class="holiday">Hari Libur</th>
										<th rowspan="2" colspan="1">Total</th>
	
										<th rowspan="1" colspan="2">Hari Kerja</th>
										<th rowspan="1" colspan="3" class="holiday">Hari Libur</th>
										<th rowspan="2" colspan="1">Total</th>
									</tr>
									<tr>
										<th rowspan="1" colspan="1">1,5x</th>
										<th rowspan="1" colspan="1">2,0x</th>
										<th rowspan="1" colspan="1" class="holiday">2,0x</th>
										<th rowspan="1" colspan="1" class="holiday">3,0x</th>
										<th rowspan="1" colspan="1" class="holiday">4,0x</th>
	
										<th rowspan="1" colspan="1">1,5x</th>
										<th rowspan="1" colspan="1">2,0x</th>
										<th rowspan="1" colspan="1" class="holiday">2,0x</th>
										<th rowspan="1" colspan="1" class="holiday">3,0x</th>
										<th rowspan="1" colspan="1" class="holiday">4,0x</th>
									</tr>
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
								<% nomor=1 %>
								%for ot_data in get_overtime(e.id, o.date):
									%for ot in ot_data.line_ids:
										%if nomor%2==0:
											<tr bgcolor="#E6F3F2">
										%else:
											<tr>
										%endif
											<td class="center padded">${nomor}</td>
											<td class="center padded">${convert_date(ot.time_start)}</td>
											<td class="center padded">${convert_time(ot.time_start)}</td>
											<td class="center padded">${convert_time(ot.time_end)}</td>
											<td class="center padded">${ot.duration}</td>
										%if is_holiday(ot.time_start)==True:
											<td class="center padded">
												<% dur_x15 = 0.0 %>
												${dur_x15}
											</td>
											<td class="center padded">
												<% dur_x2 = 0.0 %>
												${dur_x2}
											</td>
											%if ot.duration<=7:
												<% dur_hol_x2 = ot.duration %>
												<td class="center padded holiday">${dur_hol_x2}</td>
											%else:
												<% dur_hol_x2 = 7.0 %>
												<td class="center padded holiday">${dur_hol_x2}</td>
											%endif
											<td class="center padded holiday">
												%if ot.duration<=7:
													<% dur_hol_x3 = 0.0 %>
													${dur_hol_x3}
												%else:
													<% dur_hol_x3 = 1.0 %>
													${dur_hol_x3}
												%endif
											</td>
											<td class="center padded holiday">
												%if ot.duration<=8:
													<% dur_hol_x4 = 0.0 %>
													${dur_hol_x4}
												%else:
													<% dur_hol_x4 = ot.duration - 8 %>
													%if dur_hol_x4>0:
														${dur_hol_x4}
													%else:
														<% dur_hol_x4=0 %>
													%endif
												%endif
											</td>
											<td class="center padded">
												<% dur_total = ot.duration %>
												${dur_total}
											</td>
											<td class="center padded">
												<% paid_x15 = 0.0 %>
												${paid_x15}
											</td>
											<td class="center padded">
												<% paid_x2 = 0.0 %>
												${paid_x2}
											</td>
											<td class="center padded holiday">
												<% paid_hol_x2 = dur_hol_x2 * 2 %>
												${paid_hol_x2}
											</td>
											<td class="center padded holiday">
												<% paid_hol_x3 = dur_hol_x3 * 3 %>
												${paid_hol_x3}
											</td>
											<td class="center padded holiday">
												<% paid_hol_x4 = dur_hol_x4 * 4 %>
												${paid_hol_x4}
											</td>
											<td class="center padded">
												<% paid_hol_tot = paid_hol_x2+paid_hol_x3+paid_hol_x4 %>
												${paid_hol_tot}
											</td>
										%else:
											<td class="center padded">
												<% dur_x15 = 1.0 %>
												${dur_x15}
											</td>
											<td class="center padded">
												<% dur_x2 = ot.duration-1%>
												%if dur_x2>0:
													<% dur_x2 %>
												%else:
													<% dur_x2=0.0 %>
												%endif
											</td>
											<td class="center padded holiday">
												<% dur_hol_x2 = 0.0 %>
												${dur_hol_x2}
											</td>
											<td class="center padded holiday">
												<% dur_hol_x3 = 0.0 %>
												${dur_hol_x3}
											</td>
											<td class="center padded holiday">
												<% dur_hol_x4 = 0.0 %>
												${dur_hol_x4}
											</td>
											<td class="center padded">
												<% dur_total = ot.duration %>
												${dur_total}
											</td>
											<td class="center padded">
												<% paid_x15 = dur_x15 * 1.5 %>
												${paid_x15}
											</td>
											<td class="center padded">
												<% paid_x2 = dur_x2 * 2 %>
												${paid_x2}
											</td>
											<td class="center padded holiday">
												<% paid_hol_x2 = 0.0 %>
												${paid_hol_x2}
											</td>
											<td class="center padded holiday">
												<% paid_hol_x3 = 0.0 %>
												${paid_hol_x3}
											</td>
											<td class="center padded holiday">
												<% paid_hol_x4 = 0.0 %>
												${paid_hol_x4}
											</td>
											<td class="center padded">
												<% paid_hol_tot = paid_x15 + paid_x2 %>
												${paid_hol_tot}
											</td>
										%endif
										</tr>
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
										<% nomor+=1 %>
									%endfor
								%endfor
									<tr>
										<td class="center padded bold total" colspan="5">Total</td>
										<td class="center padded sum">${sum_dur_x15}</td>
										<td class="center padded sum">${sum_dur_x2}</td>
										<td class="center padded sum">${sum_dur_hol_x2}</td>
										<td class="center padded sum">${sum_dur_hol_x3}</td>
										<td class="center padded sum">${sum_dur_hol_x4}</td>
										<td class="center padded sum">${sum_dur_total}</td>
										<td class="center padded sum">${sum_paid_x15}</td>
										<td class="center padded sum">${sum_paid_x2}</td>
										<td class="center padded sum">${sum_paid_hol_x2}</td>
										<td class="center padded sum">${sum_paid_hol_x3}</td>
										<td class="center padded sum">${sum_paid_hol_x4}</td>
										<td class="center padded sum">${sum_paid_hol_tot}</td>
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
							<td class="center">Diketahui Oleh,</td>
						</tr>
						%if get_dept().manager_id:
							<tr>
								<td class="nama"><u>${get_dept().manager_id.name.upper() or ""}</u></td>
							</tr>
							<tr>
								<td class="center">Manajer ${get_dept().name.upper() or "SDM & Umum"}</td>
							</tr>
						%else:
							<tr>
								<td class="nama"><u></u></td>
							</tr>
							<tr>
								<td class="center">Manajer SDM & Umum</td>
							</tr>
						%endif
					</table>
				<% tcounter+=1 %>
			%endfor
		%endfor
	</body>
</html>