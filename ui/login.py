import streamlit as st

def render_login():
    """Affiche la page de connexion calquée exactement sur l'image de référence."""

    # --- CSS PIXEL-PERFECT LOGIN ---
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Josefin+Sans:wght@100;200;300;400;600&display=swap');

        /* 1. Global Reset & Fond Immersif avec Particules */
        .stApp {
            background: #010409 !important;
            font-family: 'Josefin Sans', sans-serif;
            overflow: hidden !important;
        }

        /* Particules subtiles en fond */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(91,142,230,0.05) 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(91,142,230,0.05) 0%, transparent 40%),
                radial-gradient(1px 1px at 10% 10%, #fff 100%, transparent 0),
                radial-gradient(1px 1px at 20% 50%, #fff 100%, transparent 0),
                radial-gradient(1px 1px at 70% 20%, #fff 100%, transparent 0),
                radial-gradient(1px 1px at 40% 80%, #fff 100%, transparent 0),
                radial-gradient(1px 1px at 90% 90%, #fff 100%, transparent 0);
            background-size: 100% 100%, 100% 100%, 300px 300px, 400px 400px, 350px 350px, 250px 250px, 500px 500px;
            opacity: 0.3;
            z-index: 0;
            pointer-events: none;
        }

        /* 2. Cacher Streamlit */
        header[data-testid="stHeader"], 
        #MainMenu, 
        footer, 
        .stDeployButton, 
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* 3. Container de centrage */
        [data-testid="block-container"] {
            padding: 0 !important;
            margin: 0 !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            min-height: 100vh !important;
            max-width: 100% !important;
            z-index: 10;
        }

        /* 4. La Carte (Look Image) */
        .login-card {
            position: relative;
            width: 100%;
            max-width: 480px;
            padding: 5rem 4rem 4rem;
            background: rgba(4, 7, 20, 0.85);
            border: 0.5px solid rgba(255, 255, 255, 0.03); /* Bordure très fine */
            box-shadow: 0 50px 100px -20px rgba(0, 0, 0, 0.8);
            border-radius: 4px;
            text-align: center;
            backdrop-filter: blur(20px);
            animation: fadeIn 1.5s ease;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* Coins en L (Coins décoratifs de l'image) */
        .corner {
            position: absolute;
            width: 15px; height: 15px;
            border-color: rgba(91, 142, 230, 0.2);
            border-style: solid;
        }
        .corner-tl { top: 20px; left: 20px; border-width: 0.5px 0 0 0.5px; }
        .corner-tr { top: 20px; right: 20px; border-width: 0.5px 0.5px 0 0; }
        .corner-bl { bottom: 20px; left: 20px; border-width: 0 0 0.5px 0.5px; }
        .corner-br { bottom: 20px; right: 20px; border-width: 0 0.5px 0.5px 0; }

        /* 5. Logo (Carré +) */
        .logo-box {
            width: 48px; height: 48px;
            border: 0.5px solid rgba(91, 142, 230, 0.4);
            margin: 0 auto 3rem;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        .logo-box::before {
            content: '+';
            font-family: 'Josefin Sans', sans-serif;
            font-size: 24px;
            font-weight: 200;
            color: rgba(91, 142, 230, 0.6);
        }

        /* 6. Titre & Sous-titre Style Image */
        .login-title {
            font-family: 'Cormorant Garamond', serif;
            font-size: 3.2rem;
            font-weight: 300;
            color: #ffffff;
            letter-spacing: 4px;
            margin-bottom: 0.5rem;
            line-height: 1;
        }
        .login-title span {
            color: #5b8ee6;
            margin-left: 10px;
        }
        .login-subtitle {
            font-family: 'Josefin Sans', sans-serif;
            font-size: 0.75rem;
            color: rgba(91, 142, 230, 0.6);
            letter-spacing: 6px;
            text-transform: uppercase;
            font-weight: 400;
            margin-bottom: 4rem;
        }

        /* 7. Séparateur (Dot & Lines) */
        .divider-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-bottom: 4rem;
        }
        .divider-line {
            width: 100px; height: 0.5px;
            background: linear-gradient(to right, transparent, rgba(91, 142, 230, 0.2), transparent);
        }
        .divider-dot {
            width: 3px; height: 3px;
            background: rgba(91, 142, 230, 0.6);
            border-radius: 50%;
        }

        /* 8. Labels & Inputs */
        .input-label {
            font-family: 'Josefin Sans', sans-serif;
            font-size: 0.65rem;
            color: rgba(91, 142, 230, 0.5);
            letter-spacing: 5px;
            text-transform: uppercase;
            margin-bottom: 1.5rem;
            display: block;
        }

        div[data-baseweb="input"] {
            background: rgba(43, 45, 43, 0.2) !important; /* Couleur sombre du mdp de l'image */
            border: 0.5px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            padding: 5px !important;
        }
        div[data-baseweb="input"] input {
            color: #ffffff !important;
            text-align: center !important;
            font-size: 1.5rem !important;
            letter-spacing: 12px !important;
            padding: 15px !important;
        }
        div[data-baseweb="input"] svg { display: none !important; }

        /* 9. Bouton Style Image */
        div[data-testid="stButton"] {
            margin-top: 2rem !important;
        }
        div[data-testid="stButton"] button {
            background: rgba(4, 7, 20, 0.8) !important;
            border: 0.5px solid rgba(91, 142, 230, 0.3) !important;
            color: #ffffff !important;
            border-radius: 8px !important;
            padding: 1.2rem !important;
            width: 100% !important;
            font-family: 'Josefin Sans', sans-serif !important;
            font-size: 1.1rem !important;
            letter-spacing: 8px !important;
            text-transform: uppercase !important;
            font-weight: 300 !important;
            transition: all 0.4s ease !important;
        }
        div[data-testid="stButton"] button:hover {
            border-color: #5b8ee6 !important;
            background: rgba(91, 142, 230, 0.05) !important;
            box-shadow: 0 0 20px rgba(91, 142, 230, 0.1) !important;
        }

        /* 10. Footer */
        .login-footer {
            margin-top: 4rem;
            font-family: 'Josefin Sans', sans-serif;
            font-size: 0.6rem;
            color: rgba(91, 142, 230, 0.25);
            letter-spacing: 5px;
            text-transform: uppercase;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- STRUCTURE HTML PIXEL-PERFECT ---
    st.markdown("""
        <div class="login-card">
            <div class="corner corner-tl"></div>
            <div class="corner corner-tr"></div>
            <div class="corner corner-bl"></div>
            <div class="corner corner-br"></div>

            <div class="logo-box"></div>
            
            <div class="login-title">Garmin <span>Stats</span></div>
            <div class="login-subtitle">BIOHACKING CENTRAL</div>

            <div class="divider-container">
                <div class="divider-line"></div>
                <div class="divider-dot"></div>
                <div class="divider-line"></div>
            </div>

            <div class="input-label">CODE D'ACCÈS SÉCURISÉ</div>
    """, unsafe_allow_html=True)

    # Input Streamlit
    entered_code = st.text_input(
        "Code", 
        type="password", 
        placeholder="••••••••", 
        label_visibility="collapsed"
    )

    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)

    if st.button("INITIALISER LA SESSION"):
        if entered_code == st.secrets.get('ACCESS_CODE', ''):
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("ACCÈS RÉVOQUÉ")

    st.markdown("""
            <div class="login-footer">SYSTÈME SÉCURISÉ · ACCÈS RESTREINT</div>
        </div>
    """, unsafe_allow_html=True)
