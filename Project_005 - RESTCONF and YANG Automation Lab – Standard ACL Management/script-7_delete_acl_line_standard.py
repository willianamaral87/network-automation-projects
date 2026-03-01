import requests
import urllib3
import json

# Import the function to open and save files.
from helpers import read_yaml

devices = read_yaml("inventory.yaml")

# Disable SSL warnings (lab only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

acl_name = "ACL-Monitoring_Tool"

number_of_line = "14"


for device in devices:
    IP = device['host']
    username = device['username']
    password = device['password']

    print(f"XXXXXXXXXXXXXXX { IP} XXXXXXXXXXXXXXX")

    url = "https://"+IP+"/restconf/data/Cisco-IOS-XE-native:native/ip/access-list/standard="+acl_name+"/access-list-seq-rule="+number_of_line

    try:
        response = requests.delete(url, auth=(username, password), verify=False)

        if response.status_code == 404:
            print("Status Code 404 - Not Found.")
            print("The line of ACL or ACL was not found.")
        elif response.status_code == 204:
            print("Status Code 204 - No Content.")
            print("The line of ACL was removed.")
        else:
            print("Check and analyze the error:")
            print(f"Status code : {response.status_code} ")
            print(f"Response : {response.text} ")

    except Exception as err:
        print(f"--->>> Error: {err}")

    print()