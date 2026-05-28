from flask import Blueprint, session, render_template, request, jsonify, redirect, url_for, flash
import json
from ..utils import apply_config_overrides, merge_user_preferences
from ..config import FLAG
import sys

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings')
def settings():
    from flask import current_app
    app_config = current_app.config['APP_CONFIG']
    
    apply_config_overrides()
    
    template_data = {
        'app_config': app_config,
        'current_profile': session.get('profile', {}),
        'session_info': {k: v for k, v in session.items() if k != 'profile'},
        'flag_data': FLAG if app_config.admin_access else None
    }
    
    return render_template('settings.html', **template_data)

@settings_bp.route('/update_settings', methods=['POST'])
def update_settings():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    section = request.form.get('section', 'general')
    
    if section == 'general':
        profile = session.get('profile', {})
        profile['display_name'] = request.form.get('display_name', '')
        profile['email'] = request.form.get('email', '')
        session['profile'] = profile
        flash('General settings updated successfully!', 'success')
    
    return redirect(url_for('settings.settings'))

@settings_bp.route('/update_profile', methods=['POST'])
def update_user_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    try:
        profile_json = request.form.get('profile_data', '{}')
        new_profile_data = json.loads(profile_json)
        
        current_profile = session.get('profile', {})
        updated_profile = merge_user_preferences(current_profile, new_profile_data)
        session['profile'] = updated_profile
        
        config_keys = ['debug_mode', 'admin_access', 'maintenance_mode', 'feature_flags']
        config_overrides = {}
        
        def extract_config_values(data, prefix=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    full_key = f"{prefix}.{key}" if prefix else key
                    if key in config_keys or any(k in key for k in ['admin', 'debug', 'maintenance']):
                        config_overrides[key] = value
                    if isinstance(value, dict):
                        extract_config_values(value, full_key)
        
        extract_config_values(new_profile_data)
        print(config_overrides, file=sys.stderr)
        
        if config_overrides:
            session['config_overrides'] = config_overrides
        
        return redirect(url_for('dashboard.dashboard') + '?success=Profile updated successfully!')
        
    except json.JSONDecodeError:
        return redirect(url_for('dashboard.dashboard') + '?error=Invalid JSON format in profile data')
    except Exception as e:
        return redirect(url_for('dashboard.dashboard') + f'?error=Profile update failed: {str(e)}')
