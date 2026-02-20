import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="TRADEX PRO V82", layout="wide")

# --- 1. HEADER (PCR 1.65 REMAINS) ---
pcr_val = 1.65 #
st.markdown(f"""
    <div style='text-align:center; padding:10px; border-bottom:3px solid #00c853;'>
        <h4 style='color:gray; margin:0;'>ACTUAL NIFTY PCR</h4>
        <h1 style='color:#00c853; font-size:55px; margin:0;'>{pcr_val}</h1>
        <div style='background:#00c853; color:white; padding:3px 15px; border-radius:5px; display:inline-block;'>TREND: EXTREME BULLISH</div>
    </div>
""", unsafe_allow_html=True)

# --- 2. INDEX CARDS (VOL + RSI + LEVELS) ---
symbols = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(4)

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="2d", interval="15m")
    if not df.empty:
        ltp = round(df['Close'].iloc[-1], 2)
        hi, lo = round(df['High'].max(), 2), round(df['Low'].min(), 2)
        sig = "BUY" if ltp > df['Close'].ewm(span=9).mean().iloc[-1] else "SELL"
        color = "#00c853" if sig == "BUY" else "#ff1744" #
        
        with cols[i]:
            st.markdown(f"""
                <div style='border:1px solid #eee; padding:15px; border-radius:10px; text-align:center; background:white;'>
                    <div style='color:gray; font-size:12px;'>{name}</div>
                    <div style='font-size:28px; font-weight:900;'>{ltp}</div>
                    <div style='background:{color}; color:white; border-radius:5px; font-weight:bold; margin:5px 0;'>{sig}</div>
                    <div style='color:#00c853; font-size:12px; font-weight:bold; border:1px solid #00c853; margin-top:5px; border-radius:3px; background:#e8f5e9;'>BULLISH ABOVE: {hi}</div>
                    <div style='color:#ff1744; font-size:12px; font-weight:bold; border:1px solid #ff1744; border-radius:3px; background:#ffebee;'>BEARISH BELOW: {lo}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 3. POWER SCANNER (WITH D-HIGH, D-LOW & TARGETS) ---
st.markdown("<br>### 🚀 NIFTY 50 POWER SCANNER (BTST/STBT)")

def get_complete_signals():
    # Top 50 Stocks selection scan
    watchlist = ["SUNPHARMA.NS", "NTPC.NS", "AXISBANK.NS", "TITAN.NS", "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"]
    scan_data = []
    for s in watchlist:
        df = yf.Ticker(s).history(period="1d", interval="15m")
        if not df.empty:
            ltp = round(df['Close'].iloc[-1], 2)
            hi, lo = round(df['High'].max(), 2), round(df['Low'].min(), 2)
            vol_spike = round((df['Volume'].iloc[-1] / df['Volume'].mean()), 1) #
            
            if ltp >= (hi * 0.998): # BTST logic
                scan_data.append({
                    "STOCK": s.split('.')[0], "LTP": ltp, "D-HIGH": hi, "D-LOW": lo, 
                    "VOL SPIKE": f"{vol_spike}x", "ACTION": "BTST ✅", "TARGET": round(ltp * 1.01, 2)
                })
    return pd.DataFrame(scan_data)

df_final = get_complete_signals()
if not df_final.empty:
    st.table(df_final) #
else:
    st.info("Scanning Market... High momentum stocks will appear here.")

time.sleep(10)
st.rerun()
