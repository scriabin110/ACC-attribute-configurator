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
    if 'current_project_id_issue' not in st.session_state:
        st.session_state.current_project_id_issue = None
    if 'current_folder_id' not in st.session_state:
        st.session_state.current_folder_id = None
    if 'urns' not in st.session_state:
        st.session_state.urns = None
    if 'update_mode' not in st.session_state:
        st.session_state.update_mode = None
    if 'issue_types' not in st.session_state:
        st.session_state.issue_types = None
    if 'account_id' not in st.session_state:
        st.session_state.account_id = None

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
            # st.success("認証が成功しました！")
        else:
            st.error("認証コードを入力してください。")
            return

    if st.session_state.token:
        hub_id = 'b.21cd4449-77cc-4f14-8dd8-597a5dfef551'
        st.session_state.account_id = hub_id.split(".")[1]

        if not st.session_state.project_list:
            with st.spinner("プロジェクトリストを取得中..."):
                st.session_state.project_list = get_projects(st.session_state.token, hub_id=hub_id)
            project_name_list = [i["attributes"]["name"] for i in st.session_state.project_list]
            project_id_list = [i["id"] for i in st.session_state.project_list]
            st.session_state.project_dict = {name: id for name, id in zip(project_name_list, project_id_list)}

        st.sidebar.header("Project")
        project_name = st.sidebar.selectbox("Select Project", list(st.session_state.project_dict.keys()))
        project_id = st.session_state.project_dict[project_name]
        st.session_state.current_project_id_issue = project_id.split(".")[1]

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

        if selected == "Document Management":
            st.session_state.update_mode = st.radio(
                "Mode:  ", 
                ["🦾 Manual Update", "📈 ***Excel Batch Update***"], 
                captions = ["Directly update issues", "Batch update issues via Excel file"],
                horizontal=True)
            
            # "🦾 Manual Update"
            if st.session_state.update_mode == "🦾 Manual Update": 
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
            
            #"📈 Custom Attributes"
            if st.session_state.update_mode == "📈 ***Excel Batch Update***": 
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
            st.session_state.update_mode = st.radio(
                "Mode:  ", 
                ["🦾 Manual Update", "📈 ***Excel Batch Update***"], 
                captions = ["Directly update issues", "Batch update issues via Excel file"],
                horizontal=True)
            
            # project_id_issue = project_id.split(".")[1]
            issue_types = get_issue_types(st.session_state.token, st.session_state.current_project_id_issue)
            st.session_state.issue_types = st.selectbox("Select Issue Type", issue_types, index=len(issue_types)-1)  #デフォルトでInformation Control Sheetを取得
            issue_type_id = issue_types[st.session_state.issue_types]
            st.write("-"*50)

            issues = get_issues(st.session_state.token, st.session_state.current_project_id_issue, issue_type_id=issue_type_id)["results"]

            issue_attribute_definitions = get_issue_attribute_definitions(st.session_state.token, st.session_state.current_project_id_issue)

            # "🦾 Manual Update"
            if st.session_state.update_mode == "🦾 Manual Update":
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
                        with st.spinner('Updating issues...'):
                            for issue_id, patch_data in unflattend_issues.items():
                                patch_issues(access_token=st.session_state.token, project_id=st.session_state.current_project_id_issue, issue_id=issue_id, data=patch_data)
                        st.success("Issuesを更新しました！")
                    except Exception as e:
                        st.error(f"Error updating issue {issue_id}: {str(e)}")

            # "📈 Custom Attributes"
            if st.session_state.update_mode == "📈 ***Excel Batch Update***":
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

                        # NaN値を None に置換
                        df = df.where(pd.notnull(df), None)

                        st.dataframe(df)
                        
                        # DataFrameを辞書のリストに変換し、NaN値をNoneに置換
                        records = df.to_dict('records')
                        for record in records:
                            for key, value in record.items():
                                if pd.isna(value):
                                    record[key] = None

                        unflattened_issues = unflatten_issue_data(records, issue_attribute_definitions)

                        if st.button("Issuesを更新"):
                            with st.spinner('Updating issues...'):
                                for issue_id, patch_data in unflattened_issues.items():
                                    # None値を持つキーを削除
                                    patch_data = {k: v for k, v in patch_data.items() if v is not None}
                                    patch_issues(access_token=st.session_state.token, project_id=st.session_state.current_project_id_issue, issue_id=issue_id, data=patch_data)
                            st.success("Issuesを更新しました！")
                    except Exception as e:
                        st.error(f"ファイルの読み込み中にエラーが発生しました: {str(e)}")
                else:
                    st.markdown('**:red[Upload File(.xlsx/.xls/.csv)]**')
            
        elif selected == "User Config":
            st.warning("実装中(240822時点)")

            ### ↓↓↓User登録を実装していく↓↓↓ ###
            token = get_2_legged_token()
            company_id = get_company_id(token, st.session_state.current_project_id_issue, st.session_state.account_id)
            st.header("company_id")
            

            ### 乱立しているdictをいつか整理したい ###
            # 1.company_dict (company一覧)
            company_dict = {}
            for i in company_id:
                company_dict[i["name"]] = i["id"]
            st.subheader("[Dict] Company")
            st.write(company_dict)

            # 2.project_users_dict (PJ user一覧)
            project_users = get_project_users(st.session_state.token, st.session_state.current_project_id_issue)
            project_users_dict = {}
            for user in project_users['results']:
                project_users_dict[user['id']] = user['name']
            st.subheader("[Dict] Project Users")
            st.write(project_users_dict)
            
            st.subheader("Project Users")
            dict_list = project_users["results"]
            st.write(dict_list)

            # 3.role_dict (role一覧)
            role_dict = {}
            for i in dict_list:
                for j in i['roles']:
                    for key, value in j.items():
                        if key == "name":
                            role_dict[value] = i["id"]
            st.subheader("[Dict] Role")
            st.write(role_dict)

            #4. product_list (product一覧)
            product_list = []
            for i in dict_list[0]["products"]:
                product_list.append(i["key"])
            st.subheader("[List] Product")
            st.write(product_list)

            # テーブル表示用にdictを整形
            new_dict_list = []
            for i in dict_list:
                new_dict = {}
                for key, value in i.items():
                    if key in ["email", 'firstName', 'lastName']:
                        new_dict[key] = value
                    elif key in ["companyId"]:
                        new_dict['companyName'] = get_keys_from_value(company_dict, value)[0]
                        # new_dict['roleName'] = get_keys_from_value(role_dict, value)[0]
                    elif key in ["roles"]:
                        if value:
                            new_dict["roleName"] = [j["name"] for j in value][0]  #いつか複数roleに対応できるようになるかもなので、紛らわしい記法にしている
                        else:
                            new_dict["roleName"] = None
                    elif key in ["products"]:
                        for j in value:
                            new_dict[j["key"]] = j["access"]
                new_dict_list.append(new_dict)

            dict_list = new_dict_list
            st.write(dict_list)

            column_config = {
                "companyName": st.column_config.SelectboxColumn(
                    "companyName",
                    help="Select your company",
                    width="medium",
                    options=list(company_dict.keys()),
                    required=True,
                ),
                "roleName": st.column_config.SelectboxColumn(
                    "roleName",
                    help="Describe your Roles",
                    width="medium",
                    options=list(role_dict.keys())
                )
            }

            # 製品リストに対する SelectboxColumn を追加
            for product in product_list:
                column_config[product] = st.column_config.SelectboxColumn(
                    product,
                    help=f"Select access for {product}",
                    width="medium",
                    options=["none", "member", "administrator"]  # アクセスレベルのオプション
                )

            df_editable = st.data_editor(
                dict_list, 
                num_rows="dynamic", 
                column_config=column_config
            )
            st.write(type(df_editable))
            # df = pd.json_normalize(project_users['results'][0])
            # st.data_editor(df, num_rows="dynamic", column_config={
            # "country": st.column_config.SelectboxColumn(
            #     "country",
            #     help="Select your country",
            #     width="medium",
            #     options=["japan", "america", "china"],
            #     required=True,
            # )})

            data = transform_user_data(df_editable, company_dict, role_dict)
            st.subheader("Post Project Users(update)")
            st.write(data)
            if st.button("Post Project Users"):
                post_project_users(st.session_state.token, st.session_state.current_project_id_issue, data)
                st.success("usersを更新しました！")
            
            # st.subheader("Patch Project Users(update)")
            # if st.button("Patch Project Users"):


            

            


            


            ### ↑↑↑User登録を実装していく↑↑↑ ###

if __name__ == '__main__':
    main()