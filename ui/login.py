import streamlit as st
import pyotp
import qrcode
from io import BytesIO

def render_login():
    """Affiche une page de connexion native avec Authentification TOTP (Google Authenticator) et QR Code."""
    
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
                submit1 = st.form_submit_button("Continuer", use_container_width=True)
                
                if submit1:
                    if code1 == st.secrets.get('ACCESS_CODE', ''):
                        st.session_state['login_step'] = 2
                        st.rerun()
                    else:
                        st.error("Code principal incorrect.")
                        
        # --- ÉTAPE 2 : TOTP (2FA) ---
        elif st.session_state['login_step'] == 2:
            st.success("Étape 1 validée.")
            st.warning("Étape 2 : Entrez le code 6 chiffres affiché par Google Authenticator sur votre téléphone.")
            
            with st.form("form_step2"):
                # Récupération du secret TOTP depuis les secrets
                totp_secret = st.secrets.get('TOTP_SECRET', '').strip()
                
                code2 = st.text_input("Code 2FA (6 chiffres)", placeholder="Ex: 123456")
                submit2 = st.form_submit_button("Vérifier", use_container_width=True)
                
                if submit2:
                    if totp_secret:
                        try:
                            totp = pyotp.TOTP(totp_secret)
                            # On vérifie le code (on autorise une petite fenêtre de temps pour la synchro)
                            if totp.verify(code2.strip()):
                                st.session_state['authenticated'] = True
                                st.session_state['login_step'] = 1 # Reset
                                st.rerun()
                            else:
                                st.error("Code 2FA invalide ou expiré. Assurez-vous d'avoir bien scanné le dernier QR Code.")
                        except Exception as e:
                            st.error(f"Erreur technique 2FA : {e}")
                    else:
                        st.error("Configuration 2FA manquante dans les secrets.")
            
            # Aide à l'installation / affichage du QR Code
            with st.expander("Comment configurer mon application Google Authenticator ?"):
                st.write("1. Ouvrez Google Authenticator sur votre smartphone.")
                st.write("2. Appuyez sur le '+' et choisissez 'Scanner un code QR'.")
                st.write("3. Scannez le code ci-dessous :")
                
                if totp_secret:
                    try:
                        # Génération de l'URI provisioning pour le QR Code
                        provisioning_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(
                            name="Utilisateur", 
                            issuer_name="Garmin Stats"
                        )
                        
                        # Création du QR Code
                        qr = qrcode.QRCode(version=1, box_size=10, border=4)
                        qr.add_data(provisioning_uri)
                        qr.make(fit=True)
                        img = qr.make_image(fill_color="black", back_color="white")
                        
                        # Conversion pour affichage
                        buf = BytesIO()
                        img.save(buf, format="PNG")
                        st.image(buf.getvalue(), caption="Scan QR Code", width=200)
                        
                        st.info(f"Secret manuel : `{totp_secret}`")
                    except Exception as e:
                        st.error(f"Erreur de génération du QR Code : {e}")
                else:
                    st.error("Secret TOTP introuvable.")
            
            if st.button("← Retour à l'étape 1"):
                st.session_state['login_step'] = 1
                st.rerun()
        
        st.divider()
        st.caption("Sécurité renforcée par Google Authenticator (TOTP).")
