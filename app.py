import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH REAL-SYNC", layout="wide")

# Initialize Session State for clicking
if 'last_clicked' not in st.session_state:
    st.session_state.last_clicked = "SUNPHARMA.NS"

st.markdown("<style>.stApp { background-color: #010b14; color: white; }</style>", unsafe_allow_html=True)

# 1. LIVE DATA
watchlist = ["SUNPHARMA.NS", "DIVISLAB.NS", "CIPLA.NS", "DRREDDY.NS", "SBIN.NS", "RELIANCE.NS", "ZOMATO.NS"]

@st.cache_data(ttl=60)
def fetch_map_data():
    data = []
    for s in watchlist:
        try:
            t = yf.Ticker(s).fast_info
            p, c = t['last_price'], ((t['last_price'] - t['previous_close']) / t['previous_close']) * 100
            data.append({"Symbol": s.replace(".NS",""), "Full": s, "Price": p, "Change": c})
        except: continue
    return pd.DataFrame(data)

df = fetch_map_data()

# 2. HEATMAP WITH SELECTION
st.markdown("<h2 style='text-align:center; color:#ff4b2b;'>🟥 CLICK ANY BOX TO SWITCH CHART</h2>", unsafe_allow_html=True)

fig = px.treemap(df, path=['Symbol'], values=[abs(x)+1 for x in df['Change']],
                 color='Change', color_continuous_scale=['#8B0000', '#FF0000', '#333333', '#00FF00'],
                 custom_data=['Full'])
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=300, template="plotly_dark")
fig.update_traces(texttemplate="<b>%{label}</b><br>%{color:+.2f}%")

# Capture Click Event
selected = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="main_heatmap")

# Update clicked stock based on selection
if selected and "selection" in selected and selected["selection"]["points"]:
    new_pick = selected["selection"]["points"][0]["customdata"][0]
    if new_pick != st.session_state.last_clicked:
        st.session_state.last_clicked = new_pick
        st.rerun()

# 3. DYNAMIC CHART (Directly using Session State)
current_stock = st.session_state.last_clicked
st.markdown(f"### 📈 CHARTING NOW: {current_stock}")

try:
    # Small cache to avoid API lag
    hist = yf.Ticker(current_stock).history(period='1d', interval='5m')
    
    col1, col2 = st.columns([3, 1])
    with col1:
        chart = go.Figure(data=[go.Candlestick(
            x=hist.index, open=hist['Open'], high=hist['High'],
            low=hist['Low'], close=hist['Close'],
            increasing_line_color='#00ff88', decreasing_line_color='#ff4b2b'
        )])
        chart.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False, height=450, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(chart, use_container_width=True, key=f"chart_{current_stock}")
        
    with col2:
        stock_row = df[df['Full'] == current_stock].iloc[0]
        st.markdown(f"""<div style="background:#0d1b2a; padding:20px; border-radius:15px; border:2px solid #ffcc00; text-align:center;">
            <h3>LTP: ₹{stock_row['Price']:.2f}</h3>
            <h4 style="color:{'#ff4b2b' if stock_row['Change'] < 0 else '#00ff88'}">{stock_row['Change']:+.2f}%</h4>
            <hr>
            <p><b>ACTIVE SCAN: {current_stock}</b></p>
        </div>""", unsafe_allow_html=True)
except:
    st.error("Select another box to refresh data connection.")

time.sleep(15)
st.rerun()
