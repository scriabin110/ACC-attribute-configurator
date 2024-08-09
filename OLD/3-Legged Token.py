import requests
import webbrowser

# Autodeskアプリケーションの設定
client_id = 'm6caOI8GGlylZY8FHGMtIWZvGiXUMZ6E3P6RLvEeGP6EpRjo'
client_secret = 'xKFPThA7G2ZuOUvAZiZyiaoVA5Gws4mRA2NxEClz9GQ58utQEBKDDT0diA3PhBAN'
redirect_uri = 'http://localhost:8080/api/auth/callback'
auth_url = 'https://developer.api.autodesk.com/authentication/v2/authorize'
token_url = 'https://developer.api.autodesk.com/authentication/v2/token'

# 1. 認証URLを生成
scope = 'data:read'
auth_params = f'?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}'
auth_url_with_params = auth_url + auth_params

print(f'認証URL: {auth_url_with_params}')

# 2. ブラウザで認証URLを開く
webbrowser.open(auth_url_with_params)

# 3. ユーザーに認証コードの入力を求める
code = input('認証後にリダイレクトされたURLからコードを抽出し、ここに入力してください: ')

# 4. トークンを取得するリクエストを送信
data = {
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': redirect_uri
}

response = requests.post(token_url, data=data, auth=(client_id, client_secret))

# 5. トークンの取得結果を確認
if response.status_code == 200:
    tokens = response.json()
    print('アクセストークン:', tokens['access_token'])
    print('リフレッシュトークン:', tokens['refresh_token'])
else:
    print('トークンの取得に失敗しました:', response.status_code, response.text)