import streamlit as st

def render_login():
    """Affiche la page de connexion épique et gère l'authentification."""
    
    # --- CSS ULTRA-PREMIUM EXPERT LOGIN ---
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;900&display=swap');
        
        /* 1. Reset Global & Fond Animé Complexe (Mesh Gradient) */
        .stApp {
            background-color: #030014 !important;
            background-image: 
                radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                radial-gradient(at 50% 0%, hsla(225,39%,30%,0.2) 0, transparent 50%), 
                radial-gradient(at 100% 0%, hsla(339,49%,30%,0.2) 0, transparent 50%);
            animation: breathe 10s ease-in-out infinite alternate !important;
        }
        @keyframes breathe {
            form { filter: brightness(0.8); }
            to { filter: brightness(1.2); }
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

        /* 4. Le Glassmorphism Panel (La Carte principale Expert) */
        .login-card {
            background: rgba(10, 10, 25, 0.45);
            backdrop-filter: blur(40px) saturate(250%);
            -webkit-backdrop-filter: blur(40px) saturate(250%);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-top: 1px solid rgba(255, 255, 255, 0.15);
            border-left: 1px solid rgba(255, 255, 255, 0.15);
            padding: 3.5rem 3rem;
            width: 100%;
            max-width: 440px;
            box-shadow: 
                0 30px 60px -10px rgba(0, 0, 0, 0.8),
                0 0 40px -10px rgba(99, 102, 241, 0.15);
            text-align: center;
            animation: slideUpFade 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            opacity: 0;
            transform: translateY(50px) scale(0.97);
            position: relative;
            overflow: hidden;
        }
        
        /* Effet de reflet interne sur la carte */
        .login-card::before {
            content: '';
            position: absolute;
            top: 0; left: -100%; width: 50%; height: 100%;
            background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.03) 50%, rgba(255,255,255,0) 100%);
            transform: skewX(-25deg);
            animation: shine 6s infinite;
        }
        @keyframes shine {
            0% { left: -100%; }
            20% { left: 200%; }
            100% { left: 200%; }
        }

        @keyframes slideUpFade {
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        /* 5. Typographie Titre & Sous-titre "Sci-Fi Clean" */
        .login-title {
            font-family: 'Outfit', sans-serif;
            font-size: 2.5rem;
            font-weight: 900;
            color: #ffffff;
            margin-bottom: 0.2rem;
            letter-spacing: -1.5px;
            line-height: 1.1;
            text-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
        }
        .login-title span {
            background: linear-gradient(to right, #6366f1, #a855f7, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% auto;
            animation: gradientText 5s linear infinite;
        }
        @keyframes gradientText {
            to { background-position: 200% center; }
        }
        
        .login-subtitle {
            font-family: 'Outfit', sans-serif;
            font-size: 0.85rem;
            color: #bbc1ce;
            text-transform: uppercase;
            letter-spacing: 4px;
            margin-bottom: 3rem;
            font-weight: 600;
            opacity: 0.8;
        }

        /* 6. Le Champ de Texte (Input) - Minimaliste et Focalisé */
        div[data-baseweb="input"] {
            background: rgba(0, 0, 0, 0.4) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px !important;
            padding: 6px 10px !important;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        div[data-baseweb="input"]:focus-within {
            background: rgba(10, 15, 30, 0.9) !important;
            border-color: rgba(168, 85, 247, 0.5) !important;
            box-shadow: 
                0 0 0 2px rgba(168, 85, 247, 0.2),
                inset 0 0 15px rgba(168, 85, 247, 0.1) !important;
            transform: translateY(-2px);
        }
        div[data-baseweb="input"] input {
            color: #ffffff !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 1.3rem !important;
            letter-spacing: 8px !important;
            text-align: center !important;
            font-weight: 700 !important;
            padding: 12px !important;
        }
        div[data-baseweb="input"] input::placeholder {
            color: #475569 !important;
            letter-spacing: 2px !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
        }
        div[data-baseweb="input"] svg { display: none !important; }

        /* 7. Le Bouton d'Action - Ultra Premium */
        div[data-testid="stButton"] button {
            background: linear-gradient(115deg, #4f46e5, #9333ea, #db2777) !important;
            background-size: 200% auto !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            padding: 1.2rem !important;
            border-radius: 12px !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 800 !important;
            font-size: 1.05rem !important;
            letter-spacing: 2.5px !important;
            text-transform: uppercase !important;
            width: 100% !important;
            margin-top: 1.5rem !important;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: 
                0 15px 30px -10px rgba(147, 51, 234, 0.6),
                inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
            position: relative;
            overflow: hidden;
        }
        div[data-testid="stButton"] button:hover {
            background-position: right center !important;
            transform: translateY(-4px) !important;
            box-shadow: 
                0 20px 40px -10px rgba(147, 51, 234, 0.8),
                inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
            letter-spacing: 3px !important;
        }
        div[data-testid="stButton"] button:active {
            transform: translateY(1px) !important;
            box-shadow: 0 5px 15px -5px rgba(147, 51, 234, 0.5) !important;
        }
        
        /* 8. Messages d'Erreur Override */
        [data-testid="stAlert"] {
            background-color: rgba(220, 38, 38, 0.05) !important;
            border: 1px solid rgba(220, 38, 38, 0.2) !important;
            color: #f7aaaa !important;
            backdrop-filter: blur(10px);
            border-radius: 12px !important;
            font-family: 'Outfit', sans-serif !important;
            margin-top: 1.5rem !important;
            box-shadow: 0 4px 15px rgba(220, 38, 38, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # --- HTML STRUCTURE POUR LE DESIGN ---
    # On encapsule la carte visuelle. 
    # Streamlit injectera le composant input et button juste en dessous dans le conteneur principal flex.
    st.markdown("""
        <div class="login-card">
            <div class="login-title">Garmin <span>Stats</span></div>
            <div class="login-subtitle">Biohacking Central</div>
    """, unsafe_allow_html=True)
    
    # --- LOGIQUE INTERACTIVE ---
    entered_code = st.text_input("Code", type="password", placeholder="CODE SECURISÉ", label_visibility="collapsed")
    
    if st.button("INITIALISER LA SESSION", type="primary", use_container_width=True):
        if entered_code == st.secrets.get('ACCESS_CODE', ''):
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("ACCÈS NON AUTORISÉ")
            
    # Fermeture de la div ouverte plus haut
    st.markdown("</div>", unsafe_allow_html=True)
