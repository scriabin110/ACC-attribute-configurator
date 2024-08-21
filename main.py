import streamlit as st
# import json
from src.auth import *
from src.api import *
from src.utils import *
import const
from streamlit_option_menu import option_menu
import pandas as pd

def initialize_session_state():
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'project_list' not in st.session_state:
        st.session_state.project_list = None
    if 'project_dict' not in st.session_state:
        st.session_state.project_dict = None
    if 'top_folders' not in st.session_state:
        st.session_state.top_folders = None
    if 'current_project_id' not in st.session_state:
        st.session_state.current_project_id = None
    if 'current_folder_id' not in st.session_state:
        st.session_state.current_folder_id = None
    if 'urns' not in st.session_state:
        st.session_state.urns = None

def main():
    st.set_page_config(**const.SET_PAGE_CONFIG)
    st.markdown(const.HIDE_ST_STYLE, unsafe_allow_html=True)

    initialize_session_state()

    selected = option_menu(
        menu_title=const.OPTION_MENU_CONFIG["menu_title"],
        options=const.OPTION_MENU_CONFIG["options"],
        icons=const.OPTION_MENU_CONFIG["icons"],
        menu_icon=const.OPTION_MENU_CONFIG["menu_icon"],
        default_index=const.OPTION_MENU_CONFIG["default_index"],
        orientation=const.OPTION_MENU_CONFIG["orientation"],
        styles=const.OPTION_MENU_CONFIG["styles"],
    )

    if not st.session_state.token:
        st.write("認証が必要です。以下のリンクをクリックして認証プロセスを開始してください。")
        auth_code = get_auth_code()
        if auth_code:
            st.session_state.token = get_access_token(auth_code)
            st.success("認証が成功しました！")
        else:
            st.error("認証コードを入力してください。")
            return

    if st.session_state.token:
        hub_id = 'b.21cd4449-77cc-4f14-8dd8-597a5dfef551'

        if not st.session_state.project_list:
            with st.spinner("プロジェクトリストを取得中..."):
                st.session_state.project_list = get_projects(st.session_state.token, hub_id=hub_id)
            project_name_list = [i["attributes"]["name"] for i in st.session_state.project_list]
            project_id_list = [i["id"] for i in st.session_state.project_list]
            st.session_state.project_dict = {name: id for name, id in zip(project_name_list, project_id_list)}

        st.sidebar.header("Project")
        project_name = st.sidebar.selectbox("Select Project", list(st.session_state.project_dict.keys()))
        project_id = st.session_state.project_dict[project_name]

        if project_id != st.session_state.current_project_id:
            st.session_state.current_project_id = project_id
            st.session_state.top_folders = None
            st.session_state.current_folder_id = None
            st.session_state.urns = None

        if not st.session_state.top_folders:
            with st.spinner("フォルダ構造を取得中..."):
                st.session_state.top_folders = get_top_folders(st.session_state.token, hub_id, project_id)

        st.sidebar.markdown("**Folder Structure**")
        folder_id = st.session_state.top_folders[0]["id"]
        folder_path = []
        i = 1

        while True:
            contents = get_folder_contents(st.session_state.token, project_id, folder_id)
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

        if folder_id != st.session_state.current_folder_id:
            st.session_state.current_folder_id = folder_id
            st.session_state.urns = get_document_id(st.session_state.token, project_id, folder_id)

        if selected == "Manual Update":
            try:
                if st.session_state.urns:
                    json_data = get_custom_Attribute(st.session_state.token, project_id, st.session_state.urns)['results']
                    custom_attributes = []
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

                    df = pd.DataFrame(custom_attributes)
                    st.markdown("**Custom Attributes**")
                    edited_df = st.data_editor(data=df, disabled=("file name", "urn", 'id', 'type', 'name'))

                    dict = transform_data(edited_df.to_dict('index'))

                    if st.button("カスタム属性を更新"):
                        for urn, data_list in dict.items():
                            update_custom_Attribute(
                                token=st.session_state.token,
                                project_id=project_id,
                                urn=urn,
                                data=data_list
                            )
                        st.success("カスタム属性を更新しました！")
                else:
                    st.warning("フォルダ内にファイルが存在しません。")
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")

        elif selected == "Batch Update":
            uploaded_file = st.file_uploader("Batch Update", type=["csv", "xlsx", "xls"])
            if uploaded_file is not None:
                try:
                    file_extension = uploaded_file.name.split('.')[-1].lower()
                    if file_extension == "csv":
                        df = pd.read_csv(uploaded_file)
                    elif file_extension in ["xlsx", "xls"]:
                        df = pd.read_excel(uploaded_file, engine='openpyxl')
                    else:
                        st.error("サポートされていないファイル形式です。")
                        return

                    st.dataframe(df)
                    dict = transform_data(df.to_dict('index'))

                    if st.button("カスタム属性を更新"):
                        for urn, data_list in dict.items():
                            update_custom_Attribute(
                                token=st.session_state.token,
                                project_id=project_id,
                                urn=urn,
                                data=data_list
                            )
                        st.success("カスタム属性を更新しました！")
                except Exception as e:
                    st.error(f"ファイルの読み込み中にエラーが発生しました: {str(e)}")
            else:
                st.markdown('**:red[Upload File(.xlsx/.xls/.csv)]**')
        
        elif selected == "Issue Config":
            # st.write(project_id)
            project_id_issue = project_id.split(".")[1]
            issue_types = get_issue_types(st.session_state.token, project_id_issue)
            issue_type_name = st.selectbox("Select Issue Type", issue_types, index=len(issue_types)-1)  #デフォルトでInformation Control Sheetを取得
            issue_type_id = issue_types[issue_type_name]
            st.write("-"*50)

            issues = get_issues(st.session_state.token, project_id_issue, issue_type_id=issue_type_id)["results"]

            issue_attribute_definitions = get_issue_attribute_definitions(st.session_state.token, project_id_issue)

            n_patch_issue = len(issues)  # ここでissue数を指定
            issues = issues[:n_patch_issue]  # issuesリストから指定数だけ取得

            patch_dirs = {}  # 辞書型オブジェクトとして初期化

            for issue in issues:
                issue_id = issue.get("id")
                if not issue_id:
                    st.warning(f"IDが見つかりません: {issue}")
                    continue

                permittedAttributes = issue.get("permittedAttributes", [])

                patchable_attributes = [
                    "title", "description", "snapshotUrn", "issueSubtypeId", "status", 
                    "assignedTo", "assignedToType", "dueDate", "startDate", "locationId", "locationDetails", 
                    "rootCauseId", "published", "permittedActions", "watchers", "customAttributes", "gpsCoordinates", "snapshotHasMarkups"
                ]

                patch_dir = {}
                for attr in permittedAttributes:
                    if attr in issue and attr in patchable_attributes:
                        patch_dir[attr] = issue[attr]

                patch_dirs[issue_id] = patch_dir

            # 辞書型オブジェクトをフラット化
            flattened_issues = flatten_issue_data(patch_dirs, issue_attribute_definitions)

            # Streamlitで表示
            edited_df = st.data_editor(data=flattened_issues, disabled=("id", "issueSubtypeId"))
            
            unflattend_issues = unflatten_issue_data(edited_df, issue_attribute_definitions)

            # パッチ処理
            if st.button("Update Issues"):
                try:
                    for issue_id, patch_data in unflattend_issues.items():
                        patch_issues(access_token=st.session_state.token, project_id=project_id_issue, issue_id=issue_id, data=patch_data)
                    st.success("Issuesを更新しました！")
                except Exception as e:
                    st.error(f"Error updating issue {issue_id}: {str(e)}")

if __name__ == '__main__':
    main()