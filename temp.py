def is_port_open(host, port):
    """
    Check if a port is open on a remote host using netcat (nc) command.
    
    Args:
        host (str): The hostname or IP address of the remote host.
        port (int): The port number to check.

    Returns:
        bool: True if the port is open, False otherwise.
    """
    # Use the nc command to attempt a connection to the host and port
    result = subprocess.run(['nc', '-z', '-v', '-w', '2', host, str(port)], capture_output=True, text=True)
    
    # Check the return code to determine if the port is open
    return result.returncode == 0
