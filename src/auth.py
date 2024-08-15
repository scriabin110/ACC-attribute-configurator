import requests
import base64
import webbrowser
import streamlit as st
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import threading
import config
import time

# グローバル変数で認証コードを保存
auth_code = None
SCOPES = ['data:read', 'data:write', 'data:create']

# CallbackHandler, start_server, get_auth_code, get_access_token 関数をここに配置
class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        auth_code = params.get('code', [None])[0]
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Authentication successful! You can close this window now.')

def start_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, CallbackHandler)
    httpd.handle_request()

def get_auth_code():
    auth_url = f"https://developer.api.autodesk.com/authentication/v2/authorize?response_type=code&client_id={config.CLIENT_ID}&redirect_uri={urllib.parse.quote_plus(config.CALLBACK_URL)}&scope={' '.join(SCOPES)}"
    # st.write(f"ブラウザで認証ページを開きます。認証後、自動的にコードが取得されます。")
    # st.write(f"認証URL: {auth_url}")
    # st.write("認証が完了したら、このページに戻ってきてください。")
    webbrowser.open_new(auth_url)
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    server_thread.join()
    return auth_code

def get_access_token(auth_code):
    token_url = 'https://developer.api.autodesk.com/authentication/v2/token'
    token_data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': config.CALLBACK_URL
    }
    auth_string = f"{config.CLIENT_ID}:{config.CLIENT_SECRET}"
    auth_bytes = auth_string.encode('ascii')
    base64_bytes = base64.b64encode(auth_bytes)
    base64_string = base64_bytes.decode('ascii')
    headers = {
        'Authorization': f'Basic {base64_string}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(token_url, data=token_data, headers=headers)
    response_data = response.json()
    if response.status_code == 200:
        return response_data['access_token']
    else:
        raise Exception('Token取得エラー: ' + response_data.get('developerMessage', ''))