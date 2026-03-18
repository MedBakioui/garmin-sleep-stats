import json
import os
import datetime

JOURNAL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sleep_journal.json")

try:
    import streamlit as st
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

class JournalManager:
    def __init__(self):
        # --- SUPABASE CONFIG ---
        self.supabase: Optional[Client] = None
        self.user_id: Optional[str] = None
        
        if SUPABASE_AVAILABLE:
            try:
                url = st.secrets.get("SUPABASE_URL")
                key = st.secrets.get("SUPABASE_KEY")
                if url and key:
                    self.supabase = create_client(url, key)
                    if 'user' in st.session_state and st.session_state.user:
                        self.user_id = st.session_state.user.id
            except:
                pass
                
        self.journal = self._load_journal()

    def _load_journal(self):
        local_journal = {}
        if os.path.exists(JOURNAL_FILE):
            try:
                with open(JOURNAL_FILE, 'r', encoding='utf-8') as f:
                    local_journal = json.load(f)
            except Exception as e:
                print(f"Erreur chargement journal: {e}")
        
        # --- SYNC DEPUIS SUPABASE ---
        if self.supabase and self.user_id:
            try:
                response = self.supabase.table("journal_entries").select("*").eq("user_id", self.user_id).execute()
                if response.data:
                    remote_data = {}
                    for row in response.data:
                        d = str(row['date'])
                        remote_data[d] = {
                            "tags": row.get("tags", []),
                            "notes": row.get("note", ""),
                            "mood": 3 # Par défaut si non stalké
                        }
                    local_journal.update(remote_data)
                    # Mise à jour locale
                    with open(JOURNAL_FILE, 'w', encoding='utf-8') as f:
                        json.dump(local_journal, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Supabase Journal Load Error: {e}")
                
        return local_journal

    def _save_journal(self):
        # Sauvegarde locale
        try:
            with open(JOURNAL_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.journal, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur sauvegarde journal: {e}")
            
        # Sauvegarde distante (Supabase)
        if self.supabase and self.user_id:
            try:
                to_upsert = []
                for d, c in self.journal.items():
                    to_upsert.append({
                        "user_id": self.user_id,
                        "date": d,
                        "tags": c.get("tags", []),
                        "note": c.get("notes", "")
                    })
                if to_upsert:
                    self.supabase.table("journal_entries").upsert(to_upsert, on_conflict="user_id,date").execute()
            except Exception as e:
                print(f"Supabase Journal Sync Error: {e}")

    def get_entry(self, date_obj: datetime.date):
        """Récupère l'entrée pour une date spécifique."""
        date_str = date_obj.isoformat()
        return self.journal.get(date_str, {"tags": [], "notes": "", "mood": 3})

    def save_entry(self, date_obj: datetime.date, tags: list, notes: str, mood: int = 3):
        """Sauvegarde les tags, notes et mood pour une date."""
        date_str = date_obj.isoformat()
        
        # Nettoyage si tout est par défaut/vide
        if not tags and not notes.strip() and mood == 3:
            if date_str in self.journal:
                del self.journal[date_str]
        else:
            self.journal[date_str] = {
                "tags": tags,
                "notes": notes.strip(),
                "mood": mood
            }
        
        self._save_journal()

    def get_all_entries(self):
        return self.journal

    def get_tag_stats(self):
        """Calcule la fréquence des tags."""
        stats = {}
        for entry in self.journal.values():
            for tag in entry.get("tags", []):
                stats[tag] = stats.get(tag, 0) + 1
        return dict(sorted(stats.items(), key=lambda item: item[1], reverse=True))

    def get_available_tags(self):
        """Retourne la liste des tags suggérés."""
        return [
            "☕ Caféine Tardive",
            "🍷 Alcool",
            "🏋️ Sport Intense",
            "🍱 Repas Copieux",
            "🧘 Méditation",
            "💻 Écrans Bleus",
            "🌡️ Température Élevée",
            "🤒 Malade",
            "🧠 Stress Élevé",
            "👶 Réveil Enfant",
            "🧴 Magnésium/Supp",
            "📚 Lecture"
        ]
