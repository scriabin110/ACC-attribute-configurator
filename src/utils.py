import streamlit as st
import pandas as pd

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
        
        for attr in issue_data['customAttributes']:
            attr_id = attr['attributeDefinitionId']
            attr_title = attr['title']
            attr_value = get_attribute_value(attr_id, attr['value'], issue_attribute_definitions)
            flat_issue[f'{attr_title}'] = attr_value
        
        del flat_issue['customAttributes']
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
            "gpsCoordinates": flat_issue.get("gpsCoordinates"),
            # "displayId": flat_issue.get("displayId")
        }
        
        custom_attributes = []
        for attr_def in issue_attribute_definitions['results']:
            attr_title = attr_def['title']
            if attr_title in flat_issue:
                attr_value = flat_issue[attr_title]
                if attr_def['dataType'] == 'list' and attr_def['metadata'].get('list'):
                    value_found = False
                    for option in attr_def['metadata']['list']['options']:
                        if option['value'] == attr_value:
                            attr_value = option['id']
                            value_found = True
                            break
                    if attr_value is not None and not value_found:
                        st.warning(f"警告: 属性 '{attr_title}' に無効な値 '{attr_value}' が指定されています。")
                        continue
                custom_attr = {
                    'attributeDefinitionId': attr_def['id'],
                    'value': attr_value
                }
                custom_attributes.append(custom_attr)
        
        unflattened_issue['customAttributes'] = custom_attributes
        
        unflattened_issues[issue_id] = unflattened_issue
    
    return unflattened_issues


def preprocess_data(record):
    """
    APIの期待する形式にデータを変換する
    """
    if 'watchers' in record and record['watchers']:
        record['watchers'] = record['watchers'].split(',') if isinstance(record['watchers'], str) else [record['watchers']]
    
    # 日付フィールドの処理
    date_fields = ['dueDate', 'startDate']
    for field in date_fields:
        if field in record and pd.notnull(record[field]):
            try:
                # 既にYYYY-MM-DD形式の場合はそのまま使用
                if isinstance(record[field], str) and len(record[field].split('-')) == 3:
                    continue
                record[field] = pd.to_datetime(record[field]).strftime('%Y-%m-%d')
            except:
                st.warning(f"Invalid date format for {field}: {record[field]}")
                record[field] = None
    
    # NaN値の処理
    for key, value in record.items():
        if pd.isna(value):
            record[key] = None
    
    return record


def validate_data(record, attribute_definitions):
    """
    データの検証を行う
    """
    for attr, value in record.items():
        if attr in attribute_definitions:
            attr_def = attribute_definitions[attr]
            if value is None and attr_def.get('required', False):
                st.warning(f"Required attribute '{attr}' is missing.")
            elif value is not None:
                if attr_def['type'] == 'string' and not isinstance(value, str):
                    st.warning(f"Attribute '{attr}' should be a string, but got {type(value)}.")
                elif attr_def['type'] == 'number' and not isinstance(value, (int, float)):
                    st.warning(f"Attribute '{attr}' should be a number, but got {type(value)}.")
                # 他の型のチェックも必要に応じて追加