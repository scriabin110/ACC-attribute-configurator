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
    project_id = project_id
    url = f'https://developer.api.autodesk.com/bim360/docs/v1/projects/{project_id}/versions/{urllib.parse.quote(urn, safe="")}/custom-attributes:batch-update'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
        }
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

def get_issues(access_token, project_id, issue_type_id=None):
    # url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects"
    if issue_type_id is not None:
      url = f"https://developer.api.autodesk.com/construction/issues/v1/projects/{project_id}/issues?filter[issueTypeId]={issue_type_id}"
    else:
      url = f"https://developer.api.autodesk.com/construction/issues/v1/projects/{project_id}/issues"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"issues取得エラー: {response.text}")
    
def get_issue_attribute_mappings(access_token, project_id):
    url = f"https://developer.api.autodesk.com/construction/issues/v1/projects/{project_id}/issue-attribute-mappings"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"attribute_mappings取得エラー: {response.text}")

def get_issue_attribute_definitions(access_token, project_id):
    url = f"https://developer.api.autodesk.com/construction/issues/v1/projects/{project_id}/issue-attribute-definitions"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"attribute_mappings取得エラー: {response.text}")

def patch_issues(access_token, project_id, issue_id, data):
    project_id = project_id
    url = f'https://developer.api.autodesk.com/construction/issues/v1/projects/{project_id}/issues/{issue_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
        }
    # data = list(data)
    response = requests.patch(url, headers=headers, json=data)
    # response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"attribute_mappings取得エラー: {response.text}")

def get_project_users(access_token, project_id):
    url = f"https://developer.api.autodesk.com/construction/admin/v1/projects/{project_id}/users"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"users取得エラー: {response.text}")



def post_project_users(token, project_id, data):
    # url = f'https://developer.api.autodesk.com/construction/admin/v2/projects/{project_id}/users:import'
    url = f"https://developer.api.autodesk.com/construction/admin/v2/projects/{project_id}/users:import"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
        }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 202:
        return response.json()
    else:
        raise Exception(f"user登録エラー: {response.text}")
    

#project user用のデータ変換
def transform_user_data(input_data, company_dict, role_dict, product_list):
    def clean_name(name):
        name = name.replace('_', ' ')
        name = name.strip()
        return ' '.join(name.split())

    transformed_data = {"users": []}
    errors = []

    for index, user in enumerate(input_data, start=1):
        transformed_user = {
            "products": []
        }
        
        # 必須項目のチェック
        if 'companyName' not in user or not user['companyName']:
            errors.append(f"User {index}: Empty company name.")
        else:
            transformed_user["companyId"] = company_dict.get(user['companyName'])
            if transformed_user["companyId"] is None:
                errors.append(f"User {index}: Invalid Company name: {user['companyName']}")

        if 'roleName' not in user or not user['roleName']:
            errors.append(f"User {index}: Empty role name.")
        else:
            transformed_user["roleIds"] = [role_dict.get(user['roleName'])]  # 取得されるrole・roleIdは1つのみであると仮定
            if transformed_user["roleIds"] is None:
                errors.append(f"User {index}: Invalid role name.: {user['roleName']}")

        if 'email' not in user and 'id' not in user:
            errors.append(f"User {index}: Email address is required.")
        else:
            if 'email' in user:
                transformed_user['email'] = user['email']
            elif 'id' in user:
                transformed_user['userId'] = user['id']
        
        # 名前フィールドを追加（存在する場合）
        if 'firstName' in user and user['firstName']:
            transformed_user['firstName'] = clean_name(user['firstName'])
        if 'lastName' in user and user['lastName']:
            transformed_user['lastName'] = clean_name(user['lastName'])
        
        # 製品アクセス権限を変換
        for product in product_list:
            if product in user:
                transformed_user['products'].append({
                    "key": product,
                    "access": user[product]
                })


        # products = user.get('products')
        # if products:
        #     for product in products:
        #         if isinstance(product, dict) and 'key' in product and 'access' in product:
        #             transformed_user['products'].append({
        #                 "key": product['key'],
        #                 "access": product['access']
        #             })
        
        # 空の文字列や空のリストを削除
        transformed_user = {k: v for k, v in transformed_user.items() if v not in ['', [], None]}
        
        transformed_data['users'].append(transformed_user)

    # エラーがある場合、Streamlitのエラーメッセージを表示
    if errors:
        for error in errors:
            st.error(error)
        return None  # エラーがある場合はNoneを返す

    return transformed_data

def get_company_id(access_token, project_id, account_id):
    url = f"https://developer.api.autodesk.com/hq/v1/accounts/{account_id}/projects/{project_id}/companies"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"company_id取得エラー: {response.text}")

#patch_project_usersをとりあえず実装する
# 下記、とりあえずコピペした状態
# def patch_project_users(access_token, project_id, user_id, data):
#     url = f'https://developer.api.autodesk.com/construction/admin/v1/projects/{project_id}/users/{user_id}'
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json'
#         }
#     response = requests.patch(url, headers=headers, json=data)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise Exception(f"attribute_mappings取得エラー: {response.text}")

def delete_project_users(access_token, project_id, user_id):
    url = f'https://developer.api.autodesk.com/construction/admin/v1/projects/{project_id}/users/{user_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        }
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        return response.json()
    else:
        raise Exception(f"Project_user削除エラー: {response.text}")

def patch_project_users(access_token, project_id, user_id, user_data):
    # url = f"https://developer.api.autodesk.com/construction/admin/v1/projects/{project_id}/users"
    url = f"https://developer.api.autodesk.com/construction/admin/v1/projects/{project_id}/users/{user_id}"
    # ここのurlは変更する
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.patch(url, headers=headers, json=user_data)
    # response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"patch_userエラー: {response.text}")

def get_rfis(access_token, container_id):
# def get_rfis(access_token):
    url = f"https://developer.api.autodesk.com/bim360/rfis/v2/containers/{container_id}/rfis"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"rfis取得エラー: {response.json()}")
