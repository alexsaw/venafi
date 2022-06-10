# Python program to demonstrate
# command line arguments
 
import getopt, sys
import ven_account, ven_help, ven_request, ven_certs, create_and_manage_defaults, ven_logs, ven_installs
import json

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]

# Options
options = "hrnf:k:u:p:co:l:v:i:s:"

# Long options
long_options = ["help", "connect", "columns=", "cols=", "disconnect", "verbosity=", "verbose=", "request", "requests", "renew", "logs", "log", "client=", "username=", "user=", "details=", "o=", "ou=", "st=", "c", "r", "organization=", "organizational_unit=", "locality=", "state=", "country=", "sans=", "uri_sans=", "ip_sans=", "dns_sans=", "uri-sans=", "ip-sans=", "dns-sans=", "algorithm=", "key_size=", "key-size=", "key_length=", "key-lenght=", "validity=", "valid_to=", "valid_from=", "valid-to=", "valid-from=", "cn=", "commonname=", "common-name=", "common_name=", "issued_by=", "issuer=", "ca=", "certificate_issuing_template=", "csr=", "file=", "api_key=", "username=", "pass=", "once", "certificates", "certs", "vsatellites=", "scanafi", "applications", "apps", "self-signed", "selfsigned", "eku=", "extended-key-usage=", "show=", "s=", "activity_type=", "activity-type=", "activity_message=", "activity-message=", "message=", "activity=", "criticality=", "admin_clear", "headers", "show_installations", "installs" ]

with open('global_vars.json', 'r') as f:
	global_vars = json.load(f)
	f.close()

	if len(argumentList) != 0:
		try:
			# Parsing argument
			arguments, values = getopt.getopt(argumentList, options, long_options)

			# check if help was called
			for currentArgument, currentValue in arguments:		
				if currentArgument in ("-h", "--help"):
					ven_help.show_help(arguments, values)
					exit()
				elif currentArgument in ("--verbosity", "verbose", "--v", "-v"):
					if global_vars["LOGGED_IN"] == 1:
						ven_account.changeVerbosity(arguments, values)
						exit()
					else:
						ven_help.not_logged_in()
					exit()


			# checking each argument
			for currentArgument, currentValue in arguments:
				if currentArgument in ("-k", "--api_key"):
					ven_account.change_key(arguments, values)
				
				elif currentArgument in ("-r", "--r", "--request"):
					if global_vars["LOGGED_IN"] == 1:
						ven_request.parse_req(arguments, values)
					else:
						ven_help.not_logged_in()
				
				elif currentArgument in ("--connect"):
					# ven_account.pretend_login_with_email_and_password()
					ven_account.connect_with_hard_coded_api_key()


					
				
				elif currentArgument in ("--disconnect"):
					# ven_account.logout()
					ven_account.logout_api_version()
				
				elif currentArgument in ("-n", "--renew"):
					if global_vars["LOGGED_IN"] == 1:
						ven_account.get_creds()
					else:
						ven_help.not_logged_in()

				elif currentArgument in ("--installs"):
					if global_vars["LOGGED_IN"] == 1:
						ven_installs.find(arguments, values)
					else:
						ven_help.not_logged_in()

				elif currentArgument in ("--logs"):
					if global_vars["LOGGED_IN"] == 1:
						ven_logs.get_logs(arguments, values)
					else:
						ven_help.not_logged_in()

				elif currentArgument in ("-c", "--c", "--certificates", "--certs"):
					if global_vars["LOGGED_IN"] == 1:
						ven_certs.find(arguments, values)
					else:
						ven_help.not_logged_in()

				elif currentArgument in ("--vsatellites"):
					print()

				elif currentArgument in ("--scanafi"):
					print()

				elif currentArgument in ("--admin_clear"):
					if global_vars["LOGGED_IN"] == 1:
						create_and_manage_defaults.adminClear()
					else:
						ven_help.not_logged_in()
					


		except getopt.error as err:
			# output error, and return with an error code
			print (str(err))

	else:
		ven_help.no_args()