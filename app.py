# Developer: Darkstar Boii Sahiil
# Full Power 24/7 Running System with Message & File Upload
# Flask + SocketIO for Real-time Updates

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_file
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sqlite3
import hashlib
import os
import json
import time
import threading
import uuid
from datetime import datetime
from pathlib import Path
from cryptography.fernet import Fernet
import base64
import subprocess
import signal
import sys

# Initialize Flask App
app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Database Configuration
DB_PATH = Path(__file__).parent / 'darkstar.db'
ENCRYPTION_KEY_FILE = Path(__file__).parent / '.encryption_key'
UPLOAD_FOLDER = Path(__file__).parent / 'uploads'
MESSAGES_FOLDER = Path(__file__).parent / 'user_messages'

# Create folders
UPLOAD_FOLDER.mkdir(exist_ok=True)
MESSAGES_FOLDER.mkdir(exist_ok=True)

# Encryption Setup
def get_encryption_key():
    if ENCRYPTION_KEY_FILE.exists():
        with open(ENCRYPTION_KEY_FILE, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(ENCRYPTION_KEY_FILE, 'wb') as f:
            f.write(key)
        return key

ENCRYPTION_KEY = get_encryption_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# Database Functions
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # User Configs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chat_id TEXT,
            name_prefix TEXT,
            delay INTEGER DEFAULT 30,
            cookies_encrypted TEXT,
            messages TEXT,
            automation_running INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Messages Table (New - for message system)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message_text TEXT NOT NULL,
            message_type TEXT DEFAULT 'text',
            file_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # File Uploads Table (New - for file tracking)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            original_filename TEXT NOT NULL,
            stored_filename TEXT NOT NULL,
            file_size INTEGER,
            file_type TEXT,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Activity Log Table (New - for 24/7 monitoring)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            activity_type TEXT NOT NULL,
            activity_detail TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def encrypt_data(data):
    if not data:
        return None
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    if not encrypted_data:
        return ""
    try:
        return cipher_suite.decrypt(encrypted_data.encode()).decode()
    except:
        return ""

def create_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        password_hash = hash_password(password)
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                      (username, password_hash))
        user_id = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO user_configs (user_id, chat_id, name_prefix, delay, messages)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, '', '', 30, ''))
        
        conn.commit()
        conn.close()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already exists!"
    except Exception as e:
        conn.close()
        return False, f"Error: {str(e)}"

def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user and user[1] == hash_password(password):
        return user[0]
    return None

def get_user_config(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT chat_id, name_prefix, delay, cookies_encrypted, messages, automation_running
        FROM user_configs WHERE user_id = ?
    ''', (user_id,))
    config = cursor.fetchone()
    conn.close()
    
    if config:
        return {
            'chat_id': config[0] or '',
            'name_prefix': config[1] or '',
            'delay': config[2] or 30,
            'cookies': decrypt_data(config[3]),
            'messages': config[4] or '',
            'automation_running': config[5] or 0
        }
    return None

def update_user_config(user_id, chat_id, name_prefix, delay, cookies, messages):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    encrypted_cookies = encrypt_data(cookies)
    cursor.execute('''
        UPDATE user_configs 
        SET chat_id = ?, name_prefix = ?, delay = ?, cookies_encrypted = ?, 
            messages = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (chat_id, name_prefix, delay, encrypted_cookies, messages, user_id))
    conn.commit()
    conn.close()

def save_message(user_id, message_text, message_type='text', file_path=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (user_id, message_text, message_type, file_path)
        VALUES (?, ?, ?, ?)
    ''', (user_id, message_text, message_type, file_path))
    conn.commit()
    conn.close()

def get_messages(user_id, limit=100):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, message_text, message_type, file_path, created_at
        FROM messages WHERE user_id = ?
        ORDER BY created_at DESC LIMIT ?
    ''', (user_id, limit))
    messages = cursor.fetchall()
    conn.close()
    return messages

def save_file_upload(user_id, original_filename, stored_filename, file_size, file_type):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO file_uploads (user_id, original_filename, stored_filename, file_size, file_type)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, original_filename, stored_filename, file_size, file_type))
    conn.commit()
    conn.close()

def get_user_files(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, original_filename, file_size, file_type, upload_time
        FROM file_uploads WHERE user_id = ?
        ORDER BY upload_time DESC
    ''', (user_id,))
    files = cursor.fetchall()
    conn.close()
    return files

def log_activity(user_id, activity_type, activity_detail):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO activity_log (user_id, activity_type, activity_detail)
        VALUES (?, ?, ?)
    ''', (user_id, activity_type, activity_detail))
    conn.commit()
    conn.close()

def set_automation_running(user_id, is_running):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE user_configs 
        SET automation_running = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (1 if is_running else 0, user_id))
    conn.commit()
    conn.close()

def get_automation_running(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT automation_running FROM user_configs WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return bool(result[0]) if result else False

# Automation State Manager
class AutomationManager:
    def __init__(self):
        self.running_processes = {}
        self.message_counts = {}
        self.logs = {}
    
    def start_automation(self, user_id, config):
        if user_id in self.running_processes:
            return False, "Already running"
        
        self.message_counts[user_id] = 0
        self.logs[user_id] = []
        set_automation_running(user_id, True)
        
        # Start automation thread
        thread = threading.Thread(target=self._run_automation, args=(user_id, config))
        thread.daemon = True
        thread.start()
        self.running_processes[user_id] = thread
        
        return True, "Automation started"
    
    def stop_automation(self, user_id):
        if user_id in self.running_processes:
            set_automation_running(user_id, False)
            del self.running_processes[user_id]
            return True, "Automation stopped"
        return False, "Not running"
    
    def _run_automation(self, user_id, config):
        self.log(user_id, "🚀 Automation started - 24/7 Mode Active")
        
        while get_automation_running(user_id):
            try:
                # Get messages from database
                messages = get_messages(user_id)
                if messages:
                    for msg in messages[:10]:  # Process last 10 messages
                        self.log(user_id, f"📝 Processing message: {msg[1][:30]}...")
                        self.message_counts[user_id] = self.message_counts.get(user_id, 0) + 1
                        
                        # Emit real-time update
                        socketio.emit('automation_update', {
                            'user_id': user_id,
                            'message_count': self.message_counts[user_id],
                            'log': f"Message sent: {msg[1][:30]}..."
                        })
                
                delay = config.get('delay', 30)
                self.log(user_id, f"⏳ Waiting {delay} seconds...")
                time.sleep(delay)
                
            except Exception as e:
                self.log(user_id, f"❌ Error: {str(e)}")
                time.sleep(5)
        
        self.log(user_id, "🛑 Automation stopped")
    
    def log(self, user_id, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        if user_id not in self.logs:
            self.logs[user_id] = []
        self.logs[user_id].append(log_entry)
        log_activity(user_id, "AUTOMATION", message)
    
    def get_status(self, user_id):
        return {
            'running': user_id in self.running_processes,
            'message_count': self.message_counts.get(user_id, 0),
            'logs': self.logs.get(user_id, [])[-50:]  # Last 50 logs
        }

automation_manager = AutomationManager()

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        user_id = verify_user(username, password)
        if user_id:
            session['user_id'] = user_id
            session['username'] = username
            log_activity(user_id, "LOGIN", f"User {username} logged in")
            return jsonify({'success': True, 'message': 'Login successful!'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials!'})
    
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    success, message = create_user(username, password)
    return jsonify({'success': success, 'message': message})

@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id:
        log_activity(user_id, "LOGOUT", f"User logged out")
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    if request.method == 'GET':
        config = get_user_config(user_id)
        return jsonify(config)
    
    elif request.method == 'POST':
        data = request.json
        update_user_config(
            user_id,
            data.get('chat_id', ''),
            data.get('name_prefix', ''),
            data.get('delay', 30),
            data.get('cookies', ''),
            data.get('messages', '')
        )
        return jsonify({'success': True, 'message': 'Configuration saved!'})

@app.route('/api/message', methods=['POST'])
def api_message():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    data = request.json
    message_text = data.get('message', '')
    
    if message_text:
        save_message(user_id, message_text)
        log_activity(user_id, "MESSAGE", f"Saved message: {message_text[:30]}...")
        return jsonify({'success': True, 'message': 'Message saved!'})
    
    return jsonify({'success': False, 'message': 'No message provided'})

@app.route('/api/messages')
def api_messages():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    messages = get_messages(user_id)
    
    return jsonify([{
        'id': m[0],
        'text': m[1],
        'type': m[2],
        'file_path': m[3],
        'created_at': m[4]
    } for m in messages])

@app.route('/api/upload', methods=['POST'])
def api_upload():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})
    
    # Create user-specific folder
    user_folder = UPLOAD_FOLDER / str(user_id)
    user_folder.mkdir(exist_ok=True)
    
    # Generate unique filename
    ext = Path(file.filename).suffix
    stored_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = user_folder / stored_filename
    
    file.save(file_path)
    file_size = file_path.stat().st_size
    
    save_file_upload(user_id, file.filename, stored_filename, file_size, file.content_type)
    save_message(user_id, f"📎 File uploaded: {file.filename}", 'file', str(file_path))
    log_activity(user_id, "UPLOAD", f"Uploaded file: {file.filename}")
    
    return jsonify({
        'success': True, 
        'message': 'File uploaded successfully!',
        'filename': file.filename,
        'size': file_size
    })

@app.route('/api/files')
def api_files():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    files = get_user_files(user_id)
    
    return jsonify([{
        'id': f[0],
        'filename': f[1],
        'size': f[2],
        'type': f[3],
        'upload_time': f[4]
    } for f in files])

@app.route('/api/automation/start', methods=['POST'])
def api_automation_start():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    config = get_user_config(user_id)
    
    if not config.get('chat_id'):
        return jsonify({'success': False, 'message': 'Please set Chat ID first!'})
    
    success, message = automation_manager.start_automation(user_id, config)
    return jsonify({'success': success, 'message': message})

@app.route('/api/automation/stop', methods=['POST'])
def api_automation_stop():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    success, message = automation_manager.stop_automation(user_id)
    return jsonify({'success': success, 'message': message})

@app.route('/api/automation/status')
def api_automation_status():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    status = automation_manager.get_status(user_id)
    return jsonify(status)

@app.route('/api/activities')
def api_activities():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT activity_type, activity_detail, timestamp
        FROM activity_log WHERE user_id = ?
        ORDER BY timestamp DESC LIMIT 50
    ''', (user_id,))
    activities = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'type': a[0],
        'detail': a[1],
        'timestamp': a[2]
    } for a in activities])

# WebSocket Events
@socketio.on('connect')
def handle_connect():
    if 'user_id' in session:
        emit('connected', {'message': 'Connected to Darkstar 24/7 System'})

@socketio.on('request_update')
def handle_update():
    if 'user_id' in session:
        user_id = session['user_id']
        status = automation_manager.get_status(user_id)
        emit('status_update', status)

# Initialize database on startup
init_db()

# Graceful shutdown handler
def signal_handler(sig, frame):
    print("\n🛑 Shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 DARKSTAR BOII SAHIIL - 24/7 FULL POWER SYSTEM")
    print("=" * 60)
    print("✅ System initialized successfully!")
    print("✅ Database ready!")
    print("✅ All modules loaded!")
    print("=" * 60)
    
    socketio.run(app, host='0.0.0.0', port=9000, debug=True, allow_unsafe_werkzeug=True)