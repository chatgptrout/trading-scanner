import streamlit as st
import yfinance as yf

st.set_page_config(page_title="TRADEX PRO LIVE", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .signal-box { padding: 5px 10px; border-radius: 5px; color: white; font-weight: bold; text-align: center; display: inline-block; width: 100px; }
    .buy-bg { background-color: #2e7d32; }
    .sell-bg { background-color: #c62828; }
    .btst-card { background-color: #F3E5F5; border-left: 10px solid #6A1B9A; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

def get_market_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if data.empty: return None
        cp = round(data['Close'].iloc[-1], 2)
        ema = round(data['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        diff = cp * 0.005
        status = "BULLISH" if cp > ema else "BEARISH"
        color = "#2e7d32" if cp > ema else "#c62828"
        bg_class = "buy-bg" if cp > ema else "sell-bg"
        return {"p": cp, "s": status, "t": round(cp + (diff if cp > ema else -diff), 2), "sl": ema, "c": color, "bg": bg_class}
    except: return None

st.title("🚀 TRADEX PRO LIVE DASHBOARD")

# --- SECTION 1: INDEX WATCH ---
st.header("🎯 INDEX WATCH")
idx_col1, idx_col2 = st.columns(2)
indices = {"NIFTY 50": "^NSEI", "BANK NIFTY": "^NSEBANK"}
for i, (name, sym) in enumerate(indices.items()):
    res = get_market_data(sym)
    if res:
        with (idx_col1 if i==0 else idx_col2):
            st.subheader(name)
            st.markdown(f"## {res['p']}")
            st.markdown(f"**Trend:** <span style='color:{res['c']}'>{res['s']} ABOVE {res['sl']}</span>", unsafe_allow_html=True)

st.divider()

# --- SECTION 2: TABLE DESIGN ---
st.header("🔥 TOP MARKET MOVERS")
MOVERS = {"ADANI ENT": "ADANIENT.NS", "RELIANCE": "RELIANCE.NS", "HDFC BANK": "HDFCBANK.NS", "ICICI BANK": "ICICIBANK.NS", "AXIS BANK": "AXISBANK.NS", "SBIN": "SBIN.NS"}

h = st.columns([2, 2, 2, 2, 2])
h[0].write("**STOCK NAME**"); h[1].write("**SIGNAL**"); h[2].write("**LTP**"); h[3].write("**TARGET**"); h[4].write("**STOPLOSS**")
st.markdown("---")

for name, sym in MOVERS.items():
    res = get_market_data(sym)
    if res:
        c = st.columns([2, 2, 2, 2, 2])
        c[0].write(f"**{name}**")
        c[1].markdown(f"<div class='signal-box {res['bg']}'>SIGNAL</div>", unsafe_allow_html=True)
        c[2].write(f"**{res['p']}**")
        c[3].markdown(f"<span style='color:#2e7d32;'>{res['t']}</span>", unsafe_allow_html=True)
        c[4].markdown(f"<span style='color:#c62828;'>{res['sl']}</span>", unsafe_allow_html=True)
        st.divider()

# --- SECTION 3: BTST SPECIAL ---
st.header("🌙 BTST / STBT SPECIAL")
BTST_LIST = {"TATA MOTORS": "TATAMOTORS.NS", "JINDAL STEEL": "JINDALSTEL.NS"}
btst_col1, btst_col2 = st.columns(2)
for i, (name, sym) in enumerate(BTST_LIST.items()):
    res = get_market_data(sym)
    if res:
        type_label = "BTST (Buy)" if res['s'] == "BULLISH" else "STBT (Sell)"
        with (btst_col1 if i==0 else btst_col2):
            st.markdown(f"""<div class="btst-card"><h3 style='color:#4A148C; margin-top:0;'>✨ {name} - {type_label}</h3><p><b>Entry:</b> {res['p']}</p><p style='color:#4A148C; font-weight:bold;'>View: {'GAP UP' if res['s'] == "BULLISH" else 'GAP DOWN'}</p></div>""", unsafe_allow_html=True)
