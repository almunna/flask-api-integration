from flask import Blueprint, request, jsonify
from app.linkedin_sales.linkedin_sales_service import get_sales_profile, get_sales_contact_info, get_company_profile,  search_leads, search_accounts, get_lead_recommendations, get_account_recommendations, create_lead_list, get_lead_lists, add_lead_to_list, remove_lead_from_list, get_leads_in_list, create_account_list, get_account_lists, add_account_to_list, remove_account_from_list, get_accounts_in_list, sync_lead_to_crm, get_crm_sync_status, get_engagement_metrics, get_inmail_quota, send_inmail, get_sent_inmails, track_inmail_response, get_smart_links, create_smart_link, get_smart_link_clicks, get_team_link_insights, get_sales_preferences, update_sales_preferences, get_saved_searches, run_saved_search, delete_saved_search, follow_lead, unfollow_lead, follow_account, unfollow_account, get_alerts, dismiss_alert, get_usage_analytics


linkedin_sales_bp = Blueprint("linkedin_sales", __name__)

@linkedin_sales_bp.route("/sales-profile", methods=["GET"])
def sales_profile():
    instance_id = request.args.get("instance_id")
    partner = request.args.get("partner")
    record_id = request.args.get("record_id")

    if not all([instance_id, partner, record_id]):
        return jsonify({
            "error": "Missing required query params: instance_id, partner, record_id"
        }), 400

    result = get_sales_profile(instance_id, partner, record_id)
    return jsonify(result)

#get_sales_contact_info
from app.linkedin_sales.linkedin_sales_service import get_sales_contact_info

@linkedin_sales_bp.route("/sales-contact-info", methods=["GET"])
def sales_contact_info():
    member_id = request.args.get("member_id")
    if not member_id:
        return jsonify({"error": "Missing required query param: member_id"}), 400

    result = get_sales_contact_info(member_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_company_profile
@linkedin_sales_bp.route("/company-profile", methods=["GET"])
def company_profile():
    company_id_or_urn = request.args.get("company_id_or_urn")
    if not company_id_or_urn:
        return jsonify({"error": "Missing required query param: company_id_or_urn"}), 400

    result = get_company_profile(company_id_or_urn)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

# search_leads
@linkedin_sales_bp.route("/search-leads", methods=["POST"])
def lead_search():
    search_params = request.get_json()

    if not search_params:
        return jsonify({"error": "Missing search parameters in JSON body"}), 400

    result = search_leads(search_params)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#search_accounts
@linkedin_sales_bp.route("/search-accounts", methods=["POST"])
def account_search():
    search_params = request.get_json()

    if not search_params:
        return jsonify({"error": "Missing search parameters in JSON body"}), 400

    result = search_accounts(search_params)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_lead_recommendations
@linkedin_sales_bp.route("/lead-recommendations", methods=["POST"])
def lead_recommendations():
    data = request.get_json()
    account_id = data.get("account_id") if data else None

    if not account_id:
        return jsonify({"error": "Missing required field: account_id"}), 400

    result = get_lead_recommendations(account_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_account_recommendations
@linkedin_sales_bp.route("/account-recommendations", methods=["POST"])
def account_recommendations():
    data = request.get_json()
    user_id = data.get("user_id") if data else None

    if not user_id:
        return jsonify({"error": "Missing required field: user_id"}), 400

    result = get_account_recommendations(user_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#create_lead_list
@linkedin_sales_bp.route("/create-lead-list", methods=["POST"])
def create_lead_list_route():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")

    if not name:
        return jsonify({"error": "Missing required field: name"}), 400

    result = create_lead_list(name, description)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_lead_lists
@linkedin_sales_bp.route("/lead-lists", methods=["GET"])
def lead_lists():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing required query param: user_id"}), 400

    result = get_lead_lists(user_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#add_lead_to_list
@linkedin_sales_bp.route("/add-lead-to-list", methods=["POST"])
def add_lead():
    data = request.get_json()
    lead_id = data.get("lead_id")
    list_id = data.get("list_id")

    if not all([lead_id, list_id]):
        return jsonify({"error": "Missing required fields: lead_id and list_id"}), 400

    result = add_lead_to_list(lead_id, list_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#remove_lead_from_list
@linkedin_sales_bp.route("/remove-lead-from-list", methods=["DELETE"])
def remove_lead():
    data = request.get_json()
    lead_id = data.get("lead_id")
    list_id = data.get("list_id")

    if not all([lead_id, list_id]):
        return jsonify({"error": "Missing required fields: lead_id and list_id"}), 400

    result = remove_lead_from_list(lead_id, list_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_leads_in_list
@linkedin_sales_bp.route("/get-leads-in-list", methods=["GET"])
def leads_in_list():
    list_id = request.args.get("list_id")
    if not list_id:
        return jsonify({"error": "Missing required query param: list_id"}), 400

    result = get_leads_in_list(list_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#create_account_list
@linkedin_sales_bp.route("/create-account-list", methods=["POST"])
def create_account():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if not name or not description:
        return jsonify({"error": "Missing required fields: name and description"}), 400

    result = create_account_list(name, description)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_account_lists
@linkedin_sales_bp.route("/get-account-lists", methods=["GET"])
def fetch_account_lists():
    user_id = request.args.get("user_id")  # Optional for mock/debug
    result = get_account_lists(user_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#add_account_to_list
@linkedin_sales_bp.route("/add-account-to-list", methods=["POST"])
def add_account():
    data = request.get_json()
    account_id = data.get("account_id")
    list_id = data.get("list_id")

    if not account_id or not list_id:
        return jsonify({"error": "Missing required fields: account_id and list_id"}), 400

    result = add_account_to_list(account_id, list_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#remove_account_from_list
@linkedin_sales_bp.route("/remove-account-from-list", methods=["DELETE"])
def remove_account():
    data = request.get_json()
    account_id = data.get("account_id")
    list_id = data.get("list_id")

    if not account_id or not list_id:
        return jsonify({"error": "Missing required fields: account_id and list_id"}), 400

    result = remove_account_from_list(account_id, list_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_accounts_in_list
@linkedin_sales_bp.route("/get-accounts-in-list", methods=["GET"])
def get_accounts():
    list_id = request.args.get("list_id")

    if not list_id:
        return jsonify({"error": "Missing required query param: list_id"}), 400

    result = get_accounts_in_list(list_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#sync_lead_to_crm
@linkedin_sales_bp.route("/sync-lead-to-crm", methods=["POST"])
def sync_lead():
    data = request.get_json()
    lead_id = data.get("lead_id")
    crm_payload = data.get("crm_payload")

    if not lead_id or not crm_payload:
        return jsonify({"error": "Missing required lead_id or crm_payload"}), 400

    result = sync_lead_to_crm(lead_id, crm_payload)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_crm_sync_status
@linkedin_sales_bp.route("/crm-sync-status", methods=["GET"])
def crm_sync_status():
    lead_id = request.args.get("lead_id")

    if not lead_id:
        return jsonify({"error": "Missing required query param: lead_id"}), 400

    result = get_crm_sync_status(lead_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_engagement_metrics
@linkedin_sales_bp.route("/engagement-metrics", methods=["GET"])
def engagement_metrics():
    lead_id = request.args.get("lead_id")

    if not lead_id:
        return jsonify({"error": "Missing required query param: lead_id"}), 400

    result = get_engagement_metrics(lead_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_inmail_quota
@linkedin_sales_bp.route("/inmail-quota", methods=["GET"])
def inmail_quota():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing required query param: user_id"}), 400

    result = get_inmail_quota(user_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#send_inmail
@linkedin_sales_bp.route("/send-inmail", methods=["POST"])
def send_inmail_route():
    data = request.get_json()
    lead_id = data.get("lead_id")
    subject = data.get("subject")
    body = data.get("body")

    if not all([lead_id, subject, body]):
        return jsonify({"error": "Missing required fields: lead_id, subject, body"}), 400

    result = send_inmail(lead_id, subject, body)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_sent_inmails
@linkedin_sales_bp.route("/sent-inmails", methods=["GET"])
def sent_inmails():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing required query param: user_id"}), 400

    result = get_sent_inmails(user_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#track_inmail_response
@linkedin_sales_bp.route("/inmail-response", methods=["GET"])
def inmail_response():
    message_id = request.args.get("message_id")

    if not message_id:
        return jsonify({"error": "Missing required query param: message_id"}), 400

    result = track_inmail_response(message_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_smart_links
@linkedin_sales_bp.route("/smart-links", methods=["GET"])
def smart_links():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing required query param: user_id"}), 400

    result = get_smart_links(user_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#create_smart_link
@linkedin_sales_bp.route("/smart-links", methods=["POST"])
def create_smart_link_route():
    data = request.get_json()
    name = data.get("name")
    target_url = data.get("target_url")

    if not name or not target_url:
        return jsonify({"error": "Missing required fields: name, target_url"}), 400

    result = create_smart_link(name, target_url)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_smart_link_clicks
@linkedin_sales_bp.route("/smart-links/<link_id>/clicks", methods=["GET"])
def smart_link_clicks(link_id):
    result = get_smart_link_clicks(link_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_team_link_insights
@linkedin_sales_bp.route("/team-link-insights", methods=["GET"])
def team_link_insights():
    team_id = request.args.get("team_id")
    result = get_team_link_insights(team_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_sales_preferences
@linkedin_sales_bp.route("/sales-preferences", methods=["GET"])
def sales_preferences():
    user_id = request.args.get("user_id")
    result = get_sales_preferences(user_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#update_sales_preferences
@linkedin_sales_bp.route("/sales-preferences", methods=["POST"])
def update_preferences():
    data = request.get_json()
    user_id = data.get("user_id")
    preferences = data.get("preferences")

    result = update_sales_preferences(user_id, preferences)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_saved_searches
@linkedin_sales_bp.route("/saved-searches", methods=["GET"])
def saved_searches():
    user_id = request.args.get("user_id")
    result = get_saved_searches(user_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#run_saved_search
@linkedin_sales_bp.route("/run-saved-search", methods=["GET"])
def run_saved_search_route():
    search_id = request.args.get("search_id")
    result = run_saved_search(search_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#delete_saved_search
@linkedin_sales_bp.route("/delete-saved-search", methods=["DELETE"])
def delete_saved_search_route():
    search_id = request.args.get("search_id")
    result = delete_saved_search(search_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#follow_lead
@linkedin_sales_bp.route("/follow-lead", methods=["POST"])
def follow_lead_route():
    data = request.get_json()
    lead_id = data.get("lead_id") if data else None

    result = follow_lead(lead_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#unfollow_lead
@linkedin_sales_bp.route("/unfollow-lead", methods=["POST"])
def unfollow_lead_route():
    data = request.get_json()
    lead_id = data.get("lead_id") if data else None

    result = unfollow_lead(lead_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#follow_account
@linkedin_sales_bp.route("/follow-account", methods=["POST"])
def follow_account_route():
    data = request.get_json()
    account_id = data.get("account_id") if data else None

    result = follow_account(account_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#unfollow_account
@linkedin_sales_bp.route("/unfollow-account", methods=["POST"])
def unfollow_account_route():
    data = request.get_json()
    account_id = data.get("account_id") if data else None

    result = unfollow_account(account_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_alerts
@linkedin_sales_bp.route("/alerts", methods=["GET"])
def get_alerts_route():
    user_id = request.args.get("user_id")
    result = get_alerts(user_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#dismiss_alert
@linkedin_sales_bp.route("/dismiss-alert", methods=["POST"])
def dismiss_alert_route():
    data = request.get_json()
    alert_id = data.get("alert_id") if data else None

    result = dismiss_alert(alert_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200

#get_usage_analytics
@linkedin_sales_bp.route("/usage-analytics", methods=["GET"])
def get_usage_analytics_route():
    user_id = request.args.get("user_id")

    result = get_usage_analytics(user_id)
    return jsonify(result), result.get("error", 200) if isinstance(result.get("error"), int) else 200
