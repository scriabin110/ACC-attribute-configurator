import base64
import requests
import json

# クライアントIDとクライアントシークレットをBase64エンコード
client_id = 'm6caOI8GGlylZY8FHGMtIWZvGiXUMZ6E3P6RLvEeGP6EpRjo'
client_secret = 'xKFPThA7G2ZuOUvAZiZyiaoVA5Gws4mRA2NxEClz9GQ58utQEBKDDT0diA3PhBAN'
encoded_credentials = base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()

# トークンを取得するためのリクエスト
url = 'https://developer.api.autodesk.com/authentication/v2/token'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'Authorization': f'Basic {encoded_credentials}'
}
data = {
    'grant_type': 'client_credentials',
    'scope': 'data:read account:write bucket:read'
}

response = requests.post(url, headers=headers, data=data)
token = response.json().get('access_token')
print(f'Access Token: {token}')

# token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjY0RE9XMnJoOE9tbjNpdk1NU0xlNGQ2VHEwUV9SUzI1NiIsInBpLmF0bSI6ImFzc2MifQ.eyJzY29wZSI6WyJkYXRhOmNyZWF0ZSIsImRhdGE6cmVhZCIsImRhdGE6d3JpdGUiXSwiY2xpZW50X2lkIjoibTZjYU9JOEdHbHlsWlk4RkhHTXRJV1p2R2lYVU1aNkUzUDZSTHZFZUdQNkVwUmpvIiwiaXNzIjoiaHR0cHM6Ly9kZXZlbG9wZXIuYXBpLmF1dG9kZXNrLmNvbSIsImF1ZCI6Imh0dHBzOi8vYXV0b2Rlc2suY29tIiwianRpIjoiY3ZzN2FmaXJPc0hXdUhYVk9BM3ByRTFlSHlXWXZ3OHprRzFjQWFwRXd2ekluV0JnZkV6dVlReXpsSmRHV2pMRCIsImV4cCI6MTcyMzA3Nzg3NCwidXNlcmlkIjoiMlM2Mlc3UEVMMlJEQ0VWSCJ9.BWwnAmmFbufb06Urb5AEspjXgHQHBMxlOkCaPWuPEx6P3O3y8UcuDMSfy6XNhgnWSfe2v6ihyaiBqskqkdQiQ-mjS_-VukNmbHwObcZPuYjzbdKpmi4n8HhrN7p3q8K5_2UpOYla7RruV9RqtO7_e_DX1loBLvcB7SW1iQiQthICOjNn8ZBLswOH8PkOeX2vynGVQqwMrXwZelN54nEiH__g8AlePBJLykaEz6U5VIRX7yu8ZyDemfONTT5uEKnMeyjPVOGoDlczZboC9VzSZjyNOMioZS4hk5BvVixSjPQfOP46gRNHq5zIiiaeHiU9pjYR2_lnNyCrl7NfBEUhhQ"

# 取得したアクセストークンを使用してハブIDを取得
acc_url = 'https://developer.api.autodesk.com/project/v1/hubs'
acc_headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

acc_response = requests.get(acc_url, headers=acc_headers)
hubs = acc_response.json()
print(json.dumps(hubs, indent=4))  # JSONをフォーマットして表示

# ハブIDを使用して次のAPIリクエストを実行
# 例として、最初のハブIDを使用
hub_id = hubs['data'][0]['id']
projects_url = f'https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects'
projects_response = requests.get(projects_url, headers=acc_headers)
projects = projects_response.json()
# print(json.dumps(projects, indent=4))  # JSONをフォーマットして表示
print(len(hubs['data']))



'''
レスポンスの内容を日本語で説明します。

### レスポンスの概要
このレスポンスは、Autodesk Construction Cloud (ACC) APIから取得したハブ（プロジェクトのグループ）に関する情報です。

### 主な内容
1. **JSON APIのバージョン**:
    - `jsonapi`: `version`が`1.0`であることを示しています。

2. **リンク**:
    - `links`: `self`には、リクエストしたURLが含まれています。

3. **データ**:
    - `data`: ハブに関する情報が含まれています。
        - `type`: `hubs`（ハブの種類）
        - `id`: ハブのID（例: `b.21cd4449-77cc-4f14-8dd8-597a5dfef551`）
        - `attributes`: ハブの属性
            - `name`: ハブの名前（例: `JGC GLOBAL ESC`）
            - `extension`: 拡張情報
                - `type`: `hubs:autodesk.bim360:Account`
                - `version`: `1.0`
                - `schema`: スキーマのURL
                - `data`: 空のデータ
            - `region`: ハブの地域（例: `US`）
        - `links`: ハブの詳細情報へのリンク
            - `self`: ハブのURL
        - `relationships`: ハブに関連するプロジェクト
            - `projects`: プロジェクトのリンク

4. **メタ情報**:
    - `meta`: 警告メッセージが含まれています。
        - `warnings`: 警告のリスト
            - `HttpStatusCode`: `403`（アクセス権限がないことを示すステータスコード）
            - `ErrorCode`: `BIM360DM_ERROR`
            - `Title`: エラーメッセージのタイトル
            - `Detail`: エラーメッセージの詳細（例: "You don't have permission to access this API"）

### 警告メッセージ
- EMEA（ヨーロッパ、中東、アフリカ）およびAPAC（アジア太平洋地域）のBIM360DMハブにアクセスする権限がないため、これらのハブの情報を取得できなかったことを示しています。

この情報が役に立つことを願っています。何か他に質問があれば教えてください！
'''
