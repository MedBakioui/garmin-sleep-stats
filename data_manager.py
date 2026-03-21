import json
import os
import datetime
import time
from datetime import date
import pandas as pd
from typing import List, Dict, Any, Optional, Union, Callable
from garmin_client import GarminClient

CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sleep_cache.json")
METRICS_CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "metrics_cache.json")

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

class DataManager:
    """Gestionnaire de données pour l'application Garmin Sleep Stats.
    
    Cette classe gère la récupération des données de sommeil et des métriques
    via GarminConnect, et assure leur persistance locale.
    """

    def __init__(self, client: GarminClient):
        """Initialise le DataManager avec un client Garmin."""
        self.client = client
        
        # --- SUPABASE CONFIG ---
        self.supabase: Optional[Client] = None
        
        if SUPABASE_AVAILABLE:
            try:
                url = st.secrets.get("SUPABASE_URL")
                key = st.secrets.get("SUPABASE_KEY")
                if url and key:
                    self.supabase = create_client(url, key)
            except:
                pass

        self._sleep_cache: Dict[str, Any] = self._load_cache(CACHE_FILE)
        self._metrics_cache: Dict[str, Any] = self._load_cache(METRICS_CACHE_FILE)

    def _load_cache(self, file_path: str) -> Dict[str, Any]:
        """Charge les données depuis le cache local (JSON) et se synchronise avec Supabase."""
        local_cache = {}
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    local_cache = json.load(f)
            except:
                pass
        
        # --- SYNC DEPUIS SUPABASE ---
        if self.supabase:
            table_name = "sleep_data" if "sleep_cache" in file_path else "daily_metrics"
            try:
                # Récupération simple
                content_col = "raw_data" if table_name == "sleep_data" else "*" 
                response = self.supabase.table(table_name).select(f"date, {content_col}").execute()
                
                if response.data:
                    remote_data = {}
                    for row in response.data:
                        d = str(row['date'])
                        if table_name == "sleep_data":
                            remote_data[d] = row['raw_data']
                        else:
                            remote_data[d] = row
                    
                    local_cache.update(remote_data)
                    
                    # Mise à jour locale
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(local_cache, f, indent=4)
            except Exception as e:
                print(f"Supabase Load Error: {e}")
                
        return local_cache

    def _save_cache(self, cache: Dict[str, Any], file_path: str):
        # Sauvegarde locale
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=4)
            
        # Sauvegarde distante (Supabase)
        if self.supabase:
            table_name = "sleep_data" if "sleep_cache" in file_path else "daily_metrics"
            try:
                to_upsert = []
                for d, c in cache.items():
                    if table_name == "sleep_data":
                        to_upsert.append({"date": d, "raw_data": c})
                    else:
                        to_upsert.append({
                            "date": d,
                            "steps": c.get("steps"),
                            "rhr": c.get("rhr"),
                            "stress_avg": c.get("stress_avg")
                        })
                
                if to_upsert:
                    self.supabase.table(table_name).upsert(to_upsert, on_conflict="date").execute()
            except Exception as e:
                print(f"Supabase Sync Error: {e}")

    def get_sleep_data(self, 
                       start_date: Union[date, str], 
                       end_date: Union[date, str], 
                       force_recent_days: int = 3, 
                       progress_callback: Optional[Callable[[int, int, str], None]] = None) -> List[Dict[str, Any]]:
        """Récupère les données de sommeil brutes pour une période donnée."""
        start_date_obj = start_date if isinstance(start_date, date) else datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = end_date if isinstance(end_date, date) else datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        today = date.today()
        
        all_data: List[Dict[str, Any]] = []
        current = start_date_obj
        
        needed_dates: List[date] = []
        while current <= end_date_obj:
            date_str = current.isoformat()
            is_recent = (today - current).days <= force_recent_days
            
            if date_str in self._sleep_cache and not is_recent:
                all_data.append(self._sleep_cache[date_str])
            else:
                needed_dates.append(current)
            current += datetime.timedelta(days=1)
            
        if needed_dates:
            total = len(needed_dates)
            for i, d in enumerate(needed_dates):
                if progress_callback: progress_callback(i, total, "Sommeil")
                
                # Politesse : délai entre les jours si ce n'est pas le premier jour de la boucle
                if i > 0:
                    time.sleep(1.5)
                    
                try:
                    day_data_list = self.client.get_sleep_data(d, d)
                    if day_data_list:
                        day_data = day_data_list[0]
                        self._sleep_cache[d.isoformat()] = day_data
                        all_data.append(day_data)
                except Exception as e:
                    print(f"Erreur sleep pour {d}: {e}")
                    if "429" in str(e):
                        # En cas de rate limit, on sauvegarde ce qu'on a déjà et on remonte l'erreur
                        self._save_cache(self._sleep_cache, CACHE_FILE)
                        raise e
            
            self._save_cache(self._sleep_cache, CACHE_FILE)
            if progress_callback: progress_callback(total, total, "Sommeil")
            
        # Re-trier par date
        all_data.sort(key=lambda x: x.get("dailySleepDTO", {}).get("calendarDate", ""))
        return all_data

    def get_metrics_data(self, 
                          start_date: Union[date, str], 
                          end_date: Union[date, str], 
                          force_recent_days: int = 3, 
                          progress_callback: Optional[Callable[[int, int, str], None]] = None) -> pd.DataFrame:
        """Récupère les métriques physiologiques avec mise en cache locale."""
        start_date_obj = start_date if isinstance(start_date, date) else datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = end_date if isinstance(end_date, date) else datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        today = date.today()
        
        data: List[Dict[str, Any]] = []
        dates_to_fetch: List[date] = []
        
        current = start_date_obj
        while current <= end_date_obj:
            date_str = current.isoformat()
            is_recent = (today - current).days <= force_recent_days
            
            if date_str in self._metrics_cache and not is_recent:
                data.append(self._metrics_cache[date_str])
            else:
                dates_to_fetch.append(current)
            current += datetime.timedelta(days=1)
            
        if dates_to_fetch:
            total = len(dates_to_fetch)
            for i, d in enumerate(dates_to_fetch):
                if progress_callback: progress_callback(i, total, "Métriques")
                
                # Politesse
                if i > 0:
                    time.sleep(1.2)
                    
                try:
                    df_day = self.client.get_daily_metrics(d, d)
                    if not df_day.empty:
                        rec = df_day.iloc[0].to_dict()
                        # Convertir pandas dates en string pour JSON
                        rec['date'] = d.isoformat()
                        self._metrics_cache[d.isoformat()] = rec
                        data.append(rec)
                except Exception as e:
                    if "429" in str(e):
                        self._save_cache(self._metrics_cache, METRICS_CACHE_FILE)
                        raise e
                    pass
            self._save_cache(self._metrics_cache, METRICS_CACHE_FILE)
            if progress_callback: progress_callback(total, total, "Métriques")

        return pd.DataFrame(data)

    def get_missing_days_count(self, start_date: Union[date, str], end_date: Union[date, str], force_recent_days: int = 3) -> int:
        start_date_obj = start_date if isinstance(start_date, date) else datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = end_date if isinstance(end_date, date) else datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        today = date.today()
        
        count = 0
        current = start_date_obj
        while current <= end_date_obj:
            date_str = current.isoformat()
            is_recent = (today - current).days <= force_recent_days
            if date_str not in self._sleep_cache or is_recent:
                count += 1
            current += datetime.timedelta(days=1)
        return count

    def get_dataframe(self, start_date: Union[date, str], end_date: Union[date, str], **kwargs: Any) -> pd.DataFrame:
        raw_data = self.get_sleep_data(start_date, end_date, **kwargs)
        df_sleep = self.client.parse_to_dataframe(raw_data)
        
        try:
            df_metrics = self.get_metrics_data(start_date, end_date, **kwargs)
            if not df_sleep.empty and not df_metrics.empty:
                df_metrics['date'] = pd.to_datetime(df_metrics['date']).dt.date
                if 'date' in df_sleep.columns:
                     df_sleep = pd.merge(df_sleep, df_metrics, on='date', how='left')
        except Exception as e:
            print(f"Warning merging metrics: {e}")
            
        return df_sleep

    def auto_sync_missing_days(self, window_days: int = 90) -> Dict[str, int]:
        """Analyse et synchronise automatiquement les jours manquants dans le cache.
        
        Args:
            window_days: Nombre de jours en arrière à analyser.
            
        Returns:
            Dict[str, int]: Nombre de jours synchronisés pour chaque type.
        """
        today = date.today()
        start_date = today - datetime.timedelta(days=window_days)
        
        missing_count = self.get_missing_days_count(start_date, today, force_recent_days=3)
        
        if missing_count > 0:
            # On utilise get_dataframe qui orchestre sleep + metrics + cache
            # get_dataframe appelle get_sleep_data et get_metrics_data qui remplissent les caches
            self.get_dataframe(start_date, today, force_recent_days=3)
            return {"synced": missing_count}
        
        return {"synced": 0}
