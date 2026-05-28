from flask import Blueprint, session, render_template
from ..utils import apply_config_overrides
from ..config import FLAG

analytics_bp = Blueprint('analytics', __name__)

def generate_analytics_data():
    return {
        'tasks_completed_today': 12,
        'productivity_score': 87,
        'weekly_trend': '+15%',
        'team_performance': 'Above Average',
        'upcoming_deadlines': 3
    }

@analytics_bp.route('/analytics')
def analytics():
    from flask import current_app
    app_config = current_app.config['APP_CONFIG']
    
    apply_config_overrides()
    analytics_data = generate_analytics_data()
    
    template_data = {
        'analytics': analytics_data,
        'app_config': app_config,
        'session_info': {k: v for k, v in session.items() if k != 'profile'},
        'flag_data': FLAG if app_config.admin_access else None
    }
    
    return render_template('analytics.html', **template_data)
