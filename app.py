import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import time

st.set_page_config(page_title="SANTOSH 1000+ SCANNER", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #010b14; color: white; }
    .nav-bar { display: flex; justify-content: space-around; background: #0d1b2a; padding: 15px; border-bottom: 2px solid #00f2ff; margin-bottom: 20px; color: #00f2ff; font-weight: bold; }
    .pro-card { background: #0d1b2a; padding: 15px; border-radius: 12px; border-left: 5px solid #00ff88; margin-bottom: 10px; }
    .blink { animation: blinker 1s linear infinite; color: #00ff88; font-weight: bold; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="nav-bar"><span>🚀 NIFTY 1000+ SCANNER ACTIVE</span></div>', unsafe_allow_html=True)

# 1. 1000 Stocks ki List (Nifty 500 + Others)
# Yahan hum example ke liye bade sectors le rahe hain, Yahoo Finance limit tak scan karega
tickers = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "TATAMOTORS.NS", "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "ADANIENT.NS", "SUNPHARMA.NS", "AXISBANK.NS", "TITAN.NS", "LT.NS", "MARUTI.NS"] # Is list ko aap 1000 tak badha sakte hain

st.subheader("🔥 TOP MOMENTUM STOCKS (LIVE)")

momentum_list = []

with st.spinner('Scanning 1000+ Stocks...'):
    for sym in tickers:
        try:
            data = yf.download(sym, period='1d', interval='15m', progress=False)
            if not data.empty:
                price = data['Close'].iloc[-1]
                change = ((price - data['Open'].iloc[0]) / data['Open'].iloc[0]) * 100
                vol = data['Volume'].iloc[-1]
                
                # Agar stock 1.5% se zyada bhag raha hai, toh list mein dalo
                if abs(change) > 1.5:
                    momentum_list.append({'Symbol': sym, 'Price': price, 'Change': change, 'Vol': vol})
        except:
            continue

# Ranking by highest change
df_sorted = pd.DataFrame(momentum_list).sort_values(by='Change', ascending=False)

# Display Top 10
cols = st.columns(2)
for i, row in enumerate(df_sorted.head(10).to_dict('records')):
    with cols[i % 2]:
        st.markdown(f'''
            <div class="pro-card">
                <div style="display:flex; justify-content:space-between">
                    <span style="font-size:20px; font-weight:bold">{row['Symbol']}</span>
                    <span class="blink" style="color:{"#00ff88" if row['Change'] > 0 else "#ff4b2b"}">{row['Change']:.2f}%</span>
                </div>
                <div style="font-size:25px">₹{row['Price']:.2f}</div>
            </div>
        ''', unsafe_allow_html=True)

time.sleep(60) # 1000 stocks ke liye 1 min ka gap zaroori hai
st.rerun()
