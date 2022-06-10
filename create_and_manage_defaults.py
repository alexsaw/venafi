import requests
import sys
import json
import os


def getDefaultApp():

	# check if default application has been created already. If yes, get APP ID
	with open('global_vars.json', 'r+') as f:
		global_vars = json.load(f)
		
		if global_vars["DEFAULT_TEMPLATE_ID"] == 0:	
			createDefaultCIT()

		if global_vars["DEFAULT_APP"] == 0:

			# create application if not and get the APP ID
			app_id = createApplication()

			# add application id to global_vars json document
			# check if default application has been created already. If yes, get APP ID
			with open('global_vars.json', 'r+') as f:
				global_vars = json.load(f)
				global_vars["DEFAULT_APP"] = app_id
				f.seek(0)
				json.dump(global_vars, f, indent=4)
				f.truncate()
				f.close()

	

def createDefaultCIT():

	with open('global_vars.json', 'r+') as f:
		global_vars = json.load(f)
		
		user = global_vars["USER"]

		payload = """
		{
		    \"name\": \"%s's Default Issuance Template\",
		    \"certificateAuthority\": \"BUILTIN\",
		    \"certificateAuthorityProductOptionId\": \"06d705c1-ae81-11e9-bdc4-e3fc25835e95\",
		    \"product\": {
		        \"certificateAuthority\": \"BUILTIN\",
		        \"productName\": \"Default Product\",
		        \"validityPeriod\": \"P90D\"
		    },
		    \"trackingData\": null,
		    \"subjectCNRegexes\": [
		        \".*\"
		    ],
		    \"subjectORegexes\": [
		        \".*\"
		    ],
		    \"subjectOURegexes\": [
		        \".*\"
		    ],
		    \"subjectLRegexes\": [
		        \".*\"
		    ],
		    \"subjectSTRegexes\": [
		        \".*\"
		    ],
		    \"subjectCValues\": [
		        \".*\"
		    ],
		    \"sanRegexes\": [
		        \".*\"
		    ],
		    \"keyTypes\": [
		        {
		            \"keyType\": \"RSA\",
		            \"keyLengths\": [
		                2048,
		                4096
		            ]
		        }
		    ],
		    \"keyReuse\": false,
		    \"csrUploadAllowed\": true,
		    \"keyGeneratedByVenafiAllowed\": false
		}
		"""%(user)

		url='https://api.venafi.cloud/v1/certificateissuingtemplates'
		headers = {
		  'tppl-api-key': global_vars["API_KEY"],
		  'accept': 'application/json',
		  'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		data = response.json()

		cit_alias = data["certificateIssuingTemplates"][0]["name"]
		cit_id = data["certificateIssuingTemplates"][0]["id"]

		global_vars["DEFAULT_TEMPLATE_ALIAS"] = cit_alias
		global_vars["DEFAULT_TEMPLATE_ID"] = cit_id

		f.seek(0)
		json.dump(global_vars, f, indent=4)
		f.truncate()
		f.close()


def createApplication():

	with open('global_vars.json', 'r+') as f:
		global_vars = json.load(f)
	
		user = global_vars["USER"]
		owner_id = global_vars["OWNER_ID"]
		username = global_vars["USERNAME"]
		cit_alias = global_vars["DEFAULT_TEMPLATE_ALIAS"]
		cit_id = global_vars["DEFAULT_TEMPLATE_ID"]
		f.close()

		payload = """
	{
	  \"name\": \"%s's Certificates (Issued by Venafi CLI)\",
	  \"description\": \"Default application created by %s using Venafi CLI\",
	  \"certificateIssuingTemplateAliasIdMap\": {
	  	  \"%s\": \"%s\"
	  	},
	  \"ownerIdsAndTypes\": [
	    {
	      \"ownerId\": \"%s\",
	      \"ownerType\": \"USER\"
	    }
	  ]
	}
		"""%(user, username, cit_alias, cit_id, owner_id)

		url='https://api.venafi.cloud/outagedetection/v1/applications'
		  
		headers = {
		  'tppl-api-key': global_vars["API_KEY"],
		  'accept': 'application/json',
		  'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		data = response.json()

		app_id = data["applications"][0]["id"]
		
		return app_id


def adminClear():

	with open('global_vars.json', 'r+') as f:
		global_vars = json.load(f)

		headers = {
		  'tppl-api-key': global_vars["API_KEY"],
		  'accept': 'application/json',
		  'Content-Type': 'application/json'
		}

		#delete Default Application
		url='https://api.venafi.cloud/outagedetection/v1/applications/%s'%global_vars["DEFAULT_APP"]
		response = requests.request("DELETE", url, headers=headers)

		#delete Default CIT
		url='https://api.venafi.cloud/v1/certificateissuingtemplates/%s'%global_vars["DEFAULT_TEMPLATE_ID"]
		response = requests.request("DELETE", url, headers=headers)

		#reset defaults in global_vars
		global_vars["API_KEY"] = 0
		global_vars["OWNER_ID"] = 0
		global_vars["USER"] = 0
		global_vars["USERNAME"] = 0
		global_vars["PASSWORD"] = 0
		global_vars["SALT"] = 0
		global_vars["DEFAULT_APP"] = 0
		global_vars["DEFAULT_TEMPLATE_ALIAS"] = 0
		global_vars["DEFAULT_TEMPLATE_ID"] = 0
		global_vars["LOGGED_IN"] = 0
		global_vars["VERBOSITY"] = 1

		f.seek(0)
		json.dump(global_vars, f, indent=4)
		f.truncate()
		f.close()

	os.system("clear")
	print(
		"""
\033[96m
 _    __                 _____ 
| |  / /__  ____  ____ _/ __(_)
| | / / _ \/ __ \/ __ `/ /_/ / 
| |/ /  __/ / / / /_/ / __/ /  
|___/\___/_/ /_/\__,_/_/ /_/   
\033[00m

Venafi CLI instance admin clear complete. Start over with "venafi --connect"
		"""
		)
