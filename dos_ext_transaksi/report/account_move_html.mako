<html>
<head>
    <style type="text/css">
        body {
              	font-family:Arial;
        }

        table #head {
        	width:100%;
        }
        .list_table0 {
			font-size:18px;
			#font-weight:bold;
			padding-top:10px;
			padding-bottom:10px;
			padding-right:15%;
			width:70%;
			border-collapse:collapse;
        	border-top:1px solid white;
        	border-bottom:1px solid white;
        	border-left:1px solid white;
		}
		.list_table1{
			width:100%;
			font-size:11px;
			border-left:1px solid black;
			border-top:1px solid black;
        	border-bottom:1px solid black;
        	border-right:1px solid black;
		}
		.list_table2 {
			font-size:10px;
		}
		.list_table3 {
			font-size:10px;
		}
		.list_table4 {
			font-size:10px;
			padding-top:5px;
			padding-bottom:5px;
		}
		.cust_info
			{
			font-size:10px;
			font-weight:bold;
			border-top:1px solid black;
			border-bottom:1px solid black;
			border-left:1px solid black;
			border-right:1px solid black;
			padding-top:6px;
			padding-bottom:6px;
			}
		.inv_line td
			{
			border-top:0px;
			border-bottom:0px;
			}
		.inv_line2 td
			{
			border-bottom:0px;
			}
    </style>
</head>
<body>
    %for ext in objects :
    <% setLang(company.partner_id.lang) %>
    <hr size="2px" color="white">
    <table width="100%">
    	<tr valign="top">
    		<td width="100%" style="font-family:Arial Black;" colspan="4" style="font-size:14" align="center"><u>JOURNAL VOUCHER</u></td>
    	</tr>
    	<tr class="list_table1" style="font-family:Arial Black;">
    		<td width="65%">Number. ${ext.name or ''|entity}</td>
    		<td width="10%"></td>
    		<td width="2%"></td>
    		<td width="23%"></td>
    	</tr>
    	<tr class="list_table1" style="font-family:Arial Black;">
    		<td width="65%">Jurnal. ${ext.journal_id.name or ''|entity}</td>
    		<td width="10%">Tanggal</td>
    		<td width="2%">:</td>
    		<td width="23%">${time.strftime('%d %b %Y', time.strptime(ext.date,'%Y-%m-%d')) or ''|entity}</td>
    	</tr>
    	<tr class="list_table1" style="font-family:Arial Black;">
    		<td width="65%">Referensi : ${ext.ref or ''|entity}</td>
    		<td width="10%">Periode</td>
    		<td width="2%">:</td>
    		<td width="23%">${ext.period_id.name or ''|entity}</td>
    	</tr>
    </table>
    <hr size="2px" color="white">
    <table class="list_table1" border="1" style="border-collapse:collapse;" width="100%" cellpadding="3">
        <tr style="text-align:center;" style="font-family:Arial Black;">
        	<th width="40%">${_("Nama")}</th>
        	<th width="25%">${_("Akun")}</th>
        	<th width="10%">${_("Kode Rekening")}</th>
        	<th width="8%">${_("Debet")}</th>
        	<th width="8%">${_("Kredit")}</th>
        	<th width="9%">${_("Amount")}</th>
        </tr>
        <%
        i = 1
        totdebit = totcredit = 0
        %>
        %for line in ext.line_id:
	        <tr class='inv_line'>
	        	<td style="text-align:left;" valign="top">${line.name or ''|entity}</td>
	        	<td style="text-align:left;" valign="top">${line.account_id.name or ''|entity}</td>
	        	<td style="text-align:center;" valign="top">${line.account_id.code or ''|entity}</td>
	        	<td style="text-align:right;" valign="top">${line.debit or ''|entity}</td>
	        	<td style="text-align:right;" valign="top">${line.credit or ''|entity}</td>
	        	<td style="text-align:right;" valign="top">${line.amount_currency or ''|entity}</td>
	        </tr>
	        <%
	        i=i+1
	        totdebit += line.debit
	        totcredit += line.credit
	        %>
        %endfor
        
        <tr class='inv_line'>
        	<td><table><tr><td style="font-size:11px;color:white;">${blank_line(i)}</td></tr></table></td>
        	<td style="text-align:center;"></td>
        	<td style="text-align:center;"></td>
        	<td styyle="text-align:left;"></td>
        	<td styyle="text-align:left;"></td>
        	<td styyle="text-align:left;"></td>
        </tr>
        <tr class='inv_line2'>
        	<td style="text-align:left;" colspan="3">Total</td>
        	<td style="text-align:right;">${ formatLang(totdebit,digits=get_digits(dp='Account')) or 0}</td>
        	<td style="text-align:right;">${ formatLang(totcredit,digits=get_digits(dp='Account')) or 0}</td>
        	<td style="text-align:right;"></td>
        </tr>
   </table>
   <br/><br/>
   <table style="float:right;border-collapse:collapse;" border="1" style="border-collapse:collapse;" width="60%" cellpadding="3">
        <tr style="text-align:center;">
        	<td width="10%">Dibuat Oleh</td>
        	<td width="10%">Diperiksa Oleh</td>
        	<td width="10%">Disetujui Oleh</td>
        </tr>
        <tr>
        	<td style="text-align:right;"><br/><br/><br/><br/></td>
        	<td style="text-align:center;"></td>
        	<td style="text-align:left;"></td>
        </tr>
    </table>	
    %endfor
</body>
</html>
