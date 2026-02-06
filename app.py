import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH LIVE SYNC", layout="wide")

# Theme Styling
st.markdown("<style>.stApp { background-color: #010b14; color: white; }</style>", unsafe_allow_html=True)

# 1. LIVE DATA FETCHING
watchlist = ["SUNPHARMA.NS", "DIVISLAB.NS", "CIPLA.NS", "DRREDDY.NS", "SBIN.NS", "RELIANCE.NS", "ZOMATO.NS"]

def get_live_map():
    data = []
    for s in watchlist:
        try:
            t = yf.Ticker(s).fast_info
            p = t['last_price']
            c = ((p - t['previous_close']) / t['previous_close']) * 100
            data.append({"Symbol": s.replace(".NS",""), "Full": s, "Price": p, "Change": c})
        except: continue
    return pd.DataFrame(data)

df = get_live_map()

# 2. INTERACTIVE HEATMAP (Fixed Click Detection)
st.markdown("<h2 style='text-align:center; color:#ff4b2b;'>🟥 SELECT ANY BOX FOR CHART</h2>", unsafe_allow_html=True)

fig = px.treemap(df, path=['Symbol'], values=[abs(x)+1 for x in df['Change']],
                 color='Change', color_continuous_scale=['#8B0000', '#FF0000', '#333333', '#00FF00'],
                 custom_data=['Full'])
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=300, template="plotly_dark")
fig.update_traces(texttemplate="<b>%{label}</b><br>%{color:+.2f}%")

# Yahan par Selection Handle ho rahi hai
selected_data = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

# AUTO-SYNC LOGIC: Clicked stock ko pakadna
clicked_stock = "SUNPHARMA.NS" # Default agar kuch select na ho
if selected_data and "selection" in selected_data and selected_data["selection"]["points"]:
    clicked_stock = selected_data["selection"]["points"][0]["customdata"][0]

# 3. DYNAMIC CHART: Wahi dikhega jispe click kiya hai
st.markdown(f"### 📈 LIVE CHART: {clicked_stock}")
try:
    hist = yf.Ticker(clicked_stock).history(period='1d', interval='5m')
    c1, c2 = st.columns([3, 1])
    
    with c1:
        chart_fig = go.Figure(data=[go.Candlestick(
            x=hist.index, open=hist['Open'], high=hist['High'],
            low=hist['Low'], close=hist['Close'],
            increasing_line_color='#00ff88', decreasing_line_color='#ff4b2b'
        )])
        chart_fig.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False, height=450, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(chart_fig, use_container_width=True)
        
    with c2:
        curr_p = df[df['Full']==clicked_stock]['Price'].values[0]
        curr_c = df[df['Full']==clicked_stock]['Change'].values[0]
        status = "🔴 SELLING" if curr_c < 0 else "🟢 BUYING"
        st.markdown(f"""<div style="background:#0d1b2a; padding:20px; border-radius:15px; border:1px solid #ff4b2b; text-align:center;">
            <h3>LTP: ₹{curr_p:.2f}</h3>
            <h4 style="color:{'#ff4b2b' if curr_c < 0 else '#00ff88'}">{curr_c:+.2f}%</h4>
            <hr>
            <p><b>TREND: {status}</b></p>
        </div>""", unsafe_allow_html=True)
except:
    st.info("Tap on a heatmap box to load its candle chart instantly!")

time.sleep(15)
st.rerun()
