import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# --- STRICT SECURITY WHITELIST ---
# Updated: Removed Hanane, kept Yahya and Mafernandez as authorized
AUTHORIZED_USERS = [
    "yahya.ouarach@arrow.com",
    "mafernandez@arrow.com"
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
        border-left: 5px solid #005a9c; white-space: pre-wrap; 
        color: #202124 !important; font-family: monospace;
    }
    [data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 1px solid #dee2e6; }
    label, p, span, h1, h2, h3 { color: #000000 !important; }
    .source-tag { font-size: 0.7rem; color: #6c757d; font-style: italic; }
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
    st.markdown(f"Contact Admin: [yahya.ouarach@arrow.com](mailto:yahya.ouarach@arrow.com)")
    
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()

# 4. DATABASE LOADING
@st.cache_data
def load_db():
    file_path = "master_ops_database.csv"
    if os.path.exists(file_path):
        # We use 'python' engine to handle complex multi-line CSVs accurately
        return pd.read_csv(file_path, encoding='utf-8', engine='python').fillna("")
    return pd.DataFrame()

df = load_db()

# 5. MAIN INTERFACE
st.title("OMT Knowledge Base")

# Search Logic
query = st.text_input("Search Procedures, Alerts, or Collectors", placeholder="Search by keyword (e.g., 'Partial', 'Rejection', 'RMA', 'Daniel')...")

if query:
    # Improved search: checks every single cell in the CSV for the keyword
    mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
    results = df[mask]
    
    if not results.empty:
        st.success(f"Found {len(results)} matching entries:")
        for _, row in results.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="result-card">
                    <span style="color:#005a9c; font-weight:bold; font-size:0.9rem;">{row['System']} ▸ {row['Process']}</span>
                    <div class="instructions">{row['Instructions']}</div>
                    <p style="margin-top:10px; font-size:0.85rem;"><strong>Rationale:</strong> {row['Rationale']}</p>
                    <span class="source-tag">Source: {row['File_Source']}</span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning(f"No results found for '{query}'.")
else:
    # Landing page message (Collector info is hidden as requested)
    st.info("👋 Welcome. Use the search bar above to access OMT procedures, email templates, and collector assignments.")
