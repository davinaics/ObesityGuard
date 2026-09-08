"""
Database operations: health_logs.
"""

from datetime import date
from typing import Optional, List, Dict, Any
import streamlit as st
from utils.supabase_client import get_supabase_client

# ── Health Logs ───────────────────────────────────────────────────────────────

def save_health_log(user_id: str, snapshot: dict, prediction_result: str) -> bool:
    supabase = get_supabase_client()
    try:
        data = {
            "user_id": user_id,
            "date": str(date.today()),
            "gender": snapshot["gender"],
            "age": snapshot["age"],
            "height": snapshot["height"],
            "weight": snapshot["weight"],
            "family_history": snapshot["family_history"],
            "favc": snapshot["favc"],
            "fcvc": str(snapshot["fcvc"]),
            "ncp": str(snapshot["ncp"]),
            "caec": snapshot["caec"],
            "ch2o": str(snapshot["ch2o"]),
            "scc": snapshot["scc"],
            "calc": snapshot["calc"],
            "smoke": snapshot.get("smoke", "no"),
            "faf": str(snapshot.get("faf", 0.0)),
            "tue": str(snapshot.get("tue", 0.0)),
            "mtrans": snapshot.get("mtrans", "Public_Transportation"),
            "prediction_result": prediction_result,
        }
        supabase.table("health_logs").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Gagal menyimpan data: {e}")
        return False

def get_health_logs(user_id: str) -> List[Dict[str, Any]]:
    supabase = get_supabase_client()
    try:
        resp = (
            supabase.table("health_logs")
            .select("*")
            .eq("user_id", user_id)
            .order("date", desc=False)
            .execute()
        )
        return resp.data or []
    except Exception as e:
        st.error(f"Gagal mengambil riwayat: {e}")
        return []