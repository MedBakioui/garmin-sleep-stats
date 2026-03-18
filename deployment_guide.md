# Guide de Déploiement - Garmin Sleep Stats

Ce guide explique comment déployer votre application sur **Streamlit Community Cloud** (recommandé) ou via **Docker**.

## Option 1 : Streamlit Community Cloud (Gratuit & Simple)

1.  **Hébergement Git** : Poussez votre code sur un dépôt GitHub (public ou privé).
2.  **Connexion** : Allez sur [share.streamlit.io](https://share.streamlit.io/) et connectez votre compte GitHub.
3.  **Nouveau App** : Sélectionnez votre dépôt, la branche (ex: `main`), et le fichier principal (`app.py`).
4.  **Configuration des Secrets** (CRITIQUE) :
    *   Dans les paramètres de l'application sur Streamlit Cloud, allez dans **Secrets**.
    *   Copiez-collez le contenu de votre fichier `.streamlit/secrets.toml` local.
    *   Ajoutez également votre clé DeepSeek : `DEEPSEEK_KEY = "votre_cle_ici"`.

## Option 2 : Déploiement Docker (Auto-hébergé)

Si vous avez votre propre serveur avec Docker :

1.  **Build de l'image** :
    ```bash
    docker build -t garmin-sleep-stats .
    ```
2.  **Lancement du conteneur** :
    ```bash
    docker run -p 8501:8501 --name sleep-stats garmin-sleep-stats
    ```
3.  **Persistance** : Utilisez un volume pour les fichiers JSON si vous n'utilisez pas Supabase pour tout.

## Sécurité et 2FA

*   **ACCESS_CODE** : C'est votre premier rempart. Changez-le dans les secrets avant de déployer.
*   **TOTP_SECRET** : C'est la clé de votre Google Authenticator. Ne la partagez jamais. Si vous la perdez, vous devrez la réinitialiser dans les secrets de déploiement et rescanner le QR Code.
*   **Supabase** : Assurez-vous que vos clés Supabase sont bien renseignées dans les secrets cloud pour la persistance des données longues durées.

## Dépendances

L'application utilise `requirements.txt` pour installer automatiquement :
- `garminconnect` : Pour les données Garmin.
- `pyotp` & `qrcode` : Pour la sécurité 2FA.
- `supabase` : Pour la base de données.
- `openai` / `python-dotenv` : Pour l'IA.
