import requests
import base64
import webbrowser
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import threading

# Autodeskアプリケーションの認証情報
CLIENT_ID = 'm6caOI8GGlylZY8FHGMtIWZvGiXUMZ6E3P6RLvEeGP6EpRjo'
CLIENT_SECRET = 'xKFPThA7G2ZuOUvAZiZyiaoVA5Gws4mRA2NxEClz9GQ58utQEBKDDT0diA3PhBAN'
CALLBACK_URL = 'http://localhost:8080/api/auth/callback'
SCOPES = ['data:read', 'data:write', 'data:create']

# グローバル変数で認証コードを保存
auth_code = None

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
    
    print(f"ブラウザで認証ページを開きます。認証後、自動的にコードが取得されます。")
    webbrowser.open(auth_url)
    
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

if __name__ == '__main__':
    try:
        auth_code = get_auth_code()
        if auth_code:
            token = get_access_token(auth_code)
            print(f'取得したアクセストークン: {token}')
        else:
            print("認証コードの取得に失敗しました。")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")


# ========================================================================================================

def get_projects(access_token, hub_id):
    url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception(f"プロジェクト取得エラー: {response.text}")

def get_top_folders(access_token, hub_id, project_id):
    url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects/{project_id}/topFolders"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception(f"トップフォルダ取得エラー: {response.text}")

def get_folder_contents(access_token, project_id, folder_id):
    url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/folders/{folder_id}/contents"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception(f"フォルダ内容取得エラー: {response.text}")

def find_folder_by_name(access_token, project_id, parent_folder_id, target_folder_name):
    contents = get_folder_contents(access_token, project_id, parent_folder_id)
    for item in contents:
        if item['type'] == 'folders' and item['attributes']['name'] == target_folder_name:
            return item['id']
    return None

if __name__ == '__main__':
    try:
        auth_code = get_auth_code()
        if auth_code:
            token = get_access_token(auth_code)
            print(f'取得したアクセストークン: {token}')

            # ここから新しいコード
            hub_id = input("Hub IDを入力してください: ")
            projects = get_projects(token, hub_id)
            
            print("利用可能なプロジェクト:")
            for project in projects:
                print(f"- {project['attributes']['name']} (ID: {project['id']})")
            
            project_id = input("プロジェクトIDを入力してください: ")
            
            top_folders = get_top_folders(token, hub_id, project_id)
            print("\nトップレベルフォルダ:")
            for folder in top_folders:
                print(f"- {folder['attributes']['name']} (ID: {folder['id']})")
            
            target_folder_name = input("\n探したいフォルダ名を入力してください: ")
            
            for top_folder in top_folders:
                folder_id = find_folder_by_name(token, project_id, top_folder['id'], target_folder_name)
                if folder_id:
                    print(f"\n'{target_folder_name}'のフォルダID: {folder_id}")
                    break
            else:
                print(f"\n'{target_folder_name}'というフォルダは見つかりませんでした。")
            
            

        else:
            print("認証コードの取得に失敗しました。")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

