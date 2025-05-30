from flask import Flask
from app.slack.slack_routes import slack_bp  # Add other blueprints here
from app.notion.notion_routes import notion_bp 
from app.teams.teams_routes import teams_bp
from app.asana.asana_routes import asana_bp 

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(slack_bp, url_prefix='/api/slack')
    app.register_blueprint(notion_bp, url_prefix='/api/notion') 
    app.register_blueprint(teams_bp, url_prefix='/api/teams') 
    app.register_blueprint(asana_bp, url_prefix='/api/asana') 
    
    return app
