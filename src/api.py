import requests
import streamlit as st
import urllib.parse
import pandas as pd
import json
from collections import defaultdict

def get_projects(access_token, hub_id):
    url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception(f"プロジェクト取得エラー: {response.text}")

def get_top_folders(access_token, hub_id, project_id):
    url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects/{project_id}/topFolders"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception(f"トップフォルダ取得エラー: {response.text}")

def get_folder_contents(access_token, project_id, folder_id):
    url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/folders/{folder_id}/contents"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f"Warning: Unable to retrieve folder contents. Status code: {response.status_code}")
        return []

def get_file_attributes(access_token, project_id, file_id):
    file_detail_url = f'https://developer.api.autodesk.com/data/v1/projects/{project_id}/items/{file_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(file_detail_url, headers=headers)
    if response.status_code == 200:
        file_detail = response.json()
        return file_detail['data']['attributes']
    else:
        print(f'Error retrieving file attributes for {file_id}: {response.status_code}')
        return None
    
def get_folder_attributes(access_token, project_id, folder_id):
    folder_detail_url = f'https://developer.api.autodesk.com/data/v1/projects/{project_id}/folders/{folder_id}'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(folder_detail_url, headers=headers)
    if response.status_code == 200:
        folder_detail = response.json()
        return folder_detail['data']['attributes']
    else:
        print(f'Error retrieving folder attributes for {folder_id}: {response.status_code}')
        return None

def get_item_attributes(access_token, project_id, item_id, item_type):
    if item_type == 'items':
        return get_file_attributes(access_token, project_id, item_id)
    elif item_type == 'folders':
        return get_folder_attributes(access_token, project_id, item_id)
    else:
        print(f'Unknown item type: {item_type}')
        return None

def get_document_id(access_token, project_id, folder_id):
    url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/folders/{folder_id}/contents"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"エラー: APIリクエストが失敗しました。ステータスコード: {response.status_code}")
        return []
    
    data = response.json()
    included = data.get('included', [])
    
    document_ids = []
    for item in included:
        if 'id' in item:
            document_ids.append(item['id'])
    
    return document_ids
    # return None

def get_custom_Attribute(token, project_id, urns):
    url = f'https://developer.api.autodesk.com/bim360/docs/v1/projects/{project_id}/versions:batch-get'
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'urns': urns
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def get_custom_Attribute_Definition(token, project_id, folder_id):
    # token = get_access_token(auth_code)
    # hub_id = 'b.21cd4449-77cc-4f14-8dd8-597a5dfef551'
    # project_id = 'b.1fd68d4e-de62-4bc3-a909-8b0baeec77e4'
    # folder_id = 'urn:adsk.wipprod:fs.folder:co.bbBsDQe2QDWHWZMhIMr3PQ'
    url = f'https://developer.api.autodesk.com/bim360/docs/v1/projects/{project_id}/folders/{folder_id}/custom-attribute-definitions'
    headers = {'Authorization': f'Bearer {token}'}
    # data = {
    #     'urns': [
    #         'urn:adsk.wipprod:fs.file:vf.3Lqfodg2RB6FYptKDOZ6-Q?version=1'
    #     ]
    # }
    # response = requests.post(url, headers=headers, json=data)
    response = requests.get(url, headers=headers)
    return response.json()

def update_custom_Attribute(token, project_id, urn, data):
    # token = get_access_token(auth_code)
    # hub_id = 'b.21cd4449-77cc-4f14-8dd8-597a5dfef551'
    project_id = project_id
    # folder_id = 'urn:adsk.wipprod:fs.folder:co.bbBsDQe2QDWHWZMhIMr3PQ'
    # urn = 'urn:adsk.wipprod:fs.file:vf.3Lqfodg2RB6FYptKDOZ6-Q?version=1'
    url = f'https://developer.api.autodesk.com/bim360/docs/v1/projects/{project_id}/versions/{urllib.parse.quote(urn, safe="")}/custom-attributes:batch-update'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
        }
    # data = [
    #     {
    #         "id": 5064287,
    #         "value": "ほげほげ"
    #     }
    # ]
    data = list(data)
    response = requests.post(url, headers=headers, json=data)
    data = response.json()
    # df = pd.DataFrame(data['results'])
    return data

def transform_data(input_data):
    # urnでグループ化するための辞書を作成
    result = defaultdict(list)

    # 入力データを処理
    for item in input_data.values():
        urn = item['urn']
        result[urn].append({
            'id': item['id'],
            'value': item['value']
        })

    # defaultdictを通常の辞書に変換
    return dict(result)

# issue_idとissue_titleをセットにした辞書を返す関数
def get_issue_types(access_token, project_id):
    url = f"https://developer.api.autodesk.com/construction/issues/v1/projects/{project_id}/issue-types"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        dir_issue_types = {}
        for i in response.json()["results"]:
          dir_issue_types[i['title']] = i['id']
        return dir_issue_types
    else:
        raise Exception(f"issues取得エラー: {response.text}")