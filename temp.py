def connect_with_retry(device, max_retries=3, retry_delay=5):
    """
    Connect to a network device using Netmiko with retry mechanism.

    Args:
        device (dict): Dictionary containing device parameters for Netmiko connection.
        max_retries (int): Maximum number of connection retries (default is 3).
        retry_delay (int): Delay in seconds between retries (default is 5).

    Returns:
        ConnectHandler: Netmiko SSH connection handler upon successful connection.

    Raises:
        Exception: If unable to establish a connection after maximum retries.
    """
    for attempt in range(1, max_retries + 1):
        print(f"Attempt {attempt} to connect to {device['ip']}...")

        try:
            # Attempt to connect to the device
            net_connect = ConnectHandler(**device)
            print(f"Connected to {device['ip']} successfully!")
            return net_connect

        except Exception as e:
            # Failed to connect due to any exception
            print(f"Failed to connect to {device['ip']}: {e}")
            if attempt < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)  # Wait before retrying
            else:
                print("Maximum retries reached. Unable to connect.")
                raise  # Re-raise the exception if max retries reached
