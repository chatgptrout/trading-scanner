import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# Version 13 - Force Refresh Layout
st.set_page_config(page_title="TRADEX MOBILE V13", layout="centered")

# --- MOBILE CSS (STRICT NO RADAR) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .mobile-clock { font-size: 32px; font-weight: 900; color: #ff5252; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
    
    .mobile-card { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 8px solid #1a237e; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .price-large { font-size: 26px; font-weight: 900; color: #212121; margin: 5px 0; }
    .bull-level { font-size: 11px; font-weight: 900; text-transform: uppercase; }

    .scanner-row { background: white; border-radius: 12px; padding: 15px; margin-bottom: 10px; border-left: 10px solid #2e7d32; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }

    .btst-container { background: #fff9c4; border: 2px solid #fbc02d; border-radius: 15px; padding: 15px; margin: 20px 0; }
    .btst-card { background: white; border-radius: 10px; padding: 12px; margin-top: 10px; border-right: 8px solid #fbc02d; display: flex; justify-content: space-between; align-items: center; }
    
    /* Hard-coding removal of Radar Signals by ID if it persists */
    #radar-signals, .radar-box, [data-testid="stVerticalBlock"] > div:nth-child(3) { 
        display: none !important; 
        height: 0px !important; 
        visibility: hidden !important; 
    }
    </style>
    """, unsafe_allow_html=True)

def get_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="2d", interval="15m")
        if df.empty: return None
        cp = round(df['Close'].iloc[-1], 2)
        ema = round(df['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        return {"p": cp, "ema": ema, "status": "BULLISH" if cp > ema else "BEARISH"}
    except: return None

# --- UI RENDER ---
st.markdown(f"<div class='mobile-clock'>🚀 {datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# 1. INDEX STATUS (Nifty, Sensex, Crude, NG)
assets = {"NIFTY": "^NSEI", "SENSEX": "^BSESN", "CRUDE": "CL=F", "NAT. GAS": "NG=F"}
cols = st.columns(2)
for i, (name, sym) in enumerate(assets.items()):
    res = get_data(sym)
    if res:
        color = "#2e7d32" if res['status'] == "BULLISH" else "#c62828"
        label = "BULLISH ABOVE" if res['status'] == "BULLISH" else "BEARISH BELOW"
        with cols[i % 2]:
            st.markdown(f"""<div class='mobile-card' style='border-left-color:{color};'>
                <div style='font-size:12px; font-weight:bold; color:#757575;'>{name}</div>
                <div class='price-large'>{res['p']}</div>
                <div class='bull-level' style='color:{color};'>{label} {res['ema']}</div>
            </div>""", unsafe_allow_html=True)

# 2. LIVE SCANNER (Full Stock List)
st.markdown("### 📊 LIVE SCANNER")
# Extended list to show more stocks as requested
SCAN_LIST = ["RELIANCE.NS", "HDFCBANK.NS", "ADANIENT.NS", "SBIN.NS", "ICICIBANK.NS", "TCS.NS", "INFY.NS", "BHARTIARTL.NS"]
for sym in SCAN_LIST:
    res = get_data(sym)
    if res:
        star = "⭐" if sym in ["RELIANCE.NS", "HDFCBANK.NS", "SBIN.NS"] else ""
        color = "#2e7d32" if res['status']=="BULLISH" else "#c62828"
        st.markdown(f"""<div class='scanner-row' style='border-left-color:{color};'>
            <div style='display:flex; justify-content:space-between;'>
                <div><b>{star} {sym.split('.')[0]}</b><br><span class='price-large'>₹{res['p']}</span></div>
                <div style='text-align:right;'>
                    <span style='color:#2e7d32; font-weight:900;'>T: {round(res['p']*1.007, 2)}</span><br>
                    <span style='color:#c62828; font-weight:900;'>S: {res['ema']}</span>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

# 3. BTST / SWING ALERTS
st.markdown("<div class='btst-container'><h3 style='margin:0; color:#1a237e;'>💰 BTST / SWING ALERTS</h3>", unsafe_allow_html=True)
for sym in ["INFY.NS", "TCS.NS", "SBIN.NS"]:
    res = get_data(sym)
    if res and res['status'] == "BULLISH":
        st.markdown(f"""<div class='btst-card'>
            <div><b>🚀 {sym.split('.')[0]}</b><br><span style='font-size:11px; color:#757575;'>Potential BTST Pick</span></div>
            <div style='text-align:right;'><b>₹{res['p']}</b><br><span style='color:#2e7d32; font-size:11px; font-weight:bold;'>MODE: STRONG</span></div>
        </div>""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
