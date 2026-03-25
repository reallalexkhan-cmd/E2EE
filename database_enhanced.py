"""
╔═══════════════════════════════════════════════════════════════╗
║     DARKSTAR BOII SAHIIL - ENHANCED DATABASE SYSTEM v2.0      ║
║              24/7 NONSTOP AUTOMATION ENGINE                   ║
╚═══════════════════════════════════════════════════════════════╝
Developer: Darkstar Boii Sahiil
"""

import sqlite3
import hashlib
import json
import os
import time
import threading
from pathlib import Path
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from contextlib import contextmanager
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent / 'darkstar_enhanced.db'
ENCRYPTION_KEY_FILE = Path(__file__).parent / '.encryption_key'

# Thread-safe connection pool
_connection_pool = {}
_pool_lock = threading.Lock()

def get_encryption_key():
    """Get or create encryption key for secure data storage"""
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

@contextmanager
def get_db_connection():
    """Thread-safe database connection context manager"""
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize enhanced database with all tables"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                is_premium INTEGER DEFAULT 1,
                is_admin INTEGER DEFAULT 0,
                last_login TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User configurations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_configs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                chat_id TEXT,
                name_prefix TEXT,
                delay INTEGER DEFAULT 30,
                cookies_encrypted TEXT,
                messages TEXT,
                automation_running INTEGER DEFAULT 0,
                auto_restart INTEGER DEFAULT 1,
                max_messages INTEGER DEFAULT 0,
                locked_group_name TEXT,
                locked_nicknames TEXT,
                lock_enabled INTEGER DEFAULT 0,
                theme TEXT DEFAULT 'dark',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Automation logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS automation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                process_id TEXT,
                log_type TEXT DEFAULT 'info',
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Message statistics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS message_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date DATE DEFAULT CURRENT_DATE,
                messages_sent INTEGER DEFAULT 0,
                sessions_count INTEGER DEFAULT 0,
                total_runtime_seconds INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, date)
            )
        ''')
        
        # Heartbeat table for 24/7 monitoring
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS heartbeats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                process_id TEXT,
                status TEXT DEFAULT 'running',
                last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                message_count INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Scheduled messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                scheduled_time TIMESTAMP NOT NULL,
                sent INTEGER DEFAULT 0,
                sent_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Add missing columns for backward compatibility
        columns_to_add = [
            ('user_configs', 'auto_restart', 'INTEGER DEFAULT 1'),
            ('user_configs', 'max_messages', 'INTEGER DEFAULT 0'),
            ('user_configs', 'theme', 'TEXT DEFAULT "dark"'),
            ('user_configs', 'automation_running', 'INTEGER DEFAULT 0'),
            ('user_configs', 'locked_group_name', 'TEXT'),
            ('user_configs', 'locked_nicknames', 'TEXT'),
            ('user_configs', 'lock_enabled', 'INTEGER DEFAULT 0'),
            ('users', 'email', 'TEXT'),
            ('users', 'is_premium', 'INTEGER DEFAULT 1'),
            ('users', 'is_admin', 'INTEGER DEFAULT 0'),
            ('users', 'last_login', 'TIMESTAMP'),
        ]
        
        for table, column, definition in columns_to_add:
            try:
                cursor.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition}')
                conn.commit()
            except sqlite3.OperationalError:
                pass
        
        conn.commit()
        logger.info("✅ Enhanced database initialized successfully!")

def hash_password(password):
    """Hash password using SHA-256 with salt"""
    salt = "darkstar_boii_sahiil_2024"
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()

def encrypt_data(data):
    """Encrypt sensitive data"""
    if not data:
        return None
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    """Decrypt sensitive data"""
    if not encrypted_data:
        return ""
    try:
        return cipher_suite.decrypt(encrypted_data.encode()).decode()
    except:
        return ""

# ============ USER FUNCTIONS ============

def create_user(username, password, email=None, is_admin=False):
    """Create new user with enhanced fields"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            password_hash = hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, password_hash, email, is_admin)
                VALUES (?, ?, ?, ?)
            ''', (username, password_hash, email, 1 if is_admin else 0))
            user_id = cursor.lastrowid
            
            cursor.execute('''
                INSERT INTO user_configs (user_id, chat_id, name_prefix, delay, messages)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, '', '', 30, ''))
            
            conn.commit()
            logger.info(f"✅ User created: {username}")
            return True, "Account created successfully! Welcome to Darkstar E2EE!"
        except sqlite3.IntegrityError:
            return False, "Username already exists!"
        except Exception as e:
            logger.error(f"❌ Create user error: {e}")
            return False, f"Error: {str(e)}"

def verify_user(username, password):
    """Verify user credentials"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if user and user['password_hash'] == hash_password(password):
            # Update last login
            cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user['id'],))
            conn.commit()
            return user['id']
        return None

def get_user(user_id):
    """Get user details"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        return dict(user) if user else None

def get_user_by_username(username):
    """Get user by username"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        return dict(user) if user else None

# ============ CONFIG FUNCTIONS ============

def get_user_config(user_id):
    """Get user configuration"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT chat_id, name_prefix, delay, cookies_encrypted, messages, 
                   automation_running, auto_restart, max_messages, theme
            FROM user_configs WHERE user_id = ?
        ''', (user_id,))
        config = cursor.fetchone()
        
        if config:
            return {
                'chat_id': config['chat_id'] or '',
                'name_prefix': config['name_prefix'] or '',
                'delay': config['delay'] or 30,
                'cookies': decrypt_data(config['cookies_encrypted']),
                'messages': config['messages'] or '',
                'automation_running': config['automation_running'] or 0,
                'auto_restart': config['auto_restart'] or 1,
                'max_messages': config['max_messages'] or 0,
                'theme': config['theme'] or 'dark'
            }
        return None

def update_user_config(user_id, **kwargs):
    """Update user configuration with flexible parameters"""
    allowed_fields = ['chat_id', 'name_prefix', 'delay', 'cookies', 'messages', 
                      'auto_restart', 'max_messages', 'theme']
    
    updates = []
    values = []
    
    for field, value in kwargs.items():
        if field in allowed_fields:
            if field == 'cookies':
                updates.append('cookies_encrypted = ?')
                values.append(encrypt_data(value))
            else:
                updates.append(f'{field} = ?')
                values.append(value)
    
    if updates:
        updates.append('updated_at = CURRENT_TIMESTAMP')
        values.append(user_id)
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE user_configs SET {', '.join(updates)}
                WHERE user_id = ?
            ''', values)
            conn.commit()
            return True
    return False

# ============ AUTOMATION STATE FUNCTIONS ============

def set_automation_running(user_id, is_running, process_id=None):
    """Set automation running state"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE user_configs 
            SET automation_running = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (1 if is_running else 0, user_id))
        
        if is_running:
            # Create/update heartbeat
            cursor.execute('''
                INSERT INTO heartbeats (user_id, process_id, status, last_heartbeat)
                VALUES (?, ?, 'running', CURRENT_TIMESTAMP)
                ON CONFLICT(user_id) DO UPDATE SET 
                    status = 'running',
                    last_heartbeat = CURRENT_TIMESTAMP,
                    process_id = ?
            ''', (user_id, process_id, process_id))
        else:
            cursor.execute('''
                UPDATE heartbeats SET status = 'stopped' WHERE user_id = ?
            ''', (user_id,))
        
        conn.commit()

def get_automation_running(user_id):
    """Get automation running state"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT automation_running FROM user_configs WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        return bool(result['automation_running']) if result else False

def update_heartbeat(user_id, process_id, message_count=0):
    """Update heartbeat for 24/7 monitoring"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE heartbeats SET 
                last_heartbeat = CURRENT_TIMESTAMP,
                message_count = ?
            WHERE user_id = ? AND process_id = ?
        ''', (message_count, user_id, process_id))
        conn.commit()

def get_heartbeat(user_id):
    """Get last heartbeat info"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM heartbeats WHERE user_id = ?
        ''', (user_id,))
        result = cursor.fetchone()
        return dict(result) if result else None

# ============ LOGGING FUNCTIONS ============

def add_log(user_id, message, log_type='info', process_id=None):
    """Add automation log"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO automation_logs (user_id, process_id, log_type, message)
            VALUES (?, ?, ?, ?)
        ''', (user_id, process_id, log_type, message))
        conn.commit()

def get_logs(user_id, limit=100):
    """Get user logs"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM automation_logs 
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        return [dict(row) for row in cursor.fetchall()]

def clear_logs(user_id):
    """Clear user logs"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM automation_logs WHERE user_id = ?', (user_id,))
        conn.commit()

# ============ STATISTICS FUNCTIONS ============

def update_stats(user_id, messages_sent=0, runtime_seconds=0):
    """Update daily statistics"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO message_stats (user_id, messages_sent, total_runtime_seconds, sessions_count)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(user_id, date) DO UPDATE SET
                messages_sent = messages_sent + ?,
                total_runtime_seconds = total_runtime_seconds + ?,
                sessions_count = sessions_count + 1
        ''', (user_id, messages_sent, runtime_seconds, messages_sent, runtime_seconds))
        conn.commit()

def get_stats(user_id, days=7):
    """Get statistics for last N days"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT date, messages_sent, sessions_count, total_runtime_seconds
            FROM message_stats
            WHERE user_id = ? AND date >= date('now', ?)
            ORDER BY date DESC
        ''', (user_id, f'-{days} days'))
        return [dict(row) for row in cursor.fetchall()]

def get_total_stats(user_id):
    """Get total statistics"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                SUM(messages_sent) as total_messages,
                SUM(sessions_count) as total_sessions,
                SUM(total_runtime_seconds) as total_runtime
            FROM message_stats
            WHERE user_id = ?
        ''', (user_id,))
        result = cursor.fetchone()
        return dict(result) if result else {'total_messages': 0, 'total_sessions': 0, 'total_runtime': 0}

# ============ LOCK SYSTEM FUNCTIONS ============

def get_lock_config(user_id):
    """Get lock configuration"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT chat_id, locked_group_name, locked_nicknames, lock_enabled, cookies_encrypted
            FROM user_configs WHERE user_id = ?
        ''', (user_id,))
        config = cursor.fetchone()
        
        if config:
            try:
                nicknames = json.loads(config['locked_nicknames']) if config['locked_nicknames'] else {}
            except:
                nicknames = {}
            
            return {
                'chat_id': config['chat_id'] or '',
                'locked_group_name': config['locked_group_name'] or '',
                'locked_nicknames': nicknames,
                'lock_enabled': bool(config['lock_enabled']),
                'cookies': decrypt_data(config['cookies_encrypted'])
            }
        return None

def update_lock_config(user_id, chat_id, locked_group_name, locked_nicknames, cookies=None):
    """Update lock configuration"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        nicknames_json = json.dumps(locked_nicknames)
        
        if cookies is not None:
            encrypted_cookies = encrypt_data(cookies)
            cursor.execute('''
                UPDATE user_configs 
                SET chat_id = ?, locked_group_name = ?, locked_nicknames = ?, 
                    cookies_encrypted = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (chat_id, locked_group_name, nicknames_json, encrypted_cookies, user_id))
        else:
            cursor.execute('''
                UPDATE user_configs 
                SET chat_id = ?, locked_group_name = ?, locked_nicknames = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (chat_id, locked_group_name, nicknames_json, user_id))
        
        conn.commit()

def set_lock_enabled(user_id, enabled):
    """Enable or disable lock system"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE user_configs SET lock_enabled = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (1 if enabled else 0, user_id))
        conn.commit()

# ============ SCHEDULED MESSAGES ============

def add_scheduled_message(user_id, message, scheduled_time):
    """Add a scheduled message"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO scheduled_messages (user_id, message, scheduled_time)
            VALUES (?, ?, ?)
        ''', (user_id, message, scheduled_time))
        conn.commit()
        return cursor.lastrowid

def get_scheduled_messages(user_id, pending_only=True):
    """Get scheduled messages"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if pending_only:
            cursor.execute('''
                SELECT * FROM scheduled_messages 
                WHERE user_id = ? AND sent = 0
                ORDER BY scheduled_time ASC
            ''', (user_id,))
        else:
            cursor.execute('''
                SELECT * FROM scheduled_messages 
                WHERE user_id = ?
                ORDER BY scheduled_time DESC
            ''', (user_id,))
        return [dict(row) for row in cursor.fetchall()]

def mark_message_sent(message_id):
    """Mark scheduled message as sent"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE scheduled_messages SET sent = 1, sent_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (message_id,))
        conn.commit()

# ============ ADMIN FUNCTIONS ============

def get_all_users():
    """Get all users (admin only)"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.id, u.username, u.email, u.is_premium, u.is_admin, u.last_login, u.created_at,
                   uc.automation_running
            FROM users u
            LEFT JOIN user_configs uc ON u.id = uc.user_id
            ORDER BY u.created_at DESC
        ''')
        return [dict(row) for row in cursor.fetchall()]

def get_active_automations():
    """Get all active automations"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.username, h.* 
            FROM heartbeats h
            JOIN users u ON h.user_id = u.id
            WHERE h.status = 'running'
        ''')
        return [dict(row) for row in cursor.fetchall()]

# Initialize on import
init_db()