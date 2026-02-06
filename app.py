import streamlit as st
import yfinance as yf
import pandas_ta as ta
from concurrent.futures import ThreadPoolExecutor
import time

st.set_page_config(page_title="SANTOSH VOLUME HUNTER", layout="wide")

# Nifty 50 Full List
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

def volume_scan(sym):
    try:
        df = yf.download(sym, period='2d', interval='5m', progress=False)
        if not df.empty and len(df) > 15:
            # Indicators
            rsi = ta.rsi(df['Close'], length=14).iloc[-1]
            price = df['Close'].iloc[-1]
            ema = ta.ema(df['Close'], length=20).iloc[-1]
            
            # Volume Logic: Current Volume vs Average of last 5 candles
            avg_vol = df['Volume'].iloc[-6:-1].mean()
            curr_vol = df['Volume'].iloc[-1]
            vol_spike = curr_vol / avg_vol if avg_vol > 0 else 0
            
            # Aggressive Strategy: RSI > 52 + Price > EMA + Volume Spike > 1.5
            if rsi > 52 and price > ema and vol_spike > 1.5:
                return {'sym': sym, 'type': 'BUY', 'price': price, 'rsi': rsi, 'vol': vol_spike}
            if rsi < 48 and price < ema and vol_spike > 1.5:
                return {'sym': sym, 'type': 'SELL', 'price': price, 'rsi': rsi, 'vol': vol_spike}
    except: return None

st.markdown('<h1 style="text-align:center; color:#00f2ff;">🦅 VOLUME HUNTER AI: NIFTY 50</h1>', unsafe_allow_html=True)

with ThreadPoolExecutor(max_workers=20) as executor:
    results = list(executor.map(volume_scan, nifty50_tickers))
    found_signals = [r for r in results if r]

if found_signals:
    for s in found_signals:
        color = "#00ff88" if s['type'] == 'BUY' else "#ff4b2b"
        st.markdown(f'''
            <div style="background:#0d1b2a; padding:15px; border-radius:10px; border-left:10px solid {color}; margin-bottom:10px;">
                <h3 style="color:{color}; margin:0;">{s['type']} | {s['sym']} (Vol: {s['vol']:.1f}x)</h3>
                <p style="font-size:22px; margin:5px 0;">Price: ₹{s['price']:.2f} | RSI: {s['rsi']:.1f}</p>
                <p style="color:#00f2ff; font-weight:bold;">🎯 Target: ₹{s['price']*1.01:.2f} | 🛑 SL: ₹{s['price']*0.995:.2f}</p>
            </div>
        ''', unsafe_allow_html=True)
else:
    st.info("Scanning for Volume Spikes in Nifty 50... 📡
