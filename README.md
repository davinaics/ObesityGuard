# 🩺 ObesityGuard – Classification & Monitoring Obesity

An interactive Streamlit-based web application designed to classify obesity levels, segment lifestyles, and provide transparency regarding classification results using SHAP (Shapley Additive Explanations).

---

## 💻 System Requirements
Make sure the following software is installed on your device:
- Python (Version 3.11 or later is recommended)
- pip (Python package manager)

---

## ⚙️ Installation Guide

1. Download or Extract the Project
   Extract the project folder to a directory of your choice on your computer.

2. Open Terminal / Command Prompt
   Change the terminal directory to the project folder:
   cd path/to/project-folder

3. Creating a Virtual Environment (Optional but Recommended)
   To keep your system libraries clean:
   - Windows:
     python -m venv venv
     venv\Scripts\activate
   - macOS / Linux:
     python3 -m venv venv
     source venv/bin/activate

4. Installing Required Libraries
   Run the following command to install all libraries listed in the configuration file:
   pip install -r requirements.txt

---

## 📁 Project Structure
```
obesity_app/
├── app.py                       
├── requirements.txt
├── model.pkl                    
├── label_encoder.pkl             
├── supabase_schema.sql           
├── .streamlit/
│   └── secrets.toml              
├── utils/
│   ├── __init__.py
│   ├── auth.py                   
│   ├── database.py              
│   ├── ml.py                    
│   ├── styles.py                
│   └── supabase_client.py        
└── pages/
    ├── __init__.py
    ├── prediksi.py               
    └── dashboard.py             
```
Here is the main directory structure of this application:
- app.py — The main file for running the Streamlit web interface and navigation.
- auth.py — A module for handling user authentication (login and registration).
- database.py — A module for managing the storage and retrieval of health history from the Supabase database.
- ml.py — Core Machine Learning module (loading model artifacts, RF Hybrid Voting Confidence Scaling prediction inference, K-Means clustering, and SHAP Waterfall Plot).
- styles.py — Module for injecting Global Custom CSS.
- supabase_client.py — Configuration file for connecting the application to the Supabase Cloud client.
- dashboard.py — View module for the monitoring dashboard and health history graph pages.
- prediction.py — View module for the physical data & lifestyle input form page, as well as the visualization of prediction results, clustering, and SHAP.
- profile.py — View module for the user profile management page.
- models/ — Folder containing trained .pkl (joblib/pickle) model files (best_rf_model.pkl, tree_weights.pkl, encoding_rules.pkl, model_kmeans.pkl, scaler_kmeans.pkl, etc.).
- requirements.txt — List of Python libraries and dependencies.

---

## 🚀 How to Run

1. Make sure you are in the project folder directory and that the virtual environment is active (if you are using one).
2. Run the following Streamlit command in the terminal:
   streamlit run app.py
3. Copy the local link (usually http://localhost:8501) that appears in the terminal, then open it in your web browser.
