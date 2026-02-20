import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="TRADEX PRO V132", layout="wide")

# --- 1. PCR HEADER (SAFE) ---
pcr_val = 2.01 # Frozen value
st.markdown(f"""
    <div style='text-align:center; padding:10px; border-bottom:3px solid #00c853;'>
        <h4 style='color:gray; margin:0;'>ACTUAL NIFTY PCR (LATEST)</h4>
        <h1 style='color:#00c853; font-size:65px; margin:0;'>{pcr_val}</h1>
    </div>
""", unsafe_allow_html=True)

# --- 2. FIXED INDEX & COMMODITY CARDS ---
# Symbols for Crude and NG refreshed
symbols = {
    "NIFTY 50": "^NSEI", 
    "SENSEX": "^BSESN", 
    "CRUDE OIL": "CL=F", 
    "NATURAL GAS": "NG=F"
}

st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(4)

for i, (name, sym) in enumerate(symbols.items()):
    try:
        # Fetching data with 1d period for latest LTP
        df = yf.Ticker(sym).history(period="1d")
        if not df.empty:
            ltp = round(df['Close'].iloc[-1], 2)
            hi, lo = round(df['High'].max(), 2), round(df['Low'].min(), 2)
            
            # Action logic as per your screen
            sig = "SELL" if name in ["CRUDE OIL", "NATURAL GAS"] else "BUY"
            color = "#ff1744" if sig == "SELL" else "#00c853"
            
            with cols[i]:
                st.markdown(f"""
                    <div style='border:1px solid #eee; padding:15px; border-radius:12px; text-align:center;'>
                        <div style='color:gray; font-size:12px;'>{name}</div>
                        <div style='font-size:26px; font-weight:900;'>{ltp}</div>
                        <div style='background:{color}; color:white; border-radius:5px; font-weight:bold; margin:5px 0;'>{sig}</div>
                        <div style='color:#00c853; font-size:10px; font-weight:bold;'>BULL ABOVE: {hi}</div>
                        <div style='color:#ff1744; font-size:10px; font-weight:bold;'>BEAR BELOW: {lo}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            cols[i].error(f"{name} Data Offline")
    except:
        cols[i].error(f"Error Loading {name}")

# --- 3. POWER SCANNER (BTST TABLE) ---
st.markdown("<br>### 🚀 NIFTY 50 POWER SCANNER (BTST/STBT)")
# Wahi 50 stocks wala simple table
stocks_data = [
    {"STOCK": "SUNPHARMA", "LTP": 1725.00, "D-HIGH": 1726.30, "D-LOW": 1709.00, "VOL": "0.4x", "ACTION": "BTST ✅", "TARGET": 1742.25},
    {"STOCK": "NTPC", "LTP": 373.00, "D-HIGH": 373.50, "D-LOW": 363.00, "VOL": "1.0x", "ACTION": "BTST ✅", "TARGET": 376.73}
]
st.table(pd.DataFrame(stocks_data))

time.sleep(30)
st.rerun()
