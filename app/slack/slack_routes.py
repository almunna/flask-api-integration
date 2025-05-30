from flask import Blueprint, request, jsonify
from time import time
from app.slack.slack_service import schedule_slack_message
from datetime import datetime, timedelta
import os
import tempfile
import re
from app.slack.slack_service import send_message_to_slack, update_slack_message, delete_slack_message, schedule_slack_message,list_slack_channels, get_thread_replies, join_channel, create_reminder, list_reminders, complete_reminder,list_all_users, get_user_info, get_user_profile, upload_file_to_slack, list_files_from_slack, list_custom_emojis, add_reaction_to_message, remove_reaction_from_message, get_reactions, leave_channel, get_channel_members, get_channel_info, get_user_presence, set_user_presence, update_user_profile, get_team_info, get_team_profile_fields, get_user_conversations, pin_message, unpin_message, list_pinned_messages, add_bookmark, list_bookmarks, remove_bookmark, list_direct_messages, open_dm, get_dm_conversation_history, revoke_slack_token



slack_bp = Blueprint('slack', __name__)

#chat.postMessage
@slack_bp.route('/send-message', methods=['POST'])
def post_message():
    try:
        data = request.json

        # Basic validation
        if not data or "channel" not in data or "text" not in data:
            return jsonify({"error": "Missing required fields: 'channel' and 'text'"}), 400

        result = send_message_to_slack(data)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#chat.update
@slack_bp.route('/update-message', methods=['POST'])
def update_message():
    try:
        data = request.json

        # Validate input
        if not data or "channel" not in data or "ts" not in data or "text" not in data:
            return jsonify({"error": "Required fields: 'channel', 'ts', and 'text'"}), 400

        result = update_slack_message(data)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#chat.delete 
@slack_bp.route('/delete-message', methods=['POST'])
def delete_message():
    try:
        data = request.json

        if not data or "channel" not in data or "ts" not in data:
            return jsonify({"error": "Required fields: 'channel' and 'ts'"}), 400

        result = delete_slack_message(data)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#chat.scheduleMessage   
@slack_bp.route('/schedule-message', methods=['POST'])
def schedule_message():
    data = request.json

    if not data or "channel" not in data or "text" not in data:
        return jsonify({"error": "Required fields: 'channel' and 'text'"}), 400

    # Support scheduling by 'minutes'
    if "minutes" in data:
        try:
            delay_seconds = int(data["minutes"]) * 60
            data["post_at"] = int(time()) + delay_seconds
        except:
            return jsonify({"error": "'minutes' must be an integer"}), 400

    # Still allow manual post_at if provided
    if "post_at" not in data:
        return jsonify({"error": "Must provide either 'post_at' or 'minutes'"}), 400

    result = schedule_slack_message(data)
    return jsonify(result)

#conversations.list
@slack_bp.route('/list-channels', methods=['GET'])
def list_channels():
    try:
        result = list_slack_channels()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

from app.slack.slack_service import get_channel_messages

#conversations.history
@slack_bp.route('/channel-messages', methods=['GET'])
def fetch_channel_messages():
    channel_id = request.args.get("channel")
    limit = request.args.get("limit", 20)
    cursor = request.args.get("cursor")

    if not channel_id:
        return jsonify({"error": "Missing 'channel' query parameter"}), 400

    try:
        result = get_channel_messages(channel_id, int(limit), cursor)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#conversations.replies
@slack_bp.route('/thread-replies', methods=['GET'])
def fetch_thread_replies():
    channel_id = request.args.get("channel")
    parent_ts = request.args.get("ts")

    if not channel_id or not parent_ts:
        return jsonify({"error": "Missing 'channel' or 'ts' query parameters"}), 400

    try:
        result = get_thread_replies(channel_id, parent_ts)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#conversations.join
@slack_bp.route('/join-channel', methods=['POST'])
def join_slack_channel():
    data = request.json
    channel_id = data.get("channel")

    if not channel_id:
        return jsonify({"error": "Missing required field: 'channel'"}), 400

    try:
        result = join_channel(channel_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


#reminders.add
@slack_bp.route('/create-reminder', methods=['POST'])
def add_reminder():
    data = request.json
    text = data.get("text")
    time_str = data.get("time")  # format: "HH:MM"
    user = data.get("user")      # optional

    if not text or not time_str:
        return jsonify({"error": "Required fields: 'text' and 'time' (format: HH:MM)"}), 400

    try:
        # Parse input time (BDT assumed)
        input_time = datetime.strptime(time_str, "%H:%M").time()
        now = datetime.now()
        reminder_datetime = datetime.combine(now.date(), input_time)

        # If time has already passed today, set it for tomorrow
        if reminder_datetime < now:
            reminder_datetime += timedelta(days=1)

        unix_timestamp = int(reminder_datetime.timestamp())
    except ValueError:
        return jsonify({"error": "Invalid time format. Use HH:MM (24-hour format)."}), 400

    result = create_reminder(text, unix_timestamp, user)
    return jsonify(result)

#reminders.list
@slack_bp.route('/list-reminders', methods=['GET'])
def get_reminders():
    try:
        result = list_reminders()
        if not result.get("ok"):
            return jsonify({"error": result.get("error", "Unknown error")}), 400
        return jsonify(result.get("reminders", []))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#reminders.complete
@slack_bp.route('/complete-reminder', methods=['POST'])
def complete_a_reminder():
    data = request.json
    reminder_id = data.get("reminder")

    # Validate input
    if not reminder_id or not isinstance(reminder_id, str):
        return jsonify({"error": "Only 'reminder' (ID) is required in the request body"}), 400

    # Call Slack API
    result = complete_reminder(reminder_id)

    # Return error if Slack fails
    if not result.get("ok"):
        return jsonify({
            "error": result.get("error", "Unknown error from Slack")
        }), 400

    return jsonify({"ok": True, "message": "Reminder completed"})

#users
@slack_bp.route('/list-users', methods=['GET'])
def get_all_users():
    result = list_all_users()

    if not result.get("ok"):
        return jsonify({"error": result.get("error", "Unknown error")}), 400

    # Optional: extract only basic info
    users = [
        {
            "id": u.get("id"),
            "real_name": u.get("real_name"),
            "email": u.get("profile", {}).get("email"),
            "avatar": u.get("profile", {}).get("image_192")
        }
        for u in result.get("members", [])
        if not u.get("deleted", False)
    ]

    return jsonify(users)

#user_info
@slack_bp.route('/user-info/<user_id>', methods=['GET'])
def user_info(user_id):
    result = get_user_info(user_id)

    if not result.get("ok"):
        return jsonify({"error": result.get("error", "Unknown error")}), 400

    user = result.get("user", {})
    profile = user.get("profile", {})

    return jsonify({
        "id": user.get("id"),
        "name": user.get("name"),
        "real_name": user.get("real_name"),
        "email": profile.get("email"),
        "title": profile.get("title"),
        "avatar": profile.get("image_192")
    })

#user profile read
@slack_bp.route('/user-profile', methods=['GET'])
def get_own_profile():
    result = get_user_profile()

    if not result.get("ok"):
        return jsonify({"error": result.get("error", "Unknown error")}), 400

    return jsonify(result.get("profile", {}))


@slack_bp.route('/user-profile/<user_id>', methods=['GET'])
def get_profile_by_id(user_id):
    result = get_user_profile(user_id)

    if not result.get("ok"):
        return jsonify({"error": result.get("error", "Unknown error")}), 400

    return jsonify(result.get("profile", {}))

#upload file
@slack_bp.route('/upload-file', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    channels = request.form.get('channels')
    filename = request.form.get('filename') or file.filename  # fallback
    title = request.form.get('title')
    comment = request.form.get('initial_comment')

    if not file or not channels:
        return jsonify({"error": "Missing 'file' or 'channels'"}), 400

    import tempfile, os
    from werkzeug.utils import secure_filename

    # Ensure filename is safe
    safe_name = secure_filename(file.filename)
    temp_dir = tempfile.gettempdir()
    safe_path = os.path.join(temp_dir, safe_name)
    file.save(safe_path)

    try:
        result = upload_file_to_slack(safe_path, channels, filename, title, comment)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Always clean up
        if os.path.exists(safe_path):
            os.remove(safe_path)

    return jsonify(result)

#file list
@slack_bp.route('/list-files', methods=['GET'])
def list_files():
    user = request.args.get('user')
    channel = request.args.get('channel')
    types = request.args.get('types')
    ts_from = request.args.get('ts_from')
    ts_to = request.args.get('ts_to')

    result = list_files_from_slack(user, channel, types, ts_from, ts_to)
    return jsonify(result)

#emoji list
@slack_bp.route('/list-emojis', methods=['GET'])
def get_emojis():
    result = list_custom_emojis()
    return jsonify(result)

#reaction add
@slack_bp.route('/add-reaction', methods=['POST'])
def add_reaction():
    data = request.json
    name = data.get("name")
    channel = data.get("channel")
    timestamp = data.get("timestamp")

    if not name or not channel or not timestamp:
        return jsonify({"error": "Required fields: 'name', 'channel', and 'timestamp'"}), 400

    result = add_reaction_to_message(name, channel, timestamp)
    return jsonify(result)

#reaction remove
@slack_bp.route('/remove-reaction', methods=['POST'])
def remove_reaction():
    data = request.json
    name = data.get("name")
    channel = data.get("channel")
    timestamp = data.get("timestamp")

    if not name or not channel or not timestamp:
        return jsonify({"error": "Required fields: 'name', 'channel', and 'timestamp'"}), 400

    result = remove_reaction_from_message(name, channel, timestamp)
    return jsonify(result)

#get reactions
@slack_bp.route('/get-reactions', methods=['GET'])
def fetch_reactions():
    channel = request.args.get("channel")
    timestamp = request.args.get("timestamp")

    if not channel or not timestamp:
        return jsonify({"error": "Required query params: 'channel' and 'timestamp'"}), 400

    result = get_reactions(channel, timestamp)
    return jsonify(result)

#leave channel
@slack_bp.route('/leave-channel', methods=['POST'])
def leave_channel_route():
    data = request.json
    channel_id = data.get("channel")

    if not channel_id:
        return jsonify({"error": "Field 'channel' is required"}), 400

    result = leave_channel(channel_id)
    return jsonify(result)

#channel members
@slack_bp.route('/channel-members', methods=['GET'])
def channel_members():
    channel_id = request.args.get("channel")

    if not channel_id:
        return jsonify({"error": "Query parameter 'channel' is required"}), 400

    result = get_channel_members(channel_id)
    return jsonify(result)

#conversations.info
@slack_bp.route('/channel-info', methods=['GET'])
def channel_info():
    channel_id = request.args.get("channel")

    if not channel_id:
        return jsonify({"error": "Query parameter 'channel' is required"}), 400

    result = get_channel_info(channel_id)
    return jsonify(result)

#users.getPresence
@slack_bp.route('/user-presence', methods=['GET'])
def user_presence():
    user_id = request.args.get("user")

    if not user_id:
        return jsonify({"error": "Query parameter 'user' is required"}), 400

    result = get_user_presence(user_id)
    return jsonify(result)

#users.getPresence
@slack_bp.route('/set-presence', methods=['POST'])
def set_presence():
    data = request.json
    presence = data.get("presence")

    if presence not in ["auto", "away"]:
        return jsonify({"error": "Invalid value. 'presence' must be 'auto' or 'away'"}), 400

    result = set_user_presence(presence)
    return jsonify(result)

#users.profile.set
@slack_bp.route('/update-profile', methods=['POST'])
def update_profile():
    data = request.json
    profile = data.get("profile")

    if not profile:
        return jsonify({"error": "Missing 'profile' object in request body"}), 400

    result = update_user_profile(profile)
    return jsonify(result)

#users.identity
@slack_bp.route('/user-profile', methods=['GET'])
def user_profile():
    user_id = request.args.get('user')  # Optional
    result = get_user_profile(user_id)
    return jsonify(result)

#get_team_info
@slack_bp.route('/team-info', methods=['GET'])
def team_info():
    result = get_team_info()
    return jsonify(result)

#team.profile
@slack_bp.route('/team-profile-fields', methods=['GET'])
def team_profile_fields():
    result = get_team_profile_fields()
    return jsonify(result)

#users.conversations
@slack_bp.route('/user-conversations', methods=['GET'])
def user_conversations():
    user_id = request.args.get("user")  # Optional query param
    result = get_user_conversations(user_id)
    return jsonify(result)

#pins.add
@slack_bp.route('/pin-message', methods=['POST'])
def pin_slack_message():
    data = request.json
    channel = data.get("channel")
    timestamp = data.get("timestamp")

    if not channel or not timestamp:
        return jsonify({"error": "Required fields: 'channel' and 'timestamp'"}), 400

    result = pin_message(channel, timestamp)
    return jsonify(result)

#pins.add
@slack_bp.route('/unpin-message', methods=['POST'])
def unpin_slack_message():
    data = request.json
    channel = data.get("channel")
    timestamp = data.get("timestamp")

    if not channel or not timestamp:
        return jsonify({"error": "Required fields: 'channel' and 'timestamp'"}), 400

    result = unpin_message(channel, timestamp)
    return jsonify(result)

#pins list
@slack_bp.route('/list-pinned', methods=['GET'])
def list_pins():
    channel = request.args.get("channel")
    
    if not channel:
        return jsonify({"error": "Query param 'channel' is required"}), 400

    result = list_pinned_messages(channel)
    return jsonify(result)

#add bookmark
@slack_bp.route('/add-bookmark', methods=['POST'])
def add_bookmark_route():
    data = request.json
    channel_id = data.get("channel_id") or data.get("channel")  # allow both keys
    title = data.get("title")
    link = data.get("link")

    if not channel_id or not title or not link:
        return jsonify({"error": "Required fields: 'channel_id' (or 'channel'), 'title', and 'link'"}), 400

    result = add_bookmark(channel_id, title, link)
    return jsonify(result)

#bookmark list
@slack_bp.route('/list-bookmarks', methods=['POST'])
def list_bookmarks_route():
    data = request.json
    channel_id = data.get("channel_id") or data.get("channel")

    if not channel_id:
        return jsonify({"error": "Missing required field: 'channel_id'"}), 400

    result = list_bookmarks(channel_id)
    return jsonify(result)

#bookmark remove
@slack_bp.route('/remove-bookmark', methods=['POST'])
def remove_bookmark_route():
    data = request.json
    bookmark_id = data.get("bookmark_id")
    channel_id = data.get("channel_id")

    if not bookmark_id or not channel_id:
        return jsonify({"error": "Missing 'bookmark_id' or 'channel_id'"}), 400

    result = remove_bookmark(bookmark_id, channel_id)
    return jsonify(result)

#conversations.list
@slack_bp.route('/list-dms', methods=['GET'])
def list_dms():
    result = list_direct_messages()
    return jsonify(result)

#im open
@slack_bp.route('/open-dm', methods=['POST'])
def open_dm_route():
    data = request.json
    user_id = data.get("user")

    if not user_id:
        return jsonify({"error": "Missing 'user' field"}), 400

    result = open_dm(user_id)
    return jsonify(result)

#im history
@slack_bp.route('/dm-history', methods=['GET'])
def dm_history():
    channel_id = request.args.get('channel_id')
    if not channel_id:
        return jsonify({"error": "channel_id is required"}), 400

    result = get_dm_conversation_history(channel_id)
    return jsonify(result)

#auth revoke
@slack_bp.route('/revoke-token', methods=['POST'])
def revoke_token():
    token = request.json.get("token")
    result = revoke_slack_token(token)
    return jsonify(result)