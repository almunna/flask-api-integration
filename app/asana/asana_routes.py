from flask import Blueprint, request, jsonify
from app.asana.asana_service import get_user_info, get_user, get_users, get_workspace, get_workspaces, get_projects, get_project, create_project, update_project, delete_project, get_tasks, get_task, create_task, update_task, delete_task, get_subtasks, add_subtask, get_sections, create_section, add_task_to_section, get_project_custom_fields, get_tags, create_tag, add_tag_to_task, remove_tag_from_task, get_comments, create_comment, get_stories, get_attachments, upload_attachment, delete_attachment, mark_task_complete, assign_task, set_due_date, get_teams, get_team_projects, get_team_users, add_favorite_project, list_favorite_projects, remove_favorite_project, duplicate_project, search_tasks

asana_bp = Blueprint("asana", __name__)

@asana_bp.route("/me", methods=["GET"])
def get_me():
    return jsonify(get_user_info())

#get_user
@asana_bp.route("/user/<user_gid>", methods=["GET"])
def fetch_user_by_id(user_gid):
    return jsonify(get_user(user_gid))

#get_users
@asana_bp.route("/users", methods=["GET"])
def fetch_users():
    workspace_gid = request.args.get("workspace_gid")
    if not workspace_gid:
        return jsonify({"error": "workspace_gid is required"}), 400

    return jsonify(get_users(workspace_gid))

#get_workspace
@asana_bp.route("/workspace/<workspace_gid>", methods=["GET"])
def fetch_workspace(workspace_gid):
    return jsonify(get_workspace(workspace_gid))

#get_workspaces
@asana_bp.route("/workspaces", methods=["GET"])
def fetch_workspaces():
    return jsonify(get_workspaces())

#get_projects
@asana_bp.route("/projects", methods=["GET"])
def fetch_projects():
    workspace_gid = request.args.get("workspace_gid")
    if not workspace_gid:
        return jsonify({"error": "workspace_gid is required"}), 400

    return jsonify(get_projects(workspace_gid))

#get_project
@asana_bp.route("/project/<project_gid>", methods=["GET"])
def fetch_project_by_gid(project_gid):
    return jsonify(get_project(project_gid))

#create_project
@asana_bp.route("/project", methods=["POST"])
def create_new_project():
    data = request.get_json()
    workspace_gid = data.get("workspace_gid")
    name = data.get("name")
    notes = data.get("notes")
    team_gid = data.get("team_gid")

    if not workspace_gid or not name:
        return jsonify({"error": "workspace_gid and name are required"}), 400

    return jsonify(create_project(workspace_gid, name, notes, team_gid))

#update_project
@asana_bp.route("/project/<project_gid>", methods=["PUT"])
def update_existing_project(project_gid):
    updates = request.get_json()
    if not updates:
        return jsonify({"error": "Update data is required"}), 400
    return jsonify(update_project(project_gid, updates))

#delete_project
@asana_bp.route("/project/<project_gid>", methods=["DELETE"])
def delete_existing_project(project_gid):
    return jsonify(delete_project(project_gid))

#get_tasks
@asana_bp.route("/project/<project_gid>/tasks", methods=["GET"])
def fetch_tasks_in_project(project_gid):
    return jsonify(get_tasks(project_gid))

#get_task
@asana_bp.route("/task/<task_gid>", methods=["GET"])
def fetch_task_by_id(task_gid):
    return jsonify(get_task(task_gid))

#create_task
@asana_bp.route("/task", methods=["POST"])
def create_new_task():
    data = request.get_json()
    
    required_fields = ["name"]
    if not any(field in data for field in ["workspace", "projects"]):
        return jsonify({"error": "Either workspace or project is required"}), 400
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required field(s): name"}), 400

    return jsonify(create_task(data))

#update_task
@asana_bp.route("/task/<task_gid>", methods=["PUT"])
def update_existing_task(task_gid):
    updates = request.get_json()
    if not updates:
        return jsonify({"error": "Update data is required"}), 400
    return jsonify(update_task(task_gid, updates))

#delete_task
@asana_bp.route("/task/<task_gid>", methods=["DELETE"])
def delete_existing_task(task_gid):
    return jsonify(delete_task(task_gid))

#get_subtasks
@asana_bp.route("/task/<task_gid>/subtasks", methods=["GET"])
def fetch_subtasks(task_gid):
    return jsonify(get_subtasks(task_gid))

#add_subtask
@asana_bp.route("/task/<parent_task_gid>/subtask", methods=["POST"])
def create_subtask(parent_task_gid):
    task_data = request.get_json()
    if not task_data or "name" not in task_data:
        return jsonify({"error": "Subtask 'name' is required"}), 400
    return jsonify(add_subtask(parent_task_gid, task_data))

#get_sections
@asana_bp.route("/project/<project_gid>/sections", methods=["GET"])
def fetch_project_sections(project_gid):
    return jsonify(get_sections(project_gid))
#create_section
@asana_bp.route("/project/<project_gid>/section", methods=["POST"])
def create_project_section(project_gid):
    data = request.get_json()
    section_name = data.get("name")

    if not section_name:
        return jsonify({"error": "Section name is required"}), 400

    return jsonify(create_section(project_gid, section_name))

#add_task_to_section
@asana_bp.route("/section/<section_gid>/add-task", methods=["POST"])
def add_task_to_specific_section(section_gid):
    data = request.get_json()
    task_gid = data.get("task_gid")

    if not task_gid:
        return jsonify({"error": "task_gid is required"}), 400

    return jsonify(add_task_to_section(section_gid, task_gid))

#get_custom_fields
@asana_bp.route("/project/<project_gid>/custom-fields", methods=["GET"])
def fetch_project_custom_fields(project_gid):
    return jsonify(get_project_custom_fields(project_gid))

#get_tags
@asana_bp.route("/workspace/<workspace_gid>/tags", methods=["GET"])
def fetch_workspace_tags(workspace_gid):
    return jsonify(get_tags(workspace_gid))

#create_tag
@asana_bp.route("/workspace/<workspace_gid>/tag", methods=["POST"])
def create_workspace_tag(workspace_gid):
    data = request.get_json()
    tag_name = data.get("name")

    if not tag_name:
        return jsonify({"error": "Tag name is required"}), 400

    return jsonify(create_tag(workspace_gid, tag_name))

#add_tag_to_task
@asana_bp.route("/task/<task_gid>/add-tag", methods=["POST"])
def tag_task(task_gid):
    data = request.get_json()
    tag_gid = data.get("tag_gid")

    if not tag_gid:
        return jsonify({"error": "tag_gid is required"}), 400

    return jsonify(add_tag_to_task(task_gid, tag_gid))

#remove_tag_from_task
@asana_bp.route("/task/<task_gid>/remove-tag", methods=["POST"])
def untag_task(task_gid):
    data = request.get_json()
    tag_gid = data.get("tag_gid")

    if not tag_gid:
        return jsonify({"error": "tag_gid is required"}), 400

    return jsonify(remove_tag_from_task(task_gid, tag_gid))

#get_comments
@asana_bp.route("/task/<task_gid>/comments", methods=["GET"])
def fetch_task_comments(task_gid):
    return jsonify(get_comments(task_gid))

#create_comment
@asana_bp.route("/task/<task_gid>/comment", methods=["POST"])
def add_comment_to_task(task_gid):
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Comment text is required"}), 400

    return jsonify(create_comment(task_gid, text))

#get_stories
@asana_bp.route("/task/<task_gid>/stories", methods=["GET"])
def fetch_task_stories(task_gid):
    return jsonify(get_stories(task_gid))

#get_attachments
@asana_bp.route("/task/<task_gid>/attachments", methods=["GET"])
def fetch_task_attachments(task_gid):
    return jsonify(get_attachments(task_gid))

#upload_attachment
@asana_bp.route("/task/<task_gid>/attachments", methods=["POST"])
def attach_file_to_task(task_gid):
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    return jsonify(upload_attachment(task_gid, file))

#delete_attachment
@asana_bp.route("/attachment/<attachment_gid>", methods=["DELETE"])
def remove_attachment(attachment_gid):
    success = delete_attachment(attachment_gid)
    if success:
        return jsonify({"message": "Attachment deleted successfully."}), 200
    else:
        return jsonify({"error": "Failed to delete attachment."}), 400

#mark_task_complete
@asana_bp.route("/task/<task_gid>/complete", methods=["PUT"])
def complete_task(task_gid):
    return jsonify(mark_task_complete(task_gid))

#assign_task
@asana_bp.route("/task/<task_gid>/assign", methods=["PUT"])
def assign_task_route(task_gid):
    data = request.get_json()
    assignee_gid = data.get("assignee_gid")

    if not assignee_gid:
        return jsonify({"error": "assignee_gid is required"}), 400

    return jsonify(assign_task(task_gid, assignee_gid))

#set_due_date
@asana_bp.route("/task/<task_gid>/due-date", methods=["PUT"])
def update_due_date(task_gid):
    data = request.get_json()
    due_on = data.get("due_on")

    if not due_on:
        return jsonify({"error": "due_on (YYYY-MM-DD) is required"}), 400

    return jsonify(set_due_date(task_gid, due_on))

#get_teams
@asana_bp.route("/organization/<organization_gid>/teams", methods=["GET"])
def list_teams(organization_gid):
    return jsonify(get_teams(organization_gid))

#get_team_projects
@asana_bp.route("/team/<team_gid>/projects", methods=["GET"])
def list_team_projects(team_gid):
    return jsonify(get_team_projects(team_gid))

#get_team_users
@asana_bp.route("/team/<team_gid>/users", methods=["GET"])
def list_team_users(team_gid):
    return jsonify(get_team_users(team_gid))

#favorite_project
@asana_bp.route("/user/<user_gid>/favorites", methods=["POST"])
def add_fav(user_gid):
    data = request.get_json()
    project_gid = data.get("project_gid")
    project_name = data.get("project_name")
    permalink_url = data.get("permalink_url")

    if not all([project_gid, project_name, permalink_url]):
        return jsonify({"error": "project_gid, project_name, and permalink_url required"}), 400

    project = {
        "project_gid": project_gid,
        "project_name": project_name,
        "permalink_url": permalink_url
    }

    return jsonify(add_favorite_project(user_gid, project))

#list_favourit
@asana_bp.route("/user/<user_gid>/favorites", methods=["GET"])
def get_fav(user_gid):
    return jsonify(list_favorite_projects(user_gid))

#unfavorite_project
@asana_bp.route("/user/<user_gid>/favorites/<project_gid>", methods=["DELETE"])
def delete_fav(user_gid, project_gid):
    return jsonify(remove_favorite_project(user_gid, project_gid))

#duplicate_project
@asana_bp.route("/project/<project_gid>/duplicate", methods=["POST"])
def duplicate_project_route(project_gid):
    try:
        result = duplicate_project(project_gid)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#search_tasks
@asana_bp.route("/workspace/<workspace_gid>/search-tasks", methods=["GET"])
def search_tasks_route(workspace_gid):
    filters = request.args.to_dict()
    try:
        result = search_tasks(workspace_gid, filters)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
