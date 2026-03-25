#!/bin/bash
# ════════════════════════════════════════════════════════════════
# DARKSTAR E2EE v2.0 - Startup Script
# ════════════════════════════════════════════════════════════════

echo "🚀 Starting Darkstar E2EE v2.0..."
echo "═══════════════════════════════════════════════════════════════"

# Check if port is already in use
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️ Port 8501 is already in use. Killing existing process..."
    kill -9 $(lsof -t -i:8501) 2>/dev/null
    sleep 2
fi

# Start Streamlit
echo "🌟 Launching Streamlit Application..."
streamlit run app_enhanced.py \
    --server.port 8501 \
    --server.headless true \
    --browser.gatherUsageStats false \
    --theme.base dark \
    --server.enableCORS false \
    --server.enableXsrfProtection false

echo "🛑 Application stopped."