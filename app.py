import streamlit as st
import plotly.graph_objects as go
import pytz
from datetime import datetime
import time

# --- CORE SETUP ---
st.set_page_config(page_title="SANTOSH ULTIMATE TRADER", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
curr_time = datetime.now(IST).strftime('%H:%M:%S')

# Professional Neo-Dark Style
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .nav-header { background: #1a1a1a; color: #00ff00; padding: 15px; border-radius: 10px; text-align: center; font-size: 24px; font-family: monospace; }
    .breakout-card { background: white; border-top: 5px solid #2ecc71; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .nagpal-signal { background: #4f46e5; color: white; padding: 2px 6px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. HEADER & LIVE CLOCK (PURANA) ---
c1, c2 = st.columns([3, 1])
with c1:
    st.title("🚀 SANTOSH ULTIMATE TRADER")
with c2:
    st.markdown(f"<div class='nav-header'>⏰ {curr_time}</div>", unsafe_allow_html=True)

# --- 2. STOCK BREAKOUT KIDHAR HAI? (NEW + NAGPAL FILTER) ---
st.subheader("🎯 Live Breakout Radar (Nagpal Strategy)")
b1, b2, b3, b4 = st.columns(4)

with b1:
    st.markdown("""<div class='breakout-card'>
        <span class='nagpal-signal'>WELL SET BUY</span><br>
        <b>BSE LTD</b><br>
        LTP: <span style='color:green;'>3185.40</span><br>
        Target: 3220 | SL: 3110
    </div>""", unsafe_allow_html=True)

with b2:
    st.markdown("""<div class='breakout-card'>
        <span class='nagpal-signal'>WELL SET BUY</span><br>
        <b>JINDAL STEL</b><br>
        LTP: <span style='color:green;'>1199.20</span><br>
        Target: 1215 | SL: 1180
    </div>""", unsafe_allow_html=True)

with b3:
    st.markdown("""<div class='breakout-card' style='border-top-color: #e74c3c;'>
        <span class='nagpal-signal' style='background:#e74c3c;'>WELL SET BEAR</span><br>
        <b>CRUDE OIL</b><br>
        LTP: <span style='color:red;'>5812.00</span><br>
        Target: 5740 | SL: 5880
    </div>""", unsafe_allow_html=True)

with b4:
    st.markdown("""<div class='breakout-card' style='border-top-color: #3498db;'>
        <span class='nagpal-signal' style='background:#3498db;'>TAKING GUARD</span><br>
        <b>NIFTY 50</b><br>
        LTP: 25935.15<br>
        Range: 25850 - 26050
    </div>""", unsafe_allow_html=True)

st.divider()

# --- 3. NEO-STYLE CHARTS (PURANA) ---
col_charts_left, col_charts_right = st.columns([2, 1])

with col_charts_left:
    st.write("### 🏗️ Market Indices & Sector Heat")
    # Multi-bar for Indices & Sectors
    fig = go.Figure(go.Bar(
        x=[25935, 60626, 3185, 1199, 5812],
        y=['NIFTY', 'BANKNIFTY', 'BSE', 'JINDAL', 'CRUDE'],
        orientation='h', marker_color=['#4f46e5', '#4f46e5', '#2ecc71', '#2ecc71', '#e74c3c']
    ))
    fig.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

with col_charts_right:
    st.write("### 🔴 Adv/Dec Ratio")
    fig_pie = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[35, 15], hole=.6, marker_colors=['#2ecc71', '#e74c3c'])])
    fig_pie.update_layout(height=350, showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_pie, use_container_width=True)

# --- 4. COMMODITY WATCH (PURANA) ---
st.divider()
st.subheader("💰 MCX Commodity Live")
mcx1, mcx2, mcx3 = st.columns(3)
mcx1.metric("CRUDE OIL", "5,812", "-0.99%")
mcx2.metric("NATURAL GAS", "279.30", "-2.85%")
mcx3.metric("GOLD", "72,480", "+0.15%")

# Auto-refresh to keep clock and breakout synced
time.sleep(1)
st.rerun()
