import streamlit as st
import yfinance as yf
import pandas_ta as ta
import time

st.set_page_config(page_title="SANTOSH EQUITY PRO", layout="wide")

# Clean Dark Theme
st.markdown("""<style>.stApp { background-color: #010b14; color: white; }
.card { background: #0d1b2a; padding: 20px; border-radius: 12px; border-left: 8px solid #00f2ff; margin-bottom: 15px; }</style>""", unsafe_allow_html=True)

# 1. INDEX WATCH (Nifty & Bank Nifty)
st.markdown("## 📊 INDEX TREND")
c1, c2 = st.columns(2)
for sym, col in zip(["^NSEI", "^NSEBANK"], [c1, c2]):
    try:
        data = yf.Ticker(sym).fast_info
        p = data['last_price']
        chg = ((p - data['previous_close']) / data['previous_close']) * 100
        name = "NIFTY 50" if sym == "^NSEI" else "BANK NIFTY"
        col.markdown(f'<div class="card"><b>{name}</b><br><h2 style="margin:0;">₹{p:,.2f}</h2><p>{chg:+.2f}%</p></div>', unsafe_allow_html=True)
    except: continue

# 2. STOCK SCANNER (Target & SL)
st.markdown("## 🦅 LIVE STOCK SIGNALS")
shikari_list = ["RELIANCE.NS", "SBIN.NS", "ZOMATO.NS", "TATAMOTORS.NS", "HAL.NS", "ADANIENT.NS"]

for sym in shikari_list:
    try:
        t = yf.Ticker(sym).fast_info
        p = t['last_price']
        c = ((p - t['previous_close']) / t['previous_close']) * 100
        color = "#00ff88" if c > 0 else "#ff4b2b"
        side = "LONG 🟢" if c > 0 else "SHORT 🔴"
        
        # Simple Target (1%) and SL (0.5%)
        t1 = p * 1.01 if c > 0 else p * 0.99
        sl = p * 0.995 if c > 0 else p * 1.005

        st.markdown(f"""<div class="card" style="border-left-color:{color}">
            <h3 style="margin:0;">{side}: {sym} @ ₹{p:.2f} ({c:+.2f}%)</h3>
            <p style="color:{color}; font-weight:bold;">Target: {t1:.2f} | Stop Loss: {sl:.2f}</p>
        </div>""", unsafe_allow_html=True)
    except: continue

time.sleep(15)
st.rerun()
