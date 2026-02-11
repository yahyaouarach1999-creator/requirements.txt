import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# Clean Professional White Styling
st.markdown("""
<style>
    /* Main Background - Clean White */
    .stApp { 
        background-color: #ffffff !important; 
        color: #000000 !important; 
    }
    
    /* Login & Search Inputs - High Contrast */
    input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #005a9c !important;
    }

    /* Result Cards - Soft Grey Border */
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
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Force all text elements to be visible in black */
    label, p, span, h1, h2, h3 { color: #000000 !important; }
    
    /* Success/Error messages visibility */
    .stAlert { color: #000000 !important; }
</style>
""", unsafe_allow_html=True)

# 2. LOGIN GATE (Arrow Email Mandatory)
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🏹 Arledge")
    st.subheader("Arrow Knowledge Center")
    st.write("Authorized Access Only")
    user_email = st.text_input("Enter Arrow Email", placeholder="user@arrow.com")
    if st.button("Sign In"):
        if user_email.lower().endswith("@arrow.com"):
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Access denied. Please use your @arrow.com email.")
    st.stop()

# 3. LOAD DATA
DB_FILE = "master_ops_database.csv"
@st.cache_data
def load_db():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE).fillna("")
    return pd.DataFrame()

df = load_db()

# 4. SEARCH INTERFACE
st.title("Arledge")
query = st.text_input("Search Procedures & Contacts", placeholder="e.g. Reno, Hong Kong, Delink, Collector...")

if query:
    # Search all columns
    results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    if not results.empty:
        st.write(f"Found {len(results)} matches:")
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="result-card">
                <span style="color:#005a9c; font-weight:bold; font-size: 0.8rem; text-transform:uppercase;">{row['System']}</span>
                <h2 style="margin-top:5px; margin-bottom:15px;">{row['Process']}</h2>
                <div class="instructions"><b>PROCEDURE:</b><br>{row['Instructions']}</div>
                <p style="margin-top:10px; font-size:0.9rem;"><i>Rationale: {row['Rationale']}</i></p>
                <small style="color:#666;">Ref: {row['File_Source']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error(f"No results found for '{query}'.")
else:
    st.info("The database is ready. Enter a keyword above to find the exact OMT process.")
