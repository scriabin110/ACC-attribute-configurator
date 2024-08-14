import requests

code = input("認証コードを入力してください：")

url = "https://developer.api.autodesk.com/authentication/v2/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "client_id": "m6caOI8GGlylZY8FHGMtIWZvGiXUMZ6E3P6RLvEeGP6EpRjo",
    "client_secret":"xKFPThA7G2ZuOUvAZiZyiaoVA5Gws4mRA2NxEClz9GQ58utQEBKDDT0diA3PhBAN",
    "grant_type": "authorization_code",
    "code": code,  # ここに(1)で取得したコードを入力
    # 例) "ej7ejyUH8mN_0CA-wpujY1b5jgFvewOf3EAxDFDm" ← http://localhost:8080/api/auth/callback?code=ej7ejyUH8mN_0CA-wpujY1b5jgFvewOf3EAxDFDm
    "redirect_uri": "http://localhost:8080/api/auth/callback"
}

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    token_data = response.json()
    access_token = token_data["access_token"]
    # print(f"Access Token: {access_token}")
else:
    print(f"Error: {response.status_code}, {response.text}")

# print(access_token)

# Set the base URL for the Autodesk Construction Cloud (ACC) API
base_url = 'https://developer.api.autodesk.com'

# Set the headers including the access token
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

def get_projects():
    url = f'{base_url}/project/v1/hubs'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        hubs = response.json()['data']
        for hub in hubs:
            hub_id = hub['id']
            hub_name = hub['attributes']['name']
            print(f"Hub ID: {hub_id}, Name: {hub_name}")
            
            # Get projects for each hub
            projects_url = f'{base_url}/project/v1/hubs/{hub_id}/projects'
            projects_response = requests.get(projects_url, headers=headers)
            
            if projects_response.status_code == 200:
                projects = projects_response.json()['data']
                for project in projects:
                    project_id = project['id']
                    project_name = project['attributes']['name']
                    print(f"  Project ID: {project_id}, Name: {project_name}")
            else:
                print(f"Error getting projects for hub {hub_id}: {projects_response.status_code}, {projects_response.text}")
    else:
        print(f"Error getting hubs: {response.status_code}, {response.text}")

# Call the function to get projects
get_projects()