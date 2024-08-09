import base64
import requests

# クライアントIDとクライアントシークレットをBase64エンコード
client_id = 'm6caOI8GGlylZY8FHGMtIWZvGiXUMZ6E3P6RLvEeGP6EpRjo'
client_secret = 'xKFPThA7G2ZuOUvAZiZyiaoVA5Gws4mRA2NxEClz9GQ58utQEBKDDT0diA3PhBAN'
encoded_credentials = base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()

# トークンを取得するためのリクエスト
url = 'https://developer.api.autodesk.com/authentication/v2/token'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'Authorization': f'Basic {encoded_credentials}'
}
data = {
    'grant_type': 'client_credentials',
    'scope': 'data:read'
}

response = requests.post(url, headers=headers, data=data)
token = response.json().get('access_token')
print(f'Access Token: {token}')

# 取得したアクセストークンを使用してAPIリクエストを実行
acc_url = 'https://developer.api.autodesk.com/project/v1/hubs'
acc_headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

acc_response = requests.get(acc_url, headers=acc_headers)
print(acc_response.json())

