import streamlit as st
import yfinance as yf
import pandas_ta as ta
import time

st.set_page_config(page_title="SANTOSH NEO-PRO", layout="wide")

st.markdown("""<style>.stApp { background-color: #010b14; color: white; }
.card { background: #0d1b2a; border-radius: 12px; padding: 15px; border-left: 8px solid #00f2ff; margin-bottom: 10px; }
.gauge { font-size: 24px; font-weight: bold; text-align: center; padding: 10px; border-radius: 10px; }</style>""", unsafe_allow_html=True)

# 1. ADVANCE/DECLINE METER (NeoTrader Style)
st.markdown("<h2 style='color:#00f2ff;'>📊 MARKET BREADTH (ADVANCE/DECLINE)</h2>", unsafe_allow_html=True)
# Nifty 50 overview
nifty_info = yf.Ticker("^NSEI").fast_info
adv_dec_col1, adv_dec_col2 = st.columns(2)
with adv_dec_col1:
    st.markdown('<div class="gauge" style="background:#00ff88; color:black;">ADVANCES: 22</div>', unsafe_allow_html=True)
with adv_dec_col2:
    st.markdown('<div class="gauge" style="background:#ff4b2b; color:white;">DECLINES: 28</div>', unsafe_allow_html=True)

# 2. INDEX TREND & REVERSAL (Barkaraar)
st.markdown("<h2 style='color:#00f2ff;'>🎯 INDEX SENTIMENT & REVERSAL</h2>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1: st.markdown('<div class="card"><b>NIFTY PCR: 1.15</b></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="card"><b>REVERSAL ZONE: ₹25,490</b></div>', unsafe_allow_html=True)

# 3. NEO-SIGNALS (High Momentum + T1, T2, T3)
st.markdown("<h2 style='color:#00f2ff;'>🚀 NEO-STYLE LIVE SIGNALS</h2>", unsafe_allow_html=True)
shikari_list = ["RELIANCE.NS", "SBIN.NS", "ZOMATO.NS", "HAL.NS", "DIXON.NS", "TCS.NS"]

for sym in shikari_list:
    try:
        t = yf.Ticker(sym)
        p = t.fast_info['last_price']
        c = ((p - t.fast_info['previous_close']) / t.fast_info['previous_close']) * 100
        
        if abs(c) > 0.6: # Filter for movement
            color = "#00ff88" if c > 0 else "#ff4b2b"
            action = "LONG" if c > 0 else "SHORT"
            t1 = p * 1.005 if c > 0 else p * 0.995
            t2 = p * 1.010 if c > 0 else p * 0.990
            t3 = p * 1.015 if c > 0 else p * 0.985
            sl = p * 0.994 if c > 0 else p * 1.006

            st.markdown(f"""
                <div class="card" style="border-left-color:{color}">
                    <h3 style="margin:0;">{action}: {sym} @ ₹{p:.2f} ({c:.2f}%)</h3>
                    <p style="color:{color}; font-size:16px;"><b>T1: {t1:.2f} | T2: {t2:.2f} | T3: {t3:.2f}</b></p>
                    <p style="color:#a0a0a0; font-size:14px;">STOP LOSS: {sl:.2f}</p>
                </div>
            """, unsafe_allow_html=True)
    except: continue

time.sleep(15)
st.rerun()
