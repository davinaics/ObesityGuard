"""
Supabase client singleton.
Baca kredensial dari st.secrets atau environment variable.
"""

import streamlit as st
from supabase import create_client, Client


@st.cache_resource(show_spinner=False)
def get_supabase_client() -> Client:
    """
    Kembalikan Supabase client (di-cache agar tidak re-inisialisasi setiap rerun).

    Tambahkan ke .streamlit/secrets.toml:
        [supabase]
        url = "https://xxxx.supabase.co"
        anon_key = "eyJhbGci..."
    """
    url: str = st.secrets["supabase"]["url"]
    key: str = st.secrets["supabase"]["anon_key"]
    return create_client(url, key)
