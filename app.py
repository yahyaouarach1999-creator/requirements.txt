import streamlit as st
import pandas as pd
import numpy as np

# 1. EXECUTIVE SETTINGS
st.set_page_config(page_title="Arrow Ops Intelligence", layout="wide", page_icon="🏹")

# 2. HIGH-END BRANDING CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    .stApp { background-color: #FFFFFF; font-family: 'Inter', sans-serif; }
    
    /* Logo Box - Fixing the "Out of Image" look */
    .logo-container {
        padding: 20px;
        text-align: center;
        background: #f8f9fa;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    
    /* Premium SOP Cards */
    .sop-card {
        background: white;
        padding: 35px;
        border-radius: 16px;
        border: 1px solid #edf2f7;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
    }

    /* Actionable Instructions Styling */
    .step-box {
        background-color: #f8fafc;
        border-left: 4px solid #1e293b;
        padding: 20px;
        color: #334155;
        border-radius: 0 8px 8px 0;
    }

    /* Sidebar Glass UI */
    section[data-testid="stSidebar"] { background-color: #f1f5f9 !important; }
    
    /* Bold Buttons */
    .stButton>button {
        background-color: #000000;
        color: white;
        border-radius: 8px;
        font-weight: 700;
        height: 50px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR WITH LOGO FIX
with st.sidebar:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("<h2 style='color:#000;'>ARROW</h2>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### **Operational Health**")
    st.progress(92, text="Unity Processing Speed")
    st.progress(100, text="Salesforce API Sync")
    st.markdown("---")
    st.link_button("CRM Terminal", "https://arrow.my.salesforce.com")
    st.link_button("ERP Unity", "https://unity.arrow.com")

# 4. DASHBOARD HEADER
st.markdown("<p style='color:#94a3b8; font-weight:700; letter-spacing:3px;'>INTERNAL OPERATIONS HUB</p>", unsafe_allow_html=True)
st.title("Ops Intelligence & Strategy")
st.markdown("---")

# 5. DATA LOADING
@st.cache_data
def load_sop_vault():
    try:
        return pd.read_csv("sop_data.csv").replace(np.nan, '', regex=True)
    except:
        return None

df = load_sop_vault()

# 6. COMMAND MODULES
if 'search' not in st.session_state: st.session_state.search = ""

c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("📦 Order Life-Cycle"): st.session_state.search = "Unity"
with c2: 
    if st.button("🚚 Logistics & Venlo"): st.session_state.search = "Venlo"
with c3: 
    if st.button("💰 Revenue Ops"): st.session_state.search = "Refund"
with c4: 
    if st.button("🔄 Clear System"): st.session_state.search = ""

# 7. SEARCH & RESULTS
query = st.text_input("", value=st.session_state.search, placeholder="Enter workflow keyword (e.g. 'RMA', 'Tracking', 'Proforma')...")

if query and df is not None:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="sop-card">
                    <span style="color:#64748b; font-size:12px; font-weight:700;">SYSTEM: {row['System'].upper()}</span>
                    <h2 style="margin-top:5px; margin-bottom:20px;">{row['Process']}</h2>
                    <div class="step-box">{row['Instructions']}</div>
                </div>
                """, unsafe_allow_html=True)
                if str(row['Screenshot_URL']).startswith("http"):
                    st.image(row['Screenshot_URL'], use_container_width=True)
    else:
        st.error("No matching enterprise process found.")
else:
    st.info("Select a workflow module above to begin process visualization.")
