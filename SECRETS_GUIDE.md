# Note Importante sur les Secrets Streamlit

Pour garantir une sécurité optimale et un fonctionnement correct de l'application (en local comme en ligne), les clés d'accès à Supabase doivent être gérées via le système de "Secrets" de Streamlit.

## Configuration Locale

Les clés sont stockées dans `.streamlit/secrets.toml`. 
**Ce fichier ne doit jamais être partagé ou ajouté à un dépôt public.**

Contenu requis :
```toml
SUPABASE_URL = "https://yzsinljiwilvkvbnbqzy.supabase.co"
SUPABASE_KEY = "votre_cle_anon_public"
```

## Configuration en Ligne (Déploiement)

Lorsque vous mettrez l'application en ligne sur Streamlit Cloud :
1. Allez dans les paramètres de votre application (**Settings**).
2. Cherchez l'onglet **Secrets**.
3. Copiez-collez le contenu de votre `secrets.toml` directement dans le champ prévu à cet effet.

Cela permettra à l'application de se connecter à la base de données sans que les clés ne soient visibles dans le code source.
