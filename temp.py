import requests

def fetch_eox_info_by_serial_number(serial_number, api_key):
    """
    Fetches EOX information for a given Cisco product serial number using the Cisco EOX API.

    Args:
        serial_number (str): The serial number of the Cisco product.
        api_key (str): Your Cisco API key.

    Returns:
        dict: The EOX information returned by the API.
    """
    url = f"https://apix.cisco.com/supporttools/eox/rest/5/EOXBySerialNumber/1/{serial_number}"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Failed to retrieve EOX data', 'status_code': response.status_code}

# Usage example
api_key = 'your_api_key_here'
serial_number = 'your_serial_number_here'
eox_info = fetch_eox_info_by_serial_number(serial_number, api_key)
print(eox_info)
