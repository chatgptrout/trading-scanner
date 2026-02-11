import streamlit as st
import pandas as pd
import time

# --- PAGE SETUP ---
st.set_page_config(page_title="TGS SNIPER LIVE", layout="wide")

# --- CUSTOM WHITE THEME ---
st.markdown("""
    <style>
    /* Main Background White */
    .stApp { background-color: #ffffff; color: #1e1e1e; }
    
    /* Sniper Card Styling */
    .sniper-card { 
        background: #f8f9fa; 
        border: 1px solid #e0e0e0; 
        border-radius: 12px; 
        padding: 20px; 
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Text Colors */
    .stock-name { font-size: 22px; font-weight: bold; color: #1a1a1a; }
    .label-text { color: #666; font-size: 12px; font-weight: bold; text-transform: uppercase; }
    .price-value { font-size: 18px; font-weight: bold; color: #2c3e50; }
    
    /* Signal Colors */
    .buy-border { border-left: 8px solid #28a745; }
    .sell-border { border-left: 8px solid #dc3545; }
    .buy-text { color: #28a745; font-weight: bold; }
    .sell-text { color: #dc3545; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1a1a1a;'>🎯 TGS LIVE SNIPER TERMINAL</h1>", unsafe_allow_html=True)

# --- 1. YOUR LIVE CSV LINK ---
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQly4ZQG_WYmZv2s5waDvjO71iG6-W28fqoS7d8Uc_7BeKnZ-6XyXebCdmBth8JVWpm8TEmUYHtwi9f/pub?output=csv"

def load_tgs_data():
    try:
        # Sheet se direct fresh data load karega
        df = pd.read_csv(CSV_URL)
        # Filter: Sirf POSITIONAL (BUY) aur SHORTS (SELL)
        df = df[df['Signal Type'].isin(['POSITIONAL', 'SHORTS'])]
        return df
    except:
        return pd.DataFrame()

# --- 2. DISPLAY DASHBOARD ---
df = load_tgs_data()

if not df.empty:
    c1, c2 = st.columns(2)
    for i, (idx, row) in enumerate(df.iterrows()):
        target_col = c1 if i % 2 == 0 else c2
        
        # UI Logic based on TGS Sheet columns
        is_buy = row['Signal Type'] == 'POSITIONAL'
        card_class = "buy-border" if is_buy else "sell-border"
        sig_text = "BUY" if is_buy else "SELL"
        sig_class = "buy-text" if is_buy else "sell-text"
        
        with target_col:
            st.markdown(f"""
                <div class="sniper-card {card_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="stock-name">{row['Symbol']}</span>
                        <span class="{sig_class}">{sig_text} ({row['Signal Type']})</span>
                    </div>
                    <div style="color: #555; font-size: 14px; margin-top: 5px;">Live LTP: <b>{row['LTP']}</b></div>
                    <hr style="border: 0.5px solid #eee; margin: 15px 0;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; text-align: center;">
                        <div><div class="label-text">ENTRY (High)</div><div class="price-value">{row['High']}</div></div>
                        <div><div class="label-text">STOP LOSS</div><div class="price-value" style="color:#dc3545;">{row['Stop Loss']}</div></div>
                        <div><div class="label-text">TARGET</div><div class="price-value" style="color:#007bff;">{row['Target']}</div></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("⌛ Waiting for POSITIONAL/SHORTS signals from TGS Sheet... (Background White Active)")

# Auto-refresh logic (5-10 seconds for Google Sheets sync)
time.sleep(10)
st.rerun()
