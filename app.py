import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
import time

st.set_page_config(page_title="SANTOSH COMMANDER PRO", layout="wide")

# --- CUSTOM CSS FOR NEO-DARK THEME ---
st.markdown("""
    <style>
    .stApp { background-color: #010b14; color: white; }
    .card { 
        background: #0d1b2a; border-radius: 12px; padding: 15px; 
        border-left: 8px solid #00f2ff; margin-bottom: 15px; 
        box-shadow: 0px 0px 10px rgba(0, 242, 255, 0.2);
    }
    .gauge-adv { background:#00ff88; color:black; padding:10px; border-radius:10px; text-align:center; font-weight:bold; }
    .gauge-dec { background:#ff4b2b; color:white; padding:10px; border-radius:10px; text-align:center; font-weight:bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. MARKET BREADTH (ADVANCE/DECLINE) ---
st.markdown("<h2 style='color:#00f2ff;'>📊 MARKET BREADTH (ADVANCE/DECLINE)</h2>", unsafe_allow_html=True)
adv_dec_col1, adv_dec_col2 = st.columns(2)
with adv_dec_col1: st.markdown('<div class="gauge-adv">ADVANCES: 22</div>', unsafe_allow_html=True)
with adv_dec_col2: st.markdown('<div class="gauge-dec">DECLINES: 28</div>', unsafe_allow_html=True)

# --- 2. LIVE INTERACTIVE CHART WITH EMA ---
st.markdown("<h2 style='color:#00f2ff;'>📈 LIVE CANDLESTICK CHART</h2>", unsafe_allow_html=True)
chart_stocks = ["RELIANCE.NS", "SBIN.NS", "TATAMOTORS.NS", "TCS.NS", "INFY.NS"]
selected_chart_stock = st.selectbox("Select Stock for Chart:", chart_stocks)

try:
    df_chart = yf.download(selected_chart_stock, period='1d', interval='5m', progress=False)
    if not df_chart.empty:
        fig = go.Figure(data=[go.Candlestick(x=df_chart.index, open=df_chart['Open'], high=df_chart['High'], low=df_chart['Low'], close=df_chart['Close'], name='Candles')])
        ema20 = ta.ema(df_chart['Close'], length=20)
        fig.add_trace(go.Scatter(x=df_chart.index, y=ema20, mode='lines', name='EMA 20', line=dict(color='#00f2ff', width=1.5)))
        fig.update_layout(template='plotly_dark', xaxis_rangeslider_visible=False, height=450, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor="#010b14", plot_bgcolor="#010b14")
        st.plotly_chart(fig, use_container_width=True)
    else: st.warning(f"Fetching chart data for {selected_chart_stock}...")
except Exception as e: st.error(f"Error loading chart: {e}")

# --- 3. NEO-STYLE LIVE SIGNALS (HIGH MOVEMENT + T1, T2, SL) ---
st.markdown("<h2 style='color:#00f2ff;'>🚀 NEO-STYLE LIVE SIGNALS</h2>", unsafe_allow_html=True)
signal_stocks = ["RELIANCE.NS", "SBIN.NS", "ZOMATO.NS", "HAL.NS", "DIXON.NS", "ADANIENT.NS", "TCS.NS"]

for sym in signal_stocks:
    try:
        t = yf.Ticker(sym)
        p = t.fast_info['last_price']
        c = ((p - t.fast_info['previous_close']) / t.fast_info['previous_close']) * 100
        
        if abs(c) > 0.6: # Movement Filter
            color = "#00ff88" if c > 0 else "#ff4b2b"
            action = "LONG" if c > 0 else "SHORT"
            t1, t2, sl = (p * 1.005, p * 1.010, p * 0.994) if c > 0 else (p * 0.995, p * 0.990, p * 1.006)

            st.markdown(f"""
                <div class="card" style="border-left-color:{color}">
                    <h3 style="margin:0;">{action}: {sym} @ ₹{p:.2f} ({c:.2f}%)</h3>
                    <p style="color:{color}; font-size:16px;"><b>T1: {t1:.2f} | T2: {t2:.2f} | SL: {sl:.2f}</b></p>
                </div>
            """, unsafe_allow_html=True)
    except: continue

time.sleep(15)
st.rerun()
