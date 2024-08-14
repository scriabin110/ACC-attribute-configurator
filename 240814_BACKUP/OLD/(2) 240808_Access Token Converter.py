import requests

url = "https://developer.api.autodesk.com/authentication/v2/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "client_id": "m6caOI8GGlylZY8FHGMtIWZvGiXUMZ6E3P6RLvEeGP6EpRjo",
    "client_secret":"xKFPThA7G2ZuOUvAZiZyiaoVA5Gws4mRA2NxEClz9GQ58utQEBKDDT0diA3PhBAN",
    "grant_type": "authorization_code",
    "code": "EHZjP3l7mQoS7GkcxSm1lcBGwuzYDipvArlK7O7m",
    "redirect_uri": "http://localhost:8080/api/auth/callback"
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    token_data = response.json()
    access_token = token_data["access_token"]
    print(f"Access Token: {access_token}")
else:
    print(f"Error: {response.status_code}, {response.text}")