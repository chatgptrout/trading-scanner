import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="SANTOSH COMMANDER", layout="wide")

tickers = ["RELIANCE.NS", "SBIN.NS", "ZOMATO.NS", "TATAMOTORS.NS", "INFY.NS"]

st.markdown("<h2 style='text-align:center;'>🎯 LIVE SIGNALS: ENTRY & EXIT</h2>", unsafe_allow_html=True)

for sym in tickers:
    try:
        t = yf.Ticker(sym)
        p = t.fast_info['last_price']
        c = ((p - t.fast_info['previous_close']) / t.fast_info['previous_close']) * 100
        
        # Simple Logic: Agar stock 0.5% upar hai toh Buy, niche hai toh Sell
        color = "#00ff88" if c > 0.5 else "#ff4b2b" if c < -0.5 else "#ffffff"
        action = "BUY" if c > 0.5 else "SELL" if c < -0.5 else "WAIT"
        
        # Calculating Target (1%) and SL (0.5%)
        target = p * 1.01 if action == "BUY" else p * 0.99
        sl = p * 0.995 if action == "BUY" else p * 1.005

        if action != "WAIT":
            st.markdown(f"""
                <div style="background:#0d1b2a; padding:15px; border-radius:12px; border-left:10px solid {color}; margin-bottom:10px;">
                    <h3 style="margin:0;">{action}: {sym} @ ₹{p:.2f}</h3>
                    <p style="color:{color}; font-size:18px; font-weight:bold;">🎯 Target: ₹{target:.2f} | 🛑 SL: ₹{sl:.2f}</p>
                </div>
            """, unsafe_allow_html=True)
    except:
        continue

time.sleep(15)
st.rerun()
