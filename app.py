import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Arrow Ops Intelligence", layout="wide", page_icon="🏹")

# 2. Styling: Modern, Bright, and Open
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #2D3436; }
    section[data-testid="stSidebar"] { background-color: #F8F9FA !important; border-right: 1px solid #F1F3F5; }

    /* Floating Studio Cards */
    .sop-card {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.04);
        border: 1px solid #F1F3F5;
        margin-bottom: 25px;
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
    }
    .stButton>button:hover { background-color: #333333 !important; color: white !important; }
    
    /* Search Bar */
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
try:
    df = pd.read_csv("sop_data.csv")
    df = df.replace(np.nan, '', regex=True)
except Exception as e:
    st.error("Missing 'sop_data.csv' file in repository.")
    st.stop()

# 6. Interaction Logic
if 'search' not in st.session_state:
    st.session_state.search = ""

# 7. Workspace Modules
st.write("### Workspace Selection")
c1, c2, c3, c4 = st.columns(4)
if c1.button("📦 Order Management"): st.session_state.search = "Unity"
if c2.button("🚚 Logistics"): st.session_state.search = "Venlo"
if c3.button("💳 Financials"): st.session_state.search = "Refund"
if c4.button("🔄 Reset View"): st.session_state.search = ""

# 8. Search Input
query = st.text_input("Query Database", value=st.session_state.search, placeholder="Search by system or process name...")

# 9. Results Output
if query:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="sop-card">
                <span style="background: #F8F9FA; padding: 6px 15px; border-radius: 30px; font-size: 11px; font-weight: bold; color: #888;">{row['System'].upper()}</span>
                <h2 style="margin-top: 15px; color: #000;">{row['Process']}</h2>
                <div style="color: #555; line-height: 1.8;">{row['Instructions']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if str(row['Screenshot_URL']).startswith("http"):
                st.image(row['Screenshot_URL'], use_container_width=True)
    else:
        st.warning("No records found.")
else:
    st.markdown("<br><p style='text-align: center; color: #CCC;'>Select a workspace above or type to search.</p>", unsafe_allow_html=True)
