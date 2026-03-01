import requests
import urllib3

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

    url = "https://"+IP+"/restconf/data/Cisco-IOS-XE-native:native/ip/access-list/standard"

    headers = {
        "Accept": "application/yang-data+json"
    }

    auth = (username, password )

    try:
        response = requests.get(
            url,
            headers=headers,
            auth=auth,
            verify=False
        )

        #print(f"Status Code: {response.status_code}")
        #print(response.text)

        if response.status_code == 200:
            print("Code 200 - Ok")
            print(response.text)
        elif response.status_code == 204:
            print("Code 204 - No Content")
            print("There is no Standard ACL configured on the end device.")
    
    except Exception as err:
        print(f"--->>> Error: {err}")



    
    