import streamlit as st
from src.auth import *
from src.api import *
from src.utils import *

def run(token, project_id, urns):
    if 'token' not in st.session_state or not st.session_state.token:
        st.error("認証が必要です。メインページで認証を行ってください。")
        return

    if 'current_project_id' not in st.session_state or not st.session_state.current_project_id:
        st.error("プロジェクトが選択されていません。サイドバーでプロジェクトを選択してください。")
        return

    # ゆくゆくはここもconfig.pyとかに移動する？
    st.session_state.update_mode = st.radio(
        "Mode:  ", 
        ["🦾 Manual Update", "📈 ***Excel Batch Update***"], 
        captions = ["Directly update issues", "Batch update issues via Excel file"],
        horizontal=True)

    if st.session_state.update_mode == "🦾 Manual Update":
        manual_update(token, project_id, urns)
        # manual_update()
    elif st.session_state.update_mode == "📈 ***Excel Batch Update***":
        excel_batch_update(token, project_id)
        # excel_batch_update()

def manual_update(token, project_id, urns):
    # "🦾 Manual Update"
    try:
        if st.session_state.urns:
            json_data = get_custom_Attribute(token, project_id, urns)['results']
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


def excel_batch_update(token, project_id):
    #"📈 Custom Attributes"
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
                        token=token,
                        project_id=project_id,
                        urn=urn,
                        data=data_list
                    )
                st.success("カスタム属性を更新しました！")
        except Exception as e:
            st.error(f"ファイルの読み込み中にエラーが発生しました: {str(e)}")
    else:
        st.markdown('**:red[Upload File(.xlsx/.xls/.csv)]**')
