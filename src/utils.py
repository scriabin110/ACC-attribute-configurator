import streamlit as st

# def print_attributes(attributes, item_type, item_id):
#     if attributes:
#         st.write(f"{'ファイル' if item_type == 'items' else 'フォルダ'}名: {attributes['displayName']}")
#         st.write(f"ID: {item_id}")
#         st.write(f"作成日時: {attributes['createTime']}")
#         st.write(f"作成者: {attributes['createUserName']}")
#         st.write(f"最終更新日時: {attributes['lastModifiedTime']}")
#         st.write(f"最終更新者: {attributes['lastModifiedUserName']}")
#         st.write(f"説明: {attributes.get('extension', {}).get('data', {}).get('description', 'N/A')}")
#         st.write(f"バージョン: {attributes.get('extension', {}).get('version', 'N/A')}")
#         try:
#             st.write(f"フォルダ内のファイル: {attributes['objectCount']}")
#         except:
#             st.write(f"フォルダではありません。")
#         st.write("-" * 50)
    
# # この行を追加して関数をエクスポート
# __all__ = ['print_attributes']

def get_attribute_value(attr_def_id, value, issue_attribute_definitions):
    for attr_def in issue_attribute_definitions['results']:
        if attr_def['id'] == attr_def_id:
            if attr_def['dataType'] == 'list':
                for option in attr_def['metadata']['list']['options']:
                    if option['id'] == value:
                        return option['value']
            return value
    return value

def flatten_issue_data(issues_dict, issue_attribute_definitions):
    flattened_data = []
    for issue_id, issue_data in issues_dict.items():
        flat_issue = issue_data.copy()
        flat_issue['id'] = issue_id
        
        # カスタム属性を展開
        for attr in issue_data['customAttributes']:
            attr_id = attr['attributeDefinitionId']
            attr_title = attr['title']
            attr_value = get_attribute_value(attr_id, attr['value'], issue_attribute_definitions)
            flat_issue[f'{attr_title}'] = attr_value
        
        del flat_issue['customAttributes']  # 元のcustomAttributes列を削除
        flattened_data.append(flat_issue)
    
    return flattened_data

# def unflatten_issue_data(flattened_data, issue_attribute_definitions):
#     unflattened_issues = {}
    
#     for flat_issue in flattened_data:
#         issue_id = flat_issue.pop('id')
#         unflattened_issue = flat_issue.copy()
        
#         # カスタム属性を再構築
#         custom_attributes = []
#         for attr_def in issue_attribute_definitions['results']:
#             attr_title = attr_def['title']
#             if attr_title in unflattened_issue:
#                 custom_attr = {
#                     'attributeDefinitionId': attr_def['id'],
#                     'value': unflattened_issue.pop(attr_title)
#                 }
#                 custom_attributes.append(custom_attr)
        
#         unflattened_issue['customAttributes'] = custom_attributes
        
#         # 不要なフィールドを削除
#         for key in list(unflattened_issue.keys()):
#             if key not in [
#                 "title", "description", "issueSubtypeId", "status", "assignedTo",
#                 "assignedToType", "dueDate", "locationId", "locationDetails",
#                 "rootCauseId", "customAttributes", "snapshotUrn", "startDate",
#                 "published", "watchers", "gpsCoordinates"
#             ]:
#                 del unflattened_issue[key]
        
#         unflattened_issues[issue_id] = unflattened_issue
    
#     return unflattened_issues


def unflatten_issue_data(flattened_data, issue_attribute_definitions):
    unflattened_issues = {}
    
    for flat_issue in flattened_data:
        issue_id = flat_issue.pop('id')
        unflattened_issue = {
            "title": flat_issue.get("title"),
            "description": flat_issue.get("description"),
            "issueSubtypeId": flat_issue.get("issueSubtypeId"),
            "status": flat_issue.get("status"),
            "assignedTo": flat_issue.get("assignedTo"),
            "assignedToType": flat_issue.get("assignedToType"),
            "dueDate": flat_issue.get("dueDate"),
            "locationId": flat_issue.get("locationId"),
            "locationDetails": flat_issue.get("locationDetails"),
            "rootCauseId": flat_issue.get("rootCauseId"),
            "snapshotUrn": flat_issue.get("snapshotUrn"),
            "startDate": flat_issue.get("startDate"),
            "published": flat_issue.get("published"),
            "watchers": flat_issue.get("watchers", []),
            "gpsCoordinates": flat_issue.get("gpsCoordinates")
        }
        
        # カスタム属性を再構築
        custom_attributes = []
        for attr_def in issue_attribute_definitions['results']:
            attr_title = attr_def['title']
            if attr_title in flat_issue:
                attr_value = flat_issue[attr_title]
                # リスト型の属性の場合、IDを探す
                if attr_def['dataType'] == 'list' and attr_def['metadata'].get('list'):
                    value_found = False
                    for option in attr_def['metadata']['list']['options']:
                        if option['value'] == attr_value:
                            attr_value = option['id']
                            value_found = True
                            break
                    if attr_value is not None and not value_found:
                        st.warning(f"警告: 属性 '{attr_title}' に無効な値 '{attr_value}' が指定されています。")
                        continue  # この属性をスキップ
                custom_attr = {
                    'attributeDefinitionId': attr_def['id'],
                    'value': attr_value
                }
                custom_attributes.append(custom_attr)
        
        unflattened_issue['customAttributes'] = custom_attributes
        
        # 不要なフィールドを削除
        # unflattened_issue = {k: v for k, v in unflattened_issue.items() if v is not None}
        
        unflattened_issues[issue_id] = unflattened_issue
    
    return unflattened_issues

def get_keys_from_value(d, val):
    return [k for k, v in d.items() if v == val]