from flask import Flask
from dotenv import load_dotenv
import os
from app.slack.slack_routes import slack_bp  # Add other blueprints here
from app.notion.notion_routes import notion_bp 
from app.teams.teams_routes import teams_bp
from app.asana.asana_routes import asana_bp 
from app.clickup.clickup_routes import clickup_bp 
from app.jira.jira_routes import jira_bp
from app.config import Config
from app.monday.monday_routes import monday_bp
from app.salesforce.salesforce_routes import salesforce_bp
from app.linkedin.linkedin_routes import linkedin_bp
from app.linkedin_sales.linkedin_routes import linkedin_sales_bp
from app.discord.discord_routes import discord_bp
from app.instagram.instagram_routes import instagram_bp
from app.facebook.facebook_routes import facebook_bp
from app.whatsapp.whatsapp_routes import whatsapp_bp


load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_insecure_dev_key")
    
    # Register blueprints
    app.register_blueprint(slack_bp, url_prefix='/api/slack')
    app.register_blueprint(notion_bp, url_prefix='/api/notion') 
    app.register_blueprint(teams_bp, url_prefix='/api/teams') 
    app.register_blueprint(asana_bp, url_prefix='/api/asana') 
    app.register_blueprint(clickup_bp, url_prefix='/api/clickup')
    app.register_blueprint(jira_bp, url_prefix='/api/jira') 
    app.register_blueprint(monday_bp, url_prefix='/api/monday')
    app.register_blueprint(salesforce_bp, url_prefix='/api/salesforce')
    app.register_blueprint(linkedin_bp, url_prefix='/api/linkedin')
    app.register_blueprint(linkedin_sales_bp, url_prefix='/api/linkedin-sales')
    app.register_blueprint(discord_bp, url_prefix="/api/discord")
    app.register_blueprint(instagram_bp, url_prefix="/api/instagram")
    app.register_blueprint(facebook_bp, url_prefix='/api/facebook')
    app.register_blueprint(whatsapp_bp, url_prefix='/api/whatsapp')


    return app
