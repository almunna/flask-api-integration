from flask import Blueprint, request, jsonify
from app.facebook.facebook_service import get_user_profile, get_user_picture, get_user_friends, get_user_feed, get_user_likes, get_user_posts, create_post, get_post, delete_post, get_post_comments, add_comment, delete_comment, get_post_reactions, add_reaction, remove_reaction, get_user_photos, upload_photo, get_user_videos, upload_video, get_video_views, get_page_info, get_page_feed, get_page_insights, post_to_page, delete_page_post, get_event_info, get_user_events, create_event, update_event, delete_event, get_group_info, get_user_groups, get_group_feed, post_to_group, delete_group_post, get_user_notifications, get_ad_accounts, get_ad_campaigns, get_ad_insights, get_instagram_business_account, get_messenger_profile, send_messenger_message, get_messenger_conversations, get_messages_from_conversation, get_user_tags, get_user_checkins

facebook_bp = Blueprint("facebook", __name__)

@facebook_bp.route("/user-profile", methods=["GET"])
def user_profile():
    result = get_user_profile()
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_user_picture
@facebook_bp.route("/user-picture", methods=["GET"])
def user_picture():
    user_id = request.args.get("user_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not user_id:
        return jsonify({"error": "Missing required parameter: user_id"}), 400

    result = get_user_picture(user_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_user_friends
@facebook_bp.route("/user-friends", methods=["GET"])
def user_friends():
    user_id = request.args.get("user_id", "me")  # default to "me"
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_user_friends(user_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_user_feed
@facebook_bp.route("/user-feed", methods=["GET"])
def user_feed():
    user_id = request.args.get("user_id", "me")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_user_feed(user_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_user_likes
@facebook_bp.route("/user-likes", methods=["GET"])
def user_likes():
    user_id = request.args.get("user_id", "me")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_user_likes(user_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_user_posts
@facebook_bp.route("/user-posts", methods=["GET"])
def user_posts():
    user_id = request.args.get("user_id", "me")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_user_posts(user_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#create_post
@facebook_bp.route("/create-post", methods=["POST"])
def create_user_post():
    data = request.get_json()
    user_id = data.get("user_id", "me")
    message = data.get("message")
    access_token = data.get("access_token") or request.headers.get("Authorization")

    if not message:
        return jsonify({"error": "Missing required field: message"}), 400
    if not access_token:
        return jsonify({"error": "Missing required field: access_token"}), 400

    result = create_post(user_id, message, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_post
@facebook_bp.route("/get-post", methods=["GET"])
def retrieve_post():
    post_id = request.args.get("post_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not post_id:
        return jsonify({"error": "Missing required parameter: post_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_post(post_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#delete_post
@facebook_bp.route("/delete-post", methods=["DELETE"])
def remove_post():
    post_id = request.args.get("post_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not post_id:
        return jsonify({"error": "Missing required parameter: post_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = delete_post(post_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_post_comments
@facebook_bp.route("/post-comments", methods=["GET"])
def post_comments():
    post_id = request.args.get("post_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not post_id:
        return jsonify({"error": "Missing required parameter: post_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_post_comments(post_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#add_comment
@facebook_bp.route("/add-comment", methods=["POST"])
def comment_on_post():
    data = request.get_json()
    post_id = data.get("post_id")
    message = data.get("message")
    access_token = data.get("access_token") or request.headers.get("Authorization")

    if not post_id or not message:
        return jsonify({"error": "Missing required fields: post_id and message"}), 400
    if not access_token:
        return jsonify({"error": "Missing required field: access_token"}), 400

    result = add_comment(post_id, message, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#delete_comment
@facebook_bp.route("/delete-comment", methods=["DELETE"])
def remove_comment():
    comment_id = request.args.get("comment_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not comment_id:
        return jsonify({"error": "Missing required parameter: comment_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = delete_comment(comment_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_post_reactions
@facebook_bp.route("/post-reactions", methods=["GET"])
def post_reactions():
    post_id = request.args.get("post_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not post_id:
        return jsonify({"error": "Missing required parameter: post_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_post_reactions(post_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#add_reaction
@facebook_bp.route("/add-reaction", methods=["POST"])
def react_to_post():
    data = request.get_json()
    post_id = data.get("post_id")
    reaction_type = data.get("type")
    access_token = data.get("access_token") or request.headers.get("Authorization")

    if not post_id or not reaction_type:
        return jsonify({"error": "Missing required fields: post_id and type"}), 400
    if not access_token:
        return jsonify({"error": "Missing required field: access_token"}), 400

    result = add_reaction(post_id, reaction_type, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#remove_reaction
@facebook_bp.route("/remove-reaction", methods=["DELETE"])
def unreact_post():
    post_id = request.args.get("post_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not post_id:
        return jsonify({"error": "Missing required parameter: post_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = remove_reaction(post_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_user_photos
@facebook_bp.route("/user-photos", methods=["GET"])
def user_photos():
    user_id = request.args.get("user_id", "me")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_user_photos(user_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#upload_photo
@facebook_bp.route("/upload-photo", methods=["POST"])
def upload_user_photo():
    user_id = request.form.get("user_id", "me")
    access_token = request.form.get("access_token") or request.headers.get("Authorization")
    image_url = request.form.get("image_url")
    caption = request.form.get("caption")
    image_file = request.files.get("image_file")

    if not access_token:
        return jsonify({"error": "Missing required field: access_token"}), 400
    if not image_url and not image_file:
        return jsonify({"error": "Either image_url or image_file must be provided"}), 400

    result = upload_photo(user_id, access_token, image_url, image_file, caption)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_user_videos
@facebook_bp.route("/user-videos", methods=["GET"])
def user_videos():
    user_id = request.args.get("user_id", "me")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_user_videos(user_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#upload_video
@facebook_bp.route("/upload-video", methods=["POST"])
def upload_user_video():
    user_id = request.form.get("user_id", "me")
    access_token = request.form.get("access_token") or request.headers.get("Authorization")
    video_file = request.files.get("video_file")
    title = request.form.get("title")
    description = request.form.get("description")

    if not access_token:
        return jsonify({"error": "Missing access_token"}), 400
    if not video_file:
        return jsonify({"error": "Missing video_file"}), 400

    result = upload_video(user_id, access_token, video_file, description, title)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_video_views
@facebook_bp.route("/video-views", methods=["GET"])
def video_views():
    video_id = request.args.get("video_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not video_id:
        return jsonify({"error": "Missing required parameter: video_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_video_views(video_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_page_info
@facebook_bp.route("/page-info", methods=["GET"])
def page_info():
    page_id = request.args.get("page_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not page_id:
        return jsonify({"error": "Missing required parameter: page_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_page_info(page_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_page_feed
@facebook_bp.route("/page-feed", methods=["GET"])
def page_feed():
    page_id = request.args.get("page_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not page_id:
        return jsonify({"error": "Missing required parameter: page_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_page_feed(page_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_page_insights
@facebook_bp.route("/page-insights", methods=["GET"])
def page_insights():
    page_id = request.args.get("page_id")
    metric = request.args.get("metric")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not page_id or not metric:
        return jsonify({"error": "Missing required parameters: page_id and metric"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_page_insights(page_id, metric, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#post_to_page
@facebook_bp.route("/post-to-page", methods=["POST"])
def publish_to_page():
    data = request.get_json()
    page_id = data.get("page_id")
    message = data.get("message")
    access_token = data.get("access_token") or request.headers.get("Authorization")

    if not page_id or not message:
        return jsonify({"error": "Missing required fields: page_id and message"}), 400
    if not access_token:
        return jsonify({"error": "Missing required field: access_token"}), 400

    result = post_to_page(page_id, message, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#delete_page_post
@facebook_bp.route("/delete-page-post", methods=["DELETE"])
def remove_page_post():
    post_id = request.args.get("post_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not post_id:
        return jsonify({"error": "Missing required parameter: post_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = delete_page_post(post_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_event_info
@facebook_bp.route("/event-info", methods=["GET"])
def event_info():
    event_id = request.args.get("event_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not event_id:
        return jsonify({"error": "Missing required parameter: event_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_event_info(event_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_user_events
@facebook_bp.route("/user-events", methods=["GET"])
def user_events():
    user_id = request.args.get("user_id", "me")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_user_events(user_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#create_event
@facebook_bp.route("/create-event", methods=["POST"])
def create_page_event():
    data = request.get_json()
    page_id = data.get("page_id")
    access_token = data.get("access_token") or request.headers.get("Authorization")
    event_data = data.get("event_data")

    if not page_id or not access_token or not event_data:
        return jsonify({"error": "Missing required fields: page_id, event_data, or access_token"}), 400

    result = create_event(page_id, event_data, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#update_event
@facebook_bp.route("/update-event", methods=["POST"])
def update_page_event():
    data = request.get_json()
    event_id = data.get("event_id")
    updates = data.get("updates")
    access_token = data.get("access_token") or request.headers.get("Authorization")

    if not event_id or not updates:
        return jsonify({"error": "Missing required fields: event_id or updates"}), 400
    if not access_token:
        return jsonify({"error": "Missing required field: access_token"}), 400

    result = update_event(event_id, updates, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#delete_event
@facebook_bp.route("/delete-event", methods=["DELETE"])
def delete_facebook_event():
    event_id = request.args.get("event_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not event_id:
        return jsonify({"error": "Missing required parameter: event_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = delete_event(event_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_group_info
@facebook_bp.route("/group-info", methods=["GET"])
def group_info():
    group_id = request.args.get("group_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not group_id:
        return jsonify({"error": "Missing required parameter: group_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_group_info(group_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_user_groups
@facebook_bp.route("/user-groups", methods=["GET"])
def user_groups():
    user_id = request.args.get("user_id", "me")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_user_groups(user_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_group_feed
@facebook_bp.route("/group-feed", methods=["GET"])
def group_feed():
    group_id = request.args.get("group_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not group_id:
        return jsonify({"error": "Missing required parameter: group_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_group_feed(group_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#post_to_group
@facebook_bp.route("/post-to-group", methods=["POST"])
def create_group_post():
    data = request.get_json()
    group_id = data.get("group_id")
    message = data.get("message")
    access_token = data.get("access_token") or request.headers.get("Authorization")

    if not group_id or not message:
        return jsonify({"error": "Missing required parameters: group_id or message"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = post_to_group(group_id, message, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#delete_group_post
@facebook_bp.route("/delete-group-post", methods=["DELETE"])
def delete_group_post_route():
    post_id = request.args.get("post_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not post_id:
        return jsonify({"error": "Missing required parameter: post_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = delete_group_post(post_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_user_notifications
@facebook_bp.route("/user-notifications", methods=["GET"])
def user_notifications():
    user_id = request.args.get("user_id", "me")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_user_notifications(user_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_ad_accounts
@facebook_bp.route("/ad-accounts", methods=["GET"])
def ad_accounts():
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_ad_accounts(access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_ad_campaigns
@facebook_bp.route("/ad-campaigns", methods=["GET"])
def ad_campaigns():
    ad_account_id = request.args.get("ad_account_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not ad_account_id:
        return jsonify({"error": "Missing required parameter: ad_account_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_ad_campaigns(ad_account_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_ad_insights
@facebook_bp.route("/ad-insights", methods=["GET"])
def ad_insights():
    ad_account_id = request.args.get("ad_account_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not ad_account_id:
        return jsonify({"error": "Missing required parameter: ad_account_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_ad_insights(ad_account_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_instagram_business_account
@facebook_bp.route("/instagram-business-account", methods=["GET"])
def instagram_business_account():
    page_id = request.args.get("page_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not page_id:
        return jsonify({"error": "Missing required parameter: page_id"}), 400
    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_instagram_business_account(page_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_messenger_profile
@facebook_bp.route("/messenger-profile", methods=["GET"])
def messenger_profile():
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not access_token:
        return jsonify({"error": "Missing required parameter: access_token"}), 400

    result = get_messenger_profile(access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#send_messenger_message
@facebook_bp.route("/send-message", methods=["POST"])
def send_message():
    data = request.get_json()
    recipient_id = data.get("recipient_id")
    message = data.get("message")
    access_token = data.get("access_token") or request.headers.get("Authorization")

    if not recipient_id or not message or not access_token:
        return jsonify({"error": "Missing one or more required parameters: recipient_id, message, access_token"}), 400

    result = send_messenger_message(recipient_id, message, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_messenger_messages
@facebook_bp.route("/messenger-conversations", methods=["GET"])
def messenger_conversations():
    page_id = request.args.get("page_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not page_id or not access_token:
        return jsonify({"error": "Missing required parameters: page_id or access_token"}), 400

    result = get_messenger_conversations(page_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)


@facebook_bp.route("/messenger-messages", methods=["GET"])
def messenger_messages():
    conversation_id = request.args.get("conversation_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not conversation_id or not access_token:
        return jsonify({"error": "Missing required parameters: conversation_id or access_token"}), 400

    result = get_messages_from_conversation(conversation_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_user_tags
@facebook_bp.route("/user-tags", methods=["GET"])
def user_tags():
    user_id = request.args.get("user_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not user_id or not access_token:
        return jsonify({"error": "Missing required parameters: user_id or access_token"}), 400

    result = get_user_tags(user_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

#get_user_checkins
@facebook_bp.route("/user-checkins", methods=["GET"])
def user_checkins():
    user_id = request.args.get("user_id")
    access_token = request.args.get("access_token") or request.headers.get("Authorization")

    if not user_id or not access_token:
        return jsonify({"error": "Missing required parameters: user_id or access_token"}), 400

    result = get_user_checkins(user_id, access_token)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)