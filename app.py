import streamlit as st
import pandas as pd
import time

# --- Page Setup ---
st.set_page_config(page_title="SANTOSH TGS SNIPER", layout="wide")

# Sniper Dark Theme
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    .sniper-card { 
        background: #161b22; 
        border: 1px solid #30363d; 
        border-radius: 12px; 
        padding: 20px; 
        margin-bottom: 15px;
    }
    .buy-label { color: #2ecc71; font-weight: bold; font-size: 18px; }
    .sell-label { color: #ff3131; font-weight: bold; font-size: 18px; }
    .price-box { background: #0d1117; padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 TGS LIVE SNIPER TERMINAL")

# --- 1. YOUR LIVE CSV LINK ---
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQly4ZQG_WYmZv2s5waDvjO71iG6-W28fqoS7d8Uc_7BeKnZ-6XyXebCdmBth8JVWpm8TEmUYHtwi9f/pub?output=csv"

def load_tgs_data():
    try:
        # Load fresh data from Google Sheet
        df = pd.read_csv(CSV_URL)
        # Filter only POSITIONAL (BUY) and SHORTS (SELL)
        df = df[df['Signal Type'].isin(['POSITIONAL', 'SHORTS'])]
        return df
    except Exception as e:
        return pd.DataFrame()

# --- 2. DISPLAY DASHBOARD ---
df = load_tgs_data()

if not df.empty:
    c1, c2 = st.columns(2)
    for i, (idx, row) in enumerate(df.iterrows()):
        target_col = c1 if i % 2 == 0 else c2
        
        # UI Logic based on TGS Signal Type
        is_buy = row['Signal Type'] == 'POSITIONAL'
        sig_color = "#2ecc71" if is_buy else "#ff3131"
        sig_text = "BUY (POSITIONAL)" if is_buy else "SELL (SHORTS)"
        
        with target_col:
            st.markdown(f"""
                <div class="sniper-card" style="border-left: 6px solid {sig_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 22px; font-weight: bold;">{row['Symbol']}</span>
                        <span style="color: {sig_color}; font-weight: bold;">{sig_text}</span>
                    </div>
                    <div style="color: #888; font-size: 14px; margin-top: 5px;">Live LTP: {row['LTP']}</div>
                    <hr style="border: 0.1px solid #333; margin: 15px 0;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; text-align: center;">
                        <div class="price-box"><small style="color:#888;">ENTRY (High)</small><br><b>{row['High']}</b></div>
                        <div class="price-box"><small style="color:#888;">STOP LOSS</small><br><b style="color:#ff3131;">{row['Stop Loss']}</b></div>
                        <div class="price-box"><small style="color:#888;">TARGET</small><br><b style="color:#58a6ff;">{row['Target']}</b></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("⌛ Waiting for POSITIONAL/SHORTS signals from TGS Sheet...")

# Refresh every 10 seconds to match sheet updates
time.sleep(10)
st.rerun()
