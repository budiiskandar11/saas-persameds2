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
%for ot in get_overtime(e.id, o.date):
	%if is_holiday(ot.time_start)==True:
		<% dur_x15 = 0.0 %>
		${dur_x15}
		<% dur_x2 = 0.0 %>
		${dur_x2}
		%if ot.duration<=7:
			<% dur_hol_x2 = ot.duration %>
		%else:
			<% dur_hol_x2 = 7.0 %>
		%endif
		
		%if ot.duration<=7:
			<% dur_hol_x3 = 0.0 %>
			${dur_hol_x3}
		%else:
			<% dur_hol_x3 = 1.0 %>
			${dur_hol_x3}
		%endif
		
		%if ot.duration<=8:
			<% dur_hol_x4 = 0.0 %>
			${dur_hol_x4}
		%else:
			<% dur_hol_x4 = ot.duration - 8 %>
			${dur_hol_x4}
		%endif
		
		<% dur_total = ot.duration %>
		${dur_total}
		
		<% paid_x15 = 0.0 %>
		${paid_x15}
		
		<% paid_x2 = 0.0 %>
		${paid_x2}
		
		<% paid_hol_x2 = dur_hol_x2 * 2 %>
		${paid_hol_x2}
		
		<% paid_hol_x3 = dur_hol_x3 * 3 %>
		${paid_hol_x3}
		
		<% paid_hol_x4 = dur_hol_x4 * 4 %>
		${paid_hol_x4}
		
		<% paid_hol_tot = paid_hol_x2+paid_hol_x3+paid_hol_x4 %>
		${paid_hol_tot}
		
	%else:
		<% dur_x15 = 1.0 %>
		${dur_x15}
		
		<% dur_x2 = ot.duration-1%>
		${dur_x2}
		
		<% dur_hol_x2 = 0.0 %>
		${dur_hol_x2}
		
		<% dur_hol_x3 = 0.0 %>
		${dur_hol_x3}
		
		<% dur_hol_x4 = 0.0 %>
		${dur_hol_x4}
		
		<% dur_total = ot.duration %>
		${dur_total}
		
		<% paid_x15 = dur_x15 * 1.5 %>
		${paid_x15}
		
		<% paid_x2 = dur_x2 * 2 %>
		${paid_x2}
		
		<% paid_hol_x2 = 0.0 %>
		${paid_hol_x2}

		<% paid_hol_x3 = 0.0 %>
		${paid_hol_x3}

		<% paid_hol_x4 = 0.0 %>
		${paid_hol_x4}

		<% paid_hol_tot = paid_x15 + paid_x2 %>
		${paid_hol_tot}
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
	<% nomor+=1 %>
%endfor
	<tr>
		<td class="center bold" colspan="5">Total</td>
		<td class="center sum">${sum_dur_x15}</td>
		<td class="center sum">${sum_dur_x2}</td>
		<td class="center sum">${sum_dur_hol_x2}</td>
		<td class="center sum">${sum_dur_hol_x3}</td>
		<td class="center sum">${sum_dur_hol_x4}</td>
		<td class="center sum">${sum_dur_total}</td>
		<td class="center sum">${sum_paid_x15}</td>
		<td class="center sum">${sum_paid_x2}</td>
		<td class="center sum">${sum_paid_hol_x2}</td>
		<td class="center sum">${sum_paid_hol_x3}</td>
		<td class="center sum">${sum_paid_hol_x4}</td>
		<td class="center sum">${sum_paid_hol_tot}</td>
	</tr>
