import streamlit as st
import pandas as pd
import re

# --- 1. SECURITY SETTINGS ---
ACCESS_KEY = "Arrow2026" # This is the key you give to your team

if 'access_granted' not in st.session_state:
    st.session_state.access_granted = False

# --- 2. THE LOGIN GATE ---
if not st.session_state.access_granted:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Arrow_Electronics_Logo.svg", width=200)
        st.title("Operations Academy")
        st.info("Please enter the Internal Access Key to proceed.")
        
        user_key = st.text_input("Access Key", type="password")
        
        if st.button("Enter Terminal"):
            if user_key == ACCESS_KEY:
                st.session_state.access_granted = True
                st.rerun()
            else:
                st.error("Invalid Key. Please contact your manager.")
    st.stop() # Stops the rest of the app from loading until key is correct

# --- 3. THE REST OF YOUR SEARCH APP ---
# (Once they pass the gate, the search engine below appears)

st.title("🏹 Ops Search Portal")
st.success("Authorized Access: Internal Arrow Only")

# ... rest of your search and CSV logic goes here ...
