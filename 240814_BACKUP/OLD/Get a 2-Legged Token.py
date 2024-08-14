import base64

client_id = 'm6caOI8GGlylZY8FHGMtIWZvGiXUMZ6E3P6RLvEeGP6EpRjo'
client_secret = 'xKFPThA7G2ZuOUvAZiZyiaoVA5Gws4mRA2NxEClz9GQ58utQEBKDDT0diA3PhBAN'
combined = f"{client_id}:{client_secret}"
encoded = base64.b64encode(combined.encode()).decode()

import requests

url = 'https://developer.api.autodesk.com/authentication/v2/token'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f'Basic {encoded}'
}
data = {
    'grant_type': 'client_credentials',
    'scope': 'data:read'
}
response = requests.post(url, headers=headers, data=data)
token = response.json().get('access_token')

# JSON形式で表示
response_json = response.json()
print(response_json)
print("")

# Access_token のみ表示
print(token)
