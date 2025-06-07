from flask import Blueprint, request, jsonify
from app.instagram.instagram_service import get_user_profile, get_user_media, get_user_insights, get_media_insights, publish_photo, publish_video, publish_carousel, get_comments, reply_to_comment, delete_comment, hide_comment, disable_comments, enable_comments, search_hashtag, get_hashtag_media, get_top_hashtag_media, get_mentioned_media, get_business_discovery, get_user_stories, get_story_insights, get_tagged_media, get_user_albums, get_album_media, get_media_likes, get_media_comments_count, get_user_followers_count, get_user_follow_stats, get_user_tags, get_user_mentions, get_user_reels, get_reel_insights, get_user_igtv, get_igtv_insights, get_user_live_video_candidates, get_live_video_insights, schedule_post, cancel_scheduled_post, get_analytics_summary, get_daily_engagement, get_profile_views

instagram_bp = Blueprint("instagram", __name__)

@instagram_bp.route("/profile", methods=["GET"])
def user_profile():
    return jsonify(get_user_profile())

@instagram_bp.route("/media", methods=["GET"])
def user_media():
    return jsonify(get_user_media(limit=10))

#get_user_insights
@instagram_bp.route("/insights", methods=["GET"])
def user_insights():
    return jsonify(get_user_insights())

#get_media_insights
@instagram_bp.route("/media/<media_id>/insights", methods=["GET"])
def media_insights(media_id):
    return jsonify(get_media_insights(media_id))

#publish_photo
instagram_bp = Blueprint("instagram", __name__)

@instagram_bp.route("/publish-photo", methods=["POST"])
def publish_photo_route():
    data = request.json
    image_url = data.get("image_url")
    caption = data.get("caption", "")
    if not image_url:
        return jsonify({"error": "Missing required field: image_url"}), 400
    return jsonify(publish_photo(image_url=image_url, caption=caption))

#publish_video
@instagram_bp.route("/publish-video", methods=["POST"])
def publish_video_route():
    data = request.json
    video_url = data.get("video_url")
    caption = data.get("caption", "")
    thumb_offset = data.get("thumb_offset", 0)

    if not video_url:
        return jsonify({"error": "Missing required field: video_url"}), 400

    return jsonify(publish_video(video_url=video_url, caption=caption, thumb_offset=thumb_offset))

#publish_carousel
@instagram_bp.route("/publish-carousel", methods=["POST"])
def publish_carousel_route():
    data = request.json
    media_urls = data.get("media_urls", [])
    caption = data.get("caption", "")

    if not media_urls or not isinstance(media_urls, list):
        return jsonify({"error": "Field 'media_urls' must be a non-empty list"}), 400

    return jsonify(publish_carousel(media_urls=media_urls, caption=caption))

#get_comments
@instagram_bp.route("/media/<media_id>/comments", methods=["GET"])
def get_comments_route(media_id):
    return jsonify(get_comments(media_id))

#reply_to_comment
@instagram_bp.route("/comments/<comment_id>/reply", methods=["POST"])
def reply_to_comment_route(comment_id):
    data = request.json
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Missing required field: message"}), 400
    return jsonify(reply_to_comment(comment_id, message))

#delete_comment
@instagram_bp.route("/comments/<comment_id>", methods=["DELETE"])
def delete_comment_route(comment_id):
    return jsonify(delete_comment(comment_id))

#hide_comment
@instagram_bp.route("/comments/<comment_id>/hide", methods=["POST"])
def hide_comment_route(comment_id):
    data = request.json or {}
    hide = data.get("hide", True)  # default: hide = true
    return jsonify(hide_comment(comment_id, hide=hide))

#unhide_comment
@instagram_bp.route("/comments/<comment_id>/unhide", methods=["POST"])
def unhide_comment_route(comment_id):
    return jsonify(hide_comment(comment_id, hide=False))

#disable_comments
@instagram_bp.route("/media/<media_id>/disable-comments", methods=["POST"])
def disable_comments_route(media_id):  
    return jsonify(disable_comments(media_id))

#enable_comments
@instagram_bp.route("/media/<media_id>/enable-comments", methods=["POST"])
def enable_comments_route(media_id):
    return jsonify(enable_comments(media_id))

#search_hashtag
@instagram_bp.route("/hashtags/search", methods=["GET"])
def search_hashtag_route():
    hashtag = request.args.get("q")
    if not hashtag:
        return jsonify({"error": "Missing required query param: q"}), 400

    return jsonify(search_hashtag(hashtag))

#get_hashtag_media
@instagram_bp.route("/hashtags/<hashtag_id>/media", methods=["GET"])
def get_hashtag_media_route(hashtag_id):
    media_type = request.args.get("type", "recent")
    return jsonify(get_hashtag_media(hashtag_id, media_type))

#get_top_hashtag_media
@instagram_bp.route("/hashtags/<hashtag_id>/top-media", methods=["GET"])
def get_top_hashtag_media_route(hashtag_id):
    return jsonify(get_top_hashtag_media(hashtag_id))

#get_mentioned_media
@instagram_bp.route("/mentioned-media", methods=["GET"])
def mentioned_media_route():
    return jsonify(get_mentioned_media())

#get_business_discovery
@instagram_bp.route("/business-discovery", methods=["GET"])
def business_discovery_route():

    username = request.args.get("username")

    if not username:
        return jsonify({"error": "Missing required query param: username"}), 400

    return jsonify(get_business_discovery(username))

#get_user_stories
@instagram_bp.route("/stories", methods=["GET"])
def get_user_stories_route():
    return jsonify(get_user_stories())

#get_story_insights
@instagram_bp.route("/stories/<story_id>/insights", methods=["GET"])
def get_story_insights_route(story_id):
    return jsonify(get_story_insights(story_id))

#get_tagged_media
@instagram_bp.route("/tagged-media", methods=["GET"])
def get_tagged_media_route():
    return jsonify(get_tagged_media())

#get_user_albums
@instagram_bp.route("/albums", methods=["GET"])
def get_user_albums_route():
    return jsonify(get_user_albums())

#get_album_media
@instagram_bp.route("/albums/<album_id>/media", methods=["GET"])
def get_album_media_route(album_id):
    return jsonify(get_album_media(album_id))

#get_media_likes
@instagram_bp.route("/media/<media_id>/likes", methods=["GET"])
def get_media_likes_route(media_id):
    return jsonify(get_media_likes(media_id))

#get_media_comments_count
@instagram_bp.route("/media/<media_id>/comments-count", methods=["GET"])
def get_media_comments_count_route(media_id):
    return jsonify(get_media_comments_count(media_id))

#get_user_followers
#Instagram Graph API does not support retrieving a full list of followers
@instagram_bp.route("/followers-count", methods=["GET"])
def get_followers_count_route():
    return jsonify(get_user_followers_count())


#The Instagram Graph API does not support
#get_user_follow_stats
@instagram_bp.route("/follow-stats", methods=["GET"])
def user_follow_stats_route():
    return jsonify(get_user_follow_stats())

#get_user_tags
@instagram_bp.route("/tags", methods=["GET"])
def user_tagged_posts_route():
    return jsonify(get_user_tags(limit=10))

#get_user_mentions
@instagram_bp.route("/mentions", methods=["GET"])
def user_mentions_route():
    return jsonify(get_user_mentions(limit=10))

#get_user_reels
@instagram_bp.route("/reels", methods=["GET"])
def user_reels_route():
    return jsonify(get_user_reels(limit=10))

#get_reel_insights
@instagram_bp.route("/reels/<reel_id>/insights", methods=["GET"])
def reel_insights_route(reel_id):
    return jsonify(get_reel_insights(reel_id))

#get_user_igtv
@instagram_bp.route("/igtv", methods=["GET"])
def user_igtv_route():
    return jsonify(get_user_igtv(limit=10))

#get_igtv_insights
@instagram_bp.route("/igtv/<video_id>/insights", methods=["GET"])
def igtv_insights_route(video_id):
    return jsonify(get_igtv_insights(video_id))

#get_user_live_videos
@instagram_bp.route("/live-videos", methods=["GET"])
def user_live_videos_route():
    return jsonify(get_user_live_video_candidates())

#get_live_video_insights
@instagram_bp.route("/live-video/<live_video_id>/insights", methods=["GET"])
def live_video_insights_route(live_video_id):
    return jsonify(get_live_video_insights(live_video_id))

#get_user_saved_media
#As of the latest Instagram Graph API its unavailable

#get_user_archived_stories
#As of the latest Instagram Graph API its unavailable

#get_user_highlights
#As of the latest Instagram Graph API its unavailable

#schedule_post
@instagram_bp.route("/schedule-post", methods=["POST"])
def schedule_post_route():
    data = request.json
    media_url = data.get("media_url")
    caption = data.get("caption", "")
    scheduled_time = data.get("scheduled_time")  # UNIX timestamp (int)
    is_video = data.get("is_video", False)

    if not media_url or not scheduled_time:
        return jsonify({"error": "Missing required fields: media_url or scheduled_time"}), 400

    return jsonify(schedule_post(media_url, caption, scheduled_time, is_video))

#cancel_scheduled_post
@instagram_bp.route("/cancel-scheduled-post/<string:media_container_id>", methods=["DELETE"])
def cancel_scheduled_post_route(media_container_id):
    return jsonify(cancel_scheduled_post(media_container_id))

#get_analytics_summary
@instagram_bp.route("/analytics-summary", methods=["GET"])
def analytics_summary_route():
    return jsonify(get_analytics_summary())

#get_daily_engagement
@instagram_bp.route("/daily-engagement", methods=["GET"])
def daily_engagement_route():
    return jsonify(get_daily_engagement())

#get_profile_views
@instagram_bp.route("/profile-views", methods=["GET"])
def profile_views_route():
    return jsonify(get_profile_views())
