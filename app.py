import streamlit as st
import pandas as pd
import os
import re

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# --- AUTHORIZATION LIST ---
ADMIN_EMAILS = ["yahya.ouarach@arrow.com", "mafernandez@arrow.com"]
USER_EMAILS = ["nassim.bouzaid@arrow.com"]
ALL_AUTHORIZED = ADMIN_EMAILS + USER_EMAILS

# 2. STYLING: HIGH-CONTRAST PROFESSIONAL UI
st.markdown("""
<style>
    /* Global White Theme */
    .stApp { background-color: #ffffff; color: #1f2937; }
    
    /* Input Field Styling */
    .stTextInput input {
        border: 2px solid #e5e7eb !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    
    /* Button Visibility Fix */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #005a9c !important;
        border: 2px solid #005a9c !important;
        font-weight: bold !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #005a9c !important;
        color: #ffffff !important;
    }

    /* Professional Instruction Text */
    .step-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: #374151;
    }
    
    .admin-badge {
        background-color: #be185d; color: white; padding: 2px 10px;
        border-radius: 12px; font-size: 0.7rem; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to format instructions into a clean list
def format_instructions(text):
    # Splits by numbers like "1.", "2." or by newlines
    steps = re.split(r'\d+\.', text)
    if len(steps) > 1:
        formatted = ""
        for i, step in enumerate(steps[1:], 1):
            if step.strip():
                formatted += f"**Step {i}:** {step.strip()}\n\n"
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

# 5. SIDEBAR
with st.sidebar:
    st.title("🏹 Arledge")
    role = "ADMIN" if st.session_state.is_admin else "USER"
    st.markdown(f"**{st.session_state.user}** <span class='admin-badge'>{role}</span>", unsafe_allow_html=True)
    
    st.divider()
    page = st.radio("Navigation", ["Knowledge Base", "Admin Dashboard"] if st.session_state.is_admin else ["Knowledge Base"])
    
    st.divider()
    st.markdown("### ⚡ Quick Access")
    st.markdown("• [☁️ Oracle Unity](https://acerpebs.arrow.com/OA_HTML/RF.jsp?function_id=16524)")
    st.markdown("• [🚩 Salesforce](https://arrowcrm.lightning.force.com/)")
    st.markdown("• [💻 SWB Dashboard](https://acswb.arrow.com/Swb/)")
    
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# 6. KNOWLEDGE BASE (Organized Click-to-Drop Style)
if page == "Knowledge Base":
    st.title("Knowledge Base")
    query = st.text_input("🔍 Search for a process, rule, or collector...", placeholder="Type keywords here...")

    if query:
        keywords = query.lower().split()
        mask = df.apply(lambda row: all(k in str(row).lower() for k in keywords), axis=1)
        results = df[mask]
        
        if not results.empty:
            st.write(f"Showing {len(results)} results:")
            for _, row in results.iterrows():
                # CLICK-
