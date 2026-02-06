import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH FINAL SYNC", layout="wide")

# 1. SESSION STATE CONTROL (Fixes the Sync Issue)
if 'selected_stock' not in st.session_state:
    st.session_state.selected_stock = "SUNPHARMA.NS"

st.markdown("<style>.stApp { background-color: #010b14; color: white; }</style>", unsafe_allow_html=True)

# 2. DATA FETCHING
watchlist = ["SUNPHARMA.NS", "DIVISLAB.NS", "CIPLA.NS", "DRREDDY.NS", "SBIN.NS", "RELIANCE.NS", "ZOMATO.NS"]

def get_market_data():
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

df = get_market_data()

# 3. DROPDOWN (Direct Control)
st.markdown("<h2 style='color:#ffcc00;'>🎯 SELECT STOCK FOR CHART</h2>", unsafe_allow_html=True)
new_selection = st.selectbox("Choose stock (Guaranteed Match):", df['Full'].tolist(), index=df['Full'].tolist().index(st.session_state.selected_stock))

# Update state and rerun if selection changes
if new_selection != st.session_state.selected_stock:
    st.session_state.selected_stock = new_selection
    st.rerun()

# 4. CHART DISPLAY (Matches the Selection 100%)
active = st.session_state.selected_stock
st.markdown(f"### 📈 LIVE CHART: {active}")

try:
    h = yf.Ticker(active).history(period='1d', interval='5m')
    c1, c2 = st.columns([3, 1])
    
    with c1:
        # Unique Key is critical here
        chart_fig = go.Figure(data=[go.Candlestick(
            x=h.index, open=h['Open'], high=h['High'],
            low=h['Low'], close=h['Close'],
            increasing_line_color='#00ff88', decreasing_line_color='#ff4b2b'
        )])
        chart_fig.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False, height=450, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(chart_fig, use_container_width=True, key=f"final_chart_{active}")
        
    with c2:
        row = df[df['Full'] == active].iloc[0]
        st.markdown(f"""<div style="background:#0d1b2a; padding:20px; border-radius:15px; border:2px solid #ffcc00; text-align:center;">
            <h3>LTP: ₹{row['Price']:.2f}</h3>
            <h4 style="color:{'#ff4b2b' if row['Change'] < 0 else '#00ff88'}">{row['Change']:+.2f}%</h4>
            <hr><p><b>{active}</b></p>
        </div>""", unsafe_allow_html=True)
except:
    st.error("Select another stock to refresh.")

# 5. VISUAL HEATMAP (Bottom)
st.markdown("---")
st.markdown("### 🟥 MARKET WATCH (VISUAL)")
fig_map = px.treemap(df, path=['Symbol'], values=[abs(x)+1 for x in df['Change']],
                     color='Change', color_continuous_scale=['#8B0000', '#FF0000', '#333333', '#00FF00'])
fig_map.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=250, template="plotly_dark")
st.plotly_chart(fig_map, use_container_width=True, key="visual_map")

time.sleep(15)
st.rerun()
