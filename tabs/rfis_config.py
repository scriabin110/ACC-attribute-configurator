import streamlit as st
import pandas as pd
from src.api import *
from src.utils import *

def run():
    st.title("RFIs Config")

    if 'token' not in st.session_state or not st.session_state.token:
        st.error("認証が必要です。メインページで認証を行ってください。")
        return

    if 'current_project_id_issue' not in st.session_state or not st.session_state.current_project_id_issue:
        st.error("プロジェクトが選択されていません。サイドバーでプロジェクトを選択してください。")
        return

    project_id = st.session_state.current_project_id_issue

    rfis = get_rfis(st.session_state.token, project_id)
    
    if not rfis:
        st.warning("RFIsが見つかりません。")
        return

    rfi_id = rfis[-2]["id"]  # 最新から2番目のRFIを選択
    rfi_per_id = get_rfi_per_id(st.session_state.token, project_id, rfi_id)
    locations_att = get_locations_att(st.session_state.token, project_id, rfi_id)
    custom_attributes = rfi_per_id["customAttributes"]
    location_node = get_locations_node(st.session_state.token, project_id)

    filtered_rfis = filter_json_data(rfis)
    rfis_for_post = transform_to_bim360_format(filtered_rfis)

    st.subheader("RFIs概要")
    st.dataframe(pd.DataFrame(filtered_rfis))

    st.subheader("RFI詳細")
    selected_rfi = st.selectbox("RFIを選択", [rfi["title"] for rfi in filtered_rfis])
    selected_rfi_data = next(rfi for rfi in filtered_rfis if rfi["title"] == selected_rfi)
    st.json(selected_rfi_data)

    st.subheader("カスタム属性")
    st.json(custom_attributes)

    st.subheader("ロケーション情報")
    st.json(locations_att)

    st.subheader("ロケーションノード")
    st.json(location_node)

    if st.button("RFIsを更新"):
        try:
            post_rfis(st.session_state.token, project_id, rfis_for_post[0])
            st.success("RFIsを更新しました！")
        except Exception as e:
            st.error(f"RFIsの更新中にエラーが発生しました: {str(e)}")

    st.subheader("RFIs テーブルビュー")
    rfi_table = create_rfi_table(filtered_rfis)
    st.dataframe(rfi_table)

def create_rfi_table(rfis):
    table_data = []
    for rfi in rfis:
        table_data.append({
            "Status": rfi.get("status"),
            "ID": rfi.get("customIdentifier"),
            "Title": rfi.get("title"),
            "Ball in court": ", ".join([r.get("name", "") for r in rfi.get("reviewers", [])]),
            "Due Date": rfi.get("dueDate"),
            "Location": ", ".join([l.get("name", "") for l in rfi.get("lbsIds", [])]),
            "Location Details": rfi.get("location", {}).get("name", ""),
            "External ID": rfi.get("reference", "")
        })
    return pd.DataFrame(table_data)
