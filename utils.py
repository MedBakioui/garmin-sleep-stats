import streamlit as st
import json
import os
from typing import Optional, Dict, Any

CREDENTIALS_FILE = "credentials.json"
SETTINGS_FILE = "settings.json"

def inject_custom_css() -> None:
    """Injects custom CSS to style the Streamlit application with a premium dark theme."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        /* --- GLOBAL THEME --- */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #0f172a; /* Slate 900 */
            color: #f1f5f9; /* Slate 100 */
        }
        
        /* --- SIDEBAR --- */
        [data-testid="stSidebar"] {
            background-color: #020617; /* Slate 950 */
            border-right: 1px solid #1e293b;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
             color: #94a3b8;
        }

        /* --- HEADERS --- */
        h1, h2, h3, h4, h5 {
            font-weight: 700;
            color: #f1f5f9;
        }
        h1 {
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* --- METRIC CARDS (GLASSMORPHISM) --- */
        div[data-testid="metric-container"] {
            background: rgba(30, 41, 59, 0.7); /* Transparence */
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease, border-color 0.2s;
        }
        div[data-testid="metric-container"]:hover {
            transform: translateY(-2px);
            border-color: #3b82f6;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        }
        label[data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
            color: #94a3b8 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
            color: #e2e8f0 !important;
        }

        /* --- TABS --- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
            margin-bottom: 20px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 40px;
            border-radius: 8px;
            color: #94a3b8;
            background-color: #1e293b;
            border: 1px solid #334155;
            flex: 1; /* Stretch */
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
            color: white !important;
            border: none;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }

        /* --- BUTTONS --- */
        div[data-testid="stButton"] button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s;
        }
        /* Primary */
        div[data-testid="stButton"] button[kind="primary"] {
            background: linear-gradient(90deg, #3b82f6, #6366f1);
            border: none;
            box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
        }
        div[data-testid="stButton"] button[kind="primary"]:hover {
             transform: scale(1.02);
             box-shadow: 0 4px 8px rgba(59, 130, 246, 0.5);
        }
        
        /* --- ALERTS & INFO --- */
        div[data-baseweb="notification"] {
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        /* --- CUSTOM SCROLLBAR --- */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0f172a; 
        }
        ::-webkit-scrollbar-thumb {
            background: #334155; 
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #475569; 
        }

        </style>
    """, unsafe_allow_html=True)


def load_credentials() -> Optional[Dict[str, str]]:
    """Loads user credentials from secrets or local file.
    
    Priority:
    1. Streamlit Secrets (for cloud deployment)
    2. Local credentials.json (for local development)

    Returns:
        Optional[Dict[str, str]]: A dictionary containing 'email' and 'password' if found, None otherwise.
    """
    # 1. Check Streamlit Secrets
    if 'GARMIN_EMAIL' in st.secrets and 'GARMIN_PASSWORD' in st.secrets:
        return {
            "email": st.secrets['GARMIN_EMAIL'],
            "password": st.secrets['GARMIN_PASSWORD']
        }

    # 2. Check local file
    if os.path.exists(CREDENTIALS_FILE):
        try:
            with open(CREDENTIALS_FILE, "r") as f:
                return json.load(f)
        except:
            return None
    return None

def save_credentials(email: str, password: str) -> None:
    """Saves user credentials to a local file.

    Args:
        email (str): The user's Garmin email.
        password (str): The user's Garmin password.
    """
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump({"email": email, "password": password}, f)

def delete_credentials() -> None:
    """Deletes the stored credentials file if it exists."""
    if os.path.exists(CREDENTIALS_FILE):
        os.remove(CREDENTIALS_FILE)

# --- NOUVEAUX : GESTION DES REGLAGES (OBJECTIFS) ---

def load_settings() -> Dict[str, Any]:
    """Loads user sleep goals and settings from local settings.json.
    
    Returns:
        Dict[str, Any]: A dictionary of settings with default values.
    """
    defaults = {
        "target_duration": 8.0,
        "target_deep_pct": 20,
        "target_bedtime": "23:00"
    }
    
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                saved = json.load(f)
                defaults.update(saved)
        except:
            pass
    return defaults

def save_settings(settings_dict: Dict[str, Any]) -> None:
    """Saves user settings to local settings.json file.
    """
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings_dict, f)
    except Exception as e:
        print(f"Erreur sauvegarde settings: {e}")
