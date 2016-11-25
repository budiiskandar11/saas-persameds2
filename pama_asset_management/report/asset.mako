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
				border-top: 0.75px solid black;
				border-bottom: 0.75px solid black;
			}
			.border_left_right
			{
				border-right: 0.75px solid black;
				border-left: 0.75px solid black;
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
<body onload="subst()">
	 %for o in objects:
        <table width="100%" class="border_top_bottom border_left_right one font12px" cellpading="3">
   			<tr>
   				<td rowspan="4" style="width=50%">
   					 ${helper.embed_image('png', o.asset_qr_code,100,100)|safe}
   				</td>
   				<td style="width=50%" class="font10px border_top_bottom border_left_right">${o.company_id.name}</td>
    		</tr>
    		<tr>
    			<td class="font8px border_top_bottom border_left_right">${o.asset_number or ''}</td>
    		</tr>
    		<tr>
    			<td class="font8px border_top_bottom border_left_right">${o.name or ''}</td>
    		</tr>
    		<tr>
    			<td class="font8px border_top_bottom border_left_right">${time.strftime('%d %b %Y', time.strptime(o.purchase_date,'%Y-%m-%d'))}</td>
    		</tr>
    	</tabel>
    %endfor
</body>
</html>
