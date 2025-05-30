from flask import Blueprint, request, jsonify
import requests
from app.config import Config
from app.notion.notion_service import create_notion_page, query_notion_database, list_notion_databases, retrieve_notion_database, query_notion_database_with_params, create_page_in_database, retrieve_page, update_page_properties, append_blocks_to_page, list_block_children, retrieve_block, update_block, list_notion_users, retrieve_notion_user, create_comment, list_comments, create_database, update_database, archive_page, archive_block, restore_page, get_page_property, delete_block, list_database_properties, update_database_properties, duplicate_notion_page, move_page_to_new_parent, update_page_title, update_page_icon, update_page_cover, get_current_user, get_integration_capabilities, relate_pages ,add_tag_to_page, remove_tag_from_page, mark_comment_as_deleted, move_block_to_new_parent, get_template_pages, create_template, add_related_page, list_related_pages, remove_related_page, mention_page_or_user, duplicate_database, archive_database, restore_database, set_page_reminder, remove_page_reminder, get_mock_database_permissions


notion_bp = Blueprint("notion", __name__)

@notion_bp.route('/add', methods=['POST'])
def add_page():
    data = request.get_json()
    title = data.get("title", "Untitled")
    result = create_notion_page(title)
    return jsonify(result)

@notion_bp.route('/query', methods=['GET'])
def query_database():
    result = query_notion_database()
    return jsonify(result)

@notion_bp.route('/search', methods=['GET'])
def search_notion():
    query = request.args.get("query", "")
    object_type = request.args.get("type")  # Optional: page, database, block

    headers = {
        "Authorization": f"Bearer {Config.NOTION_TOKEN}",
        "Notion-Version": Config.NOTION_VERSION,
        "Content-Type": "application/json"
    }

    payload = {"query": query}
    if object_type:
        payload["filter"] = {
            "value": object_type,
            "property": "object"
        }

    response = requests.post("https://api.notion.com/v1/search", headers=headers, json=payload)
    return jsonify(response.json())

#search
@notion_bp.route('/search', methods=['GET'])
def handle_search():
    query = request.args.get("query", "")
    object_type = request.args.get("type")  # page, database, block
    result = search_notion(query, object_type)
    return jsonify(result)

#database list
@notion_bp.route('/databases', methods=['GET'])
def get_databases():
    result = list_notion_databases()
    return jsonify(result)

#databases.retrieve
@notion_bp.route('/databases/<string:database_id>', methods=['GET'])
def get_database_details(database_id):
    result = retrieve_notion_database(database_id)
    return jsonify(result)

#databases.query
@notion_bp.route('/databases/<string:database_id>/query', methods=['POST'])
def query_database_with_filter(database_id):  # ✅ include it here
    data = request.get_json()
    filters = data.get("filter")
    sorts = data.get("sort")
    result = query_notion_database_with_params(database_id, filters, sorts)
    return jsonify(result)

#pages.create
@notion_bp.route('/databases/<string:database_id>/add', methods=['POST'])
def add_page_to_database(database_id):
    data = request.get_json()
    title = data.get("title", "Untitled")
    age = data.get("age", "")

    result = create_page_in_database(database_id, title, age)
    return jsonify(result)

#pages.retrieve
@notion_bp.route('/pages/<string:page_id>', methods=['GET'])
def get_page(page_id):
    result = retrieve_page(page_id)
    return jsonify(result)

#pages.update
@notion_bp.route('/pages/<string:page_id>/update', methods=['PATCH'])
def update_page(page_id):
    data = request.get_json()

    # Optional: simple validation
    if "title" not in data and "age" not in data:
        return jsonify({"error": "Nothing to update"}), 400

    updated_props = {}

    if "title" in data:
        updated_props["Name"] = {
            "title": [{
                "text": {"content": data["title"]}
            }]
        }

    if "age" in data:
        updated_props["age"] = {
            "rich_text": [{
                "text": {"content": data["age"]}
            }]
        }

    result = update_page_properties(page_id, updated_props)
    return jsonify(result)

#blocks.children.append
@notion_bp.route('/pages/<string:page_id>/append-blocks', methods=['PATCH'])
def append_blocks(page_id):
    data = request.get_json()

    # Example: expect a list of blocks in "blocks"
    blocks = data.get("blocks")
    if not blocks:
        return jsonify({"error": "Missing 'blocks' in request body"}), 400

    result = append_blocks_to_page(page_id, blocks)
    return jsonify(result)

#blocks.children.list
@notion_bp.route('/blocks/<string:block_id>/children', methods=['GET'])
def get_block_children(block_id):
    result = list_block_children(block_id)
    return jsonify(result)

#block.retrieve
@notion_bp.route('/blocks/<string:block_id>', methods=['GET'])
def get_block(block_id):
    result = retrieve_block(block_id)
    return jsonify(result)

#block.update
@notion_bp.route('/blocks/<string:block_id>/update', methods=['PATCH'])
def update_block_content(block_id):
    data = request.get_json()

    # Example: expect full JSON block structure (e.g., paragraph, heading)
    if not data:
        return jsonify({"error": "Missing content body"}), 400

    result = update_block(block_id, data)
    return jsonify(result)

#users.list
@notion_bp.route('/users', methods=['GET'])
def get_users():
    result = list_notion_users()
    return jsonify(result)

#users.retrieve
@notion_bp.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    result = retrieve_notion_user(user_id)
    return jsonify(result)

#create comment
@notion_bp.route('/comments', methods=['POST'])
def post_comment():
    data = request.get_json()
    parent_id = data.get("parent_id")
    text = data.get("text")
    is_page = data.get("is_page", True)  # default to page_id

    if not parent_id or not text:
        return jsonify({"error": "Missing parent_id or text"}), 400

    result = create_comment(parent_id, text, is_page)
    return jsonify(result)

#comment list
@notion_bp.route('/comments/<string:block_id>', methods=['GET'])
def get_comments(block_id):
    result = list_comments(block_id)
    return jsonify(result)

#create database
@notion_bp.route('/databases/create', methods=['POST'])
def create_new_database():
    data = request.get_json()
    page_id = data.get("page_id")
    title = data.get("title")
    properties = data.get("properties")

    if not page_id or not title or not properties:
        return jsonify({"error": "Missing page_id, title, or properties"}), 400

    result = create_database(page_id, title, properties)
    return jsonify(result)

#update database
@notion_bp.route('/databases/<string:database_id>/update', methods=['PATCH'])
def update_db(database_id):
    data = request.get_json()
    title = data.get("title")
    properties = data.get("properties")

    if not title and not properties:
        return jsonify({"error": "Provide at least a title or properties to update"}), 400

    result = update_database(database_id, title, properties)
    return jsonify(result)

#page.archive
@notion_bp.route('/pages/<string:page_id>/archive', methods=['PATCH'])
def archive_notion_page(page_id):
    result = archive_page(page_id)
    return jsonify(result)

#block.archive
@notion_bp.route('/blocks/<string:block_id>/archive', methods=['PATCH'])
def archive_notion_block(block_id):
    result = archive_block(block_id)
    return jsonify(result)

#restore page
@notion_bp.route('/pages/<string:page_id>/restore', methods=['PATCH'])
def restore_notion_page(page_id):
    result = restore_page(page_id)
    return jsonify(result)

#pages.properties.retrieve
@notion_bp.route('/pages/<string:page_id>/properties/<string:property_id>', methods=['GET'])
def retrieve_page_property(page_id, property_id):
    result = get_page_property(page_id, property_id)
    return jsonify(result)

#blocks.delete
@notion_bp.route('/blocks/<string:block_id>/delete', methods=['PATCH'])
def archive_block_as_delete(block_id):
    result = delete_block(block_id)
    return jsonify(result)

#databases.properties.list
@notion_bp.route('/databases/<string:database_id>/properties', methods=['GET'])
def get_database_properties(database_id):
    properties = list_database_properties(database_id)
    return jsonify(properties)

#databases.properties.update
@notion_bp.route('/databases/<string:database_id>/properties/update', methods=['PATCH'])
def patch_database_properties(database_id):
    data = request.get_json()
    updated_properties = data.get("properties")
    result = update_database_properties(database_id, updated_properties)
    return jsonify(result)

#pages.duplicate
@notion_bp.route('/pages/<string:page_id>/duplicate', methods=['POST'])
def duplicate_page(page_id):
    result, status = duplicate_notion_page(page_id)
    return jsonify(result), status

#pages.move
@notion_bp.route('/pages/<string:page_id>/move', methods=['PATCH'])
def move_page(page_id):
    data = request.get_json()
    new_parent_id = data.get("new_parent_id")
    result, status = move_page_to_new_parent(page_id, new_parent_id)
    return jsonify(result), status

#page.title.update
@notion_bp.route('/pages/<string:page_id>/title', methods=['PATCH'])
def update_title(page_id):
    data = request.get_json()
    new_title = data.get("new_title")
    result, status = update_page_title(page_id, new_title)
    return jsonify(result), status

#page.icon.update
@notion_bp.route('/pages/<string:page_id>/icon', methods=['PATCH'])
def update_icon(page_id):
    data = request.get_json()
    icon_type = data.get("type")
    value = data.get("value")
    result, status = update_page_icon(page_id, icon_type, value)
    return jsonify(result), status

#page.cover.update
@notion_bp.route('/pages/<string:page_id>/cover', methods=['PATCH'])
def update_cover(page_id):
    data = request.get_json()
    image_url = data.get("image_url")
    if not image_url:
        return jsonify({"error": "Missing 'image_url'"}), 400
    result, status = update_page_cover(page_id, image_url)
    return jsonify(result), status

#user.settings.retrieve
@notion_bp.route('/users/me', methods=['GET'])
def fetch_current_user():
    result, status = get_current_user()
    return jsonify(result), status

#integration.capabilities.list
@notion_bp.route('/capabilities', methods=['GET'])
def fetch_capabilities():
    result, status = get_integration_capabilities()
    return jsonify(result), status

#pages.link.create
@notion_bp.route('/pages/link', methods=['POST'])
def link_pages():
    data = request.json
    source_id = data.get("source_page_id")
    target_id = data.get("target_page_id")
    relation_prop = data.get("relation_property_name")  # Must match Notion schema

    result, status = relate_pages(source_id, relation_prop, target_id)
    return jsonify(result), status

#pages.tags.retrieve
@notion_bp.route('/pages/<string:page_id>/tags', methods=['GET'])
def get_page_tags(page_id):
    from app.notion.notion_service import get_page_tags
    result, status = get_page_tags(page_id)
    return jsonify(result), status

#pages.tags.add
@notion_bp.route('/pages/<string:page_id>/tags/add', methods=['POST'])
def add_tag(page_id):
    data = request.get_json()
    tag_name = data.get("tag")

    if not tag_name:
        return jsonify({"error": "Tag name is required"}), 400

    result, status = add_tag_to_page(page_id, tag_name)
    return jsonify(result), status

#remove tag
@notion_bp.route('/pages/<string:page_id>/tags/remove', methods=['POST'])
def remove_tag(page_id):
    data = request.get_json()
    tag_name = data.get("tag_name")
    if not tag_name:
        return {"error": "Missing tag_name"}, 400
    result, status = remove_tag_from_page(page_id, tag_name)
    return jsonify(result), status

#comments.delete
#noton directy doesn't support delete
@notion_bp.route('/comments/<string:page_id>/mark-deleted', methods=['PATCH'])
def mark_comment_as_deleted_route(page_id):
    result, status = mark_comment_as_deleted(page_id)
    return jsonify(result), status

#move block
@notion_bp.route('/blocks/<string:block_id>/move', methods=['PATCH'])
def move_block(block_id):
    data = request.get_json()
    new_parent_id = data.get("new_parent_id")

    if not new_parent_id:
        return jsonify({"error": "new_parent_id is required"}), 400

    result, status = move_block_to_new_parent(block_id, new_parent_id)
    return jsonify(result), status

#database.templates.list
#Notion's API does not currently support listing database templates
@notion_bp.route("/databases/<string:database_id>/templates", methods=["GET"])
def list_template_pages(database_id):
    result, status = get_template_pages(database_id)
    return jsonify(result), status

#database.templates.create
@notion_bp.route('/databases/<string:database_id>/templates', methods=['POST'])
def create_template_page(database_id):
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")  # Optional

    result, status = create_template(database_id, title, content)
    return jsonify(result), status

#pages.relations.add
@notion_bp.route('/pages/<string:page_id>/relations', methods=['PATCH'])
def add_relation_to_page(page_id):
    data = request.get_json()
    property_name = data.get("property_name")
    related_page_id = data.get("related_page_id")

    result, status = add_related_page(page_id, property_name, related_page_id)
    return jsonify(result), status

#pages.relations.list
@notion_bp.route('/pages/<string:page_id>/relations/<string:relation_property_id>', methods=['GET'])
def get_related_pages(page_id, relation_property_id):
    result, status = list_related_pages(page_id, relation_property_id)
    return jsonify(result), status

#pages.relations.remove
#Notion API doesn't provide a dedicated pages.relations.remove
@notion_bp.route('/pages/<string:page_id>/relations/<string:property_id>/remove', methods=['PATCH'])
def remove_relation(page_id, property_id):
    data = request.get_json()
    related_page_id = data.get("related_page_id")

    if not related_page_id:
        return jsonify({"error": "related_page_id is required"}), 400

    result, status = remove_related_page(page_id, property_id, related_page_id)
    return jsonify(result), status

#page mention
#Notion API does not provide a direct endpoint named pages.mention
@notion_bp.route('/blocks/<string:block_id>/mention', methods=['PATCH'])
def mention_target(block_id):
    data = request.get_json()
    target_id = data.get("target_id")
    target_type = data.get("target_type", "page")  # "page" or "user"

    if not target_id:
        return jsonify({"error": "target_id is required"}), 400

    result, status = mention_page_or_user(block_id, target_id, target_type)
    return jsonify(result), status

#databases.duplicate
#Notion API does not provide a direct endpoint named databases.duplicate
@notion_bp.route('/databases/<string:database_id>/duplicate', methods=['POST'])
def duplicate_db(database_id):
    data = request.get_json()
    new_title = data.get("title", "Copy of Database")
    parent_page_id = data.get("parent_page_id")
    
    result, status = duplicate_database(database_id, parent_page_id, new_title)
    return jsonify(result), status

#databases.delete
#Notion API does not provide a direct endpoint named databases.delete
@notion_bp.route('/databases/<string:database_id>/delete', methods=['PATCH'])
def delete_database(database_id):
    result, status = archive_database(database_id)
    return jsonify(result), status

#databases.restore
#Notion API does not provide a direct endpoint named databases.restore
@notion_bp.route('/databases/<string:database_id>/restore', methods=['PATCH'])
def restore_database_route(database_id):
    result, status = restore_database(database_id)
    return jsonify(result), status

#pages.reminder.set
#Notion API does not provide a direct endpoint named pages.reminder.set
@notion_bp.route('/pages/<string:page_id>/reminder', methods=['PATCH'])
def set_reminder_route(page_id):
    data = request.get_json()
    property_name = data.get("property_name", "Reminder")
    reminder_time = data.get("reminder_time")

    if not reminder_time:
        return jsonify({"error": "reminder_time is required"}), 400

    result, status = set_page_reminder(page_id, property_name, reminder_time)
    return jsonify(result), status

#pages.reminder.remove
#Notion API does not provide a direct endpoint named pages.reminder.remove
@notion_bp.route('/pages/<string:page_id>/reminder/remove', methods=['PATCH'])
def remove_reminder_route(page_id):
    data = request.get_json()
    property_name = data.get("property_name", "Reminder")
    result, status = remove_page_reminder(page_id, property_name)
    return jsonify(result), status

#databases.permissions.get
#Notion API does not provide a direct endpoint named databases.permissions.get
@notion_bp.route('/databases/<string:database_id>/permissions', methods=['GET'])
def get_database_permissions(database_id):
    result, status = get_mock_database_permissions(database_id)
    return jsonify(result), status