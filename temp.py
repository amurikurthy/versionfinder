import paramiko

def get_ssh_key_info(hostnames, port=22, username='username', password='password'):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for hostname in hostnames:
        try:
            client.connect(hostname, port=port, username=username, password=password, look_for_keys=False, allow_agent=False)
            print(f"\nConnected to {hostname}...")
            # Retrieve the host key and print information about each available key
            host_keys = client.get_host_keys()
            if hostname in host_keys:
                for key_type, key in host_keys[hostname].items():
                    print(f"Host Key Type: {key.get_name()}")
                    print(f"Key Size: {key.get_bits()} bits")
            else:
                print("No host key found.")
        except Exception as e:
            print(f"Failed to connect to {hostname}: {str(e)}")
        finally:
            client.close()

# List of hostnames to connect to
hostnames = ['hostname1', 'hostname2', 'hostname3']
get_ssh_key_info(hostnames)
