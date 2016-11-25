<html>
<head>
    <style type="text/css">
        table #head {
        	width:100%;
        }
        .list_table0 {
			font-size:18px;
			font-weight:bold;
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
    </style>
</head>
<body>
    %for adv in objects :
    <% setLang(company.partner_id.lang) %>
    <table width="100%" class="list_table0">
	    <tr>
		    <td width="50%" rowspan="2">
		    <span style="text-align:right;font-size:24">${helper.embed_logo_by_name('bsp_logo_small')}&nbsp;&nbsp;&nbsp;<b>${_("BUMI SIAK PUSAKO")}</b></span>
		    </td>
	    </tr>
    </table>
    <hr size="2px" color="white">
	<table width="100%" class="list_table1" cellpadding="3">
	    <tr valign="top">
	    	<td width="100%" colspan="6" style="font-size:14" align="center"><u>BUKTI KAS BON GANTUNG</u></td>
	    </tr>
	    <tr valign="top">
	    	<td width="14%">Sudah Terima oleh</td>
	    	<td width="1%">:</td>
	    	<td width="35%">${adv.employee_id.name or ''|entity}${'/'+adv.employee_id.nik or ''|entity}</td>
	    	<td width="14%">Voucher No.</td>
	    	<td width="1%">:</td>
	    	<td width="35%">${adv.number or ''|entity}</td>
	    </tr>
	    <tr valign="top">
	    	<td width="14%">Uang Sejumlah</td>
	    	<td width="1%">:</td>
	    	<td width="35%">${ adv.currency_id.symbol or '' } ${ formatLang(adv.amount) or 0|entity}</td>
	    	<td width="14%">Tanggal</td>
	    	<td width="1%">:</td>
	    	<td width="35%">${time.strftime('%d %b %Y', time.strptime(adv.date,'%Y-%m-%d')) or ''|entity}</td>
	    </tr>
	    <tr valign="top">
	    	<td width="14%"></td>
	    	<td width="1%"></td>
	    	<td width="35%"><i>( ${convert(adv.amount,adv.currency_id.name) or 0|entity} )</i></td>
	    	<td width="14%">Tipe Pembayaran</td>
	    	<td width="1%">:</td>
	    	<td width="35%">
	    	%if adv.payment_adm == 'cash':
	    	Cash
	    	%elif adv.payment_adm == 'free_transfer':
	    	Non Payment Administration Transfer
	    	%elif adv.payment_adm == 'transfer':
	    	Transfer
	    	%elif adv.payment_adm == 'cheque':
	    	Cheque No. ${ adv.cheque_number or ''}
	    	%else:
	    	-
	    	%endif
	    	</td>
	    </tr>
	    <tr valign="top">
	    	<td width="14%">Memo</td>
	    	<td width="1%">:</td>
	    	<td width="35%" colspan="4">${ adv.name or ''}</td>
	    </tr>
    </table>
    <table class="list_table1" border="1" style="border-collapse:collapse;" width="100%" cellpadding="6">
        <tr style="text-align:center;"><td width="2%">${_("No")}</td><td width="49%" colspan="2">${_("Deskripsi")}</td><td width="49%" colspan="2">${_("Kas")}</td></tr>
        <%
        i = 1
        %>
        %for line in adv.line_ids:
	        <tr class='inv_line'>
	        	<td style="text-align:right;">${i}.</td>
	        	<td style="text-align:left;" colspan="2">${line.name or ''|entity}</td>
	        	<td style="text-align:right;">${line.amount or ''|entity}</td>
	        </tr>
        <%
        i=i+1
        %>
        %endfor
        <tr class='inv_line'>
        	<td style="color:white;">${blank_line([line for line in adv.line_ids])}</td>
        	<td style="text-align:left;" colspan="2"></td>
        	<td style="text-align:right;"></td>
        </tr>
        <tr style="text-align:center;">
        	<td width="2%"></td>
        	<td width="24%">Dibuat Oleh,</td>
        	<td width="25%">Disetujui Oleh,</td>
        	<td width="24%">Penerima Uang,</td>
        </tr>
        <tr>
        	<td style="text-align:right;"><br/><br/><br/><br/></td>
        	<td style="text-align:center;" valign="bottom">${user.name}</td>
        	<td style="text-align:right;"></td>
        	<td style="text-align:left;"></td>
        </tr>
    </table>
    %endfor
</body>
</html>
