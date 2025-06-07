import requests
from flask import current_app
import base64
import urllib.parse


def get_current_user(access_token: str) -> dict:
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/users/@me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

#modify_current_user
def image_to_base64(path: str) -> str:
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"

def modify_bot_profile(username: str = None, avatar_path: str = None) -> dict:
    """
    Modify the current bot's Discord profile (username, avatar).
    """
    url = "https://discord.com/api/users/@me"
    bot_token = current_app.config["DISCORD_BOT_TOKEN"]

    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }

    payload = {}
    if username:
        payload["username"] = username
    if avatar_path:
        payload["avatar"] = image_to_base64(avatar_path)

    try:
        response = requests.patch(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e), "response": response.text if 'response' in locals() else None}

#get_user
def get_user_by_id(user_id: str, bot_token: str) -> dict:
    url = f"https://discord.com/api/users/{user_id}"
    headers = {
        "Authorization": f"Bot {bot_token}"
    }

    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    else:
        return {
            "error": response.status_code,
            "message": response.text
        }
    
#create_dm
def create_dm_channel(bot_token: str, user_id: str) -> dict:
    url = "https://discord.com/api/users/@me/channels"
    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "recipient_id": user_id
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        return response.json()
    else:
        return {"error": response.status_code, "details": response.text}

def send_dm_message(channel_id: str, content: str) -> dict:
    """
    Sends a message to a DM channel using the bot token.
    """
    url = f"https://discord.com/api/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}",
        "Content-Type": "application/json"
    }
    payload = {
        "content": content
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "details": response.text if 'response' in locals() else None
        }

#create_group_dm
def create_group_dm(initiator_token: str, access_tokens: list, nicks: dict) -> dict:

    url = "https://discord.com/api/users/@me/channels"
    headers = {
        "Authorization": f"Bearer {initiator_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "access_tokens": access_tokens,
        "nicks": nicks
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "details": response.text if 'response' in locals() else None
        }

#get_channel_by_id
def get_channel_by_id(channel_id: str) -> dict:
    """
    Fetches a Discord channel by its ID using the bot token.

    Args:
        channel_id (str): The ID of the channel to retrieve.

    Returns:
        dict: The channel object or an error message.
    """
    url = f"https://discord.com/api/channels/{channel_id}"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "details": response.text if 'response' in locals() else None
        }

#modify_channel
def modify_channel(channel_id: str, token: str, data: dict, reason: str = None) -> dict:
    url = f"https://discord.com/api/channels/{channel_id}"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    if reason:
        headers["X-Audit-Log-Reason"] = reason

    try:
        response = requests.patch(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#delete_channel
def delete_channel(channel_id: str) -> dict:
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/channels/{channel_id}"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}"
    }

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return {"status": "success", "message": f"Channel {channel_id} deleted"}
    except requests.RequestException as e:
        return {"error": str(e), "response": response.text if 'response' in locals() else "No response"}
    
#send_message_to_channel
def send_message_to_channel(channel_id: str, content: str) -> dict:
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}",
        "Content-Type": "application/json"
    }
    payload = {
        "content": content
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "details": response.text if 'response' in locals() else "No response"
        }
    
#get_channel_messages
def get_channel_messages(channel_id: str, bot_token: str, limit: int = 10):
    url = f"https://discord.com/api/channels/{channel_id}/messages?limit={limit}"
    headers = {
        "Authorization": f"Bot {bot_token}"
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        return response.json()
    else:
        return {
            "error": response.status_code,
            "details": response.text
        }

#get_channel_message
def get_channel_message(channel_id: str, message_id: str, bot_token: str) -> dict:
    url = f"https://discord.com/api/channels/{channel_id}/messages/{message_id}"
    headers = {
        "Authorization": f"Bot {bot_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e), "response": getattr(e.response, "text", None)}

#edit_channel_message
def edit_channel_message(channel_id: str, message_id: str, new_content: str, bot_token: str) -> dict:
    url = f"https://discord.com/api/channels/{channel_id}/messages/{message_id}"
    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "content": new_content
    }

    try:
        response = requests.patch(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e), "response": getattr(e.response, "text", None)}
    
#delete_channel_message
def delete_channel_message(channel_id: str, message_id: str, bot_token: str) -> dict:
    url = f"https://discord.com/api/channels/{channel_id}/messages/{message_id}"
    headers = {
        "Authorization": f"Bot {bot_token}"
    }

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return {"status": "success", "message": "Message deleted"}
    except requests.RequestException as e:
        return {"error": str(e), "response": getattr(e.response, "text", None)}
    
#bulk_delete_messages
def bulk_delete_messages(channel_id: str, message_ids: list, bot_token: str) -> dict:
    url = f"https://discord.com/api/channels/{channel_id}/messages/bulk-delete"
    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": message_ids
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {"status": "success", "deleted": message_ids}
    except requests.RequestException as e:
        return {"error": str(e), "response": getattr(e.response, "text", None)}
    
#add_reaction_to_message
def add_reaction_to_message(channel_id: str, message_id: str, emoji: str) -> dict:
    """
    Adds a reaction to a message in a specified channel.
    Emoji must be URL-encoded.
    """
    base_url = current_app.config['DISCORD_API_BASE_URL']
    encoded_emoji = urllib.parse.quote(emoji)

    url = f"{base_url}/channels/{channel_id}/messages/{message_id}/reactions/{encoded_emoji}/@me"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}"
    }

    response = requests.put(url, headers=headers)

    if response.status_code == 204:
        return {"success": True, "message": "Reaction added successfully"}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }
#delete_own_reaction
def delete_own_reaction(channel_id: str, message_id: str, emoji: str) -> dict:
    """
    Deletes the bot's own reaction from a specific message.
    """
    base_url = current_app.config['DISCORD_API_BASE_URL']
    encoded_emoji = urllib.parse.quote(emoji)

    url = f"{base_url}/channels/{channel_id}/messages/{message_id}/reactions/{encoded_emoji}/@me"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return {"success": True, "message": "Reaction removed successfully"}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

#delete_user_reaction 
def delete_user_reaction(channel_id: str, message_id: str, emoji: str, user_id: str) -> dict:
    """
    Deletes a reaction from a specific user on a specific message.
    Requires Manage Messages permission.
    """
    import urllib.parse
    import requests

    base_url = current_app.config['DISCORD_API_BASE_URL']
    encoded_emoji = urllib.parse.quote(emoji)

    url = f"{base_url}/channels/{channel_id}/messages/{message_id}/reactions/{encoded_emoji}/{user_id}"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return {"success": True, "message": "User reaction removed successfully"}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

#get_reactions
def get_reactions(channel_id: str, message_id: str, emoji: str) -> dict:
    """
    Retrieves a list of users who reacted with a specific emoji to a message.
    """
    import urllib.parse
    import requests

    base_url = current_app.config['DISCORD_API_BASE_URL']
    encoded_emoji = urllib.parse.quote(emoji)

    url = f"{base_url}/channels/{channel_id}/messages/{message_id}/reactions/{encoded_emoji}"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {"success": True, "users": response.json()}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

#create_guild
def create_guild(user_access_token: str, name: str) -> dict:
    import requests
    url = "https://discord.com/api/v10/guilds"

    headers = {
        "Authorization": f"Bearer {user_access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": name
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        return {"success": True, "guild": response.json()}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

#get_guild
def get_guild(guild_id: str) -> dict:
    """
    Fetches details about a Discord guild by its ID.
    The bot must be in the guild.
    """
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/guilds/{guild_id}"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {"success": True, "guild": response.json()}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }
    
#modify_guild
def modify_guild(guild_id: str, updates: dict) -> dict:
    """
    Modifies an existing guild's settings.
    Requires the bot to have 'MANAGE_GUILD' permission.
    """
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/guilds/{guild_id}"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}",
        "Content-Type": "application/json"
    }

    response = requests.patch(url, headers=headers, json=updates)

    if response.status_code == 200:
        return {"success": True, "updated_guild": response.json()}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }
    
#delete_guild is not supported
def delete_guild_template(guild_id: str, template_code: str) -> dict:
    """
    Deletes a specific guild template by code from a guild.
    Requires MANAGE_GUILD permission.
    """
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/guilds/{guild_id}/templates/{template_code}"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        return {"success": True, "deleted_template": response.json()}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

#get_guild_channels
def get_guild_channels(guild_id: str) -> dict:
    """
    Fetches the list of channels for a given guild.
    Bot must be a member of the guild.
    """
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/guilds/{guild_id}/channels"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {"success": True, "channels": response.json()}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

#create_guild_channel
def create_guild_channel(guild_id: str, channel_data: dict) -> dict:
    """
    Creates a new channel in the specified guild.
    The bot must have MANAGE_CHANNELS permission.
    """
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/guilds/{guild_id}/channels"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=channel_data)

    if response.status_code == 201:
        return {"success": True, "channel": response.json()}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

#get_guild_member
def get_guild_member(guild_id: str, user_id: str) -> dict:
    """
    Fetches a member's information from a guild.
    Requires GUILD_MEMBERS intent enabled in the bot.
    """
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/guilds/{guild_id}/members/{user_id}"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {"success": True, "member": response.json()}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

#list_guild_members(
def list_guild_members(guild_id: str, limit: int = 100, after: str = "0") -> dict:
    """
    Retrieves a list of members from a Discord guild (up to 1000).
    Requires the bot to have GUILD_MEMBERS intent enabled.
    """
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/guilds/{guild_id}/members"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}"
    }

    params = {
        "limit": limit,
        "after": after
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return {"success": True, "members": response.json()}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

#add_guild_member
def add_guild_member(guild_id: str, user_id: str, user_access_token: str, optional_fields: dict = {}) -> dict:
    """
    Adds a user to a guild using their OAuth2 access token.
    Requires bot authorization and the user's token with `guilds.join` scope.
    """
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/guilds/{guild_id}/members/{user_id}"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}",
        "Content-Type": "application/json"
    }

    data = {
        "access_token": user_access_token
    }
    data.update(optional_fields)  # e.g. {"nick": "UserName", "roles": [...]} if needed

    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [201, 204]:
        return {
            "success": True,
            "status": response.status_code,
            "message": "User added to guild" if response.status_code == 201 else "User already in guild"
        }
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

#modify_guild_member
def modify_guild_member(guild_id: str, user_id: str, updates: dict) -> dict:
    """
    Modify a member in the guild (nickname, roles, mute, deaf, timeout, etc).
    """
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/guilds/{guild_id}/members/{user_id}"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}",
        "Content-Type": "application/json"
    }

    response = requests.patch(url, headers=headers, json=updates)

    if response.status_code == 200:
        return {"success": True, "updated_member": response.json()}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

#remove_guild_member
def remove_guild_member(guild_id: str, user_id: str, reason: str = None) -> dict:
    """
    Kicks a user from the guild.
    Requires KICK_MEMBERS permission.
    """
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/guilds/{guild_id}/members/{user_id}"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}"
    }

    if reason:
        headers["X-Audit-Log-Reason"] = reason

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return {"success": True, "message": "Member removed from guild"}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

#create_guild_role
def create_guild_role(guild_id: str, role_data: dict, reason: str = None) -> dict:
    """
    Creates a new role in the specified guild.
    Requires MANAGE_ROLES permission.
    """
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/guilds/{guild_id}/roles"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}",
        "Content-Type": "application/json"
    }

    if reason:
        headers["X-Audit-Log-Reason"] = reason

    response = requests.post(url, headers=headers, json=role_data)

    if response.status_code == 200:
        return {"success": True, "role": response.json()}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

#modify_guild_role
def modify_guild_role(guild_id: str, role_id: str, role_data: dict, reason: str = None) -> dict:
    """
    Modifies an existing role in a guild.
    Requires MANAGE_ROLES permission.
    """
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/guilds/{guild_id}/roles/{role_id}"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}",
        "Content-Type": "application/json"
    }

    if reason:
        headers["X-Audit-Log-Reason"] = reason

    response = requests.patch(url, headers=headers, json=role_data)

    if response.status_code == 200:
        return {"success": True, "updated_role": response.json()}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

#delete_guild_role
def delete_guild_role(guild_id: str, role_id: str, reason: str = None) -> dict:
    """
    Deletes a role in a Discord guild.
    Requires MANAGE_ROLES permission.
    """
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/guilds/{guild_id}/roles/{role_id}"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}"
    }

    if reason:
        headers["X-Audit-Log-Reason"] = reason

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return {"success": True, "message": "Role deleted successfully"}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

#get_guild_roles
def get_guild_roles(guild_id: str) -> dict:
    """
    Retrieves all roles from a guild.
    """
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/guilds/{guild_id}/roles"
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {"success": True, "roles": response.json()}
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response.text
        }

#create_webhook
def create_webhook(channel_id: str, bot_token: str, name: str, avatar: str = None) -> dict:
    url = f"https://discord.com/api/v10/channels/{channel_id}/webhooks"
    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }
    data = {
        "name": name
    }
    if avatar:
        data["avatar"] = avatar  # base64-encoded image data, optional

    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json() if response.ok else {
            "error": response.status_code,
            "message": response.text
        }
    except requests.RequestException as e:
        return {"error": "Request failed", "message": str(e)}
    
#get_channel_webhooks
def get_channel_webhooks(channel_id: str, bot_token: str) -> dict:
    url = f"https://discord.com/api/v10/channels/{channel_id}/webhooks"
    headers = {
        "Authorization": f"Bot {bot_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        return response.json() if response.ok else {
            "error": response.status_code,
            "message": response.text
        }
    except requests.RequestException as e:
        return {"error": "Request failed", "message": str(e)}
    
#get_guild_webhooks
def get_guild_webhooks(guild_id: str, bot_token: str) -> dict:
    url = f"https://discord.com/api/v10/guilds/{guild_id}/webhooks"
    headers = {
        "Authorization": f"Bot {bot_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        return response.json() if response.ok else {
            "error": response.status_code,
            "message": response.text
        }
    except requests.RequestException as e:
        return {"error": "Request failed", "message": str(e)}
    
#modify_webhook
def modify_webhook(webhook_id: str, data: dict) -> dict:
    url = f"https://discord.com/api/v10/webhooks/{webhook_id}"
    
    headers = {
        "Authorization": f"Bot {current_app.config['DISCORD_BOT_TOKEN']}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.patch(url, json=data, headers=headers)
        return response.json() if response.ok else {
            "error": response.status_code,
            "message": response.text
        }
    except requests.RequestException as e:
        return {"error": 500, "message": str(e)}
    
#delete_webhook
def delete_webhook(webhook_id):
    token = current_app.config["DISCORD_BOT_TOKEN"]
    url = f"https://discord.com/api/v10/webhooks/{webhook_id}"

    headers = {
        "Authorization": f"Bot {token}"
    }

    response = requests.delete(url, headers=headers)
    return {
        "status_code": response.status_code,
        "success": response.status_code == 204,
        "message": "Deleted successfully" if response.status_code == 204 else response.text
    }

#execute_webhook
def execute_webhook(webhook_id, webhook_token, message_data):
    url = f"https://discord.com/api/v10/webhooks/{webhook_id}/{webhook_token}"

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=message_data)

    return {
        "status_code": response.status_code,
        "success": response.ok,
        "message": response.json() if response.ok else response.text
    }

#get_gateway
def get_gateway_url():
    url = "https://discord.com/api/v10/gateway"
    response = requests.get(url)
    
    return {
        "status_code": response.status_code,
        "success": response.ok,
        "data": response.json() if response.ok else response.text
    }