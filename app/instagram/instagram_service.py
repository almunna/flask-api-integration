import requests
from flask import current_app

def _call_instagram_api(endpoint: str, params: dict = None, method: str = "GET", data: dict = None) -> dict:
    access_token = current_app.config.get("INSTAGRAM_ACCESS_TOKEN")
    base_url = current_app.config.get("INSTAGRAM_API_BASE_URL")

    if not access_token or not base_url:
        return {"error": "Missing configuration for Instagram API"}

    url = f"{base_url}/{endpoint}"
    params = params or {}
    params["access_token"] = access_token

    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, params=params, data=data)
        else:
            return {"error": f"Unsupported HTTP method: {method}"}

        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

def get_user_profile() -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")
    return _call_instagram_api(
        endpoint=f"{ig_user_id}",
        params={
            "fields": "id,username,account_type,media_count,followers_count,follows_count,name,profile_picture_url"
        }
    )

def get_user_media(limit: int = 10) -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")
    return _call_instagram_api(
        endpoint=f"{ig_user_id}/media",
        params={
            "fields": "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username",
            "limit": limit
        }
    )

#get_user_insights
def get_user_insights(metrics: list = None, period: str = "day") -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")
    metrics = metrics or ["impressions", "reach", "profile_views", "follower_count"]

    return _call_instagram_api(
        endpoint=f"{ig_user_id}/insights",
        params={
            "metric": ",".join(metrics),
            "period": period
        }
    )

#get_media_insights
def get_media_insights(media_id: str, metrics: list = None) -> dict:
    metrics = metrics or ["impressions", "reach", "engagement", "saved"]
    return _call_instagram_api(
        endpoint=f"{media_id}/insights",
        params={
            "metric": ",".join(metrics)
        }
    )

#publish_photo
def publish_photo(image_url: str, caption: str = "") -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")

    # Step 1: Create Media Container
    creation_response = _call_instagram_api(
        endpoint=f"{ig_user_id}/media",
        method="POST",
        data={
            "image_url": image_url,
            "caption": caption
        }
    )

    if "id" not in creation_response:
        return {
            "error": "Failed to create media container",
            "details": creation_response
        }

    creation_id = creation_response["id"]

    # Step 2: Publish Media Container
    publish_response = _call_instagram_api(
        endpoint=f"{ig_user_id}/media_publish",
        method="POST",
        data={"creation_id": creation_id}
    )

    return publish_response

#publish_video
def publish_video(video_url: str, caption: str = "", thumb_offset: int = 0) -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")

    # Step 1: Create media container
    creation_response = _call_instagram_api(
        endpoint=f"{ig_user_id}/media",
        method="POST",
        data={
            "media_type": "VIDEO",
            "video_url": video_url,
            "caption": caption,
            "thumb_offset": thumb_offset
        }
    )

    if "id" not in creation_response:
        return {
            "error": "Failed to create video container",
            "details": creation_response
        }

    creation_id = creation_response["id"]

    # Step 2: Publish the video
    publish_response = _call_instagram_api(
        endpoint=f"{ig_user_id}/media_publish",
        method="POST",
        data={"creation_id": creation_id}
    )

    return publish_response

#publish_carousel
def publish_carousel(media_urls: list, caption: str = "") -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")

    container_ids = []

    for item in media_urls:
        media_type = item.get("type", "IMAGE").upper()
        url_field = "video_url" if media_type == "VIDEO" else "image_url"
        media_url = item.get("url")

        if not media_url:
            return {"error": "Each item must include a valid 'url' field."}

        data = {
            url_field: media_url,
            "is_carousel_item": True
        }

        response = _call_instagram_api(
            endpoint=f"{ig_user_id}/media",
            method="POST",
            data=data
        )

        if "id" not in response:
            return {
                "error": f"Failed to create {media_type} container",
                "details": response
            }

        container_ids.append(response["id"])

    # Step 2: Create the carousel container
    children = ",".join(container_ids)
    creation_response = _call_instagram_api(
        endpoint=f"{ig_user_id}/media",
        method="POST",
        data={
            "media_type": "CAROUSEL",
            "children": children,
            "caption": caption
        }
    )

    if "id" not in creation_response:
        return {
            "error": "Failed to create carousel container",
            "details": creation_response
        }

    creation_id = creation_response["id"]

    # Step 3: Publish the carousel
    publish_response = _call_instagram_api(
        endpoint=f"{ig_user_id}/media_publish",
        method="POST",
        data={"creation_id": creation_id}
    )

    return publish_response

#get_comments
def get_comments(media_id: str, limit: int = 25) -> dict:
    return _call_instagram_api(
        endpoint=f"{media_id}/comments",
        params={
            "fields": "id,text,username,timestamp",
            "limit": limit
        }
    )

#reply_to_comment
def reply_to_comment(comment_id: str, message: str) -> dict:
    if not message:
        return {"error": "Reply message cannot be empty."}

    return _call_instagram_api(
        endpoint=f"{comment_id}/replies",
        method="POST",
        data={
            "message": message
        }
    )

#delete_comment
def _call_instagram_api(endpoint: str, params: dict = None, method: str = "GET", data: dict = None) -> dict:
    access_token = current_app.config.get("INSTAGRAM_ACCESS_TOKEN")
    base_url = current_app.config.get("INSTAGRAM_API_BASE_URL")

    if not access_token or not base_url:
        return {"error": "Missing configuration for Instagram API"}

    url = f"{base_url}/{endpoint}"
    params = params or {}
    params["access_token"] = access_token

    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, params=params, data=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, params=params)
        else:
            return {"error": f"Unsupported HTTP method: {method}"}

        response.raise_for_status()
        return response.json() if response.content else {"success": True}

    except requests.RequestException as e:
        return {
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

def delete_comment(comment_id: str) -> dict:
    return _call_instagram_api(
        endpoint=f"{comment_id}",
        method="DELETE"
    )

#hide_comment/unhide
def hide_comment(comment_id: str, hide: bool = True) -> dict:
    return _call_instagram_api(
        endpoint=f"{comment_id}",
        method="POST",
        data={
            "hidden": str(hide).lower()  # must be 'true' or 'false' as string
        }
    )

#disable_comments
def disable_comments(media_id: str) -> dict:
    return _call_instagram_api(
        endpoint=f"{media_id}",
        method="POST",
        data={
            "comment_enabled": "false"
        }
    )

#enable_comments
def enable_comments(media_id: str) -> dict:
    return _call_instagram_api(
        endpoint=f"{media_id}",
        method="POST",
        data={
            "comment_enabled": "true"
        }
    )

#search_hashtag
def search_hashtag(hashtag_name: str) -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")
    
    return _call_instagram_api(
        endpoint="ig_hashtag_search",
        params={
            "user_id": ig_user_id,
            "q": hashtag_name
        }
    )

#get_hashtag_media
def get_hashtag_media(hashtag_id: str, media_type: str = "recent") -> dict:
    """
    media_type: "recent" or "top"
    """
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")

    if media_type not in ["recent", "top"]:
        return {"error": "Invalid media_type. Use 'recent' or 'top'."}

    endpoint = f"{hashtag_id}/{media_type}_media"

    return _call_instagram_api(
        endpoint=endpoint,
        params={
            "user_id": ig_user_id,
            "fields": "id,caption,media_type,media_url,permalink,timestamp,username"
        }
    )

#get_top_hashtag_media
def get_top_hashtag_media(hashtag_id: str) -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")

    return _call_instagram_api(
        endpoint=f"{hashtag_id}/top_media",
        params={
            "user_id": ig_user_id,
            "fields": "id,caption,media_type,media_url,permalink,timestamp,username"
        }
    )

#get_mentioned_media
def get_mentioned_media(limit: int = 10) -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")

    return _call_instagram_api(
        endpoint=f"{ig_user_id}/mentioned_media",
        params={
            "fields": "id,media_type,media_url,username,caption,permalink,timestamp",
            "limit": limit
        }
    )

#get_business_discovery
def get_business_discovery(target_username: str) -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")

    fields = (
        "username,biography,followers_count,follows_count,"
        "media_count,profile_picture_url,website,name"
    )

    return _call_instagram_api(
        endpoint=f"{ig_user_id}",
        params={
            "fields": f"business_discovery.username({target_username}){{{fields}}}"
        }
    )

#get_user_stories
def get_user_stories(limit: int = 10) -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")

    return _call_instagram_api(
        endpoint=f"{ig_user_id}/stories",
        params={
            "fields": "id,media_type,media_url,timestamp,permalink",
            "limit": limit
        }
    )

#get_story_insights
def get_story_insights(story_id: str) -> dict:
    return _call_instagram_api(
        endpoint=f"{story_id}/insights",
        params={
            "metric": "impressions,reach,replies,taps_forward,taps_back,exits"
        }
    )

#get_tagged_media
def get_tagged_media(limit: int = 10) -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")

    return _call_instagram_api(
        endpoint=f"{ig_user_id}/tags",
        params={
            "fields": "id,media_type,media_url,caption,username,timestamp,permalink",
            "limit": limit
        }
    )

#get_user_albums
def get_user_albums(limit: int = 25) -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")

    media_response = _call_instagram_api(
        endpoint=f"{ig_user_id}/media",
        params={
            "fields": "id,caption,media_type,media_url,permalink,timestamp,username",
            "limit": limit
        }
    )

    if "data" not in media_response:
        return media_response

    albums = [item for item in media_response["data"] if item.get("media_type") == "CAROUSEL_ALBUM"]

    return {"albums": albums}

#get_album_media
def get_album_media(album_id: str) -> dict:
    return _call_instagram_api(
        endpoint=f"{album_id}/children",
        params={
            "fields": "id,media_type,media_url,permalink,timestamp"
        }
    )

#get_media_likes
def get_media_likes(media_id: str) -> dict:
    response = _call_instagram_api(
        endpoint=f"{media_id}/insights",
        params={
            "metric": "likes"
        }
    )

    if "data" in response:
        for metric in response["data"]:
            if metric["name"] == "likes":
                return {"likes": metric["values"][0]["value"]}

    return {"error": "Like count not available", "raw": response}

#get_media_comments_count
def get_media_comments_count(media_id: str) -> dict:
    return _call_instagram_api(
        endpoint=f"{media_id}",
        params={
            "fields": "comments_count"
        }
    )

#get_user_followers
#Instagram Graph API does not support retrieving a full list of followers
def get_user_followers_count() -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")
    return _call_instagram_api(
        endpoint=f"{ig_user_id}",
        params={"fields": "followers_count"}
    )

#get_user_follow_stats
#The Instagram Graph API does not support
def get_user_follow_stats() -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")
    return _call_instagram_api(
        endpoint=f"{ig_user_id}",
        params={"fields": "followers_count,follows_count"}
    )


#get_user_tags
def get_user_tags(limit: int = 10) -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")
    return _call_instagram_api(
        endpoint=f"{ig_user_id}/tags",
        params={
            "fields": "id,caption,media_type,media_url,permalink,timestamp,username",
            "limit": limit
        }
    )

#get_user_mentions
from .utils import _call_instagram_api
def get_user_mentions(limit: int = 10) -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")
    return _call_instagram_api(
        endpoint=f"{ig_user_id}/mentioned_media",
        params={
            "fields": "id,caption,media_type,media_url,permalink,timestamp,username",
            "limit": limit
        }
    )

#get_user_reels
def get_user_reels(limit: int = 10) -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")
    return _call_instagram_api(
        endpoint=f"{ig_user_id}/media",
        params={
            "fields": "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username",
            "limit": limit
        },
        filter_func=lambda items: [item for item in items if item.get("media_type") == "REEL"]
    )

#get_reel_insights
def get_reel_insights(reel_id: str) -> dict:
    return _call_instagram_api(
        endpoint=f"{reel_id}/insights",
        params={
            "metric": "impressions,reach,engagement,saved,video_views"
        }
    )

#get_user_igtv
def get_user_igtv(limit: int = 10) -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")
    return _call_instagram_api(
        endpoint=f"{ig_user_id}/media",
        params={
            "fields": "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username",
            "limit": limit
        },
        filter_func=lambda items: [
            item for item in items
            if item.get("media_type") == "VIDEO"
        ]
    )

#get_igtv_insights
def get_igtv_insights(video_id: str) -> dict:
    return _call_instagram_api(
        endpoint=f"{video_id}/insights",
        params={
            "metric": "impressions,reach,engagement,saved,video_views"
        }
    )

#get_user_live_videos
def get_user_live_video_candidates(limit: int = 20) -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")
    return _call_instagram_api(
        endpoint=f"{ig_user_id}/media",
        params={
            "fields": "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username",
            "limit": limit
        },
        filter_func=lambda items: [
            item for item in items
            if item.get("media_type") == "VIDEO" and "live" in item.get("caption", "").lower()
        ]
    )

#get_live_video_insights
def get_live_video_insights(live_video_id: str) -> dict:
    return _call_instagram_api(
        endpoint=f"{live_video_id}/insights",
        params={
            "metric": "total_video_impressions,total_video_views,total_video_10s_views"
        }
    )

#get_user_saved_media
#As of the latest Instagram Graph API its unavailable

#get_user_archived_stories
#As of the latest Instagram Graph API its unavailable

#get_user_highlights
#As of the latest Instagram Graph API its unavailable

#schedule_post
def schedule_post(media_url: str, caption: str, scheduled_time: int, is_video: bool = False) -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")
    access_token = current_app.config.get("INSTAGRAM_ACCESS_TOKEN")
    api_base_url = current_app.config.get("INSTAGRAM_API_BASE_URL")

    url = f"{api_base_url}/{ig_user_id}/media"
    media_type_field = "video_url" if is_video else "image_url"

    payload = {
        media_type_field: media_url,
        "caption": caption,
        "scheduled_publish_time": scheduled_time,
        "access_token": access_token
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json()  # Returns container ID and status
    except requests.RequestException as e:
        return {
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#cancel_scheduled_post
def cancel_scheduled_post(media_container_id: str) -> dict:
    access_token = current_app.config.get("INSTAGRAM_ACCESS_TOKEN")
    api_base_url = current_app.config.get("INSTAGRAM_API_BASE_URL")

    url = f"{api_base_url}/{media_container_id}"
    params = {"access_token": access_token}

    try:
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return {"status": "cancelled", "media_container_id": media_container_id}
    except requests.RequestException as e:
        return {
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#get_analytics_summary
def get_analytics_summary(metrics=None, period="day") -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")
    access_token = current_app.config.get("INSTAGRAM_ACCESS_TOKEN")
    api_base_url = current_app.config.get("INSTAGRAM_API_BASE_URL")

    default_metrics = [
        "impressions",
        "reach",
        "profile_views",
        "website_clicks",
        "email_contacts",
        "get_directions_clicks"
    ]

    metrics = metrics or default_metrics
    params = {
        "metric": ",".join(metrics),
        "period": period,
        "access_token": access_token
    }

    url = f"{api_base_url}/{ig_user_id}/insights"

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#get_daily_engagement
def get_daily_engagement(metrics=None) -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")
    access_token = current_app.config.get("INSTAGRAM_ACCESS_TOKEN")
    api_base_url = current_app.config.get("INSTAGRAM_API_BASE_URL")

    default_metrics = [
        "impressions",
        "reach",
        "profile_views",
        "website_clicks",
        "email_contacts",
        "get_directions_clicks"
    ]

    metrics = metrics or default_metrics
    params = {
        "metric": ",".join(metrics),
        "period": "day",
        "access_token": access_token
    }

    url = f"{api_base_url}/{ig_user_id}/insights"

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#get_profile_views
def get_profile_views(period="day") -> dict:
    ig_user_id = current_app.config.get("INSTAGRAM_USER_ID")
    access_token = current_app.config.get("INSTAGRAM_ACCESS_TOKEN")
    api_base_url = current_app.config.get("INSTAGRAM_API_BASE_URL")

    params = {
        "metric": "profile_views",
        "period": period,
        "access_token": access_token
    }

    url = f"{api_base_url}/{ig_user_id}/insights"

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }
