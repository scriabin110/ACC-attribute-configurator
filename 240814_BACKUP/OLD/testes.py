import requests
import json

# APS認証情報
client_id = 'm6caOI8GGlylZY8FHGMtIWZvGiXUMZ6E3P6RLvEeGP6EpRjo'
client_secret = 'xKFPThA7G2ZuOUvAZiZyiaoVA5Gws4mRA2NxEClz9GQ58utQEBKDDT0diA3PhBAN'

# プロジェクト情報
hub_id = 'b.21cd4449-77cc-4f14-8dd8-597a5dfef551'
project_id = 'b.74d0a9fe-dbcc-4aed-be6b-dbd118667cda'

# アクセストークンを取得
# def get_access_token():
#     url = 'https://developer.api.autodesk.com/authentication/v1/authenticate'
#     data = {
#         'client_id': client_id,
#         'client_secret': client_secret,
#         'grant_type': 'client_credentials',
#         'scope': 'data:read'
#     }
#     response = requests.post(url, data=data)
#     return response.json()['access_token']

# フォルダ構造を取得
def get_folder_contents(access_token, project_id):
    url = f'https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects/{project_id}/topFolders'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

# メイン処理
if __name__ == '__main__':
    # access_token = get_access_token()
    access_token = "afTiZrJ1B3pH05uH4WWFkrLFqrfZ-INtrVwGJSmu"
    folder_contents = get_folder_contents(access_token, project_id)
    
    # 結果をJSON形式で出力
    print(json.dumps(folder_contents, indent=2))
