import streamlit as st
import plotly.graph_objects as go
import time

# VIP Dashboard Styling
st.markdown("""
    <style>
    .sentiment-box {
        background-color: #1e1e1e; padding: 15px; border-radius: 10px;
        border: 1px solid #444; margin-bottom: 20px;
    }
    .bearish-tag {
        background-color: #ff4b4b; color: white; padding: 5px 15px;
        border-radius: 20px; font-weight: bold; font-size: 18px;
    }
    .live-indicator { color: #888; font-size: 14px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 1. SOFTWARE INDICATION SECTION
st.markdown("<div class='sentiment-box'>", unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("<span style='color: #d4af37; font-size: 20px; font-weight: bold;'>NIFTY 50</span>", unsafe_allow_html=True)
    st.markdown("<span class='live-indicator'>● LIVE</span>", unsafe_allow_html=True)
with col2:
    st.markdown("<span class='bearish-tag'>BEARISH</span>", unsafe_allow_html=True)
st.markdown("<p style='color: #888; margin-top: 10px;'>Software Indication: Nifty should remain bearish today ✅</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 2. VIP INSIGHTS (CRUDE UPDATE)
st.info("💎 VIP UPDATE: Crude 5801 to 5838 Done! Book or Trail profits.")

# 3. PROFIT LOG (LOGO KA REACTION)
st.success("💰 Community Win: Today's Overall P&L +₹18,881.50 (LICI, NIFTY, POWERINDIA)")

time.sleep(10)
st.rerun()
