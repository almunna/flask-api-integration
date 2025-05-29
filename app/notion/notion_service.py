import os
import requests
from app.config import Config

NOTION_TOKEN = Config.NOTION_TOKEN
NOTION_VERSION = Config.NOTION_VERSION
DATABASE_ID = Config.NOTION_DATABASE_ID
NOTION_API_URL = "https://api.notion.com/v1"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json"
}

def create_notion_page(title: str):
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": { "database_id": DATABASE_ID },
        "properties": {
            "Name": {
                "title": [{
                    "text": { "content": title }
                }]
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def query_notion_database():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    return response.json()

#search
def search_notion(query="", object_type=None):
    url = "https://api.notion.com/v1/search"
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

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#database list 
def list_notion_databases():
    url = "https://api.notion.com/v1/search"
    payload = {
        "filter": {
            "property": "object",
            "value": "database"
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#databases.retrieve
def retrieve_notion_database(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}"
    response = requests.get(url, headers=headers)
    return response.json()

#databases.query
def query_notion_database_with_params(database_id, filters=None, sorts=None):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    payload = {}
    if filters:
        payload["filter"] = filters
    if sorts:
        payload["sorts"] = sorts

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#pages.create
def create_page_in_database(database_id, title, age_value):
    url = "https://api.notion.com/v1/pages"

    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [{
                    "text": {"content": title}
                }]
            },
            "age": {
                "rich_text": [{
                    "text": {"content": age_value}
                }]
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#pages.retrieve
def retrieve_page(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.get(url, headers=headers)
    return response.json()

#pages.update
def update_page_properties(page_id, updated_properties):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": updated_properties
    }

    response = requests.patch(url, headers=headers, json=payload)
    return response.json()

#blocks.children.append
def append_blocks_to_page(page_id, blocks):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    payload = {
        "children": blocks
    }

    response = requests.patch(url, headers=headers, json=payload)
    return response.json()

#blocks.children.list
def list_block_children(block_id):
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    response = requests.get(url, headers=headers)
    return response.json()

#block.retrieve
def retrieve_block(block_id):
    url = f"https://api.notion.com/v1/blocks/{block_id}"
    response = requests.get(url, headers=headers)
    return response.json()

#block.update
def update_block(block_id, new_content):
    url = f"https://api.notion.com/v1/blocks/{block_id}"
    response = requests.patch(url, headers=headers, json=new_content)
    return response.json()

#users.list
def list_notion_users():
    url = "https://api.notion.com/v1/users"
    response = requests.get(url, headers=headers)
    return response.json()

#users.retrieve
def retrieve_notion_user(user_id):
    url = f"https://api.notion.com/v1/users/{user_id}"
    response = requests.get(url, headers=headers)
    return response.json()

#create comment
def create_comment(parent_id, comment_text, is_page=True):
    url = "https://api.notion.com/v1/comments"
    parent_key = "page_id" if is_page else "block_id"
    
    payload = {
        "parent": {
            parent_key: parent_id
        },
        "rich_text": [
            {
                "type": "text",
                "text": {
                    "content": comment_text
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#comment list
def list_comments(block_id):
    url = f"https://api.notion.com/v1/comments?block_id={block_id}"
    response = requests.get(url, headers=headers)
    return response.json()

#create database
def create_database(parent_page_id, title, properties):
    url = "https://api.notion.com/v1/databases"
    
    payload = {
        "parent": {
            "type": "page_id",
            "page_id": parent_page_id
        },
        "title": [
            {
                "type": "text",
                "text": {
                    "content": title
                }
            }
        ],
        "properties": properties
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

#update database
def update_database(database_id, title=None, properties=None):
    url = f"https://api.notion.com/v1/databases/{database_id}"

    payload = {}
    if title:
        payload["title"] = [
            {
                "type": "text",
                "text": {
                    "content": title
                }
            }
        ]
    if properties:
        payload["properties"] = properties

    response = requests.patch(url, headers=headers, json=payload)
    return response.json()

#page.archive
def archive_page(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = { "archived": True }
    response = requests.patch(url, headers=headers, json=payload)
    return response.json()

#block.archive
def archive_block(block_id):
    url = f"https://api.notion.com/v1/blocks/{block_id}"
    payload = { "archived": True }
    response = requests.patch(url, headers=headers, json=payload)
    return response.json()

#restore page
def restore_page(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = { "archived": False }
    response = requests.patch(url, headers=headers, json=payload)
    return response.json()

#pages.properties.retrieve
def get_page_property(page_id, property_id):
    url = f"https://api.notion.com/v1/pages/{page_id}/properties/{property_id}"
    response = requests.get(url, headers=headers)
    return response.json()

#blocks.delete
def delete_block(block_id):
    url = f"https://api.notion.com/v1/blocks/{block_id}"
    payload = { "archived": True }
    response = requests.patch(url, headers=headers, json=payload)
    return response.json()

##databases.properties.list
def list_database_properties(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}"
    response = requests.get(url, headers=headers)
    return response.json().get("properties", {})

#databases.properties.update
def update_database_properties(database_id, updated_properties):
    url = f"https://api.notion.com/v1/databases/{database_id}"
    payload = { "properties": updated_properties }
    response = requests.patch(url, headers=headers, json=payload)
    return response.json()

#pages.duplicate
def duplicate_notion_page(page_id):
    # Step 1: Retrieve original page details
    page_url = f"https://api.notion.com/v1/pages/{page_id}"
    page_resp = requests.get(page_url, headers=headers)
    if page_resp.status_code != 200:
        return {"error": "Failed to retrieve original page"}, page_resp.status_code

    page_data = page_resp.json()
    parent = page_data.get("parent")
    properties = page_data.get("properties")

    # Optional: Modify title to show it's a duplicate
    if "Name" in properties and "title" in properties["Name"]:
        original_title = properties["Name"]["title"][0]["text"]["content"]
        properties["Name"]["title"][0]["text"]["content"] = f"{original_title} (Copy)"

    # Step 2: Create new page with same properties
    create_url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": parent,
        "properties": properties
    }

    create_resp = requests.post(create_url, headers=headers, json=payload)
    return create_resp.json(), create_resp.status_code

#pages.move
def move_page_to_new_parent(page_id, new_parent_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "parent": {
            "type": "page_id",
            "page_id": new_parent_id
        }
    }
    response = requests.patch(url, headers=headers, json=payload)
    return response.json(), response.status_code

#page.title.update
def update_page_title(page_id, new_title):
    url = f"{NOTION_API_URL}/pages/{page_id}"
    payload = {
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": new_title
                        }
                    }
                ]
            }
        }
    }
    res = requests.patch(url, headers=headers, json=payload)
    return res.json(), res.status_code

#page.icon.update
def update_page_icon(page_id, icon_type, value):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    
    if icon_type == "emoji":
        icon = {
            "type": "emoji",
            "emoji": value
        }
    elif icon_type == "external":
        icon = {
            "type": "external",
            "external": { "url": value }
        }
    else:
        return {"error": "Invalid icon_type. Use 'emoji' or 'external'."}, 400

    res = requests.patch(
        url,
        headers=headers,
        json={"icon": icon}
    )
    return res.json(), res.status_code

#page.cover.update
def update_page_cover(page_id, image_url):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "cover": {
            "type": "external",
            "external": {
                "url": image_url
            }
        }
    }
    response = requests.patch(url, headers=headers, json=payload)
    return response.json(), response.status_code

#user.settings.retrieve
def get_current_user():
    url = "https://api.notion.com/v1/users/me"
    response = requests.get(url, headers=headers)
    return response.json(), response.status_code

#integration.capabilities.list
def get_integration_capabilities():
    url = "https://api.notion.com/v1/search"
    payload = {
        "sort": {
            "direction": "descending",
            "timestamp": "last_edited_time"
        },
        "page_size": 10
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json(), response.status_code

#pages.link.create
def relate_pages(source_page_id, relation_property_name, target_page_id):
    url = f"https://api.notion.com/v1/pages/{source_page_id}"
    payload = {
        "properties": {
            relation_property_name: {
                "relation": [{"id": target_page_id}]
            }
        }
    }

    response = requests.patch(url, headers=headers, json=payload)
    return response.json(), response.status_code

#databases.views.list
def list_all_databases_with_filter_and_sort(filter_obj=None, sort_obj=None):
    url = "https://api.notion.com/v1/search"

    payload = {
        "filter": {
            "value": "database",
            "property": "object"
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    if not response.ok:
        return data, response.status_code

    results = data.get("results", [])

    # Optional: Apply filter manually
    if filter_obj:
        for key, value in filter_obj.items():
            results = [
                db for db in results
                if db.get("properties", {}).get(key, {}).get("name", "") == value
            ]

    # Optional: Sort manually
    if sort_obj:
        sort_key = sort_obj.get("key")
        reverse = sort_obj.get("order", "asc").lower() == "desc"
        results = sorted(
            results,
            key=lambda db: db.get("properties", {}).get(sort_key, {}).get("name", ""),
            reverse=reverse
        )

    return {"results": results}, 200

#pages.tags.retrieve
def get_page_tags(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.get(url, headers=headers)

    if not response.ok:
        return response.json(), response.status_code

    data = response.json()
    tags = []

    for key, prop in data.get("properties", {}).items():
        if prop["type"] in ["multi_select", "select"] and key.lower() == "tags":
            if prop["type"] == "multi_select":
                tags = [t["name"] for t in prop["multi_select"]]
            elif prop["type"] == "select":
                tags = [prop["select"]["name"]] if prop["select"] else []

    return {"tags": tags}, 200

#pages.tags.add
def add_tag_to_page(page_id, tag_name):
    # Step 1: Get the page
    page_url = f"https://api.notion.com/v1/pages/{page_id}"
    page_res = requests.get(page_url, headers=headers)
    if not page_res.ok:
        return page_res.json(), page_res.status_code

    page_data = page_res.json()
    properties = page_data.get("properties", {})

    # Step 2: Find the multi_select property
    tag_prop_name = None
    for key, value in properties.items():
        if value["type"] == "multi_select":
            tag_prop_name = key
            break

    if not tag_prop_name:
        return {"error": "No multi_select property found"}, 400

    existing_tags = properties[tag_prop_name].get("multi_select", [])
    tag_names = [t["name"] for t in existing_tags]

    # Step 3: Add tag if not already present
    if tag_name not in tag_names:
        existing_tags.append({"name": tag_name})

    # Step 4: Patch page
    update_url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            tag_prop_name: {
                "multi_select": existing_tags
            }
        }
    }

    patch_res = requests.patch(update_url, headers=headers, json=payload)
    return patch_res.json(), patch_res.status_code

#remove tag
def remove_tag_from_page(page_id, tag_name):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    headers = {
        "Authorization": f"Bearer {Config.NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    # Get existing page data to find Tags property
    response = requests.get(url, headers=headers)
    if not response.ok:
        return {"error": "Page not found"}, 404

    page_data = response.json()
    tags_prop = None

    for prop_name, prop in page_data.get("properties", {}).items():
        if prop["type"] == "multi_select":
            tags_prop = prop_name
            break

    if not tags_prop:
        return {"error": "No multi_select property found"}, 400

    # Remove the specified tag
    current_tags = page_data["properties"][tags_prop]["multi_select"]
    new_tags = [tag for tag in current_tags if tag["name"] != tag_name]

    payload = {
        "properties": {
            tags_prop: {
                "multi_select": new_tags
            }
        }
    }

    update_response = requests.patch(url, json=payload, headers=headers)
    return update_response.json(), update_response.status_code

#comments.delete
#noton directy doesn't support delete
def mark_comment_as_deleted(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            "Status": {
                "select": {
                    "name": "Deleted"
                }
            }
        }
    }

    response = requests.patch(url, headers=headers, json=payload)
    return response.json(), response.status_code

#move block
def move_block_to_new_parent(block_id, new_parent_id):
    # Step 1: Get existing block
    block_data = retrieve_block(block_id)
    if "object" not in block_data:
        return {"error": "Invalid block"}, 400

    # Step 2: Recreate block under new parent
    block_type = block_data.get("type")
    block_content = block_data.get(block_type)

    if not block_content:
        return {"error": "Block content missing"}, 400

    new_block = {
        "object": "block",
        "type": block_type,
        block_type: block_content
    }

    append_resp = append_blocks_to_page(new_parent_id, [new_block])

    # Step 3: Archive original block
    archive_resp = archive_block(block_id)

    return {"moved": append_resp, "archived": archive_resp}, 200

#database.templates.list
#Notion's API does not currently support listing database templates
def get_template_pages(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    payload = {
        "filter": {
            "property": "Type",
            "rich_text": {
                "equals": "Template"
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json(), response.status_code

#database.templates.create
def create_template(database_id, template_title, content_blocks=None):
    url = "https://api.notion.com/v1/pages"
    
    payload = {
        "parent": { "database_id": database_id },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": template_title
                        }
                    }
                ]
            },
            "Type": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Template"
                        }
                    }
                ]
            }
        }
    }

    if content_blocks:
        payload["children"] = content_blocks

    response = requests.post(url, headers=headers, json=payload)
    return response.json(), response.status_code

#pages.relations.add
def add_related_page(page_id, relation_property_name, related_page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            relation_property_name: {
                "relation": [{"id": related_page_id}]
            }
        }
    }

    response = requests.patch(url, headers=headers, json=payload)
    return response.json(), response.status_code

#pages.relations.list
def list_related_pages(page_id, relation_property_id):
    url = f"https://api.notion.com/v1/pages/{page_id}/properties/{relation_property_id}"
    response = requests.get(url, headers=headers)

    if not response.ok:
        return response.json(), response.status_code

    data = response.json()
    related_ids = [rel["id"] for rel in data.get("results", []) if "id" in rel]

    related_pages = []
    for rel_id in related_ids:
        page_res = requests.get(f"https://api.notion.com/v1/pages/{rel_id}", headers=headers)
        if page_res.ok:
            related_pages.append(page_res.json())

    return {"related_pages": related_pages}, 200

#pages.relations.remove
#Notion API doesn't provide a dedicated pages.relations.remove
def remove_related_page(page_id, property_id, related_page_id_to_remove):
    # Step 1: Get current related pages
    prop_url = f"https://api.notion.com/v1/pages/{page_id}/properties/{property_id}"
    prop_res = requests.get(prop_url, headers=headers)

    if not prop_res.ok:
        return prop_res.json(), prop_res.status_code

    current_relations = prop_res.json().get("results", [])
    updated_relations = [
        {"id": rel["id"]}
        for rel in current_relations
        if rel["id"] != related_page_id_to_remove
    ]

    # Step 2: Patch with updated list
    patch_url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            property_id: {
                "relation": updated_relations
            }
        }
    }

    patch_res = requests.patch(patch_url, headers=headers, json=payload)
    return patch_res.json(), patch_res.status_code

#page mention
#Notion API does not provide a direct endpoint named pages.mention
def mention_page_or_user(block_id, target_id, target_type="page"):
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"

    if target_type == "page":
        mention = {
            "type": "mention",
            "mention": {
                "type": "page",
                "page": {
                    "id": target_id
                }
            }
        }
    elif target_type == "user":
        mention = {
            "type": "mention",
            "mention": {
                "type": "user",
                "user": {
                    "id": target_id
                }
            }
        }
    else:
        return {"error": "Invalid target_type. Use 'page' or 'user'"}, 400

    payload = {
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        mention
                    ]
                }
            }
        ]
    }

    response = requests.patch(url, headers=headers, json=payload)
    return response.json(), response.status_code

#databases.duplicate
#Notion API does not provide a direct endpoint named databases.duplicate
def duplicate_database(original_db_id, parent_page_id, new_title):
    # Step 1: Get the original database
    retrieve_url = f"https://api.notion.com/v1/databases/{original_db_id}"
    response = requests.get(retrieve_url, headers=headers)
    if not response.ok:
        return response.json(), response.status_code

    original_data = response.json()
    original_properties = original_data.get("properties", {})

    # Step 2: Prepare the new database creation payload
    create_url = "https://api.notion.com/v1/databases"
    payload = {
        "parent": {
            "type": "page_id",
            "page_id": parent_page_id
        },
        "title": [
            {
                "type": "text",
                "text": {
                    "content": new_title
                }
            }
        ],
        "properties": original_properties
    }

    # Step 3: Create the new database
    create_resp = requests.post(create_url, headers=headers, json=payload)
    return create_resp.json(), create_resp.status_code

#databases.delete
#Notion API does not provide a direct endpoint named databases.delete
def archive_database(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}"
    payload = {
        "archived": True
    }
    response = requests.patch(url, headers=headers, json=payload)
    return response.json(), response.status_code

#databases.restore
#Notion API does not provide a direct endpoint named databases.restore
def restore_database(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}"
    payload = {
        "archived": False
    }
    response = requests.patch(url, headers=headers, json=payload)
    return response.json(), response.status_code

#pages.reminder.set
#Notion API does not provide a direct endpoint named pages.reminder.set
def set_page_reminder(page_id, property_name, reminder_time):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            property_name: {
                "date": {
                    "start": reminder_time  # ISO 8601 format: "2025-06-01T10:00:00Z"
                }
            }
        }
    }
    response = requests.patch(url, headers=headers, json=payload)
    return response.json(), response.status_code

#pages.reminder.remove
#Notion API does not provide a direct endpoint named pages.reminder.remove
def remove_page_reminder(page_id, property_name="Reminder"):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            property_name: {
                "date": None
            }
        }
    }

    response = requests.patch(url, headers=headers, json=payload)
    return response.json(), response.status_code

#databases.permissions.get
#Notion API does not provide a direct endpoint named databases.permissions.get
# Mock database permissions (you can replace this with a real database later)
MOCK_DATABASE_PERMISSIONS = {
    "db1-id": [
        {"user_id": "user1", "role": "editor"},
        {"user_id": "user2", "role": "viewer"}
    ],
    "db2-id": [
        {"user_id": "user3", "role": "admin"}
    ]
}

def get_mock_database_permissions(database_id):
    if database_id in MOCK_DATABASE_PERMISSIONS:
        return {
            "database_id": database_id,
            "permissions": MOCK_DATABASE_PERMISSIONS[database_id]
        }, 200
    return {"error": "Database not found or permissions not set"}, 404
