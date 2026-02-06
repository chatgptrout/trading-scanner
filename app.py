import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH MULTI-MARKET PRO", layout="wide")

# Dark Theme Style
st.markdown("""<style>.stApp { background-color: #010b14; color: white; }
.sentiment-box { border: 5px solid #ff4b2b; border-radius: 50%; width: 140px; height: 140px; line-height: 140px; text-align: center; margin: auto; font-size: 28px; font-weight: bold; background: #0d1b2a; }
.mcx-card { background: linear-gradient(135deg, #1e3a5f, #0d1b2a); padding: 15px; border-radius: 12px; border-top: 5px solid #ffcc00; margin-bottom: 10px; }</style>""", unsafe_allow_html=True)

# 1. MARKET SENTIMENT GAUGE (image_1000104586.jpg)
st.markdown("<h2 style='text-align:center; color:#00f2ff;'>🧭 MARKET SENTIMENT (BULL VS BEAR)</h2>", unsafe_allow_html=True)
col_a, col_b, col_c = st.columns([1,2,1])
with col_b:
    # Based on PCR 0.72 from your image
    st.markdown('<div class="sentiment-box" style="color:#ff4b2b; border-color:#ff4b2b;">BEAR 🐻</div>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:20px; color:#ff4b2b;'>Sentiment: Highly Bearish</p>", unsafe_allow_html=True)

# 2. MCX COMMODITY SPECIAL (Crude, Gold, Silver)
st.markdown("<h2 style='color:#ffcc00;'>🔥 MCX LIVE COMMODITY SIGNALS</h2>", unsafe_allow_html=True)
mcx_list = {
    "CRUDE OIL": "CL=F", 
    "GOLD": "GC=F", 
    "SILVER": "SI=F"
}

c1, c2, c3 = st.columns(3)
cols = [c1, c2, c3]

for (name, sym), col in zip(mcx_list.items(), cols):
    try:
        t = yf.Ticker(sym)
        p = t.fast_info['last_price']
        change = ((p - t.fast_info['previous_close']) / t.fast_info['previous_close']) * 100
        color = "#00ff88" if change > 0 else "#ff4b2b"
        
        with col:
            st.markdown(f"""
                <div class="mcx-card">
                    <h3 style="margin:0; color:#ffcc00;">{name}</h3>
                    <h2 style="margin:5px 0;">${p:.2f}</h2>
                    <p style="color:{color}; font-size:18px; font-weight:bold;">{change:.2f}%</p>
                    <p style="font-size:14px; color:#a0a0a0;">Target: {p*1.005:.2f} | SL: {p*0.997:.2f}</p>
                </div>
            """, unsafe_allow_html=True)
    except: continue

# 3. EQUITY X-FACTOR RECAP (image_1000104573.jpg)
st.markdown("<h2 style='color:#00f2ff;'>🦅 EQUITY DAY SUMMARY</h2>", unsafe_allow_html=True)
equity_list = ["SYNGENE.NS", "PERSISTENT.NS", "RELIANCE.NS"]
for s in equity_list:
    try:
        data = yf.Ticker(s).fast_info
        st.write(f"✅ {s}: Last Price ₹{data['last_price']:.2f} | Day Change: {((data['last_price']-data['previous_close'])/data['previous_close'])*100:.2f}%")
    except: continue

time.sleep(15)
st.rerun()
