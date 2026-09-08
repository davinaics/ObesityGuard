"""
Halaman Prediksi: form input, inferensi model, hasil, XAI SHAP, simpan.
"""

import math
import streamlit as st
from utils.ml import (
    predict,
    get_prediction_color_class,
    get_prediction_icon,
    LABEL_DISPLAY,
    predict_lifestyle_persona,
    load_all_artifacts,
    generate_shap_plot
)
from utils.supabase_client import get_supabase_client # IMPORT SUPABASE

# ── KAMUS TRANSLASI UI (TAMPILAN) ──
MAP_YESNO = {"no": "Tidak", "yes": "Ya"}
MAP_FREQ = {"no": "Tidak Pernah", "Sometimes": "Kadang-kadang", "Frequently": "Sering", "Always": "Selalu"}
MAP_FCVC = {1.0: "Tidak pernah", 2.0: "Kadang-kadang", 3.0: "Selalu"}
MAP_NCP = {1.0: "1 kali", 2.0: "2 kali", 3.0: "3 kali", 4.0: "4 kali"}
MAP_CH2O = {1.0: "Kurang dari 1 Liter", 2.0: "Antara 1 hingga 2 Liter", 3.0: "Lebih dari 2 Liter"}
MAP_FAF = {0.0: "Tidak pernah", 1.0: "1 atau 2 hari", 2.0: "2 atau 4 hari", 3.0: "4 atau 5 hari"}
MAP_TUE = {0.0: "0 hingga 2 jam", 1.0: "3 hingga 5 jam", 2.0: "Lebih dari 5 jam"}
MAP_MTRANS = {"Automobile": "Mobil Pribadi", "Motorbike": "Sepeda Motor", "Public_Transportation": "Kendaraan Umum", "Bike": "Sepeda", "Walking": "Jalan Kaki"}

# ── HELPER TARIK DATA PROFIL ──
def _get_user_profile(user_id: str):
    """Fungsi diam-diam untuk menarik data statis user dari tabel profiles."""
    supabase = get_supabase_client()
    try:
        resp = supabase.table("profiles").select("*").eq("id", user_id).execute()
        if resp.data:
            return resp.data[0]
        return None
    except Exception as e:
        return None


def show_prediksi_page():
    st.markdown('<div class="page-header"><h1>🔍 Form Pemantauan Obesitas</h1><p>Evaluasi kondisi fisik dan gaya hidup Anda saat ini</p></div>', unsafe_allow_html=True)

    # 1. Ambil data profil user yang sedang login
    user_id = st.session_state.get("user_id", "")
    profile = _get_user_profile(user_id)

    # Proteksi kalau user belum punya profil 
    if not profile:
        st.warning("⚠️ Data profil fisik Anda belum lengkap. Silakan logout dan buat akun baru untuk pengalaman maksimal.")
        return

    # Tampilkan banner info yang elegan
    disp_gender = "Laki-laki" if profile['gender'] == "Male" else "Perempuan"
    st.info(f"👤 **Menganalisis untuk:** {disp_gender}, {profile['age']} tahun, Tinggi {profile['height']} m. *(Data ditarik otomatis dari profil Anda)*")

    with st.form("form_prediksi", clear_on_submit=False):
        # ── 1. BAGIAN BERAT BADAN SAAT INI ──
        st.markdown('<div class="section-title">⚖️ Berat Badan Saat Ini</div>', unsafe_allow_html=True)
        weight = st.number_input("Masukkan Berat Badan Terbaru (kg)", min_value=30.0, max_value=200.0, value=None, step=0.5)

        # ── 2. BAGIAN KEBIASAAN GAYA HIDUP DINAMIS ──
        st.markdown('<div class="section-title">🥗 Pola Makan & Aktivitas Harian</div>', unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            favc = st.radio("Sering makan kalori tinggi (Gorengan/Manis)?", options=MAP_YESNO.keys(), format_func=lambda x: MAP_YESNO[x], index=None)
            fcvc = st.selectbox("Frekuensi makan sayur?", options=MAP_FCVC.keys(), format_func=lambda x: MAP_FCVC[x], index=None)
            ncp = st.selectbox("Berapa kali makan besar sehari?", options=MAP_NCP.keys(), format_func=lambda x: MAP_NCP[x], index=None)
            caec = st.selectbox("Sering ngemil di antara jam makan?", options=MAP_FREQ.keys(), format_func=lambda x: MAP_FREQ[x], index=None)
            smoke = st.radio("Apakah Anda merokok?", options=MAP_YESNO.keys(), format_func=lambda x: MAP_YESNO[x], index=None)
            faf = st.selectbox("Frekuensi aktivitas fisik / olahraga?", options=MAP_FAF.keys(), format_func=lambda x: MAP_FAF[x], index=None)
            
        with col4:
            ch2o = st.selectbox("Berapa banyak minum air putih sehari?", options=MAP_CH2O.keys(), format_func=lambda x: MAP_CH2O[x], index=None)
            scc = st.radio("Suka memantau asupan kalori harian?", options=MAP_YESNO.keys(), format_func=lambda x: MAP_YESNO[x], index=None)
            calc = st.selectbox("Frekuensi konsumsi alkohol?", options=MAP_FREQ.keys(), format_func=lambda x: MAP_FREQ[x], index=None)
            tue = st.selectbox("Durasi pakai perangkat teknologi?", options=MAP_TUE.keys(), format_func=lambda x: MAP_TUE[x], index=None)
            mtrans = st.selectbox("Moda transportasi utama?", options=MAP_MTRANS.keys(), format_func=lambda x: MAP_MTRANS[x], index=None)

        submitted = st.form_submit_button("🤖 Analisis Sekarang", use_container_width=True)

        if submitted:
            # Pengecekan agar tidak ada kotak dinamis yang kosong
            inputs = [weight, favc, fcvc, ncp, caec, smoke, ch2o, scc, faf, tue, calc, mtrans]
            if None in inputs:
                st.error("⚠️ Ups! Mohon isi dan pilih SEMUA kotak pertanyaan sebelum melakukan analisis ya!")
            else:
                # MERGER DATA: 4 Data Profil + 12 Data Form 
                snapshot = {
                    "gender": profile["gender"], 
                    "age": profile["age"], 
                    "height": float(profile["height"]), 
                    "family_history": profile["family_history"],
                    "weight": weight, "favc": favc, "fcvc": fcvc, 
                    "ncp": ncp, "caec": caec, "smoke": smoke, "ch2o": ch2o, 
                    "scc": scc, "faf": faf, "tue": tue, "calc": calc, "mtrans": mtrans 
                }
                st.session_state["input_snapshot"] = snapshot
                
                with st.spinner("Memproses analisis..."):
                    result = predict(snapshot)

                st.session_state["prediction_result"] = result
                st.session_state["is_saved"] = False

    # ── Tampilkan Hasil Utama ──────────────────────────────────────────────────
    result = st.session_state.get("prediction_result")
    if result is None: return

    _show_prediction_result(result)

    # ── Tampilkan Analisis XAI (SHAP) ──────────────────────────────────────────
    snapshot = st.session_state.get("input_snapshot")
    _show_xai_analysis(result, snapshot)

    _show_save_section(result)


# ── Sub-renderers (Tidak ada perubahan, otomatis menerima snapshot komplit) ──
def _show_prediction_result(result: dict):
    color, icon, display, conf = get_prediction_color_class(result["label"]), get_prediction_icon(result["label"]), result["display"], result["confidence"]
    st.markdown('<div class="section-title">📊 Hasil Klasifikasi & Segmentasi</div>', unsafe_allow_html=True)
    
    col_pred, col_proba = st.columns([1, 1.3])

    with col_pred:
        st.markdown(f"""
            <div class="pred-card pred-card-{color}">
                <div class="pred-icon">{icon}</div>
                <div class="pred-label pred-{color}">{display}</div>
                <div class="pred-conf">Tingkat Keyakinan: <b>{conf:.1f}%</b></div>
            </div>""", unsafe_allow_html=True)

    with col_proba:
        html_content = '<div class="card"><div class="card-title">📈 Probabilitas Tingkat Obesitas</div>'
        for cls, prob in sorted(result["probas"].items(), key=lambda x: x[1], reverse=True):
            is_top = cls == result["label"]
            if is_top: 
                if cls == "Insufficient_Weight": bar_color, text_color = ("#42A5F5", "#1565C0") 
                elif cls == "Normal_Weight": bar_color, text_color = ("#4CAF50", "#2E7D32") 
                elif cls in ("Overweight_Level_I", "Overweight_Level_II"): bar_color, text_color = ("#F9A825", "#F57F17") 
                else: bar_color, text_color = ("#E53935", "#B71C1C") 
            else: 
                bar_color, text_color = "#BDBDBD", "#757575"
                
            html_content += f"""<div style="margin-bottom:10px;"><div style="display:flex;justify-content:space-between;font-size:13px;font-weight:{"700" if is_top else "400"};color:{text_color};"><span>{"▶ " if is_top else ""}{LABEL_DISPLAY.get(cls, cls)}</span><span>{prob:.1f}%</span></div><div style="background:#E0E0E0;border-radius:4px;height:8px;margin-top:4px;"><div style="background:{bar_color};width:{prob:.1f}%;height:8px;border-radius:4px;"></div></div></div>"""
        html_content += '</div>'
        st.markdown(html_content, unsafe_allow_html=True)

    # Memanggil model K-Means
    user_data = st.session_state.get("input_snapshot")
    persona_info = predict_lifestyle_persona(user_data)
    
    if persona_info["cluster"] is not None:
        
        # Card Persona ──
        cluster_id = persona_info["cluster"]
        
        # Pisahkan warna per klaster biar konsisten dengan Progress Bar
        if cluster_id == 0:
            # Persona 0: Si Mager (Merah)
            k_class = "red"
            t_color = "#B71C1C"
        elif cluster_id == 1:
            # Persona 1: Si Transum (Oranye/Kuning)
            k_class = "yellow"
            t_color = "#F9A825" 
        else:
            # Persona 2: Si Sehat (Hijau)
            k_class = "green"
            t_color = "#2E7D32"

        st.markdown(f"""
        <div class="pred-card pred-card-{k_class}" style="text-align: left; padding: 24px; margin-top: 16px;">
            <div style="font-size: 12px; color: {t_color}; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px; opacity: 0.8;">🧬 Profil Persona Gaya Hidup</div>
            <div style="font-size: 22px; font-weight: 800; color: {t_color}; margin-bottom: 8px;">{persona_info['persona']}</div>
            <div style="font-size: 14.5px; color: #424242; line-height: 1.6; font-weight: 500;">{persona_info['desc']}</div>
        </div>""", unsafe_allow_html=True)

def _show_xai_analysis(result, snapshot):
    st.markdown('<div class="section-title">🧠 Mengapa Anda Divonis Demikian? (SHAP Waterfall Plot)</div>', unsafe_allow_html=True)
    
    # ── Teks Info SHAP dibuat Minimalis ──
    st.markdown("""
        <div style="font-size: 13.5px; color: #616161; line-height: 1.6; margin-bottom: 20px;">
            <i>💡 <b>Cara Membaca Grafik:</b> Batang yang mengarah ke Kanan (Merah) adalah faktor kebiasaan yang mendorong Anda ke arah vonis saat ini. Sedangkan batang yang mengarah ke Kiri (Biru) adalah faktor yang menahan/mencegah Anda dari vonis tersebut.</i>
        </div>
    """, unsafe_allow_html=True)

    with st.spinner("Membedah logika AI..."):
        try:
            artifacts = load_all_artifacts()
            shap_fig = generate_shap_plot(artifacts["rf_model"], result["X_final_df"], result['label'], artifacts["encoding_rules"])
            st.pyplot(shap_fig)
        except Exception as e:
            st.error(f"⚠️ Terjadi kesalahan saat memuat grafik SHAP: {e}")

def _show_save_section(result: dict):
    st.markdown('<div class="section-title">💾 Simpan Hasil Pemantauan</div>', unsafe_allow_html=True)
    snapshot = st.session_state.get("input_snapshot", {})
    if not snapshot: return

    col_save, col_info = st.columns([1, 2])
    with col_save:
        if st.button("💾 Simpan ke Riwayat", use_container_width=True, key="btn_save"):
            from utils.database import save_health_log
            if save_health_log(st.session_state.get("user_id", ""), snapshot, result["label"]):
                st.success("✅ Hasil pemantauan berhasil disimpan ke Database!")
                st.session_state["is_saved"] = True

    with col_info:
        if result["label"] == "Insufficient_Weight": res_color = "#1565C0"
        elif result["label"] == "Normal_Weight": res_color = "#2E7D32" 
        elif result["label"] in ("Overweight_Level_I", "Overweight_Level_II"): res_color = "#F57F17" 
        else: res_color = "#B71C1C" 
        
        disp_gender = "Laki-laki" if snapshot.get('gender') == "Male" else "Perempuan" if snapshot.get('gender') == "Female" else "–"
        disp_fh = MAP_YESNO.get(snapshot.get('family_history'), "–")
        disp_favc = MAP_YESNO.get(snapshot.get('favc'), "–")
        disp_fcvc = MAP_FCVC.get(snapshot.get('fcvc'), "–")
        disp_ncp = MAP_NCP.get(snapshot.get('ncp'), "–")
        disp_caec = MAP_FREQ.get(snapshot.get('caec'), "–")
        disp_smoke = MAP_YESNO.get(snapshot.get('smoke'), "–")
        disp_ch2o = MAP_CH2O.get(snapshot.get('ch2o'), "–")
        disp_scc = MAP_YESNO.get(snapshot.get('scc'), "–")
        disp_calc = MAP_FREQ.get(snapshot.get('calc'), "–")
        disp_faf = MAP_FAF.get(snapshot.get('faf'), "–")
        disp_tue = MAP_TUE.get(snapshot.get('tue'), "–")
        disp_mtrans = MAP_MTRANS.get(snapshot.get('mtrans'), "–")

        st.markdown(f"""
            <div class="card">
                <div class="card-title">📋 Ringkasan Data Pemantauan</div>
                <table style="width:100%;font-size:13px;border-collapse:collapse;">
                    <tr><td style="color:#757575;padding:4px 0;">Jenis Kelamin</td><td style="font-weight:600;text-align:right;">{disp_gender}</td></tr>
                    <tr><td style="color:#757575;padding:4px 0;">Usia</td><td style="font-weight:600;text-align:right;">{snapshot.get('age', '–')} tahun</td></tr>
                    <tr><td style="color:#757575;padding:4px 0;">Tinggi / Berat Badan</td><td style="font-weight:600;text-align:right;">{snapshot.get('height', '–')} m / {snapshot.get('weight', '–')} kg</td></tr>
                    <tr><td style="color:#757575;padding:4px 0;">Riwayat Genetik Obesitas</td><td style="font-weight:600;text-align:right;">{disp_fh}</td></tr>
                    <tr><td colspan="2" style="padding-top:8px;"><hr style="margin:4px 0; border:none; border-top:1px dashed #E0E0E0;"></td></tr>
                    <tr><td style="color:#757575;padding:4px 0;">Makan Berkalori Tinggi</td><td style="font-weight:600;text-align:right;">{disp_favc}</td></tr>
                    <tr><td style="color:#757575;padding:4px 0;">Makan Sayur</td><td style="font-weight:600;text-align:right;">{disp_fcvc}</td></tr>
                    <tr><td style="color:#757575;padding:4px 0;">Jumlah Makan Besar</td><td style="font-weight:600;text-align:right;">{disp_ncp}</td></tr>
                    <tr><td style="color:#757575;padding:4px 0;">Ngemil</td><td style="font-weight:600;text-align:right;">{disp_caec}</td></tr>
                    <tr><td style="color:#757575;padding:4px 0;">Konsumsi Air Putih</td><td style="font-weight:600;text-align:right;">{disp_ch2o}</td></tr>
                    <tr><td style="color:#757575;padding:4px 0;">Pantau Kalori Harian</td><td style="font-weight:600;text-align:right;">{disp_scc}</td></tr>
                    <tr><td style="color:#757575;padding:4px 0;">Konsumsi Alkohol</td><td style="font-weight:600;text-align:right;">{disp_calc}</td></tr>
                    <tr><td style="color:#757575;padding:4px 0;">Merokok</td><td style="font-weight:600;text-align:right;">{disp_smoke}</td></tr>
                    <tr><td style="color:#757575;padding:4px 0;">Olahraga / Aktivitas Fisik</td><td style="font-weight:600;text-align:right;">{disp_faf}</td></tr>
                    <tr><td style="color:#757575;padding:4px 0;">Screen Time</td><td style="font-weight:600;text-align:right;">{disp_tue}</td></tr>
                    <tr><td style="color:#757575;padding:4px 0;">Transportasi Utama</td><td style="font-weight:600;text-align:right;">{disp_mtrans}</td></tr>
                    <tr><td style="color:#757575;padding:12px 0 8px;border-top:1px solid #E0E0E0;">Status Obesitas</td><td style="font-weight:800;color:{res_color};text-align:right;font-size:15px;padding:12px 0 8px;border-top:1px solid #E0E0E0;">{result['display']}</td></tr>
                </table>
            </div>""", unsafe_allow_html=True)