import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Config
st.set_page_config(page_title="Arrow Ops Intelligence", layout="wide", page_icon="🏹")

# 2. "Creative Open" CSS (Bright, Airy, and Professional)
st.markdown("""
    <style>
    /* Clean White Background */
    .stApp {
        background-color: #FFFFFF;
        color: #1A1A1A;
    }
    
    /* Sidebar: Soft Gray */
    section[data-testid="stSidebar"] {
        background-color: #F8F9FA !important;
        border-right: 1px solid #E9ECEF;
    }

    /* SOP Cards: Floating White Paper Effect */
    .sop-card {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid #F1F3F5;
        margin-bottom: 25px;
    }
    
    /* Creative Buttons: Modern Outlines */
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: #FFFFFF;
        border-radius: 30px; /* Rounded pill shape */
        font-weight: 600;
        border: none;
        height: 45px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #333333 !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Search Bar: Subtle & Rounded */
    .stTextInput input {
        background-color: #F8F9FA !important;
        border: 1px solid #E9ECEF !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }

    /* Titles */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Navigation
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("## ARROW")
    
    st.markdown("---")
    st.markdown("### 📊 **Live Connectivity**")
    st.info("Unity: Connected")
    st.info("Salesforce: Active")
    st.markdown("---")
    st.link_button("CRM Access", "https://arrow.my.salesforce.com")
    st.link_button("ERP Portal", "https://unity.arrow.com")

# 4. Header & Branding
st.markdown("<p style='letter-spacing: 3px; color: #ADB5BD; font-weight: 600; margin-bottom:0;'>EXCELLENCE HUB</p>", unsafe_allow_html=True)
st.title("Ops Intelligence Portal")
st.markdown("---")

# 5. Data Retrieval
try:
    df = pd.read_csv("sop_data.csv")
    df = df.replace(np.nan, '', regex=True)
except Exception as e:
    st.error(f"Database unavailable: {e}")
    st.stop()

# 6. Interaction State
if 'search' not in st.session_state:
    st.session_state.search = ""

# 7. Creative Module Selection
st.write("### Choose a Workflow")
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("📦 Order Management"): st.session_state.search = "Unity"
with c2:
    if st.button("🚚 Logistics Flow"): st.session_state.search = "Venlo"
with c3:
    if st.button("💳 Financial SOPs"): st.session_state.search = "Refund"
with c4:
    if st.button("🔄 Reset View"): st.session_state.search = ""

# 8. Search Field
query = st.text_input("", value=st.session_state.search, placeholder="Search by keyword, system, or process name
