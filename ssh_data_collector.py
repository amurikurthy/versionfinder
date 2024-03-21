import socket
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from netmiko import ConnectHandler, exceptions, SSHDetect
from napalm import get_network_driver
from datetime import datetime


def check_ip_address(ip, progress_callback,  username, password):
    try:
        ip_dict = {
            "device_type": "autodetect",
            "host": ip,
            "username": username,
            "password": password,
        }
        progress_callback()
        guesser = SSHDetect(**ip_dict)
        best_match = guesser.autodetect()
        if best_match == "cisco_nxos":
            ip_dict["device_type"] = "nxos_ssh"
        elif best_match == "cisco_ios":
            ip_dict["device_type"] = "ios"

            
        if ip_dict["device_type"] != "autodetect":
            driver = get_network_driver(ip_dict["device_type"])
            device = driver(ip_dict["host"], username, password, optional_args={'port': 22})
            device.open()
            device_facts = device.get_facts()
            device_facts.pop("interface_list")
            device_facts["ip_address"] = ip
            device.close()
            progress_callback()
            return device_facts
        else:
            print("\nUnknown OS Skipping...")
        
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

def ssh_data_collector(ip_addresses, username, password):

    start_time = datetime.now()
    print("\n***********************************")  
    print("***START SSH DATA COLLECTOR***")
    print("***********************************")  
    
    print(f"\n")
    device_info, duplicate_counter, auth_fail_counter = process_ip(ip_addresses, username, password, lambda scanned_ips, total_ips: print_progress(scanned_ips, total_ips))
    print_progress(1, 1)
    print()
      
    end_time = datetime.now()
    print("\n***********************************")  
    print("-----------------------------------") 
    print("SSH DATA COLLECTOR Time: ", end_time - start_time)
    print("Found " + str(auth_fail_counter) + " failed auth IP(s)")
    print("Found " + str(duplicate_counter) + " duplicate device IP(s)")
    print("-----------------------------------")    
    print("***END SSH DATA COLLECTOR***")
    print("***********************************\n")
    return device_info
