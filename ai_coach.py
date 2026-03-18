import streamlit as st
from openai import OpenAI
import pandas as pd
import json

class AICoach:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        
    def generate_context(self, df, settings):
        """Prépare un résumé des données pour l'IA."""
        if df.empty: return "Aucune donnée de sommeil disponible."
        
        # Stats globales
        avg_dur = df['total_sleep_hours'].mean()
        avg_score = df.dropna(subset=['sleep_score'])['sleep_score'].mean() if 'sleep_score' in df.columns else 0
        
        # Dernières nuits
        last_3 = df.tail(3)[['date', 'total_sleep_hours', 'sleep_score']].to_dict('records')
        
        # Objectifs
        target_dur = settings.get('target_duration', 8.0)
        
        context = f"""
        CONTEXTE UTILISATEUR:
        - Moyenne durée (période): {avg_dur:.1f}h (Objectif: {target_dur}h)
        - Score moyen: {avg_score:.1f}/100
        - 3 dernières nuits: {last_3}
        
        Tu es un Coach de Sommeil expert et bienveillant. Analyse ces données pour répondre à la question de l'utilisateur.
        Sois concis, motivant, et base-toi sur les données fournies. Si les données sont mauvaises, propose des conseils pratiques, ne sois pas trop dur.
        """
        return context

    def ask(self, context, question):
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": question}
                ],
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Erreur API DeepSeek : {e}"
