import streamlit as st
import pandas as pd
import time

# --- WHITE THEME (CLEAN & SHARP) ---
st.set_page_config(page_title="TGS SNIPER LIVE", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    .sniper-card { 
        background: #ffffff; border: 1px solid #e1e4e8; border-radius: 12px; 
        padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border-left: 10px solid #28a745;
    }
    .sell-card { border-left-color: #dc3545; }
    .wait-card { border-left-color: #adb5bd; opacity: 0.7; }
    </style>
    """, unsafe_allow_html=True)

# Aapka Final CSV Link
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQly4ZQG_WYmZv2s5waDvjO71iG6-W28fqoS7d8Uc_7BeKnZ-6XyXebCdmBth8JVWpm8TEmUYHtwi9f/pub?output=csv"

def get_data():
    try:
        # Direct fetch from TGS Sheet
        df = pd.read_csv(CSV_URL)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

st.markdown("<h2 style='text-align: center;'>🎯 TGS DASHBOARD - LIVE SNIPER</h2>", unsafe_allow_html=True)

df_live = get_data()

if not df_live.empty:
    col1, col2 = st.columns(2)
    # Hum top stocks dikhayenge taaki screen khali na lage
    for i, (idx, row) in enumerate(df_live.head(10).iterrows()):
        t_col = col1 if i % 2 == 0 else col2
        sig = str(row['Signal Type']).strip().upper()
        
        # Color Logic
        if "POSITIONAL" in sig:
            style = ""
            color = "#28a745"
            label = "BUY"
        elif "SHORTS" in sig:
            style = "sell-card"
            color = "#dc3545"
            label = "SELL"
        else:
            style = "wait-card"
            color = "#6c757d"
            label = "WAIT"
            
        with t_col:
            st.markdown(f"""
                <div class="sniper-card {style}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <b style="font-size: 22px;">{row['Symbol']}</b>
                        <b style="color: {color};">{label}</b>
                    </div>
                    <div style="margin-top: 15px; display: grid; grid-template-columns: 1fr 1fr 1fr; text-align: center;">
                        <div><small>LTP</small><br><b>{row['LTP']}</b></div>
                        <div><small>SL</small><br><b style="color:#dc3545;">{row['Stop Loss']}</b></div>
                        <div><small>TARGET</small><br><b style="color:#007bff;">{row['Target']}</b></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("⌛ Bhai, data aane mein thoda waqt lag raha hai. Bas 1 minute rukiye...")

time.sleep(10)
st.rerun()
