import streamlit as st

def print_attributes(attributes, item_type, item_id):
    if attributes:
        st.write(f"{'ファイル' if item_type == 'items' else 'フォルダ'}名: {attributes['displayName']}")
        st.write(f"ID: {item_id}")
        st.write(f"作成日時: {attributes['createTime']}")
        st.write(f"作成者: {attributes['createUserName']}")
        st.write(f"最終更新日時: {attributes['lastModifiedTime']}")
        st.write(f"最終更新者: {attributes['lastModifiedUserName']}")
        st.write(f"説明: {attributes.get('extension', {}).get('data', {}).get('description', 'N/A')}")
        st.write(f"バージョン: {attributes.get('extension', {}).get('version', 'N/A')}")
        try:
            st.write(f"フォルダ内のファイル: {attributes['objectCount']}")
        except:
            st.write(f"フォルダではありません。")
        st.write("-" * 50)
    
# この行を追加して関数をエクスポート
__all__ = ['print_attributes']