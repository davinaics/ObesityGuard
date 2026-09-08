"""
Machine Learning helpers: load model, encode input, predict.
"""

import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path
import matplotlib.pyplot as plt
import joblib

# ── Label mapping ─────────────────────────────
LABEL_DISPLAY = {
    "Insufficient_Weight": "Berat Badan Kurang",
    "Normal_Weight":       "Berat Badan Normal",
    "Overweight_Level_I":  "Kelebihan Berat I",
    "Overweight_Level_II": "Kelebihan Berat II",
    "Obesity_Type_I":      "Obesitas Tipe I",
    "Obesity_Type_II":     "Obesitas Tipe II",
    "Obesity_Type_III":    "Obesitas Tipe III",
}

# ── Load Semua Model & Artifacts ──────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_all_artifacts():
    artifacts = {}
    base_path = Path("models")
    
    rf_path = base_path / "best_rf_model.pkl"
    if rf_path.exists(): artifacts["rf_model"] = joblib.load(rf_path)
    else: st.error("❌ File best_rf_model.pkl tidak ditemukan!"); st.stop()

    weight_path = base_path / "tree_weights.pkl"
    if weight_path.exists(): artifacts["tree_weights"] = joblib.load(weight_path)
    else: st.error("❌ File tree_weights.pkl tidak ditemukan!"); st.stop()

    rules_path = base_path / "encoding_rules.pkl"
    if rules_path.exists(): artifacts["encoding_rules"] = joblib.load(rules_path)
    else: st.error("❌ File encoding_rules.pkl tidak ditemukan!"); st.stop()

    km_path = base_path / "model_kmeans.pkl" 
    if km_path.exists(): artifacts["kmeans_model"] = joblib.load(km_path)

    scaler_path = base_path / "scaler_kmeans.pkl"
    if scaler_path.exists(): artifacts["kmeans_scaler"] = joblib.load(scaler_path)

    kolom_path = base_path / "kolom_kmeans.pkl"
    if kolom_path.exists(): artifacts["kmeans_columns"] = joblib.load(kolom_path)
        
    return artifacts

# ── Inference (Prediksi Random Forest) ────────────────────────────────────────
def predict(user_data: dict) -> dict:
    artifacts = load_all_artifacts()
    model = artifacts["rf_model"]
    rules = artifacts["encoding_rules"]

    # Gunakan feature_columns dari rules untuk memastikan urutan kolom benar
    expected_cols = rules['feature_columns']

    # Ambil kamus aturan dari file pickle 
    rules = artifacts["encoding_rules"]
    binary_map = rules['binary_mapping']   # isinya {'no': 0, 'yes': 1}
    gender_map = rules['gender_mapping']   # isinya {'Female': 0, 'Male': 1}
    ordinal_map = rules['ordinal_mapping'] # isinya {'no': 0, 'Sometimes': 1, ...}

    # Bikin DataFrame Mentah dari input form
    # 1. Bikin DataFrame Mentah dengan mengambil aturan otomatis dari Pickle
    df_raw = pd.DataFrame([{
        "Gender": gender_map.get(user_data.get('gender')),
        "Age": user_data.get('age'),
        "Height": user_data.get('height'),
        "Weight": user_data.get('weight'),
        "family_history": binary_map.get(user_data.get('family_history')), 
        "FAVC": binary_map.get(user_data.get('favc', 'no')),
        "FCVC": float(user_data.get('fcvc', 2.0)),
        "NCP": float(user_data.get('ncp', 3.0)),
        "CAEC": ordinal_map.get(user_data.get('caec', 'no')),
        "SMOKE": binary_map.get(user_data.get('smoke', 'no')),
        "CH2O": float(user_data.get('ch2o', 2.0)),
        "SCC": binary_map.get(user_data.get('scc', 'no')),
        "FAF": float(user_data.get('faf', 0.0)),
        "TUE": float(user_data.get('tue', 0.0)),
        "CALC": ordinal_map.get(user_data.get('calc', 'no')),
        "MTRANS": user_data.get('mtrans') 
    }])

    # 2. Lakukan One-Hot Encoding otomatis
    df_encoded = pd.get_dummies(df_raw)

    # 3. Selaraskan dengan cetakan kolom pasti dari model Random Forest
    expected_cols = model.feature_names_in_
    X_final = df_encoded.reindex(columns=expected_cols, fill_value=0)

    # 4. PREDIKSI MENGGUNAKAN RANDOM FOREST WITH HYBRID VOTING CONFIDENCE SCALING (NOVELTY) 
    tree_weights = artifacts["tree_weights"] # Ini adalah w_i
    classes = model.classes_
    
    # Siapkan wadah kosong untuk menjumlahkan probabilitas
    weighted_probas = np.zeros(len(classes)) # Wadah untuk Simbol Sigma (Σ)
    total_weight = sum(tree_weights) # Ini adalah Total Bobot

    # Looping: Ekstraksi probabilitas per pohon dan kalikan dengan bobot OOB masing-masing
    for pohon, bobot in zip(model.estimators_, tree_weights):
        proba_satu_pohon = pohon.predict_proba(X_final.values)[0] # Ini adalah P_i(y|x) (Tebakan tiap pohon)
        weighted_probas += (proba_satu_pohon * bobot) # Ini adalah w_i * P_i(y|x) (Tebakan dikali bobot)

    # Lakukan normalisasi dengan membagi total bobot (Weighted Average)
    probas_arr = weighted_probas / total_weight # Ini adalah 1 / Σw_i (Hasil akhir probabilitas hybrid)
    
    # Tentukan kelas final berdasarkan probabilitas tertinggi (Argmax)
    best_class_idx = np.argmax(probas_arr)
    raw_label = classes[best_class_idx]
    
    # Ambil mapping dari rules
    target_mapping = rules['target_mapping'] 

    # Balik mapping biar bisa cari dari angka ke string
    INT_TO_LABEL = {v: k for k, v in target_mapping.items()}

    # Menerjemahkan angka (0-6) kembali ke teks
    label = INT_TO_LABEL.get(raw_label, raw_label)

    # Menerjemahkan label probabilitas juga
    probas = {INT_TO_LABEL.get(cls, cls): float(prob * 100) for cls, prob in zip(classes, probas_arr)}

    return {
        "label":      label,
        "display":    LABEL_DISPLAY.get(label, label),
        "confidence": float(probas_arr.max() * 100),
        "probas":     probas,
        "X_final_df": X_final # Kirim data yang sudah rapi untuk SHAP Plot nanti
    }

# ── UI helpers ────────────────────────────────────────────────────────────────
def get_prediction_color_class(label: str) -> str:
    if label == "Insufficient_Weight": return "blue"
    elif label == "Normal_Weight": return "green"
    elif label in ("Overweight_Level_I", "Overweight_Level_II"): return "yellow"
    return "red"

def get_prediction_icon(label: str) -> str:
    icons = {
        "Insufficient_Weight": "🔵", 
        "Normal_Weight": "🟢",       
        "Overweight_Level_I": "🟡",  
        "Overweight_Level_II": "🟡", 
        "Obesity_Type_I": "🔴",      
        "Obesity_Type_II": "🔴",     
        "Obesity_Type_III": "🔴"      
    }
    return icons.get(label, "❓")

# ── SHAP EXPLAINABLE AI ───────────────────────────────────────────────────────
def generate_shap_plot(model, X_final, predicted_label, rules):
    import shap
    import matplotlib.pyplot as plt
    
    # 1. Buat Explainer
    explainer = shap.TreeExplainer(model)
    
    # 2. Dapatkan Object Explanation utuh
    explanation = explainer(X_final)
    
    # Kamus translasi agar nama fitur nyaman dibaca
    kamus_terjemahan = {
        "Weight": "Berat Badan", 
        "Height": "Tinggi Badan", 
        "Age": "Usia",
        "NCP": "Jumlah Makan Besar", 
        "CH2O": "Konsumsi Air Putih", 
        "FCVC": "Makan Sayur",
        "FAF": "Olahraga/Aktivitas Fisik", 
        "TUE": "Screen Time", 
        "Gender": "Jenis Kelamin",
        "family_history": "Genetik Obesitas",
        "FAVC": "Makan Berkalori Tingi",
        "CAEC": "Ngemil",
        "CALC": "Konsumsi Alkohol",
        "SCC": "Pantau Kalori Harian",
        "SMOKE": "Merokok",
        "MTRANS_Automobile": "Mobil Pribadi",
        "MTRANS_Motorbike": "Motor",
        "MTRANS_Public_Transportation": "Kendaraan Umum",
        "MTRANS_Walking": "Jalan Kaki",
        "MTRANS_Bike": "Naik Sepeda"
    }

    # Ubah nama kolom DataFrame sesuai kamus
    clean_names = [kamus_terjemahan.get(f, f.replace('_', ' ')) for f in X_final.columns]

    # 3. Cari tahu index dari kelas yang diprediksi 
    target_mapping = rules['target_mapping']

    # Mencari nilai angka (0-6) dari label string menggunakan mapping yang dinamis
    raw_label_int = target_mapping.get(predicted_label)
    
    # Fallback jika tidak ketemu (memastikan tipe data int)
    if raw_label_int is None:
        raw_label_int = next((v for k, v in target_mapping.items() if str(k) == str(predicted_label)), None)
    
    # Konversi ke int agar sinkron dengan model.classes_
    raw_label_int = int(raw_label_int)
    class_index = list(model.classes_).index(raw_label_int)
    
    # 4. Ekstrak data khusus untuk pasien ini (index 0) dan kelas prediksinya
    explanation_single = explanation[0, :, class_index]
    
    # Timpa nama fiturnya dengan nama yang sudah rapi
    explanation_single.feature_names = clean_names
    explanation_single.data = None
    
    # 5. Gambar Waterfall Plot Asli
    fig = plt.figure(figsize=(10, 6))
    
    # Memanggil fungsi waterfall asli bawaan library SHAP
    shap.plots.waterfall(explanation_single, show=False, max_display=10)
    
    # Rapikan layout
    plt.title(f'Alur Keputusan AI untuk: {predicted_label}', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    return fig

# ── INTEGRASI K-MEANS CLUSTERING (PERSONA GAYA HIDUP) ──
def predict_lifestyle_persona(user_data: dict) -> dict:
    artifacts = load_all_artifacts()
    
    if "kmeans_model" not in artifacts:
        return {"cluster": None, "persona": "Model K-Means belum siap", "desc": "", "color": "#000000"}

    kmeans = artifacts["kmeans_model"]
    scaler = artifacts["kmeans_scaler"]
    kolom_mesin = artifacts["kmeans_columns"]
    
    # Ambil kamus dari encoding_rules
    rules = artifacts["encoding_rules"]
    binary_map = rules['binary_mapping']   # {'no': 0, 'yes': 1}
    ordinal_map = rules['ordinal_mapping'] # {'no': 0, 'Sometimes': 1, ...}

    # Bikin DataFrame dengan mapping yang sudah terpusat
    df_raw = pd.DataFrame([{
        'FAVC':  binary_map.get(user_data.get('favc', 'no'), 0),
        'FCVC':  float(user_data.get('fcvc', 2.0)),
        'NCP':   float(user_data.get('ncp', 3.0)),
        'CAEC':  ordinal_map.get(user_data.get('caec', 'no'), 0),
        'SMOKE': binary_map.get(user_data.get('smoke', 'no'), 0),
        'CH2O':  float(user_data.get('ch2o', 2.0)),
        'SCC':   binary_map.get(user_data.get('scc', 'no'), 0),
        'FAF':   float(user_data.get('faf', 0.0)),
        'TUE':   float(user_data.get('tue', 0.0)),
        'CALC':  ordinal_map.get(user_data.get('calc', 'no'), 0),
        'MTRANS': user_data.get('mtrans', 'Public_Transportation')
    }])

    # One-hot encoding & reindexing agar urutan kolom sama dengan K-Means
    df_encoded = pd.get_dummies(df_raw, columns=['MTRANS'])
    df_final = df_encoded.reindex(columns=kolom_mesin, fill_value=0)

    # Prediksi
    X_scaled = scaler.transform(df_final)
    cluster_id = kmeans.predict(X_scaled)[0]

    # Persona definition
    personas = {
        0: {
            "name": '"Kamu Si Mager Berkendaraan Pribadi" (The Urban Driver)',
            "desc": "Kelompok ini menggambarkan gaya hidup masyarakat dengan kendaraan pribadi, yang secara umum tingkat aktivitas fisiknya moderat dan memiliki asupan kalori yang sangat tinggi.",
            "color": "#B71C1C" 
        },
        1: {
            "name": '"Kamu Si Pejuang Transportasi Umum Doyan Kalori" (The Commuter Snacker)',
            "desc": "Kelompok ini menggambarkan gaya hidup masyarakat dengan kendaraan umum, yang secara umum tingkat aktivitas fisiknya paling rendah dan bergantung pada makanan berkalori tinggi paling tinggi.",
            "color": "#F9A825"
        },
        2: {
            "name": '"Kamu Si Sadar Sehat & Aktif" (The Health-Conscious Active)',
            "desc": "Kelompok ini menggambarkan gaya hidup masyarakat dengan awareness kesehatan paling tinggi, yang secara umum menghindari kalori tinggi, memantau kalori harian, dan paling aktif bergerak (termasuk berjalan kaki).",
            "color": "#2E7D32"
        }
    }

    result = personas.get(cluster_id, {"name": "Unknown", "desc": "", "color": "#000000"})
    
    return {
        "cluster": int(cluster_id),
        "persona": result["name"],
        "desc": result["desc"],
        "color": result["color"],
    }