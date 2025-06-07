import requests
from flask import current_app

def get_user_profile():
    """Fetch basic user profile from Facebook Graph API."""
    access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")
    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")

    url = f"{base_url}/me"
    params = {
        "fields": "id,name,email,picture",
        "access_token": access_token
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }

#get_user_picture
def get_user_picture(user_id: str, access_token: str = None):
    """Fetches the user's profile picture object from Facebook Graph API."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{user_id}/picture"
    
    params = {
        "redirect": "false",  # Important to get the URL instead of being redirected
        "access_token": access_token
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # Returns a JSON with picture URL, height, width, etc.
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_user_friends
def get_user_friends(user_id: str, access_token: str = None):
    """Fetch list of a user's friends (only those who authorized the app)."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{user_id}/friends"
    params = {
        "access_token": access_token
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_user_feed
def get_user_feed(user_id: str, access_token: str = None):
    """Fetch posts from a user's feed."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{user_id}/feed"

    params = {
        "access_token": access_token,
        "fields": "id,message,story,created_time,from,full_picture,permalink_url"  # Customize as needed
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }

#get_user_likes
def get_user_likes(user_id: str, access_token: str = None):
    """Fetches the list of pages liked by the user."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{user_id}/likes"

    params = {
        "access_token": access_token,
        "fields": "name,category,created_time"  # You can add `picture{url}` if needed
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_user_posts
def get_user_posts(user_id: str, access_token: str = None):
    """Fetches posts created by the authenticated user."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{user_id}/posts"

    params = {
        "access_token": access_token,
        "fields": "id,message,story,created_time,full_picture,permalink_url"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
 #create_post
def create_post(user_id: str, message: str, access_token: str = None):
    """Creates a post on the user's timeline or feed (if permissions allow)."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{user_id}/feed"

    data = {
        "message": message,
        "access_token": access_token
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()  # Returns post_id if successful
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_post
def get_post(post_id: str, access_token: str = None):
    """Retrieves a specific post by ID from Facebook Graph API."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{post_id}"

    params = {
        "access_token": access_token,
        "fields": "id,message,story,created_time,from,permalink_url,full_picture"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#delete_post
def delete_post(post_id: str, access_token: str = None):
    """Deletes a specific Facebook post by ID."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{post_id}"

    params = {
        "access_token": access_token
    }

    try:
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return {"success": True, "message": f"Post {post_id} deleted successfully"}
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    

#get_post_comments
def get_post_comments(post_id: str, access_token: str = None):
    """Fetches comments on a specific Facebook post."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{post_id}/comments"

    params = {
        "access_token": access_token,
        "fields": "id,message,created_time,from"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#add_comment
def add_comment(post_id: str, message: str, access_token: str = None):
    """Adds a comment to a specific Facebook post."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{post_id}/comments"

    data = {
        "message": message,
        "access_token": access_token
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()  # Contains comment ID
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#delete_comment
def delete_comment(comment_id: str, access_token: str = None):
    """Deletes a specific Facebook comment by ID."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{comment_id}"

    params = {
        "access_token": access_token
    }

    try:
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return {"success": True, "message": f"Comment {comment_id} deleted successfully"}
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_post_reactions
def get_post_reactions(post_id: str, access_token: str = None):
    """Fetches reactions on a Facebook post."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{post_id}/reactions"

    params = {
        "access_token": access_token,
        "fields": "id,name,type"  # You can customize this
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#add_reaction
def add_reaction(post_id: str, reaction_type: str, access_token: str = None):
    """
    Adds a reaction (LIKE, LOVE, WOW, etc.) to a post.
    Only works with a valid Page access token.
    """
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{post_id}/reactions"

    data = {
        "type": reaction_type.upper(),  # Must be LIKE, LOVE, WOW, HAHA, SAD, ANGRY, THANKFUL
        "access_token": access_token
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return {"success": True, "message": f"Reaction {reaction_type} added to post {post_id}"}
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#remove_reaction
def remove_reaction(post_id: str, access_token: str = None):
    """
    Removes the current user's (or page's) reaction from a post.
    Works only if that user/page has reacted to it.
    """
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{post_id}/reactions"

    params = {
        "access_token": access_token
    }

    try:
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return {"success": True, "message": f"Reaction removed from post {post_id}"}
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_user_photos
def get_user_photos(user_id: str, access_token: str = None):
    """Fetches photos uploaded by the user."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")
    
    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{user_id}/photos"

    params = {
        "type": "uploaded",
        "access_token": access_token,
        "fields": "id,name,created_time,images,link"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # Returns list of photo objects
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#upload_photo
def upload_photo(user_id: str, access_token: str, image_url: str = None, image_file=None, caption: str = None):
    """Uploads a new photo to the user's timeline via URL or file."""
    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{user_id}/photos"

    params = {
        "access_token": access_token
    }

    data = {}
    if caption:
        data["caption"] = caption

    try:
        if image_url:
            # Upload using image URL
            data["url"] = image_url
            response = requests.post(url, params=params, data=data)
        elif image_file:
            # Upload using local file
            files = {"source": image_file}
            response = requests.post(url, params=params, data=data, files=files)
        else:
            return {"error": "Either image_url or image_file must be provided"}

        response.raise_for_status()
        return response.json()  # Returns the photo ID
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_user_videos
def get_user_videos(user_id: str, access_token: str = None):
    """Fetches videos uploaded by a user."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{user_id}/videos"

    params = {
        "access_token": access_token,
        "fields": "id,title,description,length,created_time,permalink_url,source,thumbnails"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # List of videos
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#upload_video
def upload_video(user_id: str, access_token: str, video_file, description: str = None, title: str = None):
    """Uploads a video file to a user's timeline."""
    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{user_id}/videos"

    params = {
        "access_token": access_token
    }

    data = {}
    if title:
        data["title"] = title
    if description:
        data["description"] = description

    files = {
        "source": video_file
    }

    try:
        response = requests.post(url, params=params, data=data, files=files)
        response.raise_for_status()
        return response.json()  # Returns the video ID
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_video_views
def get_video_views(video_id: str, access_token: str = None):
    """Fetches the view count of a Facebook video by ID."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")
    
    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{video_id}"

    params = {
        "access_token": access_token,
        "fields": "id,permalink_url,description,created_time,views"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # Includes view count
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_page_info
def get_page_info(page_id: str, access_token: str = None):
    """Fetches basic information about a Facebook Page."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{page_id}"

    params = {
        "access_token": access_token,
        "fields": "id,name,about,fan_count,category,link,cover,picture,description,location,website"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_page_feed
def get_page_feed(page_id: str, access_token: str = None):
    """Fetches the feed/posts from a Facebook Page."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")
    
    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{page_id}/feed"

    params = {
        "access_token": access_token,
        "fields": "id,message,story,created_time,permalink_url,from,full_picture"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # List of posts
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_page_insights
def get_page_insights(page_id: str, metric: str, access_token: str = None):
    """Fetches page insights based on a specific metric."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")
    
    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{page_id}/insights"

    params = {
        "access_token": access_token,
        "metric": metric
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # Insight data
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#post_to_page
def post_to_page(page_id: str, message: str, access_token: str = None):
    """Posts a message to the page's timeline."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")
    
    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{page_id}/feed"

    data = {
        "message": message,
        "access_token": access_token
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()  # Should include "id": "page_id_post_id"
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#delete_page_post
def delete_page_post(post_id: str, access_token: str = None):
    """Deletes a specific post made by a Facebook Page."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")
    
    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{post_id}"

    params = {
        "access_token": access_token
    }

    try:
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return {"success": True, "message": f"Post {post_id} deleted successfully"}
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_event_info
def get_event_info(event_id: str, access_token: str = None):
    """Fetches details of a Facebook event by ID."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")
    
    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{event_id}"

    params = {
        "access_token": access_token,
        "fields": "id,name,description,start_time,end_time,place,cover,attending_count,maybe_count,declined_count,owner"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_user_events
def get_user_events(user_id: str, access_token: str = None):
    """Fetches events the user is attending or invited to."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")
    
    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{user_id}/events"

    params = {
        "access_token": access_token,
        "fields": "id,name,description,start_time,end_time,place,cover,rsvp_status"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # List of events
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#create_event
def create_event(page_id: str, event_data: dict, access_token: str = None):
    """Creates a new event on a Facebook Page."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")
    
    url = f"https://graph.facebook.com/v18.0/{page_id}/events"

    # Ensure mandatory fields are present
    required_fields = ["name", "start_time", "end_time"]
    for field in required_fields:
        if field not in event_data:
            return {"error": f"Missing required field: {field}"}

    event_data["access_token"] = access_token

    try:
        response = requests.post(url, data=event_data)
        response.raise_for_status()
        return response.json()  # Contains 'id' of the new event
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#update_event
def update_event(event_id: str, updates: dict, access_token: str = None):
    """Updates a Facebook event's details."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    url = f"https://graph.facebook.com/v18.0/{event_id}"
    updates["access_token"] = access_token

    try:
        response = requests.post(url, data=updates)
        response.raise_for_status()
        return {"success": True, "message": f"Event {event_id} updated successfully"}
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#delete_event
def delete_event(event_id: str, access_token: str = None):
    """Deletes a Facebook event created by a Page."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")
    
    url = f"https://graph.facebook.com/v18.0/{event_id}"
    params = {
        "access_token": access_token
    }

    try:
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return {
            "success": True,
            "message": f"Event {event_id} deleted successfully"
        }
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_group_info
def get_group_info(group_id: str, access_token: str = None):
    """Fetches information about a Facebook group."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")
    
    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{group_id}"

    params = {
        "access_token": access_token,
        "fields": "id,name,privacy,description,icon,updated_time,member_count"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # Group object
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_user_groups
def get_user_groups(user_id: str, access_token: str = None):
    """Fetches groups the user is an admin of."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")
    
    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{user_id}/groups"

    params = {
        "access_token": access_token,
        "fields": "id,name,privacy,description,icon,updated_time"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # List of groups
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_group_feed
def get_group_feed(group_id: str, access_token: str = None):
    """Retrieves posts (feed) from a Facebook Group."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")
    
    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{group_id}/feed"

    params = {
        "access_token": access_token,
        "fields": "id,message,created_time,from,permalink_url"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # List of posts
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#post_to_group
def post_to_group(group_id: str, message: str, access_token: str = None):
    """Creates a new post in a Facebook Group."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{group_id}/feed"

    payload = {
        "message": message,
        "access_token": access_token
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json()  # Returns post_id
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#delete_group_post
def delete_group_post(post_id: str, access_token: str = None):
    """Deletes a post from a Facebook Group."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{post_id}"

    params = {
        "access_token": access_token
    }

    try:
        response = requests.delete(url, params=params)
        response.raise_for_status()
        return {
            "success": True,
            "message": f"Post {post_id} deleted successfully"
        }
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_user_notifications
def get_user_notifications(user_id: str = "me", access_token: str = None):
    """Retrieves recent notifications for a Facebook user."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{user_id}/notifications"

    params = {
        "access_token": access_token,
        "fields": "title,link,unread,created_time"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # List of notifications
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_ad_accounts
def get_ad_accounts(access_token: str = None):
    """Retrieves ad accounts associated with the authenticated user."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/me/adaccounts"

    params = {
        "access_token": access_token,
        "fields": "id,account_id,name,account_status,currency,timezone_name,amount_spent"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # List of ad accounts
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_ad_campaigns
def get_ad_campaigns(ad_account_id: str, access_token: str = None):
    """Retrieves ad campaigns under a specific Facebook ad account."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    # Facebook requires `act_` prefix for ad account ID
    prefixed_id = f"act_{ad_account_id}"
    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{prefixed_id}/campaigns"

    params = {
        "access_token": access_token,
        "fields": "id,name,status,effective_status,budget_remaining,start_time,stop_time,daily_budget"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_ad_insights
def get_ad_insights(ad_account_id: str, access_token: str = None):
    """Fetches insights (performance metrics) for a Facebook ad account."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    prefixed_id = f"act_{ad_account_id}"
    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{prefixed_id}/insights"

    params = {
        "access_token": access_token,
        "level": "campaign",
        "date_preset": "last_30_days",
        "fields": "campaign_name,impressions,clicks,spend,reach,cpc,ctr"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_instagram_business_account
def get_instagram_business_account(page_id: str, access_token: str = None):
    """Retrieves the Instagram Business Account linked to a Facebook Page."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{page_id}"

    params = {
        "fields": "instagram_business_account",
        "access_token": access_token
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # Contains instagram_business_account.id
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_messenger_profile
def get_messenger_profile(access_token: str = None):
    """Fetches the Messenger profile settings for a Facebook Page."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    url = "https://graph.facebook.com/v18.0/me/messenger_profile"
    params = {
        "access_token": access_token,
        "fields": "greeting,get_started,persistent_menu,whitelisted_domains"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#send_messenger_message
def send_messenger_message(recipient_id: str, message: str, access_token: str = None):
    """Sends a message to a user via Facebook Messenger."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    url = "https://graph.facebook.com/v18.0/me/messages"
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "recipient": { "id": recipient_id },
        "message": { "text": message },
        "messaging_type": "RESPONSE",
        "access_token": access_token
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()  # Should include message_id
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }

#get_messenger_messages
def get_messenger_conversations(page_id: str, access_token: str = None):
    """Fetches list of Messenger conversations for a page."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{page_id}/conversations"

    params = {
        "access_token": access_token,
        "fields": "id,updated_time,snippet,senders"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # List of conversation threads
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }


def get_messages_from_conversation(conversation_id: str, access_token: str = None):
    """Fetches messages from a specific Messenger conversation."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    url = f"https://graph.facebook.com/v18.0/{conversation_id}/messages"
    params = {
        "access_token": access_token,
        "fields": "id,message,from,to,created_time"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_user_tags
def get_user_tags(user_id: str, access_token: str = None):
    """Gets media (photos/videos) where the user is tagged."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{user_id}/tags"

    params = {
        "access_token": access_token,
        "fields": "id,name,created_time,from,picture,link"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()  # Returns media objects where the user is tagged
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }
    
#get_user_checkins
def get_user_checkins(user_id: str, access_token: str = None):
    """Fetches user posts that include check-in locations."""
    if not access_token:
        access_token = current_app.config.get("FACEBOOK_ACCESS_TOKEN")

    base_url = current_app.config.get("FACEBOOK_GRAPH_API_BASE_URL", "https://graph.facebook.com/v18.0")
    url = f"{base_url}/{user_id}/posts"

    params = {
        "access_token": access_token,
        "fields": "place,message,created_time",
        "limit": 100  # Optional: fetch more or paginate
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        posts = response.json().get("data", [])
        # Filter posts that have a place (i.e., check-ins)
        checkins = [post for post in posts if "place" in post]
        return {"checkins": checkins}
    except requests.RequestException as e:
        return {
            "error": str(e),
            "response": getattr(e.response, "text", None)
        }