import os
import ven_output_formats

# size = os.get_terminal_size()


def tabular_output(data_type, data, count, selected_columns, show_cert_installs):
	if data_type == "logs":
		col_desc = ven_output_formats.log_data_format
		color = "\033[36;1m"
	elif data_type == "certs":
		col_desc = ven_output_formats.cert_data_format
		color = "\033[35;1m"
	elif data_type == "installs":
		col_desc = ven_output_formats.installation_data_format
		color = "\033[32;1m"
	r_i = 0
	format_string = ""
	header_titles = []
	total_cols = len(selected_columns)
	for s in selected_columns:
		col_h = col_desc[s]
		length = col_h["format"][0]
		title = col_h["format"][1]
		if r_i == 0:
			format_string +="\033[4m%s{:%s}\033[00m"%(color, length)
		elif r_i == total_cols:
			format_string +="\033[4m%s{:%s}\033[00m"%(color, length)
		else:
			format_string +="  \033[4m%s{:%s}\033[00m"%(color, length)
		header_titles.append(title)
		r_i += 1

	formatted_headers = format_string.format(*header_titles)
	print(formatted_headers)

	rows = {}
	i = 0
	for d in data:
		row = []
		for s in selected_columns:
			data_format = col_desc[s]
			s = str(s)
			if s in d:
				data_length = data_format["format"][0]
				new_length = data_length - 3
				selector = col_desc[s]["selector"]
				if "selectItem" in data_format:
					item = data_format["selectItem"]
					field = d[selector][item]
					field = str(field)
				else:
					field = d[selector]
					field = str(field)
				if "specialFormatting" in data_format:
					params = data_format["specialFormatting"]
					field = field[:params]
					if len(field) >= data_length:
						row.append(field[:new_length]+"...")
					else:
						row.append(field)
				elif len(field) >= data_length:
					row.append(field[:new_length]+"...")
				else:
					row.append(field)
			elif "subsection" in col_desc[s]:
				subsection = col_desc[s]["subsection"]
				data_length = data_format["format"][0]
				new_length = data_length - 3
				selector = col_desc[s]["selector"]
				if selector in d[subsection]:
					field = d[subsection][selector]
					field = str(field)
					if "specialFormatting" in data_format:
						params = data_format["specialFormatting"]
						field = field[:params]	
						if len(field) >= data_length:
							row.append(field[:new_length]+"...")
						else:
							row.append(field)
					elif len(field) >= data_length:
						row.append(field[:new_length]+"...")
					else:
						row.append(field)
				else:
					row.append("--")
			else:
				row.append("--")
		installations = []
		if (data_type == "certs") and (show_cert_installs == True):
			for instance in d["instances"]:
				install = {
					"ipAddress": instance["ipAddress"],
					"certificateSource": instance["certificateSource"]
				}
				installations.append(install)
			row.append(installations)

		rows[i] = row
		i += 1
	

	format_data_string = ""
	for s in selected_columns:
		data_length = col_desc[s]["format"][0]
		format_data_string +="{:%s}  "%data_length
	columns = len(selected_columns)
	for k, v in rows.items():
		print(format_data_string.format(*v))



def csv_output(data_type, data, count, selected_columns, include_headers, show_cert_installs):

	if data_type == "logs":
		col_desc = ven_output_formats.log_data_format
	elif data_type == "certs":
		col_desc = ven_output_formats.cert_data_format
	elif data_type == "installs":
		col_desc = ven_output_formats.installation_data_format

	header_row=""
	if include_headers == True:
		col_i = 0
		for col in selected_columns:
			col_i += 1
			if col_i == len(selected_columns):
				header_row += "%s\n"%col
			else:
				header_row += "%s, "%col

	rows = ""
	for d in data:
		row = ""
		s_i = 0
		for s in selected_columns:
			s_i += 1
			data_format = col_desc[s]
			s = str(s)				
			if s in d:
				data_length = data_format["format"][0]
				new_length = data_length - 3
				selector = col_desc[s]["selector"]
				if "selectItem" in data_format:
					item = data_format["selectItem"]
					field = d[selector][item]
					field = str(field)
				else:
					field = d[selector]
					field = str(field)
				if "specialFormatting" in data_format:
					params = data_format["specialFormatting"]
					field = field[:params]
					if s_i == len(selected_columns):
						row += "%s\n"%field
					else:
						row += "%s, "%field
				else:
					if s_i == len(selected_columns):
						row += "%s\n"%field
					else:
						row += "%s, "%field
			elif "subsection" in col_desc[s]:
				subsection = col_desc[s]["subsection"]
				data_length = data_format["format"][0]
				new_length = data_length - 3
				selector = col_desc[s]["selector"]
				if selector in d[subsection]:
					field = d[subsection][selector]
					field = str(field)
					if "specialFormatting" in data_format:
						params = data_format["specialFormatting"]
						field = field[:params]	
						if s_i == len(selected_columns):
							row += "%s\n"%field
						else:
							row += "%s, "%field
					else:
						if s_i == len(selected_columns):
							row += "%s\n"%field
						else:
							row += "%s, "%field
				else:
					if s_i == len(selected_columns):
						row += "--\n"
					else:
						row += "--, "
			else:
				if s_i == len(selected_columns):
					row += "--\n"
				else:
					row += "--, "
		rows += row

	all_rows = header_row + rows
	print(all_rows)






