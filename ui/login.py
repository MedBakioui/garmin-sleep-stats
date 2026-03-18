import streamlit as st

def render_login():
    """Affiche la page de connexion épique et gère l'authentification."""
    
    # --- CSS EPIC & PRO LOGIN ---
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;900&display=swap');
        
        /* 1. Reset Global & Fond Animé */
        .stApp {
            background: linear-gradient(-45deg, #0f172a, #1e1b4b, #020617, #171717) !important;
            background-size: 400% 400% !important;
            animation: gradientBG 15s ease infinite !important;
        }
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
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
        }

        /* 4. Le Glassmorphism Panel (La Carte principale) */
        .login-card {
            background: rgba(15, 23, 42, 0.4);
            backdrop-filter: blur(30px) saturate(200%);
            -webkit-backdrop-filter: blur(30px) saturate(200%);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 3rem 2.5rem;
            width: 100%;
            max-width: 420px;
            box-shadow: 
                0 25px 50px -12px rgba(0, 0, 0, 0.7),
                0 0 0 1px rgba(255,255,255,0.05) inset;
            text-align: center;
            animation: slideUpFade 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            opacity: 0;
            transform: translateY(40px);
        }
        @keyframes slideUpFade {
            to { opacity: 1; transform: translateY(0); }
        }

        /* 5. Typographie Titre & Sous-titre */
        .login-title {
            font-family: 'Outfit', sans-serif;
            font-size: 2.2rem;
            font-weight: 900;
            color: #ffffff;
            margin-bottom: 0.2rem;
            letter-spacing: -1px;
            line-height: 1.1;
            text-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }
        .login-title span {
            background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .login-subtitle {
            font-family: 'Outfit', sans-serif;
            font-size: 0.9rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 2.5rem;
            font-weight: 500;
        }

        /* 6. Le Champ de Texte (Input) */
        div[data-baseweb="input"] {
            background: rgba(0, 0, 0, 0.3) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            padding: 4px 8px !important;
            transition: all 0.3s ease !important;
        }
        div[data-baseweb="input"]:focus-within {
            background: rgba(15, 23, 42, 0.8) !important;
            border-color: #a855f7 !important;
            box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.2) !important;
            transform: translateY(-2px);
        }
        div[data-baseweb="input"] input {
            color: #ffffff !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 1.1rem !important;
            letter-spacing: 4px !important; /* Pour les points du mdp */
            text-align: center !important;
            font-weight: 500 !important;
            padding: 12px !important;
        }
        div[data-baseweb="input"] input::placeholder {
            color: #475569 !important;
            letter-spacing: 1px !important;
            font-size: 0.9rem !important;
        }
        /* Icône oeil optionnelle cachée pour l'élégance pure */
        div[data-baseweb="input"] svg { display: none !important; }

        /* 7. Le Bouton d'Action */
        div[data-testid="stButton"] button {
            background: linear-gradient(135deg, #4f46e5 0%, #c026d3 100%) !important;
            color: white !important;
            border: none !important;
            padding: 1rem !important;
            border-radius: 12px !important;
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            letter-spacing: 1.5px !important;
            text-transform: uppercase !important;
            width: 100% !important;
            margin-top: 1rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 10px 20px -10px rgba(192, 38, 211, 0.5) !important;
        }
        div[data-testid="stButton"] button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 15px 25px -10px rgba(192, 38, 211, 0.8) !important;
            filter: brightness(1.1);
        }
        div[data-testid="stButton"] button:active {
            transform: translateY(1px) !important;
        }
        
        /* 8. Messages d'Erreur Override */
        [data-testid="stAlert"] {
            background-color: rgba(220, 38, 38, 0.1) !important;
            border: 1px solid rgba(220, 38, 38, 0.3) !important;
            color: #fca5a5 !important;
            border-radius: 10px !important;
            font-family: 'Outfit', sans-serif !important;
            margin-top: 1rem !important;
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
