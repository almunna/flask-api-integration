from flask import Blueprint, request, jsonify
from app.jira.jira_service import create_issue, list_projects, get_myself, get_users, get_user, get_projects, get_project, get_project_roles, get_issue, create_issue, update_issue, delete_issue, assign_issue, transition_issue, get_transitions, get_issue_comments, add_comment, update_comment, delete_comment, get_issue_attachments, add_attachment, delete_attachment, get_issue_watchers, add_watcher, remove_watcher, get_issue_votes, add_vote, remove_vote, get_issue_worklogs, add_worklog, update_worklog, delete_worklog, get_issue_types, get_issue_types, get_priorities, get_statuses, get_resolutions, search_issues, get_favorite_filters, get_board_issues, get_sprints, get_user_permissions, get_user_notifications


jira_bp = Blueprint("jira_bp", __name__)

@jira_bp.route("/create-issue", methods=["POST"])
def create_jira_issue():
    data = request.json
    project_key = data.get("project_key")
    summary = data.get("summary")
    description = data.get("description")

    if not all([project_key, summary, description]):
        return jsonify({"error": "Missing required fields"}), 400

    result = create_issue(project_key, summary, description)
    return jsonify(result)


#get_myself
@jira_bp.route("/me", methods=["GET"])  # ✅ New route
def get_jira_user_info():
    return jsonify(get_myself())

#get_user
@jira_bp.route("/user/<account_id>", methods=["GET"])
def get_specific_user(account_id):
    return jsonify(get_user(account_id))

#get_users
@jira_bp.route("/users", methods=["GET"])
def search_users():
    query = request.args.get("query", "")
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    return jsonify(get_users(query))

#get_projects
@jira_bp.route("/projects", methods=["GET"])
def fetch_projects():
    return jsonify(get_projects())

#get_project
@jira_bp.route("/project/<project_id_or_key>", methods=["GET"])
def get_project_details(project_id_or_key):
    return jsonify(get_project(project_id_or_key))

##get_project_roles
@jira_bp.route("/project/<project_id_or_key>/roles", methods=["GET"])
def get_project_roles_route(project_id_or_key):
    return jsonify(get_project_roles(project_id_or_key))


#get_issue
@jira_bp.route("/issue/<issue_id_or_key>", methods=["GET"])
def get_issue_details(issue_id_or_key):
    return jsonify(get_issue(issue_id_or_key))

#create_issue
@jira_bp.route("/issue", methods=["POST"])
def create_issue_route():
    data = request.get_json()
    return jsonify(create_issue(data))

#update_issue
@jira_bp.route("/issue/<issue_id_or_key>", methods=["PUT"])
def update_issue_route(issue_id_or_key):
    updates = request.get_json()
    return jsonify(update_issue(issue_id_or_key, updates))

#delete_issue
@jira_bp.route("/issue/<issue_id_or_key>", methods=["DELETE"])
def delete_issue_route(issue_id_or_key):
    return jsonify(delete_issue(issue_id_or_key))

#assign_issue
@jira_bp.route("/issue/<issue_id_or_key>/assign", methods=["PUT"])
def assign_issue_route(issue_id_or_key):
    data = request.get_json()
    account_id = data.get("accountId")

    if not account_id:
        return jsonify({"error": "Missing 'accountId'"}), 400

    return jsonify(assign_issue(issue_id_or_key, account_id))

#transition_issue
@jira_bp.route("/transition-issue", methods=["POST"])
def transition_jira_issue():
    data = request.json
    issue_key = data.get("issue_key")
    transition_id = data.get("transition_id")

    if not issue_key or not transition_id:
        return jsonify({
            "status": "error",
            "message": "Missing required fields: issue_key or transition_id"
        }), 400

    result = transition_issue(issue_key, transition_id)
    return jsonify(result)

#get_transitions
@jira_bp.route("/issue/<issue_id_or_key>/transitions", methods=["GET"])
def get_transitions_route(issue_id_or_key):
    return jsonify(get_transitions(issue_id_or_key))

#get_issue_comments
@jira_bp.route("/issue/<issue_id_or_key>/comments", methods=["GET"])
def get_issue_comments_route(issue_id_or_key):
    return jsonify(get_issue_comments(issue_id_or_key))

#add_comment
@jira_bp.route("/issue/<issue_id_or_key>/comment", methods=["POST"])
def add_comment_route(issue_id_or_key):
    data = request.get_json()
    comment_text = data.get("comment")

    if not comment_text:
        return {"error": "Comment text is required"}, 400

    return jsonify(add_comment(issue_id_or_key, comment_text))

#update_comment
@jira_bp.route("/issue/<issue_id_or_key>/comment/<comment_id>", methods=["PUT"])
def update_comment_route(issue_id_or_key, comment_id):
    data = request.get_json()
    new_body = data.get("comment")

    if not new_body:
        return {"error": "Updated comment text is required"}, 400

    return jsonify(update_comment(issue_id_or_key, comment_id, new_body))

#delete_comment
@jira_bp.route("/issue/<issue_id_or_key>/comment/<comment_id>", methods=["DELETE"])
def delete_comment_route(issue_id_or_key, comment_id):
    return jsonify(delete_comment(issue_id_or_key, comment_id))

#get_issue_attachments
@jira_bp.route("/issue/<issue_id_or_key>/attachments", methods=["GET"])
def get_issue_attachments_route(issue_id_or_key):
    return jsonify(get_issue_attachments(issue_id_or_key))

#add_attachment
@jira_bp.route("/issue/<issue_id_or_key>/attachment", methods=["POST"])
def add_attachment_route(issue_id_or_key):
    if "file" not in request.files:
        return jsonify({"error": "File is required"}), 400

    file = request.files["file"]
    return jsonify(add_attachment(issue_id_or_key, file))

#delete_attachment
@jira_bp.route("/attachment/<attachment_id>", methods=["DELETE"])
def delete_attachment_route(attachment_id):
    return jsonify(delete_attachment(attachment_id))

#get_issue_watchers
@jira_bp.route("/issue/<issue_id_or_key>/watchers", methods=["GET"])
def get_watchers(issue_id_or_key):
    return jsonify(get_issue_watchers(issue_id_or_key))

#add_watcher
@jira_bp.route("/issue/<issue_id_or_key>/watchers", methods=["POST"])
def add_issue_watcher(issue_id_or_key):
    data = request.json
    account_id = data.get("accountId")

    if not account_id:
        return jsonify({"error": "accountId is required"}), 400

    return jsonify(add_watcher(issue_id_or_key, account_id))

#remove_watcher
@jira_bp.route("/issue/<issue_id_or_key>/watchers", methods=["DELETE"])
def remove_issue_watcher(issue_id_or_key):
    data = request.json
    account_id = data.get("accountId")

    if not account_id:
        return jsonify({"error": "accountId is required"}), 400

    return jsonify(remove_watcher(issue_id_or_key, account_id))

#get_issue_votes
@jira_bp.route("/issue/<issue_id_or_key>/votes", methods=["GET"])
def get_votes_on_issue(issue_id_or_key):
    return jsonify(get_issue_votes(issue_id_or_key))

#add_vote
@jira_bp.route("/issue/<issue_id_or_key>/vote", methods=["POST"])
def add_issue_vote(issue_id_or_key):
    return jsonify(add_vote(issue_id_or_key))

#remove_vote
@jira_bp.route("/issue/<issue_id_or_key>/vote", methods=["DELETE"])
def remove_vote_from_issue(issue_id_or_key):
    return jsonify(remove_vote(issue_id_or_key))

#get_issue_worklogs
@jira_bp.route("/issue/<issue_id_or_key>/worklogs", methods=["GET"])
def get_issue_worklogs_route(issue_id_or_key):
    return jsonify(get_issue_worklogs(issue_id_or_key))

#add_worklog
@jira_bp.route("/issue/<issue_id_or_key>/worklog", methods=["POST"])
def add_worklog_to_issue(issue_id_or_key):
    data = request.json
    time_spent = data.get("timeSpent")
    comment = data.get("comment")
    started = data.get("started")

    if not time_spent:
        return jsonify({"error": "timeSpent is required"}), 400

    result = add_worklog(issue_id_or_key, time_spent, comment, started)
    return jsonify(result)

#update_worklog
@jira_bp.route("/issue/<issue_id_or_key>/worklog/<worklog_id>", methods=["PUT"])
def update_worklog_entry(issue_id_or_key, worklog_id):
    data = request.json
    time_spent = data.get("timeSpent")
    comment = data.get("comment")
    started = data.get("started")

    result = update_worklog(issue_id_or_key, worklog_id, time_spent, comment, started)
    return jsonify(result)

#delete_worklog
@jira_bp.route("/issue/<issue_id_or_key>/worklog/<worklog_id>", methods=["DELETE"])
def delete_worklog_entry(issue_id_or_key, worklog_id):
    return jsonify(delete_worklog(issue_id_or_key, worklog_id))

#get_issue_types
@jira_bp.route("/issue-types", methods=["GET"])
def list_issue_types():
    return jsonify(get_issue_types())

#get_priorities
@jira_bp.route("/priorities", methods=["GET"])
def list_priorities():
    return jsonify(get_priorities())

#get_statuses
@jira_bp.route("/statuses", methods=["GET"])
def list_statuses():
    return jsonify(get_statuses())

#get_resolutions
@jira_bp.route("/resolutions", methods=["GET"])
def list_resolutions():
    return jsonify(get_resolutions())

#search_issues
@jira_bp.route("/search", methods=["POST"])
def search_issues_route():
    jql_query = request.json.get("jql")
    max_results = request.json.get("max_results", 50)
    return jsonify(search_issues(jql_query, max_results))

#get_favorites_filters
@jira_bp.route("/filters/favorites", methods=["GET"])
def get_favorite_filters_route():
    return jsonify(get_favorite_filters())

#get_board_issues
@jira_bp.route("/board/<board_id>/issues", methods=["GET"])
def get_board_issues_route(board_id):
    return jsonify(get_board_issues(board_id))

#get_sprints
@jira_bp.route("/board/<board_id>/sprints", methods=["GET"])
def get_sprints_route(board_id):
    return jsonify(get_sprints(board_id))

#get_user_permissions
@jira_bp.route("/permissions", methods=["GET"])
def get_permissions():
    return jsonify(get_user_permissions())

#get_user_notifications
@jira_bp.route("/notifications", methods=["GET"])
def get_notifications():
    try:
        return jsonify({"notifications": get_user_notifications()})
    except Exception as e:
        return jsonify({
            "message": "Failed to retrieve notifications",
            "details": str(e),
            "status": "error",
            "status_code": 500
        })
