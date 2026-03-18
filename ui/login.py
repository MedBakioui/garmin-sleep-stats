import streamlit as st
import pyotp
import qrcode
from io import BytesIO
import extra_streamlit_components as stx
import datetime

def get_cookie_manager():
    return stx.CookieManager(key="garmin_cookies")

def render_login():
    """Affiche une page de connexion native avec Authentification TOTP (Google Authenticator) et QR Code."""
    
    # --- LOGIQUE REMEMBER ME (COOKIES) ---
    login_token = st.secrets.get('ACCESS_CODE', 'default_token')
    
    cookie_manager = get_cookie_manager()
    
    # 1. Lecture native et synchrone (Streamlit 1.30+)
    saved_token = None
    if hasattr(st, 'context') and hasattr(st.context, 'cookies'):
        saved_token = st.context.cookies.get("garmin_stats_auth_token")
    
    # 2. Fallback via le composant (Asynchrone)
    if not saved_token:
        try:
            saved_token = cookie_manager.get(cookie="garmin_stats_auth_token")
        except:
            pass

    if saved_token == login_token:
        st.session_state['authenticated'] = True
        st.rerun()

    if st.query_params.get("remember") == login_token:
        st.session_state['authenticated'] = True
        cookie_manager.set("garmin_stats_auth_token", login_token, expires_at=datetime.datetime.now() + datetime.timedelta(days=365))
        st.rerun()

    # Initialisation de l'état de l'authentification
    if 'login_step' not in st.session_state:
        st.session_state['login_step'] = 1
        
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("")
        st.write("")
        st.title("🔐 Garmin Stats")
        st.subheader("Biohacking Central")
        
        # --- ÉTAPE 1 : CODE D'ACCÈS ---
        if st.session_state['login_step'] == 1:
            st.info("Étape 1 : Entrez votre code d'accès principal.")
            with st.form("form_step1"):
                code1 = st.text_input("Code d'accès", type="password", placeholder="••••••••")
                remember_me = st.checkbox("Se souvenir de moi sur ce navigateur", value=True)
                submit1 = st.form_submit_button("Continuer", use_container_width=True)
                
                if submit1:
                    if code1 == st.secrets.get('ACCESS_CODE', ''):
                        st.session_state['remember_me'] = remember_me
                        st.session_state['login_step'] = 2
                        st.rerun()
                    else:
                        st.error("Code principal incorrect.")
                        
        # --- ÉTAPE 2 : TOTP (2FA) ---
        elif st.session_state['login_step'] == 2:
            if st.session_state.get('login_success_wait', False):
                st.success("✅ Connexion réussie et Cookie sauvegardé !")
                st.info("Votre session a été mise en mémoire cache sécurisée.")
                if st.button("🚀 Entrer dans le tableau de bord", use_container_width=True, type="primary"):
                    st.session_state['authenticated'] = True
                    st.session_state['login_step'] = 1
                    del st.session_state['login_success_wait']
                    st.rerun()
            else:
                st.success("Étape 1 validée.")
                st.warning("Étape 2 : Entrez le code de votre application 2FA.")
                
                with st.form("form_step2"):
                    totp_secret = st.secrets.get('TOTP_SECRET', '').strip()
                    code2 = st.text_input("Code 2FA (6 chiffres)", placeholder="Ex: 123456")
                    submit2 = st.form_submit_button("Vérifier", use_container_width=True)
                    
                    if submit2:
                        if totp_secret:
                            try:
                                totp = pyotp.TOTP(totp_secret)
                                if totp.verify(code2.strip()):
                                    # Si Remember Me était coché, on persiste le token dans le navigateur via un Cookie
                                    if st.session_state.get('remember_me', False):
                                        cookie_manager.set("garmin_stats_auth_token", login_token, expires_at=datetime.datetime.now() + datetime.timedelta(days=365))
                                        st.session_state['login_success_wait'] = True
                                        st.rerun()
                                    else:
                                        st.session_state['authenticated'] = True
                                        st.session_state['login_step'] = 1
                                        st.rerun()
                                else:
                                    st.error("Code 2FA invalide ou expiré.")
                            except Exception as e:
                                st.error(f"Erreur technique 2FA : {e}")
                # Aide & QR Code
                with st.expander("Configurer Google Authenticator"):
                    if totp_secret:
                        provisioning_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(name="Utilisateur", issuer_name="Garmin Stats")
                        qr = qrcode.QRCode(version=1, box_size=10, border=4)
                        qr.add_data(provisioning_uri)
                        qr.make(fit=True)
                        img = qr.make_image(fill_color="black", back_color="white")
                        buf = BytesIO()
                        img.save(buf, format="PNG")
                        st.image(buf.getvalue(), caption="Scannez avec votre téléphone", width=200)
                    else:
                        st.error("Secret TOTP introuvable.")
                
                if st.button("← Retour"):
                    st.session_state['login_step'] = 1
                    st.rerun()
        
        st.divider()
        st.caption("Sécurité TOTP active. En cochant 'Se souvenir de moi', une clé est enregistrée dans votre navigateur.")
