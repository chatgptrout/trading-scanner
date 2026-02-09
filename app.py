import streamlit as st
import plotly.graph_objects as go
import time
from datetime import datetime

# Page Configuration
st.set_page_config(layout="wide", page_title="Santosh Tradex Master")

# Custom Styling to match your Tradex layout
st.markdown("""
    <style>
    .tradex-bar { background-color: #f9f9f9; padding: 10px; border-radius: 5px; border: 1px solid #eee; margin-top: 20px;}
    .live-tag { background-color: #ff4b4b; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .signal-text { color: #4f46e5; background: #eef2ff; padding: 2px 10px; border-radius: 4px; font-size: 12px; }
    .bullish-text { color: #2ecc71; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 1. Header with Time
st.markdown(f"### 🛡️ SANTOSH TRADEX MASTER | {datetime.now().strftime('%H:%M:%S')}")

# 2. Market Mood (Bulls vs Bears) Donut Chart
st.write("Market Mood (Bulls vs Bears)")
fig = go.Figure(data=[go.Pie(labels=['Bulls', 'Bears'], values=[73, 27], hole=.75, 
                             marker_colors=['#2ecc71', '#ff4b4b'], textinfo='percent')])
fig.update_layout(showlegend=False, height=300, margin=dict(t=0,b=0,l=0,r=0))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 3. Tradex Live Signal Table
st.markdown("""
    <div class='tradex-bar'>
        <span style='font-weight: bold;'>TRADEX</span> <span class='live-tag'>LIVE</span> <span style='color:#888; font-size:12px; margin-left:10px;'>2 Signals</span>
    </div>
    """, unsafe_allow_html=True)

# Creating the signal table data
data = {
    "SCRIPT": ["CRUDE FEB FUTURE", "BANK NIFTY"],
    "SIGNAL": ["SIGNAL", "SIGNAL"],
    "LEVELS": ["BULLISH ABOVE 5801", "BULLISH ABOVE 60660"],
    "TYPE": ["SWING", "VOLATILE"]
}

# Displaying the table with your custom levels
cols = st.columns([2, 1, 2, 1])
headers = ["SCRIPT", "SIGNAL", "LEVELS", "TYPE"]

# Header Row
for i, h in enumerate(headers):
    cols[i].markdown(f"<small style='color:#888;'>{h}</small>", unsafe_allow_html=True)

# Signal Rows
for i in range(len(data["SCRIPT"])):
    c = st.columns([2, 1, 2, 1])
    c[0].markdown(f"**{data['SCRIPT'][i]}**")
    c[1].markdown(f"<span class='signal-text'>{data['SIGNAL'][i]}</span>", unsafe_allow_html=True)
    c[2].markdown(f"<span class='bullish-text'>{data['LEVELS'][i]}</span>", unsafe_allow_html=True)
    c[3].markdown(f"<small>{data['TYPE'][i]}</small>", unsafe_allow_html=True)

# Refresh Logic
time.sleep(10)
st.rerun()
