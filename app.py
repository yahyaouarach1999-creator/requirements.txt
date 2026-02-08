import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Arrow Ops Intelligence", layout="wide", page_icon="🏹")

# 2. Styling (Clean, Bright, Minimalist)
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #2D3436; }
    section[data-testid="stSidebar"] { background-color: #F8F9FA !important; border-right: 1px solid #F1F3F5; }
    .sop-card {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.04);
        border: 1px solid #F1F3F5;
        margin-bottom: 25px;
    }
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: #FFFFFF;
        border-radius: 50px;
        font-weight: 600;
        border: none;
        height: 50px;
    }
    .stButton>button:hover { background-color: #333333 !important; color: white !important; }
    .stTextInput input {
        background-color: #F8F9FA !important;
        border: 1px solid #E9ECEF !important;
        border-radius: 15px !important;
        height: 50px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("### **ARROW OPS**")
    st.markdown("---")
    st.success("● Unity Connected")
    st.success("● SFDC Active")
    st.markdown("---")
    st.link_button("Salesforce CRM", "https://arrow.my.salesforce.com")
    st.link_button("Unity Portal", "https://unity.arrow.com")

# 4. Header
st.markdown("<p style='color: #A0A0A0; letter-spacing: 4px; font-weight: bold;'>KNOWLEDGE SYSTEM</p>", unsafe_allow_html=True)
st.title("Operations Intelligence Hub")
st.markdown("---")

# 5. Safe Data Load
@st.cache_data # PRO TIP: This makes your app much faster!
def load_data():
    try:
        data = pd.read_csv("sop_data.csv")
        return data.replace(np.nan, '', regex=True)
    except:
        return None

df = load_data()

if df is None:
    st.error("Missing 'sop_data.csv' file in repository.")
    st.stop()

# 6. Session State for Search
if 'search' not in st.session_state:
    st.session_state.search = ""

# 7. Workspace Modules (Using a callback for smoother transitions)
st.write("### Workspace Selection")
c1, c2, c3, c4 = st.columns(4)

if c1.button("📦 Order Management"): st.session_state.search = "Unity"
if c2.button("🚚 Logistics"): st.session_state.search = "Venlo"
