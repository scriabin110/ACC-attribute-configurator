import streamlit as st
import pandas as pd
import numpy as np
import time
from src.api import *
from src.utils import *

def run():
    if 'token' not in st.session_state or not st.session_state.token:
        st.error("認証が必要です。メインページで認証を行ってください。")
        return

    if 'current_project_id_issue' not in st.session_state or not st.session_state.current_project_id_issue:
        st.error("プロジェクトが選択されていません。サイドバーでプロジェクトを選択してください。")
        return

    project_id = st.session_state.current_project_id_issue

    # タブ選択
    update_mode = st.radio(
        "Mode: ",
        ["🦾 Manual Update", "📈 ***Excel Batch Update***"],
        captions=["Directly update issues", "Batch update issues via Excel file"],
        horizontal=True
    )

    # SubTypeも含めて取得
    issue_types = get_issue_types(st.session_state.token, project_id, True)

    # IssueType, SubTypeを辞書に変換
    ## IssueType
    dir_issue_types = {i['title']: i['id'] for i in issue_types["results"]}
    selected_issue_type = st.selectbox("Select Issue Type", dir_issue_types, index=len(issue_types["results"])-1)

    ## SubType
    dir_issue_subtypes = {}
    for i in issue_types["results"]:
        if i['title'] == selected_issue_type:
            dir_issue_subtypes = {j['title']: j['id'] for j in i['subtypes']}
    selected_issue_subtype = st.selectbox("Select Issue SubType", dir_issue_subtypes, index=len(dir_issue_subtypes)-1)

    # IssueType, SubTypeをIDに変換
    issue_type_id = dir_issue_types[selected_issue_type]
    issue_subtype_id = dir_issue_subtypes[selected_issue_subtype]

    # カスタム属性の定義を取得
    issue_attribute_definitions = get_issue_attribute_definitions(st.session_state.token, project_id)

    if update_mode == "🦾 Manual Update":
        manual_update(st.session_state.token, project_id, issue_type_id, issue_attribute_definitions)
    elif update_mode == "📈 ***Excel Batch Update***":
        excel_batch_update(st.session_state.token, project_id, issue_attribute_definitions)

def manual_update(token, project_id, issue_type_id, issue_attribute_definitions):
    try:
        all_issues = get_all_issues(token, project_id, issue_type_id)
        patch_dirs = prepare_patch_data(all_issues)
        flattened_issues = flatten_issue_data(patch_dirs, issue_attribute_definitions)

        edited_df = st.data_editor(
            data=flattened_issues,
            disabled=("id",),
            column_config={
                "issueSubtypeId": None,
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["draft", "open", "pending", "in_progress", "completed", "in_review", "not_approved", "in_dispute", "closed"]
                )
            }
        )

        unflattened_issues = unflatten_issue_data(edited_df, issue_attribute_definitions)

        if st.button("Update Issues"):
            update_issues(token, project_id, unflattened_issues)

    except Exception as e:
        st.error(f"Error getting or updating issues: {str(e)}")

def excel_batch_update(token, project_id, issue_attribute_definitions):
    uploaded_file = st.file_uploader("Batch Update", type=["csv", "xlsx", "xls"])
    if uploaded_file is not None:
        try:
            df = read_uploaded_file(uploaded_file)
            df = df.replace({np.nan: None})
            st.dataframe(df)

            records = df.to_dict('records')
            records = [preprocess_data(record) for record in records]

            for record in records:
                validate_data(record, issue_attribute_definitions)

            unflattened_issues = unflatten_issue_data(records, issue_attribute_definitions)

            if st.button("Issuesを更新"):
                update_issues_batch(token, project_id, unflattened_issues)

        except Exception as e:
            st.error(f"ファイルの読み込み中にエラーが発生しました: {str(e)}")
    else:
        st.markdown('**:red[Upload File(.xlsx/.xls/.csv)]**')

def get_all_issues(token, project_id, issue_type_id):
    all_issues = []
    offset = 0
    limit = 100
    while True:
        issues = get_issues(token, project_id, issue_type_id=issue_type_id, offset=offset)["results"]
        if not issues:
            break
        all_issues.extend(issues)
        offset += limit
    return all_issues

def prepare_patch_data(issues):
    patchable_attributes = [
        "title", "description", "snapshotUrn", "issueSubtypeId", "status",
        "assignedTo", "assignedToType", "dueDate", "startDate", "locationId",
        "locationDetails", "rootCauseId", "published", "permittedActions",
        "watchers", "customAttributes", "gpsCoordinates", "snapshotHasMarkups"
    ]
    patch_dirs = {}
    for issue in issues:
        issue_id = issue.get("id")
        if not issue_id:
            continue
        patch_dir = {"displayId": issue["displayId"]}
        for attr in issue.get("permittedAttributes", []):
            if attr in issue and attr in patchable_attributes:
                patch_dir[attr] = issue[attr]
        patch_dirs[issue_id] = patch_dir
    return patch_dirs

def update_issues(token, project_id, unflattened_issues):
    with st.spinner('Updating issues...'):
        success_count = 0
        error_count = 0
        for issue_id, patch_data in unflattened_issues.items():
            try:
                patch_issues(token, project_id, issue_id, patch_data)
                success_count += 1
            except Exception as e:
                error_count += 1
                st.error(f"Error updating issue {issue_id}: {str(e)}")
            st.text(f"Progress: {success_count + error_count}/{len(unflattened_issues)}")
            time.sleep(0.5)
        st.success(f"更新完了: {success_count}件成功, {error_count}件失敗")

def read_uploaded_file(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension == "csv":
        return pd.read_csv(uploaded_file)
    elif file_extension in ["xlsx", "xls"]:
        return pd.read_excel(uploaded_file, engine='openpyxl')
    else:
        raise ValueError("サポートされていないファイル形式です。")

def update_issues_batch(token, project_id, unflattened_issues):
    with st.spinner('Updating issues...'):
        success_count = 0
        error_count = 0
        for issue_id, patch_data in unflattened_issues.items():
            try:
                patch_data = {k: v for k, v in patch_data.items() if v is not None}
                patch_issues_with_retry(token, project_id, issue_id, patch_data)
                success_count += 1
            except Exception as e:
                error_count += 1
                st.error(f"Error updating issue {issue_id}: {str(e)}")
            st.text(f"Progress: {success_count + error_count}/{len(unflattened_issues)}")
            time.sleep(0.5)
        st.success(f"更新完了: {success_count}件成功, {error_count}件失敗")