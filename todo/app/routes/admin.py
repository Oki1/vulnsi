from flask import Blueprint, session, render_template, redirect, url_for, flash
from ..utils import apply_config_overrides
from ..config import FLAG

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_panel():
    from flask import current_app
    app_config = current_app.config['APP_CONFIG']
    
    apply_config_overrides()
    
    if not app_config.admin_access:
        flash('Access denied. Administrative privileges required.', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    template_data = {
        'app_config': app_config,
        'session_info': {k: v for k, v in session.items() if k != 'profile'},
        'flag_data': FLAG
    }
    
    return render_template('admin.html', **template_data)
