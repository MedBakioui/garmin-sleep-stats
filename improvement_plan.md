# Plan d'Amélioration Technique "Pro"

Ce document détaille les étapes pour élever la qualité technique du projet vers des standards professionnels (Modularité, Robustesse, Maintenabilité).

## 1. Typage Statique (Type Hinting)
Ajouter des annotations de type partout pour améliorer la lisibilité et permettre l'analyse statique (avec `mypy` par exemple).

**Avant :**
```python
def get_dataframe(start_date, end_date):
    ...
```

**Après (Pro) :**
```python
from datetime import date
import pandas as pd

def get_dataframe(start_date: date, end_date: date) -> pd.DataFrame:
    ...
```

## 2. Documentation (Docstrings)
Adopter le standard **Google Style Python Docstrings** pour toutes les fonctions et classes.

```python
def compute_compliance(sub_df: pd.DataFrame, t_dur: float, t_deep: int) -> dict:
    """Calcule les indicateurs de respect des objectifs de sommeil.

    Args:
        sub_df (pd.DataFrame): Le sous-ensemble de données à analyser.
        t_dur (float): L'objectif de durée (heures).
        t_deep (int): L'objectif de sommeil profond (%).

    Returns:
        dict: Un dictionnaire contenant les moyennes et pourcentages de succès.
    """
```

## 3. Gestion des Erreurs et Logs
Remplacer les `print()` et certains `st.error()` génériques par un vrai système de logging.

- Créer un module `logger.py`.
- Utiliser `logging.getLogger(__name__)`.
- Définir des exceptions personnalisées (ex: `GarminAuthError`, `DataFetchError`).

## 4. Tests Unitaires (Pytest)
Mettre en place une suite de tests pour fiabiliser le code, notamment la logique de transformation de données.

- **Tests de `GarminClient`** : Mocker les appels API.
- **Tests de `DataManager`** : Vérifier le chargement/sauvegarde du cache et le merge des données.
- **Tests de `visualizations`** : Vérifier que les fonctions retournent bien des objets `plotly.graph_objects.Figure`.

Structure cible :
```text
tests/
  ├── test_client.py
  ├── test_data_manager.py
  └── test_visualizations.py
```

## 5. Validation de Données (Pydantic)
Utiliser **Pydantic** pour valider la structure des données (settings, entrées journal, réponse API) plutôt que des dictionnaires bruts.

```python
from pydantic import BaseModel

class SleepObjective(BaseModel):
    target_duration: float
    target_deep_pct: int
    target_bedtime: str
```

## 6. Intégration Continue (CI/CD)
Si le projet était sur GitHub/GitLab :
- Automatiser le linting (`ruff`, `black`).
- Lancer les tests automatiquement à chaque commit.

## 7. Optimisation de l'Interface (UI/UX Avancé)
- **State Management** : Centraliser l'état de l'application dans une classe `AppState` unique pour éviter la dispersion des clés `st.session_state`.
- **Composants Réutilisables** : Extraire les cards, les KPIs et les graphiques dans des composants UI génériques.

---

### Prochaine étape recommandée
Commencer par le point **1 (Typage)** et **2 (Documentation)** sur le module `utils.py` et `data_manager.py` pour sécuriser le cœur de l'application.
