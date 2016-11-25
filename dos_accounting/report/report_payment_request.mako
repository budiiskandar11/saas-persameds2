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
	%for o in objects:
	 <body style="border:0; margin: 0;" onload="subst()">
        
        <table class="header" style="border-bottom: 0px solid black; width: 100%">
            <tr>
                <td style="width: 20%">${helper.embed_company_logo()|safe}</td>
                <td style="width: 80%">
	                <table class="font12px one" style="border:0; margin: 0;" >
	                	<tr>
	                		<td style="width: 20%"></td>
	                		<td style="width: 30%; padding: 2px; text-align:center;" class="border_black font10px">PAYMENT REQUEST</td>
	                		<td style="width: 20%"></td>
	                		<td style="width: 30%; padding: 2px; text-align:center;" class="border_black font10px" >Due Payment Date</td>
	                	</tr>
	                	<tr>
	                		<td style="width: 20%"></td>
	                		<td style="width: 30%; padding:2px; text-align:center;" class="border_black font10px ">No. ${o.payment_request_number}</td>
	                		<td style="width: 20%"></td>
	                		<td style="width: 30%; padding:2px; text-align:center;" class="border_black font10px"  >${o.date_due  or ''}</td>
	                	</tr>
	                	
		               </table>
	             </td>
            </tr>
            	
        	</table> ${_debug or ''|safe}
        	<table padding-top="20px" cellpadding="2px" width="100%" class="font12px one">
        		<tr>
        		<td><br/>
        		</td>
        		<tr>
        		<tr>
        			<td width="10%">Date</td>
        			<td width="20%">: ${time.strftime('%d %B %Y', time.strptime( o.date_recieved,'%Y-%m-%d'))}</td>
        			<td></td>
        			<td></td>
        			<td colspan="2">Bank Account Details</td>
        			<td></td>
        		</tr>
        		<tr>
        			<td>To</td>
        			<td>: ${o.partner_id.name or ''}</td>
        			<td></td>
        			<td></td>
        			<td colspan="2">Account No : ${o.partner_bank_id.acc_number or ''}</td>
        			<td></td>
        		</tr>
        		<tr>
        			<td></td>
        			<td>: ${o.partner_id.street or ''}, ${o.partner_id.street2 or ''}</td>
        			<td></td>
        			<td></td>
        			<td colspan="2">Beneficiary Name : ${o.partner_bank_id.partner_id.name or ''}</td>
        			<td></td>
        		</tr>
        		<tr>
        			<td></td>
        			<td>:</td>
        			<td></td>
        			<td></td>
        			<td colspan="2">Beneficiary Bank : ${o.partner_bank_id.bank_name or ''}</td>
        			<td></td>
        		</tr>
        		<tr>
        			<td>Description</td>
        			<td colspan="2">: ${o.reference or ''}</td>
        			<td></td>
        			<td></td>
        			<td></td>
        			<td></td>
        		</tr>
        		<tr>
        			<td>Amount</td>
        			<td>: ${ o.currency_id.symbol or ''} ${ formatLang(o.amount_total) or formatLang(0)}</td>
        			<td></td>
        			<td></td>
        			<td></td>
        			<td></td>
        		</tr>
        		<tr>
        			<td>Says</td>
        			<td>: ${(o.amount_string or '')}</td>
        			<td></td>
        			<td></td>
        			<td></td>
        			<td></td>
        		</tr>
        		<tr>
        			<td>Description</td>
        			<td colspan="6">: ${o.comment}</td>
        			<td></td>
        			<td></td>
        			<td></td>
        			<td></td>
        		</tr>
        		<tr>
        		<td><br/></td>
        		</tr>
        	<tr class="font10px">
				<td class=" border_left_right border_bottom border_top font10px" width="15%" align="center">REQUESTOR</td>
		     	<td class=" border_left_right border_bottom border_top" width="15%" align="center">APPROVE</td>
		     	<td class=" border_left_right border_bottom border_top" width="15%" align="center">ACCOUNTING</td>
		     	<td class=" border_left_right border_bottom border_top" width="15%" align="center">TAX</td>
		     	<td class=" border_left_right border_bottom border_top" width="15%" align="center">TREASURY</td>
		     	<td class=" border_left_right border_bottom border_top" width="15%" align="center">PAYMENT APPROVE</td>  	
			</tr>
			<tr>
			   <td class=" border_left_right border_bottom">  
			   		<br></br>
					<br></br>
					<br></br>
					<br></br>
					<br></br>
				</td>
				<td class=" border_left_right border_bottom"></td>
				<td class=" border_left_right border_bottom"></td>
				<td class=" border_left_right border_bottom"></td>
				<td class=" border_left_right border_bottom"></td>
				<td class=" border_left_right border_bottom"></td>
				
				
			<tr  class="font10px">
				<td class=" border_left_right border_bottom" width="15%" align="center"></td>
				<td class=" border_left_right border_bottom" width="15%" align="center"></td>
		     	<td class=" border_left_right border_bottom" width="15%" align="center"></td>
		     	<td class=" border_left_right border_bottom" width="15%" align="center"></td>
		     	<td class=" border_left_right border_bottom" width="15%" align="center"></td>
		     	<td class=" border_left_right border_bottom" width="15%" align="center">Muliadi Setio</td>
		     	
			</tr>
			<tr><td><br/></td></tr>
			<tr  class="font10px">
				<td class=" border_left_right border_bottom border_top" width="15%" align="center">Budget Code</td>
				<td class=" border_left_right border_bottom border_top" width="15%" align="center">Div/Dept</td>
		     	<td class=" border_left_right border_bottom border_top" width="15%" align="center">Major</td>
		     	<td class=" border_left_right border_bottom border_top" width="15%" align="center">Sub</td>
		     	<td class=" border_left_right border_bottom border_top" width="15%" align="left">Budget Used : </td>
		     	<td class=" border_left_right border_bottom border_top" width="15%" align="right"></td>
		     	
			</tr>
				
			<tr  class="font10px">
				<td class=" border_left_right border_bottom" width="15%" align="center"></td>
				<td class=" border_left_right border_bottom" width="15%" align="center"></td>
		     	<td class=" border_left_right border_bottom" width="15%" align="center"></td>
		     	<td class=" border_left_right border_bottom" width="15%" align="center"></td>
		     	<td class=" border_left_right border_bottom" width="15%" align="left">Budget Remain :</td>
		     	<td class=" border_left_right border_bottom" width="15%" align="right"></td>
		     	
			</tr>
        	
        	</table>
       
       %endfor 	
       </body>
   </html>	