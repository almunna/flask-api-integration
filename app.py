from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize Flask app and Slack client
app = Flask(__name__)
slack_token = os.getenv("SLACK_BOT_TOKEN")
slack_client = WebClient(token=slack_token)

@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.get_json()
    channel = data.get("channel")
    text = data.get("text")

    if not channel or not text:
        return jsonify({"error": "channel and text are required"}), 400

    try:
        response = slack_client.chat_postMessage(
            channel=channel,
            text=text
        )
        return jsonify({
            "ok": response["ok"],
            "channel": response["channel"],
            "ts": response["ts"],
            "message": response["message"]
        })
    except SlackApiError as e:
        return jsonify({
            "error": e.response["error"]
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
