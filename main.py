from ssh_subnet_scanner import ssh_subnet_scanner
from ssh_auth_data_scanner import ssh_auth_data_scanner
from datetime import datetime


start_time = datetime.now()

subnets = ["192.168.99.0/24"]

ip_addresses = ssh_subnet_scanner(subnets)

device_info = ssh_auth_data_scanner(ip_addresses, "***", "***")

for device in device_info:
    print("Hostname:", device["hostname"])
    print("OS Version:", device["os_version"])
    print("\n")


end_time = datetime.now()
print("\n***********************************")    
print("Total Time: ", end_time - start_time)
print("***********************************\n")    