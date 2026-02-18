import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# Mobile-First Page Config
st.set_page_config(page_title="TRADEX MOBILE", layout="centered")

# --- MOBILE OPTIMIZED CSS ---
st.markdown("""
    <style>
    /* Mobile Background & Font */
    .stApp { background-color: #f8f9fa; }
    
    /* Large Mobile Clock */
    .mobile-clock { font-size: 30px; font-weight: 900; color: #ff5252; text-align: center; margin-bottom: 20px; border-bottom: 2px solid #eee; padding-bottom: 10px; }
    
    /* Responsive Grid for Index Cards */
    .mobile-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 12px; border-left: 8px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .price-large { font-size: 26px; font-weight: 900; color: #212121; margin: 5px 0; }
    
    /* Radar: Full Width for Mobile */
    .mobile-radar { background: #e3f2fd; border-left: 8px solid #1565c0; border-radius: 8px; padding: 15px; margin-bottom: 10px; font-size: 16px; }
    .radar-alert { background: #ffebee; border-left-color: #ff5252; color: #c62828; }

    /* Scanner: Optimized Row */
    .scanner-box { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border: 1px solid #eee; }
    .flex-row { display: flex; justify-content: space-between; align-items: center; }
    .stock-tag { font-size: 20px; font-weight: 900; color: #1a237e; }
    
    /* BTST: Mobile VIP Style */
    .btst-mobile { background: #fff9c4; border-radius: 12px; padding: 15px; margin-top: 20px; border: 1px solid #fbc02d; }
    
    /* Force Small Padding for Mobile Screens */
    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCTIONS ---
def get_ist_time():
    IST = pytz.timezone('Asia/Kolkata')
    return datetime.now(IST).strftime("%H:%M:%S")

def get_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="2d", interval="15m")
        if df.empty: return None
        cp = round(df['Close'].iloc[-1], 2)
        ema = round(df['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = round(100 - (100 / (1 + rs)).iloc[-1], 2)
        
        return {"p": cp, "ema": ema, "rsi": rsi, "status": "BULLISH" if cp > ema else "BEARISH"}
    except: return None

# --- UI RENDER ---
st.markdown(f"<div class='mobile-clock'>🚀 {get_ist_time()}</div>", unsafe_allow_html=True)

# 1. Index Status (Stacked for Mobile)
assets = {"NIFTY": "^NSEI", "SENSEX": "^BSESN", "CRUDE": "CL=F", "GOLD": "GC=F"}
results = {}

cols = st.columns(2) # 2 cards per row on mobile is better than 4
for i, (name, sym) in enumerate(assets.items()):
    res = get_data(sym)
    results[name] = res
    if res:
        color = "#2e7d32" if res['status'] == "BULLISH" else "#c62828"
        if res['rsi'] > 80: color = "#ff5252"
        with cols[i % 2]:
            st.markdown(f"""
            <div class='mobile-card' style='border-left-color: {color};'>
                <div style='font-size:14px; font-weight:bold; color:#757575;'>{name}</div>
                <div class='price-large'>{res['p']}</div>
                <div style='font-size:11px; color:{color}; font-weight:bold;'>RSI: {res['rsi']}</div>
            </div>""", unsafe_allow_html=True)

# 2. Strike Price Radar (Full Width)
st.markdown("### 🔥 RADAR SIGNALS")
for name, strike in [("NIFTY", "25800 CE"), ("SENSEX", "83700 CE")]:
    res = results.get(name)
    if res:
        style = "mobile-radar radar-alert" if res['rsi'] > 80 else "mobile-radar"
        label = "DANGER! HIGH RSI" if res['rsi'] > 80 else f"BUY ABOVE: {res['p']} 👁️🙏"
        st.markdown(f"<div class='{style}'><b>{strike}</b><br>{label}</div>", unsafe_allow_html=True)

# 3. Live Scanner (Simplified for Mobile)
st.markdown("### 📊 LIVE SCANNER")
for sym in ["RELIANCE.NS", "HDFCBANK.NS", "ADANIENT.NS"]:
    res = get_data(sym)
    if res:
        star = "⭐" if sym in ["RELIANCE.NS", "HDFCBANK.NS"] else ""
        color = "#2e7d32" if res['status']=="BULLISH" else "#c62828"
        st.markdown(f"""
        <div class='scanner-box' style='border-left: 10px solid {color};'>
            <div class='flex-row'>
                <div><span class='stock-tag'>{star}{sym.split('.')[0]}</span><br><span class='price-large'>₹{res['p']}</span></div>
                <div style='text-align:right;'>
                    <span style='color:#2e7d32; font-weight:900;'>T: {round(res['p']*1.007, 2)}</span><br>
                    <span style='color:#c62828; font-weight:900;'>S: {res['ema']}</span>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

# 4. BTST (Big Touch Area)
st.markdown("### 💰 BTST ALERTS")
for sym in ["TCS.NS", "INFY.NS"]:
    res = get_data(sym)
    if res and res['status'] == "BULLISH":
        st.markdown(f"""
        <div class='btst-mobile'>
            <div class='flex-row'>
                <b>🚀 {sym.split('.')[0]}</b>
                <b style='font-size:20px;'>₹{res['p']}</b>
            </div>
        </div>""", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
