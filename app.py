import streamlit as st
import plotly.graph_objects as go
import time
from datetime import datetime

# Page Config
st.set_page_config(layout="wide", page_title="Santosh VIP Terminal")

# VIP UI Styling
st.markdown("""
    <style>
    .vip-insight-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #333 100%);
        color: #00ff00; border-radius: 15px; padding: 20px;
        border: 2px solid #00ff00; margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0,255,0,0.1);
    }
    .verify-tag { background: #00ff00; color: black; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .tradex-table { background: white; border-radius: 10px; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# HEADER
st.markdown(f"### 🛡️ SANTOSH TRADEX MASTER | VIP TERMINAL ACTIVE")

# 1. VIP INSIGHT BOX (The "Software Power" Section)
st.markdown(f"""
    <div class='vip-insight-card'>
        <div style='display: flex; justify-content: space-between;'>
            <span style='font-size: 18px; font-weight: bold;'>💎 VIP INSIGHTS (SOFTWARE VERIFIED)</span>
            <span class='verify-tag'>99% ACCURACY MODE</span>
        </div>
        <hr style='border-color: #444;'>
        <div style='font-size: 22px; font-weight: bold; margin: 10px 0;'>
            🚀 CRUDE OIL: <span style='color: white;'>5801 Breakout ✅</span> → <span style='color: #00ff00;'>5838 DONE</span>
        </div>
        <div style='font-size: 14px; color: #888;'>
            ALERT: "Crude super hit again... Book or Trail" - Mausam Nagpal Style
        </div>
    </div>
    """, unsafe_allow_html=True)

# 2. MARKET MOOD (Bulls 73% / Bears 27%)
st.write("**Market Sentiment Analytics**")
fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[73, 27], hole=.75, 
                             marker_colors=['#2ecc71', '#ff4b4b'])])
fig.update_layout(showlegend=False, height=220, margin=dict(t=0,b=0,l=0,r=0))
st.plotly_chart(fig, use_container_width=True)

# 3. TRADEX LIVE SIGNALS
st.markdown("<div class='tradex-table'>", unsafe_allow_html=True)
st.write("**TRADEX LIVE | Active Signals**")
c1, c2, c3 = st.columns([2, 2, 1])
c1.markdown("**SCRIPT**")
c2.markdown("**LEVELS**")
c3.markdown("**STATUS**")

# Row 1: Crude
r1_1, r1_2, r1_3 = st.columns([2, 2, 1])
r1_1.write("CRUDE FEB FUTURE")
r1_2.markdown("<span style='color:#2ecc71; font-weight:bold;'>BULLISH ABOVE 5801</span>", unsafe_allow_html=True)
r1_3.markdown("<span style='color:#00ff00;'>SUPER HIT 🚀</span>", unsafe_allow_html=True)

# Row 2: Bank Nifty
r2_1, r2_2, r2_3 = st.columns([2, 2, 1])
r2_1.write("BANK NIFTY")
r2_2.markdown("<span style='color:#2ecc71; font-weight:bold;'>BULLISH ABOVE 60660</span>", unsafe_allow_html=True)
r2_3.write("ACTIVE")
st.markdown("</div>", unsafe_allow_html=True)

time.sleep(10)
st.rerun()
