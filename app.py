import streamlit as st
import pandas as pd
import re
import urllib.parse

# --- 1. CONFIG & AUTHENTICATION ---
st.set_page_config(page_title="Arrow Ops Masterclass", layout="wide")

# Simple Login Logic
if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.role = None

def check_login():
    st.title("🏹 Arrow Ops Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if pwd == "Arrow2026": # USER PASSWORD
            st.session_state.auth = True
            st.session_state.role = "User"
            st.rerun()
        elif pwd == "ArrowAdmin": # ADMIN PASSWORD
            st.session_state.auth = True
            st.session_state.role = "Admin"
            st.rerun()
        else:
            st.error("Invalid Credentials")

if not st.session_state.auth:
    check_login()
    st.stop()

# --- 2. DATA ENGINE ---
@st.cache_data(ttl=1)
def load_data():
    return pd.read_csv("sop_data.csv", encoding='utf-8-sig').fillna("")

df = load_data()

# --- 3. THE "ADMIN" EDITOR PAGE ---
if st.session_state.role == "Admin":
    with st.sidebar:
        st.divider()
        if st.checkbox("🛠️ Open Admin Editor"):
            st.session_state.view = 'admin'

if st.session_state.get('view') == 'admin':
    st.title("📝 Master Data Editor")
    st.warning("You are editing the LIVE database. Changes will reflect for all users.")
    
    # Editable Table
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 Save Changes to CSV"):
        edited_df.to_csv("sop_data.csv", index=False)
        st.success("Database Updated Successfully!")
        st.cache_data.clear()
    
    if st.button("🔙 Back to Search"):
        st.session_state.view = 'home'
        st.rerun()
    st.stop()

# --- 4. STANDARD SEARCH PORTAL (REST OF CODE) ---
# [Insert the Page 1 Search and Page 2 Detail logic from previous step here]
