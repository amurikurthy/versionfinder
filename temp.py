import subprocess

def ping_host(host):
    """
    Ping a host and return True if the host is reachable, False otherwise.
    """
    # Use the ping command with count 1
    result = subprocess.run(['ping', '-c', '1', host], capture_output=True, text=True)
    
    # Check the return code to determine if the ping was successful
    return result.returncode == 0

# Example usage:
host = 'google.com'
if ping_host(host):
    print(f"{host} is reachable.")
else:
    print(f"{host} is unreachable.")
