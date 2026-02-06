import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH FIXED SYNC", layout="wide")

# Theme
st.markdown("<style>.stApp { background-color: #010b14; color: white; }</style>", unsafe_allow_html=True)

# 1. LIVE DATA FETCHING
watchlist = ["SUNPHARMA.NS", "DIVISLAB.NS", "CIPLA.NS", "DRREDDY.NS", "SBIN.NS", "RELIANCE.NS", "ZOMATO.NS"]

def get_data():
    data = []
    for s in watchlist:
        try:
            t = yf.Ticker(s).fast_info
            data.append({
                "Symbol": s.replace(".NS",""), 
                "Full": s, 
                "Price": t['last_price'], 
                "Change": ((t['last_price'] - t['previous_close']) / t['previous_close']) * 100
            })
        except: continue
    return pd.DataFrame(data)

df = get_data()

# 2. SELECTION BOX (This will fix the Noooooooo issue)
st.markdown("<h2 style='color:#ffcc00;'>🎯 SELECT STOCK FOR CHART</h2>", unsafe_allow_html=True)
# Is box se select karte hi chart 100% match hoga
active_selection = st.selectbox("Choose stock from here (Guaranteed Sync):", df['Full'].tolist())

# 3. DYNAMIC CHART DISPLAY
st.markdown(f"### 📈 CHART: {active_selection}")
try:
    h = yf.Ticker(active_selection).history(period='1d', interval='5m')
    
    col1, col2 = st.columns([3, 1])
    with col1:
        # Candlestick with dynamic key
        chart = go.Figure(data=[go.Candlestick(
            x=h.index, open=h['Open'], high=h['High'],
            low=h['Low'], close=h['Close'],
            increasing_line_color='#00ff88', decreasing_line_color='#ff4b2b'
        )])
        chart.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(chart, use_container_width=True, key=f"fixed_chart_{active_selection}")
        
    with col2:
        row = df[df['Full'] == active_selection].iloc[0]
        st.markdown(f"""<div style="background:#0d1b2a; padding:20px; border-radius:15px; border:1px solid #ffcc00; text-align:center;">
            <h3>LTP: ₹{row['Price']:.2f}</h3>
            <h4 style="color:{'#ff4b2b' if row['Change'] < 0 else '#00ff88'}">{row['Change']:+.2f}%</h4>
        </div>""", unsafe_allow_html=True)
except:
    st.error("Select another stock.")

# 4. HEATMAP (Sirf dekhne ke liye)
st.markdown("---")
st.markdown("### 🟥 MARKET WATCH (VISUAL)")
fig = px.treemap(df, path=['Symbol'], values=[abs(x)+1 for x in df['Change']],
                 color='Change', color_continuous_scale=['#8B0000', '#FF0000', '#333333', '#00FF00'])
fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=250, template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

time.sleep(15)
st.rerun()
