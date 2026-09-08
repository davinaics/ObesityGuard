"""
Klasifikasi dan Monitoring Obesitas Berdasarkan Aktivitas Fisik dan Pola Makan
Menggunakan Random Forest
"""

import streamlit as st
from utils.auth import init_session, login_page
from utils.styles import inject_global_css
from utils.supabase_client import get_supabase_client
from views.prediksi import show_prediksi_page
from views.dashboard import show_dashboard_page
from views.profil import show_profil_page  

# ── Page config (WAJIB paling atas) ──────────────────────────────────────────
st.set_page_config(
    page_title="ObesityGuard – Klasifikasi Obesitas",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject CSS global ─────────────────────────────────────────────────────────
inject_global_css()

# ── Inisialisasi session ──────────────────────────────────────────────────────
init_session()


def show_sidebar():
    """Render sidebar: navigasi + info user + logout."""
    with st.sidebar:
        # ── Logo / judul ─────────────────────────────────────────────────────
        st.markdown(
            """
            <div class="sidebar-header">
                <div class="sidebar-logo">🩺</div>
                <div class="sidebar-title">ObesityGuard</div>
                <div class="sidebar-subtitle">Health Monitoring System</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # ── Info user ─────────────────────────────────────────────────────────
        email = st.session_state.get("email", "")
        st.markdown(
            f"""
            <div class="user-info-card">
                <div class="user-avatar">👤</div>
                <div class="user-email">{email}</div>
                <div class="user-status">● Online</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # ── Navigasi ──────────────────────────────────────────────────────────
        st.markdown('<p class="sidebar-nav-label">MENU UTAMA</p>', unsafe_allow_html=True)

        # 🔥 TAMBAHAN BARU: Nambahin tombol Profil di menu samping
        menu_options = {
            "🔍 Prediksi": "prediksi",
            "📊 Dashboard": "dashboard",
            "👤 Profil Saya": "profil", 
        }

        selected_label = st.radio(
            "Navigasi",
            list(menu_options.keys()),
            label_visibility="collapsed",
        )
        active_page = menu_options[selected_label]

        st.markdown("---")

        # ── Logout ────────────────────────────────────────────────────────────
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            supabase = get_supabase_client()
            try:
                supabase.auth.sign_out()
            except Exception:
                pass
            for key in ["user_id", "email", "logged_in", "prediction_result", "recommendations", "input_snapshot", "rec_refresh_key", "is_saved"]:
                st.session_state.pop(key, None)
            st.rerun()

    return active_page


def main():
    # ── Guard: belum login → tampilkan halaman login ──────────────────────────
    if not st.session_state.get("logged_in", False):
        login_page()
        return

    # ── Sudah login → tampilkan aplikasi utama ────────────────────────────────
    active_page = show_sidebar()

    # 🔥 TAMBAHAN BARU: Jalankan halaman sesuai menu yang diklik
    if active_page == "prediksi":
        show_prediksi_page()
    elif active_page == "dashboard":
        show_dashboard_page()
    elif active_page == "profil":
        show_profil_page()


if __name__ == "__main__":
    main()