import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH CLICK-HEATMAP", layout="wide")

# Deep Red Theme Styling
st.markdown("""<style>.stApp { background-color: #010b14; color: white; }
.main-card { background: #0d1b2a; padding: 20px; border-radius: 15px; border: 1px solid #ff4b2b; }</style>""", unsafe_allow_html=True)

# 1. WATCHLIST (Pharma & Heavyweights)
watchlist = ["SUNPHARMA.NS", "DIVISLAB.NS", "CIPLA.NS", "DRREDDY.NS", "LUPIN.NS", "RELIANCE.NS", "SBIN.NS", "ZOMATO.NS"]

def get_data():
    rows = []
    for sym in watchlist:
        try:
            t = yf.Ticker(sym).fast_info
            p, c = t['last_price'], ((t['last_price'] - t['previous_close']) / t['previous_close']) * 100
            rows.append({"Symbol": sym.replace(".NS",""), "FullSym": sym, "Price": p, "Change": c})
        except: continue
    return pd.DataFrame(rows)

df = get_data()

# 2. THE "DEEP RED" HEATMAP (Clickable)
st.markdown("<h2 style='text-align:center; color:#ff4b2b;'>🟥 SELECT STOCK FROM HEATMAP</h2>", unsafe_allow_html=True)
fig = px.treemap(df, path=['Symbol'], values=[abs(x)+1 for x in df['Change']],
                 color='Change', color_continuous_scale=['#8B0000', '#FF0000', '#333333', '#00FF00'],
                 custom_data=['FullSym', 'Price', 'Change'])
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=350, template="plotly_dark")
fig.update_traces(texttemplate="<b>%{label}</b><br>%{customdata[2]:+.2f}%")

# Click Detection Logic
selected_event = st.plotly_chart(fig, use_container_width=True, on_select="rerun")
selected_stock = "SUNPHARMA.NS" # Default

# Agar user box pe click karega toh ye update hoga
if selected_event and 'selection' in selected_event and selected_event['selection']['points']:
    point = selected_event['selection']['points'][0]
    selected_stock = point['customdata'][0]

# 3. SHOW CHART FOR CLICKED STOCK
st.markdown(f"### 📊 Live Chart: {selected_stock}")
try:
    hist = yf.Ticker(selected_stock).history(period='1d', interval='5m')
    col1, col2 = st.columns([2, 1])
    with col1:
        chart = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'],
                                             increasing_line_color='#00ff88', decreasing_line_color='#ff4b2b')])
        chart.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(chart, use_container_width=True)
    with col2:
        curr_p = yf.Ticker(selected_stock).fast_info['last_price']
        st.markdown(f'<div class="main-card"><h3>LTP: ₹{curr_p:.2f}</h3><p>Signal: Checking Patterns...</p></div>', unsafe_allow_html=True)
except: st.error("Click a box to view chart")

time.sleep(20)
st.rerun()
