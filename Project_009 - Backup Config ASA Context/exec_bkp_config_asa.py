from netmiko import ConnectHandler

from pprint import pprint

# ReadTimeout: occurs when the device does not respond in time while reading data.
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException, ReadTimeout

# Imports the time module to use time-related functions
import time

# Imports the datetime class from the datetime module to work with dates and times
from datetime import datetime



import yaml

with open("inventory.yaml", "r") as file:
    devices = yaml.safe_load(file)

#print(devices)

for device in devices: 

    connection = ConnectHandler(**device)

    connection.enable()

    output = connection.send_command("show run", use_textfsm=True)

    #pprint(output)

    filename = f"bkp-asa-{device['host']}"

    with open(filename, "w") as file:
        file.write(output)

    connection.disconnect()

    print(f"Backup realizado: {device['host']}")