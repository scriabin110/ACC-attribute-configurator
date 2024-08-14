import requests
import base64
import webbrowser
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import threading
import config
import json

# Autodeskアプリケーションの認証情報
CLIENT_ID = config.CLIENT_ID
CLIENT_SECRET = config.CLIENT_SECRET
CALLBACK_URL = config.CALLBACK_URL
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
        return response.json().get('data', [])
    else:
        print(f"Warning: Unable to retrieve folder contents. Status code: {response.status_code}")
        return []

def get_file_attributes(access_token, project_id, file_id):
    file_detail_url = f'https://developer.api.autodesk.com/data/v1/projects/{project_id}/items/{file_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(file_detail_url, headers=headers)
    if response.status_code == 200:
        file_detail = response.json()
        return file_detail['data']['attributes']
    else:
        print(f'Error retrieving file attributes for {file_id}: {response.status_code}')
        return None

def get_folder_attributes(access_token, project_id, folder_id):
    folder_detail_url = f'https://developer.api.autodesk.com/data/v1/projects/{project_id}/folders/{folder_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(folder_detail_url, headers=headers)
    if response.status_code == 200:
        folder_detail = response.json()
        return folder_detail['data']['attributes']
    else:
        print(f'Error retrieving folder attributes for {folder_id}: {response.status_code}')
        return None

def get_item_attributes(access_token, project_id, item_id, item_type):
    if item_type == 'items':
        return get_file_attributes(access_token, project_id, item_id)
    elif item_type == 'folders':
        return get_folder_attributes(access_token, project_id, item_id)
    else:
        print(f'Unknown item type: {item_type}')
        return None

def get_document_id(access_token, project_id, folder_id):
    url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/folders/{folder_id}/contents"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        included = data.get('included', [])
        for item in included:
            if 'id' in item:
                return item['id']
    return None

def print_attributes(attributes, item_type, item_id):
    if attributes:
        print(f"\n{'ファイル' if item_type == 'items' else 'フォルダ'}名: {attributes['displayName']}")
        print(f"ID: {item_id}")
        print(f"作成日時: {attributes['createTime']}")
        print(f"作成者: {attributes['createUserName']}")
        print(f"最終更新日時: {attributes['lastModifiedTime']}")
        print(f"最終更新者: {attributes['lastModifiedUserName']}")
        print(f"説明: {attributes.get('extension', {}).get('data', {}).get('description', 'N/A')}")
        print(f"バージョン: {attributes.get('extension', {}).get('version', 'N/A')}")
        try:
            print(f"フォルダ内のファイル: {attributes['objectCount']}")
        except:
            print(f"フォルダではありません。")
        print("-" * 50)

def get_custom_Attribute(token):
    # token = get_access_token(auth_code)
    # hub_id = 'b.21cd4449-77cc-4f14-8dd8-597a5dfef551'
    project_id = 'b.1fd68d4e-de62-4bc3-a909-8b0baeec77e4'
    # folder_id = 'urn:adsk.wipprod:fs.folder:co.Lkhbj4P6TAOWxEbCSjhsBA'
    url = f'https://developer.api.autodesk.com/bim360/docs/v1/projects/{project_id}/versions:batch-get'
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'urns': [
            'urn:adsk.wipprod:fs.file:vf.3Lqfodg2RB6FYptKDOZ6-Q?version=1'
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    # response = requests.get(url, headers=headers)
    return response.json()

def get_custom_Attribute_Definition(token):
    # token = get_access_token(auth_code)
    # hub_id = 'b.21cd4449-77cc-4f14-8dd8-597a5dfef551'
    project_id = 'b.1fd68d4e-de62-4bc3-a909-8b0baeec77e4'
    folder_id = 'urn:adsk.wipprod:fs.folder:co.bbBsDQe2QDWHWZMhIMr3PQ'
    # url = f'https://developer.api.autodesk.com/bim360/docs/v1/projects/{project_id}/versions:batch-get'
    url = f'https://developer.api.autodesk.com/bim360/docs/v1/projects/{project_id}/folders/{folder_id}/custom-attribute-definitions'
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'urns': [
            'urn:adsk.wipprod:fs.file:vf.3Lqfodg2RB6FYptKDOZ6-Q?version=1'
        ]
    }
    # response = requests.post(url, headers=headers, json=data)
    response = requests.get(url, headers=headers)
    return response.json()

if __name__ == '__main__':
    try:
        auth_code = get_auth_code()
        if auth_code:
            token = get_access_token(auth_code)
            hub_id = 'b.21cd4449-77cc-4f14-8dd8-597a5dfef551'
            project_id = 'b.1fd68d4e-de62-4bc3-a909-8b0baeec77e4'  # ← 6-4512_BIM Training 2
            folder_id = "urn:adsk.wipprod:fs.folder:co.Lkhbj4P6TAOWxEbCSjhsBA"

            contents = get_folder_contents(token, project_id, folder_id)
            print("\n取得した項目の属性情報:")
            for item in contents:
                attributes = get_item_attributes(token, project_id, item['id'], item['type'])
                document_id = get_document_id(token, project_id, item['id']) if item['type'] == 'folders' else None
                print(f'document_id: {document_id}')
                print_attributes(attributes, item['type'], item['id'])
            print(json.dumps(get_custom_Attribute(token), indent=2, ensure_ascii=False))
            print("="*50)
            print(json.dumps(get_custom_Attribute_Definition(token), indent=2, ensure_ascii=False))
        else:
            print("認証コードの取得に失敗しました。プログラムを終了します。")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
