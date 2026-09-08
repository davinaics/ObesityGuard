"""
Halaman Dashboard: summary cards, chart progres berat, riwayat klasifikasi.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

from utils.database import get_health_logs
from utils.ml import LABEL_DISPLAY

def show_dashboard_page():
    # ── Page Header ───────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="page-header">
            <h1>📊 Dashboard Monitoring Obesitas</h1>
            <p>Pantau progres berat badan dan status kesehatan Anda dari waktu ke waktu</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    user_id = st.session_state.get("user_id", "")
    logs    = get_health_logs(user_id)

    if not logs:
        st.info(
            "📭 Belum ada data riwayat. "
            "Lakukan prediksi dan simpan hasilnya di halaman **Prediksi** terlebih dahulu."
        )
        return

    df = pd.DataFrame(logs)
    df["date"]   = pd.to_datetime(df["date"])
    df["weight"] = df["weight"].astype(float)
    df["height"] = df["height"].astype(float)
    df["bmi"]    = df["weight"] / (df["height"] ** 2)

    # ── Summary Cards ─────────────────────────────────────────────────────────
    _show_summary_cards(df)
    st.markdown("<br>", unsafe_allow_html=True) 

    # ── Chart 1: Progres Berat ────────────────────────────────────────────────
    _show_weight_chart(df)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chart 2: Riwayat Klasifikasi ──────────────────────────────────────────
    _show_classification_history(df)


# ── Sub-renderers ─────────────────────────────────────────────────────────────

def _show_summary_cards(df: pd.DataFrame):
    """Tampilkan 3 kartu metrik utama dengan desain estetik dan seragam."""
    st.markdown('<div class="section-title">📌 Ringkasan Terkini</div>', unsafe_allow_html=True)

    latest = df.sort_values("date").iloc[-1]
    bmi    = latest["bmi"]
    status = LABEL_DISPLAY.get(latest["prediction_result"], latest["prediction_result"])
    tanggal = latest['date'].strftime('%d %b %Y')

    # Tentukan warna status
    pred = latest["prediction_result"]
    if pred == "Insufficient_Weight": status_color = "#1565C0" # Biru
    elif pred == "Normal_Weight": status_color = "#2E7D32" # Hijau
    elif pred in ("Overweight_Level_I", "Overweight_Level_II"): status_color = "#F9A825" # Kuning
    else: status_color = "#C62828" # Merah

    # Template CSS untuk Kartu 
    card_style = """
        height: 140px;
        background: white; 
        border-radius: 16px; 
        padding: 20px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.04); 
        text-align: center; 
        display: flex; 
        flex-direction: column; 
        justify-content: center; 
        align-items: center;
        border: 1px solid #F0F0F0;
        transition: transform 0.2s ease;
    """

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div style="{card_style}">
                <div style="font-size: 12px; color: #757575; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">⚖️ Berat Terakhir</div>
                <div style="font-size: 34px; font-weight: 800; color: #2E7D32; line-height: 1.1;">{latest['weight']:.1f}</div>
                <div style="font-size: 13px; color: #9E9E9E; font-weight: 500; margin-top: 4px;">kilogram</div>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style="{card_style}">
                <div style="font-size: 12px; color: #757575; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">📏 BMI Terakhir</div>
                <div style="font-size: 34px; font-weight: 800; color: #0277BD; line-height: 1.1;">{bmi:.1f}</div>
                <div style="font-size: 13px; color: #9E9E9E; font-weight: 500; margin-top: 4px;">kg/m²</div>
            </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div style="{card_style} border-bottom: 4px solid {status_color};">
                <div style="font-size: 12px; color: #757575; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">🏷️ Status Terakhir</div>
                <div style="font-size: 20px; font-weight: 800; color: {status_color}; line-height: 1.2;">{status}</div>
                <div style="font-size: 13px; color: #9E9E9E; font-weight: 500; margin-top: 4px;">{tanggal}</div>
            </div>""", unsafe_allow_html=True)


def _show_weight_chart(df: pd.DataFrame):
    """Line chart progres berat badan."""
    st.markdown('<div class="section-title">📉 Progres Berat Badan</div>', unsafe_allow_html=True)

    df_sorted = df.sort_values(["date", "created_at"])
    df_sorted["tanggal_bersih"] = df_sorted["date"].dt.strftime("%d %b %Y")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_sorted["tanggal_bersih"], 
        y=df_sorted["weight"], 
        mode="lines+markers", 
        name="Berat (kg)",
        line=dict(color="#4CAF50", width=3, shape="spline"),
        marker=dict(color="#2E7D32", size=8, symbol="circle"),
        fill="tozeroy", fillcolor="rgba(76,175,80,0.08)",
        hovertemplate="<b>%{x}</b><br>Berat: %{y:.1f} kg<extra></extra>",
    ))

    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="DM Sans, sans-serif", color="#424242"),
        xaxis=dict(title="", gridcolor="#F5F5F5", type="category"),
        yaxis=dict(title="Berat Badan (kg)", showgrid=True, gridcolor="#F5F5F5", rangemode="tozero"),
        hovermode="x unified", margin=dict(l=0, r=0, t=10, b=0), height=320,
    )
    
    st.plotly_chart(fig, use_container_width=True, key="chart_progres_berat")


def _show_classification_history(df: pd.DataFrame):
    """Line chart riwayat klasifikasi dengan filter hari."""
    st.markdown('<div class="section-title">📅 Riwayat Status Medis</div>', unsafe_allow_html=True)

    col_filter, _ = st.columns([1, 3])
    with col_filter:
        period = st.selectbox("Periode Waktu:", ["7 hari terakhir", "30 hari terakhir", "Semua Waktu"], key="period_select")

    df_f = df.copy()
    if period != "Semua Waktu":
        days = 7 if "7" in period else 30
        cutoff = pd.Timestamp(date.today() - timedelta(days=days))
        df_f = df_f[df_f["date"] >= cutoff].sort_values(["date", "created_at"])
    else:
        df_f = df_f.sort_values(["date", "created_at"])

    if df_f.empty:
        st.info("Tidak ada data dalam periode ini.")
        return

    df_f["tanggal_bersih"] = df_f["date"].dt.strftime("%d %b %Y")

    CUSTOM_ORDER = {
        "Insufficient_Weight": 0, "Normal_Weight": 1,
        "Overweight_Level_I": 2, "Overweight_Level_II": 3,
        "Obesity_Type_I": 4, "Obesity_Type_II": 5, "Obesity_Type_III": 6
    }
    
    df_f["label_num"] = df_f["prediction_result"].map(CUSTOM_ORDER)
    df_f["label_disp"] = df_f["prediction_result"].map(LABEL_DISPLAY)

    fig = go.Figure()

    fig.add_hrect(y0=-0.5, y1=0.5, fillcolor="rgba(21,101,192,0.06)", line_width=0, annotation_text="Kurus", annotation_position="left")
    fig.add_hrect(y0=0.5, y1=1.5, fillcolor="rgba(76,175,80,0.06)", line_width=0, annotation_text="Normal", annotation_position="left")
    fig.add_hrect(y0=1.5, y1=3.5, fillcolor="rgba(249,168,37,0.06)", line_width=0, annotation_text="Overweight", annotation_position="left")
    fig.add_hrect(y0=3.5, y1=6.5, fillcolor="rgba(229,57,53,0.06)", line_width=0, annotation_text="Obesitas", annotation_position="left")

    fig.add_trace(go.Scatter(
        x=df_f["tanggal_bersih"], 
        y=df_f["label_num"], 
        mode="lines+markers+text",
        text=df_f["label_disp"], textposition="top center", textfont=dict(size=10, color="#424242"),
        line=dict(color="#424242", width=2, shape="vh"), 
        marker=dict(color="#2E7D32", size=10, symbol="diamond"),
        hovertemplate="<b>%{x}</b><br>Status: %{text}<extra></extra>",
    ))

    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        font=dict(family="DM Sans, sans-serif", color="#424242"),
        xaxis=dict(title="", gridcolor="#F5F5F5", type="category"),
        yaxis=dict(
            title="",
            tickmode="array",
            tickvals=list(CUSTOM_ORDER.values()),
            ticktext=[LABEL_DISPLAY[k] for k in CUSTOM_ORDER.keys()],
            showgrid=True, gridcolor="#F5F5F5",
        ),
        margin=dict(l=0, r=0, t=10, b=0), height=380,
    )
    
    st.plotly_chart(fig, use_container_width=True, key="chart_riwayat")