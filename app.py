import streamlit as st
import requests

st.title("SANTOSH SCANNER")

token = st.sidebar.text_input("Mobile Token", type="password")

if token:
    try:
        # Direct API URL
        url = "https://api.dhan.co/v2/marketfeed/ltp"
        headers = {'access-token': token, 'Content-Type': 'application/json'}
        
        # Exact Symbol match for MCX Crude Oil Feb Future
        payload = {
            "instruments": [
                {"symbol": "CRUDEOIL FEB FUT", "exchange": "MCX", "instrument_type": "FUTCOM"}
            ]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            # Checking if data exists
            prices = data.get('data', {})
            if prices:
                # Loop to find the price even if key format changes
                val = list(prices.values())[0]
                st.header(f"PRICE: Rs {val}")
                st.success("CONNECTED")
            else:
                st.warning("Market Data Empty - Check Token or Symbol")
        else:
            st.error(f"Dhan Error: {data.get('remarks')}")
            
    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.info("Paste Token in Sidebar")


