import streamlit as st
import requests

st.title("SANTOSH SCANNER")

token = st.sidebar.text_input("Mobile Token", type="password")

if token:
    try:
        # Market Feed URL
        url = "https://api.dhan.co/v2/marketfeed/ltp"
        headers = {'access-token': token, 'Content-Type': 'application/json'}
        
        # MCX Crude Oil Feb Fut ki asli Security ID '63' hai
        payload = {
            "instruments": [
                {"symbol": "CRUDEOIL FEB FUT", "exchange": "MCX", "instrument_type": "FUTCOM", "security_id": "63"}
            ]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        if response.status_code == 200:
            # Price nikalne ka sabse foolproof tarika
            price_dict = data.get('data', {})
            if price_dict:
                price = list(price_dict.values())[0]
                st.header(f"CRUDE OIL: Rs {price}")
                st.success("LIVE MATCHED")
            else:
                st.warning("No Data: Dhan is not sending price for this ID.")
        else:
            st.error(f"Dhan Error: {data.get('remarks')}")
            
    except Exception as e:
        st.error(f"System Error: {e}")
else:
    st.info("Paste 'OfficeScanner' Token in Sidebar")
