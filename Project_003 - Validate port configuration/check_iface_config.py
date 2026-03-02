################## IMPORT SESSIONS ##################
# Import the ConnectHandler class from the Netmiko library to connect to network devices via SSH.
from netmiko import ConnectHandler

# Import Netmiko exceptions to handle connection, authentication, and timeout errors.
# NetmikoTimeoutException: occurs when the connection times out.
# NetmikoAuthenticationException: occurs when the username or password is incorrect.
# ReadTimeout: occurs when the device does not respond in time during data reading.
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException, ReadTimeout

# Import the function to open and save files.
from helpers import read_yaml, save_file_append

# Import the module that validates the company naming convention.
from validate_name_convention import (
    validate_trunk_uplink_pattern,
    validate_trunk_downlink_pattern,
    validate_trunk_access_point_pattern,
    validate_access_port_pc_pattern,
    validate_access_port_printer_pattern,
    validate_access_port_time_clock_pattern,
)

# Capture date and time to rename the output file
from datetime import datetime

#import ipdb

#####################################################

# Concatenate the interface commands.
# Returns a string with the concatenated commands.
def print_port_config(dados_interfaces):
    output = []
    output.append(dados_interfaces[0])
    for i in dados_interfaces[1:]:
        output.append(f" {i}")
    return "\n".join(output)

# Concatenate the template interface commands.
# Returns a string
def print_port_config_template(dados_interfaces):
    output = []
    #print("Original Configuration:")
    for i in dados_interfaces:
        #print(f"i --->>{i}")
        output.append(f" {i}")
    return "\n".join(output)

# Returns commands present in template_commands but missing from interface_config.
def f_to_be_added(template_commands,interface_config):
    to_be_added = list(set(template_commands) - set(interface_config))
    return to_be_added

# Returns commands present in interface_config but missing from template_commands.
def f_to_be_removed(interface_config, template_commands):
    to_be_removed = list(set(interface_config) - set(template_commands))
    return to_be_removed

# Create output of string to be printed or saved.
def printer_result(device_ip, interface_name, result_to_be_added, result_to_be_removed ):
    result = f"\nDevice : {device_ip} - {interface_name} "

    # Commands should be added:
    result += "\nTo be added: \n"

    if result_to_be_added:
        for i in result_to_be_added:
            result += " + " + i + "\n"
    else:
        result += "There is nothing to add.\n"

    # Commands should be removed:
    result += "\nTo be removed:\n"
    if result_to_be_removed:
        for i in result_to_be_removed:
            result += " - " + i + "\n"
    else:
        result += "There is nothing to remove."

    result += "\n"
    result += "*"*60

    return result

####################### LOAD FILES ##########################
# Load devices from YAML file
devices = read_yaml("inventory.yaml")

# Load trunk port template switch from YAML file
port_template = read_yaml("port_template.yaml")

######### MANIPULATE TEMPLATE FILES TO VARIABLES ############
trunk_uplink_config = port_template['trunk_uplink_config']
access_point_config = port_template['access_point_config']
trunk_downlink_config = port_template['trunk_downlink_config']
access_pc_config = port_template['access_pc_config']
access_printer_config = port_template['access_printer_config']
access_time_clock_config = port_template['access_time_clock_config']

#####################################################
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"output/output_{timestamp}.txt"

# Connect to each device
for device in devices:
    # Python tries to execute the code here; if an error occurs, the except block prevents the execution from breaking
    try:
        # Uses a context manager to handle Netmiko and open an SSH connection to the device
        with ConnectHandler(**device) as conn:
            # Accesses privileged mode — especially important in multivendor environments
            conn.enable()

            # Imprimir na tela o device o sistema operacional do equipamento.
            print('\n')
            print('#'*60)
            print(f"######### Connected to {device['host']} - ({device['device_type']}) ########## ")
            print('#'*60)

            # Command to run on the device
            command = "show ip interface brief"

            # Parse the interface using Genie to select only the inferfaces from show run
            parsed = conn.send_command(command, use_genie=True)

            # Capture only the interface name
            interfaces = parsed["interface"].keys()

            # Access each interface configured on the switch.
            for interface in interfaces:
                # Command to run on the device
                command = "show running-config interface " + interface

                # Output parsing via genie - String format
                interface_config_original = conn.send_command(command, use_genie=True)

                # Output parsed contains just the interface and in list format
                interface_config_original = interface_config_original.splitlines()

                interface_config = []

                # Iterates over each command in the interface configuration and removes unused data
                for cmd in interface_config_original[4:-1]:
                    # Removes leading and trailing whitespace from the command
                    interface_config.append(cmd.strip())

                # Extracts the interface description
                description = interface_config[1]

                # Remove the command description while keeping the space.
                description = description[11:]

                # Check each port type based on its description.
                # TRUNK UPLINK
                if validate_trunk_uplink_pattern(description):
                    print("------ SWITCH TRUNK UPLINK PORT! ------")
                    print(print_port_config(interface_config))

                    print('\nTemplate Configuration:')
                    print(print_port_config_template(trunk_uplink_config))

                    # Check for commands that should be added or removed
                    result_to_be_added = f_to_be_added(trunk_uplink_config, interface_config)
                    result_to_be_removed = f_to_be_removed(interface_config[2:], trunk_uplink_config)

                    # Create a string containing the result.
                    result = printer_result(device['host'], interface_config[0], result_to_be_added, result_to_be_removed )

                    # Print the output and save the result on text file.
                    print(result)
                    save_file_append(filename, result)

                # TRUNK DOWNLINK
                elif validate_trunk_downlink_pattern(description):
                    print("------ SWITCH TRUNK DOWNLINK PORT! ------")
                    print(print_port_config(interface_config))

                    print('\nTemplate Configuration:')
                    print(print_port_config_template(trunk_downlink_config))

                    # Check for commands that should be added or removed
                    result_to_be_added = f_to_be_added(trunk_downlink_config, interface_config)
                    result_to_be_removed = f_to_be_removed(interface_config[2:], trunk_downlink_config)

                    # Create a string containing the result.
                    result = printer_result(device['host'], interface_config[0], result_to_be_added, result_to_be_removed )

                    # Print the output and save the result on text file.
                    print(result)
                    save_file_append(filename, result)

                # ACCESS POINT
                elif validate_trunk_access_point_pattern(description):
                    print("------ ACCESS POINT TRUNK PORT! ------")
                    print(print_port_config(interface_config))

                    print('\nTemplate Configuration:')
                    print(print_port_config_template(access_point_config))

                    # Check for commands that should be added or removed
                    result_to_be_added = f_to_be_added(access_point_config, interface_config)
                    result_to_be_removed = f_to_be_removed(interface_config[2:], access_point_config)

                    # Create a string containing the result.
                    result = printer_result(device['host'], interface_config[0], result_to_be_added, result_to_be_removed )

                    # Print the output and save the result on text file.
                    print(result)
                    save_file_append(filename, result)

                elif validate_access_port_pc_pattern(description):
                    print("------ ACCESS PORT - PC + VOIP! ------")
                    print(print_port_config(interface_config))

                    print('\nTemplate Configuration:')
                    print(print_port_config_template(access_pc_config))

                    # Check for commands that should be added or removed
                    result_to_be_added = f_to_be_added(access_pc_config, interface_config)
                    result_to_be_removed = f_to_be_removed(interface_config[2:], access_pc_config)

                    # Create a string containing the result.
                    result = printer_result(device['host'], interface_config[0], result_to_be_added, result_to_be_removed )

                    # Print the output and save the result on text file.
                    print(result)
                    save_file_append(filename, result)

                elif validate_access_port_printer_pattern(description):
                    print("------ ACCESS PORT - PRINTER! ------")
                    print(print_port_config(interface_config))

                    print('\nTemplate Configuration:')
                    print(print_port_config_template(access_printer_config))

                    # Check for commands that should be added or removed
                    result_to_be_added = f_to_be_added(access_printer_config, interface_config)
                    result_to_be_removed = f_to_be_removed(interface_config[2:], access_printer_config)

                    # Create a string containing the result.
                    result = printer_result(device['host'], interface_config[0], result_to_be_added, result_to_be_removed )

                    # Print the output and save the result on text file.
                    print(result)
                    save_file_append(filename, result)

                # TIME CLOCK
                elif validate_access_port_time_clock_pattern(description):
                    print("------ ACCESS PORT - TIME CLOCK PORT! ------")
                    print(print_port_config(interface_config))

                    print('\nTemplate Configuration:')
                    print(print_port_config_template(access_time_clock_config))

                    # Check for commands that should be added or removed
                    result_to_be_added = f_to_be_added(access_time_clock_config, interface_config)
                    result_to_be_removed = f_to_be_removed(interface_config[2:], access_time_clock_config)

                    # Create a string containing the result.
                    result = printer_result(device['host'], interface_config[0], result_to_be_added, result_to_be_removed )

                    # Print the output and save the result on text file.
                    print(result)
                    save_file_append(filename, result)
                else:
                    print('------ CHECK THE CONFIGURATION PORT  ------')
                    print(f"{print_port_config(interface_config)}")
                    print('!---> The description format or port type does not match the existing template port configuration.')

                    result = f"\nDevice : {device['host']} - {interface_config[0]}"
                    result += "\n!---> The description format or port type does not match the existing template port configuration."
                    result += "\n!---> Check the configuration port."
                    result += "\n\n"
                    result += "*"*60
                    result += "\n"

                    save_file_append(filename, result)

                print()

    # Handles a timeout error when the SSH connection cannot be established, for example due to a DNS failure or if the device is unreachable.
    except NetmikoTimeoutException as e:
        print("TimeOut Error, possible reasons:\n Check DNS resolution")
        print(f"error: {e}")
    # Handles credential errors.
    except NetmikoAuthenticationException as e:
        print("Authentication to device failed. Check the username and password")
        print(f"error: {e}")
    # Handles the error when the device type exists but is not the correct device type for the equipment.
    except ReadTimeout as e:
        print(f"The device type {device['device_type']} exist but it is not compatible with the device")
        print(f"error: {e}")
    # Handles the case when the device type does not exist.
    except ValueError as e:
        print(f"The device type {device['device_type']} does not exist. Check the correct on: {e}")
    # Handles exceptions not listed above.
    except Exception as e:
        print(f"The error is: {e}")