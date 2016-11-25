<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
	<head>
		<%
		import addons
		path=addons.get_module_resource("ad_hr_training/static/jquery-1.8.3.min.js")
		%>
		<script src="${path}" type="text/javascript"></script>
		<style>
			.break { page-break-after: always; }
		
			h2
			{
			text-align:'center';
			}
			
			table.general
			{
			border-collapse:collapse;
			border: black solid thin;
			padding:10px;
			width:100%;
			}
			
			td.data
			{
			border-bottom:thin solid black;
			width:69%;
			}
			
			.var
			{
			font-weight:bold;
			}
			
			.padded
			{
			text-align:center;
			padding-top:30px;
			}
			
			.ttd
			{
			text-align:center;
			padding-bottom:80px;
			width:50%
			}
			
			.nama
			{
			text-align:center;
			width:50%;
			font-weight:bold;
			}
			
			th
			{
			border-bottom:medium solid black;
			font-size:150%;
			width:80%;
			}
			
		</style>
		<script>
			$(document).ready(function(){
				$('table:last-child').css('page-break-after',"auto");
			})
		</script>
	</head>
	<body>
		%for o in get_object(data):
		<% setLang('id_ID' or 'en_US') %>
			%for e in o.employee:
			<table cellpadding=10px class="general break">
				<tr>
					<th colspan="3">
						USULAN PENGIRIMAN TRAINING <br />
						BUMI SIAK PUSAKO
					</th>
				</tr>
				<tr>
					<td class="var">Yang akan dikirim</td>
					<td>:</td>
					<td class="data">${e.name}</td>
				</tr>
				<tr>
					<td class="var">NIK</td>
					<td>:</td>
					<td class="data">${e.nik}</td>
				</tr>
				<tr>
					<td width="30%" class="var">Jabatan</td>
					<td>:</td>
					<td class="data">${e.job_id.name}</td>
				</tr>
				<tr>
					<td class="var">Nama Pelatihan</td>
					<td>:</td>
					<td class="data">${o.name}</td>
				</tr>
				<tr>
					<td class="var">Jenis</td>
					<td>:</td>
					<td class="data">${o.type.name or "-"}</td>
				</tr>
				<tr>
					<td class="var">Penyelenggara</td>
					<td>:</td>
					<td class="data">${o.provider.name}</td>
				</tr>
				<tr>
					<td class="var">Biaya</td>
					<td>:</td>
					<td class="data">${o.currency.symbol or ""} ${formatLang(int(o.cost),digits=get_digits(dp='Sale Price'))}</td>
				</tr>
				<tr>
					<td class="var">Tempat</td>
					<td>:</td>
					<td class="data">${o.location}</td>
				</tr>
				<tr>
					<td class="var">Waktu</td>
					<td>:</td>
					<td class="data">${get_start(o.date_start)} - ${get_end(o.date_end)}</td>
				</tr>
				<tr>
					<td class="var" valign="top">Alasan Pengusulan</td>
					<td valign="top">:</td>
					<td class="data">${o.purpose or "-"}</td>
				</tr>
				<tr>
					<td class="padded" colspan="3">
						${o.pengusul.work_location.title() or ""}, ${get_current_date()}
					</td>
				</tr>
				%if o.pengusul.parent_id or e.parent_id:
				<tr>
					<td colspan="3">
						<table width="100%">
							<tr>
								<td class="ttd">Diusulkan Oleh</td>
								<td class="ttd">Mengetahui</td>
							</tr>
							<tr>
								<td class="nama"><u>${o.pengusul.name.title()}</u></td>
								<td class="nama"><u>${o.pengusul.parent_id.name.title() or e.parent_id.name.title() or "-"}</u></td>
							</tr>
							<tr>
								<td align="center">${o.job_id.name}</td>
								<td align="center">${o.pengusul.parent_id.job_id.name or e.parent_id.job_id.name or ""}</td>
							</tr>
							<tr>
								<td class="ttd" colspan="2" padding-top="10px">Disetujui Oleh</td>
							</tr>
							%if o.department.company_id.partner_id.director:
							<tr>
								<td class="nama" colspan="2"><u>${o.department.company_id.partner_id.director.name.title() or "-"}</u></td>
							</tr>
							%endif
							<tr>
								<td align="center" colspan="2">Direktur</td>
							</tr>
						</table>
					</td>
				</tr>
				%else:
				<tr>
					<td colspan="3">
						<table width="100%">
							<tr>
								<td class="ttd">Diusulkan Oleh</td>
								<td class="ttd">Disetujui Oleh</td>
							</tr>
							<tr>
								<td class="nama"><u>${o.pengusul.name.title()}</u></td>
								%if o.department.company_id.partner_id.director:
								<td class="nama"><u>${o.department.company_id.partner_id.director.name.title() or "-"}</u></td>
								%endif
							</tr>
							<tr>
								<td align="center">${o.job_id.name}</td>
								<td align="center">Direktur</td>
							</tr>
						</table>
					</td>
				</tr>
				%endif
			</table>
			%endfor
		%endfor
	</body>
</html>