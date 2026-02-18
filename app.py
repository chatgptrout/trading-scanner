import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

st.set_page_config(page_title="TRADEX MOBILE V6", layout="centered")

# --- MOBILE CSS (With BTST Glow) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .mobile-clock { font-size: 30px; font-weight: 900; color: #ff5252; text-align: center; padding-bottom: 10px; border-bottom: 2px solid #eee; }
    .mobile-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 12px; border-left: 8px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .price-large { font-size: 26px; font-weight: 900; color: #212121; margin: 5px 0; }
    
    /* BTST Special Design */
    .btst-container { background: #fff9c4; border: 2px solid #fbc02d; border-radius: 15px; padding: 15px; margin: 20px 0; }
    .btst-card { background: white; border-radius: 10px; padding: 12px; margin-top: 10px; border-right: 8px solid #fbc02d; display: flex; justify-content: space-between; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

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
st.markdown(f"<div class='mobile-clock'>🚀 {datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 1. INDEX STATUS
assets = {"NIFTY": "^NSEI", "SENSEX": "^BSESN", "CRUDE": "CL=F", "NAT. GAS": "NG=F"}
results = {}
cols = st.columns(2)
for i, (name, sym) in enumerate(assets.items()):
    res = get_data(sym)
    results[name] = res
    if res:
        color = "#2e7d32" if res['status'] == "BULLISH" else "#c62828"
        with cols[i % 2]:
            st.markdown(f"<div class='mobile-card' style='border-left-color:{color};'><div style='font-size:13px; font-weight:bold; color:#757575;'>{name}</div><div class='price-large'>{res['p']}</div><div style='font-size:11px; color:{color}; font-weight:bold;'>{res['status']} {res['ema']}</div></div>", unsafe_allow_html=True)

# 2. RADAR
st.markdown("### 🔥 RADAR SIGNALS")
for name, strike in [("NIFTY", "25800 CE"), ("SENSEX", "83700 CE")]:
    res = results.get(name)
    if res:
        style = "background:#e3f2fd; border-left:8px solid #1565c0; border-radius:8px; padding:15px; margin-bottom:10px;"
        if res['rsi'] > 80: style = "background:#ffebee; border-left:8px solid #ff5252; border-radius:8px; padding:15px; margin-bottom:10px; color:#c62828;"
        msg = f"BUY ABOVE: {res['p']} 👁️🙏" if res['rsi'] <= 80 else "🚨 CRITICAL RSI"
        st.markdown(f"<div style='{style}'><b>{strike}</b><br>{msg}</div>", unsafe_allow_html=True)

# 3. LIVE SCANNER
st.markdown("### 📊 LIVE SCANNER")
for sym in ["RELIANCE.NS", "HDFCBANK.NS", "ADANIENT.NS"]:
    res = get_data(sym)
    if res:
        color = "#2e7d32" if res['status']=="BULLISH" else "#c62828"
        st.markdown(f"<div style='background:white; border-radius:12px; padding:15px; margin-bottom:10px; border-left:10px solid {color};'><div style='display:flex; justify-content:space-between;'><div><b>⭐ {sym.split('.')[0]}</b><br><span class='price-large'>₹{res['p']}</span></div><div style='text-align:right;'><span style='color:#2e7d32; font-weight:900;'>T: {round(res['p']*1.007, 2)}</span><br><span style='color:#c62828; font-weight:900;'>S: {res['ema']}</span></div></div></div>", unsafe_allow_html=True)

# 4. BTST SECTION (RE-ADDED)
st.markdown("<div class='btst-container'><h3 style='margin:0; color:#1a237e;'>💰 BTST / SWING ALERTS</h3>", unsafe_allow_html=True)
for sym in ["TCS.NS", "INFY.NS", "ICICIBANK.NS"]:
    res = get_data(sym)
    if res and res['status'] == "BULLISH":
        st.markdown(f"<div class='btst-card'><div><b style='font-size:18px;'>🚀 {sym.split('.')[0]}</b><br><span style='color:#757575; font-size:12px;'>Potential BTST Pick</span></div><div style='text-align:right;'><span style='font-size:20px; font-weight:900;'>₹{res['p']}</span><br><span style='color:#2e7d32; font-weight:bold; font-size:12px;'>MODE: STRONG</span></div></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
