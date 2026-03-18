import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

def has_valid_data(df, columns):
    """Vérifie si les colonnes existent et ne sont pas toutes vides."""
    if df.empty: return False
    for c in columns:
        if c not in df.columns or df[c].isna().all():
            return False
    return True

# --- CONFIGURATION DU THÈME PREMIUM ---
THEME_COLORS = {
    "background": "rgba(0,0,0,0)",
    "text": "#cbd5e1", # Slate 300
    "grid": "#334155", # Slate 700
    "primary": "#3b82f6", # Blue 500
    "secondary": "#a855f7", # Purple 500
    "success": "#10b981", # Emerald 500
    "warning": "#f59e0b", # Amber 500
    "danger": "#ef4444", # Red 500
    "info": "#0ea5e9"    # Sky 500
}

def update_premium_layout(fig, title=None):
    """Applique le style Deep Night à une figure Plotly."""
    fig.update_layout(
        paper_bgcolor=THEME_COLORS["background"],
        plot_bgcolor=THEME_COLORS["background"],
        font_color=THEME_COLORS["text"],
        title_font_size=18,
        title_x=0,  # Align title left
        margin=dict(l=40, r=40, t=60, b=40),
        hoverlabel=dict(
            bgcolor="#1e293b",
            font_size=14,
            font_family="Inter"
        ),
        xaxis=dict(
            showgrid=False, 
            zeroline=False,
            showline=True, 
            linecolor=THEME_COLORS["grid"]
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor="rgba(51, 65, 85, 0.4)", # Subtle grid
            zeroline=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_layout(title_text=title if title else "")
        
    return fig

# --- FONCTIONS DE VISUALISATION ---

def plot_sleep_structure(df, targets=None):
    phases = ['deep_sleep_hours', 'light_sleep_hours', 'rem_sleep_hours', 'awake_sleep_hours']
    # On affiche si au moins une phase est dispo
    if df.empty or not any(c in df.columns for c in phases): return

    st.subheader("Structure des Nuits")
    present_cols = [c for c in phases if c in df.columns]
    
    target_val = targets.get('target_duration', 8.0) if targets else 8.0
    
    labels_map = {
        'deep_sleep_hours': 'Profond',
        'light_sleep_hours': 'Léger',
        'rem_sleep_hours': 'Paradoxal (REM)',
        'awake_sleep_hours': 'Éveillé',
        'date': 'Date',
        'value': 'Durée (h)',
        'variable': 'Type'
    }
    
    fig = px.bar(
        df, 
        x='date', 
        y=present_cols,
        labels=labels_map,
        color_discrete_map={
                'deep_sleep_hours': THEME_COLORS['primary'],
                'light_sleep_hours': THEME_COLORS['secondary'],
                'rem_sleep_hours': '#f43f5e', # Rose
                'awake_sleep_hours': THEME_COLORS['warning']
        }
    )
    # Clean Names
    new_names = labels_map
    fig.for_each_trace(lambda t: t.update(name=new_names.get(t.name, t.name)))
    
    fig.update_traces(hovertemplate='<b>%{x}</b><br>%{data.name}: %{y:.1f} h')

    # Objectif & Moyenne
    avg_hours = df['total_sleep_hours'].mean()
    fig.add_hline(y=avg_hours, line_dash="dot", line_color="rgba(255,255,255,0.5)", annotation_text=f"Moy: {avg_hours:.1f}h")
    fig.add_hline(y=target_val, line_dash="dash", line_color=THEME_COLORS['success'], annotation_text=f"Obj: {target_val}h")
    
    update_premium_layout(fig)
    st.plotly_chart(fig, width="stretch", key="chart_structure")
    st.caption("ℹ️ Un cycle de sommeil sain alterne entre sommeil léger, profond (récupération physique) et REM (mental).")

def plot_deep_sleep_ratio(df, targets=None):
    if not has_valid_data(df, ['deep_sleep_hours', 'total_sleep_hours']): return

    st.subheader("Qualité Profonde")
    target_val = targets.get('target_deep_pct', 20) if targets else 20
    
    df['deep_ratio'] = (df['deep_sleep_hours'] / df['total_sleep_hours']) * 100
    
    fig = px.area(df, x='date', y='deep_ratio', markers=True, 
                        labels={'deep_ratio': '% Profond', 'date': 'Date'})
    
    fig.update_traces(
        line_color=THEME_COLORS['success'], 
        fillcolor="rgba(16, 185, 129, 0.1)",
        hovertemplate='<b>%{x}</b><br>Profond: %{y:.1f}%'
    )
    
    fig.add_hline(y=target_val, line_dash="dash", line_color="white", annotation_text=f"Objectif {target_val}%")
    
    update_premium_layout(fig)
    fig.update_layout(yaxis_title="% Sommeil Profond")
    st.plotly_chart(fig, width="stretch", key="chart_deep")
    st.caption("ℹ️ Le sommeil profond est essentiel pour la régénération cellulaire et immunitaire.")

def plot_distribution(df, targets=None):
    if not has_valid_data(df, ['total_sleep_hours']): return

    st.subheader("Distribution des Durées")
    fig = px.histogram(df, x="total_sleep_hours", nbins=15, 
                            color_discrete_sequence=[THEME_COLORS['info']],
                            labels={'total_sleep_hours': 'Durée (h)'})
    
    val = 8.0
    if targets and 'target_duration' in targets:
        try: val = float(targets['target_duration'])
        except: pass
    
    fig.add_vline(x=val, line_color=THEME_COLORS['success'], line_dash="dash", annotation_text=f"Obj: {val}h")

    fig.update_traces(
        marker_line_width=1, marker_line_color="#1e293b",
        hovertemplate='<b>%{x} h</b><br>Nuits: %{y}<extra></extra>'
    )
    fig.update_layout(bargap=0.1)
    
    update_premium_layout(fig)
    fig.update_layout(
        xaxis_title="Heures de Sommeil", 
        yaxis_title="Nombre de Nuits", 
        showlegend=False,
        title_text="" # Fix 'undefined'
    )
    st.plotly_chart(fig, width="stretch", key="chart_dist")
    st.caption("ℹ️ Visualisez la régularité de vos nuits. Une courbe resserrée indique une bonne routine.")

def plot_heatmap(df, targets=None):
    if not has_valid_data(df, ['total_sleep_hours', 'date']): return

    st.subheader("Calendrier d'Endurance")
    df_heat = df.copy()
    df_heat['Semaine'] = df_heat['date'].dt.isocalendar().week
    df_heat['Jour_Index'] = df_heat['date'].dt.dayofweek
    
    heatmap_data = df_heat.pivot_table(index='Jour_Index', columns='Semaine', values='total_sleep_hours', aggfunc='mean')
    
    if heatmap_data.empty: return

    days_map = {0: 'Lun', 1: 'Mar', 2: 'Mer', 3: 'Jeu', 4: 'Ven', 5: 'Sam', 6: 'Dim'}
    heatmap_data = heatmap_data.reindex(range(7)).rename(index=days_map)
    
    fig = px.imshow(heatmap_data, 
                            labels=dict(x="Semaine", y="Jour", color="Heures"), 
                            color_continuous_scale='Teal', text_auto='.1f', aspect="auto")
    
    fig.update_yaxes(autorange="reversed")
    update_premium_layout(fig)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    
    st.plotly_chart(fig, width="stretch", key="chart_heat")
    st.caption("ℹ️ Vue globale de votre année. Les cases claires indiquent des nuits courtes.")

def plot_weekend_comparison(df, targets=None):
    if not has_valid_data(df, ['total_sleep_hours', 'date']): return

    st.subheader("Semaine vs Week-end")
    df['type_jour'] = df['date'].dt.dayofweek.apply(lambda x: 'Week-end' if x >= 5 else 'Semaine')
    
    fig = px.box(df, x="type_jour", y="total_sleep_hours", color="type_jour", points="all", 
                              color_discrete_map={'Semaine': THEME_COLORS['primary'], 'Week-end': THEME_COLORS['warning']},
                              labels={'total_sleep_hours': 'Durée (h)', 'type_jour': ''})
                              
    if targets:
            val = targets.get('target_duration', 8.0)
            fig.add_hline(y=val, line_color=THEME_COLORS['success'], line_dash="dash")

    update_premium_layout(fig)
    st.plotly_chart(fig, width="stretch", key="chart_week")
    st.caption("ℹ️ Le \"Jetlag Social\" se voit ici si le Week-end est nettement plus élevé.")

def plot_timeline(df, targets=None):
    if not has_valid_data(df, ['start_time', 'end_time']): return

    st.subheader("Chronologie Coucher/Lever")
    df_reg = df.dropna(subset=['start_time', 'end_time'])
    if df_reg.empty: return

    fig = px.timeline(df_reg, x_start="start_time", x_end="end_time", y="date", 
                                color="total_sleep_hours", 
                                color_continuous_scale='PuBu', # Purple-Blue
                                labels={'total_sleep_hours': 'Durée'})
    
    fig.update_yaxes(autorange="reversed")
    update_premium_layout(fig)
    st.plotly_chart(fig, width="stretch", key="chart_time")
    st.caption("ℹ️ Un coucher régulier (même heure) favorise l'endormissement rapide.")

def plot_sleep_efficiency(df, targets=None):
    if not has_valid_data(df, ['total_sleep_hours', 'awake_sleep_hours']): return

    st.subheader("Efficacité (%)")
    df['efficiency'] = (df['total_sleep_hours'] / (df['total_sleep_hours'] + df['awake_sleep_hours'])) * 100
    
    fig = px.line(df, x='date', y='efficiency', markers=True)
    fig.update_traces(line_color=THEME_COLORS['info'], line_shape='spline')
    
    fig.add_hline(y=85, line_dash="dot", line_color=THEME_COLORS['success'], annotation_text="Cible > 85%")
    
    update_premium_layout(fig)
    fig.update_layout(yaxis_title="Efficacité (%)")
    st.plotly_chart(fig, width="stretch", key="chart_eff")
    st.caption("ℹ️ L'efficacité est le temps dormi divisé par le temps passé au lit. Visez > 85%.")

def plot_awake_trend(df, targets=None):
    if not has_valid_data(df, ['awake_sleep_hours']): return

    st.subheader("Temps Éveillé (Agitation)")
    fig = px.bar(df, x='date', y='awake_sleep_hours', 
                        color_discrete_sequence=[THEME_COLORS['warning']])
    
    update_premium_layout(fig)
    fig.update_layout(yaxis_title="Heures")
    st.plotly_chart(fig, width="stretch", key="chart_awake")
    st.caption("ℹ️ Les réveils nocturnes sont normaux, mais s'ils dépassent 1h au total, cela peut indiquer un trouble.")



def plot_sleep_debt(df, targets=None):
    if not has_valid_data(df, ['total_sleep_hours']): return

    target_val = targets.get('target_duration', 8.0) if targets else 8.0
    st.subheader(f"Dette Cumulée (vs {target_val}h)")
    
    df_debt = df.copy()
    df_debt['daily_diff'] = df_debt['total_sleep_hours'] - target_val
    df_debt['cumulative_debt'] = df_debt['daily_diff'].cumsum()
    
    # Color conditional?
    fig = px.area(df_debt, x='date', y='cumulative_debt')
    fig.update_traces(line_color=THEME_COLORS['danger'] if df_debt['cumulative_debt'].iloc[-1] < 0 else THEME_COLORS['success'])
    
    fig.add_hline(y=0, line_color="white", line_width=1)
    update_premium_layout(fig)
    fig.update_layout(yaxis_title="Heures Cumulées")
    st.plotly_chart(fig, width="stretch", key="chart_debt")
    st.caption("ℹ️ Une dette importante augmente les risques cardiovasculaires et le stress.")

def plot_rem_deep_ratio(df, targets=None):
    if not has_valid_data(df, ['deep_sleep_hours', 'rem_sleep_hours']): return

    st.subheader("Physique (Profond) vs Mental (REM)")
    df_melt = df.melt(id_vars=['date'], value_vars=['deep_sleep_hours', 'rem_sleep_hours'], 
                        var_name='Phase', value_name='Heures')
    
    names = {'deep_sleep_hours': 'Profond', 'rem_sleep_hours': 'REM'}
    df_melt['Phase'] = df_melt['Phase'].map(names)
    
    fig = px.line(df_melt, x='date', y='Heures', color='Phase',
                        color_discrete_map={'Profond': THEME_COLORS['success'], 'REM': THEME_COLORS['secondary']})
    
    update_premium_layout(fig)
    st.plotly_chart(fig, width="stretch", key="chart_rem_deep")
    st.caption("ℹ️ Un bon équilibre Deep/REM est signe d'une récupération complète.")

def plot_bedtime_correlation(df, targets=None):
    if not has_valid_data(df, ['start_time', 'total_sleep_hours']): return

    st.subheader("Corrélation Coucher/Durée")
    df_corr = df.dropna(subset=['start_time']).copy()
    
    def to_dec(dt):
        val = dt.hour + dt.minute/60.0
        if val < 12: val += 24
        return val
        
    df_corr['couch_dec'] = df_corr['start_time'].apply(to_dec)
    
    fig = px.scatter(df_corr, x='couch_dec', y='total_sleep_hours', trendline="ols",
                            labels={'couch_dec': 'Heure Coucher (Décimale)', 'total_sleep_hours': 'Durée (h)'})
    
    fig.update_traces(marker=dict(size=10, color=THEME_COLORS['info'], line=dict(width=1, color='white')))
    update_premium_layout(fig)
    # Custom ticks needed for X axis to be readable? Standard decimal is ok for now.
    st.plotly_chart(fig, width="stretch", key="chart_corr")
    st.caption("ℹ️ Vérifie si se coucher plus tôt allonge réellement vos nuits.")

def plot_bedtime_distribution(df, targets=None):
    if not has_valid_data(df, ['start_time']): return

    st.subheader("Distribution Heure Coucher")
    df_dist = df.dropna(subset=['start_time']).copy()
    df_dist['h'] = df_dist['start_time'].dt.hour
    df_dist['h_sort'] = df_dist['h'].apply(lambda x: x+24 if x<12 else x)
    
    counts = df_dist['h_sort'].value_counts().sort_index()
    labels = [f"{h-24}h" if h>=24 else f"{h}h" for h in counts.index]
    
    fig = px.bar(x=labels, y=counts.values, color_discrete_sequence=[THEME_COLORS['secondary']])
    
    fig.update_traces(hovertemplate='<b>%{x}</b><br>Nuits: %{y}<extra></extra>')
    
    update_premium_layout(fig)
    fig.update_layout(title_text="", showlegend=False)
    st.plotly_chart(fig, width="stretch", key="chart_bed_dist")
    st.caption("ℹ️ La constance de l'heure de coucher est un pilier de l'hygiène de sommeil.")

def plot_rolling_average(df, targets=None):
    if not has_valid_data(df, ['total_sleep_hours']): return

    st.subheader("Moyenne Mobile (7j)")
    df_roll = df.copy().sort_values('date')
    df_roll['Moyenne 7j'] = df_roll['total_sleep_hours'].rolling(7, center=True).mean()
    
    fig = px.line(df_roll, x='date', y=['total_sleep_hours', 'Moyenne 7j'],
                        color_discrete_sequence=["rgba(255,255,255,0.3)", THEME_COLORS['primary']])
    
    # Override brute line dash
    fig.data[0].update(line=dict(dash='dot'), name='Brut')
    fig.data[1].update(width=3, name='Lissé (7j)')
    
    update_premium_layout(fig)
    st.plotly_chart(fig, width="stretch", key="chart_roll")
    st.caption("ℹ️ Lisse les variations quotidiennes pour montrer la tendance réelle.")

def plot_global_phase_breakdown(df, targets=None):
    phases = ['deep_sleep_hours', 'light_sleep_hours', 'rem_sleep_hours', 'awake_sleep_hours']
    # On affiche s'il y a au moins une phase, mais idéalement toutes
    present = [p for p in phases if p in df.columns]
    if not present: return

    st.subheader("Répartition Globale")
    sums = df[present].sum()
    names = {'deep_sleep_hours': 'Profond', 'light_sleep_hours': 'Léger', 'rem_sleep_hours': 'REM', 'awake_sleep_hours': 'Éveillé'}
    labels = [names.get(x,x) for x in sums.index]
    
    fig = px.pie(values=sums.values, names=labels, hole=0.4,
                        color_discrete_sequence=[THEME_COLORS['success'], THEME_COLORS['secondary'], THEME_COLORS['primary'], THEME_COLORS['warning']])
    
    update_premium_layout(fig)
    st.plotly_chart(fig, width="stretch", key="chart_pie")
    st.caption("ℹ️ Proportion totale de chaque phase sur la période.")


def plot_activity_interactions(df, targets=None):
    # Check basics. Individually specific plots check their own cols below.
    # But if NO metrics available at all, hide entire section?
    # Actually user wants "supprime les".
    
    # We will check individually.
    has_steps = has_valid_data(df, ['steps', 'total_sleep_hours'])
    has_rhr = has_valid_data(df, ['rhr', 'deep_sleep_hours'])
    has_stress = has_valid_data(df, ['stress_avg', 'sleep_score'])
    
    if not (has_steps or has_rhr or has_stress): return

    st.subheader("Correlations Activité & Santé")
    
    # 1. Scatter: Steps vs Sleep Duration
    if has_steps:
        st.markdown("##### 👣 Pas vs Durée de Sommeil")
        fig1 = px.scatter(
            df, x='steps', y='total_sleep_hours', 
            trendline="ols",
            color='sleep_score' if 'sleep_score' in df.columns else None,
            labels={'steps': 'Pas Quotidiens', 'total_sleep_hours': 'Durée Sommeil (h)', 'sleep_score': 'Score'},
            color_continuous_scale='Teal'
        )
        update_premium_layout(fig1)
        st.plotly_chart(fig1, width="stretch", key="act_scatter_1")
        st.caption("ℹ️ L'activité physique favorise généralement un sommeil plus long et profond.")

    # 2. Scatter: RHR vs Deep Sleep %
    if has_rhr and 'total_sleep_hours' in df.columns:
        st.markdown("##### ❤️ RHR vs Sommeil Profond (%)")
        df['deep_pct'] = (df['deep_sleep_hours'] / df['total_sleep_hours']) * 100
        fig2 = px.scatter(
            df, x='rhr', y='deep_pct', 
            trendline="ols",
            labels={'rhr': 'RHR (bpm)', 'deep_pct': '% Profond'},
        )
        fig2.update_traces(marker=dict(color=THEME_COLORS['secondary']))
        update_premium_layout(fig2)
        st.plotly_chart(fig2, width="stretch", key="act_scatter_2")
        st.caption("ℹ️ Une fréquence cardiaque de repos basse est souvent corrélée à une meilleure récupération.")

    # 3. Dual Axis: Stress vs Sleep Score (Time Series)
    if has_stress:
        st.markdown("##### 🧘 Stress vs Score de Sommeil")
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go

        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Line for Stress
        fig3.add_trace(
            go.Scatter(x=df['date'], y=df['stress_avg'], name="Stress Moyen", line=dict(color=THEME_COLORS['warning'])),
            secondary_y=False
        )
        
        # Bars for Sleep Score
        fig3.add_trace(
            go.Bar(x=df['date'], y=df['sleep_score'], name="Score Sommeil", marker_color="rgba(59, 130, 246, 0.5)"),
            secondary_y=True
        )
        
        fig3.update_layout(title_text="Stress & Qualité")
        fig3.update_xaxes(title_text="Date")
        fig3.update_yaxes(title_text="Stress (0-100)", secondary_y=False)
        fig3.update_yaxes(title_text="Score Sommeil", secondary_y=True)
        
        update_premium_layout(fig3)
        st.plotly_chart(fig3, use_container_width=True, key="act_dual_stress")
        st.caption("ℹ️ Le stress élevé en journée impacte souvent négativement le score de la nuit suivante.")
        

def plot_wakeup_time_distribution(df, targets=None):
    if not has_valid_data(df, ['end_time']): return

    st.subheader("Distribution Heure de Réveil")
    df_dist = df.dropna(subset=['end_time']).copy()
    df_dist['h'] = df_dist['end_time'].dt.hour + df_dist['end_time'].dt.minute/60
    
    fig = px.histogram(df_dist, x="h", nbins=20, 
                        labels={'h': 'Heure de Réveil'},
                        color_discrete_sequence=[THEME_COLORS['primary']])
    
    fig.update_traces(hovertemplate='<b>%{x:.1f} h</b><br>Nuits: %{y}<extra></extra>')
    update_premium_layout(fig)
    fig.update_layout(xaxis_title="Heure (Décimale)", yaxis_title="Fréquence", title_text="", showlegend=False)
    st.plotly_chart(fig, width="stretch", key="dist_wakeup")
    st.caption("ℹ️ Un réveil à heure fixe aide à synchroniser votre rythme circadien.")

def plot_deep_sleep_distribution(df, targets=None):
    if not has_valid_data(df, ['deep_sleep_hours']): return

    st.subheader("Distribution Sommeil Profond (h)")
    fig = px.histogram(df, x="deep_sleep_hours", nbins=15, marginal="box",
                        color_discrete_sequence=[THEME_COLORS['success']],
                        labels={'deep_sleep_hours': 'Heures'})
    fig.update_traces(hovertemplate='<b>%{x} h</b><br>Nuits: %{y}<extra></extra>')
    update_premium_layout(fig)
    fig.update_layout(title_text="", showlegend=False)
    st.plotly_chart(fig, width="stretch", key="dist_deep")
    st.caption("ℹ️ Utile pour repérer si vous atteignez souvent votre cible de profond.")

def plot_rem_sleep_distribution(df, targets=None):
    if not has_valid_data(df, ['rem_sleep_hours']): return

    st.subheader("Distribution Sommeil REM (h)")
    fig = px.histogram(df, x="rem_sleep_hours", nbins=15, marginal="box",
                        color_discrete_sequence=[THEME_COLORS['secondary']],
                        labels={'rem_sleep_hours': 'Heures'})
    fig.update_traces(hovertemplate='<b>%{x} h</b><br>Nuits: %{y}<extra></extra>')
    update_premium_layout(fig)
    fig.update_layout(title_text="", showlegend=False)
    st.plotly_chart(fig, width="stretch", key="dist_rem")
    st.caption("ℹ️ Le REM soutient la mémoire et la régulation émotionnelle.")

def plot_sleep_score_distribution(df, targets=None):
    if not has_valid_data(df, ['sleep_score']): return

    st.subheader("Distribution des Scores")
    fig = px.histogram(df, x="sleep_score", nbins=10, 
                        color_discrete_sequence=["#8b5cf6"],
                        labels={'sleep_score': 'Score'})
    fig.update_traces(hovertemplate='<b>Score %{x}</b><br>Nuits: %{y}<extra></extra>')
    update_premium_layout(fig)
    fig.update_layout(title_text="", showlegend=False)
    st.plotly_chart(fig, width="stretch", key="dist_score")
    st.caption("ℹ️ Plus la courbe est à droite, plus votre qualité globale est haute.")

def plot_stress_score_distribution(df, targets=None):
    if not has_valid_data(df, ['stress_avg']): return

    st.subheader("Distribution du Stress")
    fig = px.histogram(df, x="stress_avg", nbins=15, 
                        color_discrete_sequence=[THEME_COLORS['warning']],
                        labels={'stress_avg': 'Stress Moyen'})
    fig.update_traces(hovertemplate='<b>Stress %{x}</b><br>Nuits: %{y}<extra></extra>')
    update_premium_layout(fig)
    fig.update_layout(title_text="", showlegend=False)
    st.plotly_chart(fig, width="stretch", key="dist_stress")
    st.caption("ℹ️ Un stress moyen bas (<25 au repos, <50 global) favorise un meilleur sommeil.")

def plot_weekday_sleep_boxplot(df, targets=None):
    if not has_valid_data(df, ['total_sleep_hours']): return

    st.subheader("Variabilité par Jour (Boxplot)")
    df['day_name'] = df['date'].dt.day_name()
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    fig = px.box(df, x="day_name", y="total_sleep_hours", 
                     category_orders={"day_name": days_order},
                     color_discrete_sequence=[THEME_COLORS['info']],
                     labels={'day_name': 'Jour', 'total_sleep_hours': 'Heures'})
    update_premium_layout(fig)
    st.plotly_chart(fig, width="stretch", key="dist_box_day")
    st.caption("ℹ️ Détectez si certains jours spécifiques sont systématiquement problématiques.")

def plot_score_by_weekday_violin(df, targets=None):
    if not has_valid_data(df, ['sleep_score']): return

    st.subheader("Scores par Jour (Violin)")
    df['day_name'] = df['date'].dt.day_name()
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    fig = px.violin(df, x="day_name", y="sleep_score", box=True, points="all",
                    category_orders={"day_name": days_order},
                    color_discrete_sequence=[THEME_COLORS['secondary']],
                    labels={'day_name': 'Jour', 'sleep_score': 'Score'})
    update_premium_layout(fig)
    st.plotly_chart(fig, width="stretch", key="dist_violin_score")
    st.caption("ℹ️ La largeur du violon montre la fréquence des scores pour ce jour.")

def plot_correlation_heatmap(df, targets=None):
    cols = ['total_sleep_hours', 'deep_sleep_hours', 'rem_sleep_hours', 'awake_sleep_hours', 'sleep_score', 'stress_avg', 'rhr', 'steps']
    valid_cols = [c for c in cols if c in df.columns and has_valid_data(df, [c])]
    
    if len(valid_cols) <= 2: return

    st.subheader("Matrice de Corrélation")
    corr = df[valid_cols].corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu_r', aspect="auto")
    update_premium_layout(fig)
    st.plotly_chart(fig, width="stretch", key="dist_corr_matrix")
    st.caption("ℹ️ Rouge = Corrélation Positive (ex: Pas & Sommeil), Bleu = Négative (ex: Stress & Score).")

def plot_weekday_distribution(df, targets=None):
    if not has_valid_data(df, ['total_sleep_hours', 'date']): return

    st.subheader("Distribution (Semaine uniquement)")
    # Filter: Mon=0 ... Fri=4. Weekday is < 5.
    df_week = df[df['date'].dt.dayofweek < 5].copy()
    
    if df_week.empty:
        st.warning("Pas de données de semaine.")
        return

    fig = px.histogram(df_week, x="total_sleep_hours", nbins=15, 
                            color_discrete_sequence=[THEME_COLORS['primary']],
                            labels={'total_sleep_hours': 'Durée (h)'})
    
    if targets:
        val = targets.get('target_duration', 8.0)
        fig.add_vline(x=val, line_color=THEME_COLORS['success'], line_dash="dash", annotation_text=f"Obj: {val}h")

    fig.update_traces(
        marker_line_width=1, marker_line_color="#1e293b",
        hovertemplate='<b>%{x} h</b><br>Nuits: %{y}<extra></extra>'
    )
    fig.update_layout(bargap=0.1)
    
    update_premium_layout(fig)
    fig.update_layout(
        xaxis_title="Heures de Sommeil (Lun-Ven)", 
        yaxis_title="Fréquence", 
        showlegend=False,
        title_text=""
    )
    st.plotly_chart(fig, width="stretch", key="dist_week_only")
    st.caption("ℹ️ Une distribution centrée sur 8h en semaine indique une bonne gestion du rythme de travail.")


def plot_trading_readiness(df, targets=None):
    if not has_valid_data(df, ['total_sleep_hours', 'date']): return

    st.subheader("Préparation Trading (Récupération)")
    
    # Target definition
    target_val = 8.0
    if targets and 'target_duration' in targets:
        try: target_val = float(targets['target_duration'])
        except: pass

    # Prepare Streak Data
    df_sort = df.sort_values('date').copy()
    streaks = []
    current_streak = 0
    
    # On itère pour calculer le streak cumulatif
    for val in df_sort['total_sleep_hours']:
        # On tolère une petite marge (ex: 7.8h est ok pour 8h ?) 
        # Pour l'instant strict >= target ou user rule >= 8.
        # User defined: "8 à 9 heures". Let's use target_val.
        if val >= target_val:
            current_streak += 1
        else:
            current_streak = 0
        streaks.append(current_streak)
        
    df_sort['streak'] = streaks
    
    # Interpretation mapping
    def interpret(s):
        if s <= 0: return "Fatigue (Risque)"
        if s <= 2: return "Amélioration"
        if s == 3: return "Cerveau OK"
        if s == 4: return "Prêt à Trader"
        return "Performance Max"

    df_sort['status'] = df_sort['streak'].apply(interpret)
    
    # Color mapping
    colors = []
    for s in df_sort['streak']:
        if s == 0: colors.append(THEME_COLORS['danger'])       # Red
        elif s <= 2: colors.append(THEME_COLORS['warning'])    # Orange
        elif s == 3: colors.append(THEME_COLORS['info'])       # Blue
        else: colors.append(THEME_COLORS['success'])           # Green

    fig = px.bar(df_sort, x='date', y='streak',
                 labels={'streak': 'Jours Consécutifs (>Obj.)', 'date': 'Date'})
    
    fig.update_traces(marker_color=colors, 
                      hovertemplate='<b>%{x}</b><br>Streak: %{y} Jours<br>Status: %{customdata[0]}<extra></extra>',
                      customdata=df_sort[['status']])
    
    # Add Threshold lines interpretation
    fig.add_hline(y=3, line_dash="dot", line_color=THEME_COLORS['info'], annotation_text="3j: Cerveau OK")
    fig.add_hline(y=4, line_dash="dash", line_color=THEME_COLORS['success'], annotation_text="4j: Prêt")
    
    update_premium_layout(fig)
    fig.update_layout(yaxis_title="Jours Consécutifs")
    
    st.plotly_chart(fig, width="stretch", key="chart_trading")
    st.caption("⏱️ '3 à 5 jours à 8h+' sont nécessaires pour une stabilité émotionnelle et une concentration optimale.")
