import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# --- STRICT SECURITY ---
# Replace with your actual Arrow email
AUTHORIZED_USER = "your_actual_email@arrow.com" 

# Styling: Clean White & High Contrast
st.markdown("""
<style>
    .stApp { background-color: #ffffff !important; color: #000000 !important; }
    input { border: 2px solid #005a9c !important; color: #000000 !important; }
    .result-card { 
        border: 1px solid #e1e4e8; padding: 20px; border-radius: 10px; 
        background-color: #fcfcfc; margin-bottom: 20px;
    }
    .instructions { 
        background-color: #f1f3f4; padding: 15px; 
        border-left: 5px solid #005a9c; white-space: pre-wrap; color: #202124 !important; 
    }
    label, p, span, h1, h2, h3 { color: #000000 !important; }
</style>
""", unsafe_allow_html=True)

if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🏹 Arledge")
    st.subheader("Secure Access Required")
    email_input = st.text_input("Enter Arrow Email Address", placeholder="e.g. jdoe@arrow.com").lower().strip()
    
    if st.button("Enter Arledge"):
        if email_input == AUTHORIZED_USER:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Access Denied: You are not authorized to view this system.")
    st.stop()

# 2. LOAD UPDATED DATABASE
@st.cache_data
def load_db():
    if os.path.exists("master_ops_database.csv"):
        return pd.read_csv("master_ops_database.csv").fillna("")
    return pd.DataFrame()

df = load_db()

# 3. SEARCH & DISPLAY
st.title("Knowledge Base Search")
query = st.text_input("", placeholder="Search collectors, procedures, or credentials...")

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
