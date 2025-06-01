from app.config import Config
import requests
import json
import os

# 🔁 Shared function for headers
def monday_headers():
    return {
        "Authorization": Config.MONDAY_API_KEY,
        "Content-Type": "application/json"
    }

# 📋 Get boards
def get_boards(ids=None, limit=None, page=None):
    query = """
    query ($ids: [ID!], $limit: Int, $page: Int) {
      boards(ids: $ids, limit: $limit, page: $page) {
        id
        name
        board_kind
        state
        owner {
          id
          name
        }
      }
    }
    """

    variables = {}
    if ids:
        variables["ids"] = ids
    if limit is not None:
        variables["limit"] = limit
    if page is not None:
        variables["page"] = page

    payload = {
        "query": query,
        "variables": variables or {}
    }

    print("🔍 PAYLOAD SENT TO MONDAY:")
    print(payload)

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    print("🔍 MONDAY RESPONSE TEXT:")
    print(response.text)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#create_board
# app/monday/monday_service.py

def create_board(board_name, board_kind, workspace_id):
    query = """
    mutation ($board_name: String!, $board_kind: BoardKind!, $workspace_id: ID!) {
      create_board(board_name: $board_name, board_kind: $board_kind, workspace_id: $workspace_id) {
        id
        name
        board_kind
        workspace_id
      }
    }
    """

    variables = {
        "board_name": board_name,
        "board_kind": board_kind,  # "public" or "private"
        "workspace_id": str(workspace_id)  # 👈 Ensure it's a string
    }

    payload = {
        "query": query,
        "variables": variables
    }

    print("📤 CREATE BOARD PAYLOAD:")
    print(payload)

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    print("📥 CREATE BOARD RESPONSE:")
    print(response.text)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#workspaces

def get_workspaces(ids=None, limit=None, page=None):
    query = """
    query ($ids: [ID!], $limit: Int, $page: Int) {
      workspaces(ids: $ids, limit: $limit, page: $page) {
        id
        name
        kind
        description
      }
    }
    """

    variables = {}
    if ids:
        variables["ids"] = ids
    if limit is not None:
        variables["limit"] = limit
    if page is not None:
        variables["page"] = page

    payload = {
        "query": query,
        "variables": variables or {}
    }

    print("📤 GET WORKSPACES PAYLOAD:")
    print(payload)

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    print("📥 WORKSPACES RESPONSE:")
    print(response.text)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#duplicate_board
def duplicate_board(board_id, duplicate_type, board_name=None):
    # Validate enum type
    valid_types = [
        "duplicate_board_with_structure",
        "duplicate_board_with_pulses",
        "duplicate_board_with_pulses_and_updates"
    ]
    if duplicate_type not in valid_types:
        raise ValueError("Invalid duplicate_type value")

    # Build GraphQL mutation (raw enum, string ID)
    query = """
    mutation {
      duplicate_board(
        board_id: %s,
        duplicate_type: %s%s
      ) {
        board {
          id
          name
          board_kind
          workspace_id
        }
      }
    }
    """ % (
        json.dumps(str(board_id)),
        duplicate_type,
        f', board_name: "{board_name}"' if board_name else ''
    )

    payload = {"query": query}

    print("📤 DUPLICATE BOARD PAYLOAD:")
    print(payload)

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    print("📥 MONDAY RESPONSE:")
    print(response.text)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#delete_board
def delete_board(board_id):
    query = """
    mutation {
      delete_board(board_id: %s) {
        id
      }
    }
    """ % json.dumps(str(board_id))  # ensure ID is stringified

    payload = {"query": query}

    print("📤 DELETE BOARD PAYLOAD:")
    print(payload)

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    print("📥 DELETE BOARD RESPONSE:")
    print(response.text)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#items
def get_items_by_ids(ids, limit=None, exclude_nonactive=None, newest_first=None, page=None):
    if not ids:
        raise ValueError("The 'ids' argument is required for querying items.")

    query = """
    query ($ids: [ID!], $limit: Int, $exclude_nonactive: Boolean, $newest_first: Boolean, $page: Int) {
      items(ids: $ids, limit: $limit, exclude_nonactive: $exclude_nonactive, newest_first: $newest_first, page: $page) {
        id
        name
        creator_id
        created_at
        updated_at
        url
        board {
          id
          name
        }
      }
    }
    """

    variables = {
        "ids": ids,
        "limit": limit,
        "exclude_nonactive": exclude_nonactive,
        "newest_first": newest_first,
        "page": page
    }

    # remove None values
    variables = {k: v for k, v in variables.items() if v is not None}

    payload = {
        "query": query,
        "variables": variables
    }

    print("📤 ITEMS QUERY PAYLOAD:")
    print(payload)

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    print("📥 RESPONSE:")
    print(response.text)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#create_item
def create_item(board_id, item_name, column_values=None, group_id=None):
    query = """
    mutation ($board_id: ID!, $item_name: String!, $group_id: String, $column_values: JSON) {
      create_item(board_id: $board_id, item_name: $item_name, group_id: $group_id, column_values: $column_values) {
        id
        name
        board {
          id
          name
        }
      }
    }
    """

    variables = {
        "board_id": str(board_id),
        "item_name": item_name
    }

    if group_id:
        variables["group_id"] = group_id

    if column_values:
        # Must be a JSON-encoded string
        variables["column_values"] = json.dumps(column_values)

    payload = {
        "query": query,
        "variables": variables
    }

    print("📤 FINAL CREATE ITEM PAYLOAD:")
    print(payload)

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    print("📥 RESPONSE:")
    print(response.text)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#update_item
def update_item_column_value(item_id, board_id, column_id, value_json):
    query = """
    mutation ($item_id: ID!, $board_id: ID!, $column_id: String!, $value: JSON!) {
      change_column_value(item_id: $item_id, board_id: $board_id, column_id: $column_id, value: $value) {
        id
        name
      }
    }
    """

    variables = {
        "item_id": str(item_id),
        "board_id": str(board_id),
        "column_id": column_id,
        "value": json.dumps(value_json)
    }

    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    print("📤 UPDATE ITEM PAYLOAD:")
    print(payload)
    print("📥 RESPONSE:")
    print(response.text)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#delete_item
def delete_item(item_id):
    query = """
    mutation ($item_id: ID!) {
      delete_item(item_id: $item_id) {
        id
      }
    }
    """

    variables = {"item_id": item_id}

    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#column_values
def get_item_column_values(item_id):
    query = """
    query ($item_id: [ID!]!) {
      items(ids: $item_id) {
        id
        name
        column_values {
          id
          type
          text
          value
        }
      }
    }
    """
    variables = {"item_id": [str(item_id)]}

    payload = {
        "query": query,
        "variables": variables
    }

    headers = monday_headers()

    response = requests.post(Config.MONDAY_API_URL, headers=headers, json=payload)

    print("📤 COLUMN VALUES PAYLOAD:", payload)
    print("📥 RESPONSE:", response.text)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#change_column_value
def change_column_value(item_id, board_id, column_id, value):
    query = """
    mutation ($item_id: ID!, $board_id: ID!, $column_id: String!, $value: JSON!) {
      change_column_value(item_id: $item_id, board_id: $board_id, column_id: $column_id, value: $value) {
        id
        name
        column_values {
          id
          text
          type
          value
        }
      }
    }
    """

    variables = {
        "item_id": str(item_id),
        "board_id": str(board_id),
        "column_id": column_id,
        "value": json.dumps(value)
    }

    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    print("📤 CHANGE COLUMN VALUE PAYLOAD:", payload)
    print("📥 RESPONSE:", response.text)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#groups
def get_board_groups(board_id):
    query = """
    query ($board_id: [ID!]!) {
      boards(ids: $board_id) {
        groups {
          id
          title
        }
      }
    }
    """

    variables = {"board_id": [board_id]}

    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#create_group
def create_group(board_id, group_name):
    query = """
    mutation ($board_id: ID!, $group_name: String!) {
      create_group(board_id: $board_id, group_name: $group_name) {
        id
        title
      }
    }
    """

    variables = {
        "board_id": board_id,
        "group_name": group_name
    }

    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#delete_group
def delete_group(board_id, group_id):
    query = """
    mutation ($board_id: ID!, $group_id: String!) {
      delete_group(board_id: $board_id, group_id: $group_id) {
        id
      }
    }
    """
    variables = {
        "board_id": board_id,
        "group_id": group_id
    }

    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#users
def get_users(ids=None, limit=None, page=None):
    query = """
    query ($ids: [ID!], $limit: Int, $page: Int) {
      users(ids: $ids, limit: $limit, page: $page) {
        id
        name
        email
        photo_small
        enabled
        is_guest
        is_admin
        teams {
          id
          name
        }
      }
    }
    """

    variables = {
        "ids": [str(i) for i in ids] if ids else None,  # Convert each ID to string
        "limit": limit,
        "page": page
    }

    payload = {
        "query": query,
        "variables": {k: v for k, v in variables.items() if v is not None}
    }

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#me
def get_authenticated_user():
    query = """
    query {
      me {
        id
        name
        email
        created_at
        enabled
        is_admin
        join_date
      }
    }
    """

    payload = {
        "query": query
    }

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    print("📤 ME QUERY PAYLOAD:", payload)
    print("📥 RESPONSE:", response.text)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#teams
def get_teams(ids=None):
    query = """
    query ($ids: [ID!]) {
      teams(ids: $ids) {
        id
        name
        picture_url
        users {
          id
          name
          email
        }
      }
    }
    """

    variables = {}
    if ids:
        variables["ids"] = ids

    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    print("📤 TEAMS QUERY PAYLOAD:", payload)
    print("📥 RESPONSE:", response.text)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#create_update
def create_update(item_id, body):
    query = """
    mutation ($item_id: ID!, $body: String!) {
      create_update(item_id: $item_id, body: $body) {
        id
        body
        created_at
        creator {
          id
          name
          email
        }
      }
    }
    """

    variables = {
        "item_id": str(item_id),
        "body": body
    }

    payload = {
        "query": query,
        "variables": variables
    }

    # Optional debug
    print("📤 CREATE_UPDATE Payload:", payload)

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    print("📥 MONDAY API Response:", response.text)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#updates
def get_updates(item_id):
    query = """
    query ($item_id: [ID!]!) {
      items(ids: $item_id) {
        id
        name
        updates {
          id
          body
          created_at
          creator {
            id
            name
            email
          }
        }
      }
    }
    """

    variables = {
        "item_id": [str(item_id)]
    }

    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    print("📤 GET UPDATES PAYLOAD:", payload)
    print("📥 RESPONSE:", response.text)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#notifications
def send_notification(user_id, text, target_id, target_type="Project"):
    query = """
    mutation ($user_id: ID!, $text: String!, $target_id: ID!, $target_type: NotificationTargetType!) {
      create_notification(
        user_id: $user_id,
        text: $text,
        target_id: $target_id,
        target_type: $target_type
      ) {
        id
        text
      }
    }
    """

    variables = {
        "user_id": str(user_id),
        "text": text,
        "target_id": str(target_id),
        "target_type": target_type  # Possible values: "Project", "Post", "Update", etc.
    }

    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#tags
def get_tags(ids=None):
    query = """
    query ($ids: [ID!]) {
      tags(ids: $ids) {
        id
        name
        color
      }
    }
    """

    variables = {}
    if ids:
        variables["ids"] = [str(i) for i in ids]  # ensure IDs are strings

    payload = {
        "query": query,
        "variables": variables
    }

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)
    
    try:
        response.raise_for_status()
        return response.json()["data"]["tags"]
    except Exception as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#create_tag
def create_or_get_tag(tag_name, board_id=None):
    query = """
    mutation ($tag_name: String!, $board_id: ID) {
      create_or_get_tag(tag_name: $tag_name, board_id: $board_id) {
        id
        name
        color
      }
    }
    """
    variables = {
        "tag_name": tag_name,
        "board_id": str(board_id) if board_id else None
    }

    payload = {
        "query": query,
        "variables": {k: v for k, v in variables.items() if v is not None}
    }

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)
    try:
        response.raise_for_status()
        return response.json()["data"]["create_or_get_tag"]
    except Exception as e:
        raise Exception(f"Monday.com API error: {e}\n{response.text}")

#Doesn't supported by Monday
#delete_tag
# def remove_tag_from_item(item_id, column_id="tags"):
#     query = """
#     mutation ($item_id: Int!, $column_id: String!, $value: JSON!) {
#       change_column_value(item_id: $item_id, column_id: $column_id, value: $value) {
#         id
#       }
#     }
#     """

#     # Note: value must be a string of JSON (not already-encoded JSON string!)
#     value_string = '{"tag_ids": []}'  # Clear all tags

#     variables = {
#         "item_id": int(item_id),
#         "column_id": column_id,
#         "value": value_string
#     }

#     payload = {"query": query, "variables": variables}

#     response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)
#     response.raise_for_status()
#     return response.json()["data"]["change_column_value"]

#workspaces
# app/monday/monday_service.py

def get_workspaces(ids=None, limit=25, page=1):
    query = """
    query ($ids: [ID!], $limit: Int, $page: Int) {
      workspaces (ids: $ids, limit: $limit, page: $page) {
        id
        name
        kind
        description
        created_at
        is_default_workspace
        state
      }
    }
    """
    variables = {
        "ids": ids,
        "limit": limit,
        "page": page
    }

    payload = {"query": query, "variables": variables}
    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)
    response.raise_for_status()
    return response.json()["data"]["workspaces"]

# create_workspace

def create_workspace(name, kind="open", description=None, account_product_id=None):
    query = """
    mutation ($name: String!, $kind: WorkspaceKind!, $description: String, $account_product_id: ID) {
      create_workspace(name: $name, kind: $kind, description: $description, account_product_id: $account_product_id) {
        id
        name
        description
        kind
      }
    }
    """
    variables = {
        "name": name,
        "kind": kind,
        "description": description,
        "account_product_id": account_product_id
    }

    payload = {"query": query, "variables": variables}
    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)
    response.raise_for_status()
    return response.json()["data"]["create_workspace"]

#delete_workspace
# app/monday/monday_service.py

def delete_workspace(workspace_id):
    query = """
    mutation ($workspace_id: ID!) {
      delete_workspace(workspace_id: $workspace_id) {
        id
      }
    }
    """
    variables = {"workspace_id": workspace_id}
    payload = {"query": query, "variables": variables}

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)
    response.raise_for_status()
    return response.json()["data"]["delete_workspace"]

#webhooks
def create_webhook(board_id, url, event, config=None):
    query = """
    mutation ($board_id: ID!, $url: String!, $event: WebhookEventType!, $config: JSON) {
        create_webhook(board_id: $board_id, url: $url, event: $event, config: $config) {
            id
            board_id
            event
            config
        }
    }
    """
    variables = {
        "board_id": str(board_id),
        "url": url,
        "event": event,
        "config": json.dumps(config) if config else None
    }
    payload = {"query": query, "variables": variables}

    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)

    try:
        response.raise_for_status()
        data = response.json()
        if "errors" in data:
            raise Exception(f"Monday.com API error: {data['errors']}")
        return data["data"]["create_webhook"]
    except Exception as e:
        raise Exception(f"Failed to create webhook: {str(e)} - Raw: {response.text}")


def get_webhooks(board_id):
    query = """
    query ($board_id: ID!) {
        webhooks(board_id: $board_id) {
            id
            event
            board_id
            config
        }
    }
    """
    payload = {"query": query, "variables": {"board_id": str(board_id)}}
    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)
    response.raise_for_status()
    return response.json()["data"]["webhooks"]

def delete_webhook(webhook_id):
    query = """
    mutation ($id: ID!) {
        delete_webhook(id: $id) {
            id
            board_id
        }
    }
    """
    payload = {"query": query, "variables": {"id": str(webhook_id)}}
    response = requests.post(Config.MONDAY_API_URL, headers=monday_headers(), json=payload)
    response.raise_for_status()
    return response.json()["data"]["delete_webhook"]

#create_asset
#cannot upload file to ltem
MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
MONDAY_API_URL = "https://api.monday.com/v2"

def add_file_to_update_service(update_id, file_stream, filename):
    url = "https://api.monday.com/v2/file"

    query = """
    mutation ($file: File!, $update_id: ID!) {
      add_file_to_update(update_id: $update_id, file: $file) {
        id
      }
    }
    """

    headers = {
        "Authorization": MONDAY_API_KEY  # No Content-Type header manually
    }

    data = {
        'query': query,
        'variables': json.dumps({
            'update_id': str(update_id)  # Fix: cast to string
        })
    }

    files = {
        'file': (filename, file_stream)
    }

    response = requests.post(url, headers=headers, data=data, files=files)
    response.raise_for_status()
    return response.json()

#activity log
def monday_headers():
    return {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }

def get_activity_logs(board_id, from_date, to_date):
    query = """
    query ($board_id: [ID!], $from: ISO8601DateTime, $to: ISO8601DateTime) {
      boards(ids: $board_id) {
        activity_logs(from: $from, to: $to) {
          id
          event
          data
          user_id
          created_at
        }
      }
    }
    """
    variables = {
        "board_id": [board_id],
        "from": from_date,
        "to": to_date
    }
    response = requests.post(
        MONDAY_API_URL,
        headers=monday_headers(),
        json={"query": query, "variables": variables}
    )
    response.raise_for_status()
    return response.json()["data"]["boards"][0]["activity_logs"]

#items_by_column_values

def get_items_by_column_value(board_id, column_id, value):
    url = "https://api.monday.com/v2"
    headers = monday_headers()

    query = """
    query ($board_id: Int!, $column_id: String!, $value: String!) {
        items_by_column_values(board_id: $board_id, column_id: $column_id, column_value: $value) {
            id
            name
            column_values {
                id
                title
                text
            }
        }
    }
    """

    variables = {
        "board_id": board_id,
        "column_id": column_id,
        "value": value
    }

    response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
    response.raise_for_status()
    return response.json()

#Filtered item list
def get_items_assigned(board_id):
    query = """
    query ($board_id: [ID!]) {
      boards(ids: $board_id) {
        items_page(query_params: {
          rules: [
            {column_id: "name", compare_value: ["assigned_to_me"], operator: any_of},
            {column_id: "name", compare_value: ["true"], operator: any_of}
          ]
        }) {
          items {
            id
            name
          }
        }
      }
    }
    """
    variables = {
        "board_id": [board_id]
    }

    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(MONDAY_API_URL, json={"query": query, "variables": variables}, headers=headers)
    response.raise_for_status()
    return response.json()


def move_item_to_board(item_id, board_id, group_id, columns_mapping=None):
    query = """
    mutation (
      $item_id: Int!,
      $board_id: Int!,
      $group_id: String!,
      $columns_mapping: [ColumnMappingInput!]
    ) {
      move_item_to_board(
        item_id: $item_id,
        board_id: $board_id,
        group_id: $group_id,
        columns_mapping: $columns_mapping
      ) {
        id
      }
    }
    """

    variables = {
        "item_id": int(item_id),
        "board_id": int(board_id),
        "group_id": group_id,
        "columns_mapping": columns_mapping or []
    }

    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(MONDAY_API_URL, json={"query": query, "variables": variables}, headers=headers)
    response.raise_for_status()
    return response.json()


#move_item_to_group
def move_item_to_group(item_id, group_id):
    query = """
    mutation ($item_id: ID!, $group_id: String!) {
      move_item_to_group(item_id: $item_id, group_id: $group_id) {
        id
        name
        group {
          id
          title
        }
      }
    }
    """

    variables = {
        "item_id": item_id,
        "group_id": group_id
    }

    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(MONDAY_API_URL, json={"query": query, "variables": variables}, headers=headers)
    response.raise_for_status()
    return response.json()

#move_item_to_board
def move_item_to_board(item_id, board_id, group_id, columns_mapping=None, subitems_columns_mapping=None):
    query = """
    mutation (
      $item_id: ID!,
      $board_id: ID!,
      $group_id: ID!,
      $columns_mapping: [ColumnMappingInput!],
      $subitems_columns_mapping: [ColumnMappingInput!]
    ) {
      move_item_to_board(
        item_id: $item_id,
        board_id: $board_id,
        group_id: $group_id,
        columns_mapping: $columns_mapping,
        subitems_columns_mapping: $subitems_columns_mapping
      ) {
        id
      }
    }
    """

    variables = {
        "item_id": item_id,
        "board_id": board_id,
        "group_id": group_id,
        "columns_mapping": columns_mapping or [],
        "subitems_columns_mapping": subitems_columns_mapping or []
    }

    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(MONDAY_API_URL, json={"query": query, "variables": variables}, headers=headers)
    response.raise_for_status()
    return response.json()

#archive_item
def archive_item(item_id):
    query = """
    mutation ($item_id: ID!) {
      archive_item(item_id: $item_id) {
        id
        name
      }
    }
    """
    variables = {
        "item_id": item_id
    }

    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(MONDAY_API_URL, json={"query": query, "variables": variables}, headers=headers)
    response.raise_for_status()
    return response.json()

#delete_group_items
def delete_item(item_id):
    query = """
    mutation ($item_id: ID!) {
      delete_item(item_id: $item_id) {
        id
      }
    }
    """
    variables = {
        "item_id": item_id
    }

    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(MONDAY_API_URL, json={"query": query, "variables": variables}, headers=headers)
    response.raise_for_status()
    return response.json()

#get_board_columns
def get_board_columns(board_id):
    query = """
    query ($board_id: [ID!]) {
      boards(ids: $board_id) {
        columns {
          id
          title
          type
          description
          archived
          settings_str
          width
        }
      }
    }
    """
    variables = {"board_id": [board_id]}
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(MONDAY_API_URL, json={"query": query, "variables": variables}, headers=headers)
    response.raise_for_status()
    return response.json()

#create_column
def create_column(board_id, title, column_type, description=None):
    query = """
    mutation ($board_id: ID!, $title: String!, $column_type: ColumnType!, $description: String) {
      create_column(board_id: $board_id, title: $title, column_type: $column_type, description: $description) {
        id
        title
        description
      }
    }
    """
    variables = {
        "board_id": board_id,
        "title": title,
        "column_type": column_type,
        "description": description
    }
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(MONDAY_API_URL, json={"query": query, "variables": variables}, headers=headers)
    response.raise_for_status()
    return response.json()


def add_file_to_update(update_id, file_path):
    query = """
    mutation ($file: File!, $update_id: ID!) {
      add_file_to_update(file: $file, update_id: $update_id) {
        id
        assets {
          id
          name
          public_url
          file_size
          file_extension
          uploaded_by {
            id
            name
          }
        }
      }
    }
    """

    operations = {
        "query": query,
        "variables": {
            "file": None,
            "update_id": update_id
        }
    }

    map_json = {
        "0": ["variables.file"]
    }

    files = {
        'operations': (None, json.dumps(operations), 'application/json'),
        'map': (None, json.dumps(map_json), 'application/json'),
        '0': (os.path.basename(file_path), open(file_path, 'rb'))
    }

    headers = {
        "Authorization": MONDAY_API_KEY
    }

    response = requests.post(MONDAY_API_URL, files=files, headers=headers)
    response.raise_for_status()
    return response.json()
