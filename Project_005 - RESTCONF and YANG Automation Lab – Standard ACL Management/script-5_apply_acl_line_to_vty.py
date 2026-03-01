import requests
import urllib3
import json

# Import the function to open and save files.
from helpers import read_yaml

devices = read_yaml("inventory.yaml")

#print(devices)

# Disable SSL warnings (lab only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

for device in devices:
    IP = device['host']
    username = device['username']
    password = device['password']

    print(f"XXXXXXXXXXXXXXX { IP} XXXXXXXXXXXXXXX")

    url = "https://"+IP+"/restconf/data/Cisco-IOS-XE-native:native/line/vty=0/access-class"

    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json"
    }


    payload = {
        "Cisco-IOS-XE-native:access-class": {
            "acccess-list": [
                {
                    "direction": "in",
                    "access-list": "ACL-Monitoring_Tool"
                }
            ]
        }
    }

    auth = (username, password )  

    try:
        response = requests.patch(url, headers=headers,auth=auth, data=json.dumps(payload), verify=False)

        if response.status_code == 204:
            print("Status Code 204 - No Content")
            print("The ACL was applied on Line VTY 0")
        else:
            print("Check and analyze the error")
            print(f"Status code : {response.status_code} ")
            print(response.text)

    except Exception as err:
        print(f"--->>> Error: {err}")

    print()