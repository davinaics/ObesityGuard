"""
Authentication helpers: init session, login page (login + register), logout.
"""

import streamlit as st
from utils.supabase_client import get_supabase_client

# ── Session Init ──────────────────────────────────────────────────────────────
def init_session():
    """Pastikan semua key session_state tersedia."""
    defaults = {
        "logged_in": False,
        "user_id": None,
        "email": None,
        "prediction_result": None,
        "recommendations": None,
        "rec_refresh_key": 0,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ── Login Page ────────────────────────────────────────────────────────────────
def login_page():
    """Render halaman login / register (belum terautentikasi)."""
    st.markdown(
        """
        <div class="auth-container">
            <div class="auth-logo">🩺🍔🏋️‍♀️</div>
            <h1 class="auth-title">ObesityGuard</h1>
            <p class="auth-subtitle">Klasifikasi &amp; Monitoring Obesitas<br>Berbasis Machine Learning</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_center = st.columns([1, 1.6, 1])[1] # Diperlebar sedikit agar form daftar rapi

    with col_center:
        tab_login, tab_register = st.tabs(["🔐 Login", "📝 Daftar"])

        # ── Tab Login ─────────────────────────────────────────────────────────
        with tab_login:
            with st.form("form_login"):
                st.markdown("### Masuk ke Akun")
                email = st.text_input("Email", placeholder="contoh@email.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                submitted = st.form_submit_button("🔐 Login", use_container_width=True)

            if submitted:
                _do_login(email, password)

        # ── Tab Register ──────────────────────────────────────────────────────
        with tab_register:
            with st.form("form_register"):
                st.markdown("### Buat Akun")
                
                # Data Akun
                st.markdown("**1. Data Akun**")
                reg_email = st.text_input("Email", placeholder="contoh@email.com", key="reg_email")
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    reg_password = st.text_input("Password (min 6 char)", type="password", key="reg_pass")
                with col_p2:
                    reg_confirm = st.text_input("Konfirmasi Password", type="password", key="reg_confirm")
                
                st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
                
                # Data Profil Kesehatan (Statis)
                st.markdown("**2. Data Fisik & Genetik**")
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    gender = st.selectbox("Jenis Kelamin", options=["Female", "Male"], index=None, placeholder="Pilih Jenis Kelamin...")
                    age = st.number_input("Umur", min_value=10, max_value=100, value=None, step=1)
                with col_f2:
                    height = st.number_input("Tinggi Badan (m, contoh: 1.65)", min_value=1.00, max_value=2.50, value=None, step=0.01)
                    family_history = st.radio("Ada keluarga riwayat obesitas?", options=["no", "yes"], format_func=lambda x: "Tidak" if x=="no" else "Ya", index=None)
                
                reg_submitted = st.form_submit_button("📝 Daftar & Simpan Profil", use_container_width=True)

            if reg_submitted:
                _do_register(reg_email, reg_password, reg_confirm, gender, age, height, family_history)


# ── Internal helpers ──────────────────────────────────────────────────────────
def _do_login(email: str, password: str):
    if not email or not password:
        st.error("Email dan password wajib diisi.")
        return
    try:
        supabase = get_supabase_client()
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = response.user
        if user:
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user.id
            st.session_state["email"] = user.email
            st.success("Login berhasil! Selamat datang 👋")
            st.rerun()
        else:
            st.error("Login gagal. Periksa email & password.")
    except Exception as e:
        err_msg = str(e)
        if "Invalid login credentials" in err_msg:
            st.error("Email atau password salah.")
        else:
            st.error(f"Login error: {err_msg}")


def _do_register(email: str, password: str, confirm: str, gender: str, age: int, height: float, family_history: str):
    if not email or not password or not confirm:
        st.error("Data akun (Email & Password) wajib diisi.")
        return
    if password != confirm:
        st.error("Password tidak cocok.")
        return
    if len(password) < 6:
        st.error("Password minimal 6 karakter.")
        return
    if gender is None or age is None or height is None or family_history is None:
        st.error("Semua Data Fisik & Genetik wajib diisi.")
        return
        
    try:
        supabase = get_supabase_client()
        # 1. Daftarkan Akun ke Supabase Auth
        response = supabase.auth.sign_up({"email": email, "password": password})
        
        if response.user:
            # 2. Simpan Data Profil ke Tabel 'profiles'
            profile_data = {
                "id": response.user.id,
                "gender": gender,
                "age": age,
                "height": height,
                "family_history": family_history
            }
            supabase.table("profiles").insert(profile_data).execute()
            
            st.success("✅ Registrasi berhasil disimpan! Silakan Login.")
        else:
            st.error("Registrasi gagal. Coba lagi.")
    except Exception as e:
        err_msg = str(e)
        if "already registered" in err_msg:
            st.error("Email sudah terdaftar. Silakan login.")
        else:
            st.error(f"Registrasi error: {err_msg}")