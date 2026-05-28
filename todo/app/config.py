import os

class AppConfig:
    def __init__(self):
        self.debug_mode = False
        self.maintenance_mode = False
        self.admin_access = False
        self.feature_flags = {
            'advanced_analytics': False,
            'team_collaboration': True,
            'export_functionality': True,
            'notification_system': True,
            'third_party_integrations': False
        }
        self.api_keys = {}
        self.security_headers = True
        self.theme_settings = {
            'primary_color': '#667eea',
            'secondary_color': '#764ba2',
            'accent_color': '#f093fb'
        }

FLAG = os.environ.get('FLAG', 'PTR{fake_flag}')
