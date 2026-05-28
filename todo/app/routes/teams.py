from flask import Blueprint, session, render_template
from ..utils import apply_config_overrides
from ..config import FLAG

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/teams')
def teams():
    from flask import current_app
    app_config = current_app.config['APP_CONFIG']
    
    apply_config_overrides()
    template_data = {
        'app_config': app_config,
        'session_info': {k: v for k, v in session.items() if k != 'profile'},
        'flag_data': FLAG if app_config.admin_access else None
    }
    
    return render_template('teams.html', **template_data)
