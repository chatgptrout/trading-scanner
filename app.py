import streamlit as st
import yfinance as yf
import pandas_ta as ta
from concurrent.futures import ThreadPoolExecutor
import time

st.set_page_config(page_title="SANTOSH ULTRA SHIKARI", layout="wide")

# Nifty 50 Full List for 100% Coverage
nifty50_tickers = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
    "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BPCL.NS", "BHARTIARTL.NS",
    "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS",
    "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS",
    "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ITC.NS",
    "INDUSINDBK.NS", "INFY.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS",
    "M&M.NS", "MARUTI.NS", "NTPC.NS", "NESTLEIND.NS", "ONGC.NS",
    "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SUNPHARMA.NS",
    "TCS.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TECHM.NS",
    "TITAN.NS", "ULTRACEMCO.NS", "UPL.NS", "WIPRO.NS"
]

def ultra_scan(sym):
    try:
        df = yf.download(sym, period='2d', interval='5m', progress=False)
        if not df.empty and len(df) > 10:
            rsi = ta.rsi(df['Close'], length=14).iloc[-1]
            price = df['Close'].iloc[-1]
            ema = ta.ema(df['Close'], length=20).iloc[-1]
            
            # Ultra Aggressive Logic: RSI 52+ (Buy) | RSI 48- (Sell)
            if rsi > 52 and price > ema: 
                return {'sym': sym, 'type': 'BUY', 'price': price, 'rsi': rsi}
            if rsi < 48 and price < ema: 
                return {'sym': sym, 'type': 'SELL', 'price': price, 'rsi': rsi}
    except: return None

st.markdown('<h1 style="text-align:center; color:#00f2ff;">🦅 ULTRA SHIKARI: NIFTY 50 LIVE</h1>', unsafe_allow_html=True)

with ThreadPoolExecutor(max_workers=20) as executor:
    results = list(executor.map(ultra_scan, nifty50_tickers))
    found_signals = [r for r in results if r]

if found_signals:
    cols = st.columns(2)
    for i, s in enumerate(found_signals):
        color = "#00ff88" if s['type'] == 'BUY' else "#ff4b2b"
        with cols[i % 2]:
            st.markdown(f'''
                <div style="background:#0d1b2a; padding:15px; border-radius:10px; border-left:8px solid {color}; margin-bottom:10px;">
                    <h3 style="color:{color}; margin:0;">{s['type']} | {s['sym']}</h3>
                    <p style="font-size:20px; margin:5px 0;">Price: ₹{s['price']:.2f} | RSI: {s['rsi']:.1f}</p>
                </div>
            ''', unsafe_allow_html=True)
else:
    st.info("Searching all 50 Nifty stocks for any micro-move... 📡")

time.sleep(10)
st.rerun()
