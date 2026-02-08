import streamlit as st
import pandas as pd
import numpy as np

# 1. GLOBAL SETTINGS
st.set_page_config(page_title="Arrow Ops Intelligence", layout="wide", page_icon="🏹")

# 2. EXECUTIVE CSS (DARK MODE & TERMINAL STYLE)
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #FFFFFF; }
    section[data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #222222; }
    
    /* SOP CARD DESIGN */
    .sop-card {
        background-color: #0f0f0f;
        padding: 24px;
        border: 1px solid #222222;
        border-left: 4px solid #ffffff;
        margin-bottom: 20px;
    }
    
    /* BUTTONS: HIGH-CONTRAST */
    .stButton>button {
        width: 100%;
        background-color: #ffffff;
        color: #000000;
        border-radius: 0px;
        font-weight: 900;
        letter-spacing: 2px;
        border: none;
        height: 45px;
    }
    
    /* SEARCH BOX */
    .stTextInput input {
        background-color: #0f0f0f !important;
        color: white !important;
        border: 1px solid #333333 !important;
        border-radius: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR: SYSTEM STATUS & LOGO
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.write("### [ LOGO PENDING ]")
        
    st.markdown("<h3 style='text-align: center; letter-spacing: 2px;'>SYSTEM STATUS</h3>", unsafe_allow_html=True)
    st.success("● UNITY: ONLINE")
    st.success("● SFDC: CONNECTED")
    st.warning("● IMS SYNC: DELAYED")
    st.markdown("---")
    st.link_button("📊 SALESFORCE CRM", "https://arrow.my.salesforce.com")
    st.link_button("⚙️ UNITY SYSTEM", "https://unity.arrow.com")
    st.caption("v3.2.0 | SECURE TERMINAL")

# 4. HEADER
st.markdown("<h1 style='letter-spacing: -1px;'>Ops Intelligence Portal</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #666666; letter-spacing: 5px; font-size: 10px;'>GLOBAL PROCESS EXCELLENCE</p>", unsafe_allow_html=True)
st.markdown("---")

# 5. MAIN LOGIC BLOCK
try:
    # DATA INGESTION
    df = pd.read_csv("sop_data.csv")
    df = df.replace(np.nan, '', regex=True)
    
    if 'search' not in st.session_state:
        st.session_state.search = ""

    # COMMAND MODULE BUTTONS
    st.write("### COMMAND MODULES")
    c1, c2, c3, c4 = st.columns(4)
    
    if c1.button("ORDER STATUS"): st.session_state.search = "Unity"
    if c2.button("LOGISTICS"): st.session_state.search = "Venlo"
    if c3.button("FINANCE"): st.session_state.search = "Refund"
    if c4.button("RESET"): st.session_state.search = ""

    # SEARCH INTERFACE
    query = st.text_input("QUERY DATABASE", value=st.session_state.search, placeholder="Enter Keyword (e.g. Case, Tracker, Unity)...")

    # RESULT GENERATION
    if query:
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
