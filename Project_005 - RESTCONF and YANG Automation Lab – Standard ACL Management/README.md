# RESTCONF & YANG Automation Lab – Standard ACL Lifecycle Management

## 1. Project Goal

The goal of this laboratory is to demonstrate programmatic management of Standard Access Control Lists (ACLs) on Cisco IOS-XE using RESTCONF and YANG models.

This project focuses on implementing the full configuration lifecycle (create, read, update and delete) through Python-based network automation.

## 2. Objectives
* Use RESTCONF to interact with Cisco IOS-XE devices
* Understand and navigate YANG data models
* Automate Standard ACL creation and modification
* Apply and remove ACLs from Line VTY
* Separate inventory data from business logic
* Improve automation reliability with structured error handling

## 3. Lab Environment
* 2 DevAsc Virtual Machines (Cisco CSR1000V with IOS XE Software - Version 17.03.04a)
* RESTCONF enabled on IOS-XE
* Python used as the orchestration layer

## 4. Project Architecture
The project is structured into 8 modular Python scripts, each responsible for a specific operation:

### ACL Management
- Retrieves existing Standard ACLs from the device:
  - script-1_get_acl_standard.py
- Creates a new Standard ACL using RESTCONF:
  - script-2_create_acl_standard.py
- Deletes an existing Standard ACL:
  - script-3_delete_acl_standard.py
- Deletes a specific entry within a Standard ACL:
  - script-7_delete_acl_line_standard.py
- Adds a new entry to an existing Standard ACL:
  - script-8_create_new_line_on_existent_acl.py

###  ACL Application to Line VTY
- Retrieves the ACL currently applied to Line VTY.
  - script-4_get_acl_applied_vty.py
- Applies a previously created ACL to Line VTY.
  - script-5_apply_acl_line_to_vty.py
- Removes the ACL from Line VTY:
  - script-6_remove_acl_applied_vty.py

## 5. How to Set Up the Laboratory?
- Start the DevAsc VM.
- Download the script from GitHub.
- If necessary, install the dependencies.
- Enable Restconf and HTTPS on the devices.
- Update the inventory file using the Virtual Machines' IP addresses or the real IP addresses of the switches.

## Notes
These scripts are compatible with IOS-XE version 17.03.04a.  
For different versions, check the GitHub link.

## References:
- https://github.com/YangModels/yang/
- www.autonetops.com

