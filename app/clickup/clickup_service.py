
import requests
from app.config import Config

BASE_URL = Config.CLICKUP_API_BASE_URL
HEADERS = {
    "Authorization": Config.CLICKUP_API_TOKEN,
    "Content-Type": "application/json"
}

# get_user
def get_user():
    return requests.get(f"{BASE_URL}/user", headers=HEADERS).json()

# get_teams
def get_teams():
    return requests.get(f"{BASE_URL}/team", headers=HEADERS).json()

# get_spaces(team_id):

def get_spaces(team_id):
    return requests.get(f"{BASE_URL}/team/{team_id}/space", headers=HEADERS).json()

# get_folders
def get_folders(space_id):
    return requests.get(f"{BASE_URL}/space/{space_id}/folder", headers=HEADERS).json()

# get_lists
def get_lists(folder_id):
    return requests.get(f"{BASE_URL}/folder/{folder_id}/list", headers=HEADERS).json()

# get_tasks
def get_tasks(list_id):
    return requests.get(f"{BASE_URL}/list/{list_id}/task", headers=HEADERS).json()

# get_task
def get_task(task_id):
    return requests.get(f"{BASE_URL}/task/{task_id}", headers=HEADERS).json()

# create_task
def create_task(list_id, data):
    return requests.post(f"{BASE_URL}/list/{list_id}/task", headers=HEADERS, json=data).json()

# update_task
def update_task(task_id, data):
    return requests.put(f"{BASE_URL}/task/{task_id}", headers=HEADERS, json=data).json()

# delete_task
def delete_task(task_id):
    response = requests.delete(f"{BASE_URL}/task/{task_id}", headers=HEADERS)

    if response.status_code == 204:
        return {"status": "success", "message": "Task deleted successfully"}

    try:
        return response.json()
    except ValueError:
        return {"status": "error", "message": "Empty response", "code": response.status_code}


#  get_task_comments
def get_task_comments(task_id):
    return requests.get(f"{BASE_URL}/task/{task_id}/comment", headers=HEADERS).json()

# add_task_comment
def add_task_comment(task_id, comment):
    return requests.post(f"{BASE_URL}/task/{task_id}/comment", headers=HEADERS, json=comment).json()

# update_comment
def update_comment(comment_id, data):
    return requests.put(f"{BASE_URL}/comment/{comment_id}", headers=HEADERS, json=data).json()

# delete_comment
def delete_comment(comment_id):
    return requests.delete(f"{BASE_URL}/comment/{comment_id}", headers=HEADERS).json()

#get_custom_field
def get_custom_fields(list_id):
    url = f"{BASE_URL}/list/{list_id}/field"
    response = requests.get(url, headers=HEADERS)

    try:
        return response.json()
    except Exception:
        return {"status": response.status_code, "detail": response.text}

# add_custom_field_to_task
def add_custom_field_to_task(task_id, field_id, value):
    return requests.post(f"{BASE_URL}/task/{task_id}/field/{field_id}", headers=HEADERS, json={"value": value}).json()

# remove_custom_field_from_tas
def remove_custom_field_from_task(task_id, field_id):
    return requests.delete(f"{BASE_URL}/task/{task_id}/field/{field_id}", headers=HEADERS).json()

# get_checklists
def get_checklists(task_id):
    url = f"{BASE_URL}/task/{task_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data.get("checklists", [])

# create_checklist
def create_checklist(task_id, data):
    return requests.post(f"{BASE_URL}/task/{task_id}/checklist", headers=HEADERS, json=data).json()

# add_checklist_item
def add_checklist_item(checklist_id, data):
    return requests.post(f"{BASE_URL}/checklist/{checklist_id}/checklist_item", headers=HEADERS, json=data).json()

# 2update_checklist_item
def update_checklist_item(checklist_id, item_id, data):
    return requests.put(f"{BASE_URL}/checklist/{checklist_id}/checklist_item/{item_id}", headers=HEADERS, json=data).json()

# delete_checklist_item
def delete_checklist_item(checklist_id, item_id):
    return requests.delete(f"{BASE_URL}/checklist/{checklist_id}/checklist_item/{item_id}", headers=HEADERS).json()

# get_tags_from_task
def get_tags_from_task(task_id):
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    response = requests.get(url, headers=HEADERS)
    task = response.json()
    return task.get("tags", [])

# clickup_service.py
def add_tag_to_task(task_id, tag_name):
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    headers = HEADERS

    # First, get the current tags
    task_resp = requests.get(url, headers=headers)
    if task_resp.status_code != 200:
        return {
            "message": "Failed to retrieve task for tag update",
            "raw": task_resp.text,
            "status": "error"
        }

    task_data = task_resp.json()
    existing_tags = [tag["name"] for tag in task_data.get("tags", [])]

    # Avoid duplicates
    if tag_name not in existing_tags:
        existing_tags.append(tag_name)

    # Update the task with new tag list
    payload = {"tags": existing_tags}
    update_resp = requests.put(url, headers=headers, json=payload)

    if update_resp.status_code != 200:
        return {
            "message": "Failed to add tag to task",
            "raw": update_resp.text,
            "status": "error"
        }

    return update_resp.json()



# remove_tag_from_task
def remove_tag_from_task(task_id, tag_name):
    url = f"https://api.clickup.com/api/v2/task/{task_id}/tag/{tag_name}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 200:
        return {"message": "Tag removed successfully", "status": "success"}
    try:
        return {"message": "Failed to remove tag", "raw": response.text, "status": "error"}
    except:
        return {"message": "Invalid response", "status": "error"}


# get_time_entries
def get_time_entries(task_id):
    return requests.get(f"{BASE_URL}/task/{task_id}/time", headers=HEADERS).json()

#create_time_entry
def create_time_entry(task_id, data):
    return requests.post(f"{BASE_URL}/task/{task_id}/time", headers=HEADERS, json=data).json()

# add_deleted_tag_to_task
def add_deleted_tag_to_task(task_id):
    url = f"https://api.clickup.com/api/v2/task/{task_id}/tag/deleted"
    headers = HEADERS

    response = requests.post(url, headers=headers)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {
            "status": "error",
            "message": "Failed to tag task as deleted.",
            "raw": response.text,
            "status_code": response.status_code,
        }


# get_goal
def get_goal(goal_id):
    return requests.get(f"{BASE_URL}/goal/{goal_id}", headers=HEADERS).json()

# get_goals
def get_goals(team_id):
    return requests.get(f"{BASE_URL}/team/{team_id}/goal", headers=HEADERS).json()

# create_goal
def create_goal(team_id, data):
    return requests.post(f"{BASE_URL}/team/{team_id}/goal", headers=HEADERS, json=data).json()

# update_goal
def update_goal(goal_id, data):
    return requests.put(f"{BASE_URL}/goal/{goal_id}", headers=HEADERS, json=data).json()

# delete_goal
def delete_goal(goal_id):
    url = f"https://api.clickup.com/api/v2/goal/{goal_id}"
    headers = HEADERS

    response = requests.delete(url, headers=headers)  # ✅ define response here

    print("ClickUp DELETE response:", response.text)  # ✅ now this is valid

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {
            "status": "error",
            "message": "Invalid or empty response from ClickUp",
            "raw": response.text,
            "status_code": response.status_code
        }

#not available in clickup
# get_notification
def get_notifications():
    return requests.get(f"{BASE_URL}/notification", headers=HEADERS).json()


#get_task_time_in_status
def get_task_time_in_status(task_id):
    return requests.get(f"{BASE_URL}/task/{task_id}/time_in_status", headers=HEADERS).json()

#get_permissions
#not available in checkup
def get_permissions():
    url = f"{BASE_URL}/user"
    headers = HEADERS

    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {
            "status": "error",
            "message": "Invalid response from ClickUp",
            "raw": response.text,
            "status_code": response.status_code
        }

#get_shared_with_me
#not available on clickup
def get_shared_with_me(team_id):
    url = f"https://api.clickup.com/api/v2/team/{team_id}/task"
    headers = HEADERS
    params = {
        "assignees[]": "me",
        "include_closed": False
    }

    response = requests.get(url, headers=headers, params=params)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {
            "status": "error",
            "message": "Invalid response from ClickUp",
            "raw": response.text,
            "status_code": response.status_code
        }


# get_task_dependencies
def get_task_dependencies(task_id):
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    headers = HEADERS

    response = requests.get(url, headers=headers)
    try:
        data = response.json()
        return {
            "task_id": task_id,
            "dependencies": data.get("dependencies", [])
        }
    except requests.exceptions.JSONDecodeError:
        return {
            "status": "error",
            "message": "Invalid or empty response from ClickUp",
            "raw": response.text,
            "status_code": response.status_code
        }



# add_task_dependen
#not available on clickup
def add_task_dependency(task_id, depends_on_task_id):
    url = f"https://api.clickup.com/api/v2/task/{task_id}/dependency"
    headers = HEADERS
    payload = {
        "depends_on": depends_on_task_id
    }

    response = requests.post(url, headers=headers, json=payload)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {
            "status": "error",
            "message": "Invalid or empty response from ClickUp",
            "raw": response.text,
            "status_code": response.status_code
        }


# remove_task_dependency
#not available on clickup
def remove_task_dependency(task_id, depends_on_task_id):
    url = f"https://api.clickup.com/api/v2/task/{task_id}/dependency"
    headers = HEADERS
    payload = {
        "depends_on": depends_on_task_id
    }

    response = requests.delete(url, headers=headers, json=payload)
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {
            "status": "error",
            "message": "Invalid or empty response from ClickUp",
            "raw": response.text,
            "status_code": response.status_code
        }


# get_workspace_members
def get_workspace_members():
    url = "https://api.clickup.com/api/v2/user"
    headers = HEADERS
    response = requests.get(url, headers=headers)
    try:
        data = response.json()
        teams = data.get("user", {}).get("teams", [])
        members = []
        for team in teams:
            team_members = team.get("members", [])
            for member in team_members:
                user = member.get("user", {})
                members.append({
                    "team_id": team.get("id"),
                    "team_name": team.get("name"),
                    "user_id": user.get("id"),
                    "username": user.get("username"),
                    "email": user.get("email"),
                    "role": member.get("role")
                })
        return members
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


#get_list_members
def get_list_members(list_id):
    url = f"https://api.clickup.com/api/v2/list/{list_id}/member"
    headers = HEADERS

    response = requests.get(url, headers=headers)

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {
            "status": "error",
            "message": "Invalid or empty response from ClickUp",
            "raw": response.text,
            "status_code": response.status_code
        }


# assign_task
def assign_task(task_id, user_id):
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    headers = HEADERS

    payload = {
        "assignees": {
            "add": [user_id]
        }
    }

    response = requests.put(url, headers=headers, json=payload)

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {
            "status": "error",
            "message": "Invalid or empty response from ClickUp",
            "raw": response.text,
            "status_code": response.status_code
        }


# set_due_date
def set_due_date(task_id, due_date):
    return requests.put(f"{BASE_URL}/task/{task_id}", headers=HEADERS, json={"due_date": due_date}).json()

# 45
def get_team_settings(team_id):
    url = "https://api.clickup.com/api/v2/user"
    headers = HEADERS
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        teams = data.get("user", {}).get("teams", [])
        matched_team = next((t for t in teams if str(t.get("id")) == str(team_id)), None)

        if not matched_team:
            return {
                "status": "error",
                "message": f"Team ID {team_id} not found or not authorized"
            }

        return {
            "team_id": matched_team.get("id"),
            "name": matched_team.get("name"),
            "color": matched_team.get("color"),
            "avatar": matched_team.get("avatar"),
            "members_count": len(matched_team.get("members", [])),
            "members": [
                {
                    "user_id": m.get("user", {}).get("id"),
                    "username": m.get("user", {}).get("username"),
                    "email": m.get("user", {}).get("email"),
                    "role": m.get("role")
                }
                for m in matched_team.get("members", [])
            ]
        }

    except requests.RequestException as e:
        return {
            "status": "error",
            "message": str(e)
        }
