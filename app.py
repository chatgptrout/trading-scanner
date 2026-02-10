import streamlit as st
import random
import time

# Styling for Professional Look
st.markdown("""
    <style>
    .metric-card { background: #f8f9fa; border-radius: 10px; padding: 15px; border-left: 5px solid #4f46e5; }
    .status-bull { color: #2ecc71; font-weight: bold; font-size: 20px; }
    .status-bear { color: #e74c3c; font-weight: bold; font-size: 20px; }
    .pcr-box { background: #1a1a1a; color: #00ff00; padding: 10px; border-radius: 8px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- ROW 1: SENSEX & NIFTY SENTIMENT ---
st.subheader("📊 Market Sentiment (Bullish/Bearish Possible)")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""<div class='metric-card'>
        <b>NIFTY 50</b><br>
        <span class='status-bear'>BEARISH POSSIBLE ▼</span><br>
        <small>Resistance: 22,500 | Support: 22,350</small>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""<div class='metric-card'>
        <b>SENSEX</b><br>
        <span class='status-bear'>BEARISH POSSIBLE ▼</span><br>
        <small>Resistance: 74,100 | Support: 73,800</small>
    </div>""", unsafe_allow_html=True)

# --- ROW 2: PCR DATA (Option Chain Mood) ---
st.markdown("---")
st.subheader("🔢 Put-Call Ratio (PCR) Analysis")
p_col1, p_col2, p_col3 = st.columns(3)

with p_col1:
    st.markdown("<div class='pcr-box'><b>NIFTY PCR</b><br><span style='font-size:24px;'>0.85</span><br><small>OVERSOLD</small></div>", unsafe_allow_html=True)
with p_col2:
    st.markdown("<div class='pcr-box'><b>BANKNIFTY PCR</b><br><span style='font-size:24px;'>0.72</span><br><small>EXTREME BEARISH</small></div>", unsafe_allow_html=True)
with p_col3:
    st.markdown("<div class='pcr-box'><b>OVERALL MOOD</b><br><span style='font-size:24px;'>Wait for Dip</span></div>", unsafe_allow_html=True)

# --- ROW 3: STOCK BREAKOUTS (Rocket Stocks) ---
st.markdown("---")
st.subheader("🚀 Stock Breakouts (Radar)")
s_col1, s_col2 = st.columns(2)

with s_col1:
    st.success("🔥 RELIANCE: Breakout above 2960 (Possible)")
    st.success("🔥 SBIN: Holding support at 715")
with s_col2:
    st.error("⚠️ HDFC BANK: Breakdown below 1650 (Watchout)")
    st.info("💡 TIP: Watch PCR for reversal at 9:45 AM")

time.sleep(15)
st.rerun()
