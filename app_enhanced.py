"""
╔═══════════════════════════════════════════════════════════════╗
║   DARKSTAR BOII SAHIIL - ENHANCED E2EE SYSTEM v2.0           ║
║         24/7 NONSTOP AUTOMATION - FULL POWER MODE             ║
║              NEW MODERN DESIGN - 2024 EDITION                 ║
╚═══════════════════════════════════════════════════════════════╝
Developer: Darkstar Boii Sahiil
"""

import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import json
from datetime import datetime, timedelta
from pathlib import Path

import database_enhanced as db
from automation_engine import automation_manager

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Darkstar E2EE v2.0",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Darkstar E2EE v2.0 - 24/7 Nonstop Automation System",
        'Report a bug': "https://github.com",
    }
)

# ═══════════════════════════════════════════════════════════════
# ENHANCED CSS STYLES - NEW MODERN DESIGN
# ═══════════════════════════════════════════════════════════════

def get_theme_css(theme='dark'):
    if theme == 'dark':
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
        
        * {
            font-family: 'Inter', sans-serif !important;
        }
        
        /* 🌙 DARK PREMIUM BACKGROUND */
        .stApp {
            background: linear-gradient(135deg, #0a0a0f 0%, #12121a 40%, #0d1117 100%);
            background-attachment: fixed;
            color: #ffffff !important;
        }
        
        /* 🔥 MAIN CONTAINER - GLASSMORPHISM */
        .main .block-container {
            background: rgba(20, 20, 30, 0.85);
            border-radius: 24px;
            padding: 35px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.6), 
                        inset 0 1px 0 rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
        }
        
        /* 🚀 HERO HEADER */
        .hero-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border-radius: 20px;
            padding: 45px 30px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5),
                        0 0 100px rgba(99, 102, 241, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.2);
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
        }
        
        .hero-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #6366f1, #8b5cf6, #d946ef, #ec4899);
        }
        
        .hero-header h1 {
            color: #ffffff;
            font-size: 2.8rem;
            font-weight: 900;
            margin-bottom: 10px;
            text-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
            letter-spacing: -0.5px;
        }
        
        .hero-header .subtitle {
            color: #a5b4fc;
            font-size: 1.1rem;
            font-weight: 500;
            opacity: 0.9;
        }
        
        .hero-header .version {
            display: inline-block;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-top: 15px;
        }
        
        /* 📊 STATS CARDS */
        .stats-container {
            display: flex;
            gap: 20px;
            margin: 25px 0;
        }
        
        .stat-card {
            flex: 1;
            background: linear-gradient(145deg, rgba(30, 30, 45, 0.9), rgba(20, 20, 35, 0.9));
            border-radius: 16px;
            padding: 25px;
            text-align: center;
            border: 1px solid rgba(99, 102, 241, 0.15);
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            border-color: rgba(99, 102, 241, 0.4);
            box-shadow: 0 15px 40px rgba(99, 102, 241, 0.15);
        }
        
        .stat-card .stat-value {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #6366f1, #d946ef);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .stat-card .stat-label {
            color: #94a3b8;
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 5px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* 📝 INPUT FIELDS */
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea {
            background: rgba(15, 15, 25, 0.9) !important;
            border-radius: 12px !important;
            padding: 16px !important;
            border: 2px solid rgba(99, 102, 241, 0.2) !important;
            color: #ffffff !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 25px rgba(99, 102, 241, 0.3) !important;
        }
        
        .stTextInput>div>div>input::placeholder,
        .stTextArea>div>div>textarea::placeholder {
            color: #64748b !important;
        }
        
        label {
            color: #a5b4fc !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }
        
        /* 🔘 BUTTONS - PREMIUM GRADIENT */
        .stButton>button {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 1.05rem !important;
            padding: 14px 28px !important;
            border-radius: 14px !important;
            border: none !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.35) !important;
            width: 100%;
        }
        
        .stButton>button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 15px 40px rgba(99, 102, 241, 0.5) !important;
        }
        
        .stButton>button:active {
            transform: translateY(0) !important;
        }
        
        .stButton>button:disabled {
            background: linear-gradient(135deg, #374151, #4b5563) !important;
            box-shadow: none !important;
            cursor: not-allowed !important;
        }
        
        /* 📑 TABS - MODERN */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(15, 15, 25, 0.9);
            border-radius: 16px;
            padding: 8px;
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 600;
            color: #94a3b8;
            border: 1px solid transparent;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(99, 102, 241, 0.1);
            color: #a5b4fc;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
            color: white !important;
            box-shadow: 0 5px 20px rgba(99, 102, 241, 0.4);
        }
        
        /* 💻 CONSOLE OUTPUT */
        .console-output {
            background: linear-gradient(180deg, #0a0a12 0%, #12121f 100%);
            border: 2px solid rgba(99, 102, 241, 0.2);
            border-radius: 16px;
            padding: 20px;
            font-family: 'JetBrains Mono', monospace;
            max-height: 450px;
            overflow-y: auto;
            box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.5);
        }
        
        .console-line {
            background: rgba(99, 102, 241, 0.05);
            padding: 10px 14px;
            border-left: 3px solid #6366f1;
            border-radius: 0 8px 8px 0;
            margin-bottom: 8px;
            font-size: 0.9rem;
            color: #e2e8f0;
        }
        
        .console-line.error {
            border-left-color: #ef4444;
            background: rgba(239, 68, 68, 0.05);
            color: #fca5a5;
        }
        
        .console-line.success {
            border-left-color: #22c55e;
            background: rgba(34, 197, 94, 0.05);
            color: #86efac;
        }
        
        /* 🎯 SIDEBAR */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f0f1a 0%, #151525 100%);
            border-right: 1px solid rgba(99, 102, 241, 0.1);
        }
        
        [data-testid="stSidebar"] .sidebar-header {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(99, 102, 241, 0.15);
        }
        
        /* ✅ STATUS BADGES */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            border-radius: 30px;
            font-weight: 600;
            font-size: 0.9rem;
        }
        
        .status-badge.running {
            background: rgba(34, 197, 94, 0.15);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }
        
        .status-badge.stopped {
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        
        /* 🎨 METRIC STYLING */
        [data-testid="stMetric"] {
            background: rgba(20, 20, 35, 0.8);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(99, 102, 241, 0.1);
        }
        
        [data-testid="stMetricValue"] {
            font-size: 2rem !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #6366f1, #d946ef);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* 📦 SECTIONS */
        .section-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(99, 102, 241, 0.2);
        }
        
        /* 🟢 PULSE ANIMATION */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        /* 🌈 SUCCESS/ERROR BOXES */
        .success-box {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(34, 197, 94, 0.05));
            border: 1px solid rgba(34, 197, 94, 0.3);
            border-radius: 12px;
            padding: 18px;
            text-align: center;
            color: #4ade80;
            font-weight: 600;
        }
        
        .error-box {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.05));
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 12px;
            padding: 18px;
            text-align: center;
            color: #f87171;
            font-weight: 600;
        }
        
        /* 📜 FOOTER */
        .footer {
            text-align: center;
            padding: 30px;
            margin-top: 30px;
            border-top: 1px solid rgba(99, 102, 241, 0.1);
        }
        
        .footer-text {
            color: #64748b;
            font-size: 0.9rem;
        }
        
        .footer-brand {
            color: #a5b4fc;
            font-weight: 700;
            font-size: 1rem;
            margin-top: 10px;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(15, 15, 25, 0.5);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            border-radius: 10px;
        }
        </style>
        """
    else:
        # Light theme CSS
        return """<style>/* Light theme placeholder */</style>"""

# Apply theme
theme = st.session_state.get('theme', 'dark')
st.markdown(get_theme_css(theme), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def render_hero_header(title, subtitle, show_version=True):
    """Render a beautiful hero header"""
    version_html = '<span class="version">v2.0 ENHANCED</span>' if show_version else ''
    st.markdown(f'''
    <div class="hero-header">
        <h1>🚀 {title}</h1>
        <p class="subtitle">{subtitle}</p>
        {version_html}
    </div>
    ''', unsafe_allow_html=True)

def render_stat_card(value, label, icon="📊"):
    """Render a stat card"""
    st.markdown(f'''
    <div class="stat-card">
        <div class="stat-value">{icon} {value}</div>
        <div class="stat-label">{label}</div>
    </div>
    ''', unsafe_allow_html=True)

def render_console(logs, max_logs=50):
    """Render console output"""
    logs_html = '<div class="console-output">'
    for log in logs[-max_logs:]:
        log_class = ''
        if 'error' in log.lower() or '❌' in log:
            log_class = 'error'
        elif 'success' in log.lower() or '✅' in log:
            log_class = 'success'
        logs_html += f'<div class="console-line {log_class}">{log}</div>'
    logs_html += '</div>'
    st.markdown(logs_html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# LOGIN PAGE
# ═══════════════════════════════════════════════════════════════

def login_page():
    render_hero_header("Darkstar E2EE", "24/7 Nonstop Automation System")
    
    tab1, tab2 = st.tabs(["🔐 Login", "✨ Sign Up"])
    
    with tab1:
        st.markdown('<div class="section-title">Welcome Back!</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            
            if st.button("🚀 LOGIN", key="login_btn", use_container_width=True):
                if username and password:
                    user_id = db.verify_user(username, password)
                    if user_id:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.session_state.auto_start_checked = False
                        
                        # Auto-start automation if it was running
                        if db.get_automation_running(user_id):
                            user_config = db.get_user_config(user_id)
                            if user_config and user_config.get('chat_id'):
                                automation_manager.start_automation(user_id, user_config)
                        
                        st.success(f"✅ Welcome back, {username.upper()}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password!")
                else:
                    st.warning("⚠️ Please enter both username and password")
        
        with col2:
            st.markdown("""
            <div style="padding: 20px; background: rgba(99, 102, 241, 0.1); border-radius: 16px; border: 1px solid rgba(99, 102, 241, 0.2);">
                <h3 style="color: #a5b4fc; margin-bottom: 15px;">🌟 Features</h3>
                <ul style="color: #94a3b8; font-size: 0.9rem;">
                    <li>24/7 Nonstop Automation</li>
                    <li>Auto-Recovery System</li>
                    <li>Message Scheduling</li>
                    <li>Real-time Monitoring</li>
                    <li>Advanced Statistics</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="section-title">Create New Account</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            new_username = st.text_input("Choose Username", placeholder="Choose a unique username", key="signup_username")
        with col2:
            new_email = st.text_input("Email (optional)", placeholder="your@email.com", key="signup_email")
        
        col1, col2 = st.columns(2)
        with col1:
            new_password = st.text_input("Choose Password", type="password", placeholder="Create a strong password", key="signup_password")
        with col2:
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password", key="confirm_password")
        
        if st.button("✨ CREATE ACCOUNT", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    success, message = db.create_user(new_username, new_password, new_email)
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Passwords do not match!")
            else:
                st.warning("⚠️ Please fill all required fields")

# ═══════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════

def main_app():
    render_hero_header("Darkstar E2EE", "Facebook E2EE Conversation Automation")
    
    # Check for auto-start
    if not st.session_state.auto_start_checked and st.session_state.user_id:
        st.session_state.auto_start_checked = True
        if db.get_automation_running(st.session_state.user_id):
            user_config = db.get_user_config(st.session_state.user_id)
            if user_config and user_config.get('chat_id'):
                automation_manager.start_automation(st.session_state.user_id, user_config)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f'''
        <div class="sidebar-header">
            <h3 style="color: #a5b4fc; margin: 0;">👤 User Dashboard</h3>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown(f"**Username:** {st.session_state.username}")
        st.markdown(f"**User ID:** {st.session_state.user_id}")
        
        st.markdown('<div class="success-box">✅ Premium Access</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Theme toggle
        theme_col1, theme_col2 = st.columns(2)
        with theme_col1:
            if st.button("🌙 Dark", use_container_width=True):
                st.session_state.theme = 'dark'
                st.rerun()
        with theme_col2:
            if st.button("☀️ Light", use_container_width=True):
                st.session_state.theme = 'light'
                st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 LOGOUT", use_container_width=True):
            # Stop automation on logout
            automation_manager.stop_automation(st.session_state.user_id)
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.auto_start_checked = False
            st.rerun()
    
    # Get user config
    user_config = db.get_user_config(st.session_state.user_id)
    
    if not user_config:
        st.warning("⚠️ Configuration not found. Please refresh the page.")
        return
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "⚙️ Configuration", 
        "🚀 Automation", 
        "📊 Statistics",
        "📅 Scheduler"
    ])
    
    # ═══════════════════════════════════════════════════════════════
    # TAB 1: CONFIGURATION
    # ═══════════════════════════════════════════════════════════════
    
    with tab1:
        st.markdown('<div class="section-title">E2EE Configuration</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔗 Connection Settings")
            chat_id = st.text_input(
                "E2EE Chat ID", 
                value=user_config.get('chat_id', ''),
                placeholder="e.g., 10000634210631",
                help="Facebook conversation ID from the URL"
            )
            
            name_prefix = st.text_input(
                "Name Prefix",
                value=user_config.get('name_prefix', ''),
                placeholder="Optional prefix for each message",
                help="Adds a prefix before each message"
            )
            
            delay = st.number_input(
                "Delay (seconds)",
                min_value=1,
                max_value=3600,
                value=int(user_config.get('delay', 30)),
                help="Wait time between messages"
            )
            
            max_messages = st.number_input(
                "Max Messages (0 = unlimited)",
                min_value=0,
                max_value=100000,
                value=int(user_config.get('max_messages', 0)),
                help="Maximum messages to send (0 = unlimited)"
            )
        
        with col2:
            st.markdown("#### 🔐 Security Settings")
            cookies = st.text_area(
                "Facebook Cookies",
                value="",
                placeholder="Paste your Facebook cookies here",
                height=120,
                help="Your cookies are encrypted and stored securely"
            )
            
            st.markdown("#### 📝 Messages")
            messages = st.text_area(
                "Messages (one per line)",
                value=user_config.get('messages', ''),
                placeholder="Enter messages, one per line",
                height=150,
                help="Each line = one message"
            )
            
            auto_restart = st.checkbox(
                "🔄 Auto-Restart on Failure",
                value=bool(user_config.get('auto_restart', 1)),
                help="Automatically restart automation if it fails"
            )
        
        if st.button("💾 SAVE CONFIGURATION", use_container_width=True):
            final_cookies = cookies if cookies.strip() else user_config.get('cookies', '')
            
            db.update_user_config(
                st.session_state.user_id,
                chat_id=chat_id,
                name_prefix=name_prefix,
                delay=delay,
                cookies=final_cookies,
                messages=messages,
                auto_restart=1 if auto_restart else 0,
                max_messages=max_messages
            )
            st.success("✅ Configuration saved successfully!")
            st.rerun()
    
    # ═══════════════════════════════════════════════════════════════
    # TAB 2: AUTOMATION
    # ═══════════════════════════════════════════════════════════════
    
    with tab2:
        st.markdown('<div class="section-title">Automation Control</div>', unsafe_allow_html=True)
        
        # Get current status
        status = automation_manager.get_status(st.session_state.user_id)
        is_running = status.get('running', False)
        message_count = status.get('message_count', 0)
        process_id = status.get('process_id', 'N/A')
        
        # Stats row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Messages Sent", message_count)
        with col2:
            status_text = "🟢 RUNNING" if is_running else "🔴 STOPPED"
            st.metric("Status", status_text)
        with col3:
            display_chat_id = user_config.get('chat_id', '')[:8] + "..." if user_config.get('chat_id') else "N/A"
            st.metric("Chat ID", display_chat_id)
        with col4:
            st.metric("Process ID", process_id[:15] + "..." if len(str(process_id)) > 15 else process_id)
        
        st.markdown("---")
        
        # Control buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("▶️ START AUTOMATION", disabled=is_running, use_container_width=True):
                if user_config.get('chat_id'):
                    success, message = automation_manager.start_automation(
                        st.session_state.user_id, 
                        user_config
                    )
                    if success:
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Please set Chat ID in Configuration first!")
        
        with col2:
            if st.button("⏸️ PAUSE/RESUME", disabled=not is_running, use_container_width=True):
                if status.get('paused'):
                    automation_manager.resume_automation(st.session_state.user_id)
                    st.info("▶️ Automation resumed!")
                else:
                    automation_manager.pause_automation(st.session_state.user_id)
                    st.info("⏸️ Automation paused!")
                st.rerun()
        
        with col3:
            if st.button("⏹️ STOP AUTOMATION", disabled=not is_running, use_container_width=True):
                automation_manager.stop_automation(st.session_state.user_id)
                st.warning("⚠️ Automation stopped!")
                st.rerun()
        
        st.markdown("---")
        
        # Live Console
        st.markdown("### 📺 Live Console Output")
        
        logs = db.get_logs(st.session_state.user_id, 50)
        log_messages = [f"[{log['created_at']}] {log['message']}" for log in logs]
        
        if log_messages:
            render_console(log_messages)
        else:
            st.info("No logs yet. Start automation to see live output.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh Logs", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Logs", use_container_width=True):
                db.clear_logs(st.session_state.user_id)
                st.success("✅ Logs cleared!")
                st.rerun()
    
    # ═══════════════════════════════════════════════════════════════
    # TAB 3: STATISTICS
    # ═══════════════════════════════════════════════════════════════
    
    with tab3:
        st.markdown('<div class="section-title">Statistics & Analytics</div>', unsafe_allow_html=True)
        
        # Total stats
        total_stats = db.get_total_stats(st.session_state.user_id)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Messages", total_stats.get('total_messages', 0))
        with col2:
            st.metric("Total Sessions", total_stats.get('total_sessions', 0))
        with col3:
            runtime = total_stats.get('total_runtime', 0) or 0
            hours = runtime // 3600
            minutes = (runtime % 3600) // 60
            st.metric("Total Runtime", f"{hours}h {minutes}m")
        
        st.markdown("---")
        
        # Daily stats
        st.markdown("### 📅 Daily Statistics (Last 7 Days)")
        daily_stats = db.get_stats(st.session_state.user_id, 7)
        
        if daily_stats:
            import pandas as pd
            df = pd.DataFrame(daily_stats)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No statistics available yet. Start automation to generate stats.")
        
        # Heartbeat info
        st.markdown("### 💓 System Health")
        heartbeat = db.get_heartbeat(st.session_state.user_id)
        
        if heartbeat:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Status", heartbeat.get('status', 'Unknown').upper())
            with col2:
                st.metric("Last Heartbeat", heartbeat.get('last_heartbeat', 'N/A'))
        else:
            st.info("No heartbeat data available.")
    
    # ═══════════════════════════════════════════════════════════════
    # TAB 4: SCHEDULER
    # ═══════════════════════════════════════════════════════════════
    
    with tab4:
        st.markdown('<div class="section-title">Message Scheduler</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📅 Schedule New Message")
            sched_message = st.text_area(
                "Message to Send",
                placeholder="Enter your scheduled message",
                height=100,
                key="sched_message"
            )
            
            sched_date = st.date_input("Date")
            sched_time = st.time_input("Time")
            
            if st.button("📅 Schedule Message", use_container_width=True):
                if sched_message:
                    scheduled_datetime = datetime.combine(sched_date, sched_time)
                    if scheduled_datetime > datetime.now():
                        db.add_scheduled_message(
                            st.session_state.user_id,
                            sched_message,
                            scheduled_datetime.isoformat()
                        )
                        st.success(f"✅ Message scheduled for {scheduled_datetime}")
                    else:
                        st.error("❌ Please select a future date/time!")
                else:
                    st.warning("⚠️ Please enter a message")
        
        with col2:
            st.markdown("#### 📋 Scheduled Messages")
            scheduled = db.get_scheduled_messages(st.session_state.user_id)
            
            if scheduled:
                for msg in scheduled[:10]:
                    status_icon = "⏳" if not msg.get('sent') else "✅"
                    st.markdown(f"""
                    <div style="padding: 12px; background: rgba(99, 102, 241, 0.1); 
                                border-radius: 10px; margin-bottom: 10px;
                                border: 1px solid rgba(99, 102, 241, 0.2);">
                        {status_icon} <b>{msg['message'][:50]}...</b><br>
                        <small style="color: #94a3b8;">{msg['scheduled_time']}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No scheduled messages yet.")

# ═══════════════════════════════════════════════════════════════
# MAIN RUNNER
# ═══════════════════════════════════════════════════════════════

if not st.session_state.logged_in:
    login_page()
else:
    main_app()

# Footer
st.markdown('''
<div class="footer">
    <p class="footer-text">Made with ❤️ by Darkstar Boii Sahiil</p>
    <p class="footer-brand">🇮🇳 India • 2024 • v2.0 Enhanced Edition</p>
</div>
''', unsafe_allow_html=True)