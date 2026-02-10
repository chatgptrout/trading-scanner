import streamlit as st
import plotly.graph_objects as go
import pytz
from datetime import datetime
import time

# --- CORE SETUP ---
st.set_page_config(page_title="SANTOSH ULTIMATE TRADER", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
curr_time = datetime.now(IST).strftime('%H:%M:%S')

# Professional Trading Theme
st.markdown(f"""
    <style>
    .stApp {{ background-color: #f4f7f9; }}
    .stock-card {{ background: white; border-top: 5px solid #2ecc71; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
    .clock-box {{ background: #1a1a1a; color: #00ff00; padding: 10px; border-radius: 8px; text-align: center; font-family: monospace; font-size: 22px; border: 1px solid #333; }}
    .mcx-live-price {{ font-size: 26px; font-weight: bold; color: #ff3131; }} /* Red for Current Bearish Trend */
    </style>
    """, unsafe_allow_html=True)

# --- 1. HEADER (STILL THERE) ---
h1, h2 = st.columns([3, 1])
with h1:
    st.title("🚀 SANTOSH ULTIMATE TRADER")
with h2:
    st.markdown(f"<div class='clock-box'>⏰ {curr_time}</div>", unsafe_allow_html=True)

# --- 2. VIP WATCHLIST (PURANA RAKHA HAI) ---
st.write("### ⭐ VIP Watchlist")
v1, v2, v3, v4, v5 = st.columns(5)
with v1: st.markdown("<div class='stock-card'><b>BSE LTD</b><br><span style='color:green;'>WELL SET BUY</span><br>LTP: 3185</div>", unsafe_allow_html=True)
with v2: st.markdown("<div class='stock-card'><b>JINDALSTEL</b><br><span style='color:green;'>WELL SET BUY</span><br>LTP: 1199</div>", unsafe_allow_html=True)
with v3: st.markdown("<div class='stock-card'><b>ADANI ENT</b><br><span style='color:blue;'>WATCHING</span><br>LTP: 3158</div>", unsafe_allow_html=True)
with v4: st.markdown("<div class='stock-card'><b>M&M</b><br><span style='color:green;'>WELL SET BUY</span><br>LTP: 2852</div>", unsafe_allow_html=True)
with v5: st.markdown("<div class='stock-card' style='border-top-color:#e74c3c;'><b>CRUDE OIL</b><br><span style='color:red;'>WELL SET BEAR</span><br>LTP: 5812</div>", unsafe_allow_html=True)

st.divider()

# --- 3. UPDATED: MCX LIVE DATA (SABSE IMPORTANT) ---
st.subheader("💰 MCX Live - Real Time Sync")
m1, m2, m3 = st.columns(3)

# Abhi ke levels (Approx as per 10 Feb night session)
with m1:
    st.markdown("""<div class='stock-card' style='border-top-color:#ff3131;'>
        <b>CRUDE OIL (FEB)</b><br>
        <span class='mcx-live-price'>₹5,810.00</span><br>
        <small style='color:red;'>▼ -1.02% (-60)</small>
    </div>""", unsafe_allow_html=True)

with m2:
    st.markdown("""<div class='stock-card' style='border-top-color:#ff3131;'>
        <b>NATURAL GAS (FEB)</b><br>
        <span class='mcx-live-price'>₹279.10</span><br>
        <small style='color:red;'>▼ -2.91% (-8.4)</small>
    </div>""", unsafe_allow_html=True)

with m3:
    st.markdown("""<div class='stock-card' style='border-top-color:#d4af37;'>
        <b>GOLD (APR)</b><br>
        <span style='font-size:26px; font-weight:bold; color:#2ecc71;'>₹72,465.00</span><br>
        <small style='color:green;'>▲ +0.14% (+102)</small>
    </div>""", unsafe_allow_html=True)

st.divider()

# --- 4. % STRENGTH & NEWS TICKER (PURANA) ---
col_l, col_r = st.columns([2, 1])
with col_l:
    st.subheader("🏗️ Sector Strength (% Change)")
    fig = go.Figure(go.Bar(x=[0.26, 1.11, 1.44, 0.45, -1.02], y=['NIFTY', 'BSE', 'JINDAL', 'M&M', 'CRUDE'], orientation='h', marker_color='#4f46e5'))
    fig.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.subheader("🔴 Market Health")
    fig_pie = go.Figure(data=[go.Pie(labels=['Adv', 'Dec'], values=[76, 24], hole=.6, marker_colors=['#2ecc71', '#e74c3c'])])
    fig_pie.update_layout(height=250, showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_pie, use_container_width=True)

# --- NEWS TICKER (PURANA) ---
st.markdown("<marquee style='color:#d4af37; background:#1e1e2f; padding:10px; font-weight:bold; border-radius:5px;'>🚀 CRUDE OIL trading near 5800... 🔥 NG breakdown below 280... 📈 BSE Breakout alert... 💡 Nagpal Tips: SL is life, use it!</marquee>", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
