import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time

st.set_page_config(page_title="SANTOSH HEATMAP PRO", layout="wide")

# Deep Red Theme Styling
st.markdown("""
    <style>
    .stApp { background-color: #010b14; color: white; }
    .reportview-container .main .block-container { padding-top: 1rem; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#ff4b2b;'>🟥 LIVE MARKET HEATMAP</h1>", unsafe_allow_html=True)

# 1. WATCHLIST (Jaise aapke screenshot mein tha)
watchlist = [
    "SUNPHARMA.NS", "DIVISLAB.NS", "CIPLA.NS", "DRREDDY.NS", 
    "LUPIN.NS", "ALKEM.NS", "AUROPHARMA.NS", "RELIANCE.NS", 
    "SBIN.NS", "TCS.NS", "INFY.NS", "ZOMATO.NS"
]

# 2. FETCH DATA FOR HEATMAP
def get_data():
    rows = []
    for sym in watchlist:
        try:
            t = yf.Ticker(sym).fast_info
            p = t['last_price']
            c = ((p - t['previous_close']) / t['previous_close']) * 100
            rows.append({"Symbol": sym.replace(".NS",""), "FullSym": sym, "Price": p, "Change": c})
        except: continue
    return pd.DataFrame(rows)

df = get_data()

# 3. INTERACTIVE SELECTION (Click feature)
selected_stock = st.selectbox("Click to Analyze Details:", df['FullSym'].tolist())

# 4. THE "DEEP RED" HEATMAP (1000104630.jpg Style)
if not df.empty:
    fig = px.treemap(
        df, path=['Symbol'], values=[abs(x)+1 for x in df['Change']],
        color='Change',
        color_continuous_scale=['#8B0000', '#FF0000', '#333333', '#006400', '#00FF00'],
        custom_data=['Price', 'Change']
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=450, template="plotly_dark")
    fig.update_traces(texttemplate="<b>%{label}</b><br>%{customdata[1]:+.2f}%")
    st.plotly_chart(fig, use_container_width=True)

# 5. CLICK DETAILS: CANDLESTICK & SIGNALS
st.markdown(f"## 📊 {selected_stock} Deep Analysis")
try:
    hist = yf.Ticker(selected_stock).history(period='1d', interval='5m')
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Candlestick Chart
        chart = go.Figure(data=[go.Candlestick(
            x=hist.index, open=hist['Open'], high=hist['High'],
            low=hist['Low'], close=hist['Close'],
            increasing_line_color='#00ff88', decreasing_line_color='#ff4b2b'
        )])
        chart.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(chart, use_container_width=True)
        
    with col2:
        # Buy/Sell Signals
        curr_p = df[df['FullSym']==selected_stock]['Price'].values[0]
        curr_c = df[df['FullSym']==selected_stock]['Change'].values[0]
        
        st.markdown(f"### LTP: ₹{curr_p:.2f}")
        st.markdown(f"### Change: {curr_c:+.2f}%")
        
        if curr_c < -1.5:
            st.error("💥 DEEP RED: STRONG SELL")
            st.write(f"Target: {curr_p*0.99:.2f} | SL: {curr_p*1.01:.2f}")
        elif curr_c > 1.5:
            st.success("🚀 BULL RUN: STRONG BUY")
            st.write(f"Target: {curr_p*1.01:.2f} | SL: {curr_p*0.99:.2f}")
        else:
            st.info("⚖️ SIDEWAYS: WAIT")
except:
    st.write("Click on a stock to load details.")

time.sleep(20)
st.rerun()
