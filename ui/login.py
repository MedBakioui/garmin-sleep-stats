import streamlit as st
import pyotp
import qrcode
from io import BytesIO

def render_login():
    """Affiche une page de connexion native avec Authentification TOTP (Google Authenticator) et QR Code."""
    
    # --- LOGIQUE REMEMBER ME (LOCAL STORAGE) ---
    login_token = st.secrets.get('ACCESS_CODE', 'default_token')
    
    # Script JS pour détecter s'il y a un token sauvegardé et rediriger
    st.markdown(f"""
        <script>
        const token = "{login_token}";
        const savedToken = localStorage.getItem("garmin_stats_auth_token");
        const urlParams = new URLSearchParams(window.location.search);
        
        // Si on a un token et qu'on n'est pas déjà en train de se déconnecter
        if (savedToken === token && !urlParams.has("logout") && !urlParams.has("remember")) {{
            // On ajoute le paramètre 'remember' à l'URL et on recharge
            urlParams.set("remember", token);
            window.location.search = urlParams.toString();
        }}
        </script>
    """, unsafe_allow_html=True)

    # Récupération automatique si le paramètre remember est présent
    if st.query_params.get("remember") == login_token:
        st.session_state['authenticated'] = True
        # On peut aussi sauvegarder dans localStorage ici par sécurité
        st.markdown(f'<script>localStorage.setItem("garmin_stats_auth_token", "{login_token}");</script>', unsafe_allow_html=True)

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
                                st.session_state['authenticated'] = True
                                # Si Remember Me était coché, on persiste le token dans le navigateur
                                if st.session_state.get('remember_me', False):
                                    st.query_params["remember"] = login_token
                                    st.markdown(f'<script>localStorage.setItem("garmin_stats_auth_token", "{login_token}");</script>', unsafe_allow_html=True)
                                
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
