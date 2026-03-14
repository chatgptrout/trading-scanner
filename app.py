import streamlit as st
import pandas as pd
from stoxkart_superr import SuperrApi
from datetime import datetime
import pytz
import yfinance as yf

# Page Config
st.set_page_config(page_title="Stoxkart Pro Scanner", layout="wide")

# 🕒 Live Indian Clock (IST)
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime('%Y-%m-%d | %H:%M:%S')

st.title("🚀 Pro Breakout Scanner")
st.subheader(f"🕒 Last Sync: {current_time} (IST)")

# 🔑 Stoxkart API Details (Aapne jo generate ki thi)
API_KEY = "6H4YuzLo1MqUgBoC"
API_SECRET = "VA6LpKmAM1Ejii8AFkR00m" # Ise screenshot se poora check karke bharein
CLIENT_ID = "SQ38296"

def get_market_data():
    # Stocks ki list
    stocks = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'INFY.NS', 'BHARTIARTL.NS', 'SBIN.NS', 'ITC.NS', 'ADANIENT.NS']
    
    results = []
    for symbol in stocks:
        # Data fetch karna (yfinance abhi backup ke liye hai)
        data = yf.download(symbol, period='2d', interval='5m', progress=False)
        
        if not data.empty:
            current_price = float(data['Close'].iloc[-1])
            prev_high = float(data['High'].iloc[:-1].max())
            prev_low = float(data['Low'].iloc[:-1].min())
            
            # 🎯 Target/SL Calculation
            target = prev_high * 1.01
            sl = prev_high * 0.995
            
            # 📊 OI Column Logic (Stoxkart API se connect hone par ye live ho jayega)
            # Abhi ke liye hum placeholder dikhayenge
            oi_val = "1.2Cr" if "NIFTY" in symbol else "45.8L"
            
            status = "🚀 BREAKOUT" if current_price > prev_high else "📉 BREAKDOWN" if current_price < prev_low else "⚖️ WAIT"
            
            results.append({
                "Stock": symbol.replace(".NS", ""),
                "Price": round(current_price, 2),
                "Buy Above": round(prev_high, 2),
                "Target (1%)": round(target, 2),
                "Stop Loss": round(sl, 2),
                "OI (Open Interest)": oi_val,  # Ye naya column hai
                "Status": status
            })
            
    return pd.DataFrame(results)

# Dashboard Display
df = get_market_data()
st.table(df)

if st.button('🔄 Refresh & Sync Stoxkart OI'):
    st.rerun()
