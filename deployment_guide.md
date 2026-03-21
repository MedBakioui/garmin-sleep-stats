# Guide de Déploiement - Garmin Sleep Stats

Ce guide explique comment déployer votre application sur **Streamlit Community Cloud** (recommandé) ou via **Docker**.

## Option 1 : Streamlit Community Cloud (Gratuit & Simple)

1. **Hébergement Git** : Poussez votre code sur un dépôt GitHub (public ou privé).
2. **Connexion** : Allez sur [share.streamlit.io](https://share.streamlit.io/) et connectez votre compte GitHub.
3. **Nouveau App** : Sélectionnez votre dépôt, la branche (ex: `main`), et le fichier principal (`app.py`).
4. **Configuration des Secrets** (CRITIQUE) :

    * **Dans les paramètres de l'application sur Streamlit Cloud, allez dans **Secrets**.
    * **Copiez-collez le contenu de votre fichier `.streamlit/secrets.toml` local.
    * **Ajoutez également votre clé DeepSeek : `DEEPSEEK_KEY = "votre_cle_ici"`.
    * **Optionnel (Connexion Auto)** : Pour ne plus avoir à vous connecter manuellement à Garmin, ajoutez :

        ```toml
        GARMIN_EMAIL = "votre@email.com"
        GARMIN_PASSWORD = "votre_mot_de_passe"
        ```

## Option 2 : Railway (Recommandé pour éviter 429)

Railway est excellent car il utilise des adresses IP moins "marquées" que Streamlit Cloud et supporte nativement Docker.

1.  **Nouveau Projet** : Connectez votre GitHub sur [Railway.app](https://railway.app/).
2.  **Déploiement** : Railway détectera automatiquement le `Dockerfile`.
3.  **Variables d'Environnement** : Allez dans l'onglet **Variables** et ajoutez toutes vos clés (GARMIN_EMAIL, DEEPSEEK_KEY, etc.).
4.  **Persistent Volume** : Pour sauvegarder vos données sans Supabase, allez dans **Settings > Volumes** et montez un dossier sur `/app/data`.

## Option 3 : Render (Gratuit et Privé)

1. **New Web Service** : Connectez GitHub sur [Render.com](https://render.com/).
2. **Configuration** : Render utilisera le fichier `render.yaml` automatiquement.
3. **Secret URL** : Lors de la création, choisissez un nom de service imprévisible (ex: `stats-sleep-88x2-xyz`). Cela rendra votre site "invisible" pour les inconnus.
4. **Environment Variables** : Ajoutez vos secrets (GARMIN_EMAIL, GARMIN_PASSWORD, ACCESS_CODE, TOTP_SECRET) dans le dashboard Render.
5. **Prévention 429** : **TRÈS IMPORTANT** : Une fois que vous avez réussi une première connexion, récupérez le contenu de `garmin_session.json` et ajoutez-le dans une variable `GARMIN_SESSION` sur Render. Cela évitera tout blocage futur.
6. **Note** : Le mode gratuit s'endort après 15 min d'inactivité. Le premier chargement prendra ~30 secondes.

## Option 4 : Déploiement Docker (Auto-hébergé)

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
