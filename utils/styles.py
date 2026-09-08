"""
Global CSS injection – Health Theme.
Primary: #4CAF50  |  Background: #E8F5E9  |  Cards: white + shadow
"""

import streamlit as st

def inject_global_css():
    st.markdown(
        """
        <style>
        /* ── Google Fonts ────────────────────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

        /* ── CSS Variables ───────────────────────────────────────────────── */
        :root {
            --primary:       #4CAF50;
            --primary-dark:  #388E3C;
            --primary-light: #81C784;
            --primary-bg:    #E8F5E9;
            --accent:        #00897B;
            --danger:        #E53935;
            --warning:       #F9A825;
            --info:          #1E88E5;
            --white:         #FFFFFF;
            --gray-50:       #FAFAFA;
            --gray-100:      #F5F5F5;
            --gray-200:      #EEEEEE;
            --gray-400:      #BDBDBD;
            --gray-600:      #757575;
            --gray-800:      #424242;
            --text-main:     #212121;
            --radius-sm:     8px;
            --radius-md:     14px;
            --radius-lg:     20px;
            --shadow-sm:     0 2px 8px rgba(76,175,80,.10);
            --shadow-md:     0 4px 20px rgba(76,175,80,.15);
            --shadow-lg:     0 8px 32px rgba(76,175,80,.18);
            
            --font-main:    'Poppins', sans-serif;
            --font-body:    'Poppins', sans-serif;
        }

        /* ── Reset & Base ────────────────────────────────────────────────── */
        html, body, [class*="css"] {
            font-family: var(--font-body);
            color: var(--text-main);
        }

        /* App background */
        .stApp {
            background: linear-gradient(135deg, #E8F5E9 0%, #F1F8E9 50%, #E0F2F1 100%) !important;
            min-height: 100vh;
        }

        /* ── Hapus Space Kosong di Atas & Sembunyikan Header ── */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
        }
        
        [data-testid="stHeader"] {
            display: none !important;
        }

        /* ── Sidebar & Menu Estetik ──────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 40%, #388E3C 100%) !important;
            border-right: none !important;
        }
        [data-testid="stSidebar"] * { color: #FFFFFF !important; }
        
        /* 1. Sembunyikan Label Judul Radio "Navigasi" */
        [data-testid="stSidebar"] .stRadio > label { display: none !important; }

        /* 2. Sembunyikan bulatan radio bawaan Streamlit */
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child {
            display: none !important;
        }
        
        /* Paksa teks menu muncul dan berwarna putih */
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"] p {
            color: white !important;
            font-size: 15px !important;
            margin: 0 !important;
        }

        /* 3. Styling bentuk dasar menu (Jadi kotak melengkung estetik) */
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"] {
            background: rgba(255,255,255, 0.05);
            padding: 12px 16px !important;
            border-radius: 12px !important;
            margin-bottom: 8px;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            width: 100%;
            cursor: pointer;
            border: 1px solid transparent;
        }

        /* 4. Efek Hover */
        [data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"]:hover {
            background: rgba(255, 255, 255, 0.15) !important;
            transform: translateX(6px);
            border-color: rgba(255,255,255, 0.3);
        }

        /* 5. Efek AKTIF (Terpilih) - Shadow & Background Putih */
        [data-testid="stSidebar"] div[role="radiogroup"] div:has(input[aria-checked="true"]) label[data-baseweb="radio"] {
            background: white !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25) !important;
            transform: translateX(4px);
            border-color: white;
        }

        /* 6. Warna teks menu saat aktif (Jadi hijau gelap) */
        [data-testid="stSidebar"] div[role="radiogroup"] div:has(input[aria-checked="true"]) label[data-baseweb="radio"] p {
            color: #1B5E20 !important; 
            font-weight: 800 !important;
        }

        /* Sidebar header */
        .sidebar-header {
            text-align: center;
            padding: 24px 0 16px;
        }
        .sidebar-logo { font-size: 52px; margin-bottom: 8px; }
        .sidebar-title {
            font-family: var(--font-main);
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -.5px;
            color: #FFFFFF;
        }
        .sidebar-subtitle {
            font-size: 12px;
            color: rgba(255,255,255,.65);
            margin-top: 4px;
        }

        /* User info */
        .user-info-card {
            background: rgba(255,255,255,.12);
            border-radius: var(--radius-md);
            padding: 14px 16px;
            margin: 0 0 4px;
            backdrop-filter: blur(8px);
        }
        .user-avatar { font-size: 28px; margin-bottom: 6px; }
        .user-email  { font-size: 13px; font-weight: 600; word-break: break-all; }
        .user-status { font-size: 11px; color: #A5D6A7; margin-top: 4px; }

        /* Nav label */
        .sidebar-nav-label {
            font-size: 10px;
            letter-spacing: 1.5px;
            color: rgba(255,255,255,.5) !important;
            margin-bottom: 8px;
        }

        /* Logout button */
        [data-testid="stSidebar"] .stButton > button {
            background: rgba(229,57,53,.25) !important;
            border: 1px solid rgba(229,57,53,.5) !important;
            color: #FFCDD2 !important;
            font-weight: 600;
            border-radius: var(--radius-sm) !important;
            transition: all .2s;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(229,57,53,.45) !important;
            border-color: #E53935 !important;
            color: #FFFFFF !important;
        }

        /* ── Main buttons ────────────────────────────────────────────────── */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: var(--radius-sm) !important;
            font-family: var(--font-main) !important;
            font-weight: 600 !important;
            padding: 10px 20px !important;
            transition: all .25s !important;
            box-shadow: 0 2px 8px rgba(76,175,80,.30) !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(76,175,80,.40) !important;
        }
        .stButton > button:active { transform: translateY(0) !important; }

        /* ── Forms / Inputs ──────────────────────────────────────────────── */
        [data-baseweb="input"] > div,
        [data-baseweb="select"] > div,
        [data-baseweb="textarea"] > div {
            border-radius: var(--radius-sm) !important;
            border-color: #C8E6C9 !important;
            background: var(--white) !important;
        }
        [data-baseweb="input"] > div:focus-within,
        [data-baseweb="select"] > div:focus-within {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 3px rgba(76,175,80,.15) !important;
        }

        /* Selectbox arrow */
        [data-baseweb="select"] svg { color: var(--primary) !important; }

        /* Number inputs */
        [data-testid="stNumberInput"] > div {
            border-radius: var(--radius-sm) !important;
        }

        /* ── Cards ───────────────────────────────────────────────────────── */
        .card {
            background: var(--white);
            border-radius: var(--radius-md);
            padding: 24px;
            box-shadow: var(--shadow-sm);
            border: 1px solid #E8F5E9;
            margin-bottom: 16px;
        }
        .card-title {
            font-family: var(--font-main);
            font-size: 16px;
            font-weight: 700;
            color: var(--primary-dark);
            margin-bottom: 4px;
        }

        /* ── Metric cards ────────────────────────────────────────────────── */
        .metric-card {
            background: var(--white);
            border-radius: var(--radius-md);
            padding: 20px 24px;
            box-shadow: var(--shadow-sm);
            border-left: 4px solid #2196F3;
            text-align: center;
        }
        .metric-label {
            font-size: 12px;
            font-weight: 600;
            color: var(--gray-600);
            letter-spacing: .8px;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .metric-value {
            font-family: var(--font-main);
            font-size: 28px;
            font-weight: 800;
            color: var(--primary-dark);
        }
        .metric-sub { font-size: 12px; color: var(--gray-600); margin-top: 2px; }

        /* ── Prediction result cards ─────────────────────────────────────── */
        .pred-card {
            border-radius: var(--radius-lg);
            padding: 28px 32px;
            text-align: center;
            box-shadow: var(--shadow-md);
            margin: 12px 0;
        }
        .pred-card-blue   { background: linear-gradient(135deg,#E3F2FD,#BBDEFB); border: 2px solid #64B5F6; }
        .pred-card-green  { background: linear-gradient(135deg,#E8F5E9,#C8E6C9); border: 2px solid #81C784; }
        .pred-card-yellow { background: linear-gradient(135deg,#FFFDE7,#FFF9C4); border: 2px solid #F9A825; }
        .pred-card-red    { background: linear-gradient(135deg,#FFEBEE,#FFCDD2); border: 2px solid #EF9A9A; }

        .pred-icon   { font-size: 52px; margin-bottom: 12px; }
        .pred-label  { font-family: var(--font-main); font-size: 22px; font-weight: 800; margin-bottom: 6px; }
        .pred-conf   { font-size: 14px; font-weight: 600; color: var(--gray-600); }

        .pred-blue   { color: #1565C0; }
        .pred-green  { color: #2E7D32; }
        .pred-yellow { color: #F57F17; }
        .pred-red    { color: #B71C1C; }

        /* ── Recommendation Cards (Food & Activity) ─────────────────────── */
        .food-card, .activity-card {
            background: var(--white);
            border-radius: var(--radius-md);
            overflow: hidden;
            box-shadow: var(--shadow-sm);
            border: 1px solid #E8F5E9;
            transition: transform .2s, box-shadow .2s;
            height: 330px;
            display: flex;
            flex-direction: column;
        }
        .food-card:hover, .activity-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-md);
        }
        .food-card img, .activity-card img {
            width: 100%;
            height: 160px;
            object-fit: cover;
            flex-shrink: 0;
        }
        .food-card-body, .activity-card-body { 
            padding: 14px 16px; 
            flex: 1; 
            display: flex;
            flex-direction: column;
        }
        .food-card-name, .activity-card-name {
            font-family: var(--font-main);
            font-size: 15px;
            font-weight: 700;
            color: var(--primary-dark);
            margin-bottom: 6px;
        }
        .food-card-desc, .activity-card-desc { 
            font-size: 13px; 
            color: var(--gray-600); 
            line-height: 1.5; 
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        /* ── Auth page ───────────────────────────────────────────────────── */
        .auth-container {
            text-align: center;
            padding: 40px 0 24px;
        }
        .auth-logo    { font-size: 64px; margin-bottom: 12px; }
        .auth-title   {
            font-family: var(--font-main);
            font-size: 32px;
            font-weight: 800;
            color: var(--primary-dark);
            margin: 0;
        }
        .auth-subtitle {
            font-size: 15px;
            color: var(--gray-600);
            margin-top: 8px;
            line-height: 1.6;
        }
        .auth-card {
            background: var(--white);
            border-radius: var(--radius-lg);
            padding: 28px;
            box-shadow: var(--shadow-lg);
            border: 1px solid #C8E6C9;
            margin-top: 8px;
        }

        /* ── Page header ─────────────────────────────────────────────────── */
        .page-header {
            background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 50%, #66BB6A 100%);
            border-radius: var(--radius-lg);
            padding: 28px 32px;
            margin-bottom: 24px;
            color: white;
            box-shadow: var(--shadow-md);
        }
        .page-header h1 {
            font-family: var(--font-main);
            font-size: 26px;
            font-weight: 800;
            margin: 0 0 6px;
            color: #FFFFFF !important;
        }
        .page-header p { font-size: 14px; color: rgba(255,255,255,.80); margin: 0; }

        /* ── Section headings ────────────────────────────────────────────── */
        .section-title {
            font-family: var(--font-main);
            font-size: 18px;
            font-weight: 700;
            color: var(--primary-dark);
            margin: 20px 0 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .section-title::after {
            content: '';
            flex: 1;
            height: 2px;
            background: linear-gradient(90deg, #C8E6C9, transparent);
            border-radius: 2px;
        }

        /* ── Tabs ────────────────────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: transparent !important;
            border-bottom: 2px solid #C8E6C9 !important;
            padding-bottom: 0 !important;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: var(--radius-sm) var(--radius-sm) 0 0 !important;
            background: #F1F8E9 !important;
            color: var(--gray-600) !important;
            font-family: var(--font-main) !important;
            font-weight: 600 !important;
            border: 1px solid #C8E6C9 !important;
            border-bottom: none !important;
        }
        .stTabs [aria-selected="true"] {
            background: var(--primary) !important;
            color: #FFFFFF !important;
            border-color: var(--primary) !important;
        }

        /* ── Streamlit default override ──────────────────────────────────── */
        h1,h2,h3,h4 {
            font-family: var(--font-main) !important;
            color: var(--primary-dark) !important;
        }
        .stAlert { border-radius: var(--radius-sm) !important; }
        [data-testid="stMetricValue"] {
            font-family: var(--font-main) !important;
            font-weight: 800 !important;
            color: var(--primary-dark) !important;
        }

        /* Hide default streamlit branding */
        #MainMenu, footer, header { visibility: hidden; }

        /* ── Percantik Form Bawaan (Login, Register, Prediksi) ── */
        [data-testid="stForm"] {
            background: #FFFFFF;
            border-radius: 20px;
            padding: 24px 28px;
            box-shadow: 0 4px 20px rgba(76,175,80,.12);
            border: 1px solid #C8E6C9;
            margin-top: 8px;
            transition: transform .2s, box-shadow .2s;
        }
        [data-testid="stForm"]:hover {
            box-shadow: 0 8px 24px rgba(76,175,80,.18);
        }

        /* ── Perbaikan Tombol Submit (Login/Daftar/Prediksi) ── */
        [data-testid="stFormSubmitButton"] > button {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: var(--radius-sm) !important;
            font-family: var(--font-main) !important;
            font-weight: 600 !important;
            padding: 10px 20px !important;
            width: 100%;
            transition: all .25s !important;
            box-shadow: 0 2px 8px rgba(76,175,80,.30) !important;
        }
        [data-testid="stFormSubmitButton"] > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(76,175,80,.40) !important;
        }

        /* ── Sembunyikan Tombol Tombol Sidebar (Panah) ── */
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )