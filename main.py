# import requests
# import base64
# import webbrowser
# import time
# from http.server import HTTPServer, BaseHTTPRequestHandler
# import urllib.parse
# import threading
# import config
# import json

# # Autodeskアプリケーションの認証情報
# CLIENT_ID = config.CLIENT_ID
# CLIENT_SECRET = config.CLIENT_SECRET
# CALLBACK_URL = config.CALLBACK_URL
# SCOPES = ['data:read', 'data:write', 'data:create']











# def print_attributes(attributes, item_type, item_id):
#     if attributes:
#         print(f"\n{'ファイル' if item_type == 'items' else 'フォルダ'}名: {attributes['displayName']}")
#         print(f"ID: {item_id}")
#         print(f"作成日時: {attributes['createTime']}")
#         print(f"作成者: {attributes['createUserName']}")
#         print(f"最終更新日時: {attributes['lastModifiedTime']}")
#         print(f"最終更新者: {attributes['lastModifiedUserName']}")
#         print(f"説明: {attributes.get('extension', {}).get('data', {}).get('description', 'N/A')}")
#         print(f"バージョン: {attributes.get('extension', {}).get('version', 'N/A')}")
#         try:
#             print(f"フォルダ内のファイル: {attributes['objectCount']}")
#         except:
#             print(f"フォルダではありません。")
#         print("-" * 50)



# if __name__ == '__main__':
#     try:
#         auth_code = get_auth_code()
#         if auth_code:
#             token = get_access_token(auth_code)
#             hub_id = 'b.21cd4449-77cc-4f14-8dd8-597a5dfef551'
#             project_id = 'b.1fd68d4e-de62-4bc3-a909-8b0baeec77e4'  # ← 6-4512_BIM Training 2
#             folder_id = "urn:adsk.wipprod:fs.folder:co.Lkhbj4P6TAOWxEbCSjhsBA"

#             contents = get_folder_contents(token, project_id, folder_id)
#             print("\n取得した項目の属性情報:")
#             for item in contents:
#                 attributes = get_item_attributes(token, project_id, item['id'], item['type'])
#                 document_id = get_document_id(token, project_id, item['id']) if item['type'] == 'folders' else None
#                 print(f'document_id: {document_id}')
#                 print_attributes(attributes, item['type'], item['id'])
#             print(json.dumps(get_custom_Attribute(token), indent=2, ensure_ascii=False))
#             print("="*50)
#             print(json.dumps(get_custom_Attribute_Definition(token), indent=2, ensure_ascii=False))
#             print(update_custom_Attribute(token))
#         else:
#             print("認証コードの取得に失敗しました。プログラムを終了します。")
#     except Exception as e:
#         print(f"エラーが発生しました: {str(e)}")


import streamlit as st
import json
from src.auth import get_auth_code, get_access_token
from src.api import (get_projects, get_top_folders, get_folder_contents,
                     get_item_attributes, get_document_id, get_custom_Attribute,
                     get_custom_Attribute_Definition, update_custom_Attribute)
from src.utils import print_attributes

def main():
    st.title("Autodesk BIM 360 Explorer")

    if 'token' not in st.session_state:
        st.write("認証が必要です。以下のボタンをクリックして認証プロセスを開始してください。")
        if st.button("認証を開始"):
            auth_code = get_auth_code()
            if auth_code:
                st.session_state.token = get_access_token(auth_code)
                st.success("認証が成功しました！")
            else:
                st.error("認証コードの取得に失敗しました。")
                return
    
    if 'token' in st.session_state:
        hub_id = 'b.21cd4449-77cc-4f14-8dd8-597a5dfef551'
        project_id = 'b.1fd68d4e-de62-4bc3-a909-8b0baeec77e4'
        folder_id = "urn:adsk.wipprod:fs.folder:co.Lkhbj4P6TAOWxEbCSjhsBA"

        contents = get_folder_contents(st.session_state.token, project_id, folder_id)

        st.header("取得した項目の属性情報:")
        for item in contents:
            attributes = get_item_attributes(st.session_state.token, project_id, item['id'], item['type'])
            document_id = get_document_id(st.session_state.token, project_id, item['id']) if item['type'] == 'folders' else None
            st.write(f'document_id: {document_id}')
            print_attributes(attributes, item['type'], item['id'])

        st.header("カスタム属性:")
        st.json(get_custom_Attribute(st.session_state.token))

        st.header("カスタム属性定義:")
        st.json(get_custom_Attribute_Definition(st.session_state.token))

        if st.button("カスタム属性を更新"):
            result = update_custom_Attribute(st.session_state.token)
            st.json(result)

if __name__ == '__main__':
    main()