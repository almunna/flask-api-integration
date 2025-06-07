from flask import Blueprint, redirect, request, session, jsonify, current_app, url_for
import requests
from app.discord.discord_service import get_current_user, get_user_by_id, modify_bot_profile, create_dm_channel, send_dm_message, create_group_dm, get_channel_by_id, modify_channel, delete_channel, send_message_to_channel, get_channel_messages, get_channel_message, edit_channel_message, delete_channel_message, bulk_delete_messages, add_reaction_to_message, delete_own_reaction, delete_user_reaction, get_reactions, create_guild, get_guild, modify_guild, delete_guild_template,get_guild_channels, create_guild_channel,get_guild_member, list_guild_members, add_guild_member, modify_guild_member, remove_guild_member, create_guild_role, modify_guild_role, delete_guild_role, get_guild_roles, create_webhook, get_channel_webhooks, get_guild_webhooks, modify_webhook, delete_webhook, execute_webhook, get_gateway_url

discord_bp = Blueprint("discord_bp", __name__)

@discord_bp.route("/login")
def discord_login():
    params = {
        "client_id": current_app.config["DISCORD_CLIENT_ID"],
        "redirect_uri": current_app.config["DISCORD_REDIRECT_URI"],
        "response_type": "code",
        "scope": "identify guilds"
    }
    url = f"{current_app.config['DISCORD_API_BASE_URL']}/oauth2/authorize"
    return redirect(f"{url}?client_id={params['client_id']}&redirect_uri={params['redirect_uri']}&response_type=code&scope={params['scope']}")

@discord_bp.route("/callback")
def discord_callback():
    code = request.args.get("code")
    data = {
        "client_id": current_app.config["DISCORD_CLIENT_ID"],
        "client_secret": current_app.config["DISCORD_CLIENT_SECRET"],
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": current_app.config["DISCORD_REDIRECT_URI"]
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(
        f"{current_app.config['DISCORD_API_BASE_URL']}/oauth2/token",
        data=data,
        headers=headers
    )
    token_data = response.json()

    # ✅ TEMPORARY: Print the token in the console
    print("Access Token from Discord:", token_data.get("access_token"))

    session["discord_token"] = token_data.get("access_token")
    return redirect(url_for("discord_bp.discord_me"))


@discord_bp.route("/me", methods=["GET"])
def discord_me():
    # First check session, then fallback to header or query (for Postman etc.)
    token = (
        session.get("discord_token") or
        request.args.get("token") or
        request.headers.get("Authorization")
    )

    if not token:
        return jsonify({"error": "Missing token"}), 401

    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")

    user = get_current_user(token)
    return jsonify(user)

#modify_current_user
@discord_bp.route("/bot/update-profile", methods=["POST"])
def update_bot_profile():
    username = request.form.get("username")
    avatar_path = request.form.get("avatar_path")  # Local path to image (server-side)

    if not username and not avatar_path:
        return jsonify({"error": "Please provide at least one of username or avatar_path"}), 400

    result = modify_bot_profile(username=username, avatar_path=avatar_path)
    return jsonify(result)

#get_user
@discord_bp.route("/bot/user/<user_id>", methods=["GET"])
def get_user(user_id):
    token = current_app.config["DISCORD_BOT_TOKEN"]
    user = get_user_by_id(user_id, token)
    return jsonify(user)

#create_dm
@discord_bp.route("/bot/dm/<user_id>", methods=["POST"])
def send_dm(user_id):
    bot_token = current_app.config["DISCORD_BOT_TOKEN"]
    dm_channel = create_dm_channel(bot_token, user_id)

    if "id" in dm_channel:
        return jsonify({"dm_channel_id": dm_channel["id"]})
    else:
        return jsonify(dm_channel), 400

@discord_bp.route("/bot/send-dm", methods=["POST"])
def send_dm1():
    data = request.json
    channel_id = data.get("channel_id")
    content = data.get("content")

    if not channel_id or not content:
        return jsonify({"error": "channel_id and content are required"}), 400

    result = send_dm_message(channel_id, content)
    return jsonify(result)

#create_group_dm
@discord_bp.route("/group-dm", methods=["POST"])
def create_group_dm_route():
    data = request.json

    initiator_token = data.get("initiator_token")
    access_tokens = data.get("access_tokens")
    nicks = data.get("nicks")

    if not initiator_token or not access_tokens or not nicks:
        return jsonify({"error": "Missing required fields: initiator_token, access_tokens, nicks"}), 400

    result = create_group_dm(initiator_token, access_tokens, nicks)
    return jsonify(result)

#get_channel_by_id
@discord_bp.route("/bot/channel/<channel_id>", methods=["GET"])
def get_channel(channel_id):
    channel = get_channel_by_id(channel_id)
    return jsonify(channel)

#modify_channel
@discord_bp.route("/modify-channel/<channel_id>", methods=["PATCH"])
def modify_channel_route(channel_id):
    token = current_app.config["DISCORD_BOT_TOKEN"]
    body = request.json  # Expected keys like name, topic, nsfw, etc.
    reason = request.headers.get("X-Audit-Log-Reason")

    result = modify_channel(channel_id, token, body, reason)
    return jsonify(result)

#delete_channel
@discord_bp.route("/delete-channel/<channel_id>", methods=["DELETE"])
def route_delete_channel(channel_id):
    result = delete_channel(channel_id)
    return jsonify(result)

#send_message_to_channel
@discord_bp.route("/send-message/<channel_id>", methods=["POST"])
def route_send_message(channel_id):
    data = request.get_json()
    content = data.get("content", "")
    if not content:
        return jsonify({"error": "Message content is required"}), 400

    result = send_message_to_channel(channel_id, content)
    return jsonify(result)

#get_channel_messages
@discord_bp.route("/get-channel-messages/<channel_id>", methods=["GET"])
def get_messages(channel_id):
    limit = request.args.get("limit", default=10, type=int)
    bot_token = current_app.config.get("DISCORD_BOT_TOKEN")

    if not bot_token:
        return jsonify({"error": "Bot token not configured"}), 500

    messages = get_channel_messages(channel_id, bot_token, limit)
    return jsonify(messages)

#get_channel_message
@discord_bp.route("/get-channel-message/<channel_id>/<message_id>", methods=["GET"])
def route_get_channel_message(channel_id, message_id):
    bot_token = current_app.config.get("DISCORD_BOT_TOKEN")
    if not bot_token:
        return jsonify({"error": "Missing bot token"}), 401

    result = get_channel_message(channel_id, message_id, bot_token)
    return jsonify(result)

#edit_channel_message
@discord_bp.route("/edit-message/<channel_id>/<message_id>", methods=["PATCH"])
def route_edit_channel_message(channel_id, message_id):
    bot_token = current_app.config.get("DISCORD_BOT_TOKEN")
    if not bot_token:
        return jsonify({"error": "Missing bot token"}), 401

    data = request.get_json()
    if not data or "content" not in data:
        return jsonify({"error": "Missing new content"}), 400

    result = edit_channel_message(channel_id, message_id, data["content"], bot_token)
    return jsonify(result)

#delete_channel_message
@discord_bp.route("/delete-message/<channel_id>/<message_id>", methods=["DELETE"])
def route_delete_channel_message(channel_id, message_id):
    bot_token = current_app.config.get("DISCORD_BOT_TOKEN")
    if not bot_token:
        return jsonify({"error": "Missing bot token"}), 401

    result = delete_channel_message(channel_id, message_id, bot_token)
    return jsonify(result)

#bulk_delete_messages
@discord_bp.route("/bulk-delete-messages/<channel_id>", methods=["POST"])
def route_bulk_delete_messages(channel_id):
    data = request.get_json()
    message_ids = data.get("message_ids")
    bot_token = current_app.config.get("DISCORD_BOT_TOKEN")

    if not bot_token:
        return jsonify({"error": "Missing bot token"}), 401
    if not message_ids or not isinstance(message_ids, list):
        return jsonify({"error": "message_ids must be a list of message IDs"}), 400

    result = bulk_delete_messages(channel_id, message_ids, bot_token)
    return jsonify(result)

#add_reaction_to_message
@discord_bp.route("/react", methods=["POST"])
def react_to_message():
    data = request.json
    channel_id = data.get("channel_id")
    message_id = data.get("message_id")
    emoji = data.get("emoji")  # Can be unicode or custom (e.g., "🔥" or "custom_emoji:emoji_id")

    if not all([channel_id, message_id, emoji]):
        return {"error": "channel_id, message_id, and emoji are required"}, 400

    result = add_reaction_to_message(channel_id, message_id, emoji)
    return result, (200 if result["success"] else result.get("status_code", 500))

#delete_own_reaction
@discord_bp.route("/react/remove", methods=["POST"])
def remove_own_reaction():
    data = request.json
    channel_id = data.get("channel_id")
    message_id = data.get("message_id")
    emoji = data.get("emoji")

    if not all([channel_id, message_id, emoji]):
        return {"error": "channel_id, message_id, and emoji are required"}, 400

    result = delete_own_reaction(channel_id, message_id, emoji)
    return result, (200 if result["success"] else result.get("status_code", 500))

#delete_user_reaction
@discord_bp.route("/react/remove-user", methods=["POST"])
def remove_user_reaction():
    data = request.json
    channel_id = data.get("channel_id")
    message_id = data.get("message_id")
    emoji = data.get("emoji")
    user_id = data.get("user_id")

    if not all([channel_id, message_id, emoji, user_id]):
        return {"error": "channel_id, message_id, emoji, and user_id are required"}, 400

    result = delete_user_reaction(channel_id, message_id, emoji, user_id)
    return result, (200 if result["success"] else result.get("status_code", 500))

#get_reactions
@discord_bp.route("/react/users", methods=["POST"])
def get_users_reacted():
    data = request.json
    channel_id = data.get("channel_id")
    message_id = data.get("message_id")
    emoji = data.get("emoji")

    if not all([channel_id, message_id, emoji]):
        return {"error": "channel_id, message_id, and emoji are required"}, 400

    result = get_reactions(channel_id, message_id, emoji)
    return result, (200 if result["success"] else result.get("status_code", 500))

#create_guild
@discord_bp.route("/guilds/create", methods=["POST"])
def create_user_guild():
    data = request.json
    token = data.get("access_token")  # OAuth2 token from user login
    name = data.get("name")

    if not token or not name:
        return {"error": "access_token and name are required"}, 400

    result = create_guild(token, name)
    return result, (200 if result["success"] else result.get("status_code", 500))

#get_guild
@discord_bp.route("/guilds/info", methods=["POST"])
def fetch_guild_info():
    data = request.json
    guild_id = data.get("guild_id")

    if not guild_id:
        return {"error": "guild_id is required"}, 400

    result = get_guild(guild_id)
    return result, (200 if result["success"] else result.get("status_code", 500))

#modify_guild
@discord_bp.route("/guilds/modify", methods=["POST"])
def update_guild():
    data = request.json
    guild_id = data.get("guild_id")
    updates = data.get("updates")

    if not guild_id or not updates:
        return {"error": "guild_id and updates are required"}, 400

    result = modify_guild(guild_id, updates)
    return result, (200 if result["success"] else result.get("status_code", 500))

#delete_guild
@discord_bp.route("/guilds/templates/delete", methods=["POST"])
def delete_template():
    data = request.json
    guild_id = data.get("guild_id")
    template_code = data.get("template_code")

    if not guild_id or not template_code:
        return {"error": "guild_id and template_code are required"}, 400

    result = delete_guild_template(guild_id, template_code)
    return result, (200 if result["success"] else result.get("status_code", 500))

#get_guild_channels
@discord_bp.route("/guilds/channels", methods=["POST"])
def fetch_guild_channels():
    data = request.json
    guild_id = data.get("guild_id")

    if not guild_id:
        return {"error": "guild_id is required"}, 400

    result = get_guild_channels(guild_id)
    return result, (200 if result["success"] else result.get("status_code", 500))

#create_guild_channel
@discord_bp.route("/guilds/channels/create", methods=["POST"])
def create_channel():
    data = request.json
    guild_id = data.get("guild_id")
    channel_data = data.get("channel")

    if not guild_id or not channel_data:
        return {"error": "guild_id and channel data are required"}, 400

    result = create_guild_channel(guild_id, channel_data)
    return result, (201 if result["success"] else result.get("status_code", 500))

#get_guild_member
@discord_bp.route("/guilds/member", methods=["POST"])
def fetch_guild_member():
    data = request.json
    guild_id = data.get("guild_id")
    user_id = data.get("user_id")

    if not guild_id or not user_id:
        return {"error": "guild_id and user_id are required"}, 400

    result = get_guild_member(guild_id, user_id)
    return result, (200 if result["success"] else result.get("status_code", 500))

#list_guild_members
@discord_bp.route("/guilds/<guild_id>/members", methods=["GET"])
def get_guild_members(guild_id):
    limit = request.args.get("limit", default=100, type=int)
    after = request.args.get("after", default="0")

    result = list_guild_members(guild_id, limit, after)
    return result, (200 if result["success"] else result.get("status_code", 500))

#add_guild_member
@discord_bp.route("/guilds/members/add", methods=["PUT"])
def add_user_to_guild():
    data = request.json
    guild_id = data.get("guild_id")
    user_id = data.get("user_id")
    access_token = data.get("access_token")
    optional_fields = data.get("options", {})

    if not guild_id or not user_id or not access_token:
        return {"error": "guild_id, user_id, and access_token are required"}, 400

    result = add_guild_member(guild_id, user_id, access_token, optional_fields)
    return result, (201 if result["success"] else result.get("status_code", 500))

#modify_guild_member
@discord_bp.route("/guilds/members/modify", methods=["PATCH"])
def update_guild_member():
    data = request.json
    guild_id = data.get("guild_id")
    user_id = data.get("user_id")
    updates = data.get("updates", {})

    if not guild_id or not user_id:
        return {"error": "guild_id and user_id are required"}, 400

    result = modify_guild_member(guild_id, user_id, updates)
    return result, (200 if result["success"] else result.get("status_code", 500))

#remove_guild_member
@discord_bp.route("/guilds/members/remove", methods=["DELETE"])
def remove_member():
    data = request.json
    guild_id = data.get("guild_id")
    user_id = data.get("user_id")
    reason = data.get("reason", None)

    if not guild_id or not user_id:
        return {"error": "guild_id and user_id are required"}, 400

    result = remove_guild_member(guild_id, user_id, reason)
    return result, (200 if result["success"] else result.get("status_code", 500))

#create_guild_role
@discord_bp.route("/guilds/<guild_id>/roles/create", methods=["POST"])
def create_role(guild_id):
    data = request.json or {}
    reason = request.headers.get("X-Audit-Log-Reason")

    result = create_guild_role(guild_id, role_data=data, reason=reason)
    return result, (200 if result["success"] else result.get("status_code", 500))

#modify_guild_role
@discord_bp.route("/guilds/<guild_id>/roles/<role_id>/modify", methods=["PATCH"])
def update_guild_role(guild_id, role_id):
    data = request.json or {}
    reason = request.headers.get("X-Audit-Log-Reason")

    result = modify_guild_role(guild_id, role_id, role_data=data, reason=reason)
    return result, (200 if result["success"] else result.get("status_code", 500))

#delete_guild_role
@discord_bp.route("/guilds/<guild_id>/roles/<role_id>/delete", methods=["DELETE"])
def remove_guild_role(guild_id, role_id):
    reason = request.headers.get("X-Audit-Log-Reason")
    result = delete_guild_role(guild_id, role_id, reason)
    return result, (200 if result["success"] else result.get("status_code", 500))

#get_guild_roles
@discord_bp.route("/guilds/<guild_id>/roles", methods=["GET"])
def fetch_guild_roles(guild_id):
    result = get_guild_roles(guild_id)
    return result, (200 if result["success"] else result.get("status_code", 500))

#create_webhook
@discord_bp.route("/webhooks/create", methods=["POST"])
def create_discord_webhook():
    data = request.json
    channel_id = data.get("channel_id")
    name = data.get("name")
    avatar = data.get("avatar")  # optional

    if not channel_id or not name:
        return jsonify({"error": "Missing channel_id or name"}), 400

    bot_token = current_app.config.get("DISCORD_BOT_TOKEN")
    if not bot_token:
        return jsonify({"error": "Missing DISCORD_BOT_TOKEN in config"}), 500

    result = create_webhook(channel_id, bot_token, name, avatar)
    return jsonify(result)

#get_channel_webhooks
@discord_bp.route("/webhooks/channel/<channel_id>", methods=["GET"])
def get_discord_channel_webhooks(channel_id):
    bot_token = current_app.config.get("DISCORD_BOT_TOKEN")
    if not bot_token:
        return jsonify({"error": "Missing DISCORD_BOT_TOKEN in config"}), 500

    result = get_channel_webhooks(channel_id, bot_token)
    return jsonify(result)

#get_guild_webhooks
@discord_bp.route("/webhooks/guild/<guild_id>", methods=["GET"])
def get_discord_guild_webhooks(guild_id):
    bot_token = current_app.config.get("DISCORD_BOT_TOKEN")
    if not bot_token:
        return jsonify({"error": "Missing DISCORD_BOT_TOKEN in config"}), 500

    result = get_guild_webhooks(guild_id, bot_token)
    return jsonify(result)

#modify_webhook
@discord_bp.route('/webhooks/<webhook_id>', methods=['PATCH'])
def route_modify_webhook(webhook_id):
    data = request.json
    result = modify_webhook(webhook_id, data)
    return jsonify(result)

#delete_webhook
@discord_bp.route("/webhooks/<webhook_id>", methods=["DELETE"])
def delete_discord_webhook(webhook_id):
    result = delete_webhook(webhook_id)
    return jsonify(result), result["status_code"]

#execute_webhook
@discord_bp.route("/webhooks/<webhook_id>/<webhook_token>/execute", methods=["POST"])
def execute_discord_webhook(webhook_id, webhook_token):
    message_data = request.json
    result = execute_webhook(webhook_id, webhook_token, message_data)
    return jsonify(result), result["status_code"]

#get_gateway
@discord_bp.route("/gateway", methods=["GET"])
def get_discord_gateway():
    result = get_gateway_url()
    return jsonify(result), result["status_code"]