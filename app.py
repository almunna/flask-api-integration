from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

# Render loads env vars from dashboard or render.yaml
slack_token = os.getenv("SLACK_BOT_TOKEN")

app = Flask(__name__)
slack_client = WebClient(token=slack_token)

@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.get_json()
    channel = data.get("channel")
    text = data.get("text")

    if not channel or not text:
        return jsonify({"error": "channel and text are required"}), 400

    try:
        response = slack_client.chat_postMessage(channel=channel, text=text)
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

# Only for local development — DO NOT USE in production manually
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
