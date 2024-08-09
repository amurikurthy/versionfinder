import requests
import pandas as pd


def divide_pid_chunks(lst, n):
    # Loop to divide into chunks of size n
    for i in range(0, len(lst), n):
        yield ','.join(lst[i:i + n])

unique_child_pid_df = pd.read_excel('Cisco Child PID.xlsx')["Child PID"].unique()

pid_chunks = list(divide_pid_chunks(unique_child_pid_df, 20))

# Token endpoint provided by Cisco
url = 'https://id.cisco.com/oauth2/default/v1/token'

# Client ID and Client Secret


# Body parameters for the token request
body = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret
}

# Headers
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# POST request to get the token
response = requests.post(url, data=body, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    access_token = response.json()['access_token']
    expires_in = response.json()['expires_in']
else:
    print("Failed to retrieve access token:", response.status_code, response.text)


# Your API key
api_key = response.json()['access_token']

# Endpoint URL for EoX API
url = 'https://apix.cisco.com/supporttools/eox/rest/5/EOXByProductID/1/{product_id}'

eox_pids = []

for pid_chunk in pid_chunks:

    # Replace '{product_id}' with the actual product ID you want to query
    product_id = pid_chunk
    formatted_url = url.format(product_id=product_id)

    # Headers to include in the request
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Make the GET request
    response = requests.get(formatted_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response
        eox_data = response.json()
        for EOLProduct in eox_data["EOXRecord"]:
            if EOLProduct["EOLProductID"]:
                eox_pids.append(EOLProduct)

    else:
        # Handle request error
        print('Failed to retrieve data:', response.status_code)

eox_pids_df = pd.DataFrame(eox_pids)
