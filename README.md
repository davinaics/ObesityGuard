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

---

## 🚀 Setup & Menjalankan

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Tambahkan model
Taruh file berikut di root folder:
- `model.pkl` – Random Forest model terlatih
- `label_encoder.pkl` – LabelEncoder untuk 7 kelas obesitas

### 3. Setup Supabase

1. Buat project di [supabase.com](https://supabase.com)
2. Aktifkan **Email Auth** di Authentication → Providers
3. Jalankan `supabase_schema.sql` di SQL Editor
4. Salin **Project URL** dan **anon key** dari Settings → API

### 4. Konfigurasi secrets
Edit `.streamlit/secrets.toml`:
```toml
[supabase]
url      = "https://YOUR_PROJECT_ID.supabase.co"
anon_key = "eyJhbGci..."
```

### 5. Jalankan aplikasi
```bash
streamlit run app.py
```

---

## 🔑 Fitur

| Fitur | Detail |
|---|---|
| **Auth** | Login & Register via Supabase Auth |
| **Prediksi** | 7 kelas obesitas dengan confidence score |
| **Rekomendasi** | Makanan dari DB per kategori, bisa di-refresh |
| **Simpan** | Hasil disimpan ke `health_logs` per user |
| **Dashboard** | Berat, BMI, faktor analisis, riwayat klasifikasi |

---

## 🏗️ Model Features

Model dilatih dengan 7 fitur:

| Kolom | Keterangan |
|---|---|
| `Age` | Usia (tahun) |
| `Height` | Tinggi badan (cm) |
| `Weight` | Berat badan (kg) |
| `FAF` | Frekuensi aktivitas fisik (0–3) |
| `FCVC` | Frekuensi konsumsi sayur (1–3) |
| `CH2O` | Konsumsi air (1–3) |
| `NCP` | Jumlah makan utama (default=3) |

---

## 🏷️ Label Kelas

| Kelas | Tampilan |
|---|---|
| `Insufficient_Weight` | Berat Badan Kurang |
| `Normal_Weight` | Berat Badan Normal |
| `Overweight_Level_I` | Kelebihan Berat I |
| `Overweight_Level_II` | Kelebihan Berat II |
| `Obesity_Type_I` | Obesitas Tipe I |
| `Obesity_Type_II` | Obesitas Tipe II |
| `Obesity_Type_III` | Obesitas Tipe III |
