from flask import Blueprint, jsonify, request
from app.salesforce.salesforce_service import get_authenticated_user_info, get_limits, get_objects, describe_object, query_salesforce, query_more, search_salesforce, create_record, retrieve_record, update_record, delete_record, upsert_record, get_deleted_records, get_updated_records, create_attachment, retrieve_attachment, delete_attachment, get_recent_items, get_my_profile, get_roles, get_groups, get_object_layout, execute_anonymous_apex, get_org_info, list_record_types, get_picklist_values, create_task, update_task, delete_task, create_event, update_event, delete_event, list_appointments, send_email, send_mass_email, get_email_status, create_case, update_case, delete_case, create_lead, update_lead, convert_lead, create_opportunity, update_opportunity, delete_opportunity, get_reports, run_report, get_dashboards, get_dashboard_data



salesforce_bp = Blueprint("salesforce", __name__)

#get_user_info
@salesforce_bp.route("/user-info", methods=["GET"])
def user_info():
    return jsonify(get_authenticated_user_info())

#get_limits
@salesforce_bp.route("/limits", methods=["GET"])
def limits():
    return jsonify(get_limits())

#get_objects
@salesforce_bp.route("/objects", methods=["GET"])
def objects():
    return jsonify(get_objects())

#describe_object
@salesforce_bp.route("/describe-object", methods=["GET"])
def describe_object_route():
    object_name = request.args.get("object_name")
    return jsonify(describe_object(object_name))

#query
from app.config import Config
@salesforce_bp.route("/query", methods=["GET"])
def query_route():
    soql = request.args.get("q")
    return jsonify(query_salesforce(soql))

#queryMore
@salesforce_bp.route("/query-more", methods=["GET"])
def query_more_route():
    next_url = request.args.get("next_url")
    return jsonify(query_more(next_url))

#search
@salesforce_bp.route("/search", methods=["GET"])
def search_route():
    sosl_query = request.args.get("q")  # e.g., q=FIND {munna}
    return jsonify(search_salesforce(sosl_query))

#create_record
@salesforce_bp.route("/create-record/<object_name>", methods=["POST"])
def create_record_route(object_name):
    data = request.get_json()
    return jsonify(create_record(object_name, data))

#retrieve_record
@salesforce_bp.route("/retrieve-record", methods=["GET"])
def retrieve_record_route():
    object_name = request.args.get("object_name")
    record_id = request.args.get("record_id")
    return jsonify(retrieve_record(object_name, record_id))

#update_record
@salesforce_bp.route("/update-record", methods=["PATCH"])
def update_record_route():
    data = request.json
    object_name = data.get("object_name")
    record_id = data.get("record_id")
    field_values = data.get("field_values")

    return jsonify(update_record(object_name, record_id, field_values))

#delete_record
@salesforce_bp.route("/delete-record", methods=["DELETE"])
def delete_record_route():
    object_name = request.args.get("object_name")
    record_id = request.args.get("record_id")
    return jsonify(delete_record(object_name, record_id))

#upsert_record
@salesforce_bp.route("/upsert-record", methods=["PATCH"])
def upsert_record_route():
    body = request.get_json()
    object_name = body.get("object_name")
    external_id_field = body.get("external_id_field")
    external_id_value = body.get("external_id_value")
    data = body.get("data")
    return jsonify(upsert_record(object_name, external_id_field, external_id_value, data))

#get_deleted
@salesforce_bp.route("/deleted-records", methods=["GET"])
def deleted_records_route():
    object_name = request.args.get("object_name")
    start_datetime = request.args.get("start")
    end_datetime = request.args.get("end")
    return jsonify(get_deleted_records(object_name, start_datetime, end_datetime))

#get_updated
@salesforce_bp.route("/updated", methods=["GET"])
def updated_records_route():
    object_name = request.args.get("object_name")
    start = request.args.get("start")
    end = request.args.get("end")
    return jsonify(get_updated_records(object_name, start, end))

#create_attachment
@salesforce_bp.route("/attachment", methods=["POST"])
def upload_attachment_route():
    parent_id = request.form.get("parent_id")
    name = request.form.get("name")
    file = request.files.get("file")

    if not file:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400

    return jsonify(create_attachment(parent_id, name, file.read()))

#retrieve_attachment
@salesforce_bp.route("/attachment/<attachment_id>", methods=["GET"])
def get_attachment(attachment_id):
    return jsonify(retrieve_attachment(attachment_id))

#delete_attachment
@salesforce_bp.route("/delete-attachment/<attachment_id>", methods=["DELETE"])
def delete_attachment_route(attachment_id):
    return jsonify(delete_attachment(attachment_id))

#get_recent_items
@salesforce_bp.route("/recent-items", methods=["GET"])
def recent_items():
    return jsonify(get_recent_items())

#get_user_list
@salesforce_bp.route("/users", methods=["GET"])
def get_users_route():
    from app.salesforce.salesforce_service import get_user_list
    return jsonify(get_user_list())

#get_profile
@salesforce_bp.route("/my-profile", methods=["GET"])
def my_profile_route():
    return jsonify(get_my_profile())

#get_roles
@salesforce_bp.route("/get-roles", methods=["GET"])
def get_roles_route():
    return jsonify(get_roles())

#get_groups
@salesforce_bp.route("/get-groups", methods=["GET"])
def get_groups_route():
    return jsonify(get_groups())

#get_object_layout
@salesforce_bp.route("/get-object-layout", methods=["GET"])
def get_object_layout_route():
    object_name = request.args.get("object_name")
    record_type_id = request.args.get("record_type_id")  # optional
    return jsonify(get_object_layout(object_name, record_type_id))


#execute_anonymous_apex
@salesforce_bp.route("/execute-anonymous-apex", methods=["POST"])
def execute_anonymous_apex_route():
    body = request.get_json()
    apex_code = body.get("apex_code")
    return jsonify(execute_anonymous_apex(apex_code))

#get_org_info
@salesforce_bp.route("/get-org-info", methods=["GET"])
def get_organization_info():
    result = get_org_info()
    return jsonify(result)

#list_record_types
@salesforce_bp.route("/list-record-types", methods=["GET"])
def list_record_types_route():
    from flask import request
    object_name = request.args.get("object_name")

    if not object_name:
        return jsonify({
            "status": "error",
            "message": "Missing 'object_name' parameter",
            "code": 400
        })

    result = list_record_types(object_name)
    return jsonify(result)

#get_picklist_values
@salesforce_bp.route("/get-picklist-values", methods=["GET"])
def get_picklist_values_route():
    from flask import request
    object_name = request.args.get("object_name")
    field_name = request.args.get("field_name")

    if not object_name or not field_name:
        return jsonify({
            "status": "error",
            "message": "Missing 'object_name' or 'field_name' parameter",
            "code": 400
        })

    result = get_picklist_values(object_name, field_name)
    return jsonify(result)

#create_task
@salesforce_bp.route("/create-task", methods=["POST"])
def create_task_route():
    from flask import request
    task_data = request.get_json()

    if not task_data:
        return jsonify({
            "status": "error",
            "message": "Missing task data in request body",
            "code": 400
        })

    result = create_task(task_data)
    return jsonify(result)

#update_task
@salesforce_bp.route("/update-task/<record_id>", methods=["PATCH"])
def update_task_route(record_id):
    """
    Endpoint to update a Salesforce Task record.
    Example: PATCH /api/salesforce/update-task/00Tf6000000HabmEAC
    """
    update_data = request.json
    result = update_task(record_id, update_data)
    return jsonify(result)

#delete_task
@salesforce_bp.route("/delete-task", methods=["DELETE"])
def delete_task_route():
    from flask import request
    record_id = request.args.get("record_id")

    if not record_id:
        return jsonify({
            "status": "error",
            "message": "Missing 'record_id' parameter",
            "code": 400
        })

    result = delete_task(record_id)
    return jsonify(result)

#create_event
@salesforce_bp.route("/create-event", methods=["POST"])
def create_event_route():
    data = request.get_json()
    if not data:
        return jsonify({
            "status": "error",
            "message": "Missing request body",
            "code": 400
        })
    
    result = create_event(data)
    return jsonify(result)

#update
@salesforce_bp.route("/update-event/<record_id>", methods=["PATCH"])
def update_event_route(record_id):
    update_data = request.json
    return jsonify(update_event(record_id, update_data))

#delete_event
@salesforce_bp.route("/delete-event", methods=["DELETE"])
def delete_event_route():
    from flask import request
    record_id = request.args.get("record_id")

    if not record_id:
        return jsonify({
            "status": "error",
            "message": "Missing 'record_id' parameter",
            "code": 400
        })

    result = delete_event(record_id)
    return jsonify(result)

#list_appointments
@salesforce_bp.route("/list-appointments", methods=["GET"])
def list_appointments_route():
    from flask import request
    user_id = request.args.get("user_id")  # optional

    result = list_appointments(user_id)
    return jsonify(result)

#send_email
@salesforce_bp.route("/send-email", methods=["POST"])
def send_email_route():
    from flask import request, jsonify

    data = request.json
    required_fields = ["emailBody", "emailAddresses", "subject"]

    if not all(field in data for field in required_fields):
        return jsonify({
            "status": "error",
            "message": "Missing required email fields: emailBody, emailAddresses, subject",
            "code": 400
        })

    result = send_email(data)
    return jsonify(result)

#send_mass_email
@salesforce_bp.route("/send-mass-email", methods=["POST"])
def send_mass_email_route():
    data = request.get_json()
    to_addresses = data.get("toAddresses")
    subject = data.get("subject")
    body = data.get("body")

    if not to_addresses or not subject or not body:
        return jsonify({
            "status": "error",
            "message": "Missing required fields: toAddresses, subject, or body",
            "code": 400
        })

    result = send_mass_email(to_addresses, subject, body)
    return jsonify(result)

#get_email_status
@salesforce_bp.route("/get-email-status", methods=["GET"])
def get_email_status_route():
    from flask import request, jsonify
    email_id = request.args.get("email_id")

    if not email_id:
        return jsonify({
            "status": "error",
            "message": "Missing 'email_id' parameter",
            "code": 400
        })

    result = get_email_status(email_id)
    return jsonify(result)

#create_case
@salesforce_bp.route("/create-case", methods=["POST"])
def create_case_route():
    from flask import request
    data = request.json

    if not data:
        return jsonify({
            "status": "error",
            "message": "Missing request body with case data",
            "code": 400
        })

    result = create_case(data)
    return jsonify(result)

#update_case
@salesforce_bp.route("/update-case", methods=["PATCH"])
def update_case_route():
    data = request.json
    record_id = data.get("record_id")
    update_fields = data.get("update_fields")

    if not record_id or not update_fields:
        return jsonify({
            "status": "error",
            "message": "Missing 'record_id' or 'update_fields'",
            "code": 400
        })

    result = update_case(record_id, update_fields)
    return jsonify(result)

#delete_case
@salesforce_bp.route("/delete-case/<record_id>", methods=["DELETE"])
def delete_case_route(record_id):
    if not record_id:
        return jsonify({
            "status": "error",
            "message": "Missing 'record_id' parameter",
            "code": 400
        })

    result = delete_case(record_id)
    return jsonify(result)

#create_lead
@salesforce_bp.route("/create-lead", methods=["POST"])
def create_lead_route():
    lead_data = request.json
    if not lead_data:
        return jsonify({
            "status": "error",
            "message": "Missing lead data",
            "code": 400
        })

    result = create_lead(lead_data)
    return jsonify(result)

#update_lead
@salesforce_bp.route("/update-lead", methods=["PATCH"])
def update_lead_route():
    from flask import request, jsonify
    data = request.get_json()

    record_id = data.get("record_id")
    field_values = data.get("field_values")

    if not record_id or not isinstance(field_values, dict):
        return jsonify({
            "status": "error",
            "message": "Missing or invalid 'record_id' or 'field_values'",
            "code": 400
        })

    result = update_lead(record_id, field_values)
    return jsonify(result)

#convert_lead
@salesforce_bp.route("/convert-lead/<lead_id>", methods=["POST"])
def convert_lead_route(lead_id):
    conversion_data = request.json or {}
    return jsonify(convert_lead(lead_id, conversion_data))

#create_opportunity
@salesforce_bp.route("/create-opportunity", methods=["POST"])
def create_opportunity_route():
    from flask import request

    field_values = request.get_json()
    if not field_values:
        return jsonify({
            "status": "error",
            "message": "Missing opportunity field values",
            "code": 400
        })

    result = create_opportunity(field_values)
    return jsonify(result)

#update_opportunity
@salesforce_bp.route("/update-opportunity", methods=["POST"])
def update_opportunity_route():
    from flask import request
    data = request.get_json()

    record_id = data.get("record_id")
    field_values = data.get("field_values")

    if not record_id or not field_values:
        return jsonify({
            "status": "error",
            "message": "Missing 'record_id' or 'field_values'",
            "code": 400
        })

    result = update_opportunity(record_id, field_values)
    return jsonify(result)

#delete_opportunity
@salesforce_bp.route("/delete-opportunity", methods=["DELETE"])
def delete_opportunity_route():
    from flask import request
    record_id = request.args.get("record_id")

    if not record_id:
        return jsonify({
            "status": "error",
            "message": "Missing 'record_id' parameter",
            "code": 400
        })

    result = delete_opportunity(record_id)
    return jsonify(result)

#get_reports
@salesforce_bp.route("/get-reports", methods=["GET"])
def get_reports_route():
    result = get_reports()
    return jsonify(result)

#run_report
@salesforce_bp.route("/run-report", methods=["GET"])
def run_report_route():
    from flask import request
    report_id = request.args.get("report_id")

    if not report_id:
        return jsonify({
            "status": "error",
            "message": "Missing 'report_id' parameter",
            "code": 400
        })

    result = run_report(report_id)
    return jsonify(result)

#get_dashboards
@salesforce_bp.route("/get-dashboards", methods=["GET"])
def get_dashboards_route():
    result = get_dashboards()
    return jsonify(result)

#get_dashboard_data
@salesforce_bp.route("/dashboard/<dashboard_id>", methods=["GET"])
def get_dashboard_data_route(dashboard_id):
    return jsonify(get_dashboard_data(dashboard_id))