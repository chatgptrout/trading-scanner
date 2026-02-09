import streamlit as st
import plotly.graph_objects as go
import time
from datetime import datetime

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Santosh Tradex Master")

# 2. Styling
st.markdown("""
    <style>
    .tradex-bar { background-color: #f9f9f9; padding: 10px; border-radius: 5px; border: 1px solid #eee; margin-top: 20px;}
    .live-tag { background-color: #ff4b4b; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .signal-pill { color: #4f46e5; background: #eef2ff; padding: 2px 10px; border-radius: 4px; font-size: 12px; }
    .rocket-card { background: #f0fff4; border-left: 5px solid #2ecc71; padding: 10px; margin-bottom: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f"### 🛡️ SANTOSH TRADEX MASTER | {datetime.now().strftime('%H:%M:%S')}")

# 3. MARKET MOOD (Bulls vs Bears)
st.write("Market Mood (Bulls vs Bears)")
fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[73, 27], hole=.75, 
                             marker_colors=['#2ecc71', '#ff4b4b'])])
fig.update_layout(showlegend=False, height=250, margin=dict(t=0,b=0,l=0,r=0))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 4. TRADEX LIVE SIGNALS (Fixed Table)
st.markdown("<div class='tradex-bar'><b>TRADEX</b> <span class='live-tag'>LIVE</span> <span style='color:#888; font-size:12px; margin-left:10px;'>2 Signals</span></div>", unsafe_allow_html=True)

col_h = st.columns([2, 1, 2, 1])
for i, h in enumerate(["SCRIPT", "SIGNAL", "LEVELS", "TYPE"]):
    col_h[i].markdown(f"<small style='color:#888;'>{h}</small>", unsafe_allow_html=True)

# Signal Rows
s1 = st.columns([2, 1, 2, 1])
s1[0].write("**CRUDE FEB FUTURE**")
s1[1].markdown("<span class='signal-pill'>SIGNAL</span>", unsafe_allow_html=True)
s1[2].markdown("<span style='color:#2ecc71; font-weight:bold;'>BULLISH ABOVE 5801</span>", unsafe_allow_html=True)
s1[3].write("SWING")

s2 = st.columns([2, 1, 2, 1])
s2[0].write("**BANK NIFTY**")
s2[1].markdown("<span class='signal-pill'>SIGNAL</span>", unsafe_allow_html=True)
s2[2].markdown("<span style='color:#2ecc71; font-weight:bold;'>BULLISH ABOVE 60660</span>", unsafe_allow_html=True)
s2[3].write("VOLATILE")

st.markdown("---")

# 5. STOCKS SECTION (Rocket Breakouts)
st.subheader("🚀 Rocket Breakout Stocks")
c1, c2 = st.columns(2)
with c1:
    st.markdown("<div class='rocket-card'><b>RELIANCE:</b> Buy Above 2950 (Target: 3020)</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='rocket-card'><b>HDFC BANK:</b> Buy Above 1680 (Target: 1715)</div>", unsafe_allow_html=True)

time.sleep(10)
st.rerun()
