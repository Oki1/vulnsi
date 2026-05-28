import copy
from flask import session, current_app
import sys

def merge_user_preferences(existing_prefs, new_prefs):
    if not isinstance(existing_prefs, dict):
        existing_prefs = {}
    if not isinstance(new_prefs, dict):
        return existing_prefs
    merged = copy.deepcopy(existing_prefs)
    for key, value in new_prefs.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_user_preferences(merged[key], value)
        else:
            merged[key] = value
    return merged

def apply_config_overrides():
    print(session, file=sys.stderr)
    app_config = current_app.config['APP_CONFIG']
    if 'config_overrides' in session:
        for attr, value in session['config_overrides'].items():
            if hasattr(app_config, attr):
                setattr(app_config, attr, value)
