import requests
from flask import Flask, request, redirect, session
import urllib.parse
import webbrowser
import threading
import time

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
    return f'''
    <html>
        <head>
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    font-family: Arial, sans-serif;
                }}
                a {{
                    font-size: 18px;
                    padding: 10px 20px;
                    background-color: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <a href="{auth_url}">Autodeskで認証</a>
        </body>
    </html>
    '''

@app.route('/api/auth/callback')
def callback():
    # 認証コードを取得
    code = request.args.get('code')
    
    if code:
        # 認証コードを表示
        return f'''
        <html>
            <head>
                <style>
                    body {{
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        font-family: Arial, sans-serif;
                    }}
                    .code {{
                        font-size: 18px;
                        padding: 20px;
                        background-color: #f0f0f0;
                        border-radius: 5px;
                        margin-bottom: 20px;
                    }}
                    .copy-button {{
                        font-size: 16px;
                        padding: 10px 20px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                    }}
                </style>
            </head>
            <body>
                <div class="code">認証コード: <span id="auth-code">{code}</span></div>
                <button class="copy-button" onclick="copyToClipboard()">コードをコピー</button>
                
                <script>
                    function copyToClipboard() {{
                        var codeElement = document.getElementById('auth-code');
                        var textArea = document.createElement('textarea');
                        textArea.value = codeElement.textContent;
                        document.body.appendChild(textArea);
                        textArea.select();
                        document.execCommand('copy');
                        document.body.removeChild(textArea);
                        alert('認証コードがクリップボードにコピーされました。');
                    }}
                </script>
            </body>
        </html>
        '''
    else:
        return '''
        <html>
            <head>
                <style>
                    body {{
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        font-family: Arial, sans-serif;
                    }}
                    .error {{
                        color: red;
                        font-size: 18px;
                    }}
                </style>
            </head>
            <body>
                <div class="error">エラー: 認証コードが取得できませんでした。</div>
            </body>
        </html>
        '''

def open_browser():
    time.sleep(1)  # サーバーが起動するのを少し待つ
    webbrowser.open('http://localhost:8080')

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(host='localhost', port=8080, debug=True)