import datetime
from datetime import date
from typing import List, Dict, Any, Optional, Tuple, Union
import time
import base64
import json
from garminconnect import Garmin
import pandas as pd

class GarminClient:
    """Client API pour l'interaction avec Garmin Connect.
    
    Cette classe encapsulate les appels à la bibliothèque garminconnect pour 
    l'authentification et la récupération des données de sommeil et de santé.

    Attributes:
        email (str): Email du compte Garmin.
        password (str): Mot de passe du compte Garmin.
        client (Optional[Garmin]): Instance authentifiée du client Garmin API.
    """

    def __init__(self, email: str, password: str, session_token: Optional[str] = None):
        """Initialise le GarminClient.

        Args:
            email (str): Email de connexion.
            password (str): Mot de passe de connexion.
            session_token (str, optional): Jeton JSON pour éviter le blocage IP.
        """
        self.email = email
        self.password = password
        self.session_token = session_token
        self.client: Optional[Garmin] = None

    def connect(self) -> Tuple[bool, str]:
        """Authentification auprès de Garmin Connect avec persistance de session."""
        import os
        import json
        session_path = "garmin_session.json"
        
        try:
            self.client = Garmin(self.email, self.password)
            
            # Priorité: Si un jeton est fourni dans les Secrets/Env
            if self.session_token:
                import streamlit as st
                st.info("🔄 Tentative de connexion via session sécurisée...")
                token_str = self.session_token.strip().strip("'").strip('"')
                
                try:
                    # 1. Décodage et Nettoyage
                    if token_str.startswith('W3s'):
                        import base64
                        decoded_bytes = base64.b64decode(token_str)
                        session_json = decoded_bytes.decode('utf-8')
                    else:
                        session_json = token_str
                    
                    # 2. Injection directe dans Garth (plus stable que le fichier)
                    self.client.garth.loads(session_json)
                    
                    # 3. Vérification immédiate
                    if self.client.garth.oauth2_token:
                        # On récupère le nom pour confirmer la connexion
                        try:
                            self.client.display_name = self.client.garth.profile.get("displayName")
                            return True, f"Session restaurée pour {self.client.display_name}"
                        except:
                            return True, "Session restaurée (Vérifiée)"
                    else:
                        st.warning("⚠️ Le jeton semble vide après chargement.")
                except Exception as de:
                    st.error(f"❌ Erreur technique sur le jeton : {str(de)}")
                    # On continue pour tenter le fichier ou le login normal
            
            # Tentative via fichier physique (si présent sur le serveur)
            if os.path.exists(session_path):
                try:
                    self.client.login(tokenstore=session_path)
                    return True, "Session restaurée (Fichier)"
                except Exception:
                    pass
            
            # Login normal si pas de session ou session expirée
            self.client.login()
            
            # Sauvegarde du nouveau token (utilisant garth sous le capot de garminconnect)
            try:
                import json
                # garminconnect uses 'garth' for session management
                # we can save the garth session as a directory or a json if supported
                # Here we use the underlying garth session tokens
                if hasattr(self.client, "garth") and hasattr(self.client.garth, "dumps"):
                    session_json = self.client.garth.dumps()
                    with open(session_path, 'w') as f:
                        json.dump(session_json, f)
            except Exception as se:
                print(f"Erreur sauvegarde session: {se}")
            
            return True, "Connexion réussie"
        except Exception as e:
            return False, str(e)

    def get_sleep_data(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Dict[str, Any]]:
        """Récupère les données de sommeil brutes pour une période donnée.
        
        Args:
            start_date: Date de début. Si None, prend hier.
            end_date: Date de fin. Si None, prend start_date.

        Returns:
            List[Dict[str, Any]]: Liste des dictionnaires de sommeil bruts de l'API.
            
        Raises:
            Exception: Si le client n'est pas connecté.
        """
        if not self.client:
            raise Exception("Client non connecté")

        if start_date is None:
            # Par défaut hier (pour avoir des données complètes)
            start_date = date.today() - datetime.timedelta(days=1)
        
        if end_date is None:
            end_date = start_date

        try:
            all_data: List[Dict[str, Any]] = []
            
            current_date = start_date
            while current_date <= end_date:
                # Politesse pour éviter le 429
                if current_date > start_date:
                    time.sleep(1.5)
                
                # get_sleep_data renvoie les détails pour un jour spécifique
                try:
                    data = self.client.get_sleep_data(current_date.isoformat())
                    if data:
                        all_data.append(data)
                except Exception as e:
                    if "429" in str(e) or "Too Many Requests" in str(e):
                        print(f"Rate limit hit at {current_date}")
                        raise Exception("Garmin Rate Limit (429): Trop de requêtes. Veuillez patienter.")
                    print(f"Erreur pour {current_date}: {e}")
                
                current_date += datetime.timedelta(days=1)
                
            return all_data
            
        except Exception as e:
            print(f"Erreur lors de la récupération : {e}")
            return []

    def parse_to_dataframe(self, raw_data_list: List[Dict[str, Any]]) -> pd.DataFrame:
        """Transforme les données de sommeil brutes en DataFrame Pandas structuré.

        Args:
            raw_data_list (List[Dict[str, Any]]): Données brutes de l'API.

        Returns:
            pd.DataFrame: DataFrame avec conversion en heures et types de données corrects.
        """
        records: List[Dict[str, Any]] = []
        for entry in raw_data_list:
            # La structure peut varier, on essaie d'extraire de 'dailySleepDTO'
            data = entry.get('dailySleepDTO', entry)
            
            # Extraction sécurisée des champs
            record = {
                'date': data.get('calendarDate'),
                'total_sleep_seconds': data.get('sleepTimeSeconds'),
                'deep_sleep_seconds': data.get('deepSleepSeconds'),
                'light_sleep_seconds': data.get('lightSleepSeconds'),
                'rem_sleep_seconds': data.get('remSleepSeconds'),
                'awake_sleep_seconds': data.get('awakeSleepSeconds'),
                'sleep_score': data.get('sleepScores', {}).get('overall', {}).get('value'),
                'sleep_quality': data.get('sleepScores', {}).get('overall', {}).get('qualifierKey'),
                'start_timestamp_gmt': data.get('sleepStartTimestampGMT'),
                'end_timestamp_gmt': data.get('sleepEndTimestampGMT'),
            }
            records.append(record)
            
        df = pd.DataFrame(records)
        if not df.empty:
            # Conversion en heures pour l'affichage facile
            cols_to_convert = ['total_sleep_seconds', 'deep_sleep_seconds', 'light_sleep_seconds', 'rem_sleep_seconds', 'awake_sleep_seconds']
            for col in cols_to_convert:
                if col in df.columns:
                    df[col.replace('_seconds', '_hours')] = df[col] / 3600
            
            # Conversion des timestamps en datetime
            if 'start_timestamp_gmt' in df.columns:
                df['start_time'] = pd.to_datetime(df['start_timestamp_gmt'], unit='ms')
            if 'end_timestamp_gmt' in df.columns:
                df['end_time'] = pd.to_datetime(df['end_timestamp_gmt'], unit='ms')
            
            # Assurer que la colonne date est au format datetime pour les fusions
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date']).dt.date
        
        return df

    def get_daily_metrics(self, start_date: date, end_date: date) -> pd.DataFrame:
        """Récupère les métriques quotidiennes (Pas, RHR, Stress).

        Args:
            start_date: Date de début.
            end_date: Date de fin.

        Returns:
            pd.DataFrame: DataFrame contenant Steps, RHR et Stress.
        """
        if not self.client:
            return pd.DataFrame()
            
        data: List[Dict[str, Any]] = []
        current = start_date
        while current <= end_date:
            # Politesse
            if current > start_date:
                time.sleep(1.2)
                
            try:
                # get_user_summary renvoie un JSON complet pour la journée
                summary = self.client.get_user_summary(current.isoformat())
                if summary:
                    rec = {
                        'date': current,
                        'steps': summary.get('totalSteps'),
                        'rhr': summary.get('restingHeartRate'),
                        'stress_avg': summary.get('averageStressLevel'),
                        'body_battery_max': summary.get('maxBodyBattery'),
                        'body_battery_min': summary.get('minBodyBattery')
                    }
                    data.append(rec)
            except Exception as e:
                if "429" in str(e) or "Too Many Requests" in str(e):
                    print(f"Rate limit hit at {current}")
                    raise Exception("Garmin Rate Limit (429): Trop de requêtes. Veuillez patienter.")
                pass # Ignorer silencieusement les autres erreurs d'un jour spécifique
            current += datetime.timedelta(days=1)
            
        df = pd.DataFrame(data)
        if not df.empty and 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date']).dt.date
            
        return df
