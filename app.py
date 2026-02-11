import streamlit as st
import pandas as pd
import io
import os
from PyPDF2 import PdfReader
import google.generativeai as genai

# --- 1. PRO PAGE CONFIG ---
st.set_page_config(page_title="OMT Command Center", layout="wide", page_icon="🏹")

# Professional Corporate Styling (Light Mode)
st.markdown("""
<style>
    .main { background-color: #ffffff; }
    .stTextInput { margin-top: -20px; }
    .sop-card {
        border: 1px solid #e1e4e8;
        padding: 20px;
        border-radius: 8px;
        background-color: #fcfcfc;
        margin-bottom: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .step-box {
        background-color: #f1f3f4;
        border-left: 5px solid #1a73e8;
        padding: 15px;
        margin: 10px 0;
        font-family: 'Segoe UI', sans-serif;
        white-space: pre-wrap;
    }
    .system-label { color: #d93025; font-weight: bold; text-transform: uppercase; font-size: 0.8rem; }
    .source-label { color: #70757a; font-size: 0.75rem; float: right; }
</style>
""", unsafe_allow_html=True)

# --- 2. CLOUD DATABASE LOGIC ---
DB_FILE = "master_ops_database.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE).fillna("")
    return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "File_Source"])

if 'df' not in st.session_state:
    st.session_state.df = load_data()

# --- 3. SIDEBAR (Tools & Upload) ---
with st.sidebar:
    st.title("🔗 Quick Links")
    st.markdown("""
    [🥷 OMT Ninja](https://omt-ninja.arrow.com) | [📋 ETQ Portal](https://etq.arrow.com)
    [💼 Salesforce](https://arrow.my.salesforce.com) | [☁️ Oracle Unity](https://ebs.arrow.com)
    """)
    st.divider()
    st.subheader("📥 Data Import")
    uploaded_files = st.file_uploader("Upload SOP PDFs", type="pdf", accept_multiple_files=True)
    if uploaded_files and st.button("Index Files"):
        # This is where your AI extraction logic lives
        st.info("Extracting data... Please wait.")
        st.rerun()
    if st.button("🗑️ Clear All Data"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.session_state.df = pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "File_Source"])
        st.rerun()

# --- 4. SEARCH INTERFACE ---
st.title("🏹 Arledge Ops Search")
st.write("Enter a keyword to find the exact step-by-step procedure.")

# Search Bar
query = st.text_input("", placeholder="Search e.g. 'Delink', 'RMA', 'Oracle Error'...")

# --- 5. DYNAMIC RESULTS (Only show if typing) ---
if query:
    df = st.session_state.df
    # Search logic across all columns
    mask = df.apply(lambda row: query.lower() in row.astype(str).str.lower().values, axis=1)
    results = df[mask]
    
    if not results.empty:
        st.success(f"Found {len(results)} relevant procedures:")
        for _, row in results.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="sop-card">
                    <span class="source-label">File: {row['File_Source']}</span>
                    <span class="system-label">{row['System']}</span>
                    <h2 style="margin: 5px 0;">{row['Process']}</h2>
                    <div class="step-box">
                        <strong>STEPS:</strong><br>{row['Instructions']}
                    </div>
                    <p style="color: #5f6368; font-size: 0.9rem;"><strong>Why we do this:</strong> {row['Rationale']}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.error("No matches found. Try a different keyword.")
else:
    # This is the "Professional Home Page" when not searching
    st.info("The system is ready. Use the search bar above to begin.")
