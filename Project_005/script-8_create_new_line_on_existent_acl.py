import requests
import urllib3
import json

# Import the function to open and save files.
from helpers import read_yaml

devices = read_yaml("inventory.yaml")

# Disable SSL warnings (lab only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

acl_name = "ACL-Monitoring_Tool"

for device in devices:
    IP = device['host']
    username = device['username']
    password = device['password']

    print(f"XXXXXXXXXXXXXXX { IP} XXXXXXXXXXXXXXX")
	
    auth = (username, password ) 

    url = "https://" + IP + "/restconf/data/Cisco-IOS-XE-native:native/ip/access-list/standard=" + acl_name   

    headers = {
        "Content-Type": "application/yang-data+json",
        "Accept": "application/yang-data+json"
    }

    payload = {
        "Cisco-IOS-XE-acl:standard": {
            "name": "ACL-Monitoring_Tool",
            "access-list-seq-rule": [
	            {
	                "sequence": "14",
	                "permit": {
	                    "std-ace": {
	                        "host": "192.168.101.14"
	                    }
                    }
                }
		    ]
        }
    }

    try:
        response = requests.patch(url, headers=headers, auth=(auth),data=json.dumps(payload), verify=False)

        print("Status Code:", response.status_code)
        print(response.text)

        print('------------')

        if response.status_code == 404:
            print("Status Code 404 - Not Found")
            print("The ACL does not exist")
        if response.status_code == 204:
            print("Status Code 204 - No Content ")
            print("The line of ACL was created")
        else:
            print("Check and analyze the error")
            print(f"Status code : {response.status_code} ")
            print(response.text)

    except Exception as err:
        print(f"--->>> Error: {err}")

    print()