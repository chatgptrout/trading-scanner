import streamlit as st
import yfinance as yf
from datetime import datetime
import time
import pytz 

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="TRADEX PRO V15", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-clock { font-size: 35px; font-weight: 900; color: #ff5252; text-align: center; margin-bottom: 20px; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px; }
    
    /* Index Status Cards */
    .index-card { background: white; border-radius: 15px; padding: 18px; margin-bottom: 12px; border-left: 10px solid #1a237e; box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
    .price-text { font-size: 28px; font-weight: 900; color: #121212; margin: 4px 0; }
    .status-tag { font-size: 11px; font-weight: 900; letter-spacing: 0.5px; }

    /* Live Scanner Rows */
    .scanner-box { background: #fafafa; border-radius: 12px; padding: 15px; margin-bottom: 12px; border: 1px solid #eee; border-left: 12px solid #2e7d32; }
    .stock-name { font-size: 20px; font-weight: 900; color: #1a237e; }
    
    /* BTST Special Zone */
    .btst-section { background: #fff9c4; border: 2px solid #fbc02d; border-radius: 15px; padding: 20px; margin-top: 30px; }
    .btst-item { background: white; border-radius: 10px; padding: 15px; margin-top: 10px; border-right: 10px solid #fbc02d; display: flex; justify-content: space-between; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
def fetch_market_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if data.empty: return None
        cp = round(data['Close'].iloc[-1], 2)
        ema = round(data['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        return {"p": cp, "ema": ema, "is_bull": cp > ema}
    except: return None

# --- 3. UI HEADER ---
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime("%H:%M:%S")
st.markdown(f"<div class='main-clock'>🚀 {current_time}</div>", unsafe_allow_html=True)

# --- 4. INDEX & COMMODITY (Nifty, Sensex, Crude, NG) ---
# No Radar Signals here anymore
indices = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
idx_cols = st.columns(2)

for i, (name, sym) in enumerate(indices.items()):
    res = fetch_market_data(sym)
    if res:
        color = "#2e7d32" if res['is_bull'] else "#c62828"
        label = "BULLISH ABOVE" if res['is_bull'] else "BEARISH BELOW"
        with idx_cols[i % 2]:
            st.markdown(f"""
            <div class='index-card' style='border-left-color: {color};'>
                <div style='color: #757575; font-weight: bold; font-size: 13px;'>{name}</div>
                <div class='price-text'>{res['p']}</div>
                <div class='status-tag' style='color: {color};'>{label} {res['ema']}</div>
            </div>""", unsafe_allow_html=True)

# --- 5. LIVE SCANNER (Expanded List) ---
st.markdown("### 📊 LIVE INSTITUTIONAL SCANNER")
stocks_to_scan = ["RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "ADANIENT.NS", "TCS.NS", "INFY.NS", "AXISBANK.NS"]

for s in stocks_to_scan:
    val = fetch_market_data(s)
    if val:
        star = "⭐" if s in ["RELIANCE.NS", "HDFCBANK.NS", "SBIN.NS"] else ""
        s_color = "#2e7d32" if val['is_bull'] else "#c62828"
        st.markdown(f"""
        <div class='scanner-box' style='border-left-color: {s_color};'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <div class='stock-name'>{star} {s.split('.')[0]}</div>
                    <div class='price-text' style='font-size: 24px;'>₹{val['p']}</div>
                </div>
                <div style='text-align: right;'>
                    <div style='color: #2e7d32; font-weight: 900;'>TGT: {round(val['p']*1.008, 2)}</div>
                    <div style='color: #c62828; font-weight: 900;'>SL: {val['ema']}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

# --- 6. BTST / SWING ZONE ---
st.markdown("<div class='btst-section'><h3>💰 BTST / SWING ALERTS</h3>", unsafe_allow_html=True)
for b_stock in ["TCS.NS", "INFY.NS", "SBIN.NS"]:
    b_val = fetch_market_data(b_stock)
    if b_val and b_val['is_bull']:
        st.markdown(f"""
        <div class='btst-item'>
            <div><b style='font-size: 18px; color: #1a237e;'>🚀 {b_stock.split('.')[0]}</b><br><span style='font-size: 12px; color: #757575;'>Institutional Momentum</span></div>
            <div style='text-align: right;'><span class='price-text' style='font-size: 22px;'>₹{b_val['p']}</span><br><b style='color: #2e7d32; font-size: 12px;'>STRONG BUY</b></div>
        </div>""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
