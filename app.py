import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Arrow Ops Intelligence", layout="wide", page_icon="🏹")

# 2. Creative Studio CSS (Bright, Minimalist, High-End)
st.markdown("""
    <style>
    /* Light Mode Base */
    .stApp {
        background-color: #FFFFFF;
        color: #2D3436;
    }
    
    /* Sidebar: Clean & Subtle */
    section[data-testid="stSidebar"] {
        background-color: #F8F9FA !important;
        border-right: 1px solid #F1F3F5;
    }

    /* Floating Paper Cards */
    .sop-card {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.04);
        border: 1px solid #F1F3F5;
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }
    .sop-card:hover {
        transform: translateY(-5px);
    }
    
    /* Modern Pill Buttons */
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: #FFFFFF;
        border-radius: 50px;
        font-weight: 600;
        border: none;
        height: 50px;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        background-color: #333333 !important;
        color: white !important;
    }
    
    /* Elegant Search Bar */
    .stTextInput input {
        background-color: #F8F9FA !important;
        border: 1px solid #E9ECEF !important;
        border-radius: 15px !important;
        height: 55px !important;
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
    st.markdown("#### **Network Status**")
    st.success("● Unity Connected")
    st.success("● SFDC Active")
    st.markdown("---")
    st.link_button("Salesforce CRM", "https://arrow.my.salesforce.com")
    st.link_button("Unity Portal", "https://unity.arrow.com")

# 4. Header Section
st.markdown("<p style='color: #A0A0A0; letter-spacing: 4px; font-weight: bold; margin:0;'>KNOWLEDGE SYSTEM</p>", unsafe_allow_html=True)
st.title("Operations Intelligence Hub")
st.markdown("---")

# 5. Data Handling
try:
    df = pd.read_csv("sop_data
