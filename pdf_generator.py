from fpdf import FPDF
import pandas as pd
from datetime import datetime
import os

class SleepReportPDF(FPDF):
    def header(self):
        # Background color for header
        self.set_fill_color(15, 23, 42) # Slate 900
        self.rect(0, 0, 210, 40, 'F')
        
        # Logo or Title
        self.set_font('helvetica', 'B', 24)
        self.set_text_color(255, 255, 255)
        self.cell(0, 20, 'GARMIN SLEEP STATS', ln=True, align='C')
        
        self.set_font('helvetica', 'I', 10)
        self.set_text_color(148, 163, 184) # Slate 400
        self.cell(0, 0, f'Généré le {datetime.now().strftime("%d/%m/%Y %H:%M")}', ln=True, align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

def generate_pdf_report(df: pd.DataFrame, start_date: str, end_date: str) -> bytes:
    """Génère un rapport de sommeil au format PDF.

    Args:
        df (pd.DataFrame): Données de sommeil et métriques.
        start_date (str): Date de début de période.
        end_date (str): Date de fin de période.

    Returns:
        bytes: Le contenu du fichier PDF.
    """
    pdf = SleepReportPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Titre de la période
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 10, f"Rapport Analytique : {start_date} au {end_date}", ln=True)
    pdf.ln(5)
    
    # --- SECTION : RÉSUMÉ DES MÉTRIQUES ---
    pdf.set_fill_color(248, 250, 252) # Slate 50
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, "Résumé Global", ln=True, fill=True)
    pdf.ln(2)
    
    avg_duration = df['total_sleep_hours'].mean()
    avg_score = df['sleep_score'].mean() if 'sleep_score' in df.columns else 0
    avg_deep = (df['deep_sleep_hours'].mean() / avg_duration * 100) if avg_duration > 0 else 0
    
    pdf.set_font('helvetica', '', 11)
    pdf.cell(60, 10, f"Durée de sommeil moy. :", 0)
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 10, f"{int(avg_duration)}h {int((avg_duration%1)*60)}m", ln=True)
    
    pdf.set_font('helvetica', '', 11)
    pdf.cell(60, 10, f"Score de sommeil moy. :", 0)
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 10, f"{avg_score:.1f}/100", ln=True)
    
    pdf.set_font('helvetica', '', 11)
    pdf.cell(60, 10, f"Ratio sommeil profond :", 0)
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 10, f"{avg_deep:.1f}%", ln=True)
    pdf.ln(10)

    # --- SECTION : TABLEAU DE DONNÉES ---
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_fill_color(248, 250, 252)
    pdf.cell(0, 10, "Détail Quotidien", ln=True, fill=True)
    pdf.ln(2)
    
    # Header du tableau
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_fill_color(226, 232, 240) # Slate 200
    cols = [('Date', 25), ('Durée', 25), ('Profond', 25), ('Score', 20), ('Pas', 25), ('RHR', 20), ('Stress', 20)]
    
    for col_name, width in cols:
        pdf.cell(width, 10, col_name, 1, 0, 'C', True)
    pdf.ln()
    
    # Données du tableau
    pdf.set_font('helvetica', '', 9)
    # Tri par date décroissante pour le rapport
    df_sorted = df.sort_values('date', ascending=False)
    
    for _, row in df_sorted.iterrows():
        # Date
        date_str = str(row['date'])
        pdf.cell(cols[0][1], 8, date_str, 1)
        
        # Durée
        h = row['total_sleep_hours']
        pdf.cell(cols[1][1], 8, f"{int(h)}h{int((h%1)*60):02d}", 1, 0, 'C')
        
        # Profond
        dp = row.get('deep_sleep_hours', 0)
        pdf.cell(cols[2][1], 8, f"{int(dp)}h{int((dp%1)*60):02d}", 1, 0, 'C')
        
        # Score
        sc = row.get('sleep_score', '-')
        pdf.cell(cols[3][1], 8, str(sc) if pd.notnull(sc) else '-', 1, 0, 'C')
        
        # Pas
        st = row.get('steps', '-')
        pdf.cell(cols[4][1], 8, f"{int(st)}" if pd.notnull(st) else '-', 1, 0, 'C')
        
        # RHR
        rh = row.get('rhr', '-')
        pdf.cell(cols[5][1], 8, f"{int(rh)}" if pd.notnull(rh) else '-', 1, 0, 'C')
        
        # Stress
        strss = row.get('stress_avg', '-')
        pdf.cell(cols[6][1], 8, f"{int(strss)}" if pd.notnull(strss) else '-', 1, 0, 'C')
        
        pdf.ln()

    return pdf.output()
