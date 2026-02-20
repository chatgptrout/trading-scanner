import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="TRADEX PRO V81", layout="wide")

# --- 1. DYNAMIC HEADER (PCR REMAINS 1.65) ---
pcr_val = 1.65 #
st.markdown(f"""
    <div style='text-align:center; padding:10px; border-bottom:3px solid #00c853;'>
        <h4 style='color:gray; margin:0;'>ACTUAL NIFTY PCR</h4>
        <h1 style='color:#00c853; font-size:55px; margin:0;'>{pcr_val}</h1>
        <div style='background:#00c853; color:white; padding:3px 15px; border-radius:5px; display:inline-block;'>TREND: EXTREME BULLISH</div>
    </div>
""", unsafe_allow_html=True)

# --- 2. INDEX CARDS WITH VOLUME, RSI & LEVELS ---
symbols = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(4)

def get_rsi(ticker_sym):
    data = yf.Ticker(ticker_sym).history(period="1mo", interval="15m")
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    return round(100 - (100 / (1 + rs)).iloc[-1], 2)

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="2d", interval="15m")
    if not df.empty:
        ltp = round(df['Close'].iloc[-1], 2)
        hi, lo = round(df['High'].max(), 2), round(df['Low'].min(), 2)
        sig = "BUY" if ltp > df['Close'].ewm(span=9).mean().iloc[-1] else "SELL"
        color = "#00c853" if sig == "BUY" else "#ff1744"
        
        # New Volume & RSI Logic
        vol_status = "HIGH ⚡" if df['Volume'].iloc[-1] > df['Volume'].mean() else "LOW ☁️"
        rsi_val = get_rsi(sym)
        
        with cols[i]:
            st.markdown(f"""
                <div style='border:1px solid #eee; padding:15px; border-radius:10px; text-align:center; background:white;'>
                    <div style='color:gray; font-size:12px;'>{name}</div>
                    <div style='font-size:28px; font-weight:900;'>{ltp}</div>
                    <div style='background:{color}; color:white; border-radius:5px; font-weight:bold; margin:5px 0;'>{sig}</div>
                    <div style='color:#1a237e; font-size:13px; font-weight:bold;'>VOL: {vol_status} | RSI: {rsi_val}</div>
                    <div style='color:#00c853; font-size:12px; font-weight:bold; border:1px solid #00c853; margin-top:5px; border-radius:3px; background:#e8f5e9;'>BULLISH ABOVE: {hi}</div>
                    <div style='color:#ff1744; font-size:12px; font-weight:bold; border:1px solid #ff1744; border-radius:3px; background:#ffebee;'>BEARISH BELOW: {lo}</div>
                </div>
            """, unsafe_allow_html=True)

# --- 3. POWER SCANNER (WITH NEXT TARGETS) ---
st.markdown("<br>### 🚀 NIFTY 50 POWER SCANNER (BTST/STBT)")

def get_btst_with_targets():
    watchlist = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "SUNPHARMA.NS", "NTPC.NS"]
    results = []
    for s in watchlist:
        df = yf.Ticker(s).history(period="1d", interval="15m")
        if not df.empty:
            ltp = round(df['Close'].iloc[-1], 2)
            hi, lo = df['High'].max(), df['Low'].min()
            vol_spike = round((df['Volume'].iloc[-1] / df['Volume'].mean()), 1)
            
            if ltp >= (hi * 0.998): # Breakout
                target = round(ltp * 1.01, 2) # 1% Target
                results.append({"STOCK": s.split('.')[0], "LTP": ltp, "VOL SPIKE": f"{vol_spike}x", "ACTION": "BTST ✅", "TARGET": target})
    return pd.DataFrame(results)

df_btst = get_btst_with_targets()
if not df_btst.empty:
    st.table(df_btst) #
else:
    st.info("Scanning for Momentum Breakouts...")

time.sleep(10)
st.rerun()
