# 🩺 ObesityGuard – Klasifikasi & Monitoring Obesitas

Aplikasi Streamlit production-ready untuk klasifikasi obesitas menggunakan **Random Forest**, berbasis aktivitas fisik dan pola makan harian.

---

## 📦 Struktur Proyek

```
obesity_app/
├── app.py                        # Entry point
├── requirements.txt
├── model.pkl                     # ⚠️ Taruh di sini
├── label_encoder.pkl             # ⚠️ Taruh di sini
├── supabase_schema.sql           # SQL untuk setup database
├── .streamlit/
│   └── secrets.toml              # Kredensial Supabase (jangan di-commit)
├── utils/
│   ├── __init__.py
│   ├── auth.py                   # Login, register, logout
│   ├── database.py               # Operasi Supabase (health_logs, food_recommendations)
│   ├── ml.py                     # Load model, prediksi, mapping input
│   ├── styles.py                 # CSS health theme
│   └── supabase_client.py        # Singleton Supabase client
└── pages/
    ├── __init__.py
    ├── prediksi.py               # Halaman prediksi & rekomendasi makanan
    └── dashboard.py              # Halaman monitoring & chart
```

# Sistem Pemantauan Obesitas Berbasis Dual-Pipeline Model & SHAP

Web interaktif berbasis Streamlit yang dirancang untuk melakukan klasifikasi tingkat obesitas, segmentasi gaya hidup, serta transparansi hasil klasifikasi menggunakan SHAP (Shapley Additive Explanations).

---

## Prasyarat Sistem (System Requirements)
Pastikan perangkat Anda telah terinstal perangkat lunak berikut:
- Python (Direkomendasikan versi 3.11 atau yang lebih baru)
- pip (Pengelola paket Python)

---

## Langkah Instalasi & Pengaturan (Installation Guide)

1. Unduh atau Ekstrak Proyek
   Ekstrak folder proyek yang Anda miliki ke direktori pilihan di komputer Anda.

2. Buka Terminal / Command Prompt
   Arahkan direktori terminal ke folder penyimpanan proyek tersebut:
   cd path/ke/folder-proyek

3. Membuat Virtual Environment (Opsional namun Disarankan)
   Untuk menjaga kebersihan pustaka sistem:
   - Windows:
     python -m venv venv
     venv\Scripts\activate
   - macOS / Linux:
     python3 -m venv venv
     source venv/bin/activate

4. Instalasi Pustaka yang Dibutuhkan
   Jalankan perintah berikut untuk menginstal seluruh pustaka yang tercatat dalam berkas konfigurasi:
   pip install -r requirements.txt

---

## Struktur Berkas Proyek (Project Structure)
Berikut adalah susunan direktori utama dari aplikasi ini:
- app.py — Berkas utama untuk menjalankan navigasi dan antarmuka web Streamlit.
- auth.py — Modul untuk menangani autentikasi pengguna (login dan registrasi).
- database.py — Modul untuk mengelola penyimpanan dan pengambilan riwayat kesehatan dari database Supabase.
- ml.py — Modul inti Machine Learning (pemuatan artefak model, inferensi prediksi RF Hybrid Voting Confidence Scaling, klasterisasi K-Means, dan SHAP Waterfall Plot).
- styles.py — Modul untuk menyuntikkan Global Custom CSS.
- supabase_client.py — Berkas konfigurasi untuk menghubungkan aplikasi dengan klien Supabase Cloud.
- dashboard.py — Modul tampilan untuk halaman dasbor monitoring dan grafik riwayat kesehatan.
- prediksi.py — Modul tampilan untuk halaman form input data fisik & gaya hidup serta visualisasi hasil prediksi, klasterisasi, dan SHAP.
- profil.py — Modul tampilan untuk halaman kelola profil pengguna.
- models/ — Folder penyimpanan berkas model .pkl (joblib/pickle) yang telah dilatih (best_rf_model.pkl, tree_weights.pkl, encoding_rules.pkl, model_kmeans.pkl, scaler_kmeans.pkl, dll).
- requirements.txt — Daftar pustaka dan dependensi Python.

---

## Cara Menjalankan Program (How to Run)

1. Pastikan Anda berada di dalam direktori folder proyek dan virtual environment sudah aktif (jika menggunakannya).
2. Jalankan perintah Streamlit berikut di terminal:
   streamlit run app.py
3. Salin tautan lokal (biasanya http://localhost:8501) yang muncul di terminal, lalu buka melalui peramban web (browser) Anda.
