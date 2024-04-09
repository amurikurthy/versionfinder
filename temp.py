from netmiko import ConnectHandler
import difflib

# Device information
device = {
    "device_type": "cisco_ios",
    "host": "your_device_ip",
    "username": "your_username",
    "password": "your_password",
}

# Connect to the device
net_connect = ConnectHandler(**device)
net_connect.enable()

# Get the running configuration
running_config = net_connect.send_command("show running-config")

# Get the startup configuration
startup_config = net_connect.send_command("show startup-config")

# Close the connection
net_connect.disconnect()

# Split configurations into lines
running_lines = running_config.splitlines()
startup_lines = startup_config.splitlines()

# Add labels to each set of lines
running_labeled = [f'- Running: {line}' for line in running_lines]
startup_labeled = [f'+ Startup: {line}' for line in startup_lines]

# Compare the configurations
diff = difflib.unified_diff(running_labeled, startup_labeled, lineterm='')

# Print the differences
print('\n'.join(diff))
