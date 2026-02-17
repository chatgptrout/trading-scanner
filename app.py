import streamlit as st
import pandas as pd
import requests
import io
import time

# --- CLEAN WHITE OFFICE UI ---
st.set_page_config(page_title="SANTOSH OFFICE PRO", layout="wide")
st.markdown("<style>.stApp { background-color: #ffffff; }</style>", unsafe_allow_html=True)

# Direct CSV Link
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQly4ZQG_WYmZv2s5waDvjO71iG6-W28fqoS7d8Uc_7BeKnZ-6XyXebCdmBth8JVWpm8TEmUYHtwi9f/pub?output=csv"

def fetch_via_requests():
    try:
        # Office firewall bypass karne ke liye requests ka use
        response = requests.get(CSV_URL, timeout=10)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            df.columns = df.columns.str.strip()
            return df
        return pd.DataFrame()
    except:
        return pd.DataFrame()

st.title("🎯 Santosh Sniper - Direct Link")

df = fetch_via_requests()

if not df.empty:
    # Sab dikhayega taaki aapko screen khali na lage
    for i, (idx, row) in enumerate(df.head(10).iterrows()):
        sig = str(row['Signal Type']).strip().upper()
        color = "#28a745" if "BULLISH" in sig else "#dc3545" if "BEARISH" in sig else "#6c757d"
        
        st.markdown(f"""
            <div style="border: 1px solid #eee; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 8px solid {color};">
                <div style="display: flex; justify-content: space-between;">
                    <b style="font-size: 20px;">{row['Symbol']}</b>
                    <b style="color: {color};">{sig}</b>
                </div>
                <div style="margin-top: 10px; display: grid; grid-template-columns: 1fr 1fr 1fr; text-align: center;">
                    <div>LTP<br><b>{row['LTP']}</b></div>
                    <div>SL<br><b style="color:red;">{row['Stop Loss']}</b></div>
                    <div>TGT<br><b style="color:blue;">{row['Target']}</b></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("Bhai, office network abhi bhi block kar raha hai. Ek baar mobile hotspot se connect karke dekho, turant chal jayega!")

time.sleep(15)
st.rerun()