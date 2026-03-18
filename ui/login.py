import streamlit as st

def render_login():
    """Affiche la page de connexion luxury minimaliste bleue (Version originale)."""

    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Josefin+Sans:wght@100;200;300;400&display=swap');

        /* 1. Reset & fond */
        * { margin: 0; padding: 0; box-sizing: border-box; }

        .stApp {
            background: #03050f !important;
            font-family: 'Josefin Sans', sans-serif;
        }

        /* 2. Lumières ambiantes */
        .stApp::before {
            content: '';
            position: fixed;
            width: 600px; height: 600px;
            background: radial-gradient(circle, rgba(59,111,212,0.12) 0%, transparent 70%);
            top: -200px; left: -200px;
            pointer-events: none;
            z-index: 0;
            animation: drift1 18s ease-in-out infinite alternate;
        }
        .stApp::after {
            content: '';
            position: fixed;
            width: 400px; height: 400px;
            background: radial-gradient(circle, rgba(26,58,122,0.1) 0%, transparent 70%);
            bottom: -150px; right: -100px;
            pointer-events: none;
            z-index: 0;
            animation: drift2 24s ease-in-out infinite alternate;
        }
        @keyframes drift1 {
            0%   { transform: translate(0, 0) scale(1); }
            100% { transform: translate(30px, -20px) scale(1.1); }
        }
        @keyframes drift2 {
            0%   { transform: translate(0, 0) scale(1); }
            100% { transform: translate(-20px, 15px) scale(1.08); }
        }

        /* 3. Masquer éléments Streamlit */
        header[data-testid="stHeader"],
        #MainMenu,
        footer,
        .stDeployButton,
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        /* 4. Centrage */
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

        /* 5. La carte */
        .login-card {
            position: relative;
            width: 100%;
            max-width: 420px;
            padding: 3.5rem 2.8rem 3rem;
            background: rgba(6, 10, 28, 0.78);
            border: 0.5px solid rgba(91, 142, 230, 0.18);
            border-top: 0.5px solid rgba(91, 142, 230, 0.45);
            border-radius: 2px;
            backdrop-filter: blur(60px);
            -webkit-backdrop-filter: blur(60px);
            animation: cardReveal 1.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            opacity: 0;
            transform: translateY(40px);
            overflow: hidden;
        }

        @keyframes cardReveal {
            to { opacity: 1; transform: translateY(0); }
        }

        /* Ligne dorée haut */
        .login-card::before {
            content: '';
            position: absolute;
            top: 0; left: 10%; right: 10%;
            height: 1px;
            background: linear-gradient(to right, transparent, #5b8ee6, transparent);
            opacity: 0.5;
        }

        /* Scan de lumière */
        .login-card::after {
            content: '';
            position: absolute;
            top: -50%; left: -60%;
            width: 40%; height: 200%;
            background: linear-gradient(to right, transparent, rgba(91,142,230,0.03), transparent);
            transform: skewX(-20deg);
            animation: scanLight 8s ease-in-out infinite;
        }
        @keyframes scanLight {
            0%, 100% { left: -60%; opacity: 0; }
            20%       { opacity: 1; }
            40%       { left: 160%; opacity: 0; }
            41%, 99%  { left: -60%; opacity: 0; }
        }

        /* Coins décoratifs */
        .corner {
            position: absolute;
            width: 12px; height: 12px;
            border-color: rgba(91, 142, 230, 0.25);
            border-style: solid;
        }
        .corner-tl { top: 12px; left: 12px; border-width: 0.5px 0 0 0.5px; }
        .corner-tr { top: 12px; right: 12px; border-width: 0.5px 0.5px 0 0; }
        .corner-bl { bottom: 12px; left: 12px; border-width: 0 0 0.5px 0.5px; }
        .corner-br { bottom: 12px; right: 12px; border-width: 0 0.5px 0.5px 0; }

        /* 6. Header */
        .login-logo {
            display: flex;
            justify-content: center;
            margin-bottom: 1.8rem;
        }
        .login-logo-mark {
            width: 44px; height: 44px;
            border: 0.5px solid rgba(91, 142, 230, 0.35);
            border-radius: 2px;
            position: relative;
            animation: logoFade 1.8s ease forwards;
            opacity: 0;
        }
        .login-logo-mark::before {
            content: '';
            position: absolute;
            width: 14px; height: 0.5px;
            background: rgba(91, 142, 230, 0.6);
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
        }
        .login-logo-mark::after {
            content: '';
            position: absolute;
            width: 0.5px; height: 14px;
            background: rgba(91, 142, 230, 0.6);
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
        }
        @keyframes logoFade { to { opacity: 1; } }

        .login-title {
            font-family: 'Cormorant Garamond', serif;
            font-size: 2.2rem;
            font-weight: 300;
            color: #dce8fa;
            letter-spacing: 0.12em;
            line-height: 1;
            margin-bottom: 0.5rem;
            text-align: center;
            animation: textReveal 1.6s cubic-bezier(0.16, 1, 0.3, 1) 0.2s forwards;
            opacity: 0;
            transform: translateY(12px);
        }
        .login-title span {
            color: #5b8ee6;
            font-weight: 400;
        }

        .login-subtitle {
            font-family: 'Josefin Sans', sans-serif;
            font-size: 0.6rem;
            font-weight: 200;
            color: rgba(91, 142, 230, 0.55);
            letter-spacing: 0.45em;
            text-transform: uppercase;
            text-align: center;
            margin-bottom: 0;
            animation: textReveal 1.6s cubic-bezier(0.16, 1, 0.3, 1) 0.35s forwards;
            opacity: 0;
            transform: translateY(12px);
        }

        @keyframes textReveal {
            to { opacity: 1; transform: translateY(0); }
        }

        /* 7. Séparateur */
        .login-divider {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 2.5rem 0;
            animation: textReveal 1.6s ease 0.5s forwards;
            opacity: 0;
        }
        .divider-line {
            flex: 1; height: 0.5px;
            background: linear-gradient(to right, transparent, rgba(91, 142, 230, 0.2));
        }
        .divider-line-r {
            background: linear-gradient(to left, transparent, rgba(91, 142, 230, 0.2));
        }
        .divider-dot {
            width: 3px; height: 3px;
            border-radius: 50%;
            background: rgba(91, 142, 230, 0.4);
        }

        /* 8. Label input */
        .input-label-custom {
            display: block;
            font-family: 'Josefin Sans', sans-serif;
            font-size: 0.6rem;
            font-weight: 300;
            letter-spacing: 0.35em;
            color: rgba(91, 142, 230, 0.5);
            text-transform: uppercase;
            margin-bottom: 0.7rem;
            animation: textReveal 1.6s ease 0.55s forwards;
            opacity: 0;
        }

        /* 9. Input Streamlit override */
        div[data-baseweb="input"] {
            background: rgba(91, 142, 230, 0.03) !important;
            border: 0.5px solid rgba(91, 142, 230, 0.12) !important;
            border-bottom: 0.5px solid rgba(91, 142, 230, 0.3) !important;
            border-radius: 0 !important;
            transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1) !important;
            animation: textReveal 1.6s ease 0.6s forwards;
            opacity: 0;
        }
        div[data-baseweb="input"]:focus-within {
            background: rgba(91, 142, 230, 0.05) !important;
            border-color: rgba(91, 142, 230, 0.4) !important;
            border-bottom-color: #5b8ee6 !important;
            box-shadow: none !important;
        }
        div[data-baseweb="input"] input {
            color: #dce8fa !important;
            font-family: 'Josefin Sans', sans-serif !important;
            font-size: 1rem !important;
            font-weight: 200 !important;
            letter-spacing: 0.5em !important;
            text-align: center !important;
            padding: 14px 16px !important;
        }
        div[data-baseweb="input"] input::placeholder {
            color: rgba(91, 142, 230, 0.2) !important;
            letter-spacing: 0.3em !important;
            font-size: 0.65rem !important;
        }
        div[data-baseweb="input"] svg { display: none !important; }

        /* 10. Bouton — aligné à droite, largeur auto */
        div[data-testid="stButton"] {
            display: flex !important;
            justify-content: flex-end !important;
            margin-top: 2rem !important;
            animation: textReveal 1.6s ease 0.75s forwards;
            opacity: 0;
        }
        div[data-testid="stButton"] button {
            display: inline-flex !important;
            align-items: center !important;
            gap: 10px !important;
            width: auto !important;
            padding: 11px 20px !important;
            background: transparent !important;
            border: 0.5px solid rgba(91, 142, 230, 0.3) !important;
            border-radius: 0 !important;
            color: #5b8ee6 !important;
            font-family: 'Josefin Sans', sans-serif !important;
            font-size: 0.85rem !important;
            font-weight: 300 !important;
            letter-spacing: 0.2em !important;
            text-transform: uppercase !important;
            transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: none !important;
            position: relative;
            overflow: hidden;
        }
        div[data-testid="stButton"] button::before {
            content: '';
            position: absolute;
            inset: 0;
            background: #5b8ee6;
            transform: translateX(101%);
            transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        }
        div[data-testid="stButton"] button:hover::before {
            transform: translateX(0) !important;
        }
        div[data-testid="stButton"] button:hover {
            color: #03050f !important;
        }
        div[data-testid="stButton"] button p::after {
            content: ' →';
        }

        /* 11. Footer */
        .login-footer {
            text-align: center;
            margin-top: 2.2rem;
            font-family: 'Josefin Sans', sans-serif;
            font-size: 0.55rem;
            letter-spacing: 0.3em;
            color: rgba(91, 142, 230, 0.18);
            text-transform: uppercase;
            animation: textReveal 1.6s ease 0.9s forwards;
            opacity: 0;
        }

        /* 12. Alerte erreur */
        [data-testid="stAlert"] {
            background-color: rgba(180, 50, 50, 0.05) !important;
            border: 0.5px solid rgba(180, 50, 50, 0.2) !important;
            border-radius: 0 !important;
            color: rgba(220, 100, 100, 0.8) !important;
            font-family: 'Josefin Sans', sans-serif !important;
            font-size: 0.65rem !important;
            letter-spacing: 0.25em !important;
            text-transform: uppercase !important;
            margin-top: 1rem !important;
            box-shadow: none !important;
            backdrop-filter: blur(10px);
        }
        </style>
    """, unsafe_allow_html=True)

    # Structure HTML de la carte
    st.markdown("""
        <div class="login-card">
            <div class="corner corner-tl"></div>
            <div class="corner corner-tr"></div>
            <div class="corner corner-bl"></div>
            <div class="corner corner-br"></div>

            <div class="login-logo">
                <div class="login-logo-mark"></div>
            </div>
            <div class="login-title">Garmin <span>Stats</span></div>
            <div class="login-subtitle">Biohacking Central</div>

            <div class="login-divider">
                <div class="divider-line"></div>
                <div class="divider-dot"></div>
                <div class="divider-line divider-line-r"></div>
            </div>

            <div class="input-label-custom">Code d'accès sécurisé</div>
    """, unsafe_allow_html=True)

    entered_code = st.text_input(
        "Code",
        type="password",
        placeholder="• • • • • • • •",
        label_visibility="collapsed"
    )

    if st.button("Déverrouiller"):
        if entered_code == st.secrets.get('ACCESS_CODE', ''):
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("ACCÈS NON AUTORISÉ")

    st.markdown("""
            <div class="login-footer">Système sécurisé · Accès restreint</div>
        </div>
    """, unsafe_allow_html=True)
