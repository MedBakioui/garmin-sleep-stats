#!/bin/bash
# This script creates a Streamlit secrets.toml from Render environment variables
# before starting the Streamlit app.

echo "🔧 Generating secrets.toml from environment variables..."

mkdir -p /app/.streamlit

cat > /app/.streamlit/secrets.toml <<EOF
# Auto-generated from Render environment variables
ACCESS_CODE = "${ACCESS_CODE:-default}"
TOTP_SECRET = "${TOTP_SECRET:-}"
GARMIN_EMAIL = "${GARMIN_EMAIL:-}"
GARMIN_PASSWORD = "${GARMIN_PASSWORD:-}"
DEEPSEEK_KEY = "${DEEPSEEK_KEY:-}"
GARMIN_SESSION = '${GARMIN_SESSION:-}'
SUPABASE_URL = "${SUPABASE_URL:-}"
SUPABASE_KEY = "${SUPABASE_KEY:-}"
EOF

echo "✅ secrets.toml created."

# Start Streamlit
exec streamlit run app.py --server.port=8501 --server.address=0.0.0.0
