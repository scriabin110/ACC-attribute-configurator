import requests
import base64
import webbrowser
import streamlit as st
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import threading
import config
import time
import os

# Streamlit Cloudで動作しているかどうかを確認
is_streamlit_cloud = os.environ.get('STREAMLIT_CLOUD') == 'true'

if is_streamlit_cloud:
    # Streamlit Cloudで動作している場合の設定
    CLIENT_ID = st.secrets["CLIENT_ID"]
    CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
    CALLBACK_URL = st.secrets["CALLBACK_URL"]
else:
    # ローカル環境での設定
    CLIENT_ID = config.CLIENT_ID
    CLIENT_SECRET = config.CLIENT_SECRET
    CALLBACK_URL = config.CALLBACK_URL

# グローバル変数で認証コードを保存
auth_code = None
SCOPES = ['data:read', 'data:write', 'data:create']

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
    auth_url = f"https://developer.api.autodesk.com/authentication/v2/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote_plus(CALLBACK_URL)}&scope={' '.join(SCOPES)}"
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
        'redirect_uri': CALLBACK_URL
    }
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
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