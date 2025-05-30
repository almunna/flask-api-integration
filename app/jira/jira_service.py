from flask import current_app
import requests
from requests.auth import HTTPBasicAuth
from flask import request

def create_issue(project_key, summary, description, issue_type="Task"):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type}
        }
    }

    response = requests.post(url, json=payload, headers=headers, auth=auth)
    return response.json()

# ✅ New function: List all accessible projects
def list_projects():
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/project"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code != 200:
        return {"error": response.text, "status": response.status_code}

    projects = response.json()
    return [{"name": p["name"], "key": p["key"]} for p in projects]

#get_myself
def get_myself():
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/myself"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code != 200:
        return {"error": response.text, "status": response.status_code}

    data = response.json()
    return {
        "name": data.get("displayName"),
        "email": data.get("emailAddress"),
        "locale": data.get("locale")
    }

#get_user
def get_user(account_id):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/user"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}
    params = {"accountId": account_id}

    response = requests.get(url, headers=headers, auth=auth, params=params)
    if response.status_code != 200:
        return {"error": response.text, "status": response.status_code}

    user = response.json()
    return {
        "name": user.get("displayName"),
        "email": user.get("emailAddress"),
        "locale": user.get("locale"),
        "accountId": user.get("accountId")
    }


#get_users
def get_users(query):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/user/search"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}
    params = {"query": query}

    response = requests.get(url, headers=headers, auth=auth, params=params)
    if response.status_code != 200:
        return {"error": response.text, "status": response.status_code}

    users = response.json()
    return [
        {
            "accountId": u.get("accountId"),
            "name": u.get("displayName"),
            "email": u.get("emailAddress"),
            "active": u.get("active")
        }
        for u in users
    ]
#get_projects
def get_projects():
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/project"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code != 200:
        return {"error": response.text, "status": response.status_code}

    projects = response.json()
    return [
        {
            "id": p.get("id"),
            "key": p.get("key"),
            "name": p.get("name"),
            "projectType": p.get("projectTypeKey"),
            "lead": p.get("lead", {}).get("displayName"),
            "url": p.get("self")
        }
        for p in projects
    ]

#get_project
def get_project(project_id_or_key):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/project/{project_id_or_key}"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code != 200:
        return {"error": response.text, "status": response.status_code}

    project = response.json()
    return {
        "id": project.get("id"),
        "key": project.get("key"),
        "name": project.get("name"),
        "projectType": project.get("projectTypeKey"),
        "description": project.get("description"),
        "lead": project.get("lead", {}).get("displayName") if project.get("lead") else None,
        "url": project.get("self"),
        "avatar": project.get("avatarUrls", {}).get("48x48")
    }

#get_project_roles
def get_project_roles(project_id_or_key):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/project/{project_id_or_key}/role"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code != 200:
        return {"error": response.text, "status": response.status_code}

    roles = response.json()

    return [
        {
            "name": name,
            "url": url
        }
        for name, url in roles.items()
    ]

#get_issue
def get_issue(issue_id_or_key):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code != 200:
        return {"error": response.text, "status": response.status_code}

    issue = response.json()
    fields = issue.get("fields", {})

    return {
        "id": issue.get("id"),
        "key": issue.get("key"),
        "summary": fields.get("summary"),
        "description": fields.get("description"),
        "issueType": fields.get("issuetype", {}).get("name"),
        "status": fields.get("status", {}).get("name"),
        "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
        "reporter": fields.get("reporter", {}).get("displayName") if fields.get("reporter") else None,
        "project": fields.get("project", {}).get("name"),
        "created": fields.get("created"),
        "updated": fields.get("updated"),
        "url": f"{base_url}/browse/{issue.get('key')}"
    }

#create_issue
def create_issue(data):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    fields = {
        "project": {"key": data["project_key"]},
        "summary": data["summary"],
        "issuetype": {"name": data.get("issue_type", "Task")}
    }

    if data.get("description"):
        fields["description"] = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": data["description"]
                        }
                    ]
                }
            ]
        }

    payload = {"fields": fields}

    response = requests.post(url, json=payload, headers=headers, auth=auth)
    if response.status_code != 201:
        return {"error": response.text, "status": response.status_code}

    issue = response.json()
    return {
        "id": issue.get("id"),
        "key": issue.get("key"),
        "url": f"{base_url}/browse/{issue.get('key')}"
    }

#update_issue
def update_issue(issue_id_or_key, updates):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    fields = {}

    if "summary" in updates:
        fields["summary"] = updates["summary"]

    if "description" in updates:
        fields["description"] = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": updates["description"]
                        }
                    ]
                }
            ]
        }

    if "issue_type" in updates:
        fields["issuetype"] = {"name": updates["issue_type"]}

    if not fields:
        return {"error": "No valid fields to update"}, 400

    payload = {"fields": fields}

    response = requests.put(url, json=payload, headers=headers, auth=auth)
    if response.status_code != 204:
        return {"error": response.text, "status": response.status_code}

    return {
        "key": issue_id_or_key,
        "updated": True,
        "url": f"{base_url}/browse/{issue_id_or_key}"
    }

#delete_issue
def delete_issue(issue_id_or_key):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.delete(url, headers=headers, auth=auth)

    if response.status_code == 204:
        return {
            "status": "success",
            "message": f"Issue {issue_id_or_key} deleted"
        }
    else:
        return {
            "status": "error",
            "message": f"Failed to delete issue {issue_id_or_key}",
            "details": response.text,
            "status_code": response.status_code
        }

#assign_issue
def assign_issue(issue_id_or_key, account_id):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/assignee"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "accountId": account_id
    }

    response = requests.put(url, json=payload, headers=headers, auth=auth)

    if response.status_code == 204:
        return {
            "status": "success",
            "message": f"Issue {issue_id_or_key} assigned to user {account_id}"
        }
    else:
        return {
            "status": "error",
            "message": "Failed to assign issue",
            "details": response.text,
            "status_code": response.status_code
        }

#transition_issue
def transition_issue(issue_id_or_key, transition_id):
    base_url = current_app.config["JIRA_BASE_URL"]
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/transitions"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "transition": {
            "id": transition_id
        }
    }

    response = requests.post(url, json=payload, headers=headers, auth=auth)
    try:
        response.raise_for_status()
        return {
            "status": "success",
            "message": f"Issue {issue_id_or_key} transitioned successfully.",
            "transition_id": transition_id
        }
    except requests.exceptions.HTTPError:
        return {
            "status": "error",
            "message": response.json()
        }
    
#get_transitions
def get_transitions(issue_id_or_key):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/transitions"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to fetch transitions",
            "details": response.text,
            "status_code": response.status_code
        }

    transitions = response.json().get("transitions", [])
    return [
        {
            "id": t.get("id"),
            "name": t.get("name"),
            "to_status": t.get("to", {}).get("name")
        }
        for t in transitions
    ]

#get_issue_comments
def get_issue_comments(issue_id_or_key):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/comment"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to retrieve comments",
            "details": response.text,
            "status_code": response.status_code
        }

    comments = response.json().get("comments", [])
    return [
        {
            "id": c.get("id"),
            "author": c.get("author", {}).get("displayName"),
            "body": c.get("body", {}).get("content", [{}])[0].get("content", [{}])[0].get("text"),
            "created": c.get("created")
        }
        for c in comments
    ]

#add_comment
def add_comment(issue_id_or_key, comment_text):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/comment"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": comment_text
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(url, json=payload, headers=headers, auth=auth)

    if response.status_code != 201:
        return {
            "status": "error",
            "message": "Failed to add comment",
            "details": response.text,
            "status_code": response.status_code
        }

    comment = response.json()
    return {
        "id": comment.get("id"),
        "created": comment.get("created"),
        "author": comment.get("author", {}).get("displayName"),
        "body": comment_text
    }

#update_comment
def update_comment(issue_id_or_key, comment_id, new_body):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/comment/{comment_id}"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": new_body
                        }
                    ]
                }
            ]
        }
    }

    response = requests.put(url, json=payload, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to update comment",
            "details": response.text,
            "status_code": response.status_code
        }

    comment = response.json()
    return {
        "id": comment.get("id"),
        "updated": comment.get("updated"),
        "body": new_body,
        "author": comment.get("author", {}).get("displayName")
    }

#delete_comment
def delete_comment(issue_id_or_key, comment_id):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/comment/{comment_id}"
    auth = HTTPBasicAuth(email, token)

    response = requests.delete(url, auth=auth)

    if response.status_code != 204:
        return {
            "status": "error",
            "message": "Failed to delete comment",
            "details": response.text,
            "status_code": response.status_code
        }

    return {
        "status": "success",
        "message": f"Comment {comment_id} deleted from issue {issue_id_or_key}"
    }

#get_issue_attachments
def get_issue_attachments(issue_id_or_key):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}?fields=attachment"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to fetch attachments",
            "details": response.text,
            "status_code": response.status_code
        }

    attachments = response.json().get("fields", {}).get("attachment", [])
    result = [
        {
            "id": att["id"],
            "filename": att["filename"],
            "mimeType": att.get("mimeType"),
            "size": att["size"],
            "created": att["created"],
            "author": att["author"]["displayName"],
            "url": att["content"]
        }
        for att in attachments
    ]

    return result

#add_attachment
def add_attachment(issue_id_or_key, file):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/attachments"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "X-Atlassian-Token": "no-check"
    }

    files = {
        "file": (file.filename, file.stream, file.mimetype)
    }

    response = requests.post(url, headers=headers, auth=auth, files=files)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to upload attachment",
            "details": response.text,
            "status_code": response.status_code
        }

    data = response.json()[0]
    return {
        "id": data["id"],
        "filename": data["filename"],
        "size": data["size"],
        "mimeType": data.get("mimeType"),
        "author": data["author"]["displayName"],
        "created": data["created"],
        "url": data["content"]
    }

#delete_attachment
def delete_attachment(attachment_id):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/attachment/{attachment_id}"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.delete(url, headers=headers, auth=auth)

    if response.status_code == 204:
        return {
            "status": "success",
            "message": f"Attachment {attachment_id} deleted"
        }
    else:
        return {
            "status": "error",
            "message": "Failed to delete attachment",
            "status_code": response.status_code,
            "details": response.text
        }

#get_issue_watchers
def get_issue_watchers(issue_id_or_key):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/watchers"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to retrieve watchers",
            "status_code": response.status_code,
            "details": response.text
        }

    data = response.json()
    return {
        "watchers": [
            {
                "accountId": watcher["accountId"],
                "displayName": watcher["displayName"],
                "emailAddress": watcher.get("emailAddress"),
                "active": watcher["active"]
            } for watcher in data.get("watchers", [])
        ]
    }

#add_watcher
def add_watcher(issue_id_or_key, account_id):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/watchers"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # According to Jira API, the body should be just the accountId or email in quotes
    payload = f"\"{account_id}\""

    response = requests.post(url, data=payload, headers=headers, auth=auth)

    if response.status_code == 204:
        return {
            "status": "success",
            "message": f"Watcher added to issue {issue_id_or_key}"
        }
    else:
        return {
            "status": "error",
            "message": "Failed to add watcher",
            "status_code": response.status_code,
            "details": response.text
        }

#remove_watcher
def remove_watcher(issue_id_or_key, account_id):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/watchers?accountId={account_id}"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json"
    }

    response = requests.delete(url, headers=headers, auth=auth)

    if response.status_code == 204:
        return {
            "status": "success",
            "message": f"Watcher removed from issue {issue_id_or_key}"
        }
    else:
        return {
            "status": "error",
            "message": "Failed to remove watcher",
            "status_code": response.status_code,
            "details": response.text
        }

#get_issue_votes
def get_issue_votes(issue_id_or_key):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/votes"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "status": "error",
            "message": "Failed to retrieve votes",
            "status_code": response.status_code,
            "details": response.text
        }

#add_vote
def add_vote(issue_id_or_key):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/votes"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, auth=auth)
    
    if response.status_code == 204:
        return {
            "message": f"Vote added to issue {issue_id_or_key}",
            "status": "success"
        }
    else:
        return {
            "message": f"Failed to add vote to issue {issue_id_or_key}",
            "details": response.text,
            "status": "error",
            "status_code": response.status_code
        }

#remove_vote
def remove_vote(issue_id_or_key):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/votes"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json"
    }

    response = requests.delete(url, headers=headers, auth=auth)
    if response.status_code == 204:
        return {
            "status": "success",
            "message": f"Vote removed from issue {issue_id_or_key}"
        }
    else:
        return {
            "status": "error",
            "message": f"Failed to remove vote from issue {issue_id_or_key}",
            "status_code": response.status_code,
            "details": response.text
        }

#get_issue_worklogs
def get_issue_worklogs(issue_id_or_key):
    from flask import current_app
    from requests.auth import HTTPBasicAuth
    import requests

    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/worklog"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code != 200:
        return {
            "status": "error",
            "message": f"Failed to retrieve worklogs for issue {issue_id_or_key}",
            "details": response.text,
            "status_code": response.status_code,
        }

    data = response.json()
    return {
        "issue": issue_id_or_key,
        "worklogs": [
            {
                "author": log["author"]["displayName"],
                "started": log["started"],
                "timeSpent": log["timeSpent"],
                "comment": log.get("comment", {}).get("content", []),
            }
            for log in data.get("worklogs", [])
        ],
    }

#add_worklog
def add_worklog(issue_id_or_key, time_spent, comment=None, started=None):
    from flask import current_app
    from requests.auth import HTTPBasicAuth
    import requests
    import datetime

    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/worklog"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "timeSpent": time_spent
    }

    if comment:
        payload["comment"] = {"type": "doc", "version": 1, "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": comment}]}
        ]}
    
    if started:
        # Format to: 2025-05-30T12:00:00.000+0000
        payload["started"] = started
    else:
        payload["started"] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000+0000")

    response = requests.post(url, json=payload, headers=headers, auth=auth)
    if response.status_code != 201:
        return {
            "status": "error",
            "message": "Failed to add worklog",
            "details": response.text,
            "status_code": response.status_code
        }
    return response.json()

#update_worklog
def update_worklog(issue_id_or_key, worklog_id, time_spent=None, comment=None, started=None):
    from flask import current_app
    from requests.auth import HTTPBasicAuth
    import requests
    import datetime

    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/worklog/{worklog_id}"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {}
    if time_spent:
        payload["timeSpent"] = time_spent
    if comment:
        payload["comment"] = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": comment}]
                }
            ]
        }
    if started:
        payload["started"] = started
    else:
        payload["started"] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000+0000")

    response = requests.put(url, json=payload, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to update worklog",
            "details": response.text,
            "status_code": response.status_code
        }

    return response.json()

#delete_worklog
def delete_worklog(issue_id_or_key, worklog_id):
    from flask import current_app
    from requests.auth import HTTPBasicAuth
    import requests

    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}/worklog/{worklog_id}"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.delete(url, headers=headers, auth=auth)

    if response.status_code == 204:
        return {
            "status": "success",
            "message": f"Worklog {worklog_id} deleted from issue {issue_id_or_key}"
        }

    return {
        "status": "error",
        "message": f"Failed to delete worklog {worklog_id} from issue {issue_id_or_key}",
        "details": response.text,
        "status_code": response.status_code
    }

#get_issue_types
def get_issue_types():
    from flask import current_app
    from requests.auth import HTTPBasicAuth
    import requests

    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/issuetype"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to fetch issue types",
            "details": response.text,
            "status_code": response.status_code
        }

    data = response.json()
    return [
        {
            "id": issue_type.get("id"),
            "name": issue_type.get("name"),
            "description": issue_type.get("description"),
            "subtask": issue_type.get("subtask")
        }
        for issue_type in data
    ]

#get_priorities
def get_priorities():
    from flask import current_app
    from requests.auth import HTTPBasicAuth
    import requests

    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/priority"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to fetch priorities",
            "details": response.text,
            "status_code": response.status_code
        }

    return [
        {
            "id": p.get("id"),
            "name": p.get("name"),
            "description": p.get("description"),
            "iconUrl": p.get("iconUrl")
        }
        for p in response.json()
    ]

#get_statuses
def get_statuses():
    from flask import current_app
    from requests.auth import HTTPBasicAuth
    import requests

    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/status"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to retrieve statuses",
            "details": response.text,
            "status_code": response.status_code
        }

    data = response.json()
    return [
        {
            "id": item.get("id"),
            "name": item.get("name"),
            "description": item.get("description"),
            "statusCategory": item.get("statusCategory", {}).get("name")
        }
        for item in data
    ]

#get_resolutions
def get_resolutions():
    from flask import current_app
    from requests.auth import HTTPBasicAuth
    import requests

    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/resolution"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to retrieve resolutions",
            "details": response.text,
            "status_code": response.status_code
        }

    return [
        {
            "id": r.get("id"),
            "name": r.get("name"),
            "description": r.get("description")
        }
        for r in response.json()
    ]

#search_issues
def search_issues(jql_query, max_results=50):
    from flask import current_app
    from requests.auth import HTTPBasicAuth
    import requests

    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/search"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "jql": jql_query,
        "maxResults": max_results
    }

    response = requests.post(url, json=payload, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to search issues",
            "details": response.text,
            "status_code": response.status_code
        }

    issues = response.json().get("issues", [])
    return [
        {
            "key": issue.get("key"),
            "summary": issue.get("fields", {}).get("summary"),
            "status": issue.get("fields", {}).get("status", {}).get("name"),
            "project": issue.get("fields", {}).get("project", {}).get("name"),
            "assignee": issue.get("fields", {}).get("assignee", {}).get("displayName") if issue.get("fields", {}).get("assignee") else None
        }
        for issue in issues
    ]

#get_favorites_filters
def get_favorite_filters():
    from flask import current_app
    from requests.auth import HTTPBasicAuth
    import requests

    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/api/3/filter/favourite"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to fetch favorite filters",
            "details": response.text,
            "status_code": response.status_code
        }

    filters = response.json()
    return [
        {
            "id": f["id"],
            "name": f["name"],
            "jql": f["jql"],
            "owner": f["owner"]["displayName"],
            "url": f["self"]
        }
        for f in filters
    ]

#get_board_issues
def get_board_issues(board_id):

    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/agile/1.0/board/{board_id}/issue"
    auth = HTTPBasicAuth(email, token)
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to fetch board issues",
            "details": response.text,
            "status_code": response.status_code
        }

    data = response.json()
    issues = data.get("issues", [])
    return [
        {
            "key": i["key"],
            "summary": i["fields"]["summary"],
            "status": i["fields"]["status"]["name"],
            "assignee": i["fields"]["assignee"]["displayName"] if i["fields"]["assignee"] else None
        }
        for i in issues
    ]

#get_sprints
def get_sprints(board_id):
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    url = f"{base_url}/rest/agile/1.0/board/{board_id}/sprint"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to fetch sprints",
            "details": response.text,
            "status_code": response.status_code
        }

    data = response.json()
    sprints = data.get("values", [])

    return [
        {
            "id": s["id"],
            "name": s["name"],
            "state": s["state"],
            "startDate": s.get("startDate"),
            "endDate": s.get("endDate"),
            "goal": s.get("goal")
        }
        for s in sprints
    ]

#get_user_permissions
def get_user_permissions():
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]

    permissions = request.args.get("permissions", "BROWSE_PROJECTS")

    url = f"{base_url}/rest/api/3/mypermissions?permissions={permissions}"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        return {
            "message": "Failed to retrieve user permissions",
            "status": "error",
            "status_code": response.status_code,
            "details": response.text
        }

    data = response.json().get("permissions", {})
    return [
        {
            "key": k,
            "name": v.get("name"),
            "granted": v.get("havePermission")
        } for k, v in data.items()
    ]

#get_user_notifications
def get_user_notifications():
    email = current_app.config["JIRA_EMAIL"]
    token = current_app.config["JIRA_API_TOKEN"]
    base_url = current_app.config["JIRA_BASE_URL"]
    

    url = f"{base_url}/rest/api/3/search"
    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)
    response.raise_for_status()

    issues = response.json().get("issues", [])
    return [
        {
            "key": issue["key"],
            "summary": issue["fields"]["summary"],
            "updated": issue["fields"]["updated"],
        }
        for issue in issues
    ]
