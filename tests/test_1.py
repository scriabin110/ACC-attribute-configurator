'''
[方針]
APIの挙動を確かめるためのコードはここに書いていく

フォルダ構造:
└── Project Files (ID: urn:adsk.wipprod:fs.folder:co.SxNW2Yj7RLSNYCutoOLxVg)
    ├── A_WIP (ID: urn:adsk.wipprod:fs.folder:co.0f4U1iQHQVa6BPWP1hR_TA)
    │   ├── _collab_ARC (ID: urn:adsk.wipprod:fs.folder:co.Lkhbj4P6TAOWxEbCSjhsBA)
    │   │   ├── Consumed (ID: urn:adsk.wipprod:fs.folder:co.bbBsDQe2QDWHWZMhIMr3PQ)


'''

# import os
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

# folder_attributes = get_folder_attributes(access_token, 'b.1fd68d4e-de62-4bc3-a909-8b0baeec77e4', 'urn:adsk.wipprod:fs.folder:co.bbBsDQe2QDWHWZMhIMr3PQ')
# print(json.dumps(folder_attributes, indent=2))

document_id = get_document_id(access_token, 'b.1fd68d4e-de62-4bc3-a909-8b0baeec77e4', 'urn:adsk.wipprod:fs.folder:co.bbBsDQe2QDWHWZMhIMr3PQ')
# print(json.dumps(document_id, indent=2))

dict = {}

for id in document_id:
    custom_Attribute_Definition = get_custom_Attribute_Definition(access_token, 'b.1fd68d4e-de62-4bc3-a909-8b0baeec77e4', 'urn:adsk.wipprod:fs.folder:co.bbBsDQe2QDWHWZMhIMr3PQ')
    dict[id] = custom_Attribute_Definition["results"]
    # for i in json.dumps(custom_Attribute_Definition["results"], indent=2):
    # print(json.dumps(custom_Attribute_Definition["results"], indent=2))
    # df = custom_Attribute_Definition
print(dict)
d = list(dict.items())
print(d)
# df=pd.json_normalize(d)


'''
{
  "results": [
    {
      "id": 4624415,
      "name": "\u3042\u3044\u3055\u3064",
      "type": "string"
    },
    {
      "id": 4674473,
      "name": "__takeoff__updatedByName",
      "type": "string"
    },
    {
      "id": 4681908,
      "name": "PS_Forcast Date",
      "type": "date"
    },
    {
      "id": 4681909,
      "name": "PS_Development",
      "type": "string"
    },
    {
      "id": 4681912,
      "name": "PS_Review Duration",
      "type": "string"
    },
    {
      "id": 5064287,
      "name": "test_240809",
      "type": "string"
    }
  ],
  "pagination": {
    "limit": 200,
    "offset": 0,
    "totalResults": 6
  }
}
{
  "results": [
    {
      "id": 4624415,
      "name": "\u3042\u3044\u3055\u3064",
      "type": "string"
    },
    {
      "id": 4674473,
      "name": "__takeoff__updatedByName",
      "type": "string"
    },
    {
      "id": 4681908,
      "name": "PS_Forcast Date",
      "type": "date"
    },
    {
      "id": 4681909,
      "name": "PS_Development",
      "type": "string"
    },
    {
      "id": 4681912,
      "name": "PS_Review Duration",
      "type": "string"
    },
    {
      "id": 5064287,
      "name": "test_240809",
      "type": "string"
    }
      "name": "PS_Review Duration",
      "type": "string"
    },
    {
      "id": 5064287,
      "name": "test_240809",
      "type": "string"
      "name": "PS_Review Duration",
      "type": "string"
    },
    {
      "id": 5064287,
      "name": "PS_Review Duration",
      "type": "string"
    },
      "name": "PS_Review Duration",
      "type": "string"
      "name": "PS_Review Duration",
      "name": "PS_Review Duration",
      "type": "string"
      "name": "PS_Review Duration",
      "type": "string"
    },
    {
      "id": 5064287,
      "name": "test_240809",
      "type": "string"
    }
  ],
  "pagination": {
    "limit": 200,
    "offset": 0,
    "totalResults": 6
  }
}
'''

