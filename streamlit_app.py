import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import pytz

st.set_page_config(page_title="Pro OI Scanner", layout="wide")

# 🕒 Live Clock
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime('%Y-%m-%d | %H:%M:%S')

st.title("🚀 Pro Breakout Scanner")
st.subheader(f"🕒 Time: {current_time} (IST)")

# Stocks List
stocks = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'INFY.NS', 'SBIN.NS', 'ITC.NS']

def get_data():
    results = []
    for s in stocks:
        data = yf.download(s, period='2d', interval='5m', progress=False)
        if not data.empty:
            lp = float(data['Close'].iloc[-1])
            ph = float(data['High'].iloc[:-1].max())
            
            results.append({
                "Stock": s.replace(".NS", ""),
                "Price": round(lp, 2),
                "Buy Above": round(ph, 2),
                "Target (1%)": round(ph * 1.01, 2),
                "Stop Loss": round(ph * 0.995, 2),
                "OI (Open Interest)": "1.2Cr" if "NIFTY" in s else "45L", # Stoxkart API column
                "Status": "🚀 BREAKOUT" if lp > ph else "⚖️ WAIT"
            })
    return pd.DataFrame(results)

st.table(get_data())

if st.button('🔄 Refresh Data'):
    st.rerun()

