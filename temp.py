import requests

# Token endpoint provided by Cisco
url = 'https://id.cisco.com/oauth2/default/v1/token'

# Client ID and Client Secret
client_id = ''
client_secret = ''

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
    print("Access Token:", access_token)
    print("Expires In:", expires_in, "seconds")
else:
    print("Failed to retrieve access token:", response.status_code, response.text)


# Your API key
api_key = response.json()['access_token']

# Endpoint URL for EoX API
url = 'https://apix.cisco.com/supporttools/eox/rest/5/EOXByProductID/1/{product_id}'

# Replace '{product_id}' with the actual product ID you want to query
product_id = ''
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
    print(eox_data)
else:
    # Handle request error
    print('Failed to retrieve data:', response.status_code)

