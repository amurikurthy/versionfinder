import paramiko
import socket

def get_ssh_host_key(host, port=22, timeout=10):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    try:
        client.connect(hostname=host, port=port, username='dummy', password='dummy', timeout=timeout, allow_agent=False, look_for_keys=False)
    except paramiko.ssh_exception.SSHException as e:
        if "No authentication methods available" in str(e) or "Authentication failed." in str(e):
            key = client.get_transport().get_remote_server_key()
            return host, key.get_name(), key.get_bits()
    except (socket.timeout, socket.error):
        return host, 'Connection Failed', None
    finally:
        client.close()

    return host, None, None

# List of hosts to check
hosts = ['192.168.1.1', '192.168.1.2', 'example.com']  # Replace or extend with your actual host list

# Collect key info from each host
for host in hosts:
    ip, algorithm, key_size = get_ssh_host_key(host)
    if algorithm:
        print(f"Host: {ip}, Key Algorithm: {algorithm}, Key Size: {key_size} bits")
    else:
        print(f"Host: {ip}, Error: {key_size}")

