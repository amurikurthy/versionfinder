def get_eol_data(serial_numbers, api_key):
    """
    Fetches EoL data for a list of Cisco product serial numbers.

    Args:
        serial_numbers (list): A list of serial numbers of Cisco products.
        api_key (str): Your Cisco API key.

    Returns:
        dict: EoL data for the provided serial numbers.
    """
    url = 'https://api.cisco.com/supporttools/eox/rest/5/EOXBySerialNumber/1'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {'serialNumbers': serial_numbers}
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to retrieve data:', response.status_code)
        return {}

# Example usage:
api_key = 'your_cisco_api_key_here'
serial_numbers = ['serial_number_1', 'serial_number_2']
eol_data = get_eol_data(serial_numbers, api_key)
print(eol_data)
