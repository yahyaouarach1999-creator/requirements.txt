import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Config
st.set_page_config(page_title="Arrow Ops Intelligence", layout="wide", page_icon="🏹")

# 2. Executive CSS (Strictly formatted to avoid Syntax Errors)
st.markdown("""
    <style>
    /* Black & White Enterprise Theme */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    section[data-testid="stSidebar"] {
        background-color: #0A0A0A !important;
        border-right: 1px solid #222222;
    }
    /* Card Styling */
    .sop-card {
        background-color: #111111;
        padding: 20px;
        border-left: 5px solid #FFFFFF;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    /* Buttons */
    .stButton>button {
        width: 100%;
        background-color: #FFFFFF;
        color: #000000;
        border-radius: 0px;
        font-weight: 800;
        letter-spacing: 1px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #CCCCCC !important;
        color: #000000 !important;
    }
    /* TextInput */
    .stTextInput input {
        background-color: #111111 !important;
        color: white !important;
        border: 1px solid #333333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Navigation & Status
with st.sidebar:
    st.image("logo.png", use_container_width=True)
    st.markdown("<h3 style='text-align: center; letter-spacing: 2px;'>SYSTEM STATUS</h3>", unsafe_allow_html=True)
    
    # Real-time feel status monitors
    st.success("● UNITY: ONLINE")
    st.success("● SALESFORCE: CONNECTED")
    st.warning("● IMS SYNC: DELAY (2m)")
    
    st.markdown("---")
    st.link_button("📊 SALESFORCE CRM", "https://arrow.my.salesforce.com")
    st.link_button("⚙️ UNITY SYSTEM", "https://unity.arrow.com")
    st.markdown("---")
    st.caption("v3.1.0 | AUTHORIZED ACCESS ONLY")

# 4. Executive Header
col_logo, col_text = st.columns([1, 5])
with col_logo:
    st.image("logo.png", width=120)

with col_text:
    st.markdown("<h1 style='margin:0;'>Ops Intelligence Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666666; letter-spacing: 3px;'>GLOBAL PROCESS EXCELLENCE & COMPLIANCE</p>", unsafe_allow_html=True)

# 5. Data Retrieval
try:
    df = pd.read_csv("sop_data.csv")
    df = df.replace(np.nan, '', regex=True)
    
    if 'search' not in st.session_state: 
        st.session_state.search = ""

    def set_search(term):
        st.session_state.search = term

    # 6. Command Center Modules
