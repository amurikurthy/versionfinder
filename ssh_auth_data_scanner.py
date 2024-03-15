import socket
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from netmiko import ConnectHandler, exceptions
from napalm import get_network_driver
from datetime import datetime



# Function to identify Cisco operating system based on output
def identify_os_driver(output):
    if "Cisco IOS" in output:
        return "ios"
    elif "Cisco Nexus Operating System (NX-OS) Software" in output:
        return "nxos_ssh"
    elif "VyOS" in output:
        return "vyos"
    else:
        return "Unknown"


def check_ip_address(ip, progress_callback,  username, password):
    try:
        ip_dict = {
            "device_type": "generic",
            "host": ip,
            "username": username,
            "password": password,
        }
        progress_callback()
        connection = ConnectHandler(**ip_dict)
        command_output = connection.send_command("show version")
        connection.disconnect()
        operating_system = identify_os_driver(command_output)
        
        if operating_system != "Unknown":
            driver = get_network_driver(operating_system)
            device = driver(ip_dict["host"], username, password, optional_args={'port': 22})
            device.open()
            device_facts = device.get_facts()
            #print("")
            #print("Serial Number:", device_facts['serial_number'])
            #print("IP:", ip_dict["host"])
            #print("Hostname:", device_facts['hostname'])
            #print("Vendor:", device_facts['vendor'])
            #print("Model:", device_facts['model'])
            #print("Operating System Version:", device_facts['os_version'])
            
            keys_to_keep = ["hostname", "serial_number", "vendor", "model", "os_version"]
            device_info = {key: device_facts[key] for key in keys_to_keep if key in device_facts}
            
            device.close()
            progress_callback()
            return device_info
        else:
            print("Unknown OS Skipping...")
        
    except exceptions.NetmikoAuthenticationException:
        progress_callback()
        return False
        
    except Exception as e:
        pass

    

def process_ip(ip_addresses, username, password, progress_callback, timeout=1):
    device_info = []
    total_ips = len(ip_addresses)
    scanned_ips = 0
    duplicate_counter = 0
    auth_fail_counter = 0

    def local_progress_callback():
        nonlocal scanned_ips
        scanned_ips += 0.5
        progress_callback(scanned_ips, total_ips)
    
    with ThreadPoolExecutor(max_workers=1000) as executor:
        futures = {executor.submit(check_ip_address, str(ip), local_progress_callback, username, password): str(ip) for ip in ip_addresses}
        
        for future in as_completed(futures):
            if future.result() == False:
                auth_fail_counter += 1
            elif future.result() != None and future.result() not in device_info:
                device_info.append(future.result())
            else:
                duplicate_counter += 1
    return device_info, duplicate_counter, auth_fail_counter

def print_progress(scanned_ips, total_ips):
    progress = scanned_ips / total_ips * 100
    print(f"\rProgress: [{'#' * int(progress / 2)}{' ' * (50 - int(progress / 2))}] {progress:.2f}%", end='', flush=True)
    if scanned_ips/total_ips == 0.5:
        print(f" (Waiting For Threads)", flush=True)

def ssh_auth_data_scanner(ip_addresses, username, password):

    start_time = datetime.now()
    print("***START SSH SUBNET DATA SCAN***")

    
    print(f"\n")
    device_info, duplicate_counter, auth_fail_counter = process_ip(ip_addresses, username, password, lambda scanned_ips, total_ips: print_progress(scanned_ips, total_ips))
    print()
      
    end_time = datetime.now()
    print("\n***********************************")    
    print("SSH Scan Time: ", end_time - start_time)
    print("Found " + str(auth_fail_counter) + " failed auth IP(s)")
    print("Found " + str(duplicate_counter) + " duplicate device IP(s)")
    print("***********************************\n")    
    print("***END SSH SUBNET DATA SCAN***")
    return device_info