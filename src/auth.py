import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import requests
import base64
import streamlit as st
import urllib.parse
import time

CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
CALLBACK_URL = st.secrets["CALLBACK_URL"]

SCOPES = ['data:read', 'data:write', 'data:create']

def get_auth_code():
    auth_url = f"https://developer.api.autodesk.com/authentication/v2/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote_plus(CALLBACK_URL)}&scope={' '.join(SCOPES)}"
    
    auth_code = [None]
    
    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            if 'code' in params:
                auth_code[0] = params['code'][0]
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                html_content = """
                <!DOCTYPE html>
                <html lang="ja">
                <head>
                    <meta charset="UTF-8">
                    <title>認証成功</title>
                </head>
                <body>
                    <h1>認証成功</h1>
                    <p>このページは閉じて構いません。</p>
                    <script>window.close();</script>
                </body>
                </html>
                """
                self.wfile.write(html_content.encode('utf-8'))

            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                error_content = """
                <!DOCTYPE html>
                <html lang="ja">
                <head>
                    <meta charset="UTF-8">
                    <title>エラー</title>
                </head>
                <body>
                    <h1>エラー</h1>
                    <p>認証コードが見つかりませんでした。</p>
                </body>
                </html>
                """
                self.wfile.write(error_content.encode('utf-8'))

    def run_server():
        server = HTTPServer(('localhost', 8080), RequestHandler)
        server.handle_request()

    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    webbrowser.open(auth_url)

    with st.spinner("認証中..."):
        while auth_code[0] is None:
            time.sleep(0.1)

    server_thread.join()

    return auth_code[0]

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