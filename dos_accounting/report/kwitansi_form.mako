<html>
<body>
%for o in objects :
<% setLang(o.partner_id.lang) %>
<div  style="margin:0px auto;">
<TABLE width=80% border="1">
	<TR>
		<TD width=100%>${ counter(o) }
			<table id="header" width=100% border="0">
				<tr>
					<td width="20%" align="center">
						<img src="data:image/png;base64,${ o.company_id.logo }" alt="Red dot" width="128px" height="89px" />
					</td>
					<td align="center">
						<font size="5"><b><u></u></b></font><br>
						<a><font size="2"><div align="left">${ o.company_id.street } ${o.company_id.city}<br> ${o.company_id.phone}<br>${o.company_id.website}</div></font></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
							&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
							&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
							&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
					</td>
					<td width="25%" valign="top">
						<font size="2">Tanda Terima Sementara<br>No.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; : ${ o.name }</font>
					</td>
				</tr>
			</table>
		</TD>
	</TR>
	<TR>
		<TD width=100%>
			<table id="isi" width=100% border="0">
				<tr>
					<td width="18%">
						<font size="2"><u>Sudah Terima dari</u><br><i>Received from</i></font>
					</td>
					<td width="1%" valign="top">
						<font size="2">:</font>
					</td>
					<td width="81%">
						${o.partner_id.name}
					</td>
				</tr>
				<tr>
					<td width="18%">
						<font size="2"><u>Banyaknya Uang</u><br><i></i></font>
					</td>
					<td width="1%" valign="top">
						<font size="2">:</font>
					</td>
					<td width="81%">
						Rp ${o.amount_to_pay}
					</td>
				</tr>
				<tr height="60">
					<td width="18%" valign="top">
						<font size="2"><u>Untuk Pembayaran</u><br><i>In Payment Of</i></font>
					</td>
					<td width="1%" valign="top">
						<font size="2">:</font>
					</td>
					<td width="81%">
						${o.ref}
					</td>
				</tr>
				<tr>
					<td width="18%" colspan="3" bgcolor="grey" height="35">
						<font size="2"><b>Rp. ${o.amount_to_pay}</b></font><br>
					</td>
				</tr>
				<tr>
					<td colspan="3">
						<table width="100%" border="0">
							<tr height="150" valign="top">
								<td width="60%"><font size="2"><b>Catatan : </b></font></td>
								<td width="40%" align="center"><font size="2">${time.strftime(time.ctime()[0:3])} , ${ time.strftime('%d/%m/%Y') }<br><br><br><br><br><br><br>(&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)</font></td>
							</tr>
						</table>
					</td>
				</tr>
			</table>
		</TD>
	</TR>
</TABLE>
</div>
%endfor
</body>
</html>