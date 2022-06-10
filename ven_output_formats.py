log_data_format = {
	"activityName": {
			"selector": "activityName",
			"format": [28, "Activity Name"]
		},
	"activityType": {
			"selector": "activityType",
			"format": [18, "Activity Type"]
		},
	"message": {
			"selector": "message",
			"format": [138, "Message"]
		},
	"activityDate": {
			"selector": "activityDate",
			"format": [24, "Timestamp"],
			"specialFormatting": -6
		},
	"clientIpAddress": {
			"subsection": "payload",
			"selector": "clientIpAddress",
			"format": [16, "Client"]
		},
	"username": {
			"subsection": "payload",
			"selector": "username",
			"format": [20, "Username"],
			"specialFormatting": -11
		},
	"criticality": {
			"subsection": "payload",
			"selector": "criticality",
			"format": [12, "Criticality"]
		}
}

cert_data_format = {
	"subjectCN": {
			"selector": "subjectCN",
			"format": [40, "Subject Common Name"],
			"selectItem": 0
		},
	"fingerprint": {
			"selector": "fingerprint",
			"format": [41, "Fingerprint"]
		},
	"validityEnd": {
			"selector": "validityEnd",
			"format": [24, "Validity End Date"],
			"specialFormatting": -6
		},
	"id": {
			"selector": "id",
			"format": [37, "Venafi UUID"]
		},
	"certificateStatus": {
			"selector": "certificateStatus",
			"format": [8, "Status"]
		},
	"encryptionType": {
			"selector": "encryptionType",
			"format": [10, "Encryption"]
		},
	"subjectL": {
			"selector": "subjectL",
			"format": [16, "Locality"]
		},
	"subjectOU": {
			"selector": "subjectOU",
			"format": [12, "Org Unit"],
			"selectItem": 0
		},
	"issuerCN": {
			"selector": "issuerCN",
			"format": [25, "Issuer Common Name"],
			"selectItem": 0
		},
	"totalInstanceCount": {
			"selector": "totalInstanceCount",
			"format": [9, "Installs"]
		},
	"subjectST": {
			"selector": "subjectST",
			"format": [15, "State"]
		},
	"subjectC": {
			"selector": "subjectC",
			"format": [8, "Country"]
		},
	"keyStrength": {
			"selector": "keyStrength",
			"format": [10, "Key Length"]
		},
	"selfSigned": {
			"selector": "selfSigned",
			"format": [12, "Self Signed"]
		},
	"extendedKeyUsage": {
			"selector": "extendedKeyUsage",
			"format": [70, "Extended Key Usage"]
		}
	
}

installation_data_format = {
	"subjectCN": {
			"selector": "subjectCN",
			"format": [40, "Subject Common Name"],
			"selectItem": 0
		},
	"fingerprint": {
			"selector": "fingerprint",
			"format": [41, "Fingerprint"]
		},
	"validityEnd": {
			"selector": "validityEnd",
			"format": [24, "Validity End Date"],
			"specialFormatting": -6
		},
	"id": {
			"selector": "id",
			"format": [37, "Venafi UUID"]
		},
	"certificateStatus": {
			"selector": "certificateStatus",
			"format": [8, "Status"]
		},
	"encryptionType": {
			"selector": "encryptionType",
			"format": [10, "Encryption"]
		},
	"keyStrength": {
			"selector": "keyStrength",
			"format": [10, "Key Length"]
		},
	"subjectL": {
			"selector": "subjectL",
			"format": [16, "Locality"]
		},
	"subjectOU": {
			"selector": "subjectOU",
			"format": [12, "Org Unit"],
			"selectItem": 0
		},
	"subjectC": {
			"selector": "subjectC",
			"format": [8, "Country"]
		},
	"issuerCN": {
			"selector": "issuerCN",
			"format": [25, "Issuer Common Name"],
			"selectItem": 0
		},
	"totalInstanceCount": {
			"selector": "totalInstanceCount",
			"format": [8, "Installs"]
		},
	"ipAddress": {
			"selector": "ipAddress",
			"format": [25, "Installation Address"]
		},
	"certificateSource": {
			"selector": "certificateSource",
			"format": [15, "Install Source"]
		},
	"port": {
			"selector": "port",
			"format": [5, "Port"]
		},
	"instanceChainValidationStatus": {
			"selector": "instanceChainValidationStatus",
			"format": [17, "Chain Validation"]
		},
	"sslValidationStatus": {
			"selector": "sslValidationStatus",
			"format": [25, "SSL Validation"]
		},
	"sslValidationStatusMessage": {
			"selector": "sslValidationStatusMessage",
			"format": [40, "SSL Validation Message"]
		},
	"sslProtocols": {
			"selector": "sslProtocols",
			"format": [22, "SSL Protocol (oldest)"],
			"selectItem": 0
		},
	"lastScanDate": {
			"selector": "lastScanDate",
			"format": [24, "Last Scanned"],
			"specialFormatting": -6
		},
	"modificationDate": {
			"selector": "modificationDate",
			"format": [24, "Last Modified"],
			"specialFormatting": -6
		},
	"deploymentStatus": {
			"selector": "deploymentStatus",
			"format": [20, "Installation Status"]
		}
}