 <!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
	<head>
	<script>
            function subst() {
            var vars={};
            var x=document.location.search.substring(1).split('&');
            for(var i in x) {var z=x[i].split('=',2);vars[z[0]] = unescape(z[1]);}
            var x=['frompage','topage','page','webpage','section','subsection','subsubsection'];
            for(var i in x) {
            var y = document.getElementsByClassName(x[i]);
            for(var j=0; j<y.length; ++j) y[j].textContent = vars[x[i]];
                }
            }
        </script>
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
				border-left : 1px solid black;
				border-right : 1px solid black;
				border-top : 1px solid black;
				background-color: lightGrey
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
				border-top: 1px solid black;
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
			.font8px
			{
				font-size: 8px;
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
        </style>
    </head>
    <body style="border:0; margin: 0;" onload="subst()">
      <table style="width: 100%" class="border_top_bottom border_left_right">  
       <tr>
       	<td>
        %for o in objects  :    
        <table cellpadding="3" class="header" style="border-bottom: 0px solid black">
           <tr>
                <td height="42" width="42">${helper.embed_company_logo(width=90, height=auto)|safe}</td>
                <td >
	                <table class="font12px" style="border:0; margin: 0;" >
	                	<tr>
	                		<td style="width: 80%" class="font14px"><b>FORM PURCHASE REQUISITION</b></td>
	                	</tr>
	                	<tr>
	                		<td style="width: 85%"><b>PT ENERGIA PRIMA NUSANTARA<b/></td>
	                	</tr>
	                	
		               </table>
	             </td>
            </tr>
            
          </table>
       
        
          <table class="font12px one" cellpadding="2" style="width: 100%">
          	<tr>
          		<td width ="20%" >Nomor PR</td>
          		<td width ="80%" colspan="8">: ${o.name}</td>
          	</tr>
          	<tr>
          		<td colspan="9"class="border_bottom"></td>
          		
          	</tr>
          	<tr>
          		<td width ="20%">Nama Kebutuhan</td>
          		<td width ="80%" colspan="8">:</td>
          	</tr>
          	<tr>
          		<td width ="20%">Jenis Kebutuhan</td>
          		<td width ="15%">: 1. Pengadaan</td>
          		%if o.type == 'asset'
          			<td  width ="5%" class="border_top_bottom border_left_right hmid">X</td>
          		%elif o.type == 'barang'
          			<td  width ="5%"class="border_top_bottom border_left_right hmid">X</td>
          		%else
          			<td  width ="5%"class="border_top_bottom border_left_right"></td>
          		%endif
          		
          		<td>Barang</td>
          		
          		<td width ="15%">2. Budget Code</td>
          		%if o.type != 'asset'
          		<td width ="5%" class="border_top_bottom border_left_right hmid">X</td>
          		%else 
          		<td width ="5%" class="border_top_bottom border_left_right"></td>
          		%endif 
          		
          		<td>Opex</td>
          		<td  width ="5%" class="border_top_bottom border_left_right"></td>
          		<td>Budgeted</td>
          		
          	</tr>
          	<tr>
          		<td class="font8px"><i>(beri tanda silang sesuai kebutuhan)<i></td>
          		<td></td>
          		%if o.type == 'jasa'
          			<td  width ="5%"class="border_top_bottom border_left_right hmid">X</td>
          		%else
          			<td  width ="5%"class="border_top_bottom border_left_right"></td>
          		%endif
          		
          		<td width ="10%">Jasa</td>
          		<td></td>
          		%if o.type == 'asset'
          		<td width ="5%" class="border_top_bottom border_left_right hmid" >X</td>
          		%else 
          		<td width ="5%" class="border_top_bottom border_left_right"></td>
          		%endif
          		<td>Capex</td>
          		<td width ="5%" class="border_top_bottom border_left_right"></td>
          		<td>Unbudgeted</td>
          	</tr>
          	<tr>
          		<td></td>
          		<td></td>
          		%if o.type == 'umum'
          			<td  width ="5%"class="border_top_bottom border_left_right hmid">X</td>
          		%else
          			<td  width ="5%"class="border_top_bottom border_left_right"></td>
          		%endif
          		<td width ="10%">Lain-lain</td>
          		<td></td>
          		<td></td>
          		<td></td>
          		<td></td>
          		<td></td>
          	</tr>
          	<tr>
          		<td width="20%" >Rincian Kebutuhan</td>
          		<td width ="40%" colspan="3">:</td>
          		
          		<td width ="20%" >Tanggal Permintaan</td>
          		<td width ="40%" colspan="4">: ${o.request_date or ''}</td>
          		
          	</tr>
          
          	<tr>
          		<td colspan="9">
          			 <table class="font12px one" cellpadding="2" style="width: 100%">
          				<tr>
          					<th>No</th>
          					<th>Uraian Kebutuhan</th>
          					<th>Jumlah</th>
          					<th>Estimasi Harga</th>
          					<th>Total</th>
          					<th>Spesifikasi Detail</th>
          				</tr>
          				%for m in o.line_ids :
          				<tr>
          					<td class="border_left_right"></td>
          					<td class="border_left_right">${m.name or ''}</td>
          					<td class="border_left_right hmid">${m.product_qty or '0'} ${m.product_uom_id.name or ''}</td>
          					<td class="border_left_right hright">${m.estimate_price or '0'}</td>
          					<td class="border_left_right hright"></td>
          					<td class="border_left_right"></td>
          				</tr>
          				%endfor
          				<tr>
          					<td class="border_left_right border_top_bottom" colspan="4">Total</td>
          					<td class="border_left_right border_top_bottom"></td>
          					<td class="border_left_right border_top_bottom"></td>
          					
          				</tr>
          				<tr>
          					<td colspan="6" class="font8px"><i>(Lampirkan gambar/detail spek yang diminta jika ada)</i></td>
          					
          					
          				</tr>
          			</table>
          		
          		
          		</td>
          		
          	</tr>
          	<tr>
          		<td width="20%" ></td>
          		<td colspan="5"></td>
          		<th colspan="2">Requestor</th>
          		<td></td>
          		
          	</tr>
          	<tr>
          		<td width="20%" >Diminta Oleh</td>
          		<td colspan="5">: ${o.request_by.name}</td>
          		<td class ="border_left_right" colspan="2"></td>
          		<td></td>
          		
          	</tr>
          	<tr>
          		<td width="20%" >NRP</td>
          		<td colspan="5">: ${o.request_by.nrp or ''} / ${o.request_by.department_id.name or ''} </td>
          		<td class ="border_left_right"  colspan="2"></td>
          		<td></td>
          		
          	</tr>
          	<tr>
          		<td width="20%" >Jabatan</td>
          		<td colspan="5">: ${o.request_by.job_id.name or ''}</td>
          		<td class ="border_left_right" colspan="2"></td>
          		<td></td>
          		
          	</tr>
          	<tr>
          		<td width="20%" ></td>
          		<td colspan="5"></td>
          		<td class ="border_left_right border_top_bottom font10px one"  colspan="2">Nama : ${o.request_by.name or ''}</td>
          		<td></td>
          		
          	</tr>
          	<tr>
          		<td width="20%" ></td>
          		<td colspan="5"></td>
          		<td class ="border_left_right border_top_bottom font10px one"  colspan="2">Tanggal : ${o.request_date or ''}</td>
          		<td></td>
          		
          	</tr>
          	<tr>
          		<td colspan="9"class="border_bottom"></td>
          		
          	</tr>
          	<tr>
          		<td colspan="9">
	          		<table class="font12px one" cellpadding="2" style="width: 100%;" border="1px">
	          			<tr>
	          				<th align="left">Alasan Permintaan</th>
	          			</tr>
	          			<tr>
	          				<td>${o.propose or ''}
	          					<br></br>
	          				
	          				</td>
	          			</tr>
	          		</table>
          		</td>
          	</tr>
          	<tr>
          		<td colspan="9">
          		<table class="font12px one" cellpadding="2" style="width: 100%">
          			<tr>
          				<td width="40%"></td>
          				<th colspan="4">Mengetahui/Menyetujui</th>
          			</tr>
          			<tr>
          				<td width="40%"></td>
          				<th width="15%">Sec. Head Terkait</th>
          				<th width="15%">Dept. Head Terkait</th>
          				<th width="15%">Board of Director</th>
          				<th width="15%">Presiden Director</th>
          			</tr>
          			<tr>
          				<td  width="40%"></td>
          				<td class="border_left_right" width="15%">
          				<br/>
          				<br/>
          				<br/>
          				</td>
          				<td class="border_left_right" width="15%"></td>
          				<td class="border_left_right" width="15%"></td>
          				<td class="border_left_right" width="15%"></td>
          			</tr>
          			
          			<tr>
          				<td width="40%"></td>
          				<td class="border_left_right border_top_bottom font10px " width="15%">Nama</td>
          				<td class="border_left_right border_top_bottom font10px " width="15%">Nama</td>
          				<td class="border_left_right border_top_bottom font10px " width="15%">Nama</td>
          				<td class="border_left_right border_top_bottom font10px " width="15%">Nama</td>
          			</tr>
          			<tr>
          				<td width="40%"></td>
          				<td class="border_left_right border_top_bottom font10px " width="15%">Tanggal</td>
          				<td class="border_left_right border_top_bottom font10px " width="15%">Tanggal</td>
          				<td class="border_left_right border_top_bottom font10px " width="15%">Tanggal</td>
          				<td class="border_left_right border_top_bottom font10px " width="15%">Tanggal</td>
          			</tr>
          			
          		</table>
          		</td>
          	</tr>
          	<tr>
          		<td colspan="9">
	          		<table class="font12px one" cellpadding="2" style="width: 100%;" border="1px">
	          			<tr>
	          				<th align="left">Alasan Penolakan</th>
	          			</tr>
	          			<tr>
	          				<td>${o.reject_reason or ''}
	          					<br></br>
	          				
	          				</td>
	          			</tr>
	          		</table>
          		</td>
          	</tr>
          	
          	
          </table>
          
          
          
      %endfor
       </td>
        </tr>
      </table>	
       </body>
   </html>
  