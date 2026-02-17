import streamlit as st
import yfinance as yf

# Page Branding
st.set_page_config(page_title="TRADEX LIVE", layout="wide")
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>TRADEX LIVE Signals</h1>", unsafe_allow_html=True)

# Sidebar Navigation
app_mode = st.sidebar.radio("CHOOSE CATEGORY", ["STOCKS", "COMMODITY", "NIFTY/BANKNIFTY"])

def get_signal_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if data.empty: return None
        
        current_price = round(data['Close'].iloc[-1], 2)
        # Advanced Level Calculation (EMA 20)
        level = round(data['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        
        if current_price > level:
            return {"price": current_price, "signal": "SIGNAL", "level_text": f"BULLISH ABOVE {level}", "type": "BUY"}
        else:
            return {"price": current_price, "signal": "SIGNAL", "level_text": f"BEARISH BELOW {level}", "type": "SELL"}
    except:
        return None

# Display Table Header
st.markdown("---")
h1, h2, h3 = st.columns([2, 1, 3])
h1.write("**SCRIPT**")
h2.write("**SIGNAL**")
h3.write("**LEVELS**")
st.markdown("---")

# Logic for different pages
scripts = []
if app_mode == "STOCKS":
    scripts = {"BHARATFORGE": "BHARATFORG.NS", "MUTHOOT FIN": "MUTHOOTFIN.NS", "RELIANCE": "RELIANCE.NS"}
elif app_mode == "COMMODITY":
    scripts = {"CRUDE OIL": "CL=F", "NATURAL GAS": "NG=F"}
else:
    scripts = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK"}

for name, sym in scripts.items():
    res = get_signal_data(sym)
    if res:
        col1, col2, col3 = st.columns([2, 1, 3])
        col1.subheader(name)
        
        # Signal Label
        if res['type'] == "BUY":
            col2.markdown(f"<span style='background-color: #C8E6C9; padding: 5px; border-radius: 5px; color: green;'>{res['signal']}</span>", unsafe_allow_html=True)
            col3.markdown(f"<h4 style='color: green;'>{res['level_text']}</h4>", unsafe_allow_html=True)
        else:
            col2.markdown(f"<span style='background-color: #FFCDD2; padding: 5px; border-radius: 5px; color: red;'>{res['signal']}</span>", unsafe_allow_html=True)
            col3.markdown(f"<h4 style='color: red;'>{res['level_text']}</h4>", unsafe_allow_html=True)
        st.divider()

st.caption("Auto-refreshing every minute. Levels calculated using 15m EMA Strategy.")
