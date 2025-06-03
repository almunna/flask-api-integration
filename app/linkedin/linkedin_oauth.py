import os
import webbrowser
import requests
import secrets
import urllib.parse
import json
from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Required for Flask session

# LinkedIn App credentials
CLIENT_ID = "865urzyji9ouwz"
CLIENT_SECRET = "WPL_AP1.nnRxkeBr6uXEH0UB.fH9Zrg=="
REDIRECT_URI = "http://localhost:5000/linkedin/callback"
SCOPES = "profile openid w_member_social email"

@app.route("/")
def start_oauth():
    state = secrets.token_urlsafe(16)
    session['oauth_state'] = state

    encoded_redirect_uri = urllib.parse.quote(REDIRECT_URI, safe="")
    encoded_scope = urllib.parse.quote(SCOPES)

    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={encoded_redirect_uri}"
        f"&scope={encoded_scope}"
        f"&state={state}"
    )

    print("🔗 LinkedIn Auth URL:", auth_url)
    webbrowser.open(auth_url)
    return "Opened LinkedIn login page in browser..."

@app.route("/linkedin/callback")
def linkedin_callback():
    code = request.args.get("code")
    returned_state = request.args.get("state")
    expected_state = session.get("oauth_state")

    if not code:
        return "❌ No code received."

    if not returned_state or returned_state != expected_state:
        return "❌ Invalid or mismatched state parameter. Possible CSRF attempt."

    # Exchange code for token
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(token_url, data=data)
    token_data = response.json()

    if "access_token" in token_data:
        access_token = token_data["access_token"]

        # Save token JSON
        with open("linkedin_token.json", "w") as f:
            json.dump(token_data, f, indent=2)

        # Fetch profile and email
        headers = {"Authorization": f"Bearer {access_token}"}

        profile_resp = requests.get("https://api.linkedin.com/v2/me", headers=headers)
        email_resp = requests.get(
            "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))",
            headers=headers
        )

        profile = profile_resp.json()
        email_data = email_resp.json()
        email = email_data["elements"][0]["handle~"]["emailAddress"]

        # Optional: Extract name
        first_name = profile.get("localizedFirstName", "")
        last_name = profile.get("localizedLastName", "")

        return (
            f"✅ Access token retrieved and saved.<br><br>"
            f"<b>Name:</b> {first_name} {last_name}<br>"
            f"<b>Email:</b> {email}<br><br>"
            f"<pre>{json.dumps(profile, indent=2)}</pre>"
        )
    else:
        return f"❌ Failed to get token: {token_data}"

if __name__ == "__main__":
    print("🌐 Server running at http://localhost:5000/")
    app.run(port=5000)


