from flask import Blueprint, session, render_template, request, jsonify, redirect, url_for, flash
import uuid
from datetime import datetime
from ..utils import apply_config_overrides
from ..config import FLAG

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks')
def tasks():
    from flask import current_app
    app_config = current_app.config['APP_CONFIG']
    todos_storage = current_app.config['TODOS_STORAGE']
    
    apply_config_overrides()
    user_id = session.get('user_id')
    user_tasks = todos_storage.get(user_id, [])
    
    template_data = {
        'user_tasks': user_tasks,
        'app_config': app_config,
        'session_info': {k: v for k, v in session.items() if k != 'profile'},
        'flag_data': FLAG if app_config.admin_access else None
    }
    
    return render_template('tasks.html', **template_data)

@tasks_bp.route('/create_task', methods=['POST'])
def create_task():
    if 'user_id' not in session:
        return jsonify({'error': 'Session required'}), 401
    
    from flask import current_app
    todos_storage = current_app.config['TODOS_STORAGE']
    
    user_id = session['user_id']
    
    new_task = {
        'id': str(uuid.uuid4()),
        'title': request.form.get('title', ''),
        'description': request.form.get('description', ''),
        'priority': request.form.get('priority', 'Medium'),
        'category': request.form.get('category', ''),
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    if user_id not in todos_storage:
        todos_storage[user_id] = []
    
    todos_storage[user_id].append(new_task)
    flash('Task created successfully!', 'success')
    
    return redirect(url_for('tasks.tasks'))

@tasks_bp.route('/complete_task', methods=['POST'])
def complete_task():
    if 'user_id' not in session:
        return jsonify({'error': 'Session required'}), 401
    
    from flask import current_app
    todos_storage = current_app.config['TODOS_STORAGE']
    
    user_id = session['user_id']
    task_id = request.form.get('task_id')
    
    if user_id in todos_storage:
        for task in todos_storage[user_id]:
            if task['id'] == task_id:
                task['completed'] = True
                flash('Task completed!', 'success')
                break
    
    return redirect(url_for('tasks.tasks'))
