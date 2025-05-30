from flask import Blueprint, request, jsonify
import os
from app.teams.teams_service import (
    list_joined_teams,
    list_user_joined_teams,
    get_team_details,
    list_team_channels,
    get_channel_details,
    list_user_chats,
    get_chat_details,
    list_chat_messages,
    send_message_to_channel,
    list_channel_messages,
    reply_to_chat_message,
    reply_to_channel_message,
    list_team_members,
    list_chat_members,
    get_user_by_id,
    get_logged_in_user,
    get_user_presence,
    create_chat_thread,
    create_channel_in_team,
    schedule_teams_meeting,
    get_meeting_details,
    list_calendar_events,
    create_calendar_event,
    update_calendar_event,
    delete_calendar_event,
    list_team_files,
    list_files_in_chat,
    upload_file_to_chat,
    upload_file_to_channel,
    add_reaction_to_message,
    remove_reaction_from_message,
    create_planner_task,
    list_tasks_in_plan,
    list_user_tasks,
    update_planner_task,
    complete_planner_task,
    list_user_meetings,
    get_meeting_join_url,
    list_user_joined_teams_light,
    list_installed_apps_in_team,
    get_team_settings

)

teams_bp = Blueprint("teams", __name__)


@teams_bp.route("/joined", methods=["GET"])
def get_joined_teams():
    """
    List all teams (app-only, uses groups with Team provisioning).
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    result = list_joined_teams(token if token else None)
    return jsonify(result)


#list joinedTeams
@teams_bp.route("/user-joined", methods=["GET"])
def get_user_joined_teams():
    """
    List teams joined by the authenticated user (user token required).
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing user access token"}), 401

    result = list_user_joined_teams(token)
    return jsonify(result)

#get team
@teams_bp.route("/details/<team_id>", methods=["GET"])
def get_team_info(team_id):
    """
    Get details of a specific team by team_id (user or app token required).
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = get_team_details(team_id, token)
    return jsonify(result)

#channel list
@teams_bp.route("/channels/<team_id>", methods=["GET"])
def get_team_channels(team_id):
    """
    Get a list of all channels in the specified team.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = list_team_channels(team_id, token)
    return jsonify(result)

#get channel
@teams_bp.route("/channel/<team_id>/<channel_id>", methods=["GET"])
def get_channel_info(team_id, channel_id):
    """
    Get details of a specific channel in a team.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = get_channel_details(team_id, channel_id, token)
    return jsonify(result)

#list charts
@teams_bp.route("/user/chats", methods=["GET"])
def get_user_chats():
    """
    List all chat threads for the authenticated user.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing user access token"}), 401

    result = list_user_chats(token)
    return jsonify(result)

#get chats
@teams_bp.route("/user/chat/<chat_id>", methods=["GET"])
def get_chat_info(chat_id):
    """
    Get details of a specific chat thread.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing user access token"}), 401

    result = get_chat_details(chat_id, token)
    return jsonify(result)

#message list
@teams_bp.route("/user/chat/<chat_id>/messages", methods=["GET"])
def get_chat_messages(chat_id):
    """
    Get all messages from a specific chat.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing user access token"}), 401

    result = list_chat_messages(chat_id, token)
    return jsonify(result)

#send_message
@teams_bp.route("/user/team/<team_id>/channel/<channel_id>/send", methods=["POST"])
def post_message_to_channel(team_id, channel_id):
    """
    Send a message to a specific channel in a team.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing user access token"}), 401

    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"error": "Missing message content"}), 400

    result = send_message_to_channel(team_id, channel_id, message, token)
    return jsonify(result)

#list messages (channel)
@teams_bp.route("/user/team/<team_id>/channel/<channel_id>/messages", methods=["GET"])
def get_channel_messages(team_id, channel_id):
    """
    Retrieve all messages in a specific channel.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing user access token"}), 401

    result = list_channel_messages(team_id, channel_id, token)
    return jsonify(result)

#replay to message (chat)
@teams_bp.route("/user/chat/<chat_id>/message/<message_id>/reply", methods=["POST"])
def reply_to_message(chat_id, message_id):
    """
    Reply to a specific message in a chat.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing user access token"}), 401

    data = request.get_json()
    reply_text = data.get("reply")
    if not reply_text:
        return jsonify({"error": "Missing reply content"}), 400

    result = reply_to_chat_message(chat_id, message_id, reply_text, token)
    return jsonify(result)

#reply_to_channel_message
@teams_bp.route("/user/team/<team_id>/channel/<channel_id>/message/<message_id>/reply", methods=["POST"])
def reply_to_channel(team_id, channel_id, message_id):
    """
    Reply to a message in a Teams channel.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing user access token"}), 401

    data = request.get_json()
    reply_text = data.get("reply")
    if not reply_text:
        return jsonify({"error": "Missing reply content"}), 400

    result = reply_to_channel_message(team_id, channel_id, message_id, reply_text, token)
    return jsonify(result)

#list members (team)
@teams_bp.route("/user/team/<team_id>/members", methods=["GET"])
def get_team_members(team_id):
    """
    List members of the given team.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = list_team_members(team_id, token)
    return jsonify(result)

#list members (chat)
@teams_bp.route("/user/chat/<chat_id>/members", methods=["GET"])
def get_chat_members(chat_id):
    """
    Get members of a specific chat.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing user access token"}), 401

    result = list_chat_members(chat_id, token)
    return jsonify(result)

#get user
@teams_bp.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    """
    Retrieve user details by user ID.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = get_user_by_id(user_id, token)
    return jsonify(result)

#get me
@teams_bp.route("/me", methods=["GET"])
def get_me():
    """
    Get current user's Microsoft profile.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing user access token"}), 401

    result = get_logged_in_user(token)
    return jsonify(result)

#get presence
@teams_bp.route("/user/<user_id>/presence", methods=["GET"])
def get_presence(user_id):
    """
    Get presence status of a user by ID.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = get_user_presence(user_id, token)
    return jsonify(result)

#create chat
@teams_bp.route("/user/chats", methods=["POST"])
def create_chat():
    """
    Create a new chat thread.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    user_ids = request.json.get("user_ids")
    if not user_ids or not isinstance(user_ids, list):
        return jsonify({"error": "user_ids must be a list of user IDs"}), 400

    result = create_chat_thread(user_ids, token)
    return jsonify(result)

#create channel
@teams_bp.route("/team/<team_id>/channels", methods=["POST"])
def create_channel(team_id):
    """
    Create a channel in a specific team.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    channel_data = request.json
    if not channel_data or "displayName" not in channel_data:
        return jsonify({"error": "Channel data must include at least 'displayName'"}), 400

    result = create_channel_in_team(team_id, channel_data, token)
    return jsonify(result)

#schedule meeting
@teams_bp.route("/meetings/schedule", methods=["POST"])
def create_meeting():
    """
    Schedule a Microsoft Teams meeting.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    meeting_data = request.json
    required_fields = ["startDateTime", "endDateTime", "subject"]
    if not all(field in meeting_data for field in required_fields):
        return jsonify({"error": "Missing required fields: startDateTime, endDateTime, subject"}), 400

    result = schedule_teams_meeting(meeting_data, token)
    return jsonify(result)

#get meeting
@teams_bp.route("/meetings/<meeting_id>", methods=["GET"])
def get_meeting(meeting_id):
    """
    Get details of a scheduled Microsoft Teams meeting.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = get_meeting_details(meeting_id, token)
    return jsonify(result)

#list calendar events
@teams_bp.route("/calendar", methods=["GET"])
def get_my_calendar():
    """
    Get events from the authenticated user's calendar.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = list_calendar_events(token)
    return jsonify(result)


@teams_bp.route("/calendar/<user_id>", methods=["GET"])
def get_user_calendar(user_id):
    """
    Get events from a specific user's calendar (requires app access and permissions).
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = list_calendar_events(token, user_id=user_id)
    return jsonify(result)

#add event
@teams_bp.route("/calendar", methods=["POST"])
def add_my_event():
    """
    Add a calendar event with Teams link for the authenticated user.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    event_data = request.json
    result = create_calendar_event(event_data, token)
    return jsonify(result)

#update event
@teams_bp.route("/calendar/<event_id>", methods=["PATCH"])
def patch_calendar_event(event_id):
    """
    Update an event using event ID.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    update_data = request.json
    result = update_calendar_event(event_id, update_data, token)
    return jsonify(result)

#delete event
@teams_bp.route("/calendar/<event_id>", methods=["DELETE"])
def remove_calendar_event(event_id):
    """
    Delete an event by its ID.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = delete_calendar_event(event_id, token)
    return jsonify(result)

#list files (team)
@teams_bp.route("/files/<team_id>", methods=["GET"])
def get_team_files(team_id):
    """
    Lists files in a team.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = list_team_files(team_id, token)
    return jsonify(result)

#list files (chat)
@teams_bp.route("/chats/<chat_id>/files", methods=["GET"])
def get_chat_files(chat_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = list_files_in_chat(chat_id, token)
    return jsonify(result)

#upload file (chat)
@teams_bp.route("/chats/<chat_id>/upload", methods=["POST"])
def upload_file(chat_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Temporarily save the file
    temp_path = f"/tmp/{file.filename}"
    file.save(temp_path)

    # Call service
    result = upload_file_to_chat(chat_id, temp_path, token)

    # Clean up
    os.remove(temp_path)

    return jsonify(result)

#upload file (channel)
@teams_bp.route("/teams/<team_id>/channels/<channel_id>/upload", methods=["POST"])
def upload_file_to_channel_route(team_id, channel_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Save temporarily
    file_path = f"/tmp/{file.filename}"
    file.save(file_path)

    result = upload_file_to_channel(team_id, channel_id, file_path, token)

    os.remove(file_path)
    return jsonify(result)

#add reaction (message)
@teams_bp.route("/chats/<chat_id>/messages/<message_id>/reaction", methods=["POST"])
def react_to_message(chat_id, message_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    body = request.get_json()
    reaction = body.get("reactionType")

    if not reaction:
        return jsonify({"error": "Missing reaction type"}), 400

    result = add_reaction_to_message(chat_id, message_id, reaction, token)
    return jsonify(result)

#remove reaction (message)
@teams_bp.route("/chats/<chat_id>/messages/<message_id>/reaction/remove", methods=["POST"])
def remove_reaction(chat_id, message_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    body = request.get_json()
    reaction = body.get("reactionType")

    if not reaction:
        return jsonify({"error": "Missing reaction type"}), 400

    result = remove_reaction_from_message(chat_id, message_id, reaction, token)
    return jsonify(result)

#create task (planner)
@teams_bp.route("/planner/tasks", methods=["POST"])
def create_task():
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    data = request.json
    plan_id = data.get("planId")
    title = data.get("title")
    user_id = data.get("userId")     # optional
    bucket_id = data.get("bucketId") # optional

    if not plan_id or not title:
        return jsonify({"error": "Missing required fields: planId, title"}), 400

    result = create_planner_task(token, plan_id, title, user_id, bucket_id)
    return jsonify(result)

#list tasks (planner)
@teams_bp.route("/planner/tasks/plan/<plan_id>", methods=["GET"])
def get_plan_tasks(plan_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = list_tasks_in_plan(token, plan_id)
    return jsonify(result)


@teams_bp.route("/planner/tasks/me", methods=["GET"])
def get_my_tasks():
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = list_user_tasks(token)
    return jsonify(result)

#update task (planner)
@teams_bp.route("/planner/tasks/<task_id>", methods=["PATCH"])
def update_task(task_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    data = request.json or {}
    etag = request.headers.get("If-Match")
    if not etag:
        return jsonify({"error": "Missing If-Match header (etag is required)"}), 400

    result = update_planner_task(token, task_id, data, etag)
    return jsonify(result)

#complete task (planner)
@teams_bp.route("/planner/tasks/<task_id>/complete", methods=["PATCH"])
def complete_task(task_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    etag = request.headers.get("If-Match")

    if not token:
        return jsonify({"error": "Missing access token"}), 401
    if not etag:
        return jsonify({"error": "Missing If-Match header (etag is required)"}), 400

    result = complete_planner_task(token, task_id, etag)
    return jsonify(result)

#list_user_meetings
@teams_bp.route("/meetings", methods=["GET"])
def list_meetings():
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    user_id = request.args.get("user_id", "me")

    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = list_user_meetings(token, user_id)
    return jsonify(result)

#join meeting link
@teams_bp.route("/meetings/<meeting_id>/join-url", methods=["GET"])
def get_join_url(meeting_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    user_id = request.args.get("user_id", "me")

    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = get_meeting_join_url(token, meeting_id, user_id)
    return jsonify(result)

#list joined teams (light)
@teams_bp.route("/joined-light", methods=["GET"])
def get_joined_teams_light():
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = list_user_joined_teams_light(token)
    return jsonify(result)

#list apps (installed)
@teams_bp.route("/teams/<team_id>/apps", methods=["GET"])
def get_installed_apps(team_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = list_installed_apps_in_team(token, team_id)
    return jsonify(result)

##get team settings
@teams_bp.route("/teams/<team_id>/settings", methods=["GET"])
def get_team_config_settings(team_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    result = get_team_settings(token, team_id)
    return jsonify(result)

