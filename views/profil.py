"""
Halaman Profil: Untuk melihat dan mengedit data statis user (Umur, Tinggi, dsb).
"""

import streamlit as st
from utils.supabase_client import get_supabase_client

def show_profil_page():
    st.markdown(
        """
        <div class="page-header">
            <h1>👤 Profil Saya</h1>
            <p>Kelola data fisik dan riwayat genetik Anda di sini</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("⚠️ Sesi tidak valid. Silakan login ulang.")
        return

    supabase = get_supabase_client()

    # ── 1. AMBIL DATA DARI DATABASE (READ) ──
    try:
        resp = supabase.table("profiles").select("*").eq("id", user_id).execute()
        profil_data = resp.data[0] if resp.data else None
    except Exception as e:
        st.error(f"Gagal menarik data profil: {e}")
        return

    if not profil_data:
        st.warning("Data profil belum lengkap. Silakan lengkapi data Anda.")
        return

    # ── 2. TAMPILKAN FORM EDIT (UPDATE) ──
    # Menentukan nilai index default berdasarkan data dari database
    gender_idx = 0 if profil_data.get("gender") == "Female" else 1
    fh_idx = 1 if profil_data.get("family_history") == "yes" else 0
    
    with st.form("form_edit_profil"):
        st.markdown('<div class="section-title" style="margin-top:0;">✏️ Edit Data Fisik & Genetik</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            new_gender = st.selectbox("Jenis Kelamin", options=["Female", "Male"], index=gender_idx)
            new_age = st.number_input("Umur", min_value=10, max_value=100, value=int(profil_data.get("age", 20)), step=1)
        
        with col2:
            new_height = st.number_input("Tinggi Badan (m)", min_value=1.00, max_value=2.50, value=float(profil_data.get("height", 1.60)), step=0.01)
            new_fh = st.radio("Ada keluarga riwayat obesitas?", options=["no", "yes"], format_func=lambda x: "Tidak" if x=="no" else "Ya", index=fh_idx)

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("💾 Simpan Perubahan", use_container_width=True)

        if submitted:
            try:
                # Paketkan data yang baru
                update_data = {
                    "gender": new_gender,
                    "age": new_age,
                    "height": new_height,
                    "family_history": new_fh
                }
                # Update ke Supabase
                supabase.table("profiles").update(update_data).eq("id", user_id).execute()
                
                st.success("✅ Yay! Profil kamu berhasil diperbarui!")
                st.rerun() # Refresh halaman biar datanya langsung berubah
                
            except Exception as e:
                st.error(f"Gagal memperbarui profil: {e}")