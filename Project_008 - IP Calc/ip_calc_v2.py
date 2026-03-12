import ipaddress
import sys

if len(sys.argv) < 2:
    print("Usage: python3 script.py <ip/prefix> [new_prefix]")
    sys.exit()

ip_input = sys.argv[1]

try:
    ip_add = ipaddress.ip_interface(ip_input)
    network = ip_add.network

    print(f"The IP typed is: {ip_add.with_netmask} : \n")

    first_usable_ip = network.network_address + 1
    last__usable_ip = network.broadcast_address - 1

    print(f"   - Network address: {network.network_address}")
    print(f"   - First usable IP: {first_usable_ip}")
    print(f"   - Last usable IP: {last__usable_ip}")
    print(f"   - Broadcast: {network.broadcast_address}")

    print(f"   - Mask: {ip_add.netmask} or /{network.prefixlen}")
    print(f"   - Wildcard: {ip_add.hostmask}")
    print(f"   - Number of addresses: {network.num_addresses}")
    print(f"   - Valid number of addresses: {network.num_addresses - 2}")

    print(f"   - Network range: {network.network_address} - {network.broadcast_address}")

    # Split network if second argument exists
    if len(sys.argv) > 2:
        new_prefix = int(sys.argv[2])

        if new_prefix >= 0 and new_prefix <= 32 and new_prefix > network.prefixlen:
            print(f"\nSplitting {network} into /{new_prefix} subnets:")

            for subnet in network.subnets(new_prefix=new_prefix):
                print(f" - {subnet}")
        else:
            print(f"*Invalid new prefix")

except ValueError:
    print("*Invalid IP address or mask")