import streamlit as st

def render_login():
    """Affiche la page de connexion épique et gère l'authentification."""
    
    # --- CSS ULTRA-PREMIUM EXPERT LOGIN v2 (Biotech Edition) ---
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;900&display=swap');
        
        /* 1. Fond Animé "Deep Biotech" (Mesh Shift) */
        .stApp {
            background-color: #020617 !important;
            background-image: 
                radial-gradient(at 0% 100%, hsla(160,84%,15%,0.3) 0, transparent 50%), 
                radial-gradient(at 100% 0%, hsla(190,90%,20%,0.3) 0, transparent 50%),
                radial-gradient(at 50% 50%, hsla(210,50%,5%,1) 0, transparent 100%);
            background-attachment: fixed !important;
            animation: colorShift 20s ease-in-out infinite alternate !important;
        }
        @keyframes colorShift {
            0% { background-position: 0% 0%; }
            100% { background-position: 100% 100%; }
        }
        
        /* 2. Hack pour cacher les éléments parasites de Streamlit */
        header[data-testid="stHeader"], 
        #MainMenu, 
        footer, 
        .stDeployButton,
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* 3. Centrage Absolu (Flexbox Container) */
        [data-testid="block-container"] {
            padding: 0 !important;
            margin: 0 !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            min-height: 100vh !important;
            max-width: 100% !important;
            position: relative;
            z-index: 10;
        }

        /* 4. La Carte "Carbon Glass" Expert */
        .login-card {
            background: rgba(8, 15, 25, 0.7);
            backdrop-filter: blur(45px) saturate(180%);
            -webkit-backdrop-filter: blur(45px) saturate(180%);
            border-radius: 28px;
            border: 1px solid rgba(0, 255, 200, 0.1);
            border-top: 1px solid rgba(0, 255, 255, 0.2);
            padding: 4rem 3rem;
            width: 100%;
            max-width: 440px;
            box-shadow: 
                0 40px 100px -20px rgba(0, 0, 0, 0.9),
                0 0 20px -5px rgba(0, 255, 200, 0.1);
            text-align: center;
            animation: emerge 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
            opacity: 0;
            transform: translateY(30px) scale(0.98);
        }
        
        @keyframes emerge {
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        /* 5. Typographie "Chrome & Emerald" */
        .login-title {
            font-family: 'Outfit', sans-serif;
            font-size: 2.6rem;
            font-weight: 900;
            color: #ffffff;
            margin-bottom: 0.3rem;
            letter-spacing: -2px;
            line-height: 1;
        }
        .login-title span {
            background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(0, 242, 254, 0.3);
        }
        
        .login-subtitle {
            font-family: 'Outfit', sans-serif;
            font-size: 0.8rem;
            color: #4ade80; /* Vert émeraude biotech */
            text-transform: uppercase;
            letter-spacing: 5px;
            margin-bottom: 3.5rem;
            font-weight: 700;
            opacity: 0.9;
        }

        /* 6. Le Champ de Texte "Void Input" */
        div[data-baseweb="input"] {
            background: rgba(0, 0, 0, 0.6) !important;
            border: 1px solid rgba(0, 255, 200, 0.05) !important;
            border-radius: 14px !important;
            padding: 8px 12px !important;
            transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
        }
        div[data-baseweb="input"]:focus-within {
            background: rgba(0, 5, 10, 0.95) !important;
            border-color: #00f2fe !important;
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.1) !important;
        }
        div[data-baseweb="input"] input {
            color: #e2e8f0 !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 1.4rem !important;
            letter-spacing: 10px !important;
            text-align: center !important;
            font-weight: 800 !important;
        }
        div[data-baseweb="input"] input::placeholder {
            color: #1e293b !important;
            letter-spacing: 3px !important;
        }
        div[data-baseweb="input"] svg { display: none !important; }

        /* 7. Le Bouton "Electric Emerald" */
        div[data-testid="stButton"] button {
            background: linear-gradient(135deg, #059669 0%, #10b981 50%, #34d399 100%) !important;
            background-size: 200% auto !important;
            color: #030014 !important; /* Texte sombre pour contraste expert */
            border: none !important;
            padding: 1.3rem !important;
            border-radius: 14px !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 900 !important;
            font-size: 1.1rem !important;
            letter-spacing: 3px !important;
            text-transform: uppercase !important;
            width: 100% !important;
            margin-top: 2rem !important;
            transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) !important;
            box-shadow: 0 20px 40px -15px rgba(16, 185, 129, 0.5) !important;
        }
        div[data-testid="stButton"] button:hover {
            background-position: right center !important;
            transform: translateY(-5px) scale(1.02) !important;
            box-shadow: 0 30px 50px -15px rgba(16, 185, 129, 0.7) !important;
            letter-spacing: 4px !important;
        }
        
        /* 8. Error Override Apex */
        [data-testid="stAlert"] {
            background: rgba(220, 38, 38, 0.05) !important;
            border: 1px solid rgba(220, 38, 38, 0.3) !important;
            color: #ef4444 !important;
            border-radius: 14px !important;
            font-weight: 600 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- HTML STRUCTURE ---
    st.markdown("""
        <div class="login-card">
            <div class="login-title">Garmin <span>Vault</span></div>
            <div class="login-subtitle">SECURE DATA INTERFACE</div>
    """, unsafe_allow_html=True)
    
    # --- LOGIQUE ---
    entered_code = st.text_input("Auth", type="password", placeholder="CODE D'ACCÈS", label_visibility="collapsed")
    
    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
    if st.button("INITIALISER LA CONNEXION", type="primary", use_container_width=True):
        if entered_code == st.secrets.get('ACCESS_CODE', ''):
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("ACCÈS RÉVOQUÉ")
            
    st.markdown("</div>", unsafe_allow_html=True)
