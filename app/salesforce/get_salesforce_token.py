import requests

# === CONFIGURATION ===
login_url = "https://login.salesforce.com"  # Use https://test.salesforce.com for sandbox
client_id = "3MVG9.Houp75EVdbqEre7cMA7SOWIDbeHJSy_CyVx2126HjbcLhwbPEmpTrB_RORsXoA020_QNlcKgLHRD3VK"
client_secret = "F09FBC455230A197D67B7F2DFD42115BABC66D2609FDB70760513D625C9F309F"
username = "munna.kuet.me-g0bv@force.com"
password = "Munna.6940"
security_token = ""  # Leave empty if IP is whitelisted

# Combine password + security token if needed
full_password = password

# === TOKEN REQUEST ===
url = f"{login_url}/services/oauth2/token"
payload = {
    "grant_type": "password",
    "client_id": client_id,
    "client_secret": client_secret,
    "username": username,
    "password": full_password
}

# Send request
response = requests.post(url, data=payload)

# Output response
print("Status:", response.status_code)
print("Response:", response.json())
