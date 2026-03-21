import streamlit as st
import os

def get_secret(key: str, default: str = None) -> str:
    """
    Get a secret from Streamlit secrets or environment variables.
    This makes the app compatible with Streamlit Cloud (secrets.toml)
    and Render/Railway/Docker (Environment Variables).
    """
    # 1. Try Streamlit context (st.secrets)
    try:
        if key in st.secrets:
            return st.secrets[key]
    except:
        pass
    
    # 2. Try Environment Variables (Render/Docker)
    return os.environ.get(key, default)
