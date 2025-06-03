import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    #Slack
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"
    
    #Notion
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    NOTION_VERSION = os.getenv("NOTION_VERSION", "2022-06-28")
    NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
    NOTION_BASE_URL = "https://api.notion.com/v1"

     #Microsoft Teams (Graph API)
    MS_CLIENT_ID = os.getenv("MS_CLIENT_ID")
    MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
    MS_TENANT_ID = os.getenv("MS_TENANT_ID")
    MS_GRAPH_API_BASE_URL = "https://graph.microsoft.com/v1.0"

    #Asana
    ASANA_PAT = os.getenv("ASANA_PAT")
    ASANA_BASE_URL = "https://app.asana.com/api/1.0"

    #Checkup
    CLICKUP_API_TOKEN = os.getenv("CLICKUP_API_TOKEN")
    CLICKUP_API_BASE_URL = "https://api.clickup.com/api/v2"

    #Jira
    JIRA_EMAIL = os.getenv("JIRA_EMAIL")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
    JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")

    #Monday
    MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
    MONDAY_API_URL = "https://api.monday.com/v2"

    #Salesforce
    SALESFORCE_CLIENT_ID = os.getenv("SALESFORCE_CLIENT_ID")
    SALESFORCE_CLIENT_SECRET = os.getenv("SALESFORCE_CLIENT_SECRET")
    SALESFORCE_USERNAME = os.getenv("SALESFORCE_USERNAME")
    SALESFORCE_PASSWORD = os.getenv("SALESFORCE_PASSWORD")
    ACCESS_TOKEN = os.getenv("SALESFORCE_SECURITY_TOKEN")
    SALESFORCE_INSTANCE_URL = os.getenv("SALESFORCE_INSTANCE_URL")

    #Linkedin
    LINKEDIN_API_BASE_URL = "https://api.linkedin.com/v2"
    LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")