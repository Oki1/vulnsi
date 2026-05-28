from flask import Flask
import os

def create_app():
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    app.secret_key = os.urandom(32)
    
    from .config import AppConfig
    from .storage import todos_storage, user_profiles, teams_storage, notifications_storage
    
    app_config = AppConfig()
    
    app.config['APP_CONFIG'] = app_config
    app.config['TODOS_STORAGE'] = todos_storage
    app.config['USER_PROFILES'] = user_profiles
    app.config['TEAMS_STORAGE'] = teams_storage
    app.config['NOTIFICATIONS_STORAGE'] = notifications_storage
    
    from .routes import register_blueprints
    register_blueprints(app)
    
    return app

app = create_app()

