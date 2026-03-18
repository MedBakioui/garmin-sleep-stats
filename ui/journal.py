import streamlit as st
import datetime

from journal_manager import JournalManager

def render_journal_tab():
    """Affiche l'onglet Journal de Bord avec un design Premium de Grade Expert."""
    
    if 'journal_manager' not in st.session_state:
        st.session_state['journal_manager'] = JournalManager()
    
    jm = st.session_state['journal_manager']

    # --- CSS JOURNAL EXPERT ---
    st.markdown("""
        <style>
        .expert-card {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .mood-btn {
            font-size: 1.8rem;
            padding: 10px;
            border-radius: 12px;
            transition: all 0.2s;
            cursor: pointer;
            filter: grayscale(0.5);
        }
        .mood-btn:hover {
            filter: grayscale(0);
            transform: scale(1.1);
        }
        .insight-pill {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(168, 85, 247, 0.1));
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 12px 18px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .insight-count {
            background: #3b82f6;
            color: white;
            padding: 2px 8px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📓 Journal de Biohacking")
    st.markdown("Identifiez les patterns invisibles qui dictent la qualité de votre récupération neurologique.")

    # --- TOP ACTIONS ---
    with st.container():
        c_date, c_stats, c_btn = st.columns([1.2, 1.5, 1], gap="medium")
        
        with c_date:
            default_date = datetime.date.today() - datetime.timedelta(days=1)
            selected_date = st.date_input("📅 Nuit du", default_date, key="journal_date_picker")
        
        with c_stats:
            # Petite stat rapide
            all_entries = jm.get_all_entries()
            st.markdown(f"📈 **Total Entrées:** `{len(all_entries)}` | ✨ **Régularité:** `{'Excellente' if len(all_entries) > 10 else 'En début'}`")

    # Données existantes
    entry = jm.get_entry(selected_date)
    current_tags = entry.get("tags", [])
    current_notes = entry.get("notes", "")
    current_mood = entry.get("mood", 3)

    st.markdown("---")

    col_input, col_insights = st.columns([1.8, 1], gap="large")

    with col_input:
        st.markdown('<div class="expert-card">', unsafe_allow_html=True)
        
        # MOOD SECTOR
        st.markdown("#### ⚡ État de Forme (Mood)")
        mood_map = {1: "😫", 2: "🙁", 3: "😐", 4: "🙂", 5: "🤩"}
        new_mood = st.select_slider(
            "Comment vous sentez-vous ?",
            options=[1, 2, 3, 4, 5],
            value=current_mood,
            format_func=lambda x: mood_map[x],
            label_visibility="collapsed"
        )
        
        st.markdown('<div style="height: 25px;"></div>', unsafe_allow_html=True)
        
        # TAGS
        st.markdown("#### 🏷️ Facteurs d'Influence (Tags)")
        available_tags = jm.get_available_tags()
        default_selection = [t for t in current_tags if t in available_tags]
        
        selected_tags = st.multiselect(
            "Qu'est-ce qui a impacté votre nuit ?", 
            available_tags, 
            default=default_selection,
            label_visibility="collapsed"
        )
        # Gestion des tags custom existants
        extra_tags = [t for t in current_tags if t not in available_tags]
        if extra_tags:
            selected_tags.extend(extra_tags)
            st.caption(f"Tags persistants: {', '.join(extra_tags)}")

        st.markdown('<div style="height: 25px;"></div>', unsafe_allow_html=True)

        # NOTES
        st.markdown("#### 📝 Observations Cognitives")
        new_notes = st.text_area(
            "Notes confidentielles", 
            height=180, 
            value=current_notes, 
            placeholder="Ressenti mental, rêves, événements de la journée...",
            label_visibility="collapsed"
        )
        
        st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
        
        if st.button("💾 SYNCHRONISER L'ENTRÉE", type="primary", use_container_width=True):
            jm.save_entry(selected_date, selected_tags, new_notes, mood=new_mood)
            st.success("Données injectées avec succès dans votre profil local.")
            if hasattr(st, "rerun"): st.rerun()
            else: st.experimental_rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

    with col_insights:
        st.markdown('<div class="expert-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Vos Patterns")
        st.write("Fréquence des facteurs relevés dans votre historique.")
        
        tag_stats = jm.get_tag_stats()
        if tag_stats:
            for tag, count in list(tag_stats.items())[:6]:
                st.markdown(f"""
                    <div class="insight-pill">
                        <span>{tag}</span>
                        <span class="insight-count">{count}x</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Utilisez des tags pour voir apparaître vos statistiques ici.")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Preview de la date sélectionnée
        if current_tags or current_notes:
            with st.expander("🔍 Résumé de la sélection", expanded=True):
                st.write(f"**Humeur:** {mood_map.get(current_mood)}")
                if current_tags: st.write(f"**Facteurs:** {', '.join(current_tags)}")
                if current_notes: st.write(f"**Notes:** {current_notes}")
