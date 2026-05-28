from flask import Blueprint, session, render_template
import uuid
from ..utils import apply_config_overrides
from ..config import FLAG

dashboard_bp = Blueprint('dashboard', __name__)

def generate_analytics_data():
    return {
        'tasks_completed_today': 12,
        'productivity_score': 87,
        'weekly_trend': '+15%',
        'team_performance': 'Above Average',
        'upcoming_deadlines': 3
    }

@dashboard_bp.route('/')
def dashboard():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['profile'] = {}
    
    from flask import current_app
    app_config = current_app.config['APP_CONFIG']
    todos_storage = current_app.config['TODOS_STORAGE']
    
    apply_config_overrides()
    
    user_id = session['user_id']
    user_tasks = todos_storage.get(user_id, [])
    analytics = generate_analytics_data()
    
    template_data = {
        'user_tasks': user_tasks[:5],
        'recent_tasks': user_tasks,
        'analytics': analytics,
        'app_config': app_config,
        'session_info': {k: v for k, v in session.items() if k != 'profile'},
        'flag_data': FLAG if app_config.admin_access else None
    }
    
    return render_template('dashboard.html', **template_data)
