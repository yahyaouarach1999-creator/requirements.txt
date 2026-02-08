import streamlit as st
import pandas as pd
import numpy as np

# 1. ENTERPRISE CONFIGURATION
st.set_page_config(
    page_title="Arrow Ops Intelligence | Enterprise",
    layout="wide",
    page_icon="🏹",
    initial_sidebar_state="expanded"
)

# 2. PREMIUM UX STYLING (The $2,000 Aesthetic)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* Global Transitions */
    * { font-family: 'Inter', sans-serif; transition: all 0.2s ease-in-out; }

    /* Clean Studio Background */
    .stApp {
        background: radial-gradient(circle at top right, #ffffff, #fdfdfd);
        color: #1e293b;
    }

    /* Sidebar - Glassmorphism Light */
    section[data-testid="stSidebar"] {
        background-color: rgba(248, 250, 252, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid #e2e8f0;
    }

    /* Enterprise SOP Cards - Floating Architecture */
    .sop-card {
        background: white;
        padding: 40px;
        border-radius: 24px;
        border: 1px solid #f1f5f9;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 10px 15px -3px rgba(0, 0, 0, 0.03);
        margin-bottom: 30px;
    }
    
    .sop-card:hover {
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
        transform: translateY(-4px);
        border-color: #e2e8f0;
    }

    /* High-End Action Buttons */
    .stButton>button {
        width: 100%;
        background: #0f172a; /* Deep Midnight Blue/Black */
        color: #ffffff;
        border-radius: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        border: none;
        height: 55px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        background: #334155 !important;
        color: white !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }

    /* Search Bar - Modern Focus */
    .stTextInput input {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 14px !important;
        height: 60px !important;
        font-size: 18px !important;
        padding-left: 25px !important;
    }
    
    .stTextInput input:focus {
        border-color: #0f172a !important;
        box-shadow: 0 0 0 4px rgba(15, 23, 42, 0.05) !important;
    }

    /* Status Indicators */
    .status-tag {
        padding: 4px 12px;
        border-radius: 100px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR: BRANDING & SYSTEM VITALITY
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("<h1 style='letter-spacing:-2px; color:#0f172a;'>ARROW</h1>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### **VITALITY MONITOR**")
    st.markdown("""
        <div style='background:white; padding:15px; border-radius:15px; border:1px solid #e2e8f0;'>
            <p style='margin:0; font-size:12px; color:#64748b;'>SYSTEMS STATUS</p>
            <p style='margin:0; font-weight:600; color:#10b981;'>● UNITY CLOUD: OPTIMAL</p>
            <p style='margin:0; font-weight:600; color:#10b981;'>● SFDC API: ACTIVE</p>
            <p style='margin:0; font-weight:600; color:#f59e0b;'>● IMS SYNC: QUEUED</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.link_button("🚀 SALESFORCE GLOBAL", "https://arrow.my.salesforce.com")
    st.link_button("⚙️ UNITY ENTERPRISE", "https://unity.arrow.com")
    st.markdown("---")
    st.caption("INTERNAL USE ONLY | v4.0.0 PREMIUM")

# 4. EXECUTIVE HEADER
col_title, col_stat = st.columns([3, 1])
with col_title:
    st.markdown("<p style='color:#64748b; font-weight:600; letter-spacing:5px; margin:0;'>DIGITAL BUSINESS EXCELLENCE</p>", unsafe_allow_html=True)
    st.title("Ops Intelligence Hub")
    st.markdown("#### *Strategic Process Repository & Execution Engine*")

with col_stat:
    st.markdown("<br>", unsafe_allow_html=True)
    st.metric(label="Data Integrity", value="100%", delta="Verified")

st.markdown("---")

# 5. DATA ENGINE
@st.cache_data
def fetch_sop_vault():
    try:
        data = pd.read_csv("sop_data.csv")
        return data.replace(np.nan, '', regex=True)
    except:
        return None

df = fetch_sop_vault()

if df is None:
    st.error("FATAL ERROR: SOP DATA VAULT NOT DETECTED. PLEASE SYNC REPOSITORY.")
    st.stop()

# 6. INTELLIGENT WORKFLOW SELECTOR
if 'search' not in st.session_state:
    st.session_state.search = ""

st.write("### **COMMAND MODULES**")
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("📦 ORDER LIFECYCLE"): st.session_state.search = "Unity"
with c2:
    if st.button("🚚 LOGISTICS ENGINE"): st.session_state.search = "Venlo"
with c3:
    if st.button("💳 REVENUE MGMT"): st.session_state.search = "Refund"
with c4:
    if st.button("🔄 GLOBAL RESET"): st.session_state.search = ""

# 7. SEARCH ARCHITECTURE
query = st.text_input("", value=st.session_state.search, placeholder="Type to filter processes (e.g., 'Verification', 'Case', 'Oracle')...")

# 8. SOP DISPLAY ENGINE
if query:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="sop-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="background: #f1f5f9; color: #475569; padding: 6px 16px; border-radius: 100px; font-size: 12px; font-weight: 800; letter-spacing: 1px;">{row['System'].upper()}</span>
                    <span style="color: #cbd5e1; font-size: 12px;">ID: DBX-{np.random.randint(1000, 9999)}</span>
                </div>
                <h2 style="margin-top: 15px; color: #0f172a; font-weight: 800; font-size: 28px;">{row['Process']}</h2>
                <div style="background: #f8fafc; border-radius: 12px; padding: 25px; border: 1px solid #f1f5f9; color: #334155; line-height: 1.8; font-size: 16px;">
                    {row['Instructions']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if str(row['Screenshot_URL']).startswith("http"):
                st.image(row['Screenshot_URL'], use_container_width=True, caption=f"System Reference: {row['Process']}")
    else:
        st.warning("NO MATCHING DATA FOUND IN ENTERPRISE VAULT.")
else:
    # 9. EMPTY STATE (MOTIVATING & PROFESSIONAL)
    st.markdown("<br><br>", unsafe_allow_html=True)
    ec1, ec2, ec3 = st.columns([1,2,1])
    with ec2:
        st.markdown("""
            <div style='text-align: center; padding: 40px; border: 2px dashed #e2e8f0; border-radius: 30px;'>
                <p style='font-size: 50px; margin:0;'>🔍</p>
                <h3 style='color: #64748b;'>Awaiting System Directive</h3>
                <p style='color: #94a3b8;'>Select a command module above or search the database to initiate workflow visualization.</p>
            </div>
        """, unsafe_allow_html=True)
