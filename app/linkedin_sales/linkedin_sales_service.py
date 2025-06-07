import requests
from flask import current_app


#get_sales_profile(i
def get_sales_profile(instance_id: str, partner: str, record_id: str) -> dict:
    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Ensure all required inputs are provided
    if not all([instance_id, partner, record_id]):
        return {
            "error": 400,
            "message": "Missing required input: instance_id, partner, or record_id"
        }
    # Construct URL
    url = f"{base_url}/salesNavigatorProfileAssociations/(instanceId:{instance_id},partner:{partner},recordId:{record_id})"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code == 403:
            return {
                "error": 403,
                "message": "Access denied. Your app may not have the required Sales Navigator scope."
            }
        elif response.status_code == 404:
            return {
                "error": 404,
                "message": "Sales Navigator profile not found. Verify instanceId, partner, and recordId."
            }
        else:
            if current_app.config.get("USE_MOCK", True):
                return mock_get_sales_profile(instance_id, partner, record_id)
            return {
                "error": response.status_code,
                "message": response.text
            }
    except requests.RequestException as e:
        return {
            "error": "network_error",
            "message": str(e)
        }
def mock_get_sales_profile(instance_id: str, partner: str, record_id: str) -> dict:
    return {
        "member": f"urn:li:person:mock_{record_id}",
        "profile": f"https://www.linkedin.com/sales/profile/mock_{record_id}",
        "profilePhoto": "https://media.licdn.com/dms/image/mock_profile_photo.jpg",
        "note": "Mock response — actual API requires LinkedIn Sales Navigator partner access."
    }

#get contract info
def get_sales_contact_info(member_id: str) -> dict:

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # This is a placeholder endpoint – replace with actual endpoint if you're approved.
    url = f"{base_url}/salesNavigatorContacts/{member_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code == 403:
            return {
                "error": 403,
                "message": "Access denied – requires scope: r_sales_nav_contacts"
            }
        elif response.status_code == 404:
            return {
                "error": 404,
                "message": "Contact info not found for the provided member ID"
            }
        else:
            return {
                "error": response.status_code,
                "message": response.text
            }
    except requests.RequestException as e:
        return {
            "error": "network_error",
            "message": str(e)
        }
    
#get_company_profile
def get_company_profile(company_id_or_urn: str) -> dict:
 
    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # This is a placeholder endpoint; replace with actual Sales Navigator endpoint if approved
    url = f"{base_url}/salesNavigatorCompanies/{company_id_or_urn}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code == 403:
            return {
                "error": 403,
                "message": "Access denied – requires scope: r_sales_nav_accounts"
            }
        elif response.status_code == 404:
            return {
                "error": 404,
                "message": "Company not found for the given ID or URN"
            }
        else:
            return {
                "error": response.status_code,
                "message": response.text
            }
    except requests.RequestException as e:
        return {
            "error": "network_error",
            "message": str(e)
        }

# search_leads
def search_leads(search_params: dict) -> dict:
    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # This endpoint is not public — replace with actual endpoint once whitelisted
    url = f"{base_url}/salesNavigatorLeadSearch"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.post(url, headers=headers, json=search_params)
        if response.ok:
            return response.json()
        elif response.status_code == 403:
            return {
                "error": 403,
                "message": "Access denied – requires scope: r_sales_nav_leads"
            }
        else:
            return {
                "error": response.status_code,
                "message": response.text
            }
    except requests.RequestException as e:
        return {
            "error": "network_error",
            "message": str(e)
        }
    
#search_accounts
def search_accounts(search_params: dict) -> dict:
    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — LinkedIn exposes actual endpoints only to approved partners
    url = f"{base_url}/salesNavigatorAccountSearch"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.post(url, headers=headers, json=search_params)
        if response.ok:
            return response.json()
        elif response.status_code == 403:
            return {
                "error": 403,
                "message": "Access denied – requires scope: r_sales_nav_accounts"
            }
        else:
            return {
                "error": response.status_code,
                "message": response.text
            }
    except requests.RequestException as e:
        return {
            "error": "network_error",
            "message": str(e)
        }
    
#get_lead_recommendations
def get_lead_recommendations(account_id: str) -> dict:
    if not account_id:
        return {"error": 400, "message": "Missing required parameter: account_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint – real access only for approved partners
    url = f"{base_url}/salesNavigatorLeadRecommendations"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        payload = {
            "accountId": account_id,
            "q": "account"
        }
        response = requests.post(url, headers=headers, json=payload)

        if response.ok:
            return response.json()
        elif response.status_code == 403:
            return {
                "error": 403,
                "message": "Access denied – requires scope: r_sales_nav_leads"
            }
        else:
            return {
                "error": response.status_code,
                "message": response.text
            }
    except requests.RequestException as e:
        return {
            "error": "network_error",
            "message": str(e)
        }

#get_account_recommendations
def get_account_recommendations(user_id: str) -> dict:
    if not user_id:
        return {"error": 400, "message": "Missing required parameter: user_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint – actual access requires approved partner status
    url = f"{base_url}/salesNavigatorAccountRecommendations"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    payload = {
        "userId": user_id,
        "q": "user"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.ok:
            return response.json()
        elif response.status_code == 403:
            return {
                "error": 403,
                "message": "Access denied – requires scope: r_sales_nav_accounts"
            }
        else:
            return {
                "error": response.status_code,
                "message": response.text
            }
    except requests.RequestException as e:
        return {
            "error": "network_error",
            "message": str(e)
        }

#create_lead_list
def create_lead_list(name: str, description: str) -> dict:
    if not name:
        return {"error": 400, "message": "Missing required field: name"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — replace with official one if you're a partner
    url = f"{base_url}/salesNavigatorLeadLists"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    payload = {
        "name": name,
        "description": description
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.ok:
            return response.json()
        elif response.status_code == 403:
            return {
                "error": 403,
                "message": "Access denied – requires scope: rw_sales_nav"
            }
        else:
            return {
                "error": response.status_code,
                "message": response.text
            }
    except requests.RequestException as e:
        return {
            "error": "network_error",
            "message": str(e)
        }
    
#get_lead_lists
def get_lead_lists(user_id: str) -> dict:
    if not user_id:
        return {"error": 400, "message": "Missing required parameter: user_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")
    url = f"{base_url}/salesNavigatorLeadLists?q=user&userId={user_id}"  # placeholder

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        else:
            # fallback for 400, 403, 404
            return mock_lead_lists(user_id)
    except requests.RequestException:
        return mock_lead_lists(user_id)

def mock_lead_lists(user_id: str) -> dict:
    return {
        "user_id": user_id,
        "lead_lists": [
            {"id": "list_001", "name": "Top CTO Prospects", "created_at": "2024-01-01"},
            {"id": "list_002", "name": "Enterprise Leads", "created_at": "2023-12-15"}
        ],
        "note": "Mock data – requires r_sales_nav_leads and Sales Navigator partner access."
    }

#add_lead_to_list
def add_lead_to_list(lead_id: str, list_id: str) -> dict:
    if not all([lead_id, list_id]):
        return {"error": 400, "message": "Missing required lead_id or list_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint (not publicly available without partner access)
    url = f"{base_url}/salesNavigatorLeadLists/{list_id}/leads"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    payload = {
        "lead": lead_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.ok:
            return response.json()
        elif response.status_code in [403, 404, 400]:
            return mock_add_lead_to_list(lead_id, list_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}

def mock_add_lead_to_list(lead_id: str, list_id: str) -> dict:
    return {
        "lead_id": lead_id,
        "list_id": list_id,
        "status": "success",
        "note": "Mock response — real API requires Sales Navigator access with rw_sales_nav scope."
    }

#remove_lead_from_list
def remove_lead_from_list(lead_id: str, list_id: str) -> dict:
    if not all([lead_id, list_id]):
        return {"error": 400, "message": "Missing required lead_id or list_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint – Sales Navigator write APIs are private
    url = f"{base_url}/salesNavigatorLeadLists/{list_id}/leads/{lead_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.delete(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code in [403, 404, 400]:
            return mock_remove_lead_from_list(lead_id, list_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}

def mock_remove_lead_from_list(lead_id: str, list_id: str) -> dict:
    return {
        "lead_id": lead_id,
        "list_id": list_id,
        "status": "success",
        "note": "Mock response — real API requires Sales Navigator access with rw_sales_nav scope."
    }

#get_leads_in_list
def get_leads_in_list(list_id: str) -> dict:
    if not list_id:
        return {"error": 400, "message": "Missing required parameter: list_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — only available to partner apps
    url = f"{base_url}/salesNavigatorLeadLists/{list_id}/leads"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code in [403, 404, 400]:
            return mock_get_leads_in_list(list_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}

def mock_get_leads_in_list(list_id: str) -> dict:
    return {
        "list_id": list_id,
        "leads": [
            {
                "id": "urn:li:lead:mock001",
                "name": "Alice Johnson",
                "title": "CTO",
                "company": "MockTech Inc"
            },
            {
                "id": "urn:li:lead:mock002",
                "name": "Bob Lee",
                "title": "VP of Engineering",
                "company": "ExampleSoft"
            }
        ],
        "note": "Mock response — real API requires r_sales_nav_leads scope and partner access."
    }

#create_account_list
def create_account_list(name: str, description: str) -> dict:
    if not name or not description:
        return {"error": 400, "message": "Missing required fields: name and description"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint – only available to Sales Navigator partners
    url = f"{base_url}/salesNavigatorAccountLists"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    payload = {
        "name": name,
        "description": description
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.ok:
            return response.json()
        elif response.status_code in [403, 404, 400]:
            return mock_create_account_list(name, description)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}

def mock_create_account_list(name: str, description: str) -> dict:
    return {
        "account_list_id": "mock_account_list_001",
        "name": name,
        "description": description,
        "status": "success",
        "note": "Mock response — real API requires Sales Navigator access with rw_sales_nav scope."
    }

#get_account_lists
def get_account_lists(user_id: str = None) -> dict:
    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — only available to LinkedIn partners
    url = f"{base_url}/salesNavigatorAccountLists"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code in [403, 404, 400]:
            return mock_get_account_lists(user_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}

def mock_get_account_lists(user_id: str = "urn:li:person:default_user") -> dict:
    return {
        "user_id": user_id,
        "account_lists": [
            {
                "id": "account_list_001",
                "name": "Top Enterprise Accounts",
                "created_at": "2024-03-01"
            },
            {
                "id": "account_list_002",
                "name": "Q1 Prospects",
                "created_at": "2024-01-10"
            }
        ],
        "note": "Mock response — real API requires r_sales_nav_accounts scope and partner access."
    }

#add_account_to_list
def add_account_to_list(account_id: str, list_id: str) -> dict:
    if not account_id or not list_id:
        return {"error": 400, "message": "Missing required fields: account_id and list_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint – only available to LinkedIn partner apps
    url = f"{base_url}/salesNavigatorAccountLists/{list_id}/accounts"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    payload = {
        "account": account_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.ok:
            return response.json()
        elif response.status_code in [403, 404, 400]:
            return mock_add_account_to_list(account_id, list_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}

def mock_add_account_to_list(account_id: str, list_id: str) -> dict:
    return {
        "account_id": account_id,
        "list_id": list_id,
        "status": "success",
        "note": "Mock response — real API requires Sales Navigator access with rw_sales_nav scope."
    }

#remove_account_from_list
def remove_account_from_list(account_id: str, list_id: str) -> dict:
    if not account_id or not list_id:
        return {"error": 400, "message": "Missing required fields: account_id and list_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — real endpoint only available to LinkedIn partners
    url = f"{base_url}/salesNavigatorAccountLists/{list_id}/accounts/{account_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.delete(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code in [403, 404, 400]:
            return mock_remove_account_from_list(account_id, list_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}

def mock_remove_account_from_list(account_id: str, list_id: str) -> dict:
    return {
        "account_id": account_id,
        "list_id": list_id,
        "status": "success",
        "note": "Mock response — real API requires Sales Navigator access with rw_sales_nav scope."
    }

#get_accounts_in_list
def get_accounts_in_list(list_id: str) -> dict:
    if not list_id:
        return {"error": 400, "message": "Missing required field: list_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — only available to Sales Navigator partners
    url = f"{base_url}/salesNavigatorAccountLists/{list_id}/accounts"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code in [403, 404, 400]:
            return mock_get_accounts_in_list(list_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return mock_get_accounts_in_list(list_id)

def mock_get_accounts_in_list(list_id: str) -> dict:
    return {
        "list_id": list_id,
        "accounts": [
            {
                "id": "urn:li:organization:mock001",
                "name": "Tech Innovators Inc.",
                "industry": "Software",
                "location": "San Francisco, CA"
            },
            {
                "id": "urn:li:organization:mock002",
                "name": "Green Energy Corp.",
                "industry": "Renewables",
                "location": "Austin, TX"
            }
        ],
        "note": "Mock response — real API requires r_sales_nav_accounts scope and partner access."
    }

#sync_lead_to_crm
def sync_lead_to_crm(lead_id: str, crm_payload: dict) -> dict:
    if not lead_id or not crm_payload:
        return {"error": 400, "message": "Missing required lead_id or CRM payload"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — partner-only functionality
    url = f"{base_url}/salesNavigatorLeads/{lead_id}/crmSync"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.post(url, headers=headers, json=crm_payload)
        if response.ok:
            return response.json()
        elif response.status_code in [400, 403, 404]:
            return mock_sync_lead_to_crm(lead_id, crm_payload)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return mock_sync_lead_to_crm(lead_id, crm_payload)

def mock_sync_lead_to_crm(lead_id: str, crm_payload: dict) -> dict:
    return {
        "lead_id": lead_id,
        "crm_data": crm_payload,
        "status": "synced",
        "note": "Mock response — actual CRM sync requires LinkedIn partner access with rw_sales_nav scope."
    }

#get_crm_sync_status
def get_crm_sync_status(lead_id: str) -> dict:
    if not lead_id:
        return {"error": 400, "message": "Missing required field: lead_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Hypothetical endpoint — only available to approved partners
    url = f"{base_url}/salesNavigatorLeads/{lead_id}/crmSyncStatus"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code in [400, 403, 404]:
            return mock_get_crm_sync_status(lead_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return mock_get_crm_sync_status(lead_id)

def mock_get_crm_sync_status(lead_id: str) -> dict:
    return {
        "lead_id": lead_id,
        "status": "synced",
        "synced_at": "2024-12-01T14:45:00Z",
        "crm_owner": "sales_rep_1",
        "crm_id": "crm-78910",
        "note": "Mock response — actual API requires r_sales_nav scope and partner access."
    }

#get_engagement_metrics
def get_engagement_metrics(lead_id: str) -> dict:
    if not lead_id:
        return {"error": 400, "message": "Missing required field: lead_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — partner-only API
    url = f"{base_url}/salesNavigatorLeads/{lead_id}/engagementMetrics"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code in [400, 403, 404]:
            return mock_get_engagement_metrics(lead_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return mock_get_engagement_metrics(lead_id)

def mock_get_engagement_metrics(lead_id: str) -> dict:
    return {
        "lead_id": lead_id,
        "profile_views": 12,
        "inmail_messages_sent": 3,
        "connection_requests_sent": 2,
        "last_engaged_at": "2024-12-01T10:30:00Z",
        "note": "Mock response — actual API requires r_sales_nav scope and partner access."
    }

#get_inmail_quota
def get_inmail_quota(user_id: str) -> dict:
    if not user_id:
        return {"error": 400, "message": "Missing required field: user_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — available to Sales Navigator partners
    url = f"{base_url}/salesNavigatorUsers/{user_id}/inmailQuota"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code in [400, 403, 404]:
            return mock_get_inmail_quota(user_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException:
        return mock_get_inmail_quota(user_id)

def mock_get_inmail_quota(user_id: str) -> dict:
    return {
        "user_id": user_id,
        "quota_remaining": 42,
        "quota_used": 8,
        "quota_total": 50,
        "reset_date": "2024-12-01",
        "note": "Mock response — actual API requires r_sales_nav scope and partner access."
    }

#send_inmail
def send_inmail(lead_id: str, subject: str, body: str) -> dict:
    if not all([lead_id, subject, body]):
        return {"error": 400, "message": "Missing one or more required fields: lead_id, subject, body"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — real endpoint available only to Sales Navigator partners
    url = f"{base_url}/salesNavigatorInmailMessages"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    payload = {
        "lead": lead_id,
        "subject": subject,
        "body": body
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.ok:
            return response.json()
        elif response.status_code in [400, 403, 404]:
            return mock_send_inmail(lead_id, subject, body)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return mock_send_inmail(lead_id, subject, body)

def mock_send_inmail(lead_id: str, subject: str, body: str) -> dict:
    return {
        "lead_id": lead_id,
        "message_id": "mock-inmail-001",
        "subject": subject,
        "body": body,
        "status": "sent",
        "note": "Mock response — real API requires rw_sales_nav scope and LinkedIn partner access."
    }

#get_sent_inmails
def get_sent_inmails(user_id: str) -> dict:
    if not user_id:
        return {"error": 400, "message": "Missing required field: user_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — LinkedIn provides this to partners only
    url = f"{base_url}/salesNavigatorUsers/{user_id}/sentInmails"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code in [400, 403, 404]:
            return mock_get_sent_inmails(user_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException:
        return mock_get_sent_inmails(user_id)

def mock_get_sent_inmails(user_id: str) -> dict:
    return {
        "user_id": user_id,
        "sent_inmails": [
            {
                "message_id": "mock-inmail-001",
                "lead_id": "urn:li:lead:mock123",
                "subject": "Let's Connect",
                "body": "Hi, would love to learn more about your work.",
                "sent_at": "2024-12-01T14:00:00Z"
            },
            {
                "message_id": "mock-inmail-002",
                "lead_id": "urn:li:lead:mock456",
                "subject": "Partnership Opportunity",
                "body": "We’re exploring collaboration opportunities.",
                "sent_at": "2024-12-03T09:15:00Z"
            }
        ],
        "note": "Mock response — actual API requires r_sales_nav scope and partner access."
    }

#track_inmail_response
def track_inmail_response(message_id: str) -> dict:
    if not message_id:
        return {"error": 400, "message": "Missing required field: message_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — requires LinkedIn Sales Navigator partner access
    url = f"{base_url}/salesNavigatorInmailMessages/{message_id}/responseStatus"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code in [400, 403, 404]:
            return mock_track_inmail_response(message_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException:
        return mock_track_inmail_response(message_id)

def mock_track_inmail_response(message_id: str) -> dict:
    return {
        "message_id": message_id,
        "status": "responded",
        "responded_at": "2024-12-05T16:00:00Z",
        "note": "Mock response — actual API requires r_sales_nav scope and partner access."
    }

#get_smart_links
def get_smart_links(user_id: str) -> dict:
    if not user_id:
        return {"error": 400, "message": "Missing required field: user_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — real endpoint available only to approved partners
    url = f"{base_url}/salesNavigatorUsers/{user_id}/smartLinks"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code in [400, 403, 404]:
            return mock_get_smart_links(user_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException:
        return mock_get_smart_links(user_id)

def mock_get_smart_links(user_id: str) -> dict:
    return {
        "user_id": user_id,
        "smart_links": [
            {
                "id": "smartlink_001",
                "title": "Product Demo Video",
                "created_at": "2024-10-01",
                "url": "https://linkedin.com/smart-link/product-demo"
            },
            {
                "id": "smartlink_002",
                "title": "Case Study – SaaS Growth",
                "created_at": "2024-11-15",
                "url": "https://linkedin.com/smart-link/saas-case-study"
            }
        ],
        "note": "Mock response — actual API requires r_sales_nav scope and partner access."
    }

#create_smart_link
def create_smart_link(name: str, target_url: str) -> dict:
    if not name or not target_url:
        return {"error": 400, "message": "Missing required fields: name, target_url"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — real API only available for LinkedIn Sales Navigator partners
    url = f"{base_url}/salesNavigatorSmartLinks"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    payload = {
        "name": name,
        "targetUrl": target_url
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.ok:
            return response.json()
        elif response.status_code in [400, 403, 404]:
            return mock_create_smart_link(name, target_url)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException:
        return mock_create_smart_link(name, target_url)

def mock_create_smart_link(name: str, target_url: str) -> dict:
    return {
        "smart_link_id": "smartlink_mock_123",
        "name": name,
        "target_url": target_url,
        "status": "created",
        "created_at": "2025-06-03",
        "note": "Mock response — actual API requires rw_sales_nav scope and partner access."
    }

#get_smart_link_clicks
def get_smart_link_clicks(link_id: str) -> dict:
    if not link_id:
        return {"error": 400, "message": "Missing required field: link_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — real API is partner-only
    url = f"{base_url}/salesNavigatorSmartLinks/{link_id}/analytics"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code in [400, 403, 404]:
            return mock_get_smart_link_clicks(link_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException:
        return mock_get_smart_link_clicks(link_id)


def mock_get_smart_link_clicks(link_id: str) -> dict:
    return {
        "link_id": link_id,
        "clicks": 37,
        "unique_views": 28,
        "avg_time_on_page_sec": 95,
        "last_clicked_at": "2025-06-03T13:45:00Z",
        "note": "Mock response — actual API requires r_sales_nav scope and LinkedIn partner access."
    }


#get_team_link_insights
def get_team_link_insights(team_id: str) -> dict:
    if not team_id:
        return {"error": 400, "message": "Missing required field: team_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Hypothetical endpoint – real endpoint requires LinkedIn partner access
    url = f"{base_url}/salesNavigatorTeams/{team_id}/smartLinkInsights"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif current_app.config.get("USE_MOCK", True):
            return mock_get_team_link_insights(team_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}
def mock_get_team_link_insights(team_id: str) -> dict:
    return {
        "team_id": team_id,
        "total_clicks": 148,
        "unique_viewers": 96,
        "top_performers": [
            {"member_id": "urn:li:person:xyz001", "clicks": 40},
            {"member_id": "urn:li:person:xyz002", "clicks": 36}
        ],
        "note": "Mock response — real API requires r_sales_nav scope and LinkedIn partner access."
    }

#get_sales_preferences
def get_sales_preferences(user_id: str) -> dict:
    """
    Retrieves Sales Navigator preferences for a given user.
    Requires: r_sales_nav scope and LinkedIn partner access.
    """
    if not user_id:
        return {"error": 400, "message": "Missing required field: user_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Hypothetical endpoint — available only to Sales Navigator partners
    url = f"{base_url}/salesNavigatorPreferences?q=viewer&viewer={user_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif current_app.config.get("USE_MOCK", True):
            return mock_get_sales_preferences(user_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}

def mock_get_sales_preferences(user_id: str) -> dict:
    return {
        "user_id": user_id,
        "preferred_industries": ["Software", "Finance"],
        "notification_frequency": "weekly",
        "territories": ["North America", "Europe"],
        "note": "Mock response — real API requires r_sales_nav scope and LinkedIn partner access."
    }

#update_sales_preferences
def update_sales_preferences(user_id: str, preferences: dict) -> dict:
    
    if not user_id or not preferences:
        return {"error": 400, "message": "Missing user_id or preferences payload"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Hypothetical endpoint — LinkedIn restricts this to Sales Nav partners
    url = f"{base_url}/salesNavigatorPreferences?action=update&viewer={user_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=preferences)
        if response.ok:
            return response.json()
        elif current_app.config.get("USE_MOCK", True):
            return mock_update_sales_preferences(user_id, preferences)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}
def mock_update_sales_preferences(user_id: str, preferences: dict) -> dict:
    return {
        "user_id": user_id,
        "updated_preferences": preferences,
        "status": "success",
        "note": "Mock response — real API requires rw_sales_nav scope and LinkedIn partner access."
    }

#get_saved_searches
def get_saved_searches(user_id: str) -> dict:
    if not user_id:
        return {"error": 400, "message": "Missing required field: user_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder URL – real endpoint is accessible to approved partners only
    url = f"{base_url}/salesNavigatorSavedSearches?q=viewer&viewer={user_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif current_app.config.get("USE_MOCK", True):
            return mock_get_saved_searches(user_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}
def mock_get_saved_searches(user_id: str) -> dict:
    return {
        "user_id": user_id,
        "saved_searches": [
            {
                "id": "search_001",
                "name": "CTOs in FinTech",
                "type": "lead",
                "created_at": "2024-10-01"
            },
            {
                "id": "search_002",
                "name": "Series A SaaS Startups",
                "type": "account",
                "created_at": "2024-11-12"
            }
        ],
        "note": "Mock response — real API requires r_sales_nav scope and LinkedIn partner access."
    }

#run_saved_search
def run_saved_search(search_id: str) -> dict:
    if not search_id:
        return {"error": 400, "message": "Missing required field: search_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — actual endpoint restricted to partners
    url = f"{base_url}/salesNavigatorSavedSearchResults?q=search&search={search_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif current_app.config.get("USE_MOCK", True):
            return mock_run_saved_search(search_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}

def mock_run_saved_search(search_id: str) -> dict:
    return {
        "search_id": search_id,
        "results": [
            {
                "id": "urn:li:lead:001",
                "name": "John Doe",
                "title": "CTO",
                "company": "FinTech Global"
            },
            {
                "id": "urn:li:lead:002",
                "name": "Jane Smith",
                "title": "VP Engineering",
                "company": "NextGen AI"
            }
        ],
        "note": "Mock response — actual API requires r_sales_nav scope and partner access."
    }

#delete_saved_search
def delete_saved_search(search_id: str) -> dict:
    if not search_id:
        return {"error": 400, "message": "Missing required field: search_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — only available to Sales Navigator partners
    url = f"{base_url}/salesNavigatorSavedSearches/{search_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.delete(url, headers=headers)
        if response.ok:
            return {"status": "deleted", "search_id": search_id}
        elif current_app.config.get("USE_MOCK", True):
            return mock_delete_saved_search(search_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}

def mock_delete_saved_search(search_id: str) -> dict:
    return {
        "search_id": search_id,
        "status": "deleted",
        "note": "Mock response — actual API requires rw_sales_nav scope and LinkedIn partner access."
    }

#follow_lead
def follow_lead(lead_id: str) -> dict:
    """
    Follows a lead in Sales Navigator.
    Requires: rw_sales_nav scope and LinkedIn partner access.
    """
    if not lead_id:
        return {"error": 400, "message": "Missing required field: lead_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — real endpoint available to approved partners only
    url = f"{base_url}/salesNavigatorLeads?action=follow"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    payload = {
        "lead": lead_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.ok:
            return response.json()
        elif current_app.config.get("USE_MOCK", True):
            return mock_follow_lead(lead_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}
def mock_follow_lead(lead_id: str) -> dict:
    return {
        "lead_id": lead_id,
        "status": "followed",
        "note": "Mock response — real API requires rw_sales_nav scope and partner access."
    }

#unfollow_lead
def unfollow_lead(lead_id: str) -> dict:
    if not lead_id:
        return {"error": 400, "message": "Missing required field: lead_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — real endpoint available to approved partners only
    url = f"{base_url}/salesNavigatorLeads?action=unfollow"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    payload = {
        "lead": lead_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.ok:
            return response.json()
        elif current_app.config.get("USE_MOCK", True):
            return mock_unfollow_lead(lead_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}
def mock_unfollow_lead(lead_id: str) -> dict:
    return {
        "lead_id": lead_id,
        "status": "unfollowed",
        "note": "Mock response — real API requires rw_sales_nav scope and partner access."
    }

#follow_account
def follow_account(account_id: str) -> dict:
    if not account_id:
        return {"error": 400, "message": "Missing required field: account_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — real API requires LinkedIn partner access
    url = f"{base_url}/salesNavigatorAccounts?action=follow"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    payload = {
        "account": account_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.ok:
            return response.json()
        elif current_app.config.get("USE_MOCK", True):
            return mock_follow_account(account_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}
def mock_follow_account(account_id: str) -> dict:
    return {
        "account_id": account_id,
        "status": "followed",
        "note": "Mock response — real API requires rw_sales_nav scope and LinkedIn partner access."
    }

#unfollow_account
def unfollow_account(account_id: str) -> dict:
    if not account_id:
        return {"error": 400, "message": "Missing required field: account_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — actual API only available to LinkedIn Sales Navigator partners
    url = f"{base_url}/salesNavigatorAccounts?action=unfollow"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    payload = {
        "account": account_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.ok:
            return response.json()
        elif current_app.config.get("USE_MOCK", True):
            return mock_unfollow_account(account_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}
def mock_unfollow_account(account_id: str) -> dict:
    return {
        "account_id": account_id,
        "status": "unfollowed",
        "note": "Mock response — real API requires rw_sales_nav scope and LinkedIn partner access."
    }

#get_alerts
def get_alerts(user_id: str) -> dict:
    if not user_id:
        return {"error": 400, "message": "Missing required field: user_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint – real endpoint available only to Sales Navigator partners
    url = f"{base_url}/salesNavigatorAlerts?q=viewer&viewer={user_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif current_app.config.get("USE_MOCK", True):
            return mock_get_alerts(user_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}
def mock_get_alerts(user_id: str) -> dict:
    return {
        "user_id": user_id,
        "alerts": [
            {
                "id": "alert_001",
                "type": "Lead Activity",
                "message": "Lead John Smith has a new job title.",
                "date": "2024-12-01T09:00:00Z"
            },
            {
                "id": "alert_002",
                "type": "Company News",
                "message": "Acme Inc. announced a new acquisition.",
                "date": "2024-12-02T15:30:00Z"
            }
        ],
        "note": "Mock response — actual API requires r_sales_nav scope and partner access."
    }

#dismiss_alert
def dismiss_alert(alert_id: str) -> dict:
    if not alert_id:
        return {"error": 400, "message": "Missing required field: alert_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — actual endpoint requires partner access
    url = f"{base_url}/salesNavigatorAlerts/{alert_id}?action=dismiss"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.post(url, headers=headers)
        if response.ok:
            return response.json()
        elif current_app.config.get("USE_MOCK", True):
            return mock_dismiss_alert(alert_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}
def mock_dismiss_alert(alert_id: str) -> dict:
    return {
        "alert_id": alert_id,
        "status": "dismissed",
        "note": "Mock response — real API requires rw_sales_nav scope and LinkedIn partner access."
    }

#get_usage_analytics
def get_usage_analytics(user_id: str) -> dict:

    if not user_id:
        return {"error": 400, "message": "Missing required field: user_id"}

    access_token = current_app.config.get("LINKEDIN_ACCESS_TOKEN")
    base_url = current_app.config.get("LINKEDIN_API_BASE_URL", "https://api.linkedin.com/v2")

    # Placeholder endpoint — real one is available to LinkedIn Sales Navigator partners
    url = f"{base_url}/salesNavigatorUsageAnalytics?q=viewer&viewer={user_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-RestLi-Protocol-Version": "2.0.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif current_app.config.get("USE_MOCK", True):
            return mock_get_usage_analytics(user_id)
        else:
            return {"error": response.status_code, "message": response.text}
    except requests.RequestException as e:
        return {"error": "network_error", "message": str(e)}
def mock_get_usage_analytics(user_id: str) -> dict:
    return {
        "user_id": user_id,
        "total_searches": 56,
        "leads_saved": 32,
        "inmails_sent": 18,
        "profile_views": 75,
        "note": "Mock response — actual API requires r_sales_nav scope and LinkedIn partner access."
    }
