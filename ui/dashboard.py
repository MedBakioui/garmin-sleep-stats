
import streamlit as st
import datetime
import pandas as pd
from utils import load_settings
from visualizations import (
    plot_sleep_structure, plot_deep_sleep_ratio, plot_distribution, 
    plot_heatmap, plot_weekend_comparison, plot_timeline,
    plot_sleep_efficiency, plot_awake_trend,
    plot_sleep_debt, plot_rem_deep_ratio, plot_bedtime_correlation,
    plot_bedtime_distribution, plot_rolling_average, plot_global_phase_breakdown,
    plot_activity_interactions,
    plot_wakeup_time_distribution, plot_deep_sleep_distribution, 
    plot_rem_sleep_distribution, plot_sleep_score_distribution, 
    plot_stress_score_distribution, plot_weekday_sleep_boxplot, 
    plot_score_by_weekday_violin, plot_correlation_heatmap,
    plot_weekday_distribution, plot_trading_readiness
)

def render_dashboard_tab(get_data_manager_func):
    """Affiche l'onglet Statistiques avec un design Premium."""
    dm = get_data_manager_func()

    if not dm:
        st.info("👋 Bienvenue ! Veuillez vous connecter dans l'onglet **⚙️ Réglages** pour commencer.")
        return

    # --- CSS DASHBOARD ---
    st.markdown("""
        <style>
        .stat-card {
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }
        .stat-value {
            font-size: 2.2rem;
            font-weight: 800;
            color: #f8fafc;
            line-height: 1;
        }
        .stat-label {
            font-size: 0.8rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 8px;
        }
        .control-panel {
            background: rgba(15, 23, 42, 0.2);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 25px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Auto-Sync au démarrage ---
    if 'last_sync_time' not in st.session_state:
        try:
            today = datetime.date.today()
            dm.get_sleep_data(today - datetime.timedelta(days=7), today, force_recent_days=0)
            st.session_state['last_sync_time'] = datetime.datetime.now()
        except Exception as e:
            st.error(f"Erreur de synchro auto : {e}")

    # Initialisation dates
    today = datetime.date.today()
    if 'date_start_val' not in st.session_state:
        st.session_state['date_start_val'] = today - datetime.timedelta(days=29)
    if 'date_end_val' not in st.session_state:
        st.session_state['date_end_val'] = today
    
    # --- HEADER & CONTROLS ---
    st.title("📊 Sleep Insights")
    
    with st.container():
        st.markdown('<div class="control-panel">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2, 2, 1], gap="medium")
        
        with c1:
            st.markdown("##### 📅 Fenêtre Temporelle")
            # Raccourcis
            rq_cols = st.columns(3)
            if rq_cols[0].button("7J", use_container_width=True):
                st.session_state['date_start_val'] = today - datetime.timedelta(days=6)
                if hasattr(st, "rerun"): st.rerun()
                else: st.experimental_rerun()
            if rq_cols[1].button("30J", use_container_width=True):
                st.session_state['date_start_val'] = today - datetime.timedelta(days=29)
                if hasattr(st, "rerun"): st.rerun()
                else: st.experimental_rerun()
            if rq_cols[2].button("All", use_container_width=True):
                st.session_state['date_start_val'] = datetime.date(2023, 1, 1)
                if hasattr(st, "rerun"): st.rerun()
                else: st.experimental_rerun()
            
            # Calendriers
            d_col1, d_col2 = st.columns(2)
            start_date = d_col1.date_input("Du", st.session_state['date_start_val'], label_visibility="collapsed")
            end_date = d_col2.date_input("Au", st.session_state['date_end_val'], label_visibility="collapsed")
            st.session_state['date_start_val'] = start_date
            st.session_state['date_end_val'] = end_date

        with c2:
            st.markdown("##### ⚡ Actions")
            st.write("") # Spacer
            start_loading = st.button("📊 CALCULER LES STATISTIQUES", type="primary", use_container_width=True)
            force_sync = st.button("🔄 FORCER SYNCHRO GARMIN", type="secondary", use_container_width=True)
            
        with c3:
            st.markdown("##### 📥 Export")
            st.write("")
            download_placeholder = st.empty()
            
        st.markdown('</div>', unsafe_allow_html=True)

    # --- DATAFRAME LOADING ---
    if start_loading or force_sync or st.session_state.get('stats_loaded', False):
        st.session_state['stats_loaded'] = True
        with st.spinner("Analyse du flux de données..."):
            try:
                days_to_force = 3 if force_sync else 0
                df = dm.get_dataframe(start_date, end_date, force_recent_days=days_to_force)

                if not df.empty:
                    # Conversion et Nettoyage
                    df['date'] = pd.to_datetime(df['date'])
                    if 'sleep_score' in df.columns:
                        df['sleep_score'] = pd.to_numeric(df['sleep_score'], errors='coerce')
                    if 'total_sleep_hours' in df.columns:
                        df['total_sleep_hours'] = pd.to_numeric(df['total_sleep_hours'], errors='coerce')

                    # Filtrage par dates
                    mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
                    df = df.loc[mask].sort_values('date')

                    if df.empty:
                        st.warning("Aucune donnée sur cette période.")
                        return

                    # --- KEY METRICS DÉSIGN ---
                    # Calcul sécurisé des moyennes (ignore NaN)
                    avg_hours = df['total_sleep_hours'].mean() if 'total_sleep_hours' in df.columns else None
                    avg_score = df['sleep_score'].mean() if 'sleep_score' in df.columns else None
                    
                    m_col1, m_col2, m_col3 = st.columns(3)
                    
                    with m_col1:
                        if pd.notnull(avg_hours):
                            h, m = divmod(int(avg_hours * 60), 60)
                            val_str = f"{h}h {m:02d}m"
                        else:
                            val_str = "--"
                        st.markdown(f'<div class="stat-card"><div class="stat-value">{val_str}</div><div class="stat-label">Volume Moyen</div></div>', unsafe_allow_html=True)
                    
                    with m_col2:
                        val_score = f"{int(avg_score)}" if pd.notnull(avg_score) else "--"
                        st.markdown(f'<div class="stat-card"><div class="stat-value">{val_score}</div><div class="stat-label">Score Sommeil</div></div>', unsafe_allow_html=True)
                    
                    with m_col3:
                        st.markdown(f'<div class="stat-card"><div class="stat-value">{len(df)}</div><div class="stat-label">Nuits Analysées</div></div>', unsafe_allow_html=True)
                    
                    # CSV Download
                    csv = df.to_csv(index=False).encode('utf-8')
                    with download_placeholder:
                        st.download_button("EXPORTER CSV", csv, "sleep_data_export.csv", "text/csv", use_container_width=True)

                    st.markdown("---")

                    # --- VISUALIZATION SELECTOR ---
                    st.subheader("🔭 Exploration Visuelle")
                    
                    categories = {
                        "🧬 STRUCTURE & PHASES": {
                            "Proportions des Cycles": plot_sleep_structure,
                            "Ratio Sommeil Profond": plot_deep_sleep_ratio,
                            "Efficacité Globale": plot_sleep_efficiency,
                            "Analyse de l'Agitation": plot_awake_trend
                        },
                        "📈 TENDANCES & ANALYSES": {
                            "Rythme Circadien (Coucher)": plot_bedtime_distribution,
                            "Rythme Circadien (Réveil)": plot_wakeup_time_distribution,
                            "Variabilité Hebdomadaire": plot_weekday_distribution,
                            "Heatmap d'Habitudes": plot_heatmap
                        },
                        "🧠 PERFORMANCE": {
                            "Readiness & Streaks": plot_trading_readiness,
                            "Sommeil vs Stress": plot_activity_interactions 
                        }
                    }
                    
                    cat_nav, graph_nav = st.columns([1, 2])
                    selected_cat = cat_nav.selectbox("Thème d'analyse", list(categories.keys()))
                    selected_graph = graph_nav.radio("Graphique spécifique", list(categories[selected_cat].keys()), horizontal=True)
                    
                    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
                    
                    # Rendu du graphique
                    try:
                        active_targets = load_settings()
                        categories[selected_cat][selected_graph](df, targets=active_targets)
                    except Exception as ve:
                        st.error(f"Erreur lors du rendu du graphique : {ve}")

                else:
                    st.warning("Impossible de récupérer les données.")
            except Exception as e:
                st.error(f"Erreur d'analyse : {e}")
                st.exception(e)
