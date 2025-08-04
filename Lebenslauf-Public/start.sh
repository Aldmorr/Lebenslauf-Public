#!/bin/bash

echo "🚀 Starting CV Chatbot..."

# Kill any existing streamlit processes
pkill -f streamlit 2>/dev/null || true

# Wait a moment
sleep 2

# Start streamlit
echo "📱 Starting Streamlit app..."
streamlit run app.py --server.port 8501

echo "✅ App should be running at http://localhost:8501"