from flask import Blueprint, session, jsonify
from ..utils import apply_config_overrides
from ..config import FLAG

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/system/status')
def system_status():
    from flask import current_app
    app_config = current_app.config['APP_CONFIG']
    
    apply_config_overrides()
    return jsonify({
        'status': 'operational',
        'version': '3.2.1',
        'debug_mode': app_config.debug_mode,
        'admin_access': app_config.admin_access,
        'maintenance_mode': app_config.maintenance_mode,
        'feature_flags': app_config.feature_flags,
        'session_config': session.get('config_overrides', {}),
        'user_profile': session.get('profile', {})
    })

@api_bp.route('/api/admin/flag')
def admin_flag_endpoint():
    from flask import current_app
    app_config = current_app.config['APP_CONFIG']
    
    apply_config_overrides()
    if app_config.admin_access:
        return jsonify({
            'flag': FLAG,
            'message': 'Administrative access confirmed - flag retrieved successfully',
            'challenge_name': 'taskflow',
            'difficulty': 'middle'
        })
    else:
        return jsonify({'error': 'Administrative privileges required'}), 403
