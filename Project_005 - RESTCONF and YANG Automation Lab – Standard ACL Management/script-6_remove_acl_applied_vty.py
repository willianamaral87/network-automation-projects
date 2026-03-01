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

    print(f"XXXXXXXXXXXXXXX { IP} XXXXXXXXXXXXXXX")

    url = "https://"+IP+"/restconf/data/Cisco-IOS-XE-native:native/line/vty=0/access-class"

    headers = {
        "Accept": "application/yang-data+json"
    }

    auth = (username, password ) 

    try:
        response = requests.delete(url, headers=headers, auth=auth, verify=False)

        if response.status_code == 204:
            print("Status Code 204 - No Content")
            print("The ACL was removed from Line VTY 0")
        else:
            print("Check and analyze the error")
            print(f"Status code : {response.status_code} ")
            print(response.text)

    except Exception as err:
        print(f"--->>> Error: {err}")

    print()