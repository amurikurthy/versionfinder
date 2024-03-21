import ipaddress
from netaddr import IPNetwork
from datetime import datetime

def ip_cleaner(subnets):
    ssh_open_hosts = []
    start_time = datetime.now()
    print("\n***********************************")  
    print("***START IP CLEAN***")
    ips = set()
    for subnet in subnets:
        if "/" in subnet:
            ips = ips.union(IPNetwork(subnet))
        else:
            ips = ips.union(ipaddress.IPv4Network(subnet + '/32', strict=False))

    sorted_ip_addresses = sorted(ips, key=lambda ip: tuple(map(int, str(ip).split('.'))))        
    end_time = datetime.now()
    print("-----------------------------------")    
    print("IP CLEAN Time: ", end_time - start_time)
    print("Found " + str(len(sorted_ip_addresses)) + " unique IP(s)")
    print("-----------------------------------")  
    print("***END IP CLEAN***")
    print("***********************************\n")

    return sorted_ip_addresses
