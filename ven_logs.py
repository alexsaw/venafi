import getopt, sys
import json
import requests
import os
import ven_help
import ven_display_data


def get_logs(arguments, values):

	include_headers = False

	search_object = {}

	expression = {
		"operator":"OR"
	}

	operands = []

	ordering = {
	    "orders": [
	        {
				"field":"activityDate",
				"direction":"DESC"
	        }
	    ]
	}

	paging = {
		"pageSize":51,
		"pageNumber":0
	}

	default_columns = [
		"activityName",
		"message",
		"clientIpAddress",
		"username",
		"activityDate"
	]

	default_search = {
		"field": "activityName",
		"operator": "FIND",
		"value": "*"
	}

	selected_columns = []

	column_options = {
		1: "activityName",
		2: "activityType",
		3: "message",
		4: "activityDate",
		5: "clientIpAddress",
		6: "username",
		7: "criticality"
	}

	activity_type_options = {
		1: "Authentication",
		2: "VSatellites",
		3: "Notifications",
		4: "Certificates",
		5: "User Security",
		6: "Applications"
	}

	activity_options = {
		1: "Login Succeeded",
		2: "Logout",
		3: "Login Failed",
		4: "Issuing Template Created",
		5: "Application Created",
		6: "CSR Generated",
		7: "Certificate Issued",
		8: "Notification sent",
		9: "VSatellite Pairing Code Created",
		10: "VSatellite Paired",
		11: "VSatellite Deleted",
		12: "Issuing Template Updated",
		13: "ApiKey Rotation Requested",
		14: "ApiKey Deleted"
	}

	try:
		for arg, val in arguments:
			if arg in ("--show", "--s", "-s"):
				paging = {
					"pageNumber": 0,
					"pageSize": int(val)
				}
			elif arg in ("--activity_type", "--activity-type"):
				for key, value in activity_type_options.items():
					if val == str(key) or val == value:
						event_type = {
							"field": "activityType",
							"operator": "FIND",
							"value": value
							}
						operands.append(event_type)
			elif arg in ("--message", "--activity-message", "--activity_message"):
				message = {
					"field": "message",
					"operator": "FIND",
					"value": val
					}
				operands.append(message)
			elif arg in ("--activity"):
				for key, value in activity_options.items():
					if val == str(key) or val == value:
						activity = {
							"field": "activityName",
							"operator": "FIND",
							"value": value
							}
						operands.append(activity)
			elif arg in ("--criticality"):
				criticality = {
					"field": "criticality",
					"operator": "EQ",
					"value": val
					}
				operands.append(criticality)
			elif arg in ("--client"):
				username = {
					"field": "payload",
					"operator": "FIND",
					"value": val
					}
				operands.append(username)
			elif arg in ("--username", "--user"):
				username = {
					"field": "payload",
					"operator": "FIND",
					"value": val
					}
				operands.append(username)
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


	except getopt.error as err:
		# output error, and return with an error code
		print (str(err))	


	if len(operands) == 0:
		expression["operands"] = default_search
	else:
		expression["operands"] = operands
		search_object["expression"] = expression

		selected_operators = []
		for op in operands:
			selected_operators.append(op["field"])

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
			print("\n\n\033[36;1mGetting your logs. One moment...\033[00m")

		url='https://api.venafi.cloud/v1/activitylogsearch'
		headers = {
		  'tppl-api-key': global_vars["API_KEY"],
		  'accept': 'application/json',
		  'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		data = response.json()

		if global_vars["VERBOSITY"] >= 1:
			os.system("clear")
			print("\n")
			print("\033[36;1mFound %s logs matching your search:"%data["count"])
			print("You can also view all your logs in Venafi: \033[4mhttps://ui.venafi.cloud/platform-settings/event-log\033[00m\n")
	
			ven_display_data.tabular_output("logs", data["activityLogEntries"], data["count"], columns_for_table, False)
		else:
			ven_display_data.csv_output("logs", data["activityLogEntries"], data["count"], columns_for_table, include_headers, False)
