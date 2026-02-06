import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="SANTOSH MULTI-ASSET", layout="wide")

# PREMIUM DASHBOARD CSS
st.markdown("""
    <style>
    .stApp { background-color: #010b14; color: white; }
    .mcx-header { color: #ffcc00; font-size: 28px; font-weight: bold; margin-bottom: 20px; }
    .asset-card {
        background: #0d1b2a; padding: 25px; border-radius: 15px;
        border-top: 5px solid #ffcc00; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5); text-align: center;
    }
    .price-text { font-size: 36px; font-weight: bold; margin: 10px 0; }
    .target-box { background: rgba(0,255,136,0.1); padding: 10px; border-radius: 8px; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# 1. MCX LIVE SECTION (Crude Oil, Gold, Natural Gas)
st.markdown('<div class="mcx-header">🔥 MCX LIVE COMMODITY SIGNALS</div>', unsafe_allow_html=True)
mcx_assets = {
    "CRUDE OIL": "CL=F", 
    "NATURAL GAS": "NG=F", 
    "GOLD": "GC=F"
}

c1, c2, c3 = st.columns(3)
cols = [c1, c2, c3]

for (name, sym), col in zip(mcx_assets.items(), cols):
    try:
        t = yf.Ticker(sym)
        p = t.fast_info['last_price']
        change = ((p - t.fast_info['previous_close']) / t.fast_info['previous_close']) * 100
        color = "#00ff88" if change > 0 else "#ff4b2b"
        
        with col:
            st.markdown(f"""
                <div class="asset-card">
                    <p style="color:#ffcc00; font-size:18px; margin:0;">{name}</p>
                    <p class="price-text">₹{p:.2f}</p>
                    <p style="color:{color}; font-size:20px; font-weight:bold;">{change:.2f}%</p>
                    <div class="target-box">
                        Target: {p*1.01:.2f} | SL: {p*0.995:.2f}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    except: continue

# 2. EQUITY TREND SUMMARY (High Volatility)
st.markdown("<h2 style='color:#00f2ff;'>🦅 EQUITY MARKET WATCH</h2>", unsafe_allow_html=True)
equity_list = ["RELIANCE.NS", "SBIN.NS", "PERSISTENT.NS", "SYNGENE.NS"]

for s in equity_list:
    try:
        data = yf.Ticker(s).fast_info
        p = data['last_price']
        c = ((p - data['previous_close']) / data['previous_close']) * 100
        col_side = "#00ff88" if c > 0 else "#ff4b2b"
        st.markdown(f"""
            <div style="background:#0d1b2a; padding:15px; border-radius:10px; border-left:8px solid {col_side}; margin-bottom:10px;">
                <b>{s}</b>: ₹{p:.2f} (<span style="color:{col_side}">{c:.2f}%</span>)
            </div>
        """, unsafe_allow_html=True)
    except: continue

time.sleep(15)
st.rerun()