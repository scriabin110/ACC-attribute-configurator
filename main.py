import requests
import base64
import webbrowser
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import threading
import config

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

def print_folder_tree(access_token, project_id, folder_id, indent="", is_last=True):
    try:
        contents = get_folder_contents(access_token, project_id, folder_id)
        folders = [item for item in contents if item['type'] == 'folders']
        files = [item for item in contents if item['type'] == 'items']

        for i, folder in enumerate(folders):
            is_last_folder = (i == len(folders) - 1) and (len(files) == 0)
            folder_name = folder['attributes'].get('name', 'Unknown Folder')
            folder_id = folder.get('id', 'Unknown ID')
            print(f"{indent}{'└── ' if is_last_folder else '├── '}{folder_name} (ID: {folder_id})")
            new_indent = indent + ("    " if is_last_folder else "│   ")
            print_folder_tree(access_token, project_id, folder_id, new_indent, is_last_folder)

        for i, file in enumerate(files):
            is_last_file = i == len(files) - 1
            file_name = file['attributes'].get('name', 'Unknown File')
            file_id = file.get('id', 'Unknown ID')
            print(f"{indent}{'└── ' if is_last_file else '├── '}{file_name} (ID: {file_id})")
    except Exception as e:
        print(f"{indent}Error: Unable to retrieve contents. {str(e)}")

def get_file_attributes(access_token, project_id, folder_id):
    contents = get_folder_contents(access_token, project_id, folder_id)
    files_attributes = []

    for item in contents:
        if item['type'] == 'items':
            file_id = item['id']
            file_detail_url = f'https://developer.api.autodesk.com/data/v1/projects/{project_id}/items/{file_id}'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(file_detail_url, headers=headers)

            if response.status_code == 200:
                file_detail = response.json()
                files_attributes.append(file_detail['data']['attributes'])
            else:
                print(f'Error retrieving file attributes for {file_id}: {response.status_code}')

    return files_attributes

if __name__ == '__main__':
    try:
        auth_code = get_auth_code()
        if auth_code:
            token = get_access_token(auth_code)
            # print(f'取得したアクセストークン: {token}')

            # hub_id = input("Hub IDを入力してください: ")
            hub_id = 'b.21cd4449-77cc-4f14-8dd8-597a5dfef551'
            # projects = get_projects(token, hub_id)
            
            # print("利用可能なプロジェクト:")
            # for project in projects:
            #     print(f"- {project['attributes']['name']} (ID: {project['id']})")
            
            # project_id = input("プロジェクトIDを入力してください: ")
            project_id = 'b.74d0a9fe-dbcc-4aed-be6b-dbd118667cda'
            
            # top_folders = get_top_folders(token, hub_id, project_id)
            # print("\nフォルダ構造:")
            # for i, folder in enumerate(top_folders):
            #     is_last = i == len(top_folders) - 1
            #     print(f"{'└── ' if is_last else '├── '}{folder['attributes']['name']} (ID: {folder['id']})")
            #     print_folder_tree(token, project_id, folder['id'], "    " if is_last else "│   ")
            
            folder_id = input("\nファイル属性を取得するフォルダIDを入力してください: ")
            file_attributes = get_file_attributes(token, project_id, folder_id)

            print("\n取得したファイルの属性情報:")
            if len(file_attributes) == 0:
                print("ファイルが見つかりませんでした。")
            else:
                for attributes in file_attributes:
                    print(f"\nファイル名: {attributes['displayName']}")
                    print(f"作成日時: {attributes['createTime']}")
                    print(f"作成者: {attributes['createUserName']}")
                    print(f"最終更新日時: {attributes['lastModifiedTime']}")
                    print(f"最終更新者: {attributes['lastModifiedUserName']}")
                    print(f"説明: {attributes.get('extension', {}).get('data', {}).get('description', 'N/A')}")
                    print("-" * 50)
        else:
            print("認証コードの取得に失敗しました。プログラムを終了します。")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

# ========================================

# if __name__ == '__main__':
#     try:
#         auth_code = get_auth_code()
#         if auth_code:
#             token = get_access_token(auth_code)
#             # print(f'取得したアクセストークン: {token}')

#             # hub_id = input("Hub IDを入力してください: ")
#             hub_id = 'b.21cd4449-77cc-4f14-8dd8-597a5dfef551'
#             projects = get_projects(token, hub_id)
            
#             print("利用可能なプロジェクト:")
#             for project in projects:
#                 print(f"- {project['attributes']['name']} (ID: {project['id']})")
            
#             project_id = input("プロジェクトIDを入力してください: ")
            
#             top_folders = get_top_folders(token, hub_id, project_id)
#             print("\nフォルダ構造:")
#             for i, folder in enumerate(top_folders):
#                 is_last = i == len(top_folders) - 1
#                 print(f"{'└── ' if is_last else '├── '}{folder['attributes']['name']} (ID: {folder['id']})")
#                 print_folder_tree(token, project_id, folder['id'], "    " if is_last else "│   ")
#         else:
#             print("認証コードの取得に失敗しました。プログラムを終了します。")
#     except Exception as e:
#         print(f"エラーが発生しました: {str(e)}")