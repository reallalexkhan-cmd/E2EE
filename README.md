# 🚀 DARKSTAR E2EE v2.0 - ENHANCED EDITION
## 24/7 Nonstop Automation System

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-orange)

---

## ✨ NEW FEATURES

### 🔥 24/7 NONSTOP AUTOMATION
- **Auto-Restart**: Automatically restarts if automation crashes
- **Heartbeat Monitoring**: Real-time health checks every 30 seconds
- **Background Worker**: Dedicated service for monitoring and recovery

### 🎨 MODERN UI DESIGN
- **Glassmorphism**: Beautiful glass-like interface
- **Dark/Light Themes**: Choose your preferred theme
- **Responsive Design**: Works on all screen sizes

### 📊 ANALYTICS & STATISTICS
- **Real-time Dashboard**: Live message count and status
- **Daily Statistics**: Track your automation performance
- **Console Output**: Live logs with color coding

### 📅 MESSAGE SCHEDULER
- **Schedule Messages**: Set messages to send at specific times
- **Multiple Schedules**: Queue multiple scheduled messages

---

## 🚀 QUICK START

### Option 1: Run with Script
```bash
./start.sh
```

### Option 2: Run Directly
```bash
streamlit run app_enhanced.py --server.port 8501
```

### Access the App
Open your browser and go to: `http://localhost:8501`

---

## 📁 FILE STRUCTURE

```
/workspace/
├── app_enhanced.py          # Main Streamlit application
├── automation_engine.py     # 24/7 automation engine
├── background_worker.py     # Background monitoring service
├── database_enhanced.py     # Enhanced database system
├── requirements_enhanced.txt # Python dependencies
├── start.sh                 # Startup script
└── README.md                # This file
```

---

## ⚙️ CONFIGURATION

### Required Settings
1. **E2EE Chat ID**: Your Facebook conversation ID
2. **Facebook Cookies**: Your session cookies (encrypted)
3. **Messages**: One message per line

### Optional Settings
- **Name Prefix**: Add prefix to each message
- **Delay**: Time between messages (seconds)
- **Max Messages**: Limit messages (0 = unlimited)
- **Auto-Restart**: Restart on failure

---

## 🔐 SECURITY

- All cookies are **encrypted** using Fernet encryption
- Passwords are **hashed** with SHA-256 + salt
- Session data is **never exposed** to other users

---

## 🛠️ TROUBLESHOOTING

### Browser Not Found
```bash
sudo apt-get install chromium chromium-driver
```

### Port Already in Use
```bash
kill -9 $(lsof -t -i:8501)
```

### Reset Database
```bash
rm darkstar_enhanced.db .encryption_key
```

---

## 👨‍💻 DEVELOPER

**Darkstar Boii Sahiil** 🇮🇳

---

## 📜 LICENSE

This project is for educational purposes only. Use responsibly.

---

## 🌟 ACCESS YOUR APP

**Live URL: https://00pcj.app.super.myninja.ai**

Enjoy your 24/7 nonstop automation! 🚀