
import streamlit as st
from garmin_client import GarminClient
from utils import load_credentials, save_credentials, delete_credentials

def render_settings_tab(get_data_manager_func):
    """Affiche l'onglet Réglages (Connexion & Cache)."""
    col_auth, col_data = st.columns(2, gap="large")
    
    with col_auth:
        st.subheader("🔑 Connexion Garmin")

        # Formulaire de connexion ou État connecté
        if 'garmin_client' not in st.session_state:
            with st.form("garmin_login_form"):
                email = st.text_input("Email Garmin")
                password = st.text_input("Mot de passe", type="password")
                save_locally = st.checkbox("Rester connecté (Enregistrer localement)", value=True)
                submit = st.form_submit_button("Se connecter", type="primary")
            
            if submit:
                if email and password:
                    client = GarminClient(email, password)
                    with st.spinner("Connexion en cours..."):
                        success, message = client.connect()
                    if success:
                        st.session_state['garmin_client'] = client
                        if save_locally:
                            save_credentials(email, password)
                        st.success("Connecté et synchronisé !")
                        st.rerun()
                    else:
                        st.error(f"Erreur : {message}")
                else:
                    st.warning("Veuillez remplir tous les champs")
        else:
            st.success("✅ Garmin Connecté")
            if st.button("🔌 Déconnecter Garmin", type="secondary"):
                if 'garmin_client' in st.session_state: del st.session_state['garmin_client']
                if 'data_manager' in st.session_state: del st.session_state['data_manager']
                st.rerun()
            
            if st.button("🗑️ Oublier mes identifiants locaux"):
                delete_credentials()
                if 'garmin_client' in st.session_state: del st.session_state['garmin_client']
                st.success("Identifiants supprimés du disque.")
                st.rerun()

    with col_data:
        st.subheader("💾 Gestion du Cache")
        dm_settings = get_data_manager_func()
        
        if dm_settings:
            # Note: dm_settings._sleep_cache est un dictionnaire
            cache_size = len(dm_settings._sleep_cache)
            st.metric("Taille du Cache", f"{cache_size} nuits", help="Données stockées dans sleep_cache.json")
            
            if st.button("🗑️ Vider le cache local"):
                dm_settings._sleep_cache = {}
                dm_settings._metrics_cache = {}
                dm_settings._save_cache(dm_settings._sleep_cache, dm_settings.__class__.__module__.replace('data_manager', 'sleep_cache.json')) # Dynamic path might be tricky, use hardcoded for safety
                # Actually, use the constants from DataManager if accessible or just clear files
                from data_manager import CACHE_FILE, METRICS_CACHE_FILE
                dm_settings._save_cache({}, CACHE_FILE)
                dm_settings._save_cache({}, METRICS_CACHE_FILE)
                
                if 'data_manager' in st.session_state:
                    del st.session_state['data_manager']
                st.success("Cache vidé.")
                st.rerun()
        else:
            st.info("Connectez-vous pour gérer le cache.")
