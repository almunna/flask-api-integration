import requests
from app.config import Config
import os

def get_app_access_token():
    """
    Use client credentials to obtain an app-only Microsoft Graph access token.
    """
    url = f"https://login.microsoftonline.com/{Config.MS_TENANT_ID}/oauth2/v2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": Config.MS_CLIENT_ID,
        "scope": "https://graph.microsoft.com/.default",
        "client_secret": Config.MS_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        print("❌ Failed to get token:", response.status_code, response.text)
        return None

    token_data = response.json()
    return token_data.get("access_token")


def get_graph_headers(access_token):
    """
    Create common headers for Microsoft Graph API requests.
    """
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }


def graph_get(url, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return safe_json(response)



def graph_post(url, access_token, payload):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=payload)
    return safe_json(response)


def list_joined_teams(access_token=None):
   
    if not access_token:
        access_token = get_app_access_token()

    if not access_token:
        return {"error": "Access token is missing or invalid."}

    url = f"{Config.MS_GRAPH_API_BASE_URL}/groups?$filter=resourceProvisioningOptions/Any(x:x eq 'Team')"
    return graph_get(url, access_token)


def list_user_joined_teams(user_access_token):
    """
    List Microsoft Teams the user has explicitly joined.
    Requires a user-delegated token with Team.ReadBasic.All.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/me/joinedTeams"
    return graph_get(url, user_access_token)


def get_team_details(team_id, access_token):

    url = f"{Config.MS_GRAPH_API_BASE_URL}/teams/{team_id}"
    return graph_get(url, access_token)


def safe_json(response):
  
    try:
        return response.json()
    except Exception as e:
        return {
            "error": "Failed to parse response",
            "details": str(e),
            "raw": response.text,
            "status": response.status_code
        }

#list channels
def list_team_channels(team_id, access_token):
    """
    List all channels in a Microsoft Team.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/teams/{team_id}/channels"
    return graph_get(url, access_token)

#get channel
def get_channel_details(team_id, channel_id, access_token):
    """
    Retrieve details about a specific channel in a team.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/teams/{team_id}/channels/{channel_id}"
    return graph_get(url, access_token)

#list chats
def list_user_chats(user_access_token):
    """
    List all chats the user is part of.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/me/chats"
    return graph_get(url, user_access_token)

#get chats
def get_chat_details(chat_id, user_access_token):
    """
    Get details of a specific chat by ID.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/chats/{chat_id}"
    return graph_get(url, user_access_token)

#message list
def list_chat_messages(chat_id, user_access_token):
    """
    List all messages from a specific chat.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/chats/{chat_id}/messages"
    return graph_get(url, user_access_token)

#send message
def send_message_to_channel(team_id, channel_id, message, user_access_token):
    """
    Send a plain text message to a channel in a team.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/teams/{team_id}/channels/{channel_id}/messages"
    payload = {
        "body": {
            "content": message
        }
    }
    return graph_post(url, user_access_token, payload)

##list messages (channel)
def list_channel_messages(team_id, channel_id, user_access_token):
    """
    List messages from a specific channel within a team.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/teams/{team_id}/channels/{channel_id}/messages"
    return graph_get(url, user_access_token)

#replay to message (chat)
def reply_to_chat_message(chat_id, message_id, reply_text, user_access_token):
    """
    Reply to a message in a specific chat.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/chats/{chat_id}/messages/{message_id}/replies"
    payload = {
        "body": {
            "content": reply_text
        }
    }
    return graph_post(url, user_access_token, payload)

#reply to message (channel)
def reply_to_channel_message(team_id, channel_id, message_id, reply_text, user_access_token):
    """
    Reply to a message in a channel.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/teams/{team_id}/channels/{channel_id}/messages/{message_id}/replies"
    payload = {
        "body": {
            "content": reply_text
        }
    }
    return graph_post(url, user_access_token, payload)

#list members (team)
def list_team_members(team_id, access_token):
    """
    List all members of a specific Microsoft Teams team.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/teams/{team_id}/members"
    return graph_get(url, access_token)

#list members (chat)
def list_chat_members(chat_id, user_access_token):
    """
    List all members in a specific Microsoft Teams chat.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/chats/{chat_id}/members"
    return graph_get(url, user_access_token)

#get user
def get_user_by_id(user_id, access_token):
    """
    Get user details by user ID.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/users/{user_id}"
    return graph_get(url, access_token)

#get me
def get_logged_in_user(access_token):
    """
    Get details of the currently authenticated user.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/me"
    return graph_get(url, access_token)

#get presence
def get_user_presence(user_id, access_token):
    """
    Get the presence status of a specific user.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/users/{user_id}/presence"
    return graph_get(url, access_token)

#create chat
def create_chat_thread(user_ids, access_token):
    """
    Create a new chat thread with a list of user IDs.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/chats"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    members = [{
        "@odata.type": "#microsoft.graph.aadUserConversationMember",
        "roles": ["owner"],
        "user@odata.bind": f"https://graph.microsoft.com/v1.0/users/{uid}"
    } for uid in user_ids]

    payload = {
        "chatType": "group" if len(user_ids) > 2 else "oneOnOne",
        "members": members
    }

    response = requests.post(url, headers=headers, json=payload)
    return safe_json(response)

##create channel
def create_channel_in_team(team_id, channel_data, access_token):
    """
    Create a new channel inside the specified team.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/teams/{team_id}/channels"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=channel_data)
    return safe_json(response)

##schedule meeting
def schedule_teams_meeting(meeting_data, access_token):
    """
    Schedule a Teams meeting using /me/onlineMeetings.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/me/onlineMeetings"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=meeting_data)
    return safe_json(response)

#get meeeting
def get_meeting_details(meeting_id, access_token):
    """
    Retrieve a scheduled Teams meeting by its ID.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/me/onlineMeetings/{meeting_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    return safe_json(response)

#list calendar events
def list_calendar_events(access_token, user_id=None):
    """
    List calendar events for the authenticated user or a specific user.
    """
    base_url = f"{Config.MS_GRAPH_API_BASE_URL}/me/events" if not user_id else f"{Config.MS_GRAPH_API_BASE_URL}/users/{user_id}/events"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(base_url, headers=headers)
    return safe_json(response)

#add event
def create_calendar_event(event_data, access_token, user_id=None):
    """
    Create a calendar event with an optional Teams link.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/me/events"
    if user_id:
        url = f"{Config.MS_GRAPH_API_BASE_URL}/users/{user_id}/events"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=event_data)
    return safe_json(response)

#update event
def update_calendar_event(event_id, update_data, access_token, user_id=None):
    """
    Update a Microsoft calendar event by ID.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/me/events/{event_id}"
    if user_id:
        url = f"{Config.MS_GRAPH_API_BASE_URL}/users/{user_id}/events/{event_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.patch(url, headers=headers, json=update_data)

    try:
        return response.json()
    except Exception as e:
        return {
            "error": "Failed to parse response",
            "details": str(e),
            "raw": response.text,
            "status": response.status_code
        }

#delete event
def delete_calendar_event(event_id, access_token, user_id=None):
    """
    Delete a calendar event by ID.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/me/events/{event_id}"
    if user_id:
        url = f"{Config.MS_GRAPH_API_BASE_URL}/users/{user_id}/events/{event_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return {"status": "Event deleted successfully."}
    else:
        try:
            return response.json()
        except Exception as e:
            return {
                "error": "Failed to parse response",
                "details": str(e),
                "raw": response.text,
                "status": response.status_code
            }

#list files (team)
def list_team_files(team_id, access_token):
    """
    Lists files in the root of a Team's default document library.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/groups/{team_id}/drive/root/children"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except Exception as e:
        return {
            "error": "Failed to parse response",
            "details": str(e),
            "raw": response.text,
            "status": response.status_code
        }

#list files (chat)
def list_files_in_chat(chat_id, access_token):
    """
    Lists files shared in a chat by extracting attachments from messages.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/chats/{chat_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    try:
        messages = response.json().get("value", [])
        files = []

        for msg in messages:
            # Files may be found in attachments or inside message body
            attachments = msg.get("attachments", [])
            for att in attachments:
                if att.get("contentType") == "reference":
                    files.append({
                        "name": att.get("name"),
                        "url": att.get("contentUrl"),
                        "type": att.get("contentType")
                    })

        return files
    except Exception as e:
        return {
            "error": "Failed to parse response",
            "details": str(e),
            "raw": response.text,
            "status": response.status_code
        }

#upload file (chat)

def upload_file_to_onedrive(file_path, access_token):
    """
    Uploads a file to OneDrive in a 'ChatUploads' folder.
    """
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/ChatUploads/{os.path.basename(file_path)}:/content"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream"
    }

    with open(file_path, "rb") as f:
        response = requests.put(url, headers=headers, data=f)
    return response.json()


def create_share_link(file_id, access_token):
    """
    Creates a shareable link for the uploaded file.
    """
    url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/createLink"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {"type": "view", "scope": "anonymous"}
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def send_file_link_to_chat(chat_id, share_url, file_name, access_token):
    """
    Sends the share link as a message to the specified chat.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/chats/{chat_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "body": {
            "contentType": "html",
            "content": f'<a href="{share_url}">{file_name}</a>'
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def upload_file_to_chat(chat_id, file_path, access_token):
    """
    Full workflow: upload -> share -> send link to chat.
    """
    upload_res = upload_file_to_onedrive(file_path, access_token)
    file_id = upload_res.get("id")
    if not file_id:
        return {"error": "File upload failed", "details": upload_res}

    link_res = create_share_link(file_id, access_token)
    share_url = link_res.get("link", {}).get("webUrl")
    if not share_url:
        return {"error": "Link creation failed", "details": link_res}

    return send_file_link_to_chat(chat_id, share_url, os.path.basename(file_path), access_token)


def get_channel_drive_id(team_id, access_token):
    url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    res = requests.get(url, headers=headers).json()
    # Find channel info with SharePoint folder
    for channel in res.get("value", []):
        if "filesFolder" in channel:
            return channel["filesFolder"]["parentReference"]["driveId"]
    return None

#upload file (channel)
def upload_file_to_channel(team_id, channel_id, file_path, access_token):
    """
    Uploads a file to the default folder (Documents) in a Microsoft Teams channel.
    """
    drive_url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/filesFolder"
    headers = {"Authorization": f"Bearer {access_token}"}
    folder_res = requests.get(drive_url, headers=headers).json()
    folder_id = folder_res.get("id")

    if not folder_id:
        return {"error": "Could not find filesFolder for channel", "details": folder_res}

    file_name = os.path.basename(file_path)
    upload_url = f"https://graph.microsoft.com/v1.0/drives/{folder_res['parentReference']['driveId']}/items/{folder_id}:/children/{file_name}:/content"

    with open(file_path, "rb") as f:
        upload_res = requests.put(upload_url, headers=headers, data=f)

    try:
        return upload_res.json()
    except Exception as e:
        return {"error": "Upload failed", "details": str(e), "status": upload_res.status_code}
    
#add reaction (message)
def add_reaction_to_message(chat_id, message_id, reaction, access_token):
    """
    Adds a reaction (like, heart, laugh, etc.) to a message in a chat.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/chats/{chat_id}/messages/{message_id}/setReaction"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "reactionType": reaction  # e.g., "like", "heart", "laugh"
    }
    response = requests.post(url, headers=headers, json=data)

    try:
        return response.json() if response.content else {"status": "Reaction added"}
    except Exception as e:
        return {"error": "Failed to parse Graph response", "details": str(e), "status": response.status_code}
    
#remove reaction (message)
def remove_reaction_from_message(chat_id, message_id, reaction, access_token):
    """
    Removes a reaction from a message in a chat.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/chats/{chat_id}/messages/{message_id}/unsetReaction"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "reactionType": reaction
    }
    response = requests.post(url, headers=headers, json=data)

    try:
        return response.json() if response.content else {"status": "Reaction removed"}
    except Exception as e:
        return {
            "error": "Failed to parse Graph response",
            "details": str(e),
            "status": response.status_code
        }

#create task (planner)
def create_planner_task(access_token, plan_id, title, user_id=None, bucket_id=None):
    url = f"{Config.MS_GRAPH_API_BASE_URL}/planner/tasks"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    task_payload = {
        "planId": plan_id,
        "title": title,
    }

    if bucket_id:
        task_payload["bucketId"] = bucket_id

    if user_id:
        task_payload["assignments"] = {
            user_id: {
                "@odata.type": "#microsoft.graph.plannerAssignment",
                "orderHint": " !"
            }
        }

    response = requests.post(url, headers=headers, json=task_payload)

    try:
        return response.json()
    except Exception as e:
        return {
            "error": "Failed to parse response",
            "details": str(e),
            "status": response.status_code
        }

#list tasks (planner)
def list_tasks_in_plan(access_token, plan_id):
    url = f"{Config.MS_GRAPH_API_BASE_URL}/planner/plans/{plan_id}/tasks"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except Exception as e:
        return {"error": "Failed to parse response", "details": str(e), "status": response.status_code}


def list_user_tasks(access_token):
    url = f"{Config.MS_GRAPH_API_BASE_URL}/me/planner/tasks"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except Exception as e:
        return {"error": "Failed to parse response", "details": str(e), "status": response.status_code}

#update task (planner)
def update_planner_task(access_token, task_id, update_fields, etag):
    url = f"{Config.MS_GRAPH_API_BASE_URL}/planner/tasks/{task_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "If-Match": etag
    }

    response = requests.patch(url, headers=headers, json=update_fields)
    
    try:
        return response.json() if response.status_code == 200 else {
            "status": response.status_code,
            "error": response.text
        }
    except Exception as e:
        return {"error": "Failed to parse response", "details": str(e)}

#complete task (planner)
def complete_planner_task(access_token, task_id, etag):
    url = f"{Config.MS_GRAPH_API_BASE_URL}/planner/tasks/{task_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "If-Match": etag
    }
    data = {
        "percentComplete": 100
    }

    response = requests.patch(url, headers=headers, json=data)
    
    try:
        return response.json() if response.status_code in [200, 204] else {
            "status": response.status_code,
            "error": response.text
        }
    except Exception as e:
        return {"error": "Failed to parse response", "details": str(e)}

#list_user_meetings
def list_user_meetings(access_token, user_id="me"):
    url = f"{Config.MS_GRAPH_API_BASE_URL}/users/{user_id}/calendar/events" if user_id != "me" else f"{Config.MS_GRAPH_API_BASE_URL}/me/calendar/events"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    
    try:
        return response.json() if response.status_code == 200 else {
            "status": response.status_code,
            "error": response.text
        }
    except Exception as e:
        return {"error": "Failed to parse response", "details": str(e)}

#join meeting link
def get_meeting_join_url(access_token, meeting_id, user_id="me"):
    url = f"{Config.MS_GRAPH_API_BASE_URL}/me/events/{meeting_id}" if user_id == "me" \
        else f"{Config.MS_GRAPH_API_BASE_URL}/users/{user_id}/events/{meeting_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    try:
        data = response.json()
        return {
            "joinUrl": data.get("onlineMeeting", {}).get("joinUrl"),
            "subject": data.get("subject"),
            "start": data.get("start"),
            "end": data.get("end")
        }
    except Exception as e:
        return {
            "error": "Failed to parse response",
            "details": str(e),
            "raw": response.text,
            "status": response.status_code
        }

#list joined teams (light)
def list_user_joined_teams_light(access_token):
    """
    List minimal info (ID and name) of joined Teams.
    """
    url = f"{Config.MS_GRAPH_API_BASE_URL}/me/joinedTeams?$select=id,displayName"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except Exception as e:
        return {
            "error": "Failed to parse response",
            "details": str(e),
            "raw": response.text,
            "status": response.status_code
        }

#list apps (installed)
def list_installed_apps_in_team(access_token, team_id):
    url = f"{Config.MS_GRAPH_API_BASE_URL}/teams/{team_id}/installedApps?$expand=teamsApp"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    try:
        return response.json()
    except Exception as e:
        return {
            "error": "Failed to parse response",
            "details": str(e),
            "raw": response.text,
            "status": response.status_code
        }

#get team settings
def get_team_settings(access_token, team_id):
    url = f"{Config.MS_GRAPH_API_BASE_URL}/teams/{team_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except Exception as e:
        return {
            "error": "Failed to parse response",
            "details": str(e),
            "raw": response.text,
            "status": response.status_code
        }

