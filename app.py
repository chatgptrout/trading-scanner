import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH SYNC PRO", layout="wide")

# Theme Styling
st.markdown("<style>.stApp { background-color: #010b14; color: white; }</style>", unsafe_allow_html=True)

# 1. FETCH DATA (Simple & Fast)
watchlist = ["SUNPHARMA.NS", "DIVISLAB.NS", "CIPLA.NS", "DRREDDY.NS", "SBIN.NS", "RELIANCE.NS", "ZOMATO.NS"]

def get_clean_data():
    data = []
    for s in watchlist:
        try:
            t = yf.Ticker(s).fast_info
            p = t['last_price']
            c = ((p - t['previous_close']) / t['previous_close']) * 100
            data.append({"Symbol": s.replace(".NS",""), "Full": s, "Price": p, "Change": c})
        except: continue
    return pd.DataFrame(data)

df = get_clean_data()

# 2. HEATMAP (Click Detection)
st.markdown("<h2 style='text-align:center; color:#ff4b2b;'>🟥 TAP A BOX TO LOAD CHART</h2>", unsafe_allow_html=True)

fig = px.treemap(df, path=['Symbol'], values=[abs(x)+1 for x in df['Change']],
                 color='Change', color_continuous_scale=['#8B0000', '#FF0000', '#333333', '#00FF00'],
                 custom_data=['Full'])
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=300, template="plotly_dark")
fig.update_traces(texttemplate="<b>%{label}</b><br>%{color:+.2f}%")

# selection trigger
selected_data = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="heatmap_master")

# 3. DYNAMIC CHART LOGIC
# Agar koi selection nahi hai, toh default 'SUNPHARMA' dikhega
active_stock = "SUNPHARMA.NS" 

if selected_data and "selection" in selected_data and selected_data["selection"]["points"]:
    active_stock = selected_data["selection"]["points"][0]["customdata"][0]

st.markdown(f"### 📈 LIVE CHART: {active_stock}")

try:
    # Fetching 5-minute data for the active stock only
    h = yf.Ticker(active_stock).history(period='1d', interval='5m')
    
    c1, c2 = st.columns([3, 1])
    with c1:
        # Candlestick creation with Unique Key for each stock
        chart = go.Figure(data=[go.Candlestick(
            x=h.index, open=h['Open'], high=h['High'],
            low=h['Low'], close=h['Close'],
            increasing_line_color='#00ff88', decreasing_line_color='#ff4b2b'
        )])
        chart.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False, height=450, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(chart, use_container_width=True, key=f"chart_display_{active_stock}")
        
    with c2:
        # Real-time info card
        row = df[df['Full'] == active_stock].iloc[0]
        st.markdown(f"""<div style="background:#0d1b2a; padding:20px; border-radius:15px; border:1px solid #ffcc00; text-align:center;">
            <h3>LTP: ₹{row['Price']:.2f}</h3>
            <h4 style="color:{'#ff4b2b' if row['Change'] < 0 else '#00ff88'}">{row['Change']:+.2f}%</h4>
            <hr><p><b>{active_stock}</b></p>
        </div>""", unsafe_allow_html=True)
except:
    st.info("Tap on a different box to refresh chart link.")

time.sleep(15)
st.rerun()
