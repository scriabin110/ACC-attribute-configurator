import streamlit as st
import json
from src.auth import get_auth_code, get_access_token
from src.api import (get_projects, get_top_folders, get_folder_contents,
                     get_item_attributes, get_document_id, get_custom_Attribute,
                     get_custom_Attribute_Definition, update_custom_Attribute, transform_data)
from src.utils import print_attributes
import const
from streamlit_option_menu import option_menu


def main():
    st.set_page_config(**const.SET_PAGE_CONFIG)
    st.markdown(const.HIDE_ST_STYLE, unsafe_allow_html=True)
    selected = option_menu(**const.OPTION_MENU_CONFIG)

    # name = st.sidebar.text_input('あなたの名前は？')
    # age = st.sidebar.slider('あなたの年齢は？', 0, 100, 10)

    # '私の名前は', name, 'です。'
    # '私の年齢は', age, '歳です。'


    # st.title("Autodesk BIM 360 Explorer")

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

        st.sidebar.header("Project")
        project_name = st.sidebar.selectbox("Select Project", project_name_list)
        project_id = project_dict[project_name]

        with st.spinner("フォルダ構造を取得中..."):
            top_folders = get_top_folders(st.session_state.token, hub_id, project_id)

        st.session_state.choosing_Folder = True

        folder_id = top_folders[0]["id"]
        contents = get_folder_contents(st.session_state.token, project_id, folder_id)

        if st.session_state.choosing_Folder:
            folder_id = top_folders[0]["id"]
            folder_path = []

            st.sidebar.markdown("**Folder Structure**")

            i = 1
            while True:
                
                contents = get_folder_contents(st.session_state.token, project_id, folder_id)
                
                # フォルダのみをフィルタリング
                folders = [item for item in contents if item.get("type") == "folders"]
                
                if not folders:
                    st.sidebar.markdown('**:red[最下層のフォルダに到達しました。]**')
                    break

                folder_name_list = [folder["attributes"]["name"] for folder in folders]
                folder_id_list = [folder["id"] for folder in folders]
                folder_dict = {name: id for name, id in zip(folder_name_list, folder_id_list)}
                
                selected_folder = st.sidebar.selectbox(
                    f"サブフォルダ{i}を選択してください",
                    [""] + folder_name_list,
                    key=f"folder_select_{len(folder_path)}",
                    index=0
                )
                
                if not selected_folder:
                    break
                
                folder_id = folder_dict[selected_folder]
                folder_path.append(selected_folder)

                i += 1

            # ここで選択されたフォルダIDを使用して何か処理を行う
            # 例: 選択されたフォルダの内容を表示
            final_contents = get_folder_contents(st.session_state.token, project_id, folder_id)

            urns = get_document_id(st.session_state.token, project_id, folder_id)

            import pandas as pd
            json_data = get_custom_Attribute(st.session_state.token, project_id, urns)['results']
            
            # カスタム属性を格納するリストを作成
            custom_attributes = []

            # 各アイテムのカスタム属性を抽出
            for item in json_data:
                name = item['name']
                urn = item['urn']
                for attr in item.get('customAttributes', []):
                    custom_attributes.append({
                        'file name': name,
                        'urn': urn,
                        'id': attr['id'],
                        'type': attr['type'],
                        'name': attr['name'],
                        'value': attr['value']
                    })

            # pandasのDataFrameに変換
            df = pd.DataFrame(custom_attributes)
            st.markdown("**Custom Attributes**")
            edited_df = st.data_editor(df)
            edited_data = edited_df.loc[:,["id","value"]].to_dict('index').values()
            # st.write(edited_data)
            dict = transform_data(edited_df.to_dict('index'))
            # st.write(dict)
            
            if st.button("カスタム属性を更新"):
                for urn, data_list in dict.items():
                    update_custom_Attribute(
                        token=st.session_state.token,
                        project_id=project_id,
                        urn=urn,
                        data=data_list
                    )
                st.success("カスタム属性を更新しました！")

if __name__ == '__main__':
    main()