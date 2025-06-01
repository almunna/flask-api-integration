# app/monday/monday_routes.py

from flask import Blueprint, request, jsonify
import os
from app.monday.monday_service import get_boards, create_board, get_workspaces, duplicate_board, delete_board, create_item, get_items_by_ids, update_item_column_value, get_item_column_values, delete_item, change_column_value, get_board_groups, create_group, delete_group, get_users, get_authenticated_user, get_teams, create_update, get_updates, send_notification, get_tags, create_or_get_tag, create_workspace, delete_workspace, get_webhooks, create_webhook, delete_webhook, add_file_to_update_service, get_activity_logs, get_items_assigned, move_item_to_board, move_item_to_group, archive_item, delete_item, get_board_columns, create_column, add_file_to_update


monday_bp = Blueprint("monday", __name__)

@monday_bp.route("/boards", methods=["GET"])
def fetch_boards():
    try:
        ids = request.args.getlist("ids")
        limit = request.args.get("limit", type=int)
        page = request.args.get("page", type=int)
        result = get_boards(ids=ids if ids else None, limit=limit, page=page)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@monday_bp.route("/boards", methods=["POST"])
def create_new_board():
    try:
        data = request.get_json()
        board_name = data.get("board_name")
        board_kind = data.get("board_kind")  # "public" or "private"
        workspace_id = data.get("workspace_id")

        if not all([board_name, board_kind, workspace_id]):
            return jsonify({"error": "Missing required fields"}), 400

        result = create_board(board_name, board_kind, workspace_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#workspaces
@monday_bp.route("/workspaces", methods=["GET"])
def fetch_workspaces():
    try:
        ids = request.args.getlist("ids")
        limit = request.args.get("limit", type=int)
        page = request.args.get("page", type=int)

        result = get_workspaces(
            ids=ids if ids else None,
            limit=limit,
            page=page
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
#duplicate_board
@monday_bp.route("/boards/duplicate", methods=["POST"])
def duplicate_existing_board():
    try:
        data = request.get_json()

        board_id = data.get("board_id")
        duplicate_type = data.get("duplicate_type")  # Required
        board_name = data.get("board_name")  # Optional

        if not all([board_id, duplicate_type]):
            return jsonify({"error": "board_id and duplicate_type are required"}), 400

        result = duplicate_board(board_id, duplicate_type, board_name)
        return jsonify(result)

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#delete_board
@monday_bp.route("/boards/<board_id>", methods=["DELETE"])
def remove_board(board_id):
    try:
        result = delete_board(board_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#items
@monday_bp.route("/items", methods=["GET"])
def fetch_items_by_ids():
    try:
        ids = request.args.getlist("ids")
        limit = request.args.get("limit", type=int)
        page = request.args.get("page", type=int)
        exclude = request.args.get("exclude_nonactive", type=lambda x: x.lower() == "true")
        newest = request.args.get("newest_first", type=lambda x: x.lower() == "true")

        if not ids:
            return jsonify({"error": "You must provide at least one item ID via ?ids=..."}), 400

        result = get_items_by_ids(
            ids=ids,
            limit=limit,
            page=page,
            exclude_nonactive=exclude,
            newest_first=newest
        )
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

#create_item
@monday_bp.route("/items", methods=["POST"])
def create_item_route():
    try:
        data = request.get_json()
        board_id = data.get("board_id")
        item_name = data.get("item_name")
        column_values = data.get("column_values", {})  # Optional dict

        if not board_id or not item_name:
            return jsonify({"error": "board_id and item_name are required"}), 400

        result = create_item(board_id, item_name, column_values)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
#update_item

@monday_bp.route("/items/update", methods=["POST"])
def update_item():
    try:
        data = request.get_json()
        item_id = data["item_id"]
        board_id = data["board_id"]
        column_id = data["column_id"]
        value = data["value"]  # this should be a dict, e.g., {"label": "Done"}

        result = update_item_column_value(item_id, board_id, column_id, value)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#delete_item
@monday_bp.route("/items/<item_id>", methods=["DELETE"])
def delete_item_route(item_id):
    try:
        result = delete_item(item_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#column_values
@monday_bp.route("/items/<item_id>/columns", methods=["GET"])
def get_columns_for_item(item_id):
    try:
        result = get_item_column_values(item_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#change_column_value
@monday_bp.route("/items/change-column-value", methods=["POST"])
def change_item_column_value_route():
    try:
        data = request.get_json()
        item_id = data.get("item_id")
        board_id = data.get("board_id")
        column_id = data.get("column_id")
        value = data.get("value")

        if not all([item_id, board_id, column_id, value]):
            return jsonify({"error": "item_id, board_id, column_id, and value are required"}), 400

        result = change_column_value(item_id, board_id, column_id, value)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#groups
@monday_bp.route("/boards/<board_id>/groups", methods=["GET"])
def get_groups(board_id):
    try:
        result = get_board_groups(board_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#create_group
@monday_bp.route("/groups", methods=["POST"])
def create_group_route():
    try:
        data = request.get_json()
        board_id = data["board_id"]
        group_name = data["group_name"]

        result = create_group(board_id, group_name)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#delete_group
@monday_bp.route("/groups/delete", methods=["POST"])
def delete_group_route():
    try:
        data = request.get_json()
        board_id = data["board_id"]
        group_id = data["group_id"]

        result = delete_group(board_id, group_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#users
@monday_bp.route("/users", methods=["GET"])
def get_users_route():
    try:
        ids = request.args.getlist("ids", type=int)
        limit = request.args.get("limit", type=int)
        page = request.args.get("page", type=int)

        result = get_users(ids=ids or None, limit=limit, page=page)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#me
@monday_bp.route("/me", methods=["GET"])
def get_me():
    try:
        result = get_authenticated_user()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#teams
@monday_bp.route("/teams", methods=["GET"])
def get_teams_route():
    try:
        ids = request.args.getlist("ids")
        result = get_teams(ids=ids if ids else None)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#create_update
@monday_bp.route("/updates", methods=["POST"])
def post_update():
    try:
        data = request.get_json()
        item_id = data.get("item_id")
        body = data.get("body")

        if not item_id or not body:
            return jsonify({"error": "item_id and body are required"}), 400

        result = create_update(item_id=item_id, body=body)
        return jsonify(result)

    except Exception as e:
        print("❌ Error posting update:", str(e))
        return jsonify({"error": str(e)}), 400

#updates
@monday_bp.route("/items/<item_id>/updates", methods=["GET"])
def get_item_updates(item_id):
    try:
        result = get_updates(item_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#notifications
@monday_bp.route("/notifications", methods=["POST"])
def create_notification():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        text = data.get("text")
        target_id = data.get("target_id")  # Board or item ID

        if not user_id or not text or not target_id:
            return jsonify({"error": "user_id, text, and target_id are required"}), 400

        result = send_notification(user_id, text, target_id)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

#tags
@monday_bp.route("/tags", methods=["GET"])
def fetch_tags():
    try:
        ids = request.args.getlist("ids")  # treat as string IDs
        result = get_tags(ids=ids if ids else None)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#create_tag
@monday_bp.route("/tags/create-or-get", methods=["POST"])
def create_or_get_tag_route():
    try:
        data = request.get_json()
        tag_name = data.get("tag_name")
        board_id = data.get("board_id")  # optional

        if not tag_name:
            return jsonify({"error": "tag_name is required"}), 400

        result = create_or_get_tag(tag_name, board_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#Doesn't supported by Monday
# #delete_tag
# @monday_bp.route("/items/<item_id>/tags/clear", methods=["POST"])
# def clear_tags(item_id):
#     try:
#         result = remove_tag_from_item(item_id)
#         return jsonify(result)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

#workspaces
# app/monday/monday_routes.py
@monday_bp.route("/workspaces", methods=["GET"])
def list_workspaces():
    try:
        ids = request.args.getlist("ids")
        limit = int(request.args.get("limit", 25))
        page = int(request.args.get("page", 1))

        # Convert empty list of IDs to None to avoid sending an empty array
        ids = ids if ids else None

        result = get_workspaces(ids, limit, page)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# acreate_workspace

@monday_bp.route("/workspaces/create", methods=["POST"])
def create_workspace_route():
    try:
        data = request.get_json()
        name = data["name"]
        kind = data.get("kind", "open")
        description = data.get("description")
        account_product_id = data.get("account_product_id")  # optional

        result = create_workspace(name, kind, description, account_product_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#delete_workspace
# app/monday/monday_routes.py

@monday_bp.route("/workspaces/delete", methods=["POST"])
def delete_workspace_route():
    try:
        data = request.get_json()
        workspace_id = data["workspace_id"]

        result = delete_workspace(workspace_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#webhook
@monday_bp.route("/webhooks", methods=["POST"])
def create_webhook_route():
    try:
        data = request.get_json()
        result = create_webhook(
            board_id=data["board_id"],
            url=data["url"],
            event=data["event"],
            config=data.get("config")
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@monday_bp.route("/webhooks/<board_id>", methods=["GET"])
def get_webhooks_route(board_id):
    try:
        result = get_webhooks(board_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@monday_bp.route("/webhooks/delete/<webhook_id>", methods=["DELETE"])
def delete_webhook_route(webhook_id):
    try:
        result = delete_webhook(webhook_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

#create_asset
@monday_bp.route("/add-file-to-update", methods=["POST"])
def add_file_to_update_route():
    try:
        update_id = request.form.get("update_id")
        file = request.files.get("file")

        if not update_id or not file:
            return jsonify({"error": "update_id and file are required"}), 400

        result = add_file_to_update_service(update_id, file.stream, file.filename)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#activity log
@monday_bp.route("/activity-logs", methods=["POST"])
def activity_logs():
    try:
        data = request.get_json()
        board_id = data.get("board_id")
        from_date = data.get("from")
        to_date = data.get("to")

        if not board_id or not from_date or not to_date:
            return jsonify({"error": "board_id, from, and to are required"}), 400

        logs = get_activity_logs(board_id, from_date, to_date)
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#items_by_column_values
@monday_bp.route("/items/filter", methods=["POST"])
def get_items_assigned1():
    board_id = request.json.get("board_id")
    return jsonify(get_items_assigned(board_id))


#move_item_to_group
@monday_bp.route("/move-item-to-group", methods=["POST"])
def move_item_to_group_route():
    data = request.json
    item_id = data.get("item_id")
    group_id = data.get("group_id")

    if not item_id or not group_id:
        return jsonify({"error": "item_id and group_id are required"}), 400

    try:
        result = move_item_to_group(item_id, group_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# move_item_to_board
@monday_bp.route("/move-item-to-board", methods=["POST"])
def move_item_to_board_route():
    data = request.json
    item_id = data.get("item_id")
    board_id = data.get("board_id")
    group_id = data.get("group_id")
    columns_mapping = data.get("columns_mapping", [])
    subitems_mapping = data.get("subitems_columns_mapping", [])

    if not item_id or not board_id or not group_id:
        return jsonify({"error": "item_id, board_id, and group_id are required"}), 400

    try:
        result = move_item_to_board(item_id, board_id, group_id, columns_mapping, subitems_mapping)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#archive_item
@monday_bp.route("/archive-item", methods=["POST"])
def archive_item_route():
    data = request.json
    item_id = data.get("item_id")

    if not item_id:
        return jsonify({"error": "item_id is required"}), 400

    try:
        result = archive_item(item_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#delete_group_items
@monday_bp.route("/delete-item", methods=["POST"])
def delete_item_route1():
    data = request.json
    item_id = data.get("item_id")

    if not item_id:
        return jsonify({"error": "item_id is required"}), 400

    try:
        result = delete_item(item_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#get_board_columns
@monday_bp.route("/get-columns/<board_id>", methods=["GET"])
def get_columns_route(board_id):
    try:
        result = get_board_columns(board_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#create_column
@monday_bp.route("/create-column", methods=["POST"])
def create_column_route():
    data = request.json
    board_id = data.get("board_id")
    title = data.get("title")
    column_type = data.get("column_type")
    description = data.get("description", "")

    if not board_id or not title or not column_type:
        return jsonify({"error": "board_id, title, and column_type are required"}), 400

    try:
        result = create_column(board_id, title, column_type, description)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


import tempfile
import os

@monday_bp.route("/upload-file-to-update", methods=["POST"])
def upload_file_to_update_route():
    update_id = request.form.get("update_id")
    file = request.files.get("file")

    if not update_id or not file:
        return jsonify({"error": "update_id and file are required"}), 400

    # Use system temp directory
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)

    try:
        result = add_file_to_update(update_id, file_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
