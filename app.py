import streamlit as st
import pandas as pd
import numpy as np
import base64

# 1. Page Config
st.set_page_config(page_title="Arrow Ops Intelligence", layout="wide", page_icon="🏹")

# 2. Enterprise CSS (Executive Dark Theme)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 1px solid #333333;
    }

    /* Clean Card Design */
    div[data-testid="column"] {
        background: #111111;
        padding: 25px;
        border-radius: 4px;
        border: 1px solid #222222;
    }
    
    /* High-Contrast Action Buttons */
    .stButton>button {
        width: 100%;
        background-color: #FFFFFF;
        color: #000000;
        border: none;
        border-radius: 2px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        height: 45px;
        transition: all 0.3s;
    }

    .stButton>button:hover {
        background-color: #CCCCCC !important;
        color: #000000 !important;
        transform: scale(1.02);
    }

    /* Search Bar Integration */
    .stTextInput input {
        background-color: #111111 !important;
        color: white !important;
        border: 1px solid #333333 !important;
        border-radius: 0px !important;
    }

    /* Metrics and Status */
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Navigation
with st.sidebar:
    # Adding the black and white logo to the sidebar
    st.image("logo.png", use_container_width=True)
    st.markdown("<h3 style='text-align: center; letter-spacing: 3px;'>CORE OPERATIONS</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.link_button("📊 SALESFORCE CRM", "https://arrow.my.salesforce.com")
    st.link_button("⚙️ UNITY SYSTEM", "https://unity.arrow.com")
    st.link_button("📂 MYCONNECT", "https://myconnect.arrow.com")
    st.markdown("---")
    st.caption("v3.0.0 | ENTERPRISE EDITION")

# 4. Executive Header
col_logo, col_text = st.columns([1, 4])
with col_logo:
    st.image("logo.png", width=150) # Secondary Logo for Header

with col_text:
    st.markdown("<h1 style='margin-bottom: 0px;'>Ops Intelligence Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888888; letter-spacing: 2px;'>GLOBAL PROCESS & SYSTEMS EXCELLENCE</p>", unsafe_allow_html=True)

# 5. Data Retrieval Logic
try:
    df = pd.read_csv("sop_data.csv")
    df = df.replace(np.nan, '', regex=True)
    
    if 'search' not in st.session_state: st.session_state.search = ""
    def set_search(term): st.session_state.search = term

    # 6. Command Center
    st.markdown("### **COMMAND CENTER**")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("ORDER STATUS"): set_search("Unity")
    with c2:
        if st.button("LOGISTICS"): set_search("Venlo")
    with c3:
        if st.button("FINANCE"): set_search("Refund")
    with c4:
        if st.button("RESET"): set_search("")

    # 7. Enterprise Search
    query = st.text_input("", value=st.session_state.search, placeholder="Search Enterprise Database (e.g. Unity, Salesforce, Case Follow-up)...")

    # 8. SOP Output (Based on SOP-7 Documentation)
    if query:
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
        
        if not results.empty:
            for _, row in results.iterrows():
                with st.container():
                    st.markdown(f"<h2 style='color: #FFFFFF; border-bottom: 1px solid #333333;'>{row['System']} | {row['Process']}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<div style='background-color: #111111; padding: 20px; border-left: 4px solid #FFFFFF;'>{row['Instructions']}</div>", unsafe_allow_html=True)
                    # Use provided doc logic for alerts
                    if "Unity" in row['System']:
                        st.warning("⚠️ ALERT OVERVIEW: Releases of alerts cannot be expedited. Coordinate with the appropriate team.")
                    st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.error("DATABASE QUERY: No matching records found.")
    else:
        st.write("---")
        st.markdown("<p style='text-align: center; color: #555555;'>Awaiting Command... Select a module or search to retrieve SOP data.</p>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"INTEGRITY ERROR: {e}")    /* Search Box Styling */
    .stTextInput input {
        background-color: #1F2937 !important;
        color: white !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Navigation
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Arrow_Electronics_logo.svg/1200px-Arrow_Electronics_logo.svg.png", width=150)
    st.markdown("### **OPERATIONS PORTAL**")
    st.markdown("---")
    st.link_button("📊 Salesforce CRM", "https://arrow.my.salesforce.com")
    st.link_button("⚙️ Unity ERP", "https://unity.arrow.com")
    st.link_button("📂 MyConnect", "https://myconnect.arrow.com")
    st.markdown("---")
    st.caption("v2.4.1 | Enterprise Support Enabled")

# 4. Main Hero Section
col_title, col_stat = st.columns([3, 1])
with col_title:
    st.title("Ops Intelligence Hub")
    st.markdown("#### *Precision-Driven Digital Workflows*")

with col_stat:
    st.metric(label="System Status", value="Operational", delta="99.9% Uptime")

# 5. Motivational Excellence Banner
st.markdown("> **“The goal is not to be better than the other man, but your previous self.”** — *Excellence in Execution*")

# 6. Data Load
try:
    df = pd.read_csv("sop_data.csv")
    df = df.replace(np.nan, '', regex=True)
    
    if 'search' not in st.session_state: st.session_state.search = ""
    def set_search(term): st.session_state.search = term

    # 7. Strategic Category Cards
    st.write("### **COMMAND CENTER**")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.write("📦 **ORDER MGMT**")
        if st.button("RUN UNITY SOP"): set_search("Unity")
    with c2:
        st.write("🚚 **LOGISTICS**")
        if st.button("RUN VENLO SOP"): set_search("Venlo")
    with c3:
        st.write("💰 **FINANCE**")
        if st.button("RUN REFUND SOP"): set_search("Refund")
    with c4:
        st.write("🔄 **SYSTEM**")
        if st.button("CLEAR ALL"): set_search("")

    st.markdown("---")

    # 8. Modern Search
    query = st.text_input("", value=st.session_state.search, placeholder="Enter process keyword or system ID...")

    # 9. Results with Professional Styling
    if query:
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
        
        if not results.empty:
            for _, row in results.iterrows():
                with st.container():
                    st.markdown(f"### 📂 {row['System']} : {row['Process']}")
                    st.info(row['Instructions'])
                    if str(row['Screenshot_URL']).startswith("http"):
                        st.image(row['Screenshot_URL'], use_container_width=True)
                    st.markdown("---")
        else:
            st.error("⚠️ DATA NOT FOUND: Please check the system keyword.")
    else:
        st.markdown("### **Awaiting Input...**")
        st.write("Select a Command Center module to begin data retrieval.")

except Exception as e:
    st.error(f"INTEGRITY ERROR: {e}")
# 5. Data Loading
try:
    df = pd.read_csv("sop_data.csv")
    df = df.replace(np.nan, '', regex=True)
    
    if 'search' not in st.session_state:
        st.session_state.search = ""

    def set_search(term):
        st.session_state.search = term

    # 6. Styled Topic Selection
    st.write("### 📂 Categories")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("📦 Order Flow"): set_search("Unity")
    with c2:
        if st.button("🚚 Logistics"): set_search("Venlo")
    with c3:
        if st.button("💳 Finance"): set_search("Refund")
    with c4:
        if st.button("🔄 Clear"): set_search("")

    # 7. Search Bar
    query = st.text_input("", value=st.session_state.search, placeholder="Search for a process (e.g., 'Address', 'Case', 'Tracking')...")

    # 8. Results
    if query:
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
        
        if not results.empty:
            for _, row in results.iterrows():
                with st.expander(f"📝 {row['System']} | {row['Process']}"):
                    st.markdown(f"**Action Steps:**")
                    st.write(row['Instructions'])
                    
                    if str(row['Screenshot_URL']).startswith("http"):
                        st.image(row['Screenshot_URL'], use_container_width=True)
        else:
            st.warning("No procedure matches that search.")
    else:
        st.write("---")
        st.subheader("Welcome to the Operations Engine")
        st.write("Select a category above to begin your workflow.")

except Exception as e:
    st.error(f"⚠️ Load Error: {e}")
