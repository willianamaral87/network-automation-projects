# Import regex
import re

# This module can be used to validate the hostname of the devices.


# How to use it ?
# On the main code import this module, like:
# from validate_name_convention import (
#    validate_trunk_uplink_pattern,
#    validate_trunk_downlink_pattern,
#    validate_trunk_access_point_pattern,
#    validate_access_port_pc_pattern,
#    validate_access_port_printer_pattern,
#    validate_access_port_time_clock_pattern,
#)

# The argument must be a description and the each function will return True or False
# validate_trunk_uplink_pattern(description):
# return True or False


################ TRUNK PORT - UPLINK ################
# Trunk uplink ports must have a description that follows this pattern:
# "^ TRUNK_UPLINK_[A-Z]{3}-[A-Z]{4,15}-SW(0{0,2}[1-9]|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5])$"
# - Starts with: TRUNK_UPLINK_
# - Followed by exactly 3 uppercase letters (site code)
# - Hyphen (-)
# - Followed by 4 to 15 uppercase letters (location or area name)
# - Hyphen (-)
# - Ends with SW plus a switch number from 1 to 255
#   (leading zeros allowed: 1, 01, 001, 20, 020, etc.)
# Ex: TRUNK_UPLINK_COUNTRY-SITE-LOCATION-DEVICE+FINALIP
# description TRUNK_UPLINK_AR-ROS-OFFICE-SW10

def validate_trunk_uplink_pattern(description):
    trunk_uplink_pattern = re.compile(r"^ TRUNK_UPLINK_[A-Z]{2}-[A-Z]{3}-[A-Z]{4,15}-SW(0{0,2}[1-9]|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5])$")

    if trunk_uplink_pattern.match(description):
        return True
    else:
        return False


################ TRUNK PORT - DOWNLINK ################
# The same as uplink port, but considering downlink port.
# Ex: TRUNK_DOWNLINK_COUNTRY-SITE-LOCATION-DEVICE+FINALIP
# description TRUNK_DOWNLINK_AR-ROS-OFFICE-SW10

def validate_trunk_downlink_pattern(description):
    regex_decription = re.compile(r"^ TRUNK_DOWNLINK_[A-Z]{2}-[A-Z]{3}-[A-Z]{4,15}-SW(0{0,2}[1-9]|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5])$")

    if regex_decription.match(description):
        return True
    else:
        return False


################ TRUNK PORT - ACCESS POINT ################
# The same as uplink port, but considering access point port.
# Ex: description ACCESS_POINT_AR-ABC-FINANCE-AP10
def validate_trunk_access_point_pattern(description):
    regex_decription = re.compile(
    r"^ ACCESS_POINT_[A-Z]{2}-[A-Z]{3}-[A-Z]{4,15}-AP(0{0,2}[1-9]|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5])$")

    if regex_decription.match(description):
        return True
    else:
        return False


################ ACCESS PORT for Computer or Laptop ################
# Access port for PC  should have the description following the pattern:
# Access ports for PCs must have a description that follows this pattern:
# "^ACCESS_PORT_PC_[A-Z]{3,10}[0-9]{0,5}$"
# - Starts with: ACCESS_PORT_PC_
# - Followed by a word containing 3 to 10 letters - location
# - Optionally followed by up to 5 digits
# Ex: description ACCESS_PORT_PC_NAME10

def validate_access_port_pc_pattern(description):
    regex_decription = re.compile(r"^ ACCESS_PORT_PC_[A-Z]{3,10}[0-9]{0,5}$")

    if regex_decription.match(description):
        return True
    else:
        return False


################ ACCESS PORT for Printer ################
# The same as before but considering Printer insted of Computer or Laptop
# Ex: description ACCESS_PORT_PRINTER_FINANCE10

def validate_access_port_printer_pattern(description):
    regex_decription = re.compile(r"^ ACCESS_PORT_PRINTER_[A-Z]{3,10}[0-9]{0,5}$")

    if regex_decription.match(description):
        return True
    else:
        return False


################ ACCESS PORT for Time Clock ################
# The same as before but considering Clock Time insted of Computer or Laptop or printer
# Ex: description description ACCESS_PORT_TIME_CLOCK_NAME10"

def validate_access_port_time_clock_pattern(description):
    regex_decription = re.compile(r"^ ACCESS_PORT_TIME_CLOCK_[A-Z]{3,10}[0-9]{0,5}$")

    if regex_decription.match(description):
        return True
    else:
        return False



