# Perform Context ASA Backup Configuration

This project uses 3 files:
- inventory.yaml : Inventory file with all ASA devices.
- exec_bkp_config_asa_context.py : erforms the backup configuration for ASA devices with contexts.
- exec_bkp_config_asa.py : performs the backup configuration for ASA devices without contexts.

For ASA devices configured without contexts, execute the exec_bkp_config_asa.py file:
- python3 exec_bkp_config_asa.py

For ASA devices configured with contexts, execute the exec_bkp_config_asa_context.py file:
- python3 exec_bkp_config_asa_context.py
  
The script will connect to each ASA device and perform the configuration backup. 

Each context will be saved in a separate file.

The filename is structed as: bkp-asa-<IP>-<context-name>
