from flask import Blueprint, request, jsonify
import os
import tempfile
from app.linkedin.linkedin_service import get_user_profile, get_user_email, get_user_posts, get_profile_picture, get_user_urn,get_organization, get_user_organizations, create_text_post, create_article_post, upload_image_to_linkedin, register_image_upload, create_image_post, register_video_upload, upload_video_to_linkedin, create_video_post, delete_linkedin_post, like_post, unlike_post, comment_post, delete_comment, get_post_comments, get_post_likes, get_post_by_urn, create_company_post, get_company_followers, get_company_updates, get_company_updates, get_job_posting, create_job_posting, update_job_posting, delete_job_posting, get_campaigns, get_lead_gen_forms, submit_lead_form_test, get_ugc_posts, get_post_statistics, get_share_statistics, get_company_insights, get_video_metrics, get_messages, get_invitations, send_message

linkedin_bp = Blueprint("linkedin", __name__)


#get_user_profile
@linkedin_bp.route("/profile", methods=["GET"])
def profile():
    access_token = request.headers.get("Authorization")
    if not access_token:
        return jsonify({"status": "error", "message": "Missing Authorization header"}), 401

    # Remove 'Bearer ' prefix if present
    access_token = access_token.replace("Bearer ", "")
    result = get_user_profile(access_token)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#get_user_email
@linkedin_bp.route("/email", methods=["GET"])
def email():
    access_token = request.headers.get("Authorization")
    if not access_token:
        return jsonify({"status": "error", "message": "Missing Authorization header"}), 401

    access_token = access_token.replace("Bearer ", "")
    result = get_user_email(access_token)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#get_connections
@linkedin_bp.route("/posts", methods=["GET"])
def get_posts():
    access_token = request.headers.get("Authorization")
    if not access_token:
        return jsonify({"status": "error", "message": "Missing Authorization header"}), 401

    access_token = access_token.replace("Bearer ", "")
    result = get_user_posts(access_token)

    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#get_profile_picture
@linkedin_bp.route("/profile-picture", methods=["GET"])
def profile_picture():
    access_token = request.headers.get("Authorization")
    if not access_token:
        return jsonify({"status": "error", "message": "Missing Authorization header"}), 401

    access_token = access_token.replace("Bearer ", "")
    result = get_profile_picture(access_token)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#get_user_urn
@linkedin_bp.route("/urn", methods=["GET"])
def urn():
    access_token = request.headers.get("Authorization")
    if not access_token:
        return jsonify({"status": "error", "message": "Missing Authorization header"}), 401
    access_token = access_token.replace("Bearer ", "")
    result = get_user_urn(access_token)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#get_organization
@linkedin_bp.route("/organization", methods=["GET"])
def organization():
    access_token = request.headers.get("Authorization")
    org_urn = request.args.get("urn")

    if not access_token:
        return jsonify({"status": "error", "message": "Missing Authorization header"}), 401
    if not org_urn:
        return jsonify({"status": "error", "message": "Missing organization URN"}), 400

    access_token = access_token.replace("Bearer ", "")
    result = get_organization(access_token, org_urn)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#get_user_organizations
@linkedin_bp.route("/organizations", methods=["GET"])
def organizations():
    access_token = request.headers.get("Authorization")
    if not access_token:
        return jsonify({"status": "error", "message": "Missing Authorization header"}), 401

    access_token = access_token.replace("Bearer ", "")
    result = get_user_organizations(access_token)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#create_text_post
@linkedin_bp.route("/post", methods=["POST"])
def post_text():
    data = request.get_json()
    access_token = request.headers.get("Authorization")
    author_urn = data.get("author_urn")
    text = data.get("text")

    if not access_token or not author_urn or not text:
        return jsonify({"status": "error", "message": "Missing required parameters"}), 400

    access_token = access_token.replace("Bearer ", "")
    result = create_text_post(access_token, author_urn, text)
    return jsonify(result), result.get("status_code", 201 if result["status"] == "success" else 400)

#create_article_post
@linkedin_bp.route("/article-post", methods=["POST"])
def article_post():
    data = request.get_json()
    access_token = request.headers.get("Authorization")
    author_urn = data.get("author_urn")
    article_url = data.get("article_url")
    text = data.get("text", "")

    if not access_token or not author_urn or not article_url:
        return jsonify({"status": "error", "message": "Missing required parameters"}), 400

    access_token = access_token.replace("Bearer ", "")
    result = create_article_post(access_token, author_urn, article_url, text)
    return jsonify(result), result.get("status_code", 201 if result["status"] == "success" else 400)

#register image
@linkedin_bp.route("/image/register", methods=["POST"])
def image_register():
    data = request.get_json()
    access_token = request.headers.get("Authorization")
    author_urn = data.get("author_urn")

    if not access_token or not author_urn:
        return jsonify({"status": "error", "message": "Missing Authorization header or author_urn"}), 400

    access_token = access_token.replace("Bearer ", "")
    result = register_image_upload(access_token, author_urn)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

# upload_image
@linkedin_bp.route("/image/upload", methods=["POST"])
def image_upload():
    upload_url = request.form.get("upload_url")
    image_file = request.files.get("image_file")

    if not upload_url or not image_file:
        return jsonify({"status": "error", "message": "Missing upload_url or image file"}), 400

    # Use a temp path that works cross-platform
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, image_file.filename)
    
    try:
        image_file.save(temp_path)
        success = upload_image_to_linkedin(upload_url, temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)  # Always clean up

    if success:
        return jsonify({"status": "success", "message": "Image uploaded successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Image upload failed"}), 400

#create_image_post
@linkedin_bp.route("/post/image", methods=["POST"])
def post_image():
    data = request.get_json()
    access_token = request.headers.get("Authorization")
    if not access_token:
        return jsonify({"status": "error", "message": "Missing access token"}), 401
    access_token = access_token.replace("Bearer ", "")

    author_urn = data.get("author_urn")
    image_urns = data.get("image_urns")
    text = data.get("text")

    if not author_urn or not image_urns or not text:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    result = create_image_post(access_token, author_urn, image_urns, text)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#upload_video_to_linkedin
@linkedin_bp.route("/video/upload", methods=["POST"])
def video_upload():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    author_urn = request.form.get("author_urn")
    video_file = request.files.get("video_file")

    if not access_token or not author_urn or not video_file:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    import tempfile
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, video_file.filename)
    video_file.save(temp_path)

    # Call your registration + upload function here
    reg = register_video_upload(access_token, author_urn)
    if reg["status"] != "success":
        os.remove(temp_path)
        return jsonify(reg), reg.get("status_code", 400)

    # Upload video binary to LinkedIn
    success = upload_video_to_linkedin(reg["uploadUrl"], temp_path)
    os.remove(temp_path)

    if success:
        return jsonify({
            "status": "success",
            "asset": reg["asset"]
        }), 200
    else:
        return jsonify({"status": "error", "message": "Upload to LinkedIn failed"}), 400

#create_video_post
@linkedin_bp.route("/video/post", methods=["POST"])
def post_video():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    data = request.json
    author_urn = data.get("author_urn")
    video_urn = data.get("video_urn")
    text = data.get("text", "Check out this video!")

    if not access_token or not author_urn or not video_urn:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    result = create_video_post(access_token, author_urn, video_urn, text)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#get_post
@linkedin_bp.route("/posts/<post_urn>", methods=["GET"])
def get_post_route(post_urn):
    access_token = request.headers.get("Authorization")

    if not access_token:
        return jsonify({"status": "error", "message": "Missing Authorization header"}), 401

    access_token = access_token.replace("Bearer ", "")
    result = get_post_by_urn(access_token, post_urn)

    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#delete_linkedin_post
@linkedin_bp.route("/posts/<path:post_urn>", methods=["DELETE"])
def delete_post(post_urn):
    access_token = request.headers.get("Authorization")
    if not access_token:
        return jsonify({"status": "error", "message": "Missing Authorization header"}), 401

    access_token = access_token.replace("Bearer ", "")
    result = delete_linkedin_post(access_token, post_urn)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)


@linkedin_bp.route("/posts/<post_urn>/like", methods=["POST"])
def like_post_route(post_urn):
    access_token = request.headers.get("Authorization")
    user_urn = request.json.get("user_urn")

    if not access_token:
        return jsonify({"status": "error", "message": "Missing Authorization header"}), 401
    if not user_urn:
        return jsonify({"status": "error", "message": "Missing user_urn in request body"}), 400

    access_token = access_token.replace("Bearer ", "")
    result = like_post(access_token, post_urn, user_urn)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#unlike post
@linkedin_bp.route("/unlike", methods=["DELETE"])
def unlike_post_route():
    access_token = request.headers.get("Authorization")
    data = request.get_json()
    post_urn = data.get("post_urn")
    user_urn = data.get("user_urn")

    if not access_token or not post_urn or not user_urn:
        return jsonify({
            "status": "error",
            "message": "Missing Authorization header, post_urn, or user_urn"
        }), 400

    access_token = access_token.replace("Bearer ", "")
    result = unlike_post(access_token, post_urn, user_urn)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#create comment
@linkedin_bp.route("/comment", methods=["POST"])
def comment_post_route():
    access_token = request.headers.get("Authorization")
    data = request.get_json()
    post_urn = data.get("post_urn")
    user_urn = data.get("user_urn")
    comment_text = data.get("comment_text")

    if not access_token or not post_urn or not user_urn or not comment_text:
        return jsonify({
            "status": "error",
            "message": "Missing Authorization header, post_urn, user_urn, or comment_text"
        }), 400

    access_token = access_token.replace("Bearer ", "")
    result = comment_post(access_token, post_urn, user_urn, comment_text)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#delete_comment
@linkedin_bp.route("/comment", methods=["DELETE"])
def delete_comment_route():
    access_token = request.headers.get("Authorization")
    post_urn = request.args.get("post_urn")
    comment_id = request.args.get("comment_id")

    if not access_token or not post_urn or not comment_id:
        return jsonify({
            "status": "error",
            "message": "Missing Authorization header, post_urn, or comment_id"
        }), 400

    access_token = access_token.replace("Bearer ", "")
    result = delete_comment(access_token, post_urn, comment_id)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#get_post_comments
@linkedin_bp.route("/comments", methods=["GET"])
def get_post_comments_route():
    access_token = request.headers.get("Authorization")
    post_urn = request.args.get("post_urn")

    if not access_token or not post_urn:
        return jsonify({
            "status": "error",
            "message": "Missing Authorization header or post_urn query param"
        }), 400

    access_token = access_token.replace("Bearer ", "")
    result = get_post_comments(access_token, post_urn)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#get_post_likes
@linkedin_bp.route("/likes", methods=["GET"])
def get_post_likes_route():
    access_token = request.headers.get("Authorization")
    post_urn = request.args.get("post_urn")

    if not access_token or not post_urn:
        return jsonify({
            "status": "error",
            "message": "Missing Authorization header or post_urn query param"
        }), 400

    access_token = access_token.replace("Bearer ", "")
    result = get_post_likes(access_token, post_urn)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)
#company post
@linkedin_bp.route("/company/post", methods=["POST"])
def post_company_text():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    data = request.get_json()

    org_urn = data.get("org_urn")
    text = data.get("text")

    if not access_token or not org_urn or not text:
        return jsonify({
            "status": "error",
            "message": "Missing access_token, org_urn, or text"
        }), 400

    result = create_company_post(access_token, org_urn, text)
    return jsonify(result), result.get("status_code", 201 if result["status"] == "success" else 400)

#follower
@linkedin_bp.route("/company/followers", methods=["GET"])
def company_followers():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    org_urn = request.args.get("org_urn")

    if not access_token or not org_urn:
        return jsonify({
            "status": "error",
            "message": "Missing access token or organization URN"
        }), 400

    result = get_company_followers(access_token, org_urn)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#updates
@linkedin_bp.route("/company/updates", methods=["GET"])
def company_updates():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    org_urn = request.args.get("org_urn")
    count = request.args.get("count", 10)

    if not access_token or not org_urn:
        return jsonify({
            "status": "error",
            "message": "Missing access token or org_urn"
        }), 400

    try:
        count = int(count)
    except ValueError:
        count = 10

    result = get_company_updates(access_token, org_urn, count)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#get_job_posting
@linkedin_bp.route("/job/<job_id>", methods=["GET"])
def get_job_by_id(job_id):
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    
    if not access_token:
        return jsonify({
            "status": "error",
            "message": "Missing Authorization header"
        }), 401

    result = get_job_posting(access_token, job_id)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#create_job_posting
@linkedin_bp.route("/job", methods=["POST"])
def create_job():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    job_data = request.get_json()

    if not access_token or not job_data:
        return jsonify({
            "status": "error",
            "message": "Missing access token or job data"
        }), 400

    result = create_job_posting(access_token, job_data)
    return jsonify(result), result.get("status_code", 201 if result["status"] == "success" else 400)

#update job
@linkedin_bp.route("/job/<job_id>", methods=["PATCH"])
def update_job(job_id):
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    job_data = request.get_json()

    if not access_token or not job_data:
        return jsonify({
            "status": "error",
            "message": "Missing access token or job data"
        }), 400

    result = update_job_posting(access_token, job_id, job_data)
    return jsonify(result), result.get("status_code", 204 if result["status"] == "success" else 400)

#delete_job_posting
@linkedin_bp.route("/job/<job_id>", methods=["DELETE"])
def delete_job(job_id):
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")

    if not access_token:
        return jsonify({
            "status": "error",
            "message": "Missing access token"
        }), 401

    result = delete_job_posting(access_token, job_id)
    return jsonify(result), result.get("status_code", 204 if result["status"] == "success" else 400)

#get_campaigns
@linkedin_bp.route("/ads/campaigns", methods=["GET"])
def get_ad_campaigns():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    ad_account_urn = request.args.get("ad_account_urn")

    if not access_token or not ad_account_urn:
        return jsonify({
            "status": "error",
            "message": "Missing access token or ad_account_urn"
        }), 400

    result = get_campaigns(access_token, ad_account_urn)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#lead gen
@linkedin_bp.route("/leadgen/forms", methods=["GET"])
def get_leadgen_forms_route():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    org_urn = request.args.get("org_urn")

    if not access_token or not org_urn:
        return jsonify({
            "status": "error",
            "message": "Missing access token or org_urn"
        }), 400

    result = get_lead_gen_forms(access_token, org_urn)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#submit_lead_form_test
@linkedin_bp.route("/leadgen/forms/test", methods=["POST"])
def submit_test_lead():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    data = request.get_json()
    form_urn = data.get("form_urn")
    test_data = data.get("test_data", {})  # optional override values

    if not access_token or not form_urn:
        return jsonify({
            "status": "error",
            "message": "Missing access token or form_urn"
        }), 400

    result = submit_lead_form_test(access_token, form_urn, test_data)
    return jsonify(result), result.get("status_code", 202 if result["status"] == "success" else 400)

#ugcpost
@linkedin_bp.route("/ugc/posts", methods=["GET"])
def get_ugc_posts_route():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    author_urn = request.args.get("author_urn")
    count = request.args.get("count", 10)

    if not access_token or not author_urn:
        return jsonify({
            "status": "error",
            "message": "Missing access token or author_urn"
        }), 400

    try:
        count = int(count)
    except ValueError:
        count = 10

    result = get_ugc_posts(access_token, author_urn, count)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#get_post_statistics
@linkedin_bp.route("/post/statistics", methods=["GET"])
def get_post_statistics_route():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    post_urn = request.args.get("post_urn")

    if not access_token or not post_urn:
        return jsonify({
            "status": "error",
            "message": "Missing access token or post_urn"
        }), 400

    result = get_post_statistics(access_token, post_urn)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)


#get_share_statistics
@linkedin_bp.route("/post/shares", methods=["GET"])
def get_share_stats_route():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    post_urn = request.args.get("post_urn")

    if not access_token or not post_urn:
        return jsonify({
            "status": "error",
            "message": "Missing access token or post_urn"
        }), 400

    result = get_share_statistics(access_token, post_urn)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#get_company_insights
@linkedin_bp.route("/company/insights", methods=["GET"])
def get_company_insights_route():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    org_urn = request.args.get("org_urn")
    start = request.args.get("start")  # epoch ms (optional)
    end = request.args.get("end")      # epoch ms (optional)

    if not access_token or not org_urn:
        return jsonify({
            "status": "error",
            "message": "Missing access token or org_urn"
        }), 400

    result = get_company_insights(access_token, org_urn, start, end)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#get_video_metrics
@linkedin_bp.route("/video/metrics", methods=["GET"])
def get_video_metrics_route():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    video_urn = request.args.get("video_urn")

    if not access_token or not video_urn:
        return jsonify({
            "status": "error",
            "message": "Missing access token or video_urn"
        }), 400

    result = get_video_metrics(access_token, video_urn)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#send and get messages restricted
@linkedin_bp.route("/message", methods=["POST"])
def send_message_route():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    data = request.get_json()

    recipient_urn = data.get("recipient_urn")
    message_text = data.get("message_text")

    if not access_token or not recipient_urn or not message_text:
        return jsonify({
            "status": "error",
            "message": "Missing access_token, recipient_urn, or message_text"
        }), 400

    result = send_message(access_token, recipient_urn, message_text)
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#get_messages
@linkedin_bp.route("/messages", methods=["GET"])
def get_messages_route():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    start = request.args.get("start", 0)
    count = request.args.get("count", 10)

    if not access_token:
        return jsonify({"status": "error", "message": "Missing access token"}), 401

    result = get_messages(access_token, start=int(start), count=int(count))
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)


# @linkedin_bp.route("/message", methods=["POST"])
# def send_message_route():
#     access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
#     data = request.get_json()
#     recipient_urn = data.get("recipient_urn")
#     message_text = data.get("message_text")

#     if not access_token or not recipient_urn or not message_text:
#         return jsonify({
#             "status": "error",
#             "message": "Missing required fields: access_token, recipient_urn, or message_text"
#         }), 400

#     result = send_message(access_token, recipient_urn, message_text)
#     return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)


# @linkedin_bp.route("/messages", methods=["GET"])
# def get_messages_route():
#     access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
#     start = request.args.get("start", 0)
#     count = request.args.get("count", 10)

#     if not access_token:
#         return jsonify({"status": "error", "message": "Missing access token"}), 401

#     result = get_messages(access_token, start=int(start), count=int(count))
#     return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)

#get_invitations
@linkedin_bp.route("/invitations", methods=["GET"])
def get_invitations_route():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    start = request.args.get("start", 0)
    count = request.args.get("count", 10)

    if not access_token:
        return jsonify({"status": "error", "message": "Missing access token"}), 401

    result = get_invitations(access_token, start=int(start), count=int(count))
    return jsonify(result), result.get("status_code", 200 if result["status"] == "success" else 400)
