import requests
import urllib3
import json

# Import the function to open and save files.
from helpers import read_yaml

devices = read_yaml("inventory.yaml")

# Disable SSL warnings (lab only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

for device in devices:
    IP = device['host']
    username = device['username']
    password = device['password']
    
    print(f"XXXXXXXXXXXXXXX { IP }  XXXXXXXXXXXXXXX")

    url = "https://"+IP+"/restconf/data/Cisco-IOS-XE-native:native/ip/access-list/"
	
    headers = {
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json"
    }

    payload = {
        "Cisco-IOS-XE-acl:standard": {
	        "name": "ACL-Monitoring_Tool",
	        "access-list-seq-rule": [
                {
                    "sequence": "5",
                    "permit": {
                        "std-ace": {
							"host": "192.168.101.10"
						}
					}
				},
				{
					"sequence": "10",
					"permit": {
						"std-ace": {
							"host": "192.168.101.222"
						}
					}
				},
				{
					"sequence": "20",
					"deny": {
						"std-ace": {
							"any": {}
						}
					}
				}
			]
		}
	}

    try:
        response = requests.post(
            url,
            headers=headers,
            auth=(username, password),
            data=json.dumps(payload),
            verify=False
	    )
	
        if response.status_code == 201:
            print("Code 201 - Created")
            print("The ACL was created. ")
        elif response.status_code == 409:
            print("Code 409 - Conflicts")
            print("You are trying to create a resource that already exists. ")
            print("\nError from end device:")
            print(response.text)
        else:
            print("Check and analyze the error")
            print(f"Status code : {response.status_code} ")
            print(response.text)
    except Exception as err:
        print(f"--->>> Error: {err}")

 
    print()