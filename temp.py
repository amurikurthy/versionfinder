import paramiko
import sys

def get_ssh_key_info(hostname, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, port=port, username='username', password='password', look_for_keys=False, allow_agent=False)
    except Exception as e:
        print(f"Failed to connect to {hostname}: {str(e)}")
        return

    # Retrieve the host key and print information about each available key
    host_keys = client.get_host_keys()
    if hostname in host_keys:
        for key_type, key in host_keys[hostname].items():
            print(f"Host Key Type: {key.get_name()}")
            print(f"Key Size: {key.get_bits()} bits")
    else:
        print("No host key found.")

    client.close()

# Replace 'hostname' with the actual hostname you want to connect to
get_ssh_key_info('hostname')
