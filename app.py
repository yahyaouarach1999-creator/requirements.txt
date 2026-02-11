import streamlit as st
import pandas as pd
import io
import os
from PyPDF2 import PdfReader

# --- 1. PRO PAGE CONFIG ---
st.set_page_config(page_title="Arledge OMT Command", layout="wide", page_icon="🏹")

# Professional Light Mode Styling
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .sop-card {
        border: 1px solid #e1e4e8;
        padding: 24px;
        border-radius: 10px;
        background-color: #ffffff;
        margin-bottom: 25px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .step-box {
        background-color: #f1f3f4;
        border-left: 5px solid #1a73e8;
        padding: 15px;
        margin: 15px 0;
        font-family: 'Segoe UI', sans-serif;
        white-space: pre-wrap;
        color: #202124;
        line-height: 1.6;
    }
    .system-label { color: #d93025; font-weight: bold; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 1px; }
    .source-tag { color: #70757a; font-size: 0.75rem; float: right; border: 1px solid #e1e4e8; padding: 2px 8px; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# --- 2. DATABASE LOADING ---
DB_FILE = "master_ops_database.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE).fillna("")
    return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "File_Source"])

if 'df' not in st.session_state:
    st.session_state.df = load_data()

# --- 3. SIDEBAR (Tools & Links) ---
with st.sidebar:
    st.title("🏹 OMT Resources")
    st.markdown("""
    **Core Portals:**
    * 🔗 [OMT Ninja](https://omt-ninja.arrow.com)
    * 🔗 [ETQ Portal](https://etq.arrow.com)
    * 🔗 [Oracle Unity](https://ebs.arrow.com)
    * 🔗 [Salesforce](https://arrow.my.salesforce.com)
    """)
    st.divider()
    if st.button("🗑️ Reset Search Index"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.session_state.df = pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "File_Source"])
        st.rerun()

# --- 4. THE SEARCH INTERFACE ---
st.title("Operational Procedures Search")
query = st.text_input("", placeholder="Type to search (e.g., 'Delink', 'Dropship', 'ETQ')...")

# --- 5. SEARCH RESULTS (Only appears when typing) ---
if query:
    df = st.session_state.df
    mask = df.apply(lambda row: query.lower() in row.astype(str).str.lower().values, axis=1)
    results = df[mask]
    
    if not results.empty:
        st.write(f"Displaying {len(results)} matches:")
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="sop-card">
                <span class="source-tag">{row['File_Source']}</span>
                <span class="system-label">{row['System']}</span>
                <h2 style="margin-top: 5px; color: #1a202c;">{row['Process']}</h2>
                <div class="step-box">
                    <strong>Standard Operating Procedure:</strong><br>{row['Instructions']}
                </div>
                <p style="font-size: 0.9rem; color: #4a5568;"><strong>Business Rationale:</strong> {row['Rationale']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No procedures found for that keyword.")
else:
    # CLEAN HOME PAGE
    st.info("System Ready. Please enter a keyword above to view specific process steps.")
