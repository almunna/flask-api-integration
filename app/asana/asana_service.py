import requests
from flask import current_app
from app.config import Config

HEADERS = {
    "Authorization": f"Bearer {Config.ASANA_PAT}",
    "Content-Type": "application/json"
}

BASE_URL = Config.ASANA_BASE_URL


def get_user_info():
    url = f"{BASE_URL}/users/me"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#get_user
def get_user(user_gid):
    url = f"{BASE_URL}/users/{user_gid}"
    response = requests.get(url, headers=HEADERS)
    return response.json()
#get_users
def get_users(workspace_gid):
    url = f"{BASE_URL}/workspaces/{workspace_gid}/users"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#get_workspace
def get_workspace(workspace_gid):
    url = f"{BASE_URL}/workspaces/{workspace_gid}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#get_workspaces
def get_workspaces():
    url = f"{BASE_URL}/workspaces"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#get_projects
def get_projects(workspace_gid):
    url = f"{BASE_URL}/projects?workspace={workspace_gid}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#get_project
def get_project(project_gid):
    url = f"{BASE_URL}/projects/{project_gid}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#create_project
def create_project(workspace_gid, name, notes=None, team_gid=None):
    url = f"{BASE_URL}/projects"
    payload = {
        "data": {
            "workspace": workspace_gid,
            "name": name
        }
    }
    if notes:
        payload["data"]["notes"] = notes
    if team_gid:
        payload["data"]["team"] = team_gid

    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

#update_project
def update_project(project_gid, updates):
    url = f"{BASE_URL}/projects/{project_gid}"
    payload = {
        "data": updates
    }
    response = requests.put(url, headers=HEADERS, json=payload)
    return response.json()

#delete_project
def delete_project(project_gid):
    url = f"{BASE_URL}/projects/{project_gid}"
    response = requests.delete(url, headers=HEADERS)
    return response.json()  # Asana returns confirmation

#get_tasks
def get_tasks(project_gid):
    url = f"{BASE_URL}/projects/{project_gid}/tasks"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#get_task
def get_task(task_gid):
    url = f"{BASE_URL}/tasks/{task_gid}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#create_task
def create_task(task_data):
    url = f"{BASE_URL}/tasks"
    payload = {
        "data": task_data
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

#update_task
def update_task(task_gid, updates):
    url = f"{BASE_URL}/tasks/{task_gid}"
    payload = {
        "data": updates
    }
    response = requests.put(url, headers=HEADERS, json=payload)
    return response.json()

#delete_task
def delete_task(task_gid):
    url = f"{BASE_URL}/tasks/{task_gid}"
    response = requests.delete(url, headers=HEADERS)
    return response.json()  # Asana returns a simple confirmation

#get_subtasks
def get_subtasks(task_gid):
    url = f"{BASE_URL}/tasks/{task_gid}/subtasks"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#add_subtask
def add_subtask(parent_task_gid, task_data):
    url = f"{BASE_URL}/tasks/{parent_task_gid}/subtasks"
    payload = {
        "data": task_data
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

#get_sections
def get_sections(project_gid):
    url = f"{BASE_URL}/projects/{project_gid}/sections"
    response = requests.get(url, headers=HEADERS)
    return response.json()
#create_section
def create_section(project_gid, name):
    url = f"{BASE_URL}/projects/{project_gid}/sections"
    payload = {
        "data": {
            "name": name
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

#add_task_to_section
def add_task_to_section(section_gid, task_gid):
    url = f"{BASE_URL}/sections/{section_gid}/addTask"
    payload = {
        "data": {
            "task": task_gid
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

#get_custom_fields
def get_project_custom_fields(project_gid):
    url = f"{BASE_URL}/projects/{project_gid}/custom_field_settings"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#get_tags
def get_tags(workspace_gid):
    url = f"{BASE_URL}/tags?workspace={workspace_gid}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#create_tag
def create_tag(workspace_gid, tag_name):
    url = f"{BASE_URL}/tags"
    payload = {
        "data": {
            "name": tag_name,
            "workspace": workspace_gid
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

#add_tag_to_task
def add_tag_to_task(task_gid, tag_gid):
    url = f"{BASE_URL}/tasks/{task_gid}/addTag"
    payload = {
        "data": {
            "tag": tag_gid
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

#remove_tag_from_task
def remove_tag_from_task(task_gid, tag_gid):
    url = f"{BASE_URL}/tasks/{task_gid}/removeTag"
    payload = {
        "data": {
            "tag": tag_gid
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

#get_comments
def get_comments(task_gid):
    url = f"{BASE_URL}/tasks/{task_gid}/stories"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#create_comment
def create_comment(task_gid, text):
    url = f"{BASE_URL}/tasks/{task_gid}/stories"
    payload = {
        "data": {
            "text": text
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

#get_stories
def get_stories(task_gid):
    url = f"{BASE_URL}/tasks/{task_gid}/stories"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#get_attachments
def get_attachments(task_gid):
    url = f"{BASE_URL}/tasks/{task_gid}/attachments"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#upload_attachment
def upload_attachment(task_gid, file):
    url = f"{BASE_URL}/tasks/{task_gid}/attachments"
    headers = {
        "Authorization": f"Bearer {Config.ASANA_PAT}"
        # ⚠️ Don't include Content-Type here, requests will set it correctly for multipart/form-data
    }
    files = {
        "file": (file.filename, file.stream, file.mimetype)
    }
    response = requests.post(url, headers=headers, files=files)
    return response.json()

#delete_attachment
def delete_attachment(attachment_gid):
    url = f"{BASE_URL}/attachments/{attachment_gid}"
    response = requests.delete(url, headers=HEADERS)
    return response.status_code == 200

#mark_task_complete
def mark_task_complete(task_gid):
    url = f"{BASE_URL}/tasks/{task_gid}"
    payload = {
        "data": {
            "completed": True
        }
    }
    response = requests.put(url, headers=HEADERS, json=payload)
    return response.json()

#assign_task
def assign_task(task_gid, assignee_gid):
    url = f"{BASE_URL}/tasks/{task_gid}"
    payload = {
        "data": {
            "assignee": assignee_gid
        }
    }
    response = requests.put(url, headers=HEADERS, json=payload)
    return response.json()

#set_due_date
def set_due_date(task_gid, due_on):
    url = f"{BASE_URL}/tasks/{task_gid}"
    payload = {
        "data": {
            "due_on": due_on  # Format: YYYY-MM-DD
        }
    }
    response = requests.put(url, headers=HEADERS, json=payload)
    return response.json()

#get_teams
def get_teams(organization_gid):
    url = f"{BASE_URL}/organizations/{organization_gid}/teams"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#get_team_projects
def get_team_projects(team_gid):
    url = f"{BASE_URL}/teams/{team_gid}/projects"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#get_team_users
def get_team_users(team_gid):
    url = f"{BASE_URL}/teams/{team_gid}/users"
    response = requests.get(url, headers=HEADERS)
    return response.json()

#favorite_project
user_favorites = {}

def add_favorite_project(user_gid, project):
    if user_gid not in user_favorites:
        user_favorites[user_gid] = []
    user_favorites[user_gid].append(project)
    return {"message": "Project favorited", "data": project}

#list_favorite
def list_favorite_projects(user_gid):
    return user_favorites.get(user_gid, [])

#unfavorite_project
def remove_favorite_project(user_gid, project_gid):
    if user_gid in user_favorites:
        user_favorites[user_gid] = [
            p for p in user_favorites[user_gid] if p.get("project_gid") != project_gid
        ]
    return {"message": "Project unfavorited"}

#duplicate_project
def get_project(project_gid):
    url = f"{BASE_URL}/projects/{project_gid}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_project_tasks(project_gid):
    url = f"{BASE_URL}/projects/{project_gid}/tasks"
    response = requests.get(url, headers=HEADERS)
    return response.json().get("data", [])

def get_task_details(task_gid):
    url = f"{BASE_URL}/tasks/{task_gid}"
    response = requests.get(url, headers=HEADERS)
    return response.json().get("data", {})

def create_project(name, workspace_gid):
    url = f"{BASE_URL}/projects"
    payload = {
        "data": {
            "name": name,
            "workspace": workspace_gid
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json().get("data", {})

def create_task_in_project(name, notes, project_gid, workspace_gid):
    url = f"{BASE_URL}/tasks"
    payload = {
        "data": {
            "name": name,
            "notes": notes,
            "projects": [project_gid],
            "workspace": workspace_gid
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json().get("data", {})

def duplicate_project(project_gid):
    original = get_project(project_gid)["data"]
    original_name = original["name"]
    workspace_gid = original["workspace"]["gid"]

    # Step 1: Create new project
    new_project = create_project(f"Copy of {original_name}", workspace_gid)
    new_project_gid = new_project["gid"]

    # Step 2: Copy tasks
    tasks = get_project_tasks(project_gid)
    for task in tasks:
        task_data = get_task_details(task["gid"])
        create_task_in_project(
            name=task_data.get("name", ""),
            notes=task_data.get("notes", ""),
            project_gid=new_project_gid,
            workspace_gid=workspace_gid
        )

    return {
        "message": "Project duplicated",
        "original_project": original_name,
        "new_project_gid": new_project_gid,
        "new_project_url": f"https://app.asana.com/0/{workspace_gid}/{new_project_gid}"
    }

#search_tasks
def search_tasks(workspace_gid, filters=None):
    url = f"{BASE_URL}/workspaces/{workspace_gid}/tasks/search"
    params = filters or {}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()
