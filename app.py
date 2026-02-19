import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- SETTINGS ---
st.set_page_config(page_title="TRADEX PRO V19", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 35px; font-weight: 900; color: #ff5252; text-align: center; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px; margin-bottom: 20px; }
    .index-card { background: white; border-radius: 15px; padding: 18px; margin-bottom: 12px; border-left: 10px solid #1a237e; box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
    .price-text { font-size: 30px; font-weight: 900; color: #121212; }
    .bull-label { color: #2e7d32; font-weight: 900; font-size: 12px; }
    .bear-label { color: #c62828; font-weight: 900; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

def fetch_live_price(ticker, is_commodity=False):
    try:
        # Fetching 1-day data with 1-minute interval for highest accuracy
        data = yf.Ticker(ticker).history(period="1d", interval="1m")
        if data.empty: return None
        
        current_price = data['Close'].iloc[-1]
        
        # Crude aur NG ke liye International to MCX Conversion (Approx)
        # Kyunki Yahoo directly MCX Rupees nahi deta, hum conversion formula use kar rahe hain
        if is_commodity:
            if "CL=F" in ticker: # Crude Oil
                current_price = current_price * 84.40 # Current USD-INR Rate
            elif "NG=F" in ticker: # Natural Gas
                current_price = current_price * 84.40 * 1.25 # Factor for MCX units
        
        ema = data['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        if is_commodity: ema = ema * 84.40
            
        return {"p": round(current_price, 2), "ema": round(ema, 2), "is_bull": current_price > ema}
    except: return None

# UI HEADER
IST = pytz.timezone('Asia/Kolkata')
st.markdown(f"<div class='main-clock'>🚀 {datetime.now(IST).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 1. LIVE INDEX & COMMODITY (The "Dhan" Match Attempt)
market_assets = {
    "NIFTY 50": "^NSEI",
    "BANK NIFTY": "^NSEBANK",
    "CRUDE OIL (MCX)": "CL=F",
    "NATURAL GAS (MCX)": "NG=F"
}

for name, sym in market_assets.items():
    is_comm = True if "CL=F" in sym or "NG=F" in sym else False
    res = fetch_live_price(sym, is_commodity=is_comm)
    
    if res:
        color = "#2e7d32" if res['is_bull'] else "#c62828"
        status = "BULLISH ABOVE" if res['is_bull'] else "BEARISH BELOW"
        
        st.markdown(f"""
        <div class='index-card' style='border-left-color: {color};'>
            <div style='color: #757575; font-weight: bold;'>{name}</div>
            <div style='display: flex; justify-content: space-between; align-items: baseline;'>
                <div class='price-text'>₹{res['p']}</div>
                <div style='color: {color}; font-weight: 900;'>{status}: {res['ema']}</div>
            </div>
        </div>""", unsafe_allow_html=True)

# 2. STOCK SCANNER
st.markdown("### 📊 LIVE STOCK WATCH")
stocks = ["RELIANCE.NS", "HDFCBANK.NS", "SBIN.NS", "ICICIBANK.NS"]
for s in stocks:
    val = fetch_live_price(s)
    if val:
        s_color = "#2e7d32" if val['is_bull'] else "#c62828"
        st.markdown(f"""
        <div style='background: #f8f9fa; padding: 12px; border-radius: 10px; margin-bottom: 8px; border-left: 5px solid {s_color}; display: flex; justify-content: space-between;'>
            <b>{s.split('.')[0]}</b>
            <b style='color: {s_color};'>₹{val['p']}</b>
        </div>""", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
