import os

# Streamlit Cloudで動作しているかどうかを確認
is_streamlit_cloud = os.environ.get('STREAMLIT_CLOUD') == 'true'

if is_streamlit_cloud:
    from dotenv import load_dotenv
    # Streamlit Cloudで動作している場合の設定

    load_dotenv()
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    CALLBACK_URL = os.getenv('CALLBACK_URL')
    SCOPES = ['data:read', 'data:write', 'data:create']