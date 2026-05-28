from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import secrets
from datetime import datetime
import base64
from hashlib import shake_128

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

FLAG = os.environ.get('FLAG', 'dctf{?????????????????????????????}')

# Structure: {username: [{'id': id, 'title': title, 'content': content, 'timestamp': timestamp}, ...]}
notes_db = {}

def encrypt_note(raw_note, ip_address):
    key = ip_address.encode()
    encrypted = bytes(x ^ y for x, y in zip(bytes(128) + raw_note.encode(), shake_128(key).digest(128 + len(raw_note))))
    return base64.b64encode(encrypted).decode()

def decrypt_note(encrypted_note, ip_address):
    try:
        key = ip_address.encode()
        decoded = base64.b64decode(encrypted_note)
        decrypted = bytes(x ^ y for x, y in zip(decoded, shake_128(key).digest(len(decoded))))
        assert decrypted[:128] == bytes(128)
        return decrypted[128:].decode()
    except: return f"[Decryption failed - Invalid key]"

notes_db['arnes'] = [{
    'id': 0,
    'title': 'FLAG',
    'content': encrypt_note(FLAG, f'153.5.{secrets.randbits(8)}.{secrets.randbits(8)}'),
    'timestamp': '',
}]

def get_client_ip():
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
        return ip
    return request.remote_addr

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_notes = notes_db.get(session['username'], [])
    return render_template('index.html', notes=user_notes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        if username not in notes_db:
            notes_db[username] = []
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if not title or not content:
            flash('Title and content are required!')
            return redirect(url_for('add_note'))
        
        user_notes = notes_db.get(session['username'], [])
        note_id = len(user_notes) + 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get client IP for encryption
        client_ip = get_client_ip()
        encrypted_content = encrypt_note(content, client_ip)
        user_notes.append({
            'id': note_id,
            'title': title,
            'content': encrypted_content,
            'timestamp': timestamp,
        })
        
        notes_db[session['username']] = user_notes
        flash('Note added successfully!')
        return redirect(url_for('index'))
    
    return render_template('add_note.html')

@app.route('/view_note/<int:note_id>')
def view_note(note_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_notes = notes_db.get(session['username'], [])
    note = next((n for n in user_notes if n['id'] == note_id), None)
    
    if note:
        display_note = note.copy()
        client_ip = get_client_ip()
        decryption_ip = note.get('encryption_ip', client_ip)
        display_note['content'] = decrypt_note(note['content'], client_ip)
        if "Decryption failed" in display_note['content'] and client_ip != decryption_ip:
            display_note['decryption_note'] = f"Note was encrypted with IP: {decryption_ip}"
        
        return render_template('view_note.html', note=display_note)
    flash('Note not found!')
    return redirect(url_for('index'))

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    
    if note_id == 0:
        flash('Shoo you evil spirit!')
        return redirect(url_for('index'))

    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_notes = notes_db.get(session['username'], [])
    note = next((n for n in user_notes if n['id'] == note_id), None)
    
    if note:
        notes_db[session['username']] = [n for n in user_notes if n['id'] != note_id]
        flash('Note deleted successfully!')
    else:
        flash('Note not found!')
        
    return redirect(url_for('index'))

@app.route('/auth')
def auth():
    x_forwarded_for = request.headers.get('X-Forwarded-For', '')
    if x_forwarded_for and ('69.69.69.69' in x_forwarded_for):
        return '', 200
    else:
        return '', 401

@app.route('/admin')
def admin_view():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if session['username'] != 'admin':
        flash('Access denied: Admin privileges required')
        return redirect(url_for('index'))
    
    all_notes = []
    for username, user_notes in notes_db.items():
        for note in user_notes:
            note_with_user = note.copy()
            note_with_user['username'] = username
            all_notes.append(note_with_user)
            
    all_notes.sort(key=lambda x: x['timestamp'], reverse=True)
    return render_template('admin_view.html', notes=all_notes)

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    app.run(debug=False)