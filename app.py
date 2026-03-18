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

def check_auth():
    if 'user' not in st.session_state:
        st.session_state['user'] = None

    if st.session_state['user'] is None:
        st.title("🔐 Connexion Garmin Sleep Stats")
        
        tab_login, tab_signup = st.tabs(["Se connecter", "Créer un compte"])
        
        with tab_login:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Mot de passe", type="password", key="login_password")
            if st.button("Connexion", kind="primary"):
                try:
                    # Initialisation temporaire pour l'auth
                    from supabase import create_client
                    url = st.secrets["SUPABASE_URL"]
                    key = st.secrets["SUPABASE_KEY"]
                    supabase = create_client(url, key)
                    
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state['user'] = res.user
                    st.success("Connecté !")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur : {e}")
        
        with tab_signup:
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Mot de passe", type="password", key="signup_password")
            if st.button("Créer mon compte"):
                try:
                    from supabase import create_client
                    url = st.secrets["SUPABASE_URL"]
                    key = st.secrets["SUPABASE_KEY"]
                    supabase = create_client(url, key)
                    
                    supabase.auth.sign_up({"email": new_email, "password": new_password})
                    st.info("Compte créé ! Vérifiez vos emails si nécessaire ou connectez-vous.")
                except Exception as e:
                    st.error(f"Erreur : {e}")
        st.stop()

check_auth()

if st.sidebar.button("Déconnexion"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

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
