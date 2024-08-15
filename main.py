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
        project_list = get_projects(st.session_state.token, hub_id=hub_id)

        project_name_list = [i["attributes"]["name"] for i in project_list]
        project_id_list = [i["id"] for i in project_list]

        project_dict = {name: id for name, id in zip(project_name_list, project_id_list)}
        print(project_dict)
        # project_id = 'b.1fd68d4e-de62-4bc3-a909-8b0baeec77e4'
        folder_id = "urn:adsk.wipprod:fs.folder:co.Lkhbj4P6TAOWxEbCSjhsBA"

        st.header("Select Project")
        project_name = st.selectbox("Select Project", project_name_list)
        project_id = project_dict[project_name]
        st.write(f"Selected Project: {project_name} (ID: {project_id})")
        # st.write(get_projects(st.session_state.token, hub_id))

        # st.write(get_top_folders(st.session_state.token, hub_id=hub_id, project_id=project_id))

        st.header("Folder Structure")
        with st.spinner("フォルダ構造を取得中..."):
            top_folders = get_top_folders(st.session_state.token, hub_id, project_id)
        # st.write("トップフォルダの取得に成功しました！")
        st.write(f"{top_folders[0]["attributes"]["name"]}")

        st.session_state.choosing_Folder = True

        folder_id = top_folders[0]["id"]
        contents = get_folder_contents(st.session_state.token, project_id, folder_id)

        if st.session_state.choosing_Folder:
            folder_id = top_folders[0]["id"]
            folder_path = []

            while True:
                contents = get_folder_contents(st.session_state.token, project_id, folder_id)
                
                # フォルダのみをフィルタリング
                folders = [item for item in contents if item.get("type") == "folders"]
                
                if not folders:
                    st.write("最下層のフォルダに到達しました。")
                    break

                folder_name_list = [folder["attributes"]["name"] for folder in folders]
                folder_id_list = [folder["id"] for folder in folders]
                folder_dict = {name: id for name, id in zip(folder_name_list, folder_id_list)}
                
                # 現在のフォルダパスを表示
                st.write("現在のパス: " + " > ".join(folder_path))
                
                selected_folder = st.selectbox(
                    "サブフォルダを選択してください",
                    [""] + folder_name_list,
                    key=f"folder_select_{len(folder_path)}",
                    index=0
                )
                
                if not selected_folder:
                    st.write("フォルダ選択を終了します。")
                    break
                
                folder_id = folder_dict[selected_folder]
                folder_path.append(selected_folder)

            st.write("選択されたフォルダパス: " + " > ".join(folder_path))
            st.write(f"最終選択フォルダID: {folder_id}")

            # ここで選択されたフォルダIDを使用して何か処理を行う
            # 例: 選択されたフォルダの内容を表示
            final_contents = get_folder_contents(st.session_state.token, project_id, folder_id)
            st.write("選択されたフォルダの内容:")
            st.write(final_contents)

        # folder_id = top_folders[0]["id"]
        # contents = get_folder_contents(st.session_state.token, project_id, folder_id)


        # st.header("トップフォルダの中身？")
        # st.write([i["attributes"]["name"] for i in contents])
        # st.write(contents)


        # with st.spinner("フォルダ構造を取得中..."):
        #     top_folders = get_top_folders(st.session_state.token, hub_id, project_id)
        
        # ===== 240815 一旦下記をコメントアウト =====
        # contents = get_folder_contents(st.session_state.token, project_id, folder_id)

        # st.header("取得した項目の属性情報:")
        # for item in contents:
        #     attributes = get_item_attributes(st.session_state.token, project_id, item['id'], item['type'])
        #     document_id = get_document_id(st.session_state.token, project_id, item['id']) if item['type'] == 'folders' else None
        #     st.write(f'document_id: {document_id}')
        #     print_attributes(attributes, item['type'], item['id'])

        # st.header("カスタム属性:")
        # st.json(get_custom_Attribute(st.session_state.token))

        # st.header("カスタム属性定義:")
        # st.json(get_custom_Attribute_Definition(st.session_state.token))

        # if st.button("カスタム属性を更新"):
        #     result = update_custom_Attribute(st.session_state.token)
        #     st.dataframe(result)
        # ===== 240815 コメントアウトここまで =====

if __name__ == '__main__':
    main()