import os
import create_and_manage_defaults
import getopt, sys
import ven_account, ven_help, ven_request
import json
import requests
import time

def parse_req(arguments, values):

	# create variables from parameters
	csr_data = {
       	"commonName": None,
        "organization": None,
        "organizationalUnits": [],
        "locality": None,
        "state": None,
        "country": None,
        "subjectAlternativeNamesByType": {
            "dnsNames": [],
            "rfc822Names": [],
            "ipAddresses": [],
            "uniformResourceIdentifiers": []
        },
        "keyTypeParameters": {
            "keyType": "RSA",
            "keyLength": 2048
        }
    }

	request_failure_messages = []

	try:
		for arg, val in arguments:
			if len(val) != 0:
				# if arg == "-d" or "--details=":
				# 	pass
				if arg in ("-o", "--o", "--organization"):
					csr_data["organization"] = val
				elif arg in ("--ou", "--organizational_unit"):
					csr_data["organizationalUnits"].append(val)
				elif arg in ("-l", "--l", "--locality"):
					csr_data["locality"] = val
				elif arg in ("--st", "--state"):
					csr_data["state"] = val
				elif arg in ("-c", "--c", "--country"):
					csr_data["country"] = val
				elif arg in ("--cn", "--common_name", "--commonname", "--common-name"):
					csr_data["commonName"] = val
				elif arg in ("--ip-sans", "--ip_sans"):
					# csr_data["subjectAlternativeNamesByType"]["ipAddresses"].append(val)
					request_failure_messages.append("Venafi CLI does not currently support IP Sans.")
				elif arg in ("--dns-sans", "--dns_sans"):
					csr_data["subjectAlternativeNamesByType"]["dnsNames"].append(val)
				elif arg in ("--uri-sans", "uri_sans"):
					# csr_data["subjectAlternativeNamesByType"]["uniformResourceIdentifiers"].append(val)
					request_failure_messages.append("Venafi CLI does not currently support URI Sans.")
				if arg in ("--sans"):
					#put the generic sans into the dns sans category, but not if it was explicitly added already
					if val not in csr_data["subjectAlternativeNamesByType"]["dnsNames"]:
						csr_data["subjectAlternativeNamesByType"]["dnsNames"].append(val)
				elif arg in ("--algorithm", "-a"):
					if val != "RSA":
						request_failure_messages.append("Venafi CLI currently only supports the RSA algorithm.")
					else:
						csr_data["keyTypeParameters"]["keyType"] = val
				elif arg in ("--key-size", "--key_size", "--key-length", "--key_length"):
					if val in ("2048", "4096", "3082"):
						csr_data["keyTypeParameters"]["keyLength"] = int(val)
				elif arg in ("--details"):
					val = json.loads(val)
					for key, value in val.items():
						if key in ("ou", "org unit", "organizational_unit"):
							csr_data["organizationalUnits"].append(value)
						elif key in ("o", "org", "organization"):
							csr_data["organization"] = value
						elif key in ("l", "locality"):
							csr_data["locality"] = value
						elif key in ("s", "state"):
							csr_data["state"] = value
						elif key in ("c", "country"):
							csr_data["country"] = value
						elif key in ("cn", "common_name", "commonname", "common-name"):
							csr_data["commonName"] = value
						elif key in ("dns", "dns-sans", "dns_sans"):
							csr_data["subjectAlternativeNamesByType"]["dnsNames"].append(value)
					# elif val in ("P256", "P512", "P128"):
					# 	csr_data["keyTypeParameters"]["keyCurve"] = val

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

	# check is there is at least a CN or on one of the SANS fields filled in my user
	if csr_data["commonName"] != None or len(csr_data["subjectAlternativeNamesByType"]["dnsNames"]) or len(csr_data["subjectAlternativeNamesByType"]["ipAddresses"]) or len(csr_data["subjectAlternativeNamesByType"]["uniformResourceIdentifiers"]) or len(csr_data["subjectAlternativeNamesByType"]["rfc822Names"]) != 0:

		csr_data = json.dumps(csr_data)

		# get default app and cit and other info if required for request
		with open('global_vars.json', 'r') as f:
			global_vars = json.load(f)
			f.close()

			if global_vars["VERBOSITY"] >= 1:
				# make request with csr inputs
				os.system("clear")
				print("\n\n\033[96mConnecting to Certificate Authority...\033[00m")

			makeRequest(csr_data, request_failure_messages)



def makeRequest(csr_data, request_errors):

	# get default app and cit and other info if required for request
	with open('global_vars.json', 'r+') as f:
		global_vars = json.load(f)

	if global_vars["VERBOSITY"] >= 1:
		#make the request for the certificate with the parameters provided by parse_req()
		time.sleep(.5)
		print("\n\n\033[96mMaking request...\033[00m")

	payload = """
	{
	  \"isVaaSGenerated\": true,
	  \"csrAttributes\": %s,
	  \"applicationId\": \"%s\",
	  \"certificateIssuingTemplateId\": \"%s\",
	  \"certificateOwnerUserId\": \"%s\",
	  \"applicationServerTypeId\": \"784938d1-ef0d-11eb-9461-7bb533ba575b\",
	  \"validityPeriod\": \"P90D\",
	  \"existingCertificateId\": null
	}
	"""%(csr_data, global_vars["DEFAULT_APP"], global_vars["DEFAULT_TEMPLATE_ID"], global_vars["OWNER_ID"] )


	url='https://api.venafi.cloud/outagedetection/v1/certificaterequests'

	headers = {
	  'tppl-api-key': global_vars["API_KEY"],
	  'accept': 'application/json',
	  'Content-Type': 'application/json'
	}
	response = requests.request("POST", url, headers=headers, data=payload)


	data = response.json()


	if global_vars["VERBOSITY"] >= 1:
		print("\n\n\033[32mCertificate Request Sucessful!")
		print("View and download your certificates here:\033[00m")
		print("\033[4m\033[1;34mhttps://ui.venafi.cloud/certificate-issuance/certificates-inventory/application/%s\033[00m\n\n"%global_vars["DEFAULT_APP"])

	else:
		print(data)
