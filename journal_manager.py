import json
import os
import datetime

JOURNAL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sleep_journal.json")

class JournalManager:
    def __init__(self):
        self.journal = self._load_journal()

    def _load_journal(self):
        if os.path.exists(JOURNAL_FILE):
            try:
                with open(JOURNAL_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erreur chargement journal: {e}")
                return {}
        return {}

    def _save_journal(self):
        try:
            with open(JOURNAL_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.journal, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur sauvegarde journal: {e}")

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
