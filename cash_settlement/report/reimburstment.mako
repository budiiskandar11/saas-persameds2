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
				padding-top: 10px;
			}
			.paddingright
			{
				padding-right: 10px;
			}
			.perjanjian
			{
				font-size:10px;
				text-align: justify;
    			text-justify: inter-word;
				line-height:12px;
				page-break-inside:avoid; page-break-after:auto;
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
			.border_bottom
			{
				border-bottom: 0.5px solid black;
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
				border-top: 0.5px solid black;
				border-bottom: 0.5px solid black;
			}
			.border_left_right
			{
				border-right: 0.5px solid black;
				border-left: 0.5px solid black;
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
            .font11px
			{
				font-size: 11px;
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
			
         	table.one 
         	{border-collapse:collapse;}
			
		</style>
</head>

    
    <body style="border:0; margin: 0;" onload="subst()">
        %for o in objects  :    
           <table class="header font12px one" style="width: 100%;" cellpadding="3">
            <tr>
               <td class="border_top_bottom border_left_right" rowspan="4" style="width: 20%" padding-left="5px">${helper.embed_company_logo(height="50px",width="auto")|safe}</td>
               <td class="hmid font14px border_top_bottom border_left_right" rowspan="4" style="width: 30%">EXPENSE REPORT
               </td>
               
               <td class="hleft font11px border_top_bottom border_left_right" style="width: 15%">Create</td>
               <td class="hleft font11px border_top_bottom border_left_right" style="width: 15%">${o.date_create}</td>
               	
            </tr>
            <tr>
            		<td class="hleft font11px border_top_bottom border_left_right" style="width: 10%">No</td>
               		<td class="hleft font11px border_top_bottom border_left_right" style="width: 10%">${o.name or ''}</td>
            	</tr>
            	<tr>
            		<td class="hleft font11px border_top_bottom border_left_right" style="width: 10%">Employee</td>
               		<td class="hleft font11px border_top_bottom border_left_right" style="width: 10%">${o.employee_id.name or ''}</td>
            	</tr>
            	<tr>
            		<td class="hleft font11px border_top_bottom border_left_right" style="width: 10%">Department</td>
               		<td class="hleft font11px border_top_bottom border_left_right" style="width: 10%">${o.department_id.name or ''}</td>
            	</tr>
            	<tr>
            		<td colspan="4" class="hleft font11px " style="width: 10%"><br/></td>
               		
            	</tr>
            	<tr>
            		<td colspan="4" class="hleft border_bottom font12px" style="width: 10%">Propose for : ${o.memo or ''}<br/></td>
               		
            	</tr>
            	<tr>
            		<td colspan="4" class="hleft font11px " style="width: 10%"><br/></td>
               		
            	</tr>
        	</table> ${_debug or ''|safe}
        	<table class="header font12px one" style="width: 100%;" cellpadding="3">
        		<tr>
        			<td class="font12px" colspan="6"><b>RINCIAN</b><br/></td>
        		</tr>
        		<tr>
        			<th class="hleft font11px" style="width: 5%">No</th>
        			<th class="hleft font11px" style="width:10%">Date</th>
        			<th class="hleft font11px" style="width:10%">Type</th>
        			<th class="hleft font11px" style="width:45%">Description</th>
        			<th class="hmid font11px" style="width:20%">Amount</th>
        			<th class="hleft font11px" style="width:10%">Check</th>
        		</tr>
        		<% set i=0 %>
        		%for line in o.line_ids :
        			<% set i=i+1%>
        		<tr>
        			<td class="hleft border_top_bottom font11px" style="width: 5%">${i}</td>
        			<td class="hmid border_top_bottom font11px" style="width: 5%">${line.date}</td>
        			<td class="hleft border_top_bottom font11px" style="width: 5%">${(line.tipe_id.name)|title}</td>
        			<td class="hleft border_top_bottom font11px" style="width: 5%">${line.name or ''}</td>
        			<td class="hright border_top_bottom font11px" style="width: 5%">${formatLang(line.subtotal) or formatLang(0)}</td>
        			<td class="hleft border_top_bottom font11px" style="width: 5%"></td>
        		</tr>
        		%endfor
        		<tr>
            		<td colspan="4" class="hright font11px " style="width: 10%">Total</td>
            		<td colspan="1" class="hright font11px " style="width: 10%">${formatLang(o.amount_total) or formatLang(0)}</td>
               		
            	</tr>
            	<tr>
            		<td colspan="6" class="hleft font11px " style="width: 10%"><br/></td>
               		
            	</tr>
        	</table>
        	<table class="header font12px one" style="width: 100%;" cellpadding="3">
        		<tr>
        			<td style="width: 20%;" class="hmid font11px border_top_bottom border_left_right">Submit By</td>
        			<td style="width: 20%;" class="hmid font11px border_top_bottom border_left_right">Submit Approve By</td>
        			<td style="width: 20%;" class="hmid font11px border_top_bottom border_left_right">Submit Checked By</td>
        			<td colspan="2" style="width: 40%;" class="hmid font11px border_top_bottom border_left_right">Payment Info</td>
        		</tr>
        		<tr>
        			<td rowspan="3" style="width: 20%;" class="font11px border_top_bottom border_left_right"></td>
        			<td rowspan="3" style="width: 20%;" class="font11px border_top_bottom border_left_right"></td>
        			<td rowspan="3" style="width: 20%;" class="font11px border_top_bottom border_left_right"></td>
        			<td style="width: 20%;" class="font11px border_top_bottom border_left_right">Payment Date</td>
        			<td style="width: 20%;" class="font11px border_top_bottom border_left_right"></td>
        		</tr>
        		<tr>
        			<td style="width: 20%;" class="font11px border_top_bottom border_left_right">Payment Method</td>
        			<td style="width: 20%;" class="font11px border_top_bottom border_left_right"></td>
        		</tr>
        		<tr>
        			<td style="width: 20%;" class="font11px border_top_bottom border_left_right">Voucher No</td>
        			<td style="width: 20%;" class="font11px border_top_bottom border_left_right"></td>
        		</tr>
        	
        	</table>
    
    %endfor
</body>
</html>
