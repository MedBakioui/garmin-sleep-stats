import streamlit as st
import datetime
import os
import json
from secret_helper import get_secret
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

# --- MAIN NAVIGATION ---

def check_auth():
    """Vérifie l'authentification. Affiche la page de connexion si nécessaire."""
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        # On force toujours l'affichage de la page de connexion
        try:
            from ui.login import render_login
            render_login()
            
            # Message d'alerte si les secrets sont absents (cas courant de déploiement)
            if not get_secret('ACCESS_CODE'):
                st.warning("⚠️ ATTENTION : ACCESS_CODE non trouvé dans les Secrets. L'authentification ne fonctionnera pas tant que vous ne l'avez pas configurée.")
                
            st.stop()
        except ImportError:
            st.error("Fichier ui/login.py introuvable.")
            st.stop()

check_auth()

# --- FONCTION DE CACHE POUR LE CLIENT GARMIN ---
@st.cache_resource(show_spinner=False)
def get_cached_garmin_client(email, password, session_token=None):
    from garmin_client import GarminClient
    client = GarminClient(email, password, session_token=session_token)
    success, message = client.connect()
    return client, success, message

# --- AUTO-LOGIN GARMIN ---
if 'garmin_client' not in st.session_state:
    from utils import load_credentials
    creds = load_credentials()
    
    # Vérification du verrouillage temporaire (429)
    is_locked = False
    lock_duration = 1800 # 30 minutes de sécurité
    if 'last_429_time' in st.session_state:
        elapsed = (datetime.datetime.now() - st.session_state['last_429_time']).total_seconds()
        if elapsed < lock_duration:
            is_locked = True
            remaining = int((lock_duration - elapsed) / 60)
            st.error("⚠️ **Garmin : Accès bloqués (Erreur 429).**")
            st.warning(f"Garmin a restreint votre IP. L'application est verrouillée pour encore **~{remaining} minutes** pour éviter une extension du bannissement.")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🔄 Tenter de forcer la reconnexion"):
                    del st.session_state['last_429_time']
                    st.rerun()
            with c2:
                if st.button("🗑️ Effacer la session locale"):
                    if os.path.exists("garmin_session.json"):
                        os.remove("garmin_session.json")
                        st.success("Session effacée. Réessayez dans 15 minutes.")
                    else:
                        st.info("Aucun fichier de session trouvé.")

    # On ne tente l'auto-login au démarrage que si :
    # 1. On a des identifiants
    # 2. ET (On n'est pas verrouillé OU on a un jeton de session pour contourner le verrouillage)
    # 3. ET On n'a pas déjà fait l'auto-login dans cette session Streamlit
    has_session_token = creds and creds.get('session')
    
    if creds and (not is_locked or has_session_token) and 'auto_login_done' not in st.session_state:
        st.session_state['auto_login_done'] = True
        with st.spinner("🚀 Restauration de votre session Garmin..." if has_session_token else "Initialisation du profil Garmin..."):
            client, success, message = get_cached_garmin_client(creds['email'], creds['password'], creds.get('session'))
            if success:
                st.session_state['garmin_client'] = client
                st.toast("✅ Profil Garmin chargé automatiquement")
                # On nettoie le flag 429 si la connexion réussit
                if 'last_429_time' in st.session_state:
                    del st.session_state['last_429_time']
            else:
                if "429" in message or "Rate limit" in message or "Too Many Requests" in message:
                    st.session_state['last_429_time'] = datetime.datetime.now()
                    get_cached_garmin_client.clear()
                    st.rerun() # Refresh pour afficher le message de verrouillage
                else:
                    st.error(f"Erreur de connexion Garmin : {message}")
                    get_cached_garmin_client.clear()

tab_obj, tab_stat, tab_journal, tab_doc, tab_ai, tab_settings = st.tabs(["🎯 Objectifs", "📊 Statistiques", "📓 Journal", "📘 Guide", "💬 Coach IA", "⚙️ Réglages"])

# Fonction pour initialiser/récupérer le DataManager
def get_data_manager():
    if 'garmin_client' in st.session_state:
        if 'data_manager' not in st.session_state:
            dm = DataManager(st.session_state['garmin_client'])
            # --- AUTO-SYNC GLOBAL ---
            if 'global_sync_done' not in st.session_state:
                with st.spinner("⚡ Synchronisation intelligente des données manquantes (Prudence 429)..."):
                    try:
                        # On réduit la fenêtre par défaut à 30 jours au lieu de 90 pour être moins agressif
                        # mais on peut garder 90 si on gère bien l'interruption
                        results = dm.auto_sync_missing_days(window_days=60)
                        st.session_state['global_sync_done'] = True
                        if results['synced'] > 0:
                            st.toast(f"✅ {results['synced']} nuits synchronisées !", icon="🌙")
                    except Exception as e:
                        if "429" in str(e):
                            st.session_state['last_429_time'] = datetime.datetime.now()
                            st.warning("⚠️ Sync interrompue : Garmin a limité les requêtes. Les données déjà récupérées sont sauvegardées.")
                            st.session_state['global_sync_done'] = True # On marque quand même comme "fait" pour ne pas reboucler
                        else:
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
        # 1. Vérifie si une clé DeepSeek est configurée
        deepseek_key = get_secret('DEEPSEEK_KEY')
        if deepseek_key:
            st.session_state['deepseek_key'] = deepseek_key
        # Secondaire : Fichier local (pour le dev)
        elif os.path.exists("deepseek.key"):
            with open("deepseek.key", "r") as f:
                st.session_state['deepseek_key'] = f.read().strip()
        else:
            if 'deepseek_key' not in st.session_state: # Initialize if not present
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
