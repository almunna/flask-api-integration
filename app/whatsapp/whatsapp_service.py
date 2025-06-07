import requests
from app.config import Config


#send_text_message
def send_text_message(phone_number: str, message: str) -> dict:
    """
    Sends a plain text message to a WhatsApp user using the Cloud API.

    Args:
        phone_number (str): Recipient’s full phone number in international format.
        message (str): Message body to send.

    Returns:
        dict: API response containing the message ID or error details.
    """
    url = f"{Config.WHATSAPP_BASE_URL}/{Config.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "status": "sent",
            "message_id": response.json().get("messages", [{}])[0].get("id"),
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }
    
#send_image_message
def send_image_message(phone_number: str, image_url: str, caption: str = "") -> dict:
    """
    Sends an image message to a WhatsApp user.

    Args:
        phone_number (str): Recipient's phone number in international format.
        image_url (str): Public URL of the image to send.
        caption (str): Optional caption text.

    Returns:
        dict: API response including message ID or error details.
    """
    url = f"{Config.WHATSAPP_BASE_URL}/{Config.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "image",
        "image": {
            "link": image_url,
            "caption": caption
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "status": "sent",
            "message_id": response.json().get("messages", [{}])[0].get("id"),
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#send_video_message
def send_video_message(phone_number: str, video_url: str, caption: str = "") -> dict:
    """
    Sends a video message to a WhatsApp user.

    Args:
        phone_number (str): Recipient's phone number in international format.
        video_url (str): Public URL of the video to send.
        caption (str): Optional caption text.

    Returns:
        dict: API response including message ID or error details.
    """
    url = f"{Config.WHATSAPP_BASE_URL}/{Config.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "video",
        "video": {
            "link": video_url,
            "caption": caption
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "status": "sent",
            "message_id": response.json().get("messages", [{}])[0].get("id"),
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#send_audio_message
def send_audio_message(phone_number: str, audio_url: str) -> dict:
    """
    Sends an audio message to a WhatsApp user.

    Args:
        phone_number (str): Recipient's phone number in international format.
        audio_url (str): Public URL of the audio file (e.g., .mp3, .ogg, .aac).

    Returns:
        dict: API response including message ID or error details.
    """
    url = f"{Config.WHATSAPP_BASE_URL}/{Config.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "audio",
        "audio": {
            "link": audio_url
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "status": "sent",
            "message_id": response.json().get("messages", [{}])[0].get("id"),
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#send_document_message
def send_document_message(phone_number: str, document_url: str, filename: str) -> dict:
    """
    Sends a document file to a WhatsApp user.

    Args:
        phone_number (str): Recipient's phone number in international format.
        document_url (str): Publicly accessible document URL (PDF, DOCX, etc.).
        filename (str): Desired filename to display in WhatsApp.

    Returns:
        dict: API response including message ID or error details.
    """
    url = f"{Config.WHATSAPP_BASE_URL}/{Config.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "document",
        "document": {
            "link": document_url,
            "filename": filename
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "status": "sent",
            "message_id": response.json().get("messages", [{}])[0].get("id"),
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#send_location_message
def send_location_message(phone_number: str, latitude: float, longitude: float, name: str, address: str) -> dict:
    """
    Sends a location pin to a WhatsApp user.

    Args:
        phone_number (str): Recipient's phone number in international format.
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        name (str): Name of the location.
        address (str): Address text for the location.

    Returns:
        dict: API response including message ID or error details.
    """
    url = f"{Config.WHATSAPP_BASE_URL}/{Config.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "location",
        "location": {
            "latitude": latitude,
            "longitude": longitude,
            "name": name,
            "address": address
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "status": "sent",
            "message_id": response.json().get("messages", [{}])[0].get("id"),
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#send_template_message
def send_template_message(phone_number: str, template_name: str, variables: list) -> dict:
    """
    Sends a pre-approved template message to a WhatsApp user.

    Args:
        phone_number (str): Recipient's phone number in international format.
        template_name (str): Name of the pre-approved template.
        variables (list): List of variable values to substitute into the template.

    Returns:
        dict: API response including message ID or error details.
    """
    url = f"{Config.WHATSAPP_BASE_URL}/{Config.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    components = [{
        "type": "body",
        "parameters": [{"type": "text", "text": v} for v in variables]
    }]

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": "en_US"},
            "components": components
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "status": "sent",
            "message_id": response.json().get("messages", [{}])[0].get("id"),
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#upload_media
def upload_media(media_file, media_type: str) -> dict:
    """
    Uploads media to WhatsApp servers and returns a media ID.

    Args:
        media_file: A FileStorage object (from Flask's request.files).
        media_type (str): MIME type (e.g., 'image/jpeg', 'application/pdf').

    Returns:
        dict: Response with media ID or error details.
    """
    url = f"{Config.WHATSAPP_BASE_URL}/{Config.WHATSAPP_PHONE_NUMBER_ID}/media"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"
        # Note: Content-Type must be set automatically by 'requests' when using 'files'
    }

    files = {
        "file": (media_file.filename, media_file.stream, media_type)
    }

    try:
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()
        return {
            "status": "uploaded",
            "media_id": response.json().get("id"),
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#get_media_url
def get_media_url(media_id: str) -> dict:
    """
    Retrieves the direct download URL for media uploaded to WhatsApp.

    Args:
        media_id (str): ID of the uploaded media.

    Returns:
        dict: Media URL or error details.
    """
    url = f"{Config.WHATSAPP_BASE_URL}/{media_id}"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {
            "status": "success",
            "media_url": response.json().get("url"),
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#delete_media
def delete_media(media_id: str) -> dict:
    """
    Deletes a media file from WhatsApp servers using its media ID.

    Args:
        media_id (str): The ID of the uploaded media to be deleted.

    Returns:
        dict: Confirmation message or error details.
    """
    url = f"{Config.WHATSAPP_BASE_URL}/{media_id}"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"
    }

    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            return {
                "status": "deleted",
                "message": f"Media with ID {media_id} deleted successfully."
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to delete media.",
                "response": response.text
            }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#mark_message_read
def mark_message_read(message_id: str) -> dict:
    """
    Marks an incoming message as read.

    Args:
        message_id (str): The ID of the message to mark as read.

    Returns:
        dict: Confirmation of the read status or error details.
    """
    url = f"{Config.WHATSAPP_BASE_URL}/{Config.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "status": "success",
            "message": f"Message {message_id} marked as read.",
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#get_message_status
def get_message_status(message_id: str) -> dict:
    """
    Simulates retrieving message status for a given message ID.
    Replace this with DB query if using webhook-based logging.

    Args:
        message_id (str): The ID of the message to check.

    Returns:
        dict: Simulated or logged message status.
    """
    # Replace this mock with actual DB lookup if using webhooks
    return {
        "status": "success",
        "message_id": message_id,
        "delivery_status": "delivered",   # or "read", "failed"
        "read": True,
        "timestamp": "2025-06-07T21:00:00Z"
    }

#get_contact_info
def get_contact_info(phone_number: str) -> dict:
    """
    Retrieves WhatsApp contact information for a given phone number.

    Args:
        phone_number (str): Phone number in international format.

    Returns:
        dict: Contact object or error details.
    """
    url = f"{Config.WHATSAPP_BASE_URL}/{Config.WHATSAPP_PHONE_NUMBER_ID}/contacts"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "blocking": "wait",
        "contacts": [phone_number]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "status": "success",
            "contact": response.json().get("contacts", [{}])[0],
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#get_business_profile
def get_business_profile() -> dict:
    """
    Retrieves the WhatsApp Business account profile.

    Returns:
        dict: Business profile object or error details.
    """
    url = f"{Config.WHATSAPP_BASE_URL}/{Config.WHATSAPP_PHONE_NUMBER_ID}/whatsapp_business_profile"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {
            "status": "success",
            "profile": response.json(),
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#update_business_profile
def update_business_profile(data: dict) -> dict:
    """
    Updates the WhatsApp Business account profile.

    Args:
        data (dict): Dictionary containing any of the updatable fields:
            - about
            - address
            - description
            - email
            - vertical
            - websites (list)

    Returns:
        dict: Updated profile response or error details.
    """
    url = f"{Config.WHATSAPP_BASE_URL}/{Config.WHATSAPP_PHONE_NUMBER_ID}/whatsapp_business_profile"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    valid_fields = {"about", "address", "description", "email", "vertical", "websites"}
    payload = {k: v for k, v in data.items() if k in valid_fields}

    if not payload:
        return {
            "status": "error",
            "message": "No valid fields provided for update."
        }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "status": "success",
            "updated_fields": payload,
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#get_phone_numbers
def get_phone_numbers() -> dict:
    """
    Retrieves all phone numbers associated with the WhatsApp Business Account (WABA).

    Returns:
        dict: List of phone numbers or error details.
    """
    waba_id = Config.WHATSAPP_PHONE_NUMBER_ID
    url = f"{Config.WHATSAPP_BASE_URL}/{waba_id}/phone_numbers"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {
            "status": "success",
            "phone_numbers": response.json().get("data", []),
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#get_phone_number_status
def get_phone_number_status(phone_number: str) -> dict:
    """
    Checks if a phone number is registered on WhatsApp.

    Args:
        phone_number (str): Phone number in international format (e.g., 8801XXXXXXXXX)

    Returns:
        dict: Status info including registration and WhatsApp ID.
    """
    url = f"{Config.WHATSAPP_BASE_URL}/{Config.WHATSAPP_PHONE_NUMBER_ID}/contacts"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "blocking": "wait",
        "contacts": [phone_number]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        contact_info = response.json().get("contacts", [{}])[0]
        return {
            "status": "success",
            "wa_id": contact_info.get("wa_id"),
            "input": contact_info.get("input"),
            "validation_status": contact_info.get("status"),
            "raw": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#get_webhook_settings
def get_webhook_settings() -> dict:
    """
    Retrieves current webhook settings for the Meta App (used by WhatsApp API).

    Returns:
        dict: Webhook config or error details.
    """
    url = f"https://graph.facebook.com/{Config.FACEBOOK_GRAPH_API_VERSION}/{Config.FACEBOOK_APP_ID}/subscriptions"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {
            "status": "success",
            "webhook_config": response.json().get("data", []),
            "raw": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#update_webhook_settings
def update_webhook_settings(callback_url: str, verify_token: str, fields: list) -> dict:
    """
    Sets or updates the webhook callback URL for the Meta App.

    Args:
        callback_url (str): The callback URL for webhook events.
        verify_token (str): A token to verify requests from Meta.
        fields (list): List of fields to subscribe to (e.g., ["messages"]).

    Returns:
        dict: Confirmation response or error details.
    """
    url = f"https://graph.facebook.com/{Config.FACEBOOK_GRAPH_API_VERSION}/{Config.FACEBOOK_APP_ID}/subscriptions"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "object": "whatsapp_business_account",
        "callback_url": callback_url,
        "verify_token": verify_token,
        "fields": fields
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "status": "success",
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }
    
#get_metrics
def get_metrics() -> dict:
    """
    Retrieves WhatsApp messaging statistics for the associated business account.

    Returns:
        dict: Messaging metrics or error details.
    """
    url = f"https://graph.facebook.com/{Config.FACEBOOK_GRAPH_API_VERSION}/{Config.WHATSAPP_PHONE_NUMBER_ID}/insights/message_delivery"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {
            "status": "success",
            "metrics": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }
    
#create_message_template
def create_message_template(template_data: dict) -> dict:
    """
    Creates a new WhatsApp message template (requires Meta approval).

    Args:
        template_data (dict): Structure defining name, category, language, and components.

    Returns:
        dict: Response with template ID or error details.
    """
    url = f"https://graph.facebook.com/{Config.FACEBOOK_GRAPH_API_VERSION}/{Config.WHATSAPP_PHONE_NUMBER_ID}/message_templates"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=template_data)
        response.raise_for_status()
        return {
            "status": "success",
            "template_id": response.json().get("id"),
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }
    
#get_templates
def get_templates() -> dict:
    """
    Retrieves all message templates for the WhatsApp business account.
    
    Returns:
        dict: A list of templates or error info.
    """
    url = f"https://graph.facebook.com/{Config.WHATSAPP_API_VERSION}/{Config.WHATSAPP_PHONE_NUMBER_ID}/message_templates"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {
            "status": "success",
            "templates": response.json().get("data", [])
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }
    
#delete_template
def delete_template(template_name: str) -> dict:
    """
    Deletes a WhatsApp message template by name.

    Args:
        template_name (str): The name of the template to delete.

    Returns:
        dict: Deletion confirmation or error info.
    """
    url = f"https://graph.facebook.com/{Config.WHATSAPP_API_VERSION}/{Config.WHATSAPP_PHONE_NUMBER_ID}/message_templates?name={template_name}"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"
    }

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return {
            "status": "success",
            "message": f"Template '{template_name}' deleted successfully.",
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }
    
#get_template_status
def get_template_status(template_name: str) -> dict:
    """
    Checks the status of a WhatsApp template.

    Args:
        template_name (str): The name of the template.

    Returns:
        dict: Status report or error details.
    """
    url = f"https://graph.facebook.com/{Config.WHATSAPP_API_VERSION}/{Config.WHATSAPP_PHONE_NUMBER_ID}/message_templates"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"
    }

    params = {
        "name": template_name
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        templates = response.json().get("data", [])

        if not templates:
            return {
                "status": "not_found",
                "message": f"Template '{template_name}' not found."
            }

        return {
            "status": "success",
            "template": templates[0]  # Template details
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }
    
#get_conversations
def get_conversations(limit: int = 25) -> dict:
    """
    Retrieves a list of WhatsApp conversations and pricing details.

    Args:
        limit (int): Number of conversations to retrieve (default is 25).

    Returns:
        dict: List of conversations or error details.
    """
    url = f"https://graph.facebook.com/{Config.WHATSAPP_API_VERSION}/{Config.WHATSAPP_PHONE_NUMBER_ID}/conversations"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"
    }
    params = {
        "limit": limit
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return {
            "status": "success",
            "conversations": response.json().get("data", [])
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }
    
#get_conversation_details
def get_conversation_details(conversation_id: str) -> dict:
    """
    Retrieves detailed information about a specific WhatsApp conversation.

    Args:
        conversation_id (str): Unique ID of the conversation.

    Returns:
        dict: Conversation detail object or error information.
    """
    url = f"https://graph.facebook.com/{Config.WHATSAPP_API_VERSION}/{conversation_id}"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {
            "status": "success",
            "conversation": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#get_phone_number_quality
def get_phone_number_quality(phone_number_id: str) -> dict:
    """
    Gets the quality score of a WhatsApp Business phone number.

    Args:
        phone_number_id (str): ID of the WhatsApp Business phone number.

    Returns:
        dict: Quality score object or error information.
    """
    url = f"https://graph.facebook.com/{Config.WHATSAPP_API_VERSION}/{phone_number_id}/quality_rating"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {
            "status": "success",
            "quality": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }
    
#get_message_templates_usage
def get_message_templates_usage(template_name: str) -> dict:
    """
    Tracks the usage of a specific message template.

    Args:
        template_name (str): The name of the WhatsApp message template.

    Returns:
        dict: Usage report or error details.
    """
    url = (
        f"https://graph.facebook.com/{Config.WHATSAPP_API_VERSION}/"
        f"{Config.WHATSAPP_PHONE_NUMBER_ID}/message_templates/name:{template_name}/analytics"
    )
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }
    
#get_blocked_status
def get_blocked_status(phone_number: str) -> dict:
    """
    Attempts to send a test message to detect if the user has blocked the number.

    Args:
        phone_number (str): The recipient's WhatsApp phone number.

    Returns:
        dict: Block status or message delivery error info.
    """
    url = f"{Config.WHATSAPP_BASE_URL}/{Config.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": "🛠️ Checking WhatsApp status... (ignore this test message)"}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        resp_json = response.json()

        if response.status_code == 200:
            return {"status": "sent", "blocked": False, "message_id": resp_json.get("messages", [{}])[0].get("id")}
        else:
            error_code = resp_json.get("error", {}).get("code")
            blocked = error_code == 131047  # Common block code
            return {
                "status": "failed",
                "blocked": blocked,
                "error": resp_json.get("error")
            }
    except requests.RequestException as e:
        return {
            "status": "error",
            "blocked": None,
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }
    
#get_profile_photo
#Not Possible via Cloud API

#get_business_hours
def get_business_hours():
    url = f"https://graph.facebook.com/{Config.WHATSAPP_API_VERSION}/{Config.WHATSAPP_PHONE_NUMBER_ID}/whatsapp_business_profile"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json().get("business_profile", {}).get("business_hours")
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }
    
#update_business_hours
def update_business_hours(data: dict) -> dict:
    url = f"https://graph.facebook.com/{Config.WHATSAPP_API_VERSION}/{Config.WHATSAPP_PHONE_NUMBER_ID}/business_profile"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "business_hours": data.get("hours", [])
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {"status": "success", "response": response.json()}
    except requests.RequestException as e:
        return {"status": "error", "error": str(e), "details": getattr(e.response, "text", None)}

#get_greeting_message
def get_greeting_message() -> dict:
    """
    Retrieves the auto-reply greeting message configured in WhatsApp Business Profile.

    Returns:
        dict: Greeting message text or error.
    """
    url = f"https://graph.facebook.com/{Config.WHATSAPP_API_VERSION}/{Config.WHATSAPP_PHONE_NUMBER_ID}/business_profile"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        greeting = data.get("greeting_message", "No greeting message found.")
        return {"status": "success", "greeting_message": greeting}
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#set_greeting_message
def set_greeting_message(message_text: str) -> dict:
   
    url = f"https://graph.facebook.com/{Config.WHATSAPP_API_VERSION}/{Config.WHATSAPP_PHONE_NUMBER_ID}/business_profile"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "greeting_message": message_text
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {"status": "success", "response": response.json()}
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }

#send_interactive_message
def send_interactive_message(phone_number: str, payload: dict) -> dict:
    url = f"{Config.WHATSAPP_BASE_URL}/{Config.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "interactive",
        "interactive": payload
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        return {
            "status": "sent",
            "message_id": response.json().get("messages", [{}])[0].get("id"),
            "response": response.json()
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": getattr(e.response, "text", None)
        }
