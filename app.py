import streamlit as st
from dhanhq import dhanhq

st.title("🚀 SMART SCANNER")

# Sidebar for Token
token = st.sidebar.text_input("Mobile Token", type="password")

if token:
    try:
        # Dhan connect using your Client ID
        dhan = dhanhq("1106004757", token) 
        
        # Correct command for fetching price
        # Note: We use 'get_ltp' instead of 'get_ltp_data'
        instruments = [{"symbol": "CRUDEOIL FEB FUT", "exchange": "MCX", "instrument_type": "FUTCOM"}]
        data = dhan.get_ltp(instruments) 
        
        if data.get('status') == 'success':
            # Extracting the live price from the response
            price = data.get('data', {}).get('MCX:CRUDEOIL FEB FUT', 0)
            st.metric("CRUDE OIL FEB FUT", f"₹{price}")
            st.success("✅ LIVE MATCHED!")
        else:
            st.error(f"Dhan Error: {data.get('remarks')}")
            
    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.info("👈 Please enter your Dhan Token in the sidebar")
