import streamlit as st
import pandas as pd
import os
import re

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# --- AUTHORIZATION LIST ---
# Consolidated list to ensure no overwrites
ADMIN_EMAILS = ["yahya.ouarach@arrow.com", "mafernandez@arrow.com"]
USER_EMAILS = ["nassim.bouzaid@arrow.com"]
ALL_AUTHORIZED = ADMIN_EMAILS + USER_EMAILS

# 2. STYLING: HIGH-CONTRAST PROFESSIONAL UI
st.markdown("""
<style>
    .stApp { background-color: #ffffff; color: #1f2937; }
    
    /* Search Bar Styling */
    .stTextInput input {
        border: 2px solid #005a9c !important;
        border-radius: 8px !important;
    }
    
    /* Professional Button UI (Fixes black button issue) */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #005a9c !important;
        border: 2px solid #005a9c !important;
        font-weight: bold !important;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #005a9c !important;
        color: #ffffff !important;
    }

    /* Expander/Accordion Styling */
    .st-expander {
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        background-color: #fcfcfc !important;
    }

    .admin-badge {
        background-color: #be185d; color: white; padding: 2px 10px;
        border-radius: 12px; font-size: 0.7rem; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Helper function for professional list formatting
def format_professional_steps(text):
    # Regex to handle various numbering styles (1., 2., Step 1:)
    steps = re.split(r'(?:\d+\.|\bStep\s*\d+[:.])', text)
    if len(steps) > 1:
        formatted = ""
        count = 1
        for s in steps:
            clean_s = s.strip()
            if clean_s:
                formatted += f"**{count}.** {clean_s}\n\n"
                count += 1
        return formatted
    return text

if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.user = ""
    st.session_state.is_admin = False

# 3. LOGIN GATE
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

# 4. DATA LOADER
@st.cache_data
def load_db():
    file_path = "master_ops_database.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path, engine='python').fillna("")
    return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "File_Source"])

df = load_db()

# 5. SIDEBAR (Links Restored)
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

# 6. KNOWLEDGE BASE (Organized Click-to-Drop)
if page == "Knowledge Base":
    st.title("Knowledge Base")
    query = st.text_input("🔍 Search for a process or rule...", placeholder="Type keywords like 'Reno' or 'Partial'...")

    if query:
        keywords = query.lower().split()
        mask = df.apply(lambda row: all(k in str(row).lower() for k in keywords), axis=1)
        results = df[mask]
        
        if not results.empty:
            st.write(f"Showing {len(results)} matches:")
            for _, row in results.iterrows():
                # PROFESSIONAL CLICK-TO-DROP STYLE
                with st.expander(f"📘 {row['System']} : {row['Process']}", expanded=False):
                    col_info, col_logic = st.columns([2.5, 1])
                    with col_info:
                        st.markdown("#### 📋 Procedure")
                        st.markdown(format_professional_steps(row['Instructions']))
                    with col_logic:
                        st.markdown("#### 💡 Rationale")
                        st.info(row['Rationale'])
        else:
            st.warning("No matches found.")
    else:
        st.info("👋 Search by keyword to access operational procedures.")

# 7. ADMIN DASHBOARD
elif page == "Admin Dashboard":
    st.title("⚙️ Admin Panel")
    st.subheader("Master Database Editor")
    
    # Allows Yahya and Mafernandez to edit live
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    
    if st.download_button("💾 Save & Download CSV", data=edited_df.to_csv(index=False), file_name="master_ops_database.csv", mime="text/csv"):
        st.success("CSV updated. Replace your local file with this version.")
