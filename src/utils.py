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

def filter_json_data(json_data):
    filtered_data = []
    
    for item in json_data:
        reviewers = item.get("reviewers")
        if reviewers is None:
            reviewer_ids = []
        elif isinstance(reviewers, list):
            reviewer_ids = [reviewer.get("oxygenId") for reviewer in reviewers if isinstance(reviewer, dict) and "oxygenId" in reviewer]
        elif isinstance(reviewers, dict):
            reviewer_ids = [reviewers.get("oxygenId")] if "oxygenId" in reviewers else []
        else:
            reviewer_ids = []

        location = item.get("location")
        location_description = location.get("description") if isinstance(location, dict) else None

        filtered_item = {
            "status": item.get("status"),
            "id": item.get("id"),
            "title": item.get("title"),
            "reviewerId": reviewer_ids[0] if reviewer_ids else None,
            "dueDate": item.get("dueDate"),
            "lbsIds": item.get("lbsIds"),
            "location": location_description,
            "reference": item.get("reference")
        }
        filtered_data.append(filtered_item)
    
    return filtered_data


def transform_to_bim360_format(filtered_data):
    bim360_data = []
    
    for item in filtered_data:
        bim360_item = {
            "id": item.get("id", ""),
            "status": item.get("status", "open"),
            "title": item.get("title", ""),
            "question": "",  # 元のデータにはこのフィールドがないため、空文字列を設定
            "suggestedAnswer": "",  # 元のデータにはこのフィールドがないため、空文字列を設定
            "assignedTo": item.get("reviewerId", ""),
            "linkedDocument": "",  # 元のデータにはこのフィールドがないため、空文字列を設定
            "linkedDocumentVersion": None,  # 元のデータにはこのフィールドがないため、Noneを設定
            "location": {
                "description": item.get("location", "")
            },
            "dueDate": item.get("dueDate"),
            "costImpact": "",  # 元のデータにはこのフィールドがないため、空文字列を設定
            "scheduleImpact": "",  # 元のデータにはこのフィールドがないため、空文字列を設定
            "priority": "",  # 元のデータにはこのフィールドがないため、空文字列を設定
            "discipline": [],  # 元のデータにはこのフィールドがないため、空のリストを設定
            "category": [],  # 元のデータにはこのフィールドがないため、空のリストを設定
            "reference": item.get("reference", ""),
            "sheetMetadata": {},  # 元のデータにはこのフィールドがないため、空の辞書を設定
            "coReviewers": [],  # 元のデータにはこのフィールドがないため、空のリストを設定
            "distributionList": [],  # 元のデータにはこのフィールドがないため、空のリストを設定
            "pushpinAttributes": {
                "externalId": "",
                "location": {},
                "objectId": "",
                "type": "TwoDRasterPushpin",
                "viewerState": {},
                "attributesVersion": 1
            }
        }
        
        # lbsIdsフィールドがある場合、それを追加
        if "lbsIds" in item:
            bim360_item["lbsIds"] = item["lbsIds"]
        
        bim360_data.append(bim360_item)
    
    return bim360_data