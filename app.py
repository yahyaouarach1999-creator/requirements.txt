import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# --- STRICT SECURITY WHITELIST ---
# Removed others - only your account remains
AUTHORIZED_USERS = [
    "yahya.ouarach@arrow.com"
]

# Styling: Professional White & High Contrast
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
    [data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 1px solid #dee2e6; }
    label, p, span, h1, h2, h3 { color: #000000 !important; }
</style>
""", unsafe_allow_html=True)

if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.user = ""

# 2. LOGIN GATE
if not st.session_state.auth:
    st.title("🏹 Arledge")
    st.subheader("Authorized Access Only")
    email_input = st.text_input("Enter Arrow Email").lower().strip()
    
    if st.button("Verify Identity"):
        if email_input in AUTHORIZED_USERS:
            st.session_state.auth = True
            st.session_state.user = email_input
            st.rerun()
        else:
            st.error("Access Denied: Email not authorized.")
    st.stop()

# 3. SIDEBAR: TOOLS & REPORTING
with st.sidebar:
    st.title("🏹 Resource Hub")
    st.caption(f"Logged in: {st.session_state.user}")
    st.divider()
    
    st.markdown("### ⚡ Quick Access")
    st.markdown("• [☁️ Oracle Unity (Direct)](https://acerpebs.arrow.com/OA_HTML/RF.jsp?function_id=16524&resp_id=57098&resp_appl_id=20008&security_group_id=0&lang_code=US&oas=k2oTjdeInl3Bik8l6rTqgA..)")
    st.markdown("• [🚩 Salesforce: My Cases](https://arrowcrm.lightning.force.com/lightning/o/Case/list?filterName=My_Open_and_Flagged_With_Reminder)")
    st.markdown("• [💻 SWB Dashboard](https://acswb.arrow.com/Swb/)")
    st.markdown("• [📋 ETQ Portal](https://arrow.etq.com/prod/rel/#/app/auth/login)")
    st.markdown("• [🛠 MyConnect IT](https://arrow.service-now.com/myconnect)")
    
    st.divider()
    st.markdown("### ⚠️ Report an Issue")
    # Updated to your email only
    st.markdown(f"Contact Admin: [yahya.ouarach@arrow.com](mailto:yahya.ouarach@arrow.com)")
    
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()

# 4. DATABASE LOADING
@st.cache_data
def load_db():
    file_path = "master_ops_database.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path, encoding='utf-8').fillna("")
    return pd.DataFrame()

df = load_db()

# 5. MAIN INTERFACE
st.title("OMT Knowledge Base")

# Search Logic (Permanent table removed from home screen)
query = st.text_input("Search Procedures, Alerts, or Collectors", placeholder="Search by keyword (e.g., 'Alpha', 'VAT', 'Alexis')...")

if query:
    mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
    results = df[mask]
    
    if not results.empty:
        st.success(f"Found {len(results)} matching entries:")
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="result-card">
                <span style="color:#005a9c; font-weight:bold; font-size:0.8rem;">{row['System']} | {row['Process']}</span>
                <div class="instructions">{row['Instructions']}</div>
                <p style="font-size:0.7rem; color:grey; margin-top:5px;">Rationale: {row['Rationale']} | Source: {row['File_Source']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning(f"No results found for '{query}'.")
else:
    st.info("👋 Welcome. Use the search bar above to find operational procedures or collector assignments.")
