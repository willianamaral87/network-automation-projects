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

    connection.send_command_timing("changeto system")

    output = connection.send_command("show context", use_textfsm=True) 

    context = []

    context.append("system")

    for line in output.splitlines():
        line = line.strip()

        if (
            line
            and "Context Name" not in line
            and "---" not in line
        ):
            ctx = line.split()[0]
            context.append(ctx)

    context.pop()

    print(context)

    bkp = ""

    print("xxxxx")
    for ctx in context:
        ctx = ctx.replace("*","")

        print("-------- Contexto atual --------- " + ctx)
        connection.send_command_timing("changeto context " + ctx)

        str = "-------- Contexto atual --------- " + ctx
        bkp += str+"\n"
        bkp = connection.send_command("show run")

        filename = f"bkp-asa-{device['host']}-{ctx}"

        with open(filename, "w") as file:
            file.write(bkp)

    connection.disconnect()

    print(f"Backup realizado: {device['host']}")
