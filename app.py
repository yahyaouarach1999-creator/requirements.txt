import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# Professional Clean White Styling
st.markdown("""
<style>
    .stApp { background-color: #ffffff !important; color: #000000 !important; }
    
    /* Search Bar Visibility */
    input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #005a9c !important;
    }

    /* Process Card Styling */
    .result-card { 
        border: 1px solid #e1e4e8; 
        padding: 24px; 
        border-radius: 10px; 
        background-color: #fcfcfc; 
        margin-bottom: 25px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Instruction Box - Professional Blue-Left Border */
    .instructions { 
        background-color: #f1f3f4; 
        padding: 18px; 
        border-left: 6px solid #005a9c; 
        white-space: pre-wrap; 
        color: #202124 !important; 
    }

    /* Force visibility of all labels */
    label, p, span, h1, h2, h3 { color: #000000 !important; }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa !important;
        border-right: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# 2. MANDATORY ARROW EMAIL LOGIN
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🏹 Arledge")
    st.subheader("Arrow Knowledge Center")
    st.info("Authorized Access Required. Please sign in with your @arrow.com email.")
    user_email = st.text_input("Arrow Email Address", placeholder="user@arrow.com")
    if st.button("Enter Arledge"):
        if user_email.lower().endswith("@arrow.com"):
            st.session_state.auth = True
            st.session_state.user = user_email
            st.rerun()
        else:
            st.error("Invalid Domain. Use your corporate @arrow.com email.")
    st.stop()

# 3. LOAD FULL DATABASE
DB_FILE = "master_ops_database.csv"
@st.cache_data
def load_db():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE).fillna("")
    return pd.DataFrame()

df = load_db()

# 4. SIDEBAR NAVIGATION & TOOLS
with st.sidebar:
    st.title("🏹 Arledge Tools")
    st.caption(f"Logged in as: {st.session_state.user}")
    st.divider()
    
    st.markdown("### 🛠 Quick Links")
    st.markdown("• [🥷 OMT Ninja](https://omt-ninja.arrow.com)")
    st.markdown("• [📋 ETQ Portal](https://etq.arrow.com)")
    st.markdown("• [💼 Salesforce](https://arrow.my.salesforce.com)")
    st.markdown("• [☁️ Oracle Unity](https://ebs.arrow.com)")
    
    st.divider()
    if st.button("Sign Out"):
        st.session_state.auth = False
        st.rerun()

# 5. SEARCH INTERFACE
st.title("Search Procedures")
query = st.text_input("", placeholder="Search 100+ OMT processes, collectors, or warehouse codes...")

if query:
    results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    if not results.empty:
        st.write(f"Showing {len(results)} matches:")
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="result-card">
                <span style="color:#005a9c; font-weight:bold; text-transform:uppercase; font-size:0.75rem;">{row['System']}</span>
                <h2 style="margin-top:5px; margin-bottom:12px;">{row['Process']}</h2>
                <div class="instructions"><b>PROCEDURE:</b><br>{row['Instructions']}</div>
                <p style="margin-top:10px; font-size:0.85rem; color:#444;"><b>Rationale:</b> {row['Rationale']}</p>
                <small style="color:#888;">File: {row['File_Source']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error(f"No results found for '{query}'.")
else:
    st.info("Type a keyword above (e.g., 'Waldom', 'Venlo', 'CoC', 'Price') to see the steps.")
