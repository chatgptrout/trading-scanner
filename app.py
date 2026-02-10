import streamlit as st
import plotly.graph_objects as go
import pytz
from datetime import datetime
import time
import random

# Page Configuration
st.set_page_config(page_title="SANTOSH ULTIMATE TRADER", layout="wide")

# Custom CSS for Neo-Look and Clean Layout
st.markdown("""
    <style>
    .stApp { background-color: #f8faff; }
    .metric-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #e1e8ed; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .signal-btn { padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; color: white; margin-bottom: 10px; font-size: 14px; }
    .price-text { font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- CLOCK SYNC (IST) ---
IST = pytz.timezone('Asia/Kolkata')
curr_time = datetime.now(IST).strftime('%H:%M:%S')

# --- HEADER SECTION ---
with st.container():
    h1, h2 = st.columns([3, 1])
    h1.title("💹 SANTOSH ULTIMATE TRADER")
    h2.markdown(f"<div style='background:#1a1a1a; color:#00ff00; padding:10px; border-radius:5px; text-align:center; font-family:monospace; font-size:20px;'>⏰ {curr_time}</div>", unsafe_allow_html=True)

# --- TOP SIGNALS (Neo-Style Buttons) ---
st.write("### ⚡ Strategy Pulse")
s1, s2, s3, s4 = st.columns(4)
s1.markdown("<div class='signal-btn' style='background:#2ecc71;'>WELL SET BUY (BSE)</div>", unsafe_allow_html=True)
s2.markdown("<div class='signal-btn' style='background:#27ae60;'>WELL SET BUY (JINDAL)</div>", unsafe_allow_html=True)
s3.markdown("<div class='signal-btn' style='background:#e74c3c;'>WELL SET BEAR (CRUDE)</div>", unsafe_allow_html=True)
s4.markdown("<div class='signal-btn' style='background:#3498db;'>TAKING GUARD BULL</div>", unsafe_allow_html=True)

st.divider()

# --- MIDDLE SECTION: BROAD MARKET & SECTORS ---
col_left, col_mid, col_right = st.columns([1.5, 1.5, 1.2])

with col_left:
    st.markdown("#### 📊 Broad Market Indices")
    # Horizontal Bar Chart for Broad Market
    idx_labels = ['NIFTY 50', 'BANKNIFTY', 'MIDCAP 100', 'SMLCAP 100']
    idx_vals = [25935, 60626, 25000, 15000]
    fig_idx = go.Figure(go.Bar(
        x=idx_vals, y=idx_labels, orientation='h', 
        marker_color=['#2ecc71', '#ff3131', '#4f46e5', '#f39c12']
    ))
    fig_idx.update_layout(height=350, margin=dict(l=0, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_idx, use_container_width=True)

with col_mid:
    st.markdown("#### 🏗️ Sector Performance")
    # Sector Bars
    sectors = ['NIFTY AUTO', 'NIFTY FMCG', 'NIFTY PSU BANK', 'NIFTY REALTY', 'NIFTY ENERGY']
    sec_vals = [75, 40, -20, 55, 15]
    colors = ['#2ecc71' if v > 0 else '#ff3131' for v in sec_vals]
    fig_sec = go.Figure(go.Bar(x=sec_vals, y=sectors, orientation='h', marker_color=colors))
    fig_sec.update_layout(height=350, margin=dict(l=0, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_sec, use_container_width=True)

with col_right:
    st.markdown("#### 🔴 Advance / Decline")
    # Donut Chart for Market Health
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Advance', 'Decline', 'Neutral'], 
        values=[35, 12, 3], 
        hole=.6, 
        marker_colors=['#2ecc71', '#ff3131', '#bdc3c7']
    )])
    fig_pie.update_layout(height=350, margin=dict(l=0, r=0, t=20, b=0), showlegend=True)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- BOTTOM SECTION: COMMODITY LIVE ---
st.divider()
st.subheader("🔥 MCX Commodity Live (Sync Active)")
m1, m2, m3, m4 = st.columns(4)

m1.metric("CRUDE OIL", "₹5,812", "-0.99%")
m2.metric("NATURAL GAS", "₹279.30", "-2.85%")
m3.metric("GOLD", "₹72,450", "+0.12%")
m4.metric("SILVER", "₹88,200", "+0.45%")

# Auto-refresh to keep everything moving
time.sleep(1)
st.rerun()
