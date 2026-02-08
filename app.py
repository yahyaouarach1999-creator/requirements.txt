import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Config
st.set_page_config(page_title="Arrow Ops Intelligence", layout="wide", page_icon="🏹")

# 2. Enterprise CSS Injection (The "Mature" Look)
st.markdown("""
    <style>
    /* Main App Background - Slate Gray */
    .stApp {
        background-color: #111827;
        color: #F9FAFB;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #1F2937 !important;
        border-right: 1px solid #374151;
    }

    /* Professional Card Styling */
    div[data-testid="column"] {
        background: #1F2937;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #374151;
        transition: transform 0.2s, border-color 0.2s;
    }
    
    div[data-testid="column"]:hover {
        border-color: #EF4444; /* Arrow Red Glow */
        transform: translateY(-5px);
    }

    /* Custom Header Text */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -1px;
        color: #FFFFFF;
    }

    /* Mature Button Styling */
    .stButton>button {
        width: 100%;
        background-color: #374151;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        background-color: #EF4444 !important;
        color: white !important;
    }

    /* Search Box Styling */
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
