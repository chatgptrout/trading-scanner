import streamlit as st
import requests

st.title("SANTOSH SCANNER")

token = st.sidebar.text_input("Mobile Token", type="password")

if token:
    try:
        url = "https://api.dhan.co/v2/marketfeed/ltp"
        headers = {'access-token': token, 'Content-Type': 'application/json'}
        
        # Dhan official symbol for Crude Oil Feb
        payload = {
            "instruments": [
                {"symbol": "CRUDEOIL FEB FUT", "exchange": "MCX", "instrument_type": "FUTCOM"}
            ]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            price_dict = data.get('data', {})
            if price_dict:
                # Direct value nikalna
                price = list(price_dict.values())[0]
                st.header(f"CRUDE OIL: Rs {price}")
                st.success("LIVE MATCHED")
            else:
                # Agar phir bhi None aaye toh response print karke check karte hain
                st.warning("Server connected but no price. Check Data API switch in Dhan Profile.")
        else:
            st.error(f"Dhan Error: {data.get('remarks')}")
            
    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.info("Paste Token in Sidebar")
