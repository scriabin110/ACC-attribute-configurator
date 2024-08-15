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
        project_list = [i["attributes"]["name"] for i in get_projects(st.session_state.token, hub_id=hub_id)]
        # project_id = 'b.1fd68d4e-de62-4bc3-a909-8b0baeec77e4'
        folder_id = "urn:adsk.wipprod:fs.folder:co.Lkhbj4P6TAOWxEbCSjhsBA"

        st.header("プロジェクト一覧")
        project_id = st.selectbox("Select Project", project_list)

        # with st.spinner("フォルダ構造を取得中..."):
        #     top_folders = get_top_folders(st.session_state.token, hub_id, project_id)
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
            st.dataframe(result)

if __name__ == '__main__':
    main()