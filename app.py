import streamlit as st
import pandas as pd
import io
import os
from PyPDF2 import PdfReader
import google.generativeai as genai

# 1. PROFESSIONAL PAGE SETUP
st.set_page_config(page_title="Arledge OMT Command Center", layout="wide", page_icon="📊")

# Professional CSS (Light Mode, Clean Borders, Corporate Fonts)
st.markdown("""
<style>
    .reportview-container { background: #f0f2f6; }
    .main { background: #ffffff; padding: 20px; border-radius: 10px; }
    .tool-card {
        border: 1px solid #e1e4e8;
        padding: 15px;
        border-radius: 8px;
        background-color: #f8f9fa;
        margin-bottom: 15px;
    }
    .instruction-box {
        background-color: #f1f3f4;
        border-left: 5px solid #2c3e50;
        padding: 12px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #202124;
    }
    .file-tag {
        color: #5f6368;
        font-size: 0.8rem;
        font-style: italic;
    }
    a { text-decoration: none; color: #1a73e8; font-weight: 500; }
    a:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)

# 2. API CONFIG
API_KEY = "AIzaSyA4xwoKlP0iuUtSOkYvpYrADquexHL7YSE"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

# 3. DATA PERSISTENCE
DB_FILE = "master_ops_database.csv"

def load_db():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE).fillna("")
    return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "File_Source"])

if 'df' not in st.session_state:
    st.session_state.df = load_db()

# 4. SIDEBAR: NAVIGATION & TOOLS
with st.sidebar:
    st.title("🏹 OMT Tools")
    st.subheader("Internal Portals")
    st.markdown("""
    * 🔗 [OMT Ninja](https://omt-ninja.arrow.com)
    * 🔗 [ETQ Portal](https://etq.arrow.com)
    * 🔗 [Oracle Unity](https://ebs.arrow.com)
    * 🔗 [Salesforce CRM](https://arrow.my.salesforce.com)
    * 🔗 [WMS Reprints](https://wms-prod.arrow.com/PAWMSReprints/)
    """)
    
    st.divider()
    st.subheader("📁 Data Management")
    uploaded_files = st.file_uploader("Upload SOP PDFs", type="pdf", accept_multiple_files=True)
    
    if uploaded_files and st.button("Index Selected Files"):
        with st.spinner("Processing..."):
            all_rows = []
            for uploaded_file in uploaded_files:
                reader = PdfReader(uploaded_file)
                for i in range(0, len(reader.pages), 5):
                    text = "".join([p.extract_text() for p in reader.pages[i:i+5]])
                    prompt = f"Extract procedures as CSV (System, Process, Instructions, Rationale). No headers. Text: {text}"
                    try:
                        response = model.generate_content(prompt)
                        csv_data = response.text.replace("```csv", "").replace("```", "").strip()
                        chunk_df = pd.read_csv(io.StringIO(csv_data), names=["System", "Process", "Instructions", "Rationale"], header=None)
                        chunk_df['File_Source'] = uploaded_file.name
                        all_rows.append(chunk_df)
                    except: continue
            
            if all_rows:
                new_df = pd.concat(all_rows, ignore_index=True)
                st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True).drop_duplicates(subset=['Process'])
                st.session_state.df.to_csv(DB_FILE, index=False)
                st.rerun()

    if st.button("Clear Database"):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.session_state.df = pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "File_Source"])
        st.rerun()

# 5. MAIN INTERFACE
st.title("Operational Procedures Search")

# Search and Filter Logic
col1, col2 = st.columns([2, 1])
with col1:
    query = st.text_input("Search processes, systems, or keywords...", placeholder="e.g. 'Dropship' or 'RMA'")
with col2:
    sources = ["All Files"] + list(st.session_state.df['File_Source'].unique())
    selected_source = st.selectbox("Search within file:", sources)

# Apply Filters
display_df = st.session_state.df
if selected_source != "All Files":
    display_df = display_df[display_df['File_Source'] == selected_source]

if query:
    mask = display_df.apply(lambda row: query.lower() in row.astype(str).str.lower().values, axis=1)
    results = display_df[mask]
    
    if not results.empty:
        st.write(f"Showing {len(results)} results")
        for _, row in results.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="tool-card">
                    <div style="display: flex; justify-content: space-between;">
                        <strong style="color: #d93025;">{row['System']}</strong>
                        <span class="file-tag">📄 {row['File_Source']}</span>
                    </div>
                    <h3 style="margin: 10px 0;">{row['Process']}</h3>
                    <div class="instruction-box">
                        <strong>Standard Procedure:</strong><br>{row['Instructions']}
                    </div>
                    <p style="margin-top: 10px; font-size: 0.9rem; color: #5f6368;">
                        <strong>Rationale:</strong> {row['Rationale']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No matches found.")
else:
    if not display_df.empty:
        st.dataframe(display_df[["System", "Process", "File_Source"]], use_container_width=True)
    else:
        st.info("Upload your first SOP file in the sidebar to begin building the command center.")
