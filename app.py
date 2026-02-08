import streamlit as st
import pandas as pd
import numpy as np

# 1. GLOBAL SETTINGS
st.set_page_config(page_title="Arrow Ops Intelligence", layout="wide", page_icon="🏹")

# 2. EXECUTIVE CSS (ULTRA-MINIMALIST DARK THEME)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    section[data-testid="stSidebar"] { background-color: #080808 !important; border-right: 1px solid #1A1A1A; }
    
    /* SOP CARD DESIGN */
    .sop-card {
        background-color: #0A0A0A;
        padding: 30px;
        border: 1px solid #1A1A1A;
        border-left: 2px solid #FFFFFF;
        margin-bottom: 25px;
    }
    
    /* BUTTONS: INDUSTRIAL STYLE */
    .stButton>button {
        width: 100%;
        background-color: #FFFFFF;
        color: #000000;
        border-radius: 0px;
        font-weight: 900;
        letter-spacing: 2px;
        border: none;
        height: 50px;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #444444 !important;
        color: #FFFFFF !important;
    }
    
    /* SEARCH BOX */
    .stTextInput input {
        background-color: #000000 !important;
        color: white !important;
        border: 1px solid #1A1A1A !important;
        border-radius: 0px !important;
        height: 45px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR: STATUS & LOGO
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("<h2 style='text-align:center;'>ARROW</h2>", unsafe_allow_html=True)
        
    st.markdown("<br><h5 style='letter-spacing: 2px; color: #444444;'>SYSTEM STATUS</h5>", unsafe_allow_html=True)
    st.info("● UNITY: ONLINE")
    st.info("● SFDC: CONNECTED")
    st.markdown("---")
    st.link_button("📊 SALESFORCE CRM", "https://arrow.my.salesforce.com")
    st.link_button("⚙️ UNITY SYSTEM", "https://unity.arrow.com")
    st.caption("SECURE TERMINAL V3.3.0")

# 4. HEADER
st.markdown("<h1 style='font-size: 3rem; font-weight: 800; margin-bottom: 0;'>Ops Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #444444; letter-spacing: 6px; font-size: 12px; margin-top: 0;'>GLOBAL PROCESS REPOSITORY</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 5. DATA LOADING (SAFE ZONE)
try:
    df = pd.read_csv("sop_data.csv")
    df = df.replace(np.nan, '', regex=True)
except Exception as e:
    st.error(f"DATABASE OFFLINE: {e}")
    st.stop()

# 6. SEARCH STATE
if 'search' not in st.session_state:
    st.session_state.search = ""

# 7. COMMAND MODULES
c1, c2, c3, c4 = st.columns(4)
if c1.button("ORDER STATUS"): st.session_state.search = "Unity"
if c2.button("LOGISTICS"): st.session_state.search = "Venlo"
if c3.button("FINANCE"): st.session_state.search = "Refund"
if c4.button("RESET"): st.session_state.search = ""

# 8. SEARCH INTERFACE
query = st.text_input("", value=st.session_state.search, placeholder="ENTER COMMAND OR KEYWORD...")

# 9. OUTPUT ENGINE
if query:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            st
