document.addEventListener('DOMContentLoaded', function() {
    // Add animations to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = (index * 0.1) + 's';
        card.classList.add('fadeInUp');
    });
    
    // Settings navigation
    document.querySelectorAll('.settings-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('.settings-link').forEach(l => l.classList.remove('active'));
            document.querySelectorAll('.settings-section').forEach(s => s.classList.remove('active'));
            this.classList.add('active');
            document.getElementById(this.dataset.section).classList.add('active');
        });
    });
});

// Configuration management
let currentConfig = {
    user_preferences: {
        theme: "light",
        dashboard: {
            layout: "standard"
        },
        notifications: true,
        language: "en"
    },
    app_settings: {
        auto_save: true,
        show_statistics: true,
        enable_shortcuts: false,
        task_reminders: true
    },
    privacy_settings: {
        session_timeout: 60,
        remember_login: false,
        analytics_enabled: true
    }
};

function updateConfig() {
    // Update configuration based on UI inputs
    currentConfig.user_preferences.theme = document.getElementById('theme_mode').value;
    currentConfig.user_preferences.dashboard.layout = document.getElementById('dashboard_layout').value;
    currentConfig.user_preferences.notifications = document.getElementById('enable_notifications').checked;
    currentConfig.user_preferences.language = document.getElementById('language').value;
    
    currentConfig.app_settings.auto_save = document.getElementById('auto_save').checked;
    currentConfig.app_settings.show_statistics = document.getElementById('show_statistics').checked;
    currentConfig.app_settings.enable_shortcuts = document.getElementById('enable_shortcuts').checked;
    currentConfig.app_settings.task_reminders = document.getElementById('task_reminders').checked;
    
    currentConfig.privacy_settings.session_timeout = parseInt(document.getElementById('session_timeout').value);
    currentConfig.privacy_settings.remember_login = document.getElementById('remember_login').checked;
    currentConfig.privacy_settings.analytics_enabled = document.getElementById('analytics_enabled').checked;
    
    // Update hidden form field
    document.getElementById('profile_data').value = JSON.stringify(currentConfig);
}

function resetConfig() {
    // Reset all UI elements to defaults
    document.getElementById('theme_mode').value = 'light';
    document.getElementById('dashboard_layout').value = 'standard';
    document.getElementById('enable_notifications').checked = true;
    document.getElementById('language').value = 'en';
    
    document.getElementById('auto_save').checked = true;
    document.getElementById('show_statistics').checked = true;
    document.getElementById('enable_shortcuts').checked = false;
    document.getElementById('task_reminders').checked = true;
    
    document.getElementById('session_timeout').value = '60';
    document.getElementById('remember_login').checked = false;
    document.getElementById('analytics_enabled').checked = true;
    
    updateConfig();
}

// Toggle feature switches
function toggleFeature(featureName, element) {
    fetch('/api/toggle-feature', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            feature: featureName,
            enabled: element.checked
        })
    });
}
