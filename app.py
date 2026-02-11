import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# Custom CSS to eliminate "White Spots" and force Dark Mode
st.markdown("""
<style>
    /* Force entire background to deep black */
    .stApp { 
        background-color: #000000 !important; 
        color: #ffffff !important; 
    }
    
    /* Login Container - No shadows, clean borders */
    .login-container { 
        max-width: 450px; 
        margin: 100px auto; 
        padding: 40px; 
        border: 1px solid #333333; 
        background-color: #000000; 
        text-align: center;
        border-radius: 8px;
    }

    /* Search Results Cards */
    .result-card { 
        border: 1px solid #333333; 
        padding: 24px; 
        border-radius: 10px; 
        background-color: #0a0a0a; 
        margin-bottom: 25px; 
    }
    
    /* Instruction Box - Dark Grey with Blue Accent */
    .instructions { 
        background-color: #1a1a1a; 
        padding: 18px; 
        border-left: 6px solid #005a9c; 
        white-space: pre-wrap; 
        color: #ffffff; 
        font-family: 'Courier New', monospace;
    }

    /* Fix for input labels appearing invisible */
    label, p, span { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# 2. LOGIN GATE
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.title("🏹 Arledge")
    st.write("Arrow Knowledge Center Access")
    user_email = st.text_input("Arrow Email", placeholder="user@arrow.com")
    if st.button("Enter System"):
        if user_email.lower().endswith("@arrow.com"):
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Access restricted to @arrow.com users.")
    st.markdown('</div>', unsafe_allow_html=True)
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
query = st.text_input("", placeholder="Search 100+ Procedures & Contacts...")

if query:
    results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="result-card">
                <b style="color:#005a9c; font-size: 0.8rem;">{row['System']}</b>
                <h2 style="margin-top:0;">{row['Process']}</h2>
                <div class="instructions">{row['Instructions']}</div>
                <p style="margin-top:10px; font-size:0.8rem; color:#888;">{row['Rationale']}</p>
            </div>
            """, unsafe_allow_html=True)
