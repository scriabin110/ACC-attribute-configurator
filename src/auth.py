import requests
import base64
import streamlit as st
import urllib.parse
import time

CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
CALLBACK_URL = st.secrets["CALLBACK_URL"]

SCOPES = ['data:read', 'data:write', 'data:create', 'account:read', 'account:write']

def get_auth_code():
    auth_url = f"https://developer.api.autodesk.com/authentication/v2/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote_plus(CALLBACK_URL)}&scope={' '.join(SCOPES)}"
    st.link_button("Authenticate", auth_url)
    auth_code = st.text_input("認証コードを入力してください:")
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

def get_2_legged_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET):
    token_url = 'https://developer.api.autodesk.com/authentication/v2/token'
    token_data = {
        'grant_type': 'client_credentials',
        'scope': 'account:read'  # スコープは必要に応じて調整してください
    }
    
    auth_string = f"{client_id}:{client_secret}"
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
        raise Exception('トークン取得エラー: ' + response_data.get('developerMessage', ''))