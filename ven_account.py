import requests
import sys
import os
import json
import create_and_manage_defaults
import getopt
import hashlib
from getpass import getpass
import ven_help

def change_key(arguments, values):

	create_and_manage_defaults.adminClear()

	with open('global_vars.json', 'r+') as f:
		global_vars = json.load(f)

		try:
			for arg, val in arguments:
				if arg in ("-k", "--api_key"):
					global_vars["API_KEY"] = val

		except getopt.error as err:
			# output error, and return with an error code
			print (str(err))

		f.seek(0)
		json.dump(global_vars, f, indent=4)
		f.truncate()
		f.close()	

def changeVerbosity(arguments, values):
	with open('global_vars.json', 'r+') as f:
		global_vars = json.load(f)

		try:
			for arg, val in arguments:
				if arg in ("--verbosity", "verbose", "--v", "-v"):
					val.strip("=")
					val = int(val)
					global_vars["VERBOSITY"] = val

		except getopt.error as err:
			# output error, and return with an error code
			print (str(err))

		f.seek(0)
		json.dump(global_vars, f, indent=4)
		f.truncate()
		f.close()

def pretend_login_with_email_and_password():
	os.system("clear")
	with open('global_vars.json', 'r+') as f:
		global_vars = json.load(f)

		if global_vars["LOGGED_IN"] == 1:
			already_logged_in(global_vars)
		else:
			ven_help.banner()
			ven_help.help_header()
			if global_vars["USERNAME"] == 0:
				#ask for email address
				global_vars["USERNAME"] = input("Enter your email address:\n")
				#ask for a password
				password = getpass("Enter your password:\n")

				salt = os.urandom(32)
				password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
				global_vars["PASSWORD"] = password.hex()
				global_vars["SALT"] = salt.hex()
				#endpoint to retrieve API key
				url='https://api.venafi.cloud/v1/useraccounts'
				
				#headers required by endpoint
				headers = {
				  'tppl-api-key': global_vars["API_KEY"],
				  'accept': 'application/json',
				}
				#make GET request to endpoint
				response = requests.request("GET", url, headers=headers)
				#return response and store in data variable
				data = response.json()

				#format response for success message
				full_name = "%s %s"%(data["user"]["firstname"], data["user"]["lastname"])
				account = data["user"]["username"]
				api_key_expiry = data["apiKey"]["validityEndDate"]
				owner_id = data["apiKey"]["userId"]

				# add application id to global_vars json document
				global_vars["USER"] = full_name
				global_vars["USERNAME"] = account
				global_vars["OWNER_ID"] = owner_id

				f.seek(0)
				json.dump(global_vars, f, indent=4)
				f.truncate()
				f.close()
				
				#login
				login()

			else:
				stored_salt = bytes.fromhex(global_vars["SALT"])
				stored_hash = bytes.fromhex(global_vars["PASSWORD"])
				#ask for email address
				username = input("Enter your email address:\n")
				#ask for password
				password_to_check = getpass("Enter your password:\n")
				new_hash = hashlib.pbkdf2_hmac('sha256', password_to_check.encode('utf-8'), stored_salt, 100000)

				
				if global_vars["USERNAME"] == username and stored_hash == new_hash:
					login()
				else:
					login_fail()

def login():
	with open('global_vars.json', 'r+') as f:
		global_vars = json.load(f)

		global_vars["LOGGED_IN"] = 1
		
		f.seek(0)
		json.dump(global_vars, f, indent=4)
		f.truncate()
		f.close()

	# default App and CIT needed for ease of use
	create_and_manage_defaults.getDefaultApp()

	login_success(global_vars)

def already_logged_in(global_vars):
	
	os.system("clear")
	print("""\033[96m
 _    __                 _____ 
| |  / /__  ____  ____ _/ __(_)
| | / / _ \/ __ \/ __ `/ /_/ / 
| |/ /  __/ / / / /_/ / __/ /  
|___/\___/_/ /_/\__,_/_/ /_/   
			"""
			)
	print("You're already logged in as %s\033[00m"%global_vars["USER"])	

def login_success(global_vars):

	os.system("clear")
	print("""\033[96m
 _    __                 _____ 
| |  / /__  ____  ____ _/ __(_)
| | / / _ \/ __ \/ __ `/ /_/ / 
| |/ /  __/ / / / /_/ / __/ /  
|___/\___/_/ /_/\__,_/_/ /_/   
			"""
			)
	print("Login successful! Welcome %s"%global_vars["USER"])
	print("• See how easy certificate requests can be by typing \"venafi -r --cn=\"www.acme.org\"")
	print("• or type \"venafi -h\" to see all Venafi CLI options.")
	print("The API key for %s will expire in XX days\033[00m"%(global_vars["USERNAME"]))


def login_fail():
	with open('global_vars.json', 'r+') as f:
		global_vars = json.load(f)

		global_vars["LOGGED_IN"] = 0
		
		f.seek(0)
		json.dump(global_vars, f, indent=4)
		f.truncate()
		f.close()
	print("Login failed. Check your credentials, or ensure that you have an active API key")


def connect_with_hard_coded_api_key():

	#retrieve global variables stores in global_vars.json
	with open('global_vars.json', 'r+') as f:
		global_vars = json.load(f)

		if global_vars["API_KEY"] == 0:
			global_vars["API_KEY"] = input("Enter your API Key:\n")
	
		#endpoint to retrieve API key
		url='https://api.venafi.cloud/v1/useraccounts'
		
		#headers required by endpoint
		headers = {
		  'tppl-api-key': global_vars["API_KEY"],
		  'accept': 'application/json',
		}
		#make GET request to endpoint
		response = requests.request("GET", url, headers=headers)
		#return response and store in data variable
		data = response.json()

		#format response for success message
		full_name = "%s %s"%(data["user"]["firstname"], data["user"]["lastname"])
		account = data["user"]["username"]
		api_key_expiry = data["apiKey"]["validityEndDate"]
		owner_id = data["apiKey"]["userId"]


		# check if default application has been created already. If yes, get APP ID
		if global_vars["USERNAME"] == 0:
			# save user

			# add application id to global_vars json document
			global_vars["USER"] = full_name
			global_vars["USERNAME"] = account
			global_vars["OWNER_ID"] = owner_id

		global_vars["LOGGED_IN"] = 1
		f.seek(0)
		json.dump(global_vars, f, indent=4)
		f.truncate()
		f.close()

	# default App and CIT needed for ease of use
	create_and_manage_defaults.getDefaultApp()

	os.system("clear")

	print("""\033[96m
 _    __                 _____ 
| |  / /__  ____  ____ _/ __(_)
| | / / _ \/ __ \/ __ `/ /_/ / 
| |/ /  __/ / / / /_/ / __/ /  
|___/\___/_/ /_/\__,_/_/ /_/   
			"""
			)
	print("Login successful! Welcome %s\n"%full_name)
	print("• See how easy certificate requests can be by typing \"venafi -r --cn=\"www.acme.org\"")
	print("• or type \"venafi -h\" to see all Venafi CLI options.")
	print("The API key for %s will expire on %s\033[00m"%(account, api_key_expiry))

#if not one time use api_key as specified with "no_env" flag, store as environment variable
#...


def logout():

	os.system("clear")

	with open('global_vars.json', 'r+') as f:
		global_vars = json.load(f)
		global_vars["LOGGED_IN"] = 0
		if global_vars["USER"] != 0:
			full_name = global_vars["USER"]
			print("""\033[96m
 _    __                 _____ 
| |  / /__  ____  ____ _/ __(_)
| | / / _ \/ __ \/ __ `/ /_/ / 
| |/ /  __/ / / / /_/ / __/ /  
|___/\___/_/ /_/\__,_/_/ /_/   
				\033[00m"""
				)
			print("%s, you are now successfully logged out"%full_name)
		f.seek(0)
		json.dump(global_vars, f, indent=4)
		f.truncate()
		f.close()

def logout_api_version():

	os.system("clear")

	with open('global_vars.json', 'r+') as f:
		global_vars = json.load(f)

		headers = {
		  'tppl-api-key': global_vars["API_KEY"],
		  'accept': 'application/json',
		  'Content-Type': 'application/json'
		}

		#reset defaults in global_vars
		global_vars["API_KEY"] = 0


		f.seek(0)
		json.dump(global_vars, f, indent=4)
		f.truncate()
		f.close()

		print("""\033[96m
 _    __                 _____ 
| |  / /__  ____  ____ _/ __(_)
| | / / _ \/ __ \/ __ `/ /_/ / 
| |/ /  __/ / / / /_/ / __/ /  
|___/\___/_/ /_/\__,_/_/ /_/   
				\033[00m"""
				)
		print("%s, you are now successfully logged out"%full_name)
