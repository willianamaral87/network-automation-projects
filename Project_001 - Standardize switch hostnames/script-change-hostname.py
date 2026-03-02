################## IMPORT SESSIONS ##################
# Imports the ConnectHandler class from the Netmiko library to connect to network devices via SSH.
from netmiko import ConnectHandler

# Imports the logging module to record log messages and debugging information.
import logging

# Imports Netmiko exceptions to handle connection, authentication, and timeout errors
# NetmikoTimeoutException: occurs when the connection times out.
# NetmikoAuthenticationException: occurs when the username or password is incorrect.
# ReadTimeout: occurs when the device does not respond in time while reading data.
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException, ReadTimeout

# Imports the function to open and save files
from helpers import read_yaml, save_file

# Imports the time module to use time-related functions
import time

# Imports the datetime class from the datetime module to work with dates and times
from datetime import datetime

################## Global Loggings ##################

# Configures the logging module
logging.basicConfig(
    # Defines the file where logs will be saved
    filename='netmiko_debug.txt',
    # Defines the minimum logging level to be recorded (DEBUG logs all messages)
    level=logging.DEBUG,
    # Defines the log message format: date/time - level - message
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Creates a specific named logger
logger = logging.getLogger('netmiko')

#####################################################

# Loads devices from the YAML file
devices = read_yaml("inventory_netmiko.yaml")

# Access each device
for device in devices:
    # Python attempts to execute the code here; if an error occurs, the except block prevents the execution from stopping.
    try:
        # Uses a Context Manager to manage Netmiko and open the SSH connection to the device
        with ConnectHandler(**device['netmiko_conn']) as conn:

            # Appends the timestamp to the session logging
            with open(device['netmiko_conn']['session_log'], "a") as f:
                f.write(f"\n ###### {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ###### \n")

            # Enters privileged mode – especially important in multivendor environments
            conn.enable()

            # Prints on the screen the device and its operating system.
            print(f"\nConnected to {device['netmiko_conn']['host']} - ({device['netmiko_conn']['device_type']})")

            # Prepares the new hostname
            new_hostname = f"hostname {device['extra']['new_hostname'].upper()}"

            # Sends the new hostname configuration command to the switch.
            conn.send_config_set(new_hostname)

            # Updates the expected prompt after changing the hostname.
            conn.set_base_prompt()

            # Saves the configuration
            conn.save_config()

            # Prints the new hostname change
            print(f"The new hostname of {device['netmiko_conn']['host']} is {new_hostname}")

    # Handles the timeout error if the SSH connection cannot be established,
    # for example: DNS failure or if the device is unreachable.
    except NetmikoTimeoutException as e:
        print("TimeOut Error, possible reasons:\n Check DNS resolution")
        print(f"error: {e}")
    # Handles credential errors
    except NetmikoAuthenticationException as e:
        print("Authentication to device failed. Check the username and password")
        print(f"error: {e}")
    # Handles the error when the device type exists but does not match the actual device type.
    except ReadTimeout as e:
        print(f"The device type {device['netmiko_conn']['device_type']} exist but it is not compatible with the device")
        print(f"error: {e}")
    # Handles the case when the device type does not exist.
    except ValueError as e:
        print(f"The device type {device['netmiko_conn']['device_type']} does not exist. Check the correct on: {e}")
    # Handles exceptions not listed above
    except Exception as e:
        print(f"The error is: {e}")