import streamlit as st
import plotly.graph_objects as go
import pytz
from datetime import datetime

# Page Setup
st.set_page_config(page_title="SANTOSH ULTIMATE TRADER", layout="wide")

# Custom CSS for Neo-Look
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; }
    .header-box { background: white; padding: 10px; border-bottom: 2px solid #00a8e8; margin-bottom: 20px; }
    .signal-btn { padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER (Clock & Title) ---
IST = pytz.timezone('Asia/Kolkata')
curr_time = datetime.now(IST).strftime('%H:%M:%S')

with st.container():
    c1, c2 = st.columns([4,1])
    c1.title("🚀 SANTOSH ULTIMATE TRADER")
    c2.markdown(f"### ⏰ {curr_time}")

# --- QUICK SIGNALS (Neo Style) ---
s1, s2, s3, s4 = st.columns(4)
s1.markdown("<div class='signal-btn' style='background:#2ecc71;'>WELL SET BUY</div>", unsafe_allow_html=True)
s2.markdown("<div class='signal-btn' style='background:#27ae60;'>WELL SET BUY</div>", unsafe_allow_html=True)
s3.markdown("<div class='signal-btn' style='background:#e74c3c;'>WELL SET BEAR</div>", unsafe_allow_html=True)
s4.markdown("<div class='signal-btn' style='background:#3498db;'>TAKING GUARD BULL</div>", unsafe_allow_html=True)

st.markdown("---")

# --- MAIN DASHBOARD LAYOUT ---
col_left, col_mid, col_right = st.columns([1.5, 1.5, 1])

with col_left:
    st.subheader("📊 Broad Market Indices")
    # Horizontal Bar Chart for Indices
    fig_idx = go.Figure(go.Bar(
        x=[25935, 60626, 25000, 15000],
        y=['NIFTY', 'BANKNIFTY', 'MIDCAP 100', 'SMLCAP 100'],
        orientation='h', marker_color='#ff3131'
    ))
    fig_idx.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_idx, use_container_width=True)

with col_mid:
    st.subheader("🏗️ Sector Performance")
    sectors = ['NIFTY AUTO', 'NIFTY FMCG', 'NIFTY PSU BANK', 'NIFTY REALTY']
    vals = [80, 45, 90, 30]
    fig_sec = go.Figure(go.Bar(x=vals, y=sectors, orientation='h', marker_color='#4f46e5'))
    fig_sec.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_sec, use_container_width=True)

with col_right:
    st.subheader("🔴 Advance/Decline")
    fig_pie = go.Figure(data=[go.Pie(labels=['Adv', 'Dec', 'Neut'], values=[1200, 800, 200], hole=.6, marker_colors=['#2ecc71', '#e74c3c', '#95a5a6'])])
    fig_pie.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- MCX COMMODITY (KEEPING IT ALIVE) ---
st.markdown("---")
st.subheader("🔥 MCX Commodity Live")
mcx1, mcx2, mcx3 = st.columns(3)
mcx1.metric("CRUDE OIL", "5,812", "-0.99%")
mcx2.metric("NATURAL GAS", "279.30", "-2.85%")
mcx3.metric("GOLD", "72,450", "+0.12%")

st.button("🔄 REFRESH TERMINAL")
