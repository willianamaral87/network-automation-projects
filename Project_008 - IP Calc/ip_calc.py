import ipaddress

import sys

ip = sys.argv[1]

try:
    #ip = input("Type the IP address + subnet mask:")

    #ip = "192.168.1.10/24"

    # ip_interface can identify if the IP is on thew format /XX or mask xxx.xx.xx.xx.
    # Accepts an IP address combined with a subnet mask in either CIDR prefix format (/24) or dotted decimal format (/255.255.255.0) 
    # and converts it into an interface object that contains the IP address and its associated network information.

    ip_add = ipaddress.ip_interface(ip)

    print(f"The IP typed is:  { ip_add.with_netmask } ")

    first_ip = ip_add.network.network_address + 1
    last_ip = ip_add.network.broadcast_address - 1

    print(f"   - Network address: { ip_add.network.network_address } ")
    print(f"   - First IP { first_ip} ")
    print(f"   - Last IP: { last_ip } ")  
    print(f"   - Broadcast: { ip_add.network.broadcast_address } ")  

    print(f"   - Mask: { ip_add.netmask} or /{ ip_add.network.prefixlen }")
    print(f"   - Wildcard: { ip_add.hostmask} ")
    print(f"   - Number of addresses: { ip_add.network.num_addresses } ")
    print(f"   - Valid Number of address: { ip_add.network.num_addresses - 2} ")


    print(f"   - Network range: { ip_add.network.network_address } - { ip_add.network.broadcast_address }  ")

except:
    print("Invalid IP address or mask")
