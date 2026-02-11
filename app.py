import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# High-Contrast CSS: Fixes invisible text and "white spots"
st.markdown("""
<style>
    /* Main Background - Deep Charcoal for better text rendering than pure black */
    .stApp { 
        background-color: #0e1117 !important; 
        color: #ffffff !important; 
    }
    
    /* Login & Search Inputs - Forced Visibility */
    input {
        background-color: #1a1c23 !important;
        color: #ffffff !important;
        border: 1px solid #3d44db !important;
    }

    /* Result Cards */
    .result-card { 
        border: 1px solid #30363d; 
        padding: 24px; 
        border-radius: 10px; 
        background-color: #161b22; 
        margin-bottom: 25px; 
    }
    
    /* Instruction Box - Bright text on dark blue background */
    .instructions { 
        background-color: #0d1117; 
        padding: 18px; 
        border-left: 6px solid #58a6ff; 
        white-space: pre-wrap; 
        color: #c9d1d9 !important; 
        font-family: sans-serif;
    }

    /* Sidebar Labels */
    [data-testid="stSidebar"] {
        background-color: #0d1117 !important;
    }
    
    /* Force all text elements to be white */
    label, p, span, h1, h2, h3 { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# 2. LOGIN GATE
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🏹 Arledge")
    st.write("Arrow Knowledge Center Access")
    user_email = st.text_input("Enter Arrow Email to reveal database", placeholder="user@arrow.com")
    if st.button("Enter System"):
        if user_email.lower().endswith("@arrow.com"):
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Access restricted to @arrow.com users.")
    st.stop()

# 3. LOAD DATA
DB_FILE = "master_ops_database.csv"
@st.cache_data
def load_db():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE).fillna("")
    return pd.DataFrame()

df = load_db()

# 4. SEARCH
st.title("Arledge")
query = st.text_input("Search Procedures", placeholder="Type a keyword (e.g. Reno, PayPal, Delink)...")

if query:
    results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="result-card">
                <b style="color:#58a6ff; font-size: 0.8rem;">{row['System']}</b>
                <h2 style="margin-top:0; color:#ffffff;">{row['Process']}</h2>
                <div class="instructions">{row['Instructions']}</div>
                <p style="margin-top:10px; font-size:0.8rem; color:#8b949e;">{row['Rationale']}</p>
            </div>
            """, unsafe_allow_html=True)
