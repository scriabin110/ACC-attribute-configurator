'''
issuesのAPIを使ってみる

[方針]
APIの挙動を確かめるためのコードはここに書いていく

フォルダ構造:
└── Project Files (ID: urn:adsk.wipprod:fs.folder:co.SxNW2Yj7RLSNYCutoOLxVg)
    ├── A_WIP (ID: urn:adsk.wipprod:fs.folder:co.0f4U1iQHQVa6BPWP1hR_TA)
    │   ├── _collab_ARC (ID: urn:adsk.wipprod:fs.folder:co.Lkhbj4P6TAOWxEbCSjhsBA)
    │   │   ├── Consumed (ID: urn:adsk.wipprod:fs.folder:co.bbBsDQe2QDWHWZMhIMr3PQ)


'''

import os
import webbrowser
from src.api import *
from src.auth import *
from src.utils import *
# import pyperclip
import http.server
import socketserver
import urllib.parse
import json
import pandas as pd

CALLBACK_PORT = 8080
# "b."の部分を削除しなければならない
project_id = '1fd68d4e-de62-4bc3-a909-8b0baeec77e4'

# get_auth_code()
def get_auth_code_2():
    auth_url = f"https://developer.api.autodesk.com/authentication/v2/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote_plus(CALLBACK_URL)}&scope={' '.join(SCOPES)}"
    
    # ローカルサーバーを設定
    class AuthHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            s= '認証が完了しました。このページを閉じてください。'
            b = s.encode('utf-8')
            self.wfile.write(b)
            
            # URLからauth_codeを抽出
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            global auth_code
            auth_code = params.get('code', [None])[0]
            
    # ブラウザで認証ページを開く
    webbrowser.open(auth_url)
    
    # ローカルサーバーを起動してコールバックを待機
    with socketserver.TCPServer(("", CALLBACK_PORT), AuthHandler) as httpd:
        print(f"サーバーがポート {CALLBACK_PORT} で起動しました")
        httpd.handle_request()
    
    if auth_code:
        print("auth_codeを取得しました")
        print(auth_code)
        return auth_code
    else:
        print("auth_codeの取得に失敗しました")
        return None

auth_code = get_auth_code_2()
access_token = get_access_token(auth_code)
print(access_token)

# issue_idとissue_titleをセットにした辞書を返す関数
def get_issue_types(access_token, project_id):
    url = f"https://developer.api.autodesk.com/construction/issues/v1/projects/{project_id}/issue-types"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        dir_issue_types = {}
        for i in response.json()["results"]:
          dir_issue_types[i['title']] = i['id']
        return dir_issue_types
    else:
        raise Exception(f"issues取得エラー: {response.text}")

issue_types = get_issue_types(access_token, project_id)
st.write(issue_types)
# issued_type_id = issue_types[issued_type_title]
# st.write(issued_type_id)
st.write("-"*50)

issue_type_id = "4be979b1-25fd-4807-be19-2c926e5899ab"

def get_issues(access_token, project_id, issue_type_id="4be979b1-25fd-4807-be19-2c926e5899ab"):
    # url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects"
    if issue_type_id is not None:
      url = f"https://developer.api.autodesk.com/construction/issues/v1/projects/{project_id}/issues?filter[issueTypeId]={issue_type_id}"
    else:
      url = f"https://developer.api.autodesk.com/construction/issues/v1/projects/{project_id}/issues"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"issues取得エラー: {response.text}")

# issues = get_issues(access_token, project_id)

# with open(os.path.join(os.getcwd(), 'output.txt'), 'w') as f:
#     json.dump(issues, f, indent=2)



# st.write(dir_issue_types)
# st.write(issue_types)