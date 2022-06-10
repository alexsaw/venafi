import os
import getopt, sys

# message to show if user uses the -h or --help flag without any other arguments. AKA the general help
def show_help(arguments, values):

	try:
		for arg, val in arguments:
			if len(arguments) != 1:
				if arg in ("-r", "--r", "--request", "--requests"):
					request_help()
				elif arg in ("-c", "--c", "--certificates", "--certs"):
					certs_help()
				elif arg in ("--logs", "--log"):
					logs_help()
				elif arg in ("--installs"):
					installs_help()
			else:
				general_help()

	except getopt.error as err:
		# output error, and return with an error code
		print (str(err))


def banner():
	print( """\033[96m _    __                 _____ 
| |  / /__  ____  ____ _/ __(_)
| | / / _ \/ __ \/ __ `/ /_/ / 
| |/ /  __/ / / / /_/ / __/ /  
|___/\___/_/ /_/\__,_/_/ /_/
\033[00m""")

def help_header():
	print( """Run "venafi -h" or "venafi --help" for a list of options.

• In-browser CLI labs and tutorials at \033[96mhttps://devhub.venafi.com/labs\033[00m
• Read more about each command at \033[96mhttps://devhub.venafi.com/documentation\033[00m
	""")


def request_help():
	os.system("clear")
	banner()
	help_header()
	print("""\033[96mCERTIFICATE REQUEST HELP:\033[00m

	-t, --test		\tcoming soon. makes the request as a test and does not result 
					in an issued
					certificate. This will test that the request that was made
					is possible with the entered paramteres, testing the CA and
					the Venafi connections. e.g. "venafi -r --cn="acme.org" -t"

	-r, --request		\trequest a certificate

These parameters can be used to make a certificate request in addition to the "-r" or "--request":

	--details		\taccept an object of certificate parameters
					e.g. --details='{"dns_sans":"www.acme.org","ou":"Marketing","c":"US"}'

	--ca			\tthe Certificate Authority (CA) that will be used to issue
					the certificate in this request

	--cn			\tthe Common Name (CN) on the requested certificate

	--dns_sans		\tthe Subject Alternative Names (SANS) on the requested
					certificate in the format
					of a DNS name such as --dns_sans="*.acme.com" 
					or --dns_sans="[www.acme.com, www.acme.org]"

	--uri_sans		\tthe SANS on the requested certificate in the format
					of a DNS name such as --dns_sans="www.acme.com/requests/001" 

	--ip_sans		\tthe SANS on the requested certificate in the format
					of a DNS name such as --dns_sans="192.168.100.10" 

	--o, --l, --s, --ou	\tthe descriptive parts of the Distinguished Name (DN)
					e.g. --ou="Marketing" or --s="US"

	-d=, --details=		\tan object containing all of the certificate description
					that is possible with the above arguments.
					e.g. --details="{"cn":"www.acme.org", "ou":"Marketing"}"
	""")

def certs_help():
	os.system("clear")
	banner()
	help_header()
	print("""\033[96mCERTIFICATE SEARCH HELP:\033[00m
These parameters can be used to make a specifc certificate search in addition to the "-c", "--certs" or "--certificates":

	--ca, --issuer		\tthe Certificate Authority (CA) that will be used to issue
					the certificate in this request

	--cn			\tthe Common Name (CN) on the requested certificate


	--dns_sans		\tthe Subject Alternative Names (SANS) on the requested
					certificate in the format
					of a DNS name such as --dns_sans="*.acme.com" 
					or --dns_sans="www.acme.com"

	--uri_sans		\tthe SANS on the requested certificate in the format
					of a DNS name such as --dns_sans="www.acme.com/requests/001" 

	--ip_sans		\tthe SANS on the requested certificate in the format
					of a DNS name such as --dns_sans="192.168.100.10" 

	--o, --l, --s, --ou	\tthe descriptive parts of the Distinguished Name (DN)
					e.g. --ou="Marketing" or --s="US"

	--eku, --extended-key-usage	finds certificates based on the following types:
					Server Authentication (1), Client Authentication (2), 
					Code Signing (3), Email Protection (4), Time Stamping (5),
					OSCP Signing (6), IPSec Internet Key Echange (7), or
					IPSec IKE Intermediate (8) (e.g. --eku="Code Signing" or 
					--extended-key-usage="[3, 2, 6]")

	--algorithm		\tcertificate's public key algorithm ("RSA" or "EC")

	--key_size, --key_length\tsearch for the key size for the certificate. for
					RSA: 1024, 2048 and 4096. For EC: P128, P256 and P512

	--show			\tchoose how many rows you want to generate with your query. 
					From 0 to 1000 (e.g. venafi --logs -e="App" --show="300")

	--columns, --cols	\tselect the columns you want to be visible from the options below.
					You can enter an individual value or an array. Use the number or string.
					(e.g. --cols="["message", 6, 4]" or --cols="all")

					1: subjectCN, 2: fingerprint, 3: validityEnd, 4: id, 5: certificateStatus,
					6: encryptionType, 7: subjectL, 8: subjectOU, 9: subjectST, 10: keyStrength,
					11: selfSigned, 12: issuerCN, 13: totalInstanceCount, 14: extendedKeyUsage

	--headers		\tAdjust the CSV output format when verbosity is set to 0.
					This allows you to pipe output to another platform with the headers.
					e.g. --certs --cols="[1,2,3]" --show="300" --headers

	""")


def logs_help():
	os.system("clear")
	banner()
	help_header()
	print("""\033[96mEVENT LOG HELP:\033[00m
These parameters can be used to make a specifc event log searches in conjunction with the "--log" or "--logs" operator:

	--activity_type		\tfilter logs by a single Activity Type (e.g. --activity_type="1").
					Use the Activity Type name or the number identifier:

					1: Authentication, 2: VSatellites, 3: Notifications, 4: Certificates,
					5: User Security, 6: Applications

	--activity		\tfilter logs by a single Activity (e.g. --activity="Logout").
					Use the Activity Type name or the number identifier:
					
					1: Login Succeeded, 2: Logout, 3: Login Failed, 4: Issuing Template Created,
					5: Application Created, 6: CSR Generated, 7: Certificate Issued, 8: Notification sent,
					9: VSatellite Pairing Code Created, 10: VSatellite Paired, 11: VSatellite Deleted,
					12: Issuing Template Updated, 13: ApiKey Rotation Requested, 14: ApiKey Deleted

	--message		\tsearches the text of log messages for partial or exact matches
					(e.g. --message="deleted")

	--criticality		\tfinds events with either a criticality of 0 or 1 
					(e.g. --criticality="0")

	--client		\tsearches for the partial or complete ip address of the client that
					initiated the log event (e.g. --client="192.168")

	--user, --username	\tsearches for the partial or complete username of the account
					that initiated the log event (e.g. --username="tammy")

	--show			\tchoose how many rows you want to generate with your query. 
					From 0 to 1000 (e.g. venafi --logs -e="App" --show="300")

	--columns, --cols	\tselect the columns you want to be visible from the options below.
					You can enter an individual value or an array. Use the number or string.
					(e.g. --cols="["message", 6, 4]" or --cols="all")

					1: activityName, 2: activityType, 3: message, 4: activityDate, 
					5: clientIpAddress, 6: username, 7: criticality

	--headers		\tAdjust the CSV output format when verbosity is set to 0.
					This allows you to pipe output to another platform with the headers.
					e.g. --logs --cols="[1,2,3]" --show="300" --headers
	""")

def installs_help():
	os.system("clear")
	banner()
	help_header()
	print("""\033[96mINSTALLATIONS HELP:\033[00m
These parameters can be used to find installations for certificates matching up to two 
criteria by using the "--installs" operator:

	--show			\tchoose how many certificates you want to return for your query. 
					From 0 to 1000 (e.g. venafi --installs --show="2")

	--columns, --cols	\tselect the columns you want to be visible from the options below.
					You can enter an individual value or an array. Use the number or string.
					(e.g. --cols="["lastScanDate", 6, 4]", or --cols="all")
 					
 					1: subjectCN, 2: fingerprint, 3: validityEnd, 4: id, 5: certificateStatus,
 					6: encryptionType, 7: keyStrength, 8: subjectL, 9: subjectOU, 10: issuerCN,
 					11: totalInstanceCount, 12: certificateSource, 13: ipAddress, 14: port,
 					15: instanceChainValidationStatus, 16: sslValidationStatus, 17: sslProtocols,
 					18: lastScanDate, 19: modificationDate, 20: deploymentStatus, 21: subjectC

	--headers		\tAdjust the CSV output format when verbosity is set to 0.
					This allows you to pipe output to another platform with the headers.
					e.g. --logs --cols="[1,2,3]" --show="300" --headers

	Examples:
		1. --installs --cn="www.acme.com" --cols="[5,12,13,1,4,17]"
		2. --installs --country="CH" --ou="Marketing" --cols="all"

	""")


def general_help():
	# os.system("clear")
	banner()
	help_header()
	print(
		"""\033[96mGENERAL VENAFI HELP:\033[00m

	-h, --help		\tget help using Venafi command. 
					get specific help by running with another command. E.g.
					"--logs --help"

	--connect		\tlogin to Venafi. use the "--once" flag to prevent your 
					API key from being stored as an environment variable.
					use either your API Key or credentials. type "venafi
					-h --login" for more details.

	--disconnect		\tlogout of Venafi.

	-v, --verbosity		\tchoose how you want output of Venafi to be.
					"0" for machine readable output perfect for automation tools
					"1" for Human readable output for interactive command line
					(e.g. --verbosity="1" or -v 0)

	-r, --request		\trequest a certificate

	-t, --test		\tComing soon. Makes a request as a test and does not result in an issued
					certificate. This will test that the request that was made
					is possible with the entered paramteres, testing the CA and
					the Venafi connections.

	--certs			\tsearch for a certificate by any of its attributes. type --certs --help
					for more details

	--installs		\tview a certificate's installations (--installs --cn="www.acme.org").
					Use --installs --help for more details

	--logs			\tview Venafi logs. Use "--logs --help" for more details

	--vsatellites		\tcoming soon. return a list of active VSatellites for my account.
					type "venafi --vsatellites -h" for more options

	--scanafi		\tcoming soon.set the parameters for a scanafi scan and then run
					a Scanafi executable locally against those paramters.
					type "venafi --scanafi -h" for more details and options.
		""")


# message to show if no arguments are provided
def no_args():
	os.system("clear")
	banner()
	print(
		"""Welcome to Venafi CLI
Run "venafi -h" or "venafi --help" for a list of options.

• In-browser CLI labs and tutorials at \033[96mhttps://devhub.venafi.com/labs\033[00m
• Read more about each command at \033[96mhttps://devhub.venafi.com/documentation\033[00m
		"""
		)


# message to show if no arguments are provided
def not_logged_in():
	os.system("clear")
	banner()
	print("You are not logged in log in by typing \"venafi --connect\"\n")
	help_header()