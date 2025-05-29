import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    #slack
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"
    
    #notion
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    NOTION_VERSION = os.getenv("NOTION_VERSION", "2022-06-28")
    NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
    NOTION_BASE_URL = "https://api.notion.com/v1"