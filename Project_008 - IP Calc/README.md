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
- Subnetting

It accepts subnet masks in two formats:

- CIDR notation → `192.168.1.10/24`
- Dotted decimal → `192.168.1.10/255.255.255.0`

### Subnetting
The script can also **split a network into smaller subnets** by providing a second argument (`new_prefix`).

Example:
- Split `192.168.0.0/23` into `/24` subnets.

Output:
```
192.168.0.0/24
192.168.1.0/24
```

## Requirements

- Python 3.x

The script only uses Python standard libraries:

- `ipaddress`
- `sys`

No external packages are required.

## Usage

Run the script from the terminal and pass the IP address as an argument.

### Basic usage
```bash
python3 ip_calc.py 192.168.1.10/24
```

### Subnetting 

```
python3 ip_calc.py 192.168.0.0/23 24
```

## Notes
- Uses Python's built-in `ipaddress` module for validation and calculations.