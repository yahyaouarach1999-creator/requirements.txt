import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# --- STRICT SECURITY ---
AUTHORIZED_USER = "yahya.ouarach@arrow.com" 

# Styling: Professional White
st.markdown("""
<style>
    .stApp { background-color: #ffffff !important; color: #000000 !important; }
    input { border: 2px solid #005a9c !important; color: #000000 !important; }
    .result-card { 
        border: 1px solid #e1e4e8; padding: 20px; border-radius: 10px; 
        background-color: #fcfcfc; margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .instructions { 
        background-color: #f1f3f4; padding: 15px; 
        border-left: 5px solid #005a9c; white-space: pre-wrap; color: #202124 !important; 
    }
    /* Sidebar text color */
    [data-testid="stSidebar"] { background-color: #f8f9fa !important; }
    label, p, span, h1, h2, h3 { color: #000000 !important; }
</style>
""", unsafe_allow_html=True)

if 'auth' not in st.session_state:
    st.session_state.auth = False

# 2. LOGIN GATE
if not st.session_state.auth:
    st.title("🏹 Arledge")
    st.subheader("Secure Access Gateway")
    email_input = st.text_input("Enter Arrow Email").lower().strip()
    
    if st.button("Access System"):
        if email_input == AUTHORIZED_USER:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Unauthorized Access.")
    st.stop()

# 3. SIDEBAR: TOOLS & REPORTING
with st.sidebar:
    st.title("🏹 Resource Hub")
    st.divider()
    
    st.markdown("### 🛠 Internal Tools")
    st.markdown("• [🥷 OMT Ninja](https://omt-ninja.arrow.com)")
    st.markdown("• [📋 ETQ Portal](https://etq.arrow.com)")
    st.markdown("• [💼 Salesforce](https://arrow.my.salesforce.com)")
    st.markdown("• [☁️ Oracle Unity](https://ebs.arrow.com)")
    
    st.divider()
    st.markdown("### ⚠️ Report an Issue")
    st.markdown("Use this for technical glitches:")
    st.markdown("• [My Connect IT Support](https://arrow.service-now.com/myconnect)")
    
    st.divider()
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()

# 4. DATA & SEARCH
@st.cache_data
def load_db():
    if os.path.exists("master_ops_database.csv"):
        return pd.read_csv("master_ops_database.csv").fillna("")
    return pd.DataFrame()

df = load_db()

st.title("Search Knowledge Center")
query = st.text_input("", placeholder="Search procedures, credentials, or collectors...")

if query:
    results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="result-card">
                <span style="color:#005a9c; font-weight:bold; font-size:0.75rem;">{row['System']}</span>
                <h3 style="margin-top:5px;">{row['Process']}</h3>
                <div class="instructions">{row['Instructions']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No results found.")
