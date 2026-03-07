# Python IP Calculator

A simple Python script that calculates network information from an IP address and subnet mask using the built-in `ipaddress` module.

## Features

The script calculates:

- Network address
- First usable IP
- Last usable IP
- Broadcast address
- Subnet mask
- Prefix length
- Wildcard mask
- Total number of addresses
- Number of valid host addresses
- Network range

It accepts subnet masks in two formats:

- CIDR notation → `192.168.1.10/24`
- Dotted decimal → `192.168.1.10/255.255.255.0`

## Requirements

- Python 3.x

The script only uses Python standard libraries:

- `ipaddress`
- `sys`

No external packages are required.

## Usage

Run the script from the terminal and pass the IP address as an argument.

```bash
python3 ip_calc.py 192.168.1.10/24