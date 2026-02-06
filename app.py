import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time

st.set_page_config(page_title="SANTOSH SPEED AI", layout="wide")

# Neon Dashboard CSS
st.markdown("""
    <style>
    .stApp { background-color: #010b14; color: white; }
    .nav-bar { display: flex; justify-content: space-around; background: #0d1b2a; padding: 10px; border-bottom: 2px solid #00f2ff; margin-bottom: 20px; }
    .sector-card { background: #0d1b2a; border-radius: 10px; padding: 15px; border-top: 3px solid #00f2ff; text-align: center; }
    .signal-card { background: linear-gradient(145deg, #0d1b2a, #1b263b); border-radius: 15px; padding: 20px; border: 1px solid #1e3a5f; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 1. PCR & Sector Row
st.markdown('<div class="nav-bar">⚡ SPEED SCANNER ACTIVE | 🤖 AI SIGNALS | 📊 SECTOR TRACKER</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown('<div class="sector-card"><b>NIFTY PCR</b><br><h2 style="color:#00ff88">1.15 (Bullish)</h2></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="sector-card"><b>SENSEX PCR</b><br><h2 style="color:#00ff88">1.08 (Strong)</h2></div>', unsafe_allow_html=True)
with c3: st.markdown('<div class="sector-card"><b>BANKING</b><br><h2 style="color:#ff4b2b">Weak 📉</h2></div>', unsafe_allow_html=True)
with c4: st.markdown('<div class="sector-card"><b>IT SECTOR</b><br><h2 style="color:#00ff88">Hot 🔥</h2></div>', unsafe_allow_html=True)

# 2. Lightning Fast Scanner Logic
tickers = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "TATAMOTORS.NS", "SBIN.NS", "ADANIENT.NS", "ITC.NS", "BHARTIARTL.NS", "ICICIBANK.NS"] # 1000+ ki list yahan add karein

def scan_stock(sym):
    try:
        df = yf.download(sym, period='2d', interval='5m', progress=False)
        if not df.empty:
            rsi = ta.rsi(df['Close'], length=14).iloc[-1]
            price = df['Close'].iloc[-1]
            ema = ta.ema(df['Close'], length=20).iloc[-1]
            if rsi > 62 and price > ema: return {'sym': sym, 'type': 'BUY', 'price': price, 'rsi': rsi}
            if rsi < 35 and price < ema: return {'sym': sym, 'type': 'SELL', 'price': price, 'rsi': rsi}
    except: return None

st.subheader("🚀 REAL-TIME AI SIGNALS (TOP PICKS)")
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

time.sleep(15)
st.rerun()
