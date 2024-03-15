import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from netaddr import IPNetwork
from datetime import datetime

def check_ssh_port(ip, progress_callback, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, 22))
            progress_callback()
            return result == 0
    except Exception as e:
        print(f"Error while checking {ip}: {e}")
        return False

def scan_ips(ips, progress_callback, timeout=1):
    subnet_ssh_open_hosts = []
    total_ips = len(ips)
    scanned_ips = 0

    def local_progress_callback():
        nonlocal scanned_ips
        scanned_ips += 1
        progress_callback(scanned_ips, total_ips)

    with ThreadPoolExecutor(max_workers=1000) as executor:
        futures = {executor.submit(check_ssh_port, str(ip), local_progress_callback, timeout): str(ip) for ip in ips}
        
        for future in as_completed(futures):
            ip = futures[future]
            if future.result():
                subnet_ssh_open_hosts.append(ip)
    
    return subnet_ssh_open_hosts

def print_progress(scanned_ips, total_ips):
    progress = scanned_ips / total_ips * 100
    print(f"\rProgress: [{'#' * int(progress / 2)}{' ' * (50 - int(progress / 2))}] {progress:.2f}% ({scanned_ips}/{total_ips} IP(s) scanned)", end='', flush=True)

def ssh_subnet_scanner(subnets):
    ssh_open_hosts = []
    start_time = datetime.now()
    print("***START SSH SUBNET SCAN***")
    ips = set()
    for subnet in subnets:
        ips = ips.union(IPNetwork(subnet))
    
    print(f"\n")
    subnet_ssh_open_hosts = scan_ips(ips, lambda scanned_ips, total_ips: print_progress(scanned_ips, total_ips))
    print()
    ssh_open_hosts.extend(subnet_ssh_open_hosts)

    sorted_ip_addresses = sorted(ssh_open_hosts, key=lambda ip: tuple(map(int, ip.split('.'))))        
    end_time = datetime.now()
    print("\n***********************************")    
    print("SSH Scan Time: ", end_time - start_time)
    print("Found " + str(len(sorted_ip_addresses)) + " IP(s) with port 22 enabled")
    print("***********************************\n")
    print("***END SSH SUBNET SCAN***\n")

    return sorted_ip_addresses
