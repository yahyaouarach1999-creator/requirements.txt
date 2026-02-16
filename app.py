import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# --- FIXED ACCESS CONTROL ---
# Admin and User lists correctly separated
ADMIN_EMAILS = ["yahya.ouarach@arrow.com", "mafernandez@arrow.com"]
USER_EMAILS = ["nassim.bouzaid@arrow.com"]
ALL_AUTHORIZED = ADMIN_EMAILS + USER_EMAILS

# Styling: High-Contrast Corporate UI (Fixes "Black Button" & "Dark Template" issues)
st.markdown("""
<style>
    /* Main Background */
    .stApp { background-color: #ffffff; color: #000000; }
    
    /* Result Card Styling */
    .result-card { 
        border: 1px solid #d1d5db; padding: 24px; border-radius: 12px; 
        background-color: #ffffff; margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Instructions Styling (Lightened and Professional) */
    .instructions { 
        background-color: #f9fafb; padding: 18px; border-left: 6px solid #005a9c; 
        white-space: pre-wrap; color: #111827 !important; 
        font-family: 'Consolas', monospace; font-size: 1rem;
        border: 1px solid #e5e7eb; border-left: 6px solid #005a9c;
        border-radius: 4px; margin-top: 10px;
    }

    /* FIX: Button Visibility */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #005a9c !important;
        border: 2px solid #005a9c !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
    }
    div.stButton > button:hover {
        background-color: #005a9c !important;
        color: #ffffff !important;
    }

    /* Admin Badge */
    .admin-badge {
        background-color: #e11d48; color: white; padding: 4px 10px;
        border-radius: 20px; font-size: 0.75rem; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.user = ""
    st.session_state.is_admin = False

# 2. LOGIN GATE
if not st.session_state.auth:
    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        st.title("🏹 Arledge Login")
        email_input = st.text_input("Arrow Email Address").lower().strip()
        if st.button("Sign In"):
            if email_input in ALL_AUTHORIZED:
                st.session_state.auth = True
                st.session_state.user = email_input
                st.session_state.is_admin = (email_input in ADMIN_EMAILS)
                st.rerun()
            else:
                st.error(f"Access Denied: {email_input} is not authorized.")
    st.stop()

# 3. DATA LOADER
@st.cache_data
def load_db():
    file_path = "master_ops_database.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path, engine='python').fillna("")
    return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "File_Source"])

df = load_db()

# 4. SIDEBAR (Restored Quick Links)
with st.sidebar:
    st.title("🏹 Arledge")
    role = "ADMIN" if st.session_state.is_admin else "USER"
    st.markdown(f"**{st.session_state.user}** <span class='admin-badge'>{role}</span>", unsafe_allow_html=True)
    
    st.divider()
    page = st.radio("Navigation", ["Knowledge Base", "Admin Dashboard"] if st.session_state.is_admin else ["Knowledge Base"])
    
    st.divider()
    st.markdown("### ⚡ Quick Access Links")
    st.markdown("• [☁️ Oracle Unity](https://acerpebs.arrow.com/OA_HTML/RF.jsp?function_id=16524&resp_id=57098&resp_appl_id=20008&security_group_id=0&lang_code=US&oas=k2oTjdeInl3Bik8l6rTqgA..)")
    st.markdown("• [🚩 Salesforce](https://arrowcrm.lightning.force.com/lightning/o/Case/list?filterName=My_Open_and_Flagged_With_Reminder)")
    st.markdown("• [💻 SWB Dashboard](https://acswb.arrow.com/Swb/)")
    st.markdown("• [📋 ETQ Portal](https://arrow.etq.com/prod/rel/#/app/auth/login)")
    st.markdown("• [🛠 MyConnect IT](https://arrow.service-now.com/myconnect)")
    
    st.divider()
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# 5. PAGE LOGIC
if page == "Knowledge Base":
    st.title("Knowledge Base") # Removed OMT from Title
    query = st.text_input("🔍 Search (e.g. 'Partial', 'Venlo', 'Daniel')...", placeholder="Search for procedures or contacts...")

    if query:
        keywords = query.lower().split()
        mask = df.apply(lambda row: all(k in str(row).lower() for k in keywords), axis=1)
        results = df[mask]
        
        if not results.empty:
            st.success(f"Found {len(results)} matches")
            for _, row in results.iterrows():
                st.markdown(f"""
                <div class="result-card">
                    <div style="color:#005a9c; font-weight:bold; font-size:0.85rem; text-transform:uppercase;">
                        {row['System']}
                    </div>
                    <h3 style="margin-top:5px; margin-bottom:15px;">{row['Process']}</h3>
                    <div class="instructions">{row['Instructions']}</div>
                    <div style="margin-top:15px; font-size:0.9rem; color:#4b5563;">
                        <b>Rationale:</b> {row['Rationale']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No matches found.")
    else:
        st.info("👋 Welcome! Search by keyword above to see procedures and templates.")

# 6. ADMIN DASHBOARD
elif page == "Admin Dashboard":
    st.title("⚙️ Admin Panel")
    
    col1, col2 = st.columns(2)
    col1.metric("Database Entries", len(df))
    col2.metric("Access Health", "All Systems Operational")
    
    st.divider()
    st.subheader("Master Database Editor")
    # Live data editor
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    
    if st.download_button("💾 Save & Download CSV", data=edited_df.to_csv(index=False), file_name="master_ops_database.csv", mime="text/csv"):
        st.success("Download complete. Replace your local CSV file with this version.")
