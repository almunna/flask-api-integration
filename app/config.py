import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"
    
