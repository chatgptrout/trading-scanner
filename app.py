import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import time

st.set_page_config(page_title="SANTOSH AI COMMANDER", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #010b14; color: white; }
    .nav-bar { display: flex; justify-content: space-around; background: #0d1b2a; padding: 15px; border-bottom: 2px solid #00f2ff; margin-bottom: 20px; color: #00f2ff; font-weight: bold; }
    .pro-card { background: #0d1b2a; padding: 20px; border-radius: 15px; border: 1px solid #1e3a5f; margin-bottom: 15px; }
    .signal-text { font-size: 18px; font-weight: bold; margin-bottom: 10px; }
    .buy-color { color: #00ff88; }
    .sell-color { color: #ff4b2b; }
    .price-tag { font-size: 24px; font-weight: bold; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="nav-bar"><span>🚀 NIFTY 1000+ AI SCANNER ACTIVE</span></div>', unsafe_allow_html=True)

# List of stocks to scan
tickers = ["RELIANCE.NS", "TATAMOTORS.NS", "SBIN.NS", "ADANIENT.NS", "NIFTYBEES.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "TCS.NS", "ITC.NS"]

st.subheader("🎯 LIVE TRADE SIGNALS (WITH TARGET & SL)")

momentum_list = []

with st.spinner('Calculating Signals...'):
    for sym in tickers:
        try:
            df = yf.download(sym, period='5d', interval='15m', progress=False)
            if not df.empty and len(df) > 20:
                df['EMA'] = ta.ema(df['Close'], length=20)
                df['RSI'] = ta.rsi(df['Close'], length=14)
                df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)
                
                price = df['Close'].iloc[-1]
                rsi = df['RSI'].iloc[-1]
                ema = df['EMA'].iloc[-1]
                atr = df['ATR'].iloc[-1]
                
                # Logic for Entry, Target, SL
                if price > ema and rsi > 62:
                    sl = price - (1.5 * atr)
                    target = price + (2.5 * atr)
                    momentum_list.append({'Symbol': sym, 'Type': 'BUY', 'Price': price, 'SL': sl, 'Target': target, 'RSI': rsi})
                elif price < ema and rsi < 35:
                    sl = price + (1.5 * atr)
                    target = price - (2.5 * atr)
                    momentum_list.append({'Symbol': sym, 'Type': 'SELL', 'Price': price, 'SL': sl, 'Target': target, 'RSI': rsi})
        except:
            continue

# Display Signals in Rows
if momentum_list:
    for row in momentum_list:
        color_class = "buy-color" if row['Type'] == 'BUY' else "sell-color"
        st.markdown(f'''
            <div class="pro-card">
                <div style="display:flex; justify-content:space-between">
                    <div>
                        <span class="signal-text {color_class}">{row['Type']} SIGNAL: {row['Symbol']}</span><br>
                        <span class="price-tag">Entry: ₹{row['Price']:.2f}</span>
                    </div>
                    <div style="text-align:right">
                        <span style="color:#00ff88">🎯 Target: ₹{row['Target']:.2f}</span><br>
                        <span style="color:#ff4b2b">🛑 SL: ₹{row['SL']:.2f}</span>
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
else:
    st.info("Searching for high-probability signals... 📡")

time.sleep(60)
st.rerun()
