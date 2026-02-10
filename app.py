import streamlit as st
import plotly.graph_objects as go
import pytz
from datetime import datetime
import time

# --- APP CONFIG ---
st.set_page_config(page_title="SANTOSH ULTIMATE TRADER", layout="wide")
IST = pytz.timezone('Asia/Kolkata')
curr_time = datetime.now(IST).strftime('%H:%M:%S')

# Professional Trading Theme
st.markdown(f"""
    <style>
    .stApp {{ background-color: #f4f7f9; }}
    .breakout-header {{ background: #2ecc71; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-bottom: 20px; }}
    .stock-card {{ background: white; border-top: 5px solid #2ecc71; padding: 15px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center; }}
    .clock-box {{ background: #1a1a1a; color: #00ff00; padding: 10px; border-radius: 8px; text-align: center; font-family: monospace; font-size: 22px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 1. HEADER (PURANA RAKHA HAI) ---
h1, h2 = st.columns([3, 1])
with h1:
    st.title("🚀 SANTOSH ULTIMATE TRADER")
with h2:
    st.markdown(f"<div class='clock-box'>⏰ {curr_time}</div>", unsafe_allow_html=True)

# --- 2. NEW: BREAKOUT STOCK SECTION (SABSE UPAR) ---
st.markdown("<div class='breakout-header'>🎯 LIVE BREAKOUT STOCKS (NEO-STYLE)</div>", unsafe_allow_html=True)
b1, b2, b3, b4 = st.columns(4)

with b1:
    st.markdown("""<div class='stock-card'>
        <b style='color:#2ecc71;'>WELL SET BUY</b><br>
        <span style='font-size:20px;'>BSE LTD</span><br>
        LTP: 3185 | <b>Breakout: 3150</b><br>
        <small>Target: 3220+</small>
    </div>""", unsafe_allow_html=True)

with b2:
    st.markdown("""<div class='stock-card'>
        <b style='color:#2ecc71;'>WELL SET BUY</b><br>
        <span style='font-size:20px;'>JINDAL STEL</span><br>
        LTP: 1199 | <b>Breakout: 1182</b><br>
        <small>Target: 1215</small>
    </div>""", unsafe_allow_html=True)

with b3:
    st.markdown("""<div class='stock-card' style='border-top-color:#e74c3c;'>
        <b style='color:#e74c3c;'>WELL SET BEAR</b><br>
        <span style='font-size:20px;'>CRUDE OIL</span><br>
        LTP: 5812 | <b>Breakdown: 5850</b><br>
        <small>Target: 5740</small>
    </div>""", unsafe_allow_html=True)

with b4:
    st.markdown("""<div class='stock-card' style='border-top-color:#3498db;'>
        <b style='color:#3498db;'>WATCHLIST</b><br>
        <span style='font-size:20px;'>NIFTY 50</span><br>
        LTP: 25935 | Range Bound<br>
        <small>Wait for 26000</small>
    </div>""", unsafe_allow_html=True)

st.divider()

# --- 3. NEO-STYLE CHARTS (PURANA) ---
col_l, col_r = st.columns([2, 1])
with col_l:
    st.subheader("🏗️ Market & Sector Strength")
    fig = go.Figure(go.Bar(x=[25935, 60626, 3185, 1199, 5812], y=['NIFTY', 'BANKNIFTY', 'BSE', 'JINDAL', 'CRUDE'], orientation='h', marker_color='#4f46e5'))
    fig.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.subheader("🔴 Adv/Dec Ratio")
    fig_pie = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[38, 12], hole=.6, marker_colors=['#2ecc71', '#e74c3c'])])
    fig_pie.update_layout(height=350, showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_pie, use_container_width=True)

# --- 4. COMMODITY SECTION (PURANA) ---
st.divider()
st.subheader("💰 MCX Commodity Live")
mcx1, mcx2, mcx3 = st.columns(3)
mcx1.metric("CRUDE OIL", "5,812", "-0.99%")
mcx2.metric("NATURAL GAS", "279.30", "-2.85%")
mcx3.metric("GOLD", "72,480", "+0.15%")

time.sleep(1)
st.rerun()
