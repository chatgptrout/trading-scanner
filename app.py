import streamlit as st
import yfinance as yf
import pandas_ta as ta
from concurrent.futures import ThreadPoolExecutor
import time

st.set_page_config(page_title="SANTOSH EAGLE EYE", layout="wide")

nifty50_tickers = [
    "ADANIENT.NS", "AXISBANK.NS", "BAJFINANCE.NS", "BHARTIARTL.NS", "HDFCBANK.NS",
    "ICICIBANK.NS", "INFY.NS", "ITC.NS", "LT.NS", "M&M.NS", "RELIANCE.NS", "SBIN.NS",
    "TCS.NS", "TATAMOTORS.NS", "WIPRO.NS", "ZOMATO.NS", "HAL.NS", "DIXON.NS"
]

def eagle_scan(sym):
    try:
        df = yf.download(sym, period='2d', interval='5m', progress=False)
        if not df.empty and len(df) > 10:
            rsi = ta.rsi(df['Close'], length=14).iloc[-1]
            price = df['Close'].iloc[-1]
            ema = ta.ema(df['Close'], length=20).iloc[-1]
            avg_vol = df['Volume'].iloc[-6:-1].mean()
            vol_spike = df['Volume'].iloc[-1] / avg_vol if avg_vol > 0 else 0
            
            if rsi > 52 and price > ema and vol_spike > 1.2:
                return {'sym': sym, 'type': 'BUY', 'price': price, 'rsi': rsi}
            if rsi < 48 and price < ema and vol_spike > 1.2:
                return {'sym': sym, 'type': 'SELL', 'price': price, 'rsi': rsi}
    except: return None

st.markdown('<h1 style="text-align:center; color:#00f2ff;">🦅 EAGLE EYE AI SCANNER</h1>', unsafe_allow_html=True)

with ThreadPoolExecutor(max_workers=15) as executor:
    results = list(executor.map(eagle_scan, nifty50_tickers))
    signals = [r for r in results if r]

if signals:
    for s in signals:
        color = "#00ff88" if s['type'] == 'BUY' else "#ff4b2b"
        st.markdown(f'''
            <div style="background:#0d1b2a; padding:15px; border-radius:10px; border-left:10px solid {color}; margin-bottom:10px;">
                <h3 style="color:{color}; margin:0;">{s['type']} | {s['sym']}</h3>
                <p style="font-size:20px; margin:5px 0;">Price: ₹{s['price']:.2f} | RSI: {s['rsi']:.1f}</p>
            </div>
        ''', unsafe_allow_html=True)
else:
    st.info("Searching for volume breakouts... 📡")

time.sleep(10)
st.rerun()
