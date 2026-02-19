import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. CONFIG (PREMIUM UI) ---
st.set_page_config(page_title="TRADEX PRO V54", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #eee; }
    
    /* Header Branding */
    .header-box { background: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
    .logo-text { font-size: 26px; font-weight: 900; color: #1a237e; letter-spacing: -1px; }
    .live-dot { height: 10px; width: 10px; background-color: #ff5252; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }

    /* Top Index Cards */
    .index-card { background: white; padding: 15px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.03); border-bottom: 4px solid #eee; }

    /* Table Styling */
    .trade-container { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.03); }
    .table-header { display: flex; background: #f1f3f4; padding: 12px; border-radius: 8px; font-weight: bold; font-size: 13px; color: #5f6368; margin-bottom: 10px; }
    .table-row { display: flex; padding: 15px; border-bottom: 1px solid #f1f3f4; align-items: center; }
    
    /* Badges */
    .badge-buy { background: #e8f5e9; color: #2e7d32; padding: 5px 12px; border-radius: 6px; font-weight: bold; font-size: 11px; }
    .badge-sell { background: #ffebee; color: #c62828; padding: 5px 12px; border-radius: 6px; font-weight: bold; font-size: 11px; }
    
    /* PCR Sidebar */
    .pcr-box { text-align: center; padding: 15px; background: #fff; border: 1px solid #eee; border-radius: 15px; margin-top: 10px; }
    .pcr-container { position: relative; width: 110px; height: 110px; margin: 10px auto; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    .pcr-inner { width: 85px; height: 85px; background: white; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; box-shadow: inset 0 0 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

def get_live_pcr():
    try:
        nifty = yf.Ticker("^NSEI").history(period="1d")
        if nifty.empty: return 0.85
        change = (nifty['Close'].iloc[-1] - nifty['Open'].iloc[-1]) / nifty['Open'].iloc[-1]
        pcr = round(max(0.4, min(1.8, 1.0 + (change * 12))), 2)
        return pcr
    except: return 0.85

def get_pro_data(ticker):
    try:
        df = yf.Ticker(ticker).history(period="1d", interval="1m")
        if df.empty: return None
        p, ema = df['Close'].iloc[-1], df['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        return {"p": round(p, 2), "ema": round(ema, 2), "bull": p > ema}
    except: return None

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<div class='logo-text'>TRADEX PRO</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:green; font-weight:bold; font-size:12px;'>● MARKET ONLINE</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("📊 **Dashboard**")
    st.markdown("---")
    st.markdown("**Market Distribution**")
    pcr_val = get_live_pcr()
    c = "#c62828" if pcr_val < 0.9 else "#2e7d32" if pcr_val > 1.1 else "#fbc02d"
    st.markdown(f"""
    <div class='pcr-box'>
        <div class='pcr-container' style='background:conic-gradient({c} {int(pcr_val*55)}%, #eee {int(pcr_val*55)}%);'>
            <div class='pcr-inner'><small>PCR</small><div style='font-size:24px; font-weight:900; color:{c};'>{pcr_val}</div></div>
        </div>
        <small style='color:gray; font-weight:bold;'>Sentiment: {'Bearish' if pcr_val < 0.9 else 'Bullish'}</small>
    </div>""", unsafe_allow_html=True)

# --- MAIN UI ---
IST = pytz.timezone('Asia/Kolkata')
