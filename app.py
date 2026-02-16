import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# --- ACCESS CONTROL LIST ---
ADMIN_EMAILS = ["yahya.ouarach@arrow.com"]
ADMIN_EMAILS = ["mafernandez@arrow.com"]
USER_EMAILS = ["Nassim.Bouzaid@arrow.com"]
ALL_AUTHORIZED = ADMIN_EMAILS + USER_EMAILS

# Styling: High-End Corporate UI
st.markdown("""
<style>
    .stApp { background-color: #ffffff; color: #000000; }
    .result-card { 
        border: 1px solid #e1e4e8; padding: 20px; border-radius: 10px; 
        background-color: #fcfcfc; margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .instructions { 
        background-color: #f1f3f4; padding: 15px; border-left: 5px solid #005a9c; 
        white-space: pre-wrap; color: #202124 !important; font-family: 'Courier New', Courier, monospace;
    }
    .admin-badge {
        background-color: #ff4b4b; color: white; padding: 2px 8px;
        border-radius: 5px; font-size: 0.7rem; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.user = ""
    st.session_state.is_admin = False

# 2. LOGIN GATE
if not st.session_state.auth:
    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.title("🏹 Arledge Login")
        email_input = st.text_input("Arrow Email Address").lower().strip()
        if st.button("Sign In"):
            if email_input in ALL_AUTHORIZED:
                st.session_state.auth = True
                st.session_state.user = email_input
                st.session_state.is_admin = email_input in ADMIN_EMAILS
                st.rerun()
            else:
                st.error("Unauthorized email address.")
    st.stop()

# 3. SIDEBAR: NAVIGATION & TOOLS
with st.sidebar:
    st.title("🏹 Arledge")
    role_label = "ADMIN" if st.session_state.is_admin else "USER"
    st.markdown(f"**Logged in as:** {st.session_state.user} <span class='admin-badge'>{role_label}</span>", unsafe_allow_html=True)
    
    st.divider()
    page = st.radio("Go To", ["Knowledge Base", "Admin Dashboard"] if st.session_state.is_admin else ["Knowledge Base"])
    
    st.divider()
    st.markdown("### ⚡ Quick Links")
    st.markdown("• [☁️ Oracle Unity](https://acerpebs.arrow.com/OA_HTML/RF.jsp?function_id=16524&resp_id=57098&resp_appl_id=20008&security_group_id=0&lang_code=US&oas=k2oTjdeInl3Bik8l6rTqgA..)")
    st.markdown("• [🚩 Salesforce](https://arrowcrm.lightning.force.com/lightning/o/Case/list?filterName=My_Open_and_Flagged_With_Reminder)")
    st.markdown("• [💻 SWB Dashboard](https://acswb.arrow.com/Swb/)")
    
    st.divider()
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()

# 4. DATA LOADER
@st.cache_data
def load_db():
    file_path = "master_ops_database.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path, engine='python').fillna("")
    return pd.DataFrame()

df = load_db()

# 5. PAGE LOGIC
if page == "Knowledge Base":
    st.title("OMT Knowledge Base")
    query = st.text_input("Search anything (SOPs, Templates, Collectors, Systems)...")

    if query:
        mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
        results = df[mask]
        
        if not results.empty:
            st.success(f"Found {len(results)} results")
            for _, row in results.iterrows():
                st.markdown(f"""
                <div class="result-card">
                    <h4 style="color:#005a9c; margin-bottom:5px;">{row['System']} ▸ {row['Process']}</h4>
                    <div class="instructions">{row['Instructions']}</div>
                    <p style="margin-top:10px; font-size:0.9rem;"><b>Rationale:</b> {row['Rationale']}</p>
                    <small style="color:gray;">Source: {row['File_Source']}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No matches found.")
    else:
        st.info("💡 Tip: Search for 'Collector' to see alpha assignments or 'Email' for canned templates.")

elif page == "Admin Dashboard":
    st.title("⚙️ Admin Control Panel")
    st.subheader("Master Database Management")
    
    # Show stats
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Procedures", len(df))
    col2.metric("Authorized Users", len(ALL_AUTHORIZED))
    col3.metric("System Engine", "Python v3.x")
    
    st.divider()
    st.markdown("### Raw Data View")
    st.dataframe(df, use_container_width=True)
    
    st.download_button(
        "Download Database for Backup",
        data=df.to_csv(index=False),
        file_name="backup_ops_db.csv",
        mime="text/csv"
    )
