import getopt, sys
import json
import requests
import os
import ven_help
import ven_display_data


def find(arguments, values):

	include_headers = False

	show_cert_installs = False

	search_object = {}

	operands = []

	expression = {
		"operator":"AND"
	}

	default_search = {
		"field": "subjectCN",
		"operator": "FIND",
		"value": "*"
	}

	ordering = {
	    "orders": [
	        {
	            "direction": "DESC",
	            "field": "certificatInstanceModificationDate"
	        }
	    ]
	}

	paging = {
		"pageNumber": 0,
		"pageSize": 50
	}

	default_columns = [
		"subjectCN",
		"id",
		"totalInstanceCount",
		"selfSigned",
		"validityEnd",
		"subjectC",
		"certificateStatus",
		"encryptionType",
		"keyStrength",
		"subjectOU",
		"issuerCN"

	]

	selected_columns = []

	eku_options = {
		1: ["Server Authentication", "1.3.6.1.5.5.7.3.1"],
		2: ["Client Authentication", "1.3.6.1.5.5.7.3.2"],
		3: ["Code Signing", "1.3.6.1.5.5.7.3.3"],
		4: ["Email Protection", "1.3.6.1.5.5.7.3.4"],
		5: ["Time Stamping", "1.3.6.1.5.5.7.3.8"],
		6: ["OSCP Signing", "1.3.6.1.5.5.7.3.9"],
		7: ["IPSec Internet Key Echange", "1.3.6.1.5.5.7.3.17"],
		8: ["IPSec IKE Intermediate", "1.3.6.1.5.5.8.2.2"]
	}

	column_options = {
		1: "subjectCN",
		2: "fingerprint",
		3: "validityEnd",
		4: "id",
		5: "certificateStatus",
		6: "encryptionType",
		7: "subjectL",
		8: "subjectOU",
		9:	"subjectST",
		10:	"keyStrength",
		11:	"selfSigned",
		12: "issuerCN",
		13: "totalInstanceCount",
		14: "extendedKeyUsage",
		15: "subjectC"
	}

	issuer_options = ["Amazon","Comodo","Cybertrust","DigiCert","Entrust","GDCA","GlobalSign","Go Daddy","Google","IdenTrust","Intermediate ca 1","Izenpe","Keynectis","Let's Encrypt","Microsoft","QuoVadis","Self-signed","SSL.com","StartCom","Swisscom","SwissSign","Symantec","Trustwave","WISeKey","WoSign"]


	try:
		for arg, val in arguments:
			# if arg == "-d" or "--details=":
			# 	pass
			if arg in ("-o", "--o", "--organization"):
				print("• searches for \"organization\" are not currently supported")
			elif arg in ("--show", "--s", "-s"):
				paging = {
					"pageNumber": 0,
					"pageSize": int(val)
				}
			elif arg in ("--ou", "--organizational_unit"):
				ou = {
					"field": "subjectOU",
					"operator": "FIND",
					"value": val
				}				
				operands.append(ou)
			elif arg in ("-l", "--locality"):
				l = {
					"field": "subjectL",
					"operator": "FIND",
					"value": val
				}				
				operands.append(l)
			elif arg in ("--st", "--state"):
				st = {
					"field": "subjectST",
					"operator": "FIND",
					"value": val
				}				
				operands.append(st)
			elif arg in ("-c", "--c", "--country"):
				c = {
					"field": "subjectC",
					"operator": "FIND",
					"value": val
				}				
				operands.append(c)
			elif arg in ("--cn", "--common_name", "--commonname", "--common-name"):
				cn = {
					"field": "subjectCN",
					"operator": "FIND",
					"value": val
					}
				operands.append(cn)
			elif arg in ("--ip-sans", "--ip_sans"):
				print("• searches for \"IP SANS\" are not currently supported")
			elif arg in ("--dns-sans", "--dns_sans"):
				print("• searches for \"DNS SANS\" are not currently supported")
			elif arg in ("--uri-sans", "uri_sans"):
				print("• searches for \"URI SANS\" are not currently supported")
			# if arg in ("--sans"):
			# 	#put the generic sans into the dns sans category, but not if it was explicitly added already
			# 	if val not in csr_data["subjectAlternativeNamesByType"]["dnsNames"]:
					
			elif arg in ("--algorithm", "-a"):
				algo = {
					"field": "encryptionType",
					"operator": "FIND",
					"value": val
				}		
				operands.append(algo)
			elif arg in ("--key-size", "--key_size", "--key-length", "--key_length"):
				key_size = {
					"field": "keyStrength",
					"operator": "EQ",
					"value": int(val)
				}				
				operands.append(key_size)		

			elif arg in ("--self-signed", "--selfsigned"):
				self_signed = {
					"field": "selfSigned",
					"operator": "FIND",
					"value": True
				}				
				operands.append(self_signed)	

			elif arg in ("--eku", "--extended-key-usage"):
				eku = {
					"field": "extendedKeyUsage",
					"operator": "MATCH",
					"values": []
				}

				if val[0] == "[":
					val = val[1:-1]
					val = val.split(",")
					for v in val:
						for key, value in eku_options.items():
							if v == str(key) or v == value[0]:
								eku["values"].append(value[1])
				else:
					for key, value in eku_options.items():
						if val == str(key) or val == value[0]:
							eku["values"].append(value[1])

				operands.append(eku)	

			elif arg in ("-i", "--issued_by", "--issuer"):
				issuers = {
					"field": "issuerCN",
					"operator": "FIND",
					"values": []
				}
				if val[0] == "[":
					val = val[1:-1]
					val = val.split(",")
					for v in val:
						v = v.strip()
						# for value in issuer_options:
						# if v == value:
						issuers["values"].append(v)
				else:
					# for value in issuer_options:
						# if val == value:
					issuers["values"].append(val)
				
				operands.append(issuers)	

			elif arg in ("--columns", "--cols"):
				
				if val == "all":
					for k, v in column_options.items():
						selected_columns.append(v)
				elif val[0] == "[":
					val = val[1:-1]
					val = val.split(",")
					for v in val:
						v = v.strip()
						for key, value in column_options.items():
							if v == str(key) or v == value:
								selected_columns.append(value)
				else:
					for key, value in column_options.items():
						if val == str(key) or val == value:
							selected_columns.append(value)
			elif arg in ("--headers"):
				include_headers = True

			elif arg in ("--show_installations"):
				show_cert_installs = True

			# elif arg == "--validity":
			# 	pass
			# elif arg == "--valid-to" or "--valid_to":
			# 	pass
			# elif arg == "--valid-from" or "--valid_from":
			# 	pass
			# elif arg == "--cit" or "--certificate_issuing_template":
 			#	pass

	except getopt.error as err:
		# output error, and return with an error code
		print (str(err))	

	if len(operands) == 0:
		expression["operands"] = default_search
	else:
		expression["operands"] = operands
		search_object["expression"] = expression

	search_object["ordering"] = ordering
	search_object["paging"] = paging

	payload = json.dumps(search_object)

	if len(selected_columns) == 0:
		columns_for_table = default_columns
	else:
		columns_for_table = selected_columns


	with open('global_vars.json', 'r') as f:
		global_vars = json.load(f)
	f.close()

	if global_vars["VERBOSITY"] >= 1:
		os.system("clear")
		print("\n\n\033[35;1mGetting your certificates. One moment...\033[00m")

	url='https://api.venafi.cloud/outagedetection/v1/certificatesearch'
	headers = {
	  'tppl-api-key': global_vars["API_KEY"],
	  'accept': 'application/json',
	  'Content-Type': 'application/json'
	}
	response = requests.request("POST", url, headers=headers, data=payload)
	data = response.json()

	if global_vars["VERBOSITY"] >= 1:
		os.system("clear")
		if data["count"] >= 1:
			print("\n")
			print("\033[35;1mFound %s Certificates matching your search:\033[00m \n"%data["count"])
			ven_display_data.tabular_output("certs", data["certificates"], data["count"], columns_for_table, show_cert_installs)
		else:
			print("\n\033[35;1mFound %s Certificates matching your search:\033[00m"%data["count"])
			print("\033[35;1mAdjust your search terms and try again or get help searching for certificates by typeing \"venafi -h -c\"\033[00m\n\n")
	else:
		ven_display_data.csv_output("certs", data["certificates"], data["count"], columns_for_table, include_headers, show_cert_installs)


# from tal those were 2 main points - cert + ip \ app \ owner infor and ability to pipe the result for a more complicated queries or actions


