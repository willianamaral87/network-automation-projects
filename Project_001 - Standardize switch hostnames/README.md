# Standardize Hostname Configuration in Multivendor Network Devices

## Motivation: 
The objective of this lab is to standardize hostname configuration across switches and routers from different vendors (multivendor environments) using the Netmiko library to automate SSH connections and apply changes in a consistent and secure manner.

The suggested hostname standardization in this lab follows the convention:

< SITE >-< AREA >-< TYPE-OF-DEVICE >< IP >, where:
- SITE: device location;
- AREA: internal area within the location;
- TYPE-OF-DEVICE: device type, such as switch or router;
- IP: fourth octet of the device’s IP address.


## Project Structure
To execute the hostname change script, three files are required:
1) script-change-hostname.py: Python script responsible for applying the hostname change on the devices.

2) inventory_netmiko.yaml:
  - Arquivo de inventário que contém a lista de dispositivos e suas informações de conexão.
  - Estrutura:
  - id: # Identificação do dispositivo
    netmiko_conn:
  
      host: r1                          # Hostname ou endereço IP do dispositivo
      username: admin                   # Username
      password: autonetops              # Password
      device_type: cisco_ios            # Device type/vendor
      session_log: r1_session_log.txt   # Execution log file
      session_log_file_mode: append     # Append mode to avoid overwriting previous logs
    extra:
      new_hostname: SPO-OFFICE-SW11     # New hostname to be applied

Note: The log file (session_log) records only the commands executed on the device; it does not capture login errors or hostname resolution issues.

3) helpers.py
- Contains helper functions, such as the function to open and read the inventory_netmiko.yaml file.
- It is not necessary to modify this file.

Execution Steps:
1) Copy the three files (script-change-hostname.py, inventory_netmiko.yaml, and helpers.py) to the same directory.
2) Edit the inventory_netmiko.yaml file to include the devices that will be configured, according to the lab setup or the production environment.

## Prepare the environment:
Go to the path:
cd /home/willian/my_projects/labs/

### Destroy the old the lab
containerlab destroy -t lab.clab.yaml 

### Deploy the lab: 
containerlab deploy -t lab.clab.yaml

### Create a new environment
python3 -m venv  venv

### Activate the virtual environment
source venv/bin/activate

### Install dependencies
pip3 install netmiko

### Execute the script:
python3.12 script-change-hostname.py 

Possible mapped outputs:

1) Successful execution:
python3.12 script-change-hostname.py 

    Connected to r1 - (cisco_ios)
    The new hostname of r1 is hostname SPO-OFFICE-SW11

    Connected to r1 - (cisco_ios)
    The new hostname of r2 is hostname RJO-PRODUCAO-SW12

    Connected to r3- (cisco_ios)
    The new hostname of r3 is hostname CPS-RH-SW13

    Connected to r4 - (arista_eos)
    The new hostname of r4 is hostname LON-TI-SW14


2) DNS failure or if the device is unreachable:
TimeOut Error, possible reasons:
 Check DNS resolution
error: DNS failure--the hostname you provided was not resolvable in DNS: r6:22	


3) In case of incorrect credentials:
Authentication to device failed. Check the username and password
error: Authentication to device failed.

4) Below is the list of supported Cisco devices:
cisco_apic
cisco_asa
cisco_ftd
cisco_ios
cisco_nxos
cisco_s200
cisco_s300
cisco_tp
cisco_viptela
cisco_wlc
cisco_xe
cisco_xr