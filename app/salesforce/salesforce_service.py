import requests
from app.config import Config
import urllib.parse

# Declare shared headers at the top
HEADERS = {
    "Authorization": f"Bearer {Config.ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

#get_user_info
def get_authenticated_user_info():
    """
    Retrieves the authenticated user's information from Salesforce.
    """
    if not Config.ACCESS_TOKEN:
        return {
            "status": "error",
            "code": 401,
            "message": "Missing Salesforce access token"
        }

    url = "https://login.salesforce.com/services/oauth2/userinfo"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": getattr(err.response, 'status_code', 500),
            "message": str(err)
        }

#get_limits
def get_limits():
    """
    Retrieves current system limits usage from Salesforce.
    """
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/limits"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": getattr(err.response, 'status_code', 500),
            "message": str(err)
        }

#get_objects
def get_objects():
    """
    Lists all available standard and custom objects in Salesforce.
    """
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json().get("sobjects", [])
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": getattr(err.response, 'status_code', 500),
            "message": str(err)
        }

#describe_object
def describe_object(object_name):
    """
    Describes the metadata for a specific Salesforce object.
    """
    if not object_name:
        return {
            "status": "error",
            "code": 400,
            "message": "Missing object_name parameter"
        }

    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/{object_name}/describe"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.HTTPError as err:
        return {
            "status": "error",
            "code": response.status_code,
            "message": response.text
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": 500,
            "message": str(err)
        }

#query
import urllib.parse

def query_salesforce(soql):
    """
    Executes a SOQL query and returns the result.
    """
    if not soql:
        return {
            "status": "error",
            "code": 400,
            "message": "Missing SOQL query string"
        }

    encoded_query = urllib.parse.quote(soql)
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/query?q={encoded_query}"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.HTTPError as err:
        return {
            "status": "error",
            "code": response.status_code,
            "message": response.text
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": 500,
            "message": str(err)
        }

#queryMore
def query_more(query_locator):
    """
    Retrieves the next page of results using the provided query locator.
    """
    if not query_locator.startswith("/services/data/"):
        return {
            "status": "error",
            "code": 400,
            "message": "Invalid query_locator format"
        }

    url = f"{Config.SALESFORCE_INSTANCE_URL}{query_locator}"  # 👈 This should be full URL

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "code": getattr(e.response, 'status_code', 500),
            "message": str(e)
        }

#search
def search_salesforce(sosl_query):
    """
    Performs a SOSL text search.
    """
    if not sosl_query:
        return {
            "status": "error",
            "code": 400,
            "message": "Missing SOSL query string"
        }

    encoded_query = urllib.parse.quote(sosl_query)
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/search/?q={encoded_query}"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.HTTPError as err:
        return {
            "status": "error",
            "code": response.status_code,
            "message": response.text
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": 500,
            "message": str(err)
        }

#create_record
def create_record(object_name, data):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/{object_name}"
    try:
        response = requests.post(url, json=data, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": getattr(err.response, 'status_code', 500),
            "message": str(err)
        }

#retrieve_record
def retrieve_record(object_name, record_id):
    """
    Retrieves a specific record from Salesforce by object name and record ID.
    """
    if not object_name or not record_id:
        return {
            "status": "error",
            "code": 400,
            "message": "Missing object_name or record_id"
        }

    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/{object_name}/{record_id}"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.HTTPError as err:
        return {
            "status": "error",
            "code": response.status_code,
            "message": response.text
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": 500,
            "message": str(err)
        }

#update_record
def update_record(object_name, record_id, field_values):
    """
    Updates a record in Salesforce by object name and record ID.
    """
    if not object_name or not record_id or not field_values:
        return {
            "status": "error",
            "code": 400,
            "message": "Missing object_name, record_id, or field_values"
        }

    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/{object_name}/{record_id}"

    try:
        response = requests.patch(url, headers=HEADERS, json=field_values)
        response.raise_for_status()
        return {
            "status": "success",
            "message": f"{object_name} with ID {record_id} updated successfully"
        }
    except requests.exceptions.HTTPError as err:
        return {
            "status": "error",
            "code": err.response.status_code,
            "message": err.response.text
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": 500,
            "message": str(err)
        }

#delete_record
def delete_record(object_name, record_id):
    """
    Deletes a Salesforce record by object name and record ID.
    """
    if not object_name or not record_id:
        return {
            "status": "error",
            "code": 400,
            "message": "Missing object_name or record_id"
        }

    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/{object_name}/{record_id}"

    try:
        response = requests.delete(url, headers=HEADERS)
        if response.status_code == 204:
            return {
                "status": "success",
                "message": f"{object_name} with ID {record_id} deleted successfully"
            }
        else:
            return {
                "status": "error",
                "code": response.status_code,
                "message": response.text
            }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": 500,
            "message": str(err)
        }

#upsert_record
def upsert_record(object_name, external_id_field, external_id_value, data):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/{object_name}/{external_id_field}/{external_id_value}"
    try:
        response = requests.patch(url, headers=HEADERS, json=data)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json() if response.text else {"success": True}
        }
    except requests.exceptions.HTTPError as err:
        return {
            "status": "error",
            "code": response.status_code,
            "message": response.text
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": 500,
            "message": str(err)
        }

#get_deleted
def get_deleted_records(object_name, start_datetime, end_datetime):
    """
    Retrieves records deleted within a specified timeframe.
    """
    if not object_name or not start_datetime or not end_datetime:
        return {
            "status": "error",
            "code": 400,
            "message": "Missing required parameters: object_name, start_datetime, end_datetime"
        }

    url = (
        f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/"
        f"{object_name}/deleted?start={start_datetime}&end={end_datetime}"
    )

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "code": getattr(e.response, 'status_code', 500),
            "message": str(e)
        }

#get_updated
def get_updated_records(object_name, start, end):
    """
    Retrieves updated records within a time frame.
    """
    if not all([object_name, start, end]):
        return {
            "status": "error",
            "code": 400,
            "message": "Missing required parameters: object_name, start, or end"
        }

    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/{object_name}/updated"
    params = {
        "start": start,
        "end": end
    }

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": getattr(err.response, 'status_code', 500),
            "message": str(err)
        }

#create_attachment
import base64

def create_attachment(parent_id, name, file_content):
    if not parent_id or not name or not file_content:
        return {
            "status": "error",
            "code": 400,
            "message": "Missing required fields: parent_id, name, or file_content"
        }

    try:
        encoded_body = base64.b64encode(file_content).decode("utf-8")
    except Exception as e:
        return {
            "status": "error",
            "code": 500,
            "message": f"Base64 encoding failed: {str(e)}"
        }

    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Attachment"
    payload = {
        "ParentId": parent_id,
        "Name": name,
        "Body": encoded_body
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.HTTPError as err:
        return {
            "status": "error",
            "code": response.status_code,
            "message": response.text  # Show exact error response from Salesforce
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": 500,
            "message": str(err)
        }

#retrieve_attachment
def retrieve_attachment(attachment_id):
    """
    Retrieves a Salesforce attachment by its ID.
    """
    if not attachment_id:
        return {
            "status": "error",
            "code": 400,
            "message": "Missing attachment_id parameter"
        }

    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Attachment/{attachment_id}"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.HTTPError as err:
        return {
            "status": "error",
            "code": response.status_code,
            "message": response.text
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": 500,
            "message": str(err)
        }

#delete_attachment
def delete_attachment(attachment_id):
    """
    Deletes an attachment by ID in Salesforce.
    """
    if not attachment_id:
        return {
            "status": "error",
            "code": 400,
            "message": "Missing attachment_id"
        }

    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Attachment/{attachment_id}"

    try:
        response = requests.delete(url, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "message": f"Attachment with ID {attachment_id} deleted successfully"
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": getattr(err.response, 'status_code', 500),
            "message": str(err)
        }

#get_recent_items
def get_recent_items():
    """
    Retrieves recently accessed records for the authenticated user.
    """
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/recent"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": getattr(err.response, 'status_code', 500),
            "message": str(err)
        }

#get_user_list
def get_user_list():
    """
    Retrieves a list of users from Salesforce.
    """
    soql = "SELECT Id, Name, Username, Email, Profile.Name, IsActive FROM User"
    encoded_query = urllib.parse.quote(soql)
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/query?q={encoded_query}"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json().get("records", [])
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": getattr(err.response, 'status_code', 500),
            "message": str(err)
        }
    
#get_profile
def get_my_profile():
    """
    Gets the profile of the currently authenticated user using /userinfo and ProfileId lookup.
    """
    user_info = get_authenticated_user_info()
    if user_info["status"] != "success":
        return user_info

    user_id = user_info["data"].get("user_id")

    # Rename to avoid calling itself
    return fetch_profile_by_user_id(user_id)

def fetch_profile_by_user_id(user_id):
    """
    Retrieves the profile details of a user by user ID.
    """
    if not user_id:
        return {
            "status": "error",
            "code": 400,
            "message": "Missing user_id parameter"
        }

    try:
        user_url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/User/{user_id}"
        user_resp = requests.get(user_url, headers=HEADERS)
        user_resp.raise_for_status()
        user_data = user_resp.json()
        profile_id = user_data.get("ProfileId")

        if not profile_id:
            return {
                "status": "error",
                "code": 404,
                "message": "ProfileId not found for the user"
            }

        profile_url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Profile/{profile_id}"
        profile_resp = requests.get(profile_url, headers=HEADERS)
        profile_resp.raise_for_status()

        return {
            "status": "success",
            "data": profile_resp.json()
        }

    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": getattr(err.response, 'status_code', 500),
            "message": str(err)
        }

#get_roles
def get_roles():
    """
    Retrieves all available user roles in the Salesforce org.
    """
    query = "SELECT Id, Name, DeveloperName, ParentRoleId FROM UserRole"
    encoded_query = urllib.parse.quote(query)
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/query?q={encoded_query}"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json().get("records", [])
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": getattr(err.response, 'status_code', 500),
            "message": str(err)
        }

#get_groups
def get_groups():
    """
    Retrieves all public groups and queues in the Salesforce org.
    """
    query = "SELECT Id, Name, Type, DeveloperName FROM Group"
    encoded_query = urllib.parse.quote(query)
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/query?q={encoded_query}"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json().get("records", [])
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": getattr(err.response, 'status_code', 500),
            "message": str(err)
        }

#get_object_layout
def get_object_layout(object_name, record_type_id=None):
    """
    Retrieves layout metadata for a Salesforce object using /describe/layouts.
    Optionally filters by recordTypeId.
    """
    if not object_name:
        return {
            "status": "error",
            "code": 400,
            "message": "Missing object_name parameter"
        }

    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v58.0/sobjects/{object_name}/describe/layouts"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        # Optional: filter by recordTypeId
        if record_type_id:
            layouts = [
                layout for layout in data.get("layouts", [])
                if layout.get("recordTypeId") == record_type_id
            ]
            data["layouts"] = layouts

        return {
            "status": "success",
            "data": data
        }

    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": getattr(err.response, 'status_code', 500),
            "message": str(err)
        }

#execute_anonymous_apex
def execute_anonymous_apex(apex_code):
    """
    Executes Apex code anonymously using the Tooling API.
    Requires 'API Enabled' and 'Modify All Data' permissions.
    """
    if not apex_code:
        return {
            "status": "error",
            "code": 400,
            "message": "Missing Apex code to execute"
        }

    encoded_code = urllib.parse.quote(apex_code)
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/tooling/executeAnonymous?anonymousBody={encoded_code}"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        result = response.json()

        return {
            "status": "success" if result.get("success") else "error",
            "compiled": result.get("compiled"),
            "success": result.get("success"),
            "line": result.get("line"),
            "column": result.get("column"),
            "exceptionMessage": result.get("exceptionMessage"),
            "compileProblem": result.get("compileProblem"),
            "debugLog": result.get("debugLog")
        }

    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": getattr(err.response, 'status_code', 500),
            "message": str(err)
        }

#get_org_info
def get_org_info():
    headers = HEADERS
  

    query = (
        "SELECT Name, InstanceName, IsSandbox, OrganizationType, TrialExpirationDate "
        "FROM Organization"
    )
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/query?q={query}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {"status": "success", "data": response.json()["records"][0]}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e), "code": e.response.status_code}
    
#list_record_types
def list_record_types(object_name):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/{object_name}/describe"
    headers = HEADERS

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        record_types = data.get("recordTypeInfos", [])
        return {"status": "success", "data": record_types}
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#get_picklist_values
def get_picklist_values(object_name, field_name):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/{object_name}/describe"
    headers = HEADERS

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        fields = response.json().get("fields", [])

        field_info = next((f for f in fields if f.get("name") == field_name), None)

        if not field_info or field_info.get("type") != "picklist":
            return {
                "status": "error",
                "message": f"Field '{field_name}' is not a valid picklist on '{object_name}'",
                "code": 400
            }

        picklist_values = [
            entry["value"] for entry in field_info.get("picklistValues", []) if not entry.get("inactive", False)
        ]

        return {"status": "success", "data": picklist_values}
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#create_task
def create_task(task_data):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Task"
    headers = HEADERS

    try:
        response = requests.post(url, headers=headers, json=task_data)
        response.raise_for_status()
        result = response.json()
        return {"status": "success", "task_id": result.get("id")}
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#update_task
def update_task(record_id, update_data):
    """
    Updates a Task record in Salesforce by its ID.
    
    Parameters:
        record_id (str): The Salesforce Task ID.
        update_data (dict): Dictionary of fields to update.
    
    Returns:
        dict: Confirmation message or error.
    """
    if not record_id or not update_data:
        return {
            "status": "error",
            "code": 400,
            "message": "Missing record_id or update data"
        }

    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Task/{record_id}"

    try:
        response = requests.patch(url, headers=HEADERS, json=update_data)
        response.raise_for_status()
        return {
            "status": "success",
            "message": f"Task with ID {record_id} updated successfully"
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": getattr(err.response, 'status_code', 500),
            "message": str(err)
        }

#delete_task
def delete_task(record_id):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Task/{record_id}"
    headers = HEADERS

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return {"status": "success", "message": f"Task {record_id} deleted successfully"}
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#create_event
def create_event(data):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Event"
    headers = HEADERS

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }
    
#update
def update_event(record_id, update_data):
    """
    Updates an Event record in Salesforce.
    :param record_id: The Salesforce Event record ID
    :param update_data: A dictionary of fields to update
    :return: Confirmation message or error
    """
    if not record_id or not update_data:
        return {
            "status": "error",
            "code": 400,
            "message": "Missing record_id or update data"
        }

    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Event/{record_id}"

    try:
        response = requests.patch(url, json=update_data, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "message": f"Event with ID {record_id} updated successfully"
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": getattr(err.response, 'status_code', 500),
            "message": str(err)
        }

#delete_event
def delete_event(record_id):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Event/{record_id}"
    headers = HEADERS

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return {"status": "success", "message": f"Event {record_id} deleted successfully."}
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#list_appointments
def list_appointments(user_id=None):
    headers = HEADERS

    # You can customize the SOQL query based on additional filter needs
    base_query = (
        "SELECT Id, Subject, StartDateTime, EndDateTime, Location, WhoId, WhatId, OwnerId "
        "FROM Event"
    )
    if user_id:
        base_query += f" WHERE OwnerId = '{user_id}'"

    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/query?q={base_query}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#send_email
def send_email(email_data):

    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/actions/standard/sendEmail"
    payload = {
        "inputs": [
            {
                "emailBody": email_data.get("emailBody"),
                "emailAddresses": email_data.get("emailAddresses"),  # comma-separated or single string
                "subject": email_data.get("subject"),
                "senderType": "CurrentUser"  # or "OrgWideEmailAddress" if configured
            }
        ]
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#send_mass_email
def send_mass_email(to_addresses, subject, body):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/actions/custom/apex/MassEmailSender.sendBulkEmail"
    headers = HEADERS

    payload = {
        "inputs": [
            {
                "toAddresses": to_addresses,
                "subject": subject,
                "body": body
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }
    
#get_email_status
def get_email_status(email_id):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/EmailMessage/{email_id}"
    headers = HEADERS

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#create_case
def create_case(data):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Case"
    headers = HEADERS

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()  # returns {"id": "...", ...}
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#update_case
def update_case(record_id, update_data):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Case/{record_id}"
    headers = HEADERS

    try:
        response = requests.patch(url, headers=headers, json=update_data)
        response.raise_for_status()
        return {
            "status": "success",
            "message": f"Case {record_id} updated successfully"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#delete_case
def delete_case(record_id):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Case/{record_id}"
    headers = HEADERS

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return {
            "status": "success",
            "message": f"Case {record_id} deleted successfully"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#create_lead
def create_lead(lead_data):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Lead"
    headers = HEADERS

    try:
        response = requests.post(url, headers=headers, json=lead_data)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#update_lead
def update_lead(record_id, field_values):

    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Lead/{record_id}"
    headers = HEADERS

    try:
        response = requests.patch(url, headers=headers, json=field_values)
        response.raise_for_status()
        return {"status": "success", "message": f"Lead {record_id} updated successfully"}
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#convert_lead
def convert_lead(lead_id, conversion_data):
    """
    Converts a Lead into Account, Contact, and optionally Opportunity.
    :param lead_id: The Lead record ID to convert
    :param conversion_data: Dict containing optional conversion settings
    :return: IDs of created Account/Contact/Opportunity or error message
    """
    if not lead_id:
        return {
            "status": "error",
            "code": 400,
            "message": "Missing lead_id"
        }

    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Lead/{lead_id}/_convert"

    try:
        response = requests.post(url, json=conversion_data, headers=HEADERS)
        response.raise_for_status()
        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.HTTPError as err:
        return {
            "status": "error",
            "code": err.response.status_code,
            "message": err.response.text
        }
    except requests.exceptions.RequestException as err:
        return {
            "status": "error",
            "code": 500,
            "message": str(err)
        }
    
#create_opportunity
def create_opportunity(field_values):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Opportunity"
    headers = HEADERS

    try:
        response = requests.post(url, headers=headers, json=field_values)
        response.raise_for_status()
        data = response.json()
        return {
            "status": "success",
            "data": data
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#update_opportunity
def update_opportunity(record_id, field_values):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Opportunity/{record_id}"
    headers = HEADERS

    try:
        response = requests.patch(url, headers=headers, json=field_values)
        response.raise_for_status()
        return {
            "status": "success",
            "message": f"Opportunity {record_id} updated successfully"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#delete_opportunity
def delete_opportunity(record_id):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/sobjects/Opportunity/{record_id}"
    headers = HEADERS

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return {
            "status": "success",
            "message": f"Opportunity {record_id} deleted successfully"
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#get_reports
def get_reports():
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/analytics/reports"
    headers = HEADERS

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Safe fallback if the response is already a list
        reports = data if isinstance(data, list) else data.get("reports", [])

        return {"status": "success", "data": reports}
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#run_report
def run_report(report_id):
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/analytics/reports/{report_id}"
    headers = HEADERS

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {"status": "success", "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#get_dashboards
def get_dashboards():
    url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/analytics/dashboards"

    headers = HEADERS

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Handle if data is a list or dict
        if isinstance(data, dict):
            dashboards = data.get("dashboards", [])
        elif isinstance(data, list):
            dashboards = data
        else:
            dashboards = []

        return {"status": "success", "data": dashboards}

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
            "code": e.response.status_code if e.response else 500
        }

#get_dashboard_data
def get_dashboard_data(dashboard_id):
    try:
        headers = HEADERS
        url = f"{Config.SALESFORCE_INSTANCE_URL}/services/data/v60.0/analytics/dashboards/{dashboard_id}"

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return {
            "status": "success",
            "data": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "code": e.response.status_code if e.response else 500,
            "message": str(e)
        }