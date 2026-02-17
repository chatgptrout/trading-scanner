import streamlit as st
import yfinance as yf

st.set_page_config(page_title="TRADEX 100 BOLD", layout="wide")

# --- CSS FOR BOLD & COMPACT DESIGN ---
st.markdown("""
    <style>
    .compact-card {
        background: white;
        border-radius: 8px;
        padding: 12px 18px;
        margin-bottom: 6px;
        border-left: 10px solid #1a237e;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stock-name { font-size: 28px !important; font-weight: 900; color: #1a237e; margin: 0; padding: 0; }
    .price-bold { font-size: 32px !important; font-weight: 900; color: #000; margin: 0; padding: 0; }
    .signal-label {
        padding: 6px 12px;
        border-radius: 4px;
        font-size: 16px;
        font-weight: 900;
        color: white;
        text-align: center;
        min-width: 80px;
    }
    .bg-buy { background-color: #2e7d32; box-shadow: 0 0 8px #2e7d32; }
    .bg-sell { background-color: #c62828; box-shadow: 0 0 8px #c62828; }
    .level-text { font-size: 18px; font-weight: bold; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

def get_market_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="2d", interval="15m")
        if data.empty: return None
        cp = round(data['Close'].iloc[-1], 2)
        ema = round(data['Close'].ewm(span=20, adjust=False).mean().iloc[-1], 2)
        status = "BUY" if cp > ema else "SELL"
        bg = "bg-buy" if cp > ema else "bg-sell"
        color = "#2e7d32" if cp > ema else "#c62828"
        diff = cp * 0.007
        return {"p": cp, "s": status, "t": round(cp + (diff if cp > ema else -diff), 2), "sl": ema, "bg": bg, "c": color}
    except: return None

st.markdown("<h1 style='text-align:center; font-size:45px; margin:0;'>🚀 TRADEX SUPER 100</h1>", unsafe_allow_html=True)

# --- NIFTY 100 SYMBOLS LIST ---
NIFTY_100 = [
    "ABB.NS", "ADANIENT.NS", "ADANIPORTS.NS", "ADANIPOWER.NS", "ATGL.NS", "AMBUJACEM.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS",
    "BAJFINANCE.NS", "BAJAJFINSV.NS", "BAJAJHLDNG.NS", "BANKBARODA.NS", "BERGEPAINT.NS", "BEL.NS", "BPCL.NS", "BHARTIARTL.NS", "BIOCON.NS", "BOSCHLTD.NS",
    "BRITANNIA.NS", "CANBK.NS", "CHOLAFIN.NS", "CIPLA.NS", "COALINDIA.NS", "COLPAL.NS", "DLF.NS", "DABUR.NS", "DIVISLAB.NS", "DRREDDY.NS",
    "EICHERMOT.NS", "GAIL.NS", "GICRE.NS", "GODREJCP.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS",
    "HAL.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS", "ITC.NS", "IOC.NS", "IRCTC.NS", "IRFC.NS", "INDUSINDBK.NS",
    "INFY.NS", "INDIGO.NS", "JSWSTEEL.NS", "JINDALSTEL.NS", "JIOFIN.NS", "KOTAKBANK.NS", "LTIM.NS", "LT.NS", "LICI.NS", "M&M.NS",
    "MARICO.NS", "MARUTI.NS", "NTPC.NS", "NESTLEIND.NS", "ONGC.NS", "PIDILITIND.NS", "PFC.NS", "POWERGRID.NS", "PNB.NS", "RELIANCE.NS",
    "SBICARD.NS", "SBILIFE.NS", "SRF.NS", "SRTRANSFIN.NS", "SHREECEM.NS", "SIEMENS.NS", "SBIN.NS", "SUNPHARMA.NS", "TATACOMM.NS", "TATACONSUM.NS",
    "TATAELXSI.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TATASTEEL.NS", "TCS.NS", "TECHM.NS", "TITAN.NS", "TORNTPHARM.NS", "TRENT.NS", "ULTRACEMCO.NS",
    "UNITDSPR.NS", "VBL.NS", "VEDL.NS", "WIPRO.NS", "ZOMATO.NS", "ZYDUSLIFE.NS", "BHARATFORG.NS", "MUTHOOTFIN.NS"
]

# --- SCANNING SECTION ---
st.markdown(f"### 🔥 Live Scanning: {len(NIFTY_100)} Stocks")

for s_sym in NIFTY_100:
    res = get_market_data(s_sym)
    if res:
        st.markdown(f"""
        <div class='compact-card' style='border-left-color:{res['c']};'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div style='flex:2;'>
                    <p class='stock-name'>{s_sym.split('.')[0]}</p>
                    <p class='price-bold'>₹{res['p']}</p>
                </div>
                <div style='flex:1;'>
                    <div class='signal-label {res['bg']}'>{res['s']}</div>
                </div>
                <div style='flex:2; text-align:right;'>
                    <p class='level-text' style='color:#2e7d32;'>TGT: {res['t']}</p>
                    <p class='level-text' style='color:#c62828;'>SL: {res['sl']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
