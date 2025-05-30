
from flask import Blueprint, request, jsonify
from app.clickup import clickup_service as cs

clickup_bp = Blueprint("clickup", __name__)

# get_user
@clickup_bp.route("/user", methods=["GET"])
def get_user():
    return jsonify(cs.get_user())

#get_teams
@clickup_bp.route("/teams", methods=["GET"])
def get_teams():
    return jsonify(cs.get_teams())

# get_spaces
@clickup_bp.route("/spaces/<team_id>", methods=["GET"])
def get_spaces(team_id):
    return jsonify(cs.get_spaces(team_id))
#get_folders
@clickup_bp.route("/folders/<space_id>", methods=["GET"])
def get_folders(space_id):
    return jsonify(cs.get_folders(space_id))

#get_lists
@clickup_bp.route("/lists/<folder_id>", methods=["GET"])
def get_lists(folder_id):
    return jsonify(cs.get_lists(folder_id))

# get_tasks
@clickup_bp.route("/tasks/<list_id>", methods=["GET"])
def get_tasks(list_id):
    return jsonify(cs.get_tasks(list_id))

#get_task
@clickup_bp.route("/task/<task_id>", methods=["GET"])
def get_task(task_id):
    return jsonify(cs.get_task(task_id))

# create_task
@clickup_bp.route("/task/<list_id>/create", methods=["POST"])
def create_task(list_id):
    return jsonify(cs.create_task(list_id, request.json))

#update_task
@clickup_bp.route("/task/<task_id>/update", methods=["PUT"])
def update_task(task_id):
    return jsonify(cs.update_task(task_id, request.json))

#delete_task
@clickup_bp.route("/task/<task_id>/delete", methods=["DELETE"])
def delete_task(task_id):
    return jsonify(cs.delete_task(task_id))

# get_task_comments
@clickup_bp.route("/task/<task_id>/comments", methods=["GET"])
def get_task_comments(task_id):
    return jsonify(cs.get_task_comments(task_id))

#add_task_comment
@clickup_bp.route("/task/<task_id>/comment", methods=["POST"])
def add_task_comment(task_id):
    return jsonify(cs.add_task_comment(task_id, request.json))

#update_comment
@clickup_bp.route("/comment/<comment_id>", methods=["PUT"])
def update_comment(comment_id):
    return jsonify(cs.update_comment(comment_id, request.json))

#delete_comment
@clickup_bp.route("/comment/<comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    return jsonify(cs.delete_comment(comment_id))

# get_custom_fields
@clickup_bp.route("/list/<list_id>/custom_fields", methods=["GET"])
def get_custom_fields(list_id):
    return jsonify(cs.get_custom_fields(list_id))

#add_custom_field_to_task
@clickup_bp.route("/task/<task_id>/custom_field/<field_id>", methods=["POST"])
def add_custom_field_to_task(task_id, field_id):
    return jsonify(cs.add_custom_field_to_task(task_id, field_id, request.json.get("value")))

#remove_custom_field_from_task
@clickup_bp.route("/task/<task_id>/custom_field/<field_id>", methods=["DELETE"])
def remove_custom_field_from_task(task_id, field_id):
    return jsonify(cs.remove_custom_field_from_task(task_id, field_id))

# get_checklists
@clickup_bp.route("/task/<task_id>/checklists", methods=["GET"])
def get_checklists(task_id):
    return jsonify(cs.get_checklists(task_id))

#create_checklist
@clickup_bp.route("/task/<task_id>/checklist", methods=["POST"])
def create_checklist(task_id):
    return jsonify(cs.create_checklist(task_id, request.json))

#add_checklist_item
@clickup_bp.route("/checklist/<checklist_id>/item", methods=["POST"])
def add_checklist_item(checklist_id):
    return jsonify(cs.add_checklist_item(checklist_id, request.json))

#update_checklist_item
@clickup_bp.route("/checklist/<checklist_id>/item/<item_id>", methods=["PUT"])
def update_checklist_item(checklist_id, item_id):
    return jsonify(cs.update_checklist_item(checklist_id, item_id, request.json))

#delete_checklist_item
@clickup_bp.route("/checklist/<checklist_id>/item/<item_id>", methods=["DELETE"])
def delete_checklist_item(checklist_id, item_id):
    return jsonify(cs.delete_checklist_item(checklist_id, item_id))

# get_tags_from_task
@clickup_bp.route("/task/<task_id>/tags", methods=["GET"])
def get_tags_from_task(task_id):
    return jsonify(cs.get_tags_from_task(task_id))


# clickup_routes.py
@clickup_bp.route("/task/<task_id>/tag", methods=["POST"])
def add_tag_to_task(task_id):
    tag_data = request.json.get("tag")
    return jsonify(cs.add_tag_to_task(task_id, tag_data))


#remove_tag_from_task
@clickup_bp.route("/task/<task_id>/tag/<tag_name>", methods=["DELETE"])
def remove_tag_from_task(task_id, tag_name):
    return jsonify(cs.remove_tag_from_task(task_id, tag_name))


# get_time_entries(
@clickup_bp.route("/task/<task_id>/time_entries", methods=["GET"])
def get_time_entries(task_id):
    return jsonify(cs.get_time_entries(task_id))

#create_time_entry
@clickup_bp.route("/task/<task_id>/time_entry", methods=["POST"])
def create_time_entry(task_id):
    return jsonify(cs.create_time_entry(task_id, request.json))

#simulate_delete_time_entry
@clickup_bp.route("/time_entry/delete_tag/<task_id>", methods=["POST"])
def simulate_delete_time_entry(task_id):
    result = cs.add_deleted_tag_to_task(task_id)
    return jsonify(result), result.get("status_code", 200)


# get_goal
@clickup_bp.route("/goal/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    return jsonify(cs.get_goal(goal_id))

#get_goals
@clickup_bp.route("/goals/<team_id>", methods=["GET"])
def get_goals(team_id):
    return jsonify(cs.get_goals(team_id))

#create_goal
@clickup_bp.route("/goal/<team_id>", methods=["POST"])
def create_goal(team_id):
    return jsonify(cs.create_goal(team_id, request.json))

#update_goal
@clickup_bp.route("/goal/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    return jsonify(cs.update_goal(goal_id, request.json))

#delete_goal
@clickup_bp.route("/goal/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    if not goal_id or len(goal_id.strip()) < 3:
        return jsonify({"error": "Invalid goal_id format"}), 400

    result = cs.delete_goal(goal_id)
    return jsonify(result), result.get("status_code", 200)

#get_notifications
#not available in clickup
@clickup_bp.route("/notifications", methods=["GET"])
def get_notifications():
    return jsonify(cs.get_notifications())

#get_task_time_in_status
@clickup_bp.route("/task/<task_id>/time_in_status", methods=["GET"])
def get_task_time_in_status(task_id):
    return jsonify(cs.get_task_time_in_status(task_id))

#get_permissions
#not available in checkup
@clickup_bp.route("/permissions", methods=["GET"])
def get_permissions():
    return jsonify(cs.get_permissions())

#get_shared_with_me
#not available on clickup
@clickup_bp.route("/shared/<team_id>", methods=["GET"])
def get_shared_with_me(team_id):
    return jsonify(cs.get_shared_with_me(team_id))

# get_task_dependencies
@clickup_bp.route("/task/<task_id>/dependencies", methods=["GET"])
def get_task_dependencies(task_id):
    return jsonify(cs.get_task_dependencies(task_id))

#add_dependency
@clickup_bp.route("/task/<task_id>/dependency", methods=["POST"])
def add_dependency(task_id):
    data = request.json  # expects: { "depends_on": "<other_task_id>" }
    depends_on_id = data.get("depends_on")
    if not depends_on_id:
        return jsonify({"error": "Missing 'depends_on' in request body"}), 400

    return jsonify(cs.add_task_dependency(task_id, depends_on_id))

#remove_dependency
@clickup_bp.route("/task/<task_id>/dependency", methods=["DELETE"])
def remove_dependency(task_id):
    data = request.json  # expects: { "depends_on": "<task_id>" }
    depends_on_id = data.get("depends_on")
    if not depends_on_id:
        return jsonify({"error": "Missing 'depends_on' in request body"}), 400

    return jsonify(cs.remove_task_dependency(task_id, depends_on_id))


#get_workspace_members
@clickup_bp.route("/workspace/members", methods=["GET"])
def get_workspace_members():
    return jsonify(cs.get_workspace_members())

#get_list_members
@clickup_bp.route("/list/<list_id>/members", methods=["GET"])
def get_list_members(list_id):
    return jsonify(cs.get_list_members(list_id))

#assign_task
@clickup_bp.route("/task/<task_id>/assign", methods=["POST"])
def assign_task(task_id):
    data = request.json  # expects: { "user_id": <int> }
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id in request body"}), 400

    return jsonify(cs.assign_task(task_id, user_id))

#set_due_date
@clickup_bp.route("/task/<task_id>/due_date", methods=["PUT"])
def set_due_date(task_id):
    return jsonify(cs.set_due_date(task_id, request.json.get("due_date")))

#get_team_settings
@clickup_bp.route("/team/<team_id>/settings", methods=["GET"])
def get_team_settings(team_id):
    return jsonify(cs.get_team_settings(team_id))
