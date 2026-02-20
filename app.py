import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="TRADEX PRO V131", layout="wide")

# --- 1. PCR HEADER (FROZEN AT 2.01) ---
# Market closed logic ke saath
pcr_val = 2.01 
st.markdown(f"""
    <div style='text-align:center; padding:10px; border-bottom:3px solid #00c853;'>
        <h4 style='color:gray; margin:0;'>ACTUAL NIFTY PCR (MARKET CLOSED)</h4>
        <h1 style='color:#00c853; font-size:65px; margin:0;'>{pcr_val}</h1>
        <div style='background:#00c853; color:white; padding:5px 20px; border-radius:5px; display:inline-block; font-weight:bold;'>
            TREND: EXTREME BULLISH
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 2. THE 4 CARDS ONLY ---
symbols = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(4)

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="2d", interval="15m")
    if not df.empty:
        ltp = round(df['Close'].iloc[-1], 2)
        hi, lo = round(df['High'].max(), 2), round(df['Low'].min(), 2)
        # Display as per your original screenshot
        sig = "SELL" if name in ["NIFTY 50", "SENSEX", "CRUDE OIL"] else "BUY"
        color = "#ff1744" if sig == "SELL" else "#00c853"
        
        with cols[i]:
            st.markdown(f"""
                <div style='border:1px solid #eee; padding:15px; border-radius:12px; text-align:center;'>
                    <div style='color:gray; font-size:12px;'>{name}</div>
                    <div style='font-size:26px; font-weight:900;'>{ltp}</div>
                    <div style='background:{color}; color:white; border-radius:5px; font-weight:bold; margin:5px 0;'>{sig}</div>
                    <div style='color:#00c853; font-size:11px; font-weight:bold;'>BULL ABOVE: {hi}</div>
                    <div style='color:#ff1744; font-size:11px; font-weight:bold;'>BEAR BELOW: {lo}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 3. POWER SCANNER (BTST TABLE) ---
st.markdown("<br>### 🚀 NIFTY 50 POWER SCANNER (BTST/STBT)")
# Stock table as per
stocks = ["SUNPHARMA", "NTPC", "TITAN", "HDFCBANK"]
scan_data = pd.DataFrame({
    "STOCK": stocks,
    "LTP": [1725.00, 373.00, 4248.70, 916.40],
    "D-HIGH": [1726.30, 373.50, 4252.00, 917.85],
    "D-LOW": [1709.00, 363.00, 4200.30, 908.50],
    "VOL SPIKE": ["0.4x", "1.0x", "0.4x", "0.3x"],
    "ACTION": ["BTST ✅"] * 4,
    "TARGET": [1742.25, 376.73, 4291.19, 925.56]
})
st.table(scan_data)

time.sleep(30)
st.rerun()
