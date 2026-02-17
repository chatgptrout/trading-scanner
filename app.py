import streamlit as st
import pandas as pd
import time

# --- OFFICE PC OPTIMIZED ---
st.set_page_config(page_title="SANTOSH LIVE OFFICE", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .status-card { 
        background: #fdfdfd; border: 1px solid #eee; border-radius: 10px; 
        padding: 15px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border-left: 8px solid #adb5bd;
    }
    .bullish { border-left-color: #28a745; background-color: #f0fff4; }
    .bearish { border-left-color: #dc3545; background-color: #fff5f5; }
    </style>
    """, unsafe_allow_html=True)

# Aapki purani sheet ka link
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQly4ZQG_WYmZv2s5waDvjO71iG6-W28fqoS7d8Uc_7BeKnZ-6XyXebCdmBth8JVWpm8TEmUYHtwi9f/pub?output=csv"

def get_data():
    try:
        # Force refresh data
        df = pd.read_csv(f"{CSV_URL}&cachebuster={time.time()}")
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

st.title("🎯 Santosh Sniper - Live Feed")

df = get_data()

if not df.empty:
    # Saara data dikhayega, kuch bhi filter nahi karega!
    col1, col2 = st.columns(2)
    for i, (idx, row) in enumerate(df.head(20).iterrows()):
        t_col = col1 if i % 2 == 0 else col2
        sig = str(row['Signal Type']).strip().upper()
        
        # Color coding logic
        status_class = ""
        if "BULLISH" in sig or "POSITIONAL" in sig: status_class = "bullish"
        elif "BEARISH" in sig or "SHORTS" in sig: status_class = "bearish"
        
        with t_col:
            st.markdown(f"""
                <div class="status-card {status_class}">
                    <div style="display: flex; justify-content: space-between;">
                        <b style="font-size: 18px;">{row['Symbol']}</b>
                        <span style="font-weight: bold;">{sig}</span>
                    </div>
                    <div style="margin-top: 10px; display: grid; grid-template-columns: 1fr 1fr 1fr; text-align: center;">
                        <div><small>LTP</small><br><b>{row['LTP']}</b></div>
                        <div><small>SL</small><br><b style="color:#dc3545;">{row['Stop Loss']}</b></div>
                        <div><small>TGT</small><br><b style="color:#007bff;">{row['Target']}</b></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("⚠️ Error: Office PC connection block kar raha hai. Ek baar browser mein link manually check karein.")

time.sleep(10)
st.rerun()
