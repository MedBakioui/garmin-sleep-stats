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
        # --- CSS EPIC & PRO LOGIN ---
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700;900&display=swap');
            
            /* Fond global avec animation subtile */
            .stApp {
                background: radial-gradient(circle at 15% 50%, #1e1b4b 0%, #020617 50%, #0f172a 100%) !important;
                background-size: 200% 200% !important;
                animation: gradientPulse 15s ease infinite !important;
            }
            @keyframes gradientPulse {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            /* Conteneur principal absolu */
            [data-testid="block-container"] {
                padding: 0 !important;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                max-width: 100% !important;
                position: relative;
            }

            /* La "Carte de Verre" Principale */
            .login-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 60px 50px;
                background: rgba(15, 23, 42, 0.45);
                backdrop-filter: blur(24px) saturate(180%);
                -webkit-backdrop-filter: blur(24px) saturate(180%);
                border-radius: 30px;
                border: 1px solid rgba(255, 255, 255, 0.08);
                box-shadow: 
                    0 30px 60px -15px rgba(0, 0, 0, 0.7),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
                width: 100%;
                max-width: 480px;
                text-align: center;
                z-index: 10;
                transform: translateY(0);
                animation: floatIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            }
            @keyframes floatIn {
                0% { opacity: 0; transform: translateY(30px) scale(0.95); }
                100% { opacity: 1; transform: translateY(0) scale(1); }
            }

            /* Typographie Titre */
            .login-title {
                font-family: 'Outfit', sans-serif;
                font-size: 2.8rem;
                font-weight: 900;
                background: linear-gradient(180deg, #ffffff 0%, #94a3b8 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 5px;
                letter-spacing: -1px;
                line-height: 1.1;
                filter: drop-shadow(0px 4px 10px rgba(0,0,0,0.5));
            }
            
            /* Sous-titre élégant */
            .login-subtitle {
                font-family: 'Outfit', sans-serif;
                color: #8b5cf6;
                font-size: 1.05rem;
                margin-bottom: 45px;
                font-weight: 500;
                letter-spacing: 1px;
                text-transform: uppercase;
            }
            
            /* Zone de saisie Hyper Moderne */
            div[data-baseweb="input"] {
                background: rgba(0, 0, 0, 0.3) !important;
                border: 1px solid rgba(255, 255, 255, 0.07) !important;
                border-radius: 16px !important;
                transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
                padding: 4px !important;
            }
            div[data-baseweb="input"]:focus-within {
                background: rgba(15, 23, 42, 0.8) !important;
                border-color: #8b5cf6 !important;
                box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.15) !important;
                transform: translateY(-2px);
            }
            div[data-baseweb="input"] input {
                color: #f8fafc !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 500 !important;
                font-size: 1.2rem !important;
                letter-spacing: 6px !important; /* Espacement pour les pastilles du mot de passe */
                text-align: center !important;
                padding: 14px !important;
            }
            div[data-baseweb="input"] input::placeholder {
                color: #475569 !important;
                letter-spacing: 2px !important;
                font-size: 1rem !important;
            }
            
            /* Bouton "Niveau Cyber" */
            div[data-testid="stButton"] button {
                background: linear-gradient(135deg, #4f46e5 0%, #a855f7 50%, #ec4899 100%) !important;
                background-size: 200% auto !important;
                color: white !important;
                border: none !important;
                padding: 16px !important;
                border-radius: 16px !important;
                font-family: 'Outfit', sans-serif !important;
                font-weight: 700 !important;
                font-size: 1.1rem !important;
                letter-spacing: 1.5px !important;
                text-transform: uppercase !important;
                transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
                margin-top: 15px !important;
                width: 100% !important;
                box-shadow: 0 10px 30px -10px rgba(168, 85, 247, 0.6) !important;
            }
            div[data-testid="stButton"] button:hover {
                background-position: right center !important;
                transform: translateY(-4px) !important;
                box-shadow: 0 20px 40px -10px rgba(168, 85, 247, 0.8) !important;
            }
            div[data-testid="stButton"] button:active {
                transform: translateY(1px) !important;
                box-shadow: 0 5px 15px -5px rgba(168, 85, 247, 0.5) !important;
            }

            /* Cacher Streamlit Native UI */
            header[data-testid="stHeader"] {display: none !important;}
            #MainMenu {display: none !important;}
            footer {display: none !important;}
            .stDeployButton {display: none !important;}
            .stApp > header {background-color: transparent !important;}
            
            /* Cacher les icônes d'oeil du mot de passe si on veut un look hyper clean */
            div[data-baseweb="input"] svg {
                color: #64748b !important;
                margin-right: 10px;
            }
            </style>
        """, unsafe_allow_html=True)

        if 'ACCESS_CODE' in st.secrets:
            # Injection via HTML pour garantir l'imbrication correcte (Streamlit peut parfois diviser les appels markdown)
            html_content = """
            <div class="login-container">
                <div class="login-title">Garmin Stats</div>
                <div class="login-subtitle">Biohacking Dashboard</div>
            </div>
            """
            
            # Pour insérer les inputs Streamlit à L'INTÉRIEUR du conteneur visuel, 
            # nous utilisons des colonnes fictives pour forcer Streamlit à générer des div propres,
            # mais l'approche la plus stable en Streamlit est de wrapper via markdown.
            
            # Hack Streamlit : on crée l'illusion du conteneur.
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            st.markdown('<div class="login-title">Garmin Stats</div>', unsafe_allow_html=True)
            st.markdown('<div class="login-subtitle">BIOHACKING DASHBOARD</div>', unsafe_allow_html=True)
            
            entered_code = st.text_input("Code", type="password", placeholder="CODE D'ACCÈS", label_visibility="collapsed")
            
            st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
            if st.button("DÉMARRER LA SESSION", type="primary", use_container_width=True):
                if entered_code == st.secrets['ACCESS_CODE']:
                    st.session_state['authenticated'] = True
                    st.rerun()
                else:
                    st.error("Accès Refusé.")
            
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
