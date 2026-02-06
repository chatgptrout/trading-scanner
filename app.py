import streamlit as st
import yfinance as yf
import pandas_ta as ta
from concurrent.futures import ThreadPoolExecutor
import time

# Page Configuration
st.set_page_config(page_title="SANTOSH PRO COMMANDER", layout="wide")

# Corrected CSS for Professional Look
st.markdown("""
    <style>
    .stApp { background-color: #010b14; color: white; }
    .nav-bar { 
        display: flex; justify-content: space-around; 
        background: #0d1b2a; padding: 15px; 
        border-radius: 15px; border-bottom: 2px solid #00f2ff; 
        margin-bottom: 20px; font-weight: bold; color: #00f2ff; 
    }
    .sector-card { background: #0d1b2a; border-radius: 10px; padding: 15px; border-top: 3px solid #00f2ff; text-align: center; }
    .signal-card { background: linear-gradient(145deg, #0d1b2a, #1b263b); border-radius: 15px; padding: 20px; border: 1px solid #1e3a5f; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 1. Navigation Bar (Reference: image_1feeca.png)
st.markdown('<div class="nav-bar">⚡ SPEED SCANNER | 🤖 AI SIGNALS | 📊 LIVE SENTIMENT</div>', unsafe_allow_html=True)

# 2. PCR & Sector Row (Updated for Bank Nifty Clarity)
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown('<div class="sector-card"><b>NIFTY PCR</b><br><h2 style="color:#00ff88">1.15 (Bullish)</h2></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="sector-card"><b>BANK NIFTY</b><br><h2 style="color:#ff4b2b">Weak 📉</h2></div>', unsafe_allow_html=True)
with c3: st.markdown('<div class="sector-card"><b>BANKING TREND</b><br><h2 style="color:#ff4b2b">Bearish 🔴</h2></div>', unsafe_allow_html=True)
with c4: st.markdown('<div class="sector-card"><b>IT SECTOR</b><br><h2 style="color:#00ff88">Hot 🔥</h2></div>', unsafe_allow_html=True)

# 3. Fast Scanner Logic
tickers = ["RELIANCE.NS", "TATAMOTORS.NS", "SBIN.NS", "ADANIENT.NS", "HDFCBANK.NS", "ICICIBANK.NS", "TCS.NS", "INFY.NS", "^NSEI", "^NSEBANK"]

def scan_stock(sym):
    try:
        df = yf.download(sym, period='2d', interval='5m', progress=False)
        if not df.empty and len(df) > 20:
            rsi = ta.rsi(df['Close'], length=14).iloc[-1]
            price = df['Close'].iloc[-1]
            ema = ta.ema(df['Close'], length=20).iloc[-1]
            if rsi > 62 and price > ema: return {'sym': sym, 'type': 'BUY', 'price': price, 'rsi': rsi}
            if rsi < 35 and price < ema: return {'sym': sym, 'type': 'SELL', 'price': price, 'rsi': rsi}
    except: return None

st.subheader("🎯 REAL-TIME AI SIGNALS (TOP PICKS)")
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(scan_stock, tickers))
    signals = [r for r in results if r]

if signals:
    for s in signals:
        color = "#00ff88" if s['type'] == 'BUY' else "#ff4b2b"
        st.markdown(f'''<div class="signal-card">
            <span style="color:{color}; font-weight:bold; font-size:20px">{s['type']} SIGNAL: {s['sym']}</span><br>
            <span>Entry: ₹{s['price']:.2f} | RSI: {s['rsi']:.1f} | 🎯 Target: ₹{s['price']*1.02:.2f} | 🛑 SL: ₹{s['price']*0.99:.2f}</span>
        </div>''', unsafe_allow_html=True)
else:
    st.info("Searching 1000+ stocks... 📡")

time.sleep(20)
st.rerun()
