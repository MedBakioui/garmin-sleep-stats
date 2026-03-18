# 🌙 Garmin Sleep Stats Dashboard

Une application avancée de visualisation et d'analyse de sommeil basée sur les données de **Garmin Connect**. Ce tableau de bord permet de comprendre en profondeur la qualité de vos nuits, de suivre vos tendances et d'obtenir des conseils personnalisés via une IA.

## ✨ Fonctionnalités
- **📊 Tableau de bord Premium** : Visualisation interactive des phases de sommeil (Léger, REM, Profond, Éveil).
- **📉 Suivi des Tendances** : Analyse de la durée de sommeil, de la régularité et de la "dette de sommeil" sur le long terme.
- **🧬 Métriques Physiologiques** : Corrélation avec la variabilité de la fréquence cardiaque (HRV) et le stress.
- **💬 Coach IA (DeepSeek)** : Un assistant intelligent qui analyse vos données pour vous donner des conseils d'amélioration.
- **☁️ Synchronisation Cloud** : Persistance des données via Supabase pour un accès fluide sur tous vos appareils (PC, Mobile).
- **🔐 Accès Sécurisé** : Protection par code d'accès pour garantir la confidentialité de vos données de santé.

## 🛠️ Stack Technique
- **Frontend** : [Streamlit](https://streamlit.io/) (Python)
- **Data** : Pandas, Plotly, Statsmodels
- **API** : GarminConnect (via `garminconnect`)
- **Base de données** : Supabase
- **IA** : DeepSeek API / OpenAI
- **Déploiement** : Docker, Docker-compose, Streamlit Cloud

## 🚀 Installation & Déploiement
Consultez le fichier `deployment_guide.md` pour les instructions détaillées sur le déploiement local (Docker) ou Cloud (Streamlit Cloud).

## 🛡️ Sécurité
Le projet est conçu pour être déployé en mode **Privé**. Les identifiants et clés API sont gérés via des secrets environnementaux ou le système de `Secrets` de Streamlit.
