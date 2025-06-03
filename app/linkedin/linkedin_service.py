import requests

# === Utility Function ===
def linkedin_get_request(url, access_token, headers=None):
    base_headers = {
        "Authorization": f"Bearer {access_token}"
    }
    if headers:
        base_headers.update(headers)

    response = requests.get(url, headers=base_headers)
    if response.status_code == 200:
        return {"ok": True, "data": response.json()}
    else:
        return {
            "ok": False,
            "message": response.text,
            "status_code": response.status_code
        }

# === get_user_profile ===
def get_user_profile(access_token):
    result = linkedin_get_request("https://api.linkedin.com/v2/userinfo", access_token)
    if result["ok"]:
        return {"status": "success", "profile": result["data"]}
    return {"status": "error", "message": result["message"], "status_code": result["status_code"]}

# === get_user_email ===
def get_user_email(access_token):
    result = linkedin_get_request("https://api.linkedin.com/v2/userinfo", access_token)
    if result["ok"]:
        return {"status": "success", "email": result["data"].get("email")}
    return {"status": "error", "message": result["message"], "status_code": result["status_code"]}

# === get_user_urn (helper for posts) ===
def get_user_urn(access_token):
    result = linkedin_get_request("https://api.linkedin.com/v2/userinfo", access_token)
    if result["ok"]:
        return result["data"].get("sub")
    return None

# === get_user_posts ===
def get_user_posts(access_token):
    user_id = get_user_urn(access_token)
    if not user_id:
        return {"status": "error", "message": "Unable to retrieve user URN", "status_code": 400}

    urn = f"urn:li:person:{user_id}"
    url = f"https://api.linkedin.com/v2/ugcPosts?q=authors&authors=List({urn})"
    result = linkedin_get_request(url, access_token, headers={"X-Restli-Protocol-Version": "2.0.0"})

    if result["ok"]:
        return {"status": "success", "posts": result["data"].get("elements", [])}
    return {"status": "error", "message": result["message"], "status_code": result["status_code"]}

# === get_profile_picture ===
def get_profile_picture(access_token):
    result = linkedin_get_request("https://api.linkedin.com/v2/userinfo", access_token)
    if result["ok"]:
        return {"status": "success", "profile_picture": result["data"].get("picture")}
    return {"status": "error", "message": result["message"], "status_code": result["status_code"]}

#get_user_urn
def get_user_urn(access_token):

    result = linkedin_get_request("https://api.linkedin.com/v2/userinfo", access_token)
    
    if result["ok"]:
        urn = result["data"].get("sub")
        return {
            "status": "success",
            "urn": urn
        }
    
    return {
        "status": "error",
        "message": result["message"],
        "status_code": result["status_code"]
    }

#get_organization
def get_organization(access_token, org_urn):
    org_id = org_urn.split(":")[-1]  # Extract numeric ID from URN
    url = f"https://api.linkedin.com/v2/organizations/{org_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {
            "status": "success",
            "organization": response.json()
        }
    else:
        return {
            "status": "error",
            "message": response.text,
            "status_code": response.status_code
        }
    
#get_user_organizations
def get_user_organizations(access_token):
    """
    Returns a list of organizations the user is an admin of.
    """
    url = (
        "https://api.linkedin.com/v2/organizationAcls"
        "?q=roleAssignee"
        "&role=ADMINISTRATOR"
        "&state=APPROVED"
        "&projection=(elements*(*,organization~*(id,localizedName,vanityName)))"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        elements = response.json().get("elements", [])
        organizations = [
            {
                "id": org.get("organization~", {}).get("id"),
                "name": org.get("organization~", {}).get("localizedName"),
                "vanityName": org.get("organization~", {}).get("vanityName"),
                "urn": org.get("organization")
            }
            for org in elements
            if "organization~" in org
        ]
        return {
            "status": "success",
            "organizations": organizations
        }

    return {
        "status": "error",
        "message": response.text,
        "status_code": response.status_code
    }

#create_text_post
def create_text_post(access_token, author_urn, text):
    """
    Create a simple text-only post for a user.
    
    :param access_token: LinkedIn OAuth token
    :param author_urn: e.g., "urn:li:person:lZjD1qQwwf"
    :param text: Text content of the post
    :return: LinkedIn post URN or error
    """
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        return {
            "status": "success",
            "post_urn": response.headers.get("x-restli-id")
        }
    else:
        return {
            "status": "error",
            "message": response.text,
            "status_code": response.status_code
        }
    
#create_article_post
def create_article_post(access_token, author_urn, article_url, text):

    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "ARTICLE",
                "media": [
                    {
                        "status": "READY",
                        "originalUrl": article_url
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        return {
            "status": "success",
            "post_urn": response.headers.get("x-restli-id")
        }
    else:
        return {
            "status": "error",
            "message": response.text,
            "status_code": response.status_code
        }
    
#create_image_post
def register_image_upload(access_token, author_urn):
    url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "registerUploadRequest": {
            "owner": author_urn,
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "serviceRelationships": [{
                "relationshipType": "OWNER",
                "identifier": "urn:li:userGeneratedContent"
            }]
        }
    }

    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200:
        data = res.json()["value"]
        return {
            "status": "success",
            "asset": data["asset"],
            "uploadUrl": data["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        }
    else:
        return {
            "status": "error",
            "message": res.text,
            "status_code": res.status_code
        }

def register_image_upload(access_token, author_urn):
    url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "registerUploadRequest": {
            "owner": author_urn,
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "serviceRelationships": [{
                "relationshipType": "OWNER",
                "identifier": "urn:li:userGeneratedContent"
            }]
        }
    }

    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200:
        data = res.json()["value"]
        return {
            "status": "success",
            "asset": data["asset"],
            "uploadUrl": data["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        }
    else:
        return {
            "status": "error",
            "message": res.text,
            "status_code": res.status_code
        }

#uploD IMge
def upload_image_to_linkedin(upload_url, image_path):
    with open(image_path, "rb") as file_data:
        headers = {"Content-Type": "application/octet-stream"}
        res = requests.put(upload_url, data=file_data, headers=headers)
        return res.status_code == 201 or res.status_code == 200

#image post
def create_image_post(access_token, author_urn, image_urns, text):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "IMAGE",
                "media": [
                    {
                        "status": "READY",
                        "media": urn
                    } for urn in image_urns
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 201:
        return {
            "status": "success",
            "post_urn": res.headers.get("x-restli-id")
        }
    else:
        return {
            "status": "error",
            "message": res.text,
            "status_code": res.status_code
        }

def register_video_upload(access_token, author_urn):
    url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "registerUploadRequest": {
            "owner": author_urn,
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-video"],
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }

    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200:
        data = res.json()["value"]
        return {
            "status": "success",
            "asset": data["asset"],
            "uploadUrl": data["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        }
    else:
        return {
            "status": "error",
            "message": res.text,
            "status_code": res.status_code
        }

#upload_video_to_linkedin
def upload_video_to_linkedin(upload_url, video_path):
    with open(video_path, "rb") as file_data:
        headers = {"Content-Type": "application/octet-stream"}
        res = requests.put(upload_url, data=file_data, headers=headers)
        return res.status_code == 201 or res.status_code == 200

#create_video_post
def create_video_post(access_token, author_urn, video_urn, text):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "VIDEO",
                "media": [
                    {
                        "status": "READY",
                        "media": video_urn
                    }
                ]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    res = requests.post(url, headers=headers, json=payload)

    if res.status_code == 201:
        return {
            "status": "success",
            "post_urn": res.headers.get("x-restli-id")
        }
    else:
        return {
            "status": "error",
            "message": res.text,
            "status_code": res.status_code
        }

#get_post
def get_post_by_urn(access_token, post_urn):
    url = f"https://api.linkedin.com/rest/posts/{post_urn}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307"  # Use active version
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {
            "status": "success",
            "post": response.json()
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

#delete_linkedin_post
def delete_linkedin_post(access_token, post_urn):
    url = f"https://api.linkedin.com/rest/posts/{post_urn}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307"  # This version must be active
    }

    response = requests.delete(url, headers=headers)
    
    if response.status_code == 204:
        return {"status": "success", "message": "Post deleted successfully"}
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }


#like_post
def like_post(access_token, post_urn, user_urn):
    url = f"https://api.linkedin.com/rest/socialActions/{post_urn}/likes"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "LinkedIn-Version": "202307"
    }
    data = {
        "actor": user_urn
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        return {
            "status": "success",
            "message": "Post liked successfully"
        }
    else:
        return {
            "status": "error",
            "message": response.text,
            "status_code": response.status_code
        }

#unlike post
def unlike_post(access_token, post_urn, user_urn):
    url = f"https://api.linkedin.com/rest/socialActions/{post_urn}/likes/{user_urn}"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307"  # ✅ Valid version format
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return {"status": "success", "message": "Post unliked successfully"}
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

#create comment
def comment_post(access_token, post_urn, user_urn, comment_text):
    url = f"https://api.linkedin.com/rest/socialActions/{post_urn}/comments"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307",
        "Content-Type": "application/json"
    }

    payload = {
        "actor": user_urn,
        "message": {
            "text": comment_text
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        return {
            "status": "success",
            "comment_urn": response.json().get("id", "unknown")
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }
#delete_comment
def delete_comment(access_token, post_urn, comment_id):
    url = f"https://api.linkedin.com/rest/socialActions/{post_urn}/comments/{comment_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return {
            "status": "success",
            "message": "Comment deleted successfully"
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }    

#get_post_comments
def get_post_comments(access_token, post_urn, count=10):
    url = f"https://api.linkedin.com/rest/socialActions/{post_urn}/comments"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307"
    }

    params = {
        "count": count
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return {
            "status": "success",
            "comments": response.json().get("elements", [])
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }
    
#get_post_likes
def get_post_likes(access_token, post_urn, count=10):
    url = f"https://api.linkedin.com/rest/socialActions/{post_urn}/likes"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307"
    }

    params = {
        "count": count
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return {
            "status": "success",
            "likes": response.json().get("elements", [])
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }
    
#company post
def create_company_post(access_token, org_urn, content_text):
 
    url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307",  # Ensure correct API version
        "Content-Type": "application/json"
    }

    payload = {
        "author": org_urn,
        "commentary": content_text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        return {
            "status": "success",
            "post_urn": response.headers.get("x-restli-id", "unknown")
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

#follower
def get_company_followers(access_token, org_urn):
  
    url = "https://api.linkedin.com/rest/organizationalEntityFollowerStatistics"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307"  # latest version
    }
    params = {
        "q": "organizationalEntity",
        "organizationalEntity": org_urn
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        stats = response.json().get("elements", [])
        follower_count = 0

        for entry in stats:
            follower_count += entry.get("followerCounts", {}).get("organicFollowerCount", 0)

        return {
            "status": "success",
            "follower_count": follower_count,
            "raw_data": stats
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

#updates
def get_company_updates(access_token, org_urn, count=10):  
    url = "https://api.linkedin.com/rest/activities"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307"
    }
    params = {
        "q": "actor",
        "actor": org_urn,
        "count": count
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        activities = response.json().get("elements", [])
        return {
            "status": "success",
            "activities": activities
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }
    
#access limited
#get_job_posting
def get_job_posting(access_token, job_id):
    """
    Retrieve a LinkedIn job post by its ID.

    :param access_token: OAuth token with r_organization_social
    :param job_id: Job post ID (e.g., 382719821)
    :return: Job object or error response
    """
    url = f"https://api.linkedin.com/rest/jobs/{job_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {
            "status": "success",
            "job": response.json()
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

#create_job_posting
def create_job_posting(access_token, job_data):
    """
    Create a job post on LinkedIn (requires LinkedIn partner permissions).

    :param access_token: OAuth token with partner-level access
    :param job_data: Dictionary containing job post fields
    :return: Success or error response
    """
    url = "https://api.linkedin.com/rest/jobs"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "LinkedIn-Version": "202307"
    }

    response = requests.post(url, headers=headers, json=job_data)

    if response.status_code == 201:
        job_urn = response.headers.get("x-restli-id", "unknown")
        return {
            "status": "success",
            "job_urn": job_urn,
            "message": "Job created successfully"
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

#update job
def update_job_posting(access_token, job_id, job_data):
    url = f"https://api.linkedin.com/rest/jobs/{job_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "LinkedIn-Version": "202307"
    }

    response = requests.patch(url, headers=headers, json=job_data)

    if response.status_code == 204:
        return {"status": "success", "message": "Job updated successfully"}
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

#delete_job_posting
def delete_job_posting(access_token, job_id):
    """
    Deletes a LinkedIn job post by ID (partner-only access).

    :param access_token: OAuth token with appropriate scopes
    :param job_id: LinkedIn Job ID to delete
    :return: Success or error response
    """
    url = f"https://api.linkedin.com/rest/jobs/{job_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return {
            "status": "success",
            "message": f"Job {job_id} deleted successfully"
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

#get_campaigns
def get_campaigns(access_token, ad_account_urn):
    """
    Retrieve ad campaigns from a LinkedIn Ad Account.

    :param access_token: OAuth token with r_ads scope
    :param ad_account_urn: e.g. "urn:li:sponsoredAccount:123456"
    :return: List of ad campaigns or error
    """
    url = "https://api.linkedin.com/rest/adCampaigns"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307"
    }

    params = {
        "q": "search",
        "search.account.values[0]": ad_account_urn
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return {
            "status": "success",
            "campaigns": response.json().get("elements", [])
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

#lead gen
def get_lead_gen_forms(access_token, org_urn):

    url = "https://api.linkedin.com/rest/leadGenForms"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307"
    }

    params = {
        "q": "organization",
        "organization": org_urn
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return {
            "status": "success",
            "forms": response.json().get("elements", [])
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

#submit_lead_form_test
def submit_lead_form_test(access_token, form_urn, test_data):

    form_id = form_urn.split(":")[-1]  # extract numeric ID
    url = f"https://api.linkedin.com/rest/leadGenForms/{form_id}/test"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307",
        "Content-Type": "application/json"
    }

    # Optional: You can provide specific values for fields like name, email
    payload = test_data or {}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 202:
        return {
            "status": "success",
            "message": "Test lead submitted successfully"
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }


#ugcpost
def get_ugc_posts(access_token, author_urn, count=10):

    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    params = {
        "q": "authors",
        "authors": f"List({author_urn})",
        "count": count
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return {
            "status": "success",
            "posts": response.json().get("elements", [])
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

#get_post_statistics
def get_post_statistics(access_token, post_urn):

    url = "https://api.linkedin.com/rest/socialMetadata"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307"
    }

    params = {
        "q": "entity",
        "entity": post_urn
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return {
            "status": "success",
            "metrics": response.json()
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

#get_share_statistics
def get_share_statistics(access_token, post_urn):
    url = "https://api.linkedin.com/rest/socialMetadata"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307"
    }

    params = {
        "q": "entity",
        "entity": post_urn
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return {
            "status": "success",
            "share_metrics": data.get("sharesSummary", {}),
            "all_metrics": data  # optionally include everything
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

#get_company_insights
def get_company_insights(access_token, org_urn, start_epoch=None, end_epoch=None):

    url = "https://api.linkedin.com/rest/organizationPageStatistics"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307"
    }

    params = {
        "q": "organization",
        "organization": org_urn,
        "timeIntervals.timeGranularityType": "DAY"
    }

    if start_epoch and end_epoch:
        params.update({
            "timeIntervals.timeRange.start": start_epoch,
            "timeIntervals.timeRange.end": end_epoch
        })

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return {
            "status": "success",
            "insights": response.json()
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

#get_video_metrics
def get_video_metrics(access_token, video_urn):

    url = "https://api.linkedin.com/rest/videoAnalytics"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202307"
    }

    params = {
        "q": "entity",
        "entity": video_urn
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return {
            "status": "success",
            "metrics": response.json().get("elements", [])
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

#send_message & get messages resitriced
def send_message(access_token, recipient_urn, message_text):
    """
    Sends a direct message to a 1st-degree LinkedIn connection.
    
    Args:
        access_token (str): LinkedIn OAuth token with messaging scope.
        recipient_urn (str): URN of the recipient (e.g., urn:li:person:xxxx).
        message_text (str): Message to send.

    Returns:
        dict: Response with message_id or error.
    """
    url = "https://api.linkedin.com/v2/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    payload = {
        "recipients": [recipient_urn],
        "subject": "Message from LinkedIn App",
        "body": message_text
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        return {
            "status": "success",
            "message_id": response.json().get("id"),
            "data": response.json()
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

#get message
def get_messages(access_token, start=0, count=10):
    """
    Fetches conversations (sent and received messages) for the authenticated LinkedIn user.

    Args:
        access_token (str): LinkedIn OAuth token with messaging permissions.
        start (int): Pagination start.
        count (int): Number of conversations/messages to retrieve.

    Returns:
        dict: List of messages or error.
    """
    url = "https://api.linkedin.com/v2/conversations"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    params = {
        "start": start,
        "count": count
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return {
            "status": "success",
            "conversations": response.json().get("elements", [])
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }

# def send_message(access_token, recipient_urn, message_text):
#     """
#     Sends a direct message to a 1st-degree connection via LinkedIn Messaging API.
#     """
#     url = "https://api.linkedin.com/v2/messages"
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json",
#         "X-Restli-Protocol-Version": "2.0.0"
#     }

#     payload = {
#         "recipients": [recipient_urn],
#         "subject": "New Message from App",
#         "body": message_text
#     }

#     response = requests.post(url, headers=headers, json=payload)

#     if response.status_code in [200, 201]:
#         return {
#             "status": "success",
#             "message_id": response.json().get("id"),
#             "data": response.json()
#         }
#     else:
#         return {
#             "status": "error",
#             "status_code": response.status_code,
#             "message": response.text
#         }

# def get_messages(access_token, start=0, count=10):

#     url = "https://api.linkedin.com/v2/conversations"
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "X-Restli-Protocol-Version": "2.0.0"
#     }
#     params = {
#         "start": start,
#         "count": count
#     }

#     response = requests.get(url, headers=headers, params=params)

#     if response.status_code == 200:
#         return {
#             "status": "success",
#             "conversations": response.json().get("elements", [])
#         }
#     else:
#         return {
#             "status": "error",
#             "status_code": response.status_code,
#             "message": response.text
#         }

#get_invitations
def get_invitations(access_token, start=0, count=10):

    url = "https://api.linkedin.com/v2/invitations"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    params = {
        "q": "receivedInvitation",
        "start": start,
        "count": count
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return {
            "status": "success",
            "invitations": response.json().get("elements", [])
        }
    else:
        return {
            "status": "error",
            "status_code": response.status_code,
            "message": response.text
        }
