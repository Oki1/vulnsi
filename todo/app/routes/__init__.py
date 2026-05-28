from .dashboard import dashboard_bp
from .tasks import tasks_bp
from .analytics import analytics_bp
from .teams import teams_bp
from .settings import settings_bp
from .admin import admin_bp
from .api import api_bp
from .health import health_bp

def register_blueprints(app):
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(health_bp)
