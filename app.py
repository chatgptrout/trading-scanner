import streamlit as st
import yfinance as yf
import time
from datetime import datetime
import pytz

st.set_page_config(page_title="TRADEX PRO V66", layout="wide")

# --- NEON STYLE WITH LEVELS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    .price-card { 
        background: linear-gradient(145deg, #111, #1a1a1a);
        padding: 20px; border-radius: 15px; 
        border: 1px solid #333; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .buy-btn { background: #00ff88; color: black; padding: 5px 15px; border-radius: 8px; font-weight: 900; }
    .sell-btn { background: #ff3e3e; color: white; padding: 5px 15px; border-radius: 8px; font-weight: 900; }
    .levels { font-size: 13px; margin-top: 10px; font-weight: bold; padding: 5px; border-radius: 5px; }
    .bull-text { color: #00ff88; border: 1px solid #00ff88; }
    .bear-text { color: #ff3e3e; border: 1px solid #ff3e3e; }
    </style>
    """, unsafe_allow_html=True)

def get_live_data_with_levels():
    symbols = {
        "NIFTY 50": "^NSEI", 
        "BANK NIFTY": "^NSEBANK",
        "CRUDE OIL": "CL=F", 
        "NATURAL GAS": "NG=F"
    }
    data = []
    for name, sym in symbols.items():
        df = yf.Ticker(sym).history(period="5d", interval="15m")
        if not df.empty:
            ltp = round(df['Close'].iloc[-1], 2)
            high_24h = round(df['High'].max(), 2)
            low_24h = round(df['Low'].min(), 2)
            ema = round(df['Close'].ewm(span=9).mean().iloc[-1], 2)
            sig = "BUY" if ltp > ema else "SELL"
            
            data.append({
                "name": name, "ltp": ltp, "sig": sig, 
                "bullish": high_24h, "bearish": low_24h
            })
    return data

# Header
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<h2 style='text-align:center; color:#00ff88;'>🦅 TRADEX PRO V66 | LIVE LEVELS</h2>", unsafe_allow_html=True)

live_data = get_live_data_with_levels()

cols = st.columns(4)
for i, item in enumerate(live_data):
    with cols[i]:
        sig_class = "buy-btn" if item['sig'] == "BUY" else "sell-btn"
        st.markdown(f"""
            <div class='price-card'>
                <div style='color:#888; font-size:12px;'>{item['name']}</div>
                <div style='font-size:35px; font-weight:900;'>{item['ltp']}</div>
                <div class='{sig_class}'>{item['sig']}</div>
                <div class='levels bull-text'>BULLISH ABOVE: {item['bullish']}</div>
                <div class='levels bear-text'>BEARISH BELOW: {item['bearish']}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("🚀 STOCK MOMENTUM LEVELS")
# Niche wala Reliance/TCS wala table levels ke saath waise hi rahega

time.sleep(5)
st.rerun()
