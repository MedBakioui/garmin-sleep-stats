
import streamlit as st
import pandas as pd
import datetime
import time
from utils import load_settings, save_settings
from data_manager import DataManager

def render_goals_tab(get_data_manager_func):
    """Affiche l'onglet Objectifs avec un design Premium & Analytique."""
    
    # --- CSS SPECIFIQUE POUR LES CARTES D'OBJECTIFS ---
    st.markdown("""
        <style>
        .goal-card {
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            transition: all 0.3s ease;
            height: 100%;
        }
        .goal-card:hover {
            transform: translateY(-5px);
            border-color: #6366f1;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }
        .goal-icon {
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        .goal-title {
            font-weight: 700;
            font-size: 1.1rem;
            color: #f8fafc;
            margin-bottom: 0.5rem;
        }
        .goal-desc {
            color: #94a3b8;
            font-size: 0.85rem;
            margin-bottom: 1.5rem;
        }
        .streak-badge {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 800;
            display: inline-block;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🎯 Architecture de Sommeil")
    st.markdown("<p style='color: #64748b; margin-top: -1rem;'>Définissez vos standards de récupération pour une performance cognitive optimale.</p>", unsafe_allow_html=True)
    
    current_settings = load_settings()
    
    # --- SECTION RÉGLAGES (CARTES) ---
    st.write("")
    col_t1, col_t2, col_t3 = st.columns(3, gap="medium")
    
    with col_t1:
        st.markdown("""
            <div class="goal-card">
                <div class="goal-icon">⏱️</div>
                <div class="goal-title">Volume Cible</div>
                <div class="goal-desc">La durée totale nécessaire pour une restauration physique complète.</div>
            </div>
        """, unsafe_allow_html=True)
        new_dur = st.number_input("Volume (Heures)", 4.0, 12.0, float(current_settings.get("target_duration", 8.0)), 0.5, key="set_dur", label_visibility="collapsed")
        st.caption("Recommandé : 7.5 - 9.0h")

    with col_t2:
        st.markdown("""
            <div class="goal-card">
                <div class="goal-icon">🧠</div>
                <div class="goal-title">Phase Profonde</div>
                <div class="goal-desc">Le pourcentage de sommeil profond requis pour la consolidation mémoire.</div>
            </div>
        """, unsafe_allow_html=True)
        new_deep = st.number_input("Profondeur (%)", 5, 60, int(current_settings.get("target_deep_pct", 20)), 1, key="set_deep", label_visibility="collapsed")
        st.caption("Cible idéale : 18 - 25%")
        
    with col_t3:
        st.markdown("""
            <div class="goal-card">
                <div class="goal-icon">🌙</div>
                <div class="goal-title">Régularité</div>
                <div class="goal-desc">L'heure limite de coucher pour respecter vos cycles circadiens.</div>
            </div>
        """, unsafe_allow_html=True)
        try:
            def_time = datetime.datetime.strptime(current_settings.get("target_bedtime", "23:00"), "%H:%M").time()
        except:
             def_time = datetime.time(23,0)
        new_bed = st.time_input("Heure Coucher", def_time, key="set_bed", label_visibility="collapsed")
        st.caption("Régularité ± 15 min")

    st.write("")
    c_save, _ = st.columns([1, 2])
    with c_save:
        if st.button("🔧 APPLIQUER LA CONFIGURATION", type="primary", use_container_width=True):
            save_settings({
                "target_duration": new_dur,
                "target_deep_pct": new_deep,
                "target_bedtime": new_bed.strftime("%H:%M")
            })
            st.toast("Standards mis à jour", icon="✅")
            time.sleep(0.5)
            st.rerun()

    st.markdown("---")

    # --- ANALYTICS ENGINE (Helper Functions) ---
    def compute_compliance(df, t_dur, t_deep):
        if df.empty: return None
        avg_dur = df['total_sleep_hours'].mean()
        pct_ok_dur = (df['total_sleep_hours'] >= t_dur - 0.1).mean() * 100
        
        avg_deep = 0
        pct_ok_deep = 0
        if 'deep_sleep_hours' in df.columns:
            ratios = (df['deep_sleep_hours'] / df['total_sleep_hours']) * 100
            avg_deep = ratios.mean()
            pct_ok_deep = (ratios >= t_deep - 2).mean() * 100 # Tolerance 2%
            
        return {
            "avg_dur": avg_dur, "success_dur": pct_ok_dur,
            "avg_deep": avg_deep, "success_deep": pct_ok_deep,
            "count": len(df)
        }

    def get_streaks(df, col, target, tolerance=0.1):
        if df.empty: return 0, 0
        df_sorted = df.sort_values('date', ascending=False)
        current = 0
        for val in df_sorted[col]:
            if pd.notnull(val) and val >= target - tolerance: current += 1
            else: break
            
        best = 0; temp = 0
        for val in df.sort_values('date')[col]:
            if pd.notnull(val) and val >= target - tolerance: temp += 1
            else: best = max(best, temp); temp = 0
        return current, max(best, temp)

    # --- SECTION SUIVI ---
    st.header("📈 Dashboard de Conformité")
    
    dm_obj = get_data_manager_func()
    if dm_obj and 'garmin_client' in st.session_state:
        end_p = datetime.date.today()
        start_p = end_p - datetime.timedelta(days=30)
        
        try:
            df_full = dm_obj.get_dataframe(start_p, end_p, force_recent_days=0)
            if df_full.empty:
                st.info("Données en cours de synchronisation...")
                return

            df_full['date'] = pd.to_datetime(df_full['date'])
            df_30 = df_full.sort_values('date')
            df_7 = df_30[df_30['date'] >= pd.Timestamp(end_p) - pd.Timedelta(days=6)]
            df_work = df_7[df_7['date'].dt.dayofweek < 5]

            res_30 = compute_compliance(df_30, new_dur, new_deep)
            res_7 = compute_compliance(df_7, new_dur, new_deep)
            res_work = compute_compliance(df_work, new_dur, new_deep)

            # AFFICHAGE KPI
            cols = st.columns(3)
            titles = ["🏢 Semaine Pro", "📅 7 Derniers Jours", "🗓️ 30 Derniers Jours"]
            data_sets = [res_work, res_7, res_30]

            for col, title, res in zip(cols, titles, data_sets):
                with col:
                    st.markdown(f"<div style='background: rgba(15, 23, 42, 0.3); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05)'><b>{title}</b>", unsafe_allow_html=True)
                    if res:
                        h, m = divmod(int(res['avg_dur'] * 60), 60)
                        diff = res['avg_dur'] - new_dur
                        st.metric("Durée Moyenne", f"{h}h {m:02d}", f"{diff:+.1f}h", delta_color="normal" if diff >= -0.2 else "inverse")
                        st.progress(int(res['success_dur']), f"Discipline Durée : {int(res['success_dur'])}%")
                        
                        st.write("")
                        diff_deep = res['avg_deep'] - new_deep
                        st.metric("Sommeil Profond", f"{res['avg_deep']:.1f}%", f"{diff_deep:+.1f}%", delta_color="normal" if diff_deep >= -2 else "inverse")
                        st.progress(int(res['success_deep']), f"Discipline Profond : {int(res['success_deep'])}%")
                    else:
                        st.caption("Données insuffisantes")
                    st.markdown("</div>", unsafe_allow_html=True)

            # SÉRIES
            st.markdown("---")
            c1, c2 = st.columns(2)
            
            cur_s, best_s = get_streaks(df_30, 'total_sleep_hours', new_dur)
            with c1:
                st.subheader("🔥 Série de Durée")
                st.markdown(f"<div style='font-size: 2.5rem; font-weight: 800; color: #f59e0b;'>{cur_s} <span style='font-size: 1rem; color: #94a3b8;'>jours consécutifs</span></div>", unsafe_allow_html=True)
                st.caption(f"Record historique : {best_s} jours")

            if 'deep_ratio_val' not in df_30.columns:
                df_30['deep_ratio_val'] = (df_30['deep_sleep_hours'] / df_30['total_sleep_hours']) * 100
            
            cur_d, best_d = get_streaks(df_30, 'deep_ratio_val', new_deep, tolerance=2)
            with c2:
                st.subheader("⚡ Série de Profondeur")
                st.markdown(f"<div style='font-size: 2.5rem; font-weight: 800; color: #6366f1;'>{cur_d} <span style='font-size: 1rem; color: #94a3b8;'>jours consécutifs</span></div>", unsafe_allow_html=True)
                st.caption(f"Record historique : {best_d} jours")

            # CONSTANCE GRID
            st.markdown("---")
            st.subheader("🗓️ Matrice de Constance (15 derniers jours)")
            last_15 = df_30.tail(15)
            
            def render_mini_grid(df, col, target, label):
                st.caption(label)
                grid_html = '<div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px;">'
                for _, row in df.iterrows():
                    val = row[col]
                    date_s = row['date'].strftime('%d %b')
                    is_ok = pd.notnull(val) and val >= target * 0.95 # Petite marge
                    color = "#22c55e" if is_ok else "#ef4444"
                    if pd.isnull(val): color = "#334155"
                    
                    grid_html += f'<div title="{date_s}: {val if pd.notnull(val) else "N/A"}" style="width: 32px; height: 32px; background: {color}; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold; color: rgba(255,255,255,0.5)">{row["date"].day}</div>'
                grid_html += '</div>'
                st.markdown(grid_html, unsafe_allow_html=True)

            cg1, cg2 = st.columns(2)
            with cg1: render_mini_grid(last_15, 'total_sleep_hours', new_dur, "Discipline Temps")
            with cg2: render_mini_grid(last_15, 'deep_ratio_val', new_deep, "Discipline Profondeur")

        except Exception as e:
            st.error(f"Analyse indisponible : {e}")
            
    else:
        st.warning("👉 Connectez-vous dans l'onglet **⚙️ Réglages** pour activer le suivi de performance.")
