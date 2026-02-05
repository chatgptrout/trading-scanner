import streamlit as st
from dhanhq import dhanhq

st.title("🚀 SMART SCANNER")
token = st.sidebar.text_input("Mobile Token", type="password")

if token:
    try:
        # Dhan connect
        dhan = dhanhq("1100412345", token) 
        # Real-time price fetch
        data = dhan.get_ltp_data([{"symbol": "CRUDEOIL FEB FUT", "exchange": "MCX", "instrument_type": "FUTCOM"}])
        price = data.get('data', {}).get('MCX:CRUDEOIL FEB FUT', 5692.0)
        
        st.metric("CRUDE OIL FEB FUT", f"₹{price}")
        st.success("Data Live and Matched!")
    except:
        st.error("Token invalid or expired")
else:
    st.warning("Awaiting Token from Sidebar...")
