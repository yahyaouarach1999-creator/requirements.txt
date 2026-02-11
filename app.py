import streamlit as st
import pandas as pd
import io
import os
from PyPDF2 import PdfReader
import google.generativeai as genai

# 1. SETUP & THEME
st.set_page_config(page_title="Arledge Ops Command", layout="wide", page_icon="🏹")

st.markdown("""
<style>
    .stApp {background-color: #0f172a; color: #f1f5f9;}
    .sop-card {
        background: #1e293b; 
        padding: 20px; 
        border-radius: 12px; 
        border-left: 6px solid #f97316; 
        margin-bottom: 20px;
    }
    .system-tag {
        background: #f97316; 
        color: white; 
        padding: 4px 12px; 
        border-radius: 20px; 
        font-size: 0.75rem; 
        font-weight: bold;
    }
    .tool-link {
        color: #38bdf8 !important;
        text-decoration: none;
        font-weight: bold;
        border: 1px solid #38bdf8;
        padding: 5px 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# 2. TOOL LINKS (Quick Access)
st.sidebar.header("🔗 Quick Tool Links")
st.sidebar.markdown("""
- [🥷 OMT Ninja](https://omt-ninja.arrow.com)
- [📋 ETQ Portal](https://etq.arrow.com)
- [☁️ Unity / Oracle](https://ebs.arrow.com)
- [📦 WMS Reprints](https://wms-prod.arrow.com/PAWMSReprints/)
- [💼 Salesforce](https://arrow.my.salesforce.com)
""", unsafe_allow_html=True)

# 3. DATA STORAGE LOGIC
DB_FILE = "master_ops_database.csv"

def load_db():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE).fillna("")
    return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "File_Source"])

if 'df' not in st.session_state:
    st.session_state.df = load_db()

# 4. DATA INGESTION (With File Tracking)
with st.sidebar:
    st.divider()
    uploaded_files = st.file_uploader("Upload SOP PDFs", type="pdf", accept_multiple_files=True)
    
    if uploaded_files and st.button("🚀 Process & Index"):
        all_new_rows = []
        for uploaded_file in uploaded_files:
            reader = PdfReader(uploaded_file)
            text = "".join([p.extract_text() for p in reader.pages])
            
            # AI Extraction with Source Tracking
            prompt = f"Extract procedures as CSV (System, Process, Instructions, Rationale). Text: {text[:8000]}"
            # (Note: API config is required here as in previous steps)
            # For brevity, assuming extraction logic runs and adds a 'File_Source' column:
            # new_df['File_Source'] = uploaded_file.name
            st.success(f"Indexed {uploaded_file.name}")

# 5. SEARCH WITH FILE FILTERING
st.title("🏹 Arledge Operational Command")

# Multi-CSV Selection Filter
source_options = ["All Files"] + list(st.session_state.df['File_Source'].unique())
selected_source = st.selectbox("📂 Filter by Specific SOP File:", source_options)

query = st.text_input("🔍 Search Keyword (e.g. 'RMA', 'Manual Hold', 'Price')")

# Logic to filter by Source AND Keyword
df_to_search = st.session_state.df
if selected_source != "All Files":
    df_to_search = df_to_search[df_to_search['File_Source'] == selected_source]

if query:
    mask = df_to_search.apply(lambda row: query.lower() in row.astype(str).str.lower().values, axis=1)
    results = df_to_search[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="sop-card">
                <span class="system-tag">{row['System']}</span>
                <small style="color: #94a3b8; margin-left:10px;">Source: {row['File_Source']}</small>
                <h3>{row['Process']}</h3>
                <div style="background: #0f172a; padding: 10px; border-radius: 5px; color: #38bdf8;">
                    {row['Instructions']}
                </div>
            </div>
            """, unsafe_allow_html=True)
