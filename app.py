import streamlit as st
import datetime
import os
import pandas as pd
from utils import inject_custom_css, load_settings, load_credentials, delete_credentials
from data_manager import DataManager
from garmin_client import GarminClient
from ai_coach import AICoach

# UI Imports
from ui.dashboard import render_dashboard_tab
from ui.goals import render_goals_tab
from ui.journal import render_journal_tab
from ui.settings import render_settings_tab

# Configuration de la page
st.set_page_config(
    page_title="Garmin Sleep Stats",
    page_icon="🌙",
    layout="wide"
)

# --- CUSTOM CSS FOR PREMIUM UI ---
inject_custom_css()

# --- GARMIN CLIENT INITIALIZATION ---
if 'garmin_client' not in st.session_state:
    creds = load_credentials()
    if creds:
        try:
            client = GarminClient(creds['email'], creds['password'])
            success, message = client.connect()
            if success:
                st.session_state['garmin_client'] = client
            else:
                st.sidebar.error(f"Erreur Garmin : {message}")
        except Exception as e:
            st.sidebar.error(f"Erreur : {e}")

# --- MAIN NAVIGATION ---

# --- MAIN NAVIGATION ---

def check_auth():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        # --- CSS PREMIUM LOGIN ---
        st.markdown("""
            <style>
            .login-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 40px;
                background: rgba(15, 23, 42, 0.4);
                backdrop-filter: blur(20px);
                border-radius: 24px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
                max-width: 450px;
                margin: 100px auto;
                text-align: center;
            }
            .login-title {
                font-family: 'Inter', sans-serif;
                font-size: 2rem;
                font-weight: 800;
                background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 10px;
            }
            .login-subtitle {
                color: #94a3b8;
                font-size: 0.9rem;
                margin-bottom: 30px;
            }
            /* Masquer le header Streamlit sur le login */
            header {visibility: hidden;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
        """, unsafe_allow_html=True)

        if 'ACCESS_CODE' in st.secrets:
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            st.markdown('<div class="login-title">🌙 Garmin Sleep Stats</div>', unsafe_allow_html=True)
            st.markdown('<div class="login-subtitle">Accès sécurisé à votre tableau de bord biologique</div>', unsafe_allow_html=True)
            
            entered_code = st.text_input("Code d'accès", type="password", placeholder="••••", label_visibility="collapsed")
            
            if st.button("DÉVERROUILLER", type="primary", use_container_width=True):
                if entered_code == st.secrets['ACCESS_CODE']:
                    st.session_state['authenticated'] = True
                    st.rerun()
                else:
                    st.error("Code incorrect.")
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.stop()
        else:
            st.session_state['authenticated'] = True

check_auth()

tab_obj, tab_stat, tab_journal, tab_doc, tab_ai, tab_settings = st.tabs(["🎯 Objectifs", "📊 Statistiques", "📓 Journal", "📘 Guide", "💬 Coach IA", "⚙️ Réglages"])

# Fonction pour initialiser/récupérer le DataManager
def get_data_manager():
    if 'garmin_client' in st.session_state:
        if 'data_manager' not in st.session_state:
            dm = DataManager(st.session_state['garmin_client'])
            # --- AUTO-SYNC GLOBAL ---
            if 'global_sync_done' not in st.session_state:
                with st.spinner("⚡ Synchronisation intelligente des données manquantes..."):
                    try:
                        results = dm.auto_sync_missing_days(window_days=90)
                        st.session_state['global_sync_done'] = True
                        if results['synced'] > 0:
                            st.toast(f"✅ {results['synced']} nuits synchronisées automatiquement !", icon="🌙")
                    except Exception as e:
                        st.error(f"Erreur de synchro auto : {e}")
            st.session_state['data_manager'] = dm
        return st.session_state['data_manager']
    return None

# --- TAB OBJECTIFS ---
with tab_obj:
    render_goals_tab(get_data_manager)

# --- TAB STATISTIQUES ---
with tab_stat:
    render_dashboard_tab(get_data_manager)

# --- TAB JOURNAL ---
with tab_journal:
    render_journal_tab()

# --- TAB GUIDE ---
with tab_doc:
    try:
        with open("documentation.md", "r", encoding="utf-8") as f:
            content = f.read()
        st.markdown(content)
    except FileNotFoundError:
        st.warning("Guide introuvable.")
    except Exception as e:
        st.error(f"Erreur : {e}")

# --- TAB AI COACH ---
with tab_ai:
    st.subheader("💬 Coach de Sommeil (DeepSeek AI)")
    
    col_k, col_info = st.columns([2, 1])
    with col_k:
        if 'deepseek_key' not in st.session_state or not st.session_state['deepseek_key']:
            if os.path.exists("deepseek.key"):
                with open("deepseek.key", "r") as f:
                    st.session_state['deepseek_key'] = f.read().strip()
            else:
                st.session_state['deepseek_key'] = ""

        api_input = st.text_input("Clé API DeepSeek", value=st.session_state['deepseek_key'], type="password", placeholder="sk-...")
        if api_input: 
            st.session_state['deepseek_key'] = api_input

    if not st.session_state['deepseek_key']:
        st.info("🔑 Entrez votre clé API pour activer le Coach.")
    else:
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Je suis prêt à analyser votre sommeil. Que voulez-vous savoir ?"}]

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Ex: 'Pourquoi mon score baisse ?'"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("Réflexion..."):
                    try:
                        coach = AICoach(st.session_state['deepseek_key'])
                        dm_ai = get_data_manager()
                        if dm_ai:
                            e_date = datetime.date.today()
                            s_date = e_date - datetime.timedelta(days=30)
                            df_ai = dm_ai.get_dataframe(s_date, e_date, force_recent_days=0)
                            settings_ai = load_settings()
                            context = coach.generate_context(df_ai, settings_ai)
                            full_response = coach.ask(context, prompt)
                            message_placeholder.markdown(full_response)
                            st.session_state.messages.append({"role": "assistant", "content": full_response})
                        else: st.error("Lien Garmin non configuré.")
                    except Exception as e: st.error(f"Erreur : {e}")

# --- TAB RÉGLAGES ---
with tab_settings:
    render_settings_tab(get_data_manager)
