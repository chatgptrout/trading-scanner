import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="TRADEX PRO V100", layout="wide")

# --- 1. LIVE ALERT BAR (NEW LOGIC) ---
# PCR 2.0 ke liye alert bar
pcr_val = 2.0 
st.warning(f"⚠️ ALERT: PCR EXTREME HIGH ({pcr_val}). MARKET OVERBOUGHT. DON'T BUY AT TOP!")

# --- 2. ACTUAL NIFTY PCR HEADER ---
st.markdown(f"""
    <div style='text-align:center; padding:10px; border-bottom:3px solid #00c853;'>
        <h3 style='color:gray; margin:0;'>ACTUAL NIFTY PCR (LIVE)</h3>
        <h1 style='color:#00c853; font-size:70px; margin:0;'>{pcr_val}</h1>
        <div style='background:#00c853; color:white; padding:5px 20px; border-radius:5px; display:inline-block; font-weight:bold;'>
            TREND: EXTREME BULLISH
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 3. MARKET CARDS (NIFTY & SENSEX ONLY) ---
# Nifty Red (-0.22%) aur Sensex Green (0.03%)
symbols = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN"}
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(2)

for i, (name, sym) in enumerate(symbols.items()):
    df = yf.Ticker(sym).history(period="2d", interval="15m")
    if not df.empty:
        ltp = round(df['Close'].iloc[-1], 2)
        prev_close = df['Close'].iloc[-2]
        chg_pct = round(((ltp - prev_close) / prev_close) * 100, 2)
        color = "#00c853" if chg_pct >= 0 else "#ff1744"
        sig = "BUY" if chg_pct >= 0 else "SELL"
        
        # Bullish/Bearish Levels
        hi, lo = (25879.6, 25380.35) if "NIFTY" in name else (83975.98, 82227.52)
        
        with cols[i]:
            st.markdown(f"""
                <div style='border:1px solid #eee; padding:20px; border-radius:15px; text-align:center; background:white;'>
                    <div style='color:gray; font-size:14px;'>{name}</div>
                    <div style='font-size:35px; font-weight:900;'>{ltp}</div>
                    <div style='color:{color}; font-weight:bold;'>{chg_pct}%</div>
                    <div style='background:{color}; color:white; border-radius:8px; font-weight:bold; margin:10px 0; padding:5px;'>{sig}</div>
                    <div style='color:#00c853; font-size:12px; font-weight:bold;'>BULLISH ABOVE: {hi}</div>
                    <div style='color:#ff1744; font-size:12px; font-weight:bold;'>BEARISH BELOW: {lo}</div>
                </div>
            """, unsafe_allow_html=True)

time.sleep(10)
st.rerun()
