import requests
from flask import Flask, request, redirect, session
import urllib.parse

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッション用の秘密鍵を設定

# Autodeskアプリケーションの認証情報
client_id = 'm6caOI8GGlylZY8FHGMtIWZvGiXUMZ6E3P6RLvEeGP6EpRjo'
client_secret = 'xKFPThA7G2ZuOUvAZiZyiaoVA5Gws4mRA2NxEClz9GQ58utQEBKDDT0diA3PhBAN'
callback_url = 'http://localhost:8080/api/auth/callback'  # コールバックURLを設定
scopes = ['data:create', 'data:read', 'data:write']

@app.route('/')
def home():
    # 認証URLを生成
    auth_url = f"https://developer.api.autodesk.com/authentication/v2/authorize?response_type=code&client_id={client_id}&redirect_uri={urllib.parse.quote_plus(callback_url)}&scope={' '.join(scopes)}"
    return f'<a href="{auth_url}">Autodeskで認証</a>'

@app.route('/callback')
def callback():
    # 認証コードを取得
    code = request.args.get('code')
    
    # アクセストークンを取得
    token_url = 'https://developer.api.autodesk.com/authentication/v2/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': callback_url
    }
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data['access_token']
        refresh_token = token_data['refresh_token']
        
        # トークンをセッションに保存
        session['access_token'] = access_token
        session['refresh_token'] = refresh_token
        
        return f'認証成功！アクセストークン: {access_token}'
    else:
        return 'トークンの取得に失敗しました。'

if __name__ == '__main__':
    app.run(debug=True)