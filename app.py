import streamlit as st
import yfinance as yf
import pandas_ta as ta
from concurrent.futures import ThreadPoolExecutor
import time

st.set_page_config(page_title="SANTOSH SHIKARI AI", layout="wide")

# Updated Aggressive Tickers (Midcap + IT + High Volume)
shikari_list = [
    "RELIANCE.NS", "TATAMOTORS.NS", "SBIN.NS", "ADANIENT.NS", "HDFCBANK.NS", 
    "INFY.NS", "TCS.NS", "WIPRO.NS", "HAL.NS", "ZOMATO.NS", "DIXON.NS", 
    "VOLTAS.NS", "BHARTIARTL.NS", "BEL.NS", "BHEL.NS", "TRENT.NS"
]

def scan_shikari(sym):
    try:
        df = yf.download(sym, period='2d', interval='5m', progress=False)
        if not df.empty and len(df) > 14:
            rsi = ta.rsi(df['Close'], length=14).iloc[-1]
            price = df['Close'].iloc[-1]
            ema = ta.ema(df['Close'], length=20).iloc[-1]
            
            # Aggressive Logic: RSI 55+ and Price > EMA (Buy)
            # RSI 42- and Price < EMA (Sell)
            if rsi > 55 and price > ema: 
                return {'sym': sym, 'type': 'BUY', 'price': price, 'rsi': rsi}
            if rsi < 42 and price < ema: 
                return {'sym': sym, 'type': 'SELL', 'price': price, 'rsi': rsi}
    except: return None

# UI Header
st.markdown('<h2 style="text-align:center; color:#00f2ff;">⚡ SHIKARI MOMENTUM SCANNER ACTIVE</h2>', unsafe_allow_html=True)

with ThreadPoolExecutor(max_workers=15) as executor:
    results = list(executor.map(scan_shikari, shikari_list))
    active_signals = [r for r in results if r]

if active_signals:
    for s in active_signals:
        color = "#00ff88" if s['type'] == 'BUY' else "#ff4b2b"
        st.markdown(f'''
            <div style="background:#0d1b2a; padding:15px; border-radius:10px; border-left:10px solid {color}; margin-bottom:10px;">
                <h3 style="color:{color}; margin:0;">{s['type']} | {s['sym']}</h3>
                <p style="font-size:22px; margin:5px 0;">Price: ₹{s['price']:.2f} | RSI: {s['rsi']:.1f}</p>
                <p style="color:#a0a0a0;">Target: ₹{s['price']*1.015:.2f} | SL: ₹{s['price']*0.99:.2f}</p>
            </div>
        ''', unsafe_allow_html=True)
else:
    st.warning("Still searching for aggressive moves... 📡")

time.sleep(15)
st.rerun()
