from flask import Flask
from app.slack.slack_routes import slack_bp  # Add other blueprints here
from app.notion.notion_routes import notion_bp 
from app.teams.teams_routes import teams_bp
from app.asana.asana_routes import asana_bp 
from app.clickup.clickup_routes import clickup_bp 
from app.jira.jira_routes import jira_bp
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register blueprints
    app.register_blueprint(slack_bp, url_prefix='/api/slack')
    app.register_blueprint(notion_bp, url_prefix='/api/notion') 
    app.register_blueprint(teams_bp, url_prefix='/api/teams') 
    app.register_blueprint(asana_bp, url_prefix='/api/asana') 
    app.register_blueprint(clickup_bp, url_prefix='/api/clickup')
    app.register_blueprint(jira_bp, url_prefix='/api/jira') 
    
    return app
