import requests
from urllib.parse import urlencode

# APS認証情報
CLIENT_ID = 'm6caOI8GGlylZY8FHGMtIWZvGiXUMZ6E3P6RLvEeGP6EpRjo'
CLIENT_SECRET = 'xKFPThA7G2ZuOUvAZiZyiaoVA5Gws4mRA2NxEClz9GQ58utQEBKDDT0diA3PhBAN'
CALLBACK_URL = 'http://localhost:8080/api/auth/callback'

# プロジェクト情報
HUB_ID = 'b.21cd4449-77cc-4f14-8dd8-597a5dfef551'
PROJECT_ID = 'b.74d0a9fe-dbcc-4aed-be6b-dbd118667cda'

# トークンを取得する関数
# def get_access_token():
#     url = 'https://developer.api.autodesk.com/authentication/v1/authenticate'
#     data = {
#         'client_id': CLIENT_ID,
#         'client_secret': CLIENT_SECRET,
#         'grant_type': 'client_credentials',
#         'scope': 'data:read account:read'
#     }
#     response = requests.post(url, data=data)
#     return response.json()['access_token']

# フォルダの内容を取得する関数
def get_folder_contents(project_id, folder_id, access_token):
    url = f'https://developer.api.autodesk.com/data/v1/projects/{project_id}/folders/{folder_id}/contents'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    return response.json()

# ファイルの属性情報を取得する関数
def get_file_attributes(project_id, file_id, access_token):
    url = f'https://developer.api.autodesk.com/data/v1/projects/{project_id}/items/{file_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    return response.json()

# メイン処理
def main():
    # access_token = get_access_token()
    access_token = "Kl0qnrp4SLiG-l04QN5ABFb0fz5JEXX-uccGJSmu"
    
    # プロジェクトのルートフォルダを取得
    root_folder = get_folder_contents(PROJECT_ID, 'urn:adsk.wipprod:fs.folder:co.Yl6gMhIRRZyXUhMwVfxHqw', access_token)
    
    # フォルダ内のファイルを処理
    for item in root_folder['data']:
        if item['type'] == 'items':
            file_id = item['id']
            file_attributes = get_file_attributes(PROJECT_ID, file_id, access_token)
            
            print(f"File Name: {file_attributes['data']['attributes']['displayName']}")
            print(f"File Type: {file_attributes['data']['attributes']['extension']['type']}")
            print(f"Version: {file_attributes['data']['attributes']['versionNumber']}")
            print(f"Last Modified: {file_attributes['data']['attributes']['lastModifiedTime']}")
            print("---")

if __name__ == '__main__':
    main()
