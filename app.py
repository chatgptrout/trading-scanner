import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH SCALPER PRO", layout="wide")

# Neo-Style Dark Theme
st.markdown("""<style>.stApp { background-color: #010b14; color: white; }
.gauge-box { border: 4px solid #ff4b2b; border-radius: 50%; width: 150px; height: 150px; line-height: 150px; text-align: center; margin: auto; font-size: 32px; font-weight: bold; color: #ff4b2b; }
.signal-card { background: #0d1b2a; padding: 15px; border-radius: 12px; border-left: 10px solid #00ff88; margin-bottom: 10px; }</style>""", unsafe_allow_html=True)

# 1. MARKET DISTRIBUTION (PCR GAUGE - image_1000104575.jpg)
st.markdown("<h2 style='text-align:center;'>📊 MARKET DISTRIBUTION (PCR)</h2>", unsafe_allow_html=True)
st.markdown('<div class="gauge-box">0.72</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ff4b2b; font-weight:bold;'>BEARISH MODE 🐻</p>", unsafe_allow_html=True)

# 2. X-FACTOR SCALPER (HIGH MOVEMENT - image_1000104573.jpg)
st.markdown("### 🚀 X-FACTOR: TOP SCALPING SIGNALS")
# Stocks like Syngene, Persistent from your screenshots
shikari_list = ["SYNGENE.NS", "PERSISTENT.NS", "SBIN.NS", "RELIANCE.NS", "ADANIENT.NS"]

for sym in shikari_list:
    try:
        t = yf.Ticker(sym)
        p = t.fast_info['last_price']
        prev = t.fast_info['previous_close']
        change = ((p - prev) / prev) * 100
        
        # Logic: High Volume/Movement tracking
        color = "#ff4b2b" if change < 0 else "#00ff88"
        status = "SELL 🔴" if change < 0 else "BUY 🟢"
        
        st.markdown(f"""
            <div class="signal-card" style="border-left-color:{color};">
                <h3 style="margin:0;">{status} | {sym} @ ₹{p:.2f}</h3>
                <p style="color:{color}; font-size:20px;"><b>Change: {change:.2f}% | X-FACTOR: {abs(change)*2:.1f}x</b></p>
                <p style="color:#00f2ff;">T1: {p*0.995:.2f} | T2: {p*0.99:.2f} | SL: {p*1.005:.2f}</p>
            </div>
        """, unsafe_allow_html=True)
    except: continue

time.sleep(10)
st.rerun()
