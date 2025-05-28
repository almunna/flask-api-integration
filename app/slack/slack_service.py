import requests
from app.config import Config
import time

#chat.postMessage
def send_message_to_slack(data):
    headers = {
        "Authorization": f"Bearer {Config.SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "channel": data.get("channel"),
        "text": data.get("text")
    }

    if "blocks" in data:
        payload["blocks"] = data["blocks"]
    if "attachments" in data:
        payload["attachments"] = data["attachments"]

    response = requests.post(Config.SLACK_POST_MESSAGE_URL, headers=headers, json=payload)
    return response.json()

#chat.update
def update_slack_message(data):
    url = "https://slack.com/api/chat.update"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "channel": data.get("channel"),
        "ts": data.get("ts"),
        "text": data.get("text")
    }

    if "blocks" in data:
        payload["blocks"] = data["blocks"]

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


#chat.delete
def delete_slack_message(data):
    url = "https://slack.com/api/chat.delete"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "channel": data.get("channel"),
        "ts": data.get("ts")
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#chat.scheduleMessage
def schedule_slack_message(data):
    url = "https://slack.com/api/chat.scheduleMessage"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Support scheduling with 'minutes' instead of raw post_at
    post_at = data.get("post_at")
    if not post_at and "minutes" in data:
        try:
            minutes = int(data["minutes"])
            post_at = int(time.time()) + (minutes * 60)
        except:
            return {"error": "'minutes' must be an integer"}

    payload = {
        "channel": data.get("channel"),
        "text": data.get("text"),
        "post_at": post_at
    }

    # Validate required fields
    if not payload["channel"] or not payload["text"] or not payload["post_at"]:
        return {"error": "Missing one of: 'channel', 'text', or valid 'post_at'"}

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#conversations.list
def list_slack_channels():
    url = "https://slack.com/api/conversations.list"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "limit": 1000,  # adjust if needed
        "types": "public_channel"  # or just "public_channel"
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()


#conversations.history
def get_channel_messages(channel_id, limit=20, cursor=None):
    url = "https://slack.com/api/conversations.history"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "channel": channel_id,
        "limit": limit
    }

    if cursor:
        params["cursor"] = cursor

    response = requests.get(url, headers=headers, params=params)
    return response.json()

#conversations.replies
def get_thread_replies(channel_id, parent_ts):
    url = "https://slack.com/api/conversations.replies"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "channel": channel_id,
        "ts": parent_ts
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

#conversations.join
def join_channel(channel_id):
    url = "https://slack.com/api/conversations.join"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "channel": channel_id
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#reminders.add
def create_reminder(text, time_str, user=None):
    url = "https://slack.com/api/reminders.add"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "time": time_str  # already a UNIX timestamp at this point
    }

    if user:
        payload["user"] = user

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#reminders.list
def list_reminders():
    url = "https://slack.com/api/reminders.list"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    print("RESPONSE FROM SLACK:", response.status_code, response.json())  # 🔍 log this
    return response.json()

#reminders.complete
def complete_reminder(reminder_id):
    url = "https://slack.com/api/reminders.complete"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "reminder": reminder_id
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#users
def list_all_users():
    url = "https://slack.com/api/users.list"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()

#user_info
def get_user_info(user_id):
    url = "https://slack.com/api/users.info"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "user": user_id
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

#user_profile_read
def get_user_profile(user_id=None):
    url = "https://slack.com/api/users.profile.get"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {}
    if user_id:
        params["user"] = user_id

    response = requests.get(url, headers=headers, params=params)
    return response.json()

#upload file
def upload_file_to_slack(file_path, channels, filename=None, title=None, initial_comment=None):
    url = "https://slack.com/api/files.upload"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = {
        "channels": channels
    }

    if filename:
        data["filename"] = filename
    if title:
        data["title"] = title
    if initial_comment:
        data["initial_comment"] = initial_comment

    with open(file_path, "rb") as file_content:
        files = {
            "file": file_content
        }
        response = requests.post(url, headers=headers, data=data, files=files)

    return response.json()

#file list
def list_files_from_slack(user=None, channel=None, types=None, ts_from=None, ts_to=None):
    url = "https://slack.com/api/files.list"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {}
    if user:
        params["user"] = user
    if channel:
        params["channel"] = channel
    if types:
        params["types"] = types
    if ts_from:
        params["ts_from"] = ts_from
    if ts_to:
        params["ts_to"] = ts_to

    response = requests.get(url, headers=headers, params=params)
    return response.json()

#emoji list
def list_custom_emojis():
    url = "https://slack.com/api/emoji.list"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()

#reaction add
def add_reaction_to_message(name, channel, timestamp):
    url = "https://slack.com/api/reactions.add"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": name,
        "channel": channel,
        "timestamp": timestamp
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#reaction remove
def remove_reaction_from_message(name, channel, timestamp):
    url = "https://slack.com/api/reactions.remove"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": name,
        "channel": channel,
        "timestamp": timestamp
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#get reactions
def get_reactions(channel, timestamp):
    url = "https://slack.com/api/reactions.get"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "channel": channel,
        "timestamp": timestamp
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

#leave channel
def leave_channel(channel_id):
    url = "https://slack.com/api/conversations.leave"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    data = {
        "channel": channel_id
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()

#channel members
def get_channel_members(channel_id):
    url = "https://slack.com/api/conversations.members"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "channel": channel_id
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

#conversations.info
def get_channel_info(channel_id):
    url = "https://slack.com/api/conversations.info"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "channel": channel_id
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

#users.getPresence
def get_user_presence(user_id):
    url = "https://slack.com/api/users.getPresence"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "user": user_id
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

#users.getPresence
def set_user_presence(presence):
    url = "https://slack.com/api/users.setPresence"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "presence": presence  # "auto" or "away"
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()

#users.profile.set
def update_user_profile(profile_data):
    url = "https://slack.com/api/users.profile.set"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "profile": profile_data
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#users.identity
def get_user_profile(user_id=None):
    url = "https://slack.com/api/users.profile.get"
    token = Config.SLACK_BOT_TOKEN  # Use your bot token

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {}
    if user_id:
        params["user"] = user_id

    response = requests.get(url, headers=headers, params=params)
    return response.json()

#get_team_info
def get_team_info():
    url = "https://slack.com/api/team.info"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()

#team.profile
def get_team_profile_fields():
    url = "https://slack.com/api/team.profile.get"
    token = Config.SLACK_BOT_TOKEN  # Requires bot token with `users.profile:read`

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    return response.json()

#users.conversations
def get_user_conversations(user_id=None, types="public_channel,private_channel", limit=100):
    url = "https://slack.com/api/users.conversations"
    token = Config.SLACK_BOT_TOKEN  # Or use SLACK_USER_TOKEN if required

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "types": types,
        "limit": limit
    }

    if user_id:
        params["user"] = user_id

    response = requests.get(url, headers=headers, params=params)
    return response.json()

#pins.add
def pin_message(channel, timestamp):
    url = "https://slack.com/api/pins.add"
    token = Config.SLACK_BOT_TOKEN  # Make sure it has `pins:write` scope

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "channel": channel,
        "timestamp": timestamp
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#pins.remove
def unpin_message(channel, timestamp):
    url = "https://slack.com/api/pins.remove"
    token = Config.SLACK_BOT_TOKEN  # Ensure you have `pins:write` scope

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "channel": channel,
        "timestamp": timestamp
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#pins list
def list_pinned_messages(channel):
    url = "https://slack.com/api/pins.list"
    token = Config.SLACK_BOT_TOKEN  # Make sure your token has `pins:read` scope

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "channel": channel
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

#add bookmark
def add_bookmark(channel_id, title, link):
    url = "https://slack.com/api/bookmarks.add"
    token = Config.SLACK_BOT_TOKEN  # Ensure you have 'bookmarks:write' scope

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "channel_id": channel_id,
        "title": title,
        "type": "link",        # required
        "link": link
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#bookmark list
def list_bookmarks(channel_id):
    url = "https://slack.com/api/bookmarks.list"
    token = Config.SLACK_BOT_TOKEN  # Must have `bookmarks:read` scope

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "channel_id": channel_id
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#bookmark remove
def remove_bookmark(bookmark_id, channel_id):
    url = "https://slack.com/api/bookmarks.remove"
    token = Config.SLACK_BOT_TOKEN  # Requires `bookmarks:write` scope

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "bookmark_id": bookmark_id,
        "channel_id": channel_id
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#conversations.list
def list_direct_messages():
    url = "https://slack.com/api/conversations.list"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "types": "im"
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

#im open
def open_dm(user_id):
    url = "https://slack.com/api/conversations.open"
    token = Config.SLACK_BOT_TOKEN

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "users": user_id
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#im history
def get_dm_conversation_history(channel_id, limit=100):
    url = "https://slack.com/api/conversations.history"
    headers = {
        "Authorization": f"Bearer {Config.SLACK_BOT_TOKEN}"
    }
    params = {
        "channel": channel_id,
        "limit": limit
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

#auth invoke
def revoke_slack_token(token=None):
    url = "https://slack.com/api/auth.revoke"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "token": token or Config.SLACK_BOT_TOKEN
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()