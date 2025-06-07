from flask import Blueprint, request, jsonify
from app.whatsapp.whatsapp_service import send_text_message, send_image_message, send_video_message, send_audio_message, send_document_message, send_location_message, send_template_message, upload_media, get_media_url, delete_media, mark_message_read, get_message_status, get_contact_info, get_business_profile, update_business_profile, get_phone_numbers, get_phone_number_status, get_phone_number_status, get_webhook_settings, update_webhook_settings, get_metrics, create_message_template, get_templates, delete_template, get_template_status, get_conversations, get_conversation_details, get_phone_number_quality, get_message_templates_usage, get_blocked_status, get_business_hours, update_business_hours, get_greeting_message, set_greeting_message, send_interactive_message

whatsapp_bp = Blueprint("whatsapp", __name__)

#send_text_message
@whatsapp_bp.route("/send-text", methods=["POST"])
def send_whatsapp_text():
    data = request.get_json()

    phone_number = data.get("phone_number")
    message = data.get("message")

    if not phone_number or not message:
        return jsonify({
            "status": "error",
            "message": "Both 'phone_number' and 'message' are required."
        }), 400

    result = send_text_message(phone_number, message)
    return jsonify(result), 200 if result.get("status") == "sent" else 500

#send_image_message
@whatsapp_bp.route("/send-image", methods=["POST"])
def send_whatsapp_image():
    data = request.get_json()

    phone_number = data.get("phone_number")
    image_url = data.get("image_url")
    caption = data.get("caption", "")

    if not phone_number or not image_url:
        return jsonify({
            "status": "error",
            "message": "Both 'phone_number' and 'image_url' are required."
        }), 400

    result = send_image_message(phone_number, image_url, caption)
    return jsonify(result), 200 if result.get("status") == "sent" else 500

#send_video_message
@whatsapp_bp.route("/send-video", methods=["POST"])
def send_whatsapp_video():
    data = request.get_json()

    phone_number = data.get("phone_number")
    video_url = data.get("video_url")
    caption = data.get("caption", "")

    if not phone_number or not video_url:
        return jsonify({
            "status": "error",
            "message": "Both 'phone_number' and 'video_url' are required."
        }), 400

    result = send_video_message(phone_number, video_url, caption)
    return jsonify(result), 200 if result.get("status") == "sent" else 500

#send_audio_message
@whatsapp_bp.route("/send-audio", methods=["POST"])
def send_whatsapp_audio():
    data = request.get_json()

    phone_number = data.get("phone_number")
    audio_url = data.get("audio_url")

    if not phone_number or not audio_url:
        return jsonify({
            "status": "error",
            "message": "Both 'phone_number' and 'audio_url' are required."
        }), 400

    result = send_audio_message(phone_number, audio_url)
    return jsonify(result), 200 if result.get("status") == "sent" else 500

#send_document_message
@whatsapp_bp.route("/send-document", methods=["POST"])
def send_whatsapp_document():
    data = request.get_json()

    phone_number = data.get("phone_number")
    document_url = data.get("document_url")
    filename = data.get("filename")

    if not phone_number or not document_url or not filename:
        return jsonify({
            "status": "error",
            "message": "'phone_number', 'document_url', and 'filename' are required."
        }), 400

    result = send_document_message(phone_number, document_url, filename)
    return jsonify(result), 200 if result.get("status") == "sent" else 500

#send_location_message
@whatsapp_bp.route("/send-location", methods=["POST"])
def send_whatsapp_location():
    data = request.get_json()

    phone_number = data.get("phone_number")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    name = data.get("name")
    address = data.get("address")

    if not all([phone_number, latitude, longitude, name, address]):
        return jsonify({
            "status": "error",
            "message": "All fields ('phone_number', 'latitude', 'longitude', 'name', 'address') are required."
        }), 400

    result = send_location_message(phone_number, latitude, longitude, name, address)
    return jsonify(result), 200 if result.get("status") == "sent" else 500

#send_template_message
@whatsapp_bp.route("/send-template", methods=["POST"])
def send_whatsapp_template():
    data = request.get_json()

    phone_number = data.get("phone_number")
    template_name = data.get("template_name")
    variables = data.get("variables", [])

    if not phone_number or not template_name:
        return jsonify({
            "status": "error",
            "message": "'phone_number' and 'template_name' are required."
        }), 400

    result = send_template_message(phone_number, template_name, variables)
    return jsonify(result), 200 if result.get("status") == "sent" else 500

#upload_media
@whatsapp_bp.route("/upload-media", methods=["POST"])
def upload_whatsapp_media():
    media_file = request.files.get("file")
    media_type = request.form.get("type")

    if not media_file or not media_type:
        return jsonify({
            "status": "error",
            "message": "Both 'file' and 'type' (MIME) are required."
        }), 400

    result = upload_media(media_file, media_type)
    return jsonify(result), 200 if result.get("status") == "uploaded" else 500

#get_media_url
@whatsapp_bp.route("/get-media-url", methods=["GET"])
def get_whatsapp_media_url():
    media_id = request.args.get("media_id")

    if not media_id:
        return jsonify({
            "status": "error",
            "message": "'media_id' query parameter is required."
        }), 400

    result = get_media_url(media_id)
    return jsonify(result), 200 if result.get("status") == "success" else 500

#delete_media
@whatsapp_bp.route("/delete-media", methods=["DELETE"])
def delete_whatsapp_media():
    media_id = request.args.get("media_id")

    if not media_id:
        return jsonify({
            "status": "error",
            "message": "'media_id' query parameter is required."
        }), 400

    result = delete_media(media_id)
    return jsonify(result), 200 if result.get("status") == "deleted" else 500

#mark_message_read
@whatsapp_bp.route("/mark-read", methods=["POST"])
def mark_whatsapp_message_read():
    data = request.get_json()
    message_id = data.get("message_id")

    if not message_id:
        return jsonify({
            "status": "error",
            "message": "'message_id' is required."
        }), 400

    result = mark_message_read(message_id)
    return jsonify(result), 200 if result.get("status") == "success" else 500

#get_message_status
@whatsapp_bp.route("/get-message-status", methods=["GET"])
def get_whatsapp_message_status():
    message_id = request.args.get("message_id")

    if not message_id:
        return jsonify({
            "status": "error",
            "message": "'message_id' query parameter is required."
        }), 400

    result = get_message_status(message_id)
    return jsonify(result), 200

#get_contact_info
@whatsapp_bp.route("/get-contact", methods=["GET"])
def get_whatsapp_contact():
    phone_number = request.args.get("phone_number")

    if not phone_number:
        return jsonify({
            "status": "error",
            "message": "'phone_number' query parameter is required."
        }), 400

    result = get_contact_info(phone_number)
    return jsonify(result), 200 if result.get("status") == "success" else 500

#get_business_profile
@whatsapp_bp.route("/get-business-profile", methods=["GET"])
def get_whatsapp_business_profile():
    result = get_business_profile()
    return jsonify(result), 200 if result.get("status") == "success" else 500

#update_business_profile
@whatsapp_bp.route("/update-business-profile", methods=["POST"])
def update_whatsapp_business_profile():
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body is empty. Provide fields to update."
        }), 400

    result = update_business_profile(data)
    return jsonify(result), 200 if result.get("status") == "success" else 500

#get_phone_numbers
@whatsapp_bp.route("/get-phone-numbers", methods=["GET"])
def get_whatsapp_phone_numbers():
    result = get_phone_numbers()
    return jsonify(result), 200 if result.get("status") == "success" else 500

#get_phone_number_status
@whatsapp_bp.route("/get-phone-number-status", methods=["GET"])
def get_whatsapp_phone_number_status():
    phone_number = request.args.get("phone_number")

    if not phone_number:
        return jsonify({
            "status": "error",
            "message": "'phone_number' query parameter is required."
        }), 400

    result = get_phone_number_status(phone_number)
    return jsonify(result), 200 if result.get("status") == "success" else 500

#get_webhook_settings
@whatsapp_bp.route("/get-webhook-settings", methods=["GET"])
def get_whatsapp_webhook_settings():
    result = get_webhook_settings()
    return jsonify(result), 200 if result.get("status") == "success" else 500

#update_webhook_settings
@whatsapp_bp.route("/update-webhook-settings", methods=["POST"])
def update_whatsapp_webhook_settings():
    data = request.json or {}
    callback_url = data.get("callback_url")
    verify_token = data.get("verify_token")
    fields = data.get("fields", ["messages"])

    if not callback_url or not verify_token:
        return jsonify({"error": "callback_url and verify_token are required"}), 400

    result = update_webhook_settings(callback_url, verify_token, fields)
    return jsonify(result), 200 if result["status"] == "success" else 500

#get_metrics
@whatsapp_bp.route("/get-metrics", methods=["GET"])
def get_whatsapp_metrics():
    result = get_metrics()
    return jsonify(result), 200 if result["status"] == "success" else 500

#create_message_template
@whatsapp_bp.route("/create-template", methods=["POST"])
def create_template():
    data = request.get_json()
    result = create_message_template(data)
    return jsonify(result), 200 if result["status"] == "success" else 400

#get_templates
@whatsapp_bp.route("/get-templates", methods=["GET"])
def get_whatsapp_templates():
    result = get_templates()
    return jsonify(result), 200 if result.get("status") == "success" else 500

#delete_template
@whatsapp_bp.route("/delete-template", methods=["DELETE"])
def delete_whatsapp_template():
    template_name = request.args.get("name")
    if not template_name:
        return jsonify({"status": "error", "message": "Template name is required"}), 400

    result = delete_template(template_name)
    return jsonify(result), 200 if result.get("status") == "success" else 500

#get_template_status
@whatsapp_bp.route("/template-status", methods=["GET"])
def whatsapp_template_status():
    template_name = request.args.get("name")
    if not template_name:
        return jsonify({"status": "error", "message": "Template name is required"}), 400

    result = get_template_status(template_name)
    return jsonify(result), 200 if result.get("status") == "success" else 404

#get_conversations
@whatsapp_bp.route("/conversations", methods=["GET"])
def whatsapp_get_conversations():
    limit = request.args.get("limit", default=25, type=int)
    result = get_conversations(limit=limit)
    return jsonify(result), 200 if result.get("status") == "success" else 500

#get_conversation_details
@whatsapp_bp.route("/conversation-details/<string:conversation_id>", methods=["GET"])
def whatsapp_get_conversation_details(conversation_id):
    result = get_conversation_details(conversation_id)
    return jsonify(result), 200 if result.get("status") == "success" else 500

#get_phone_number_quality
@whatsapp_bp.route("/phone-number-quality/<string:phone_number_id>", methods=["GET"])
def whatsapp_get_phone_number_quality(phone_number_id):
    result = get_phone_number_quality(phone_number_id)
    return jsonify(result), 200 if result.get("status") == "success" else 500

#get_message_templates_usage
@whatsapp_bp.route("/template-usage/<string:template_name>", methods=["GET"])
def whatsapp_template_usage(template_name):
    result = get_message_templates_usage(template_name)
    return jsonify(result), 200 if result.get("status") == "success" else 500

#get_blocked_status
@whatsapp_bp.route("/blocked-status/<string:phone_number>", methods=["GET"])
def whatsapp_blocked_status(phone_number):
    result = get_blocked_status(phone_number)
    return jsonify(result), 200 if result.get("status") in ["sent", "failed"] else 500

#get_profile_photo
#Not Possible via Cloud API

#get_business_hours
@whatsapp_bp.route("/get-business-hours", methods=["GET"])
def get_business_hours_route():
    result = get_business_hours()
    return jsonify(result), 200 if result["status"] == "success" else 500

#update_business_hours
@whatsapp_bp.route("/update-business-hours", methods=["POST"])
def route_update_business_hours():
    data = request.get_json()
    result = update_business_hours(data)
    return jsonify(result), 200 if result["status"] == "success" else 500

#get_greeting_message
@whatsapp_bp.route("/get-greeting-message", methods=["GET"])
def route_get_greeting_message():
    result = get_greeting_message()
    return jsonify(result), 200 if result["status"] == "success" else 500

#set_greeting_message
@whatsapp_bp.route("/set-greeting-message", methods=["POST"])
def route_set_greeting_message():
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"status": "error", "error": "Missing 'message' in request body"}), 400
    result = set_greeting_message(message)
    return jsonify(result), 200 if result["status"] == "success" else 500

#send_interactive_message
@whatsapp_bp.route("/send-interactive-message", methods=["POST"])
def route_send_interactive_message():
    data = request.get_json()
    phone = data.get("phone_number")
    payload = data.get("payload")

    if not phone or not payload:
        return jsonify({"status": "error", "error": "Missing 'phone_number' or 'payload'"}), 400

    result = send_interactive_message(phone, payload)
    return jsonify(result), 200 if result["status"] == "sent" else 500