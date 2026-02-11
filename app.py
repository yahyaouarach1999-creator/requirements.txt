import streamlit as st
import pandas as pd
import io
import os
from PyPDF2 import PdfReader
import google.generativeai as genai

# 1. SETUP & THEME
st.set_page_config(page_title="Arledge Ops Command", layout="wide", page_icon="🏹")

# Custom CSS for the "Pro" look
st.markdown("""
<style>
    .stApp {background-color: #0f172a; color: #f1f5f9;}
    .sop-card {
        background: #1e293b; 
        padding: 20px; 
        border-radius: 12px; 
        border-left: 6px solid #f97316; 
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .system-tag {
        background: #f97316; 
        color: white; 
        padding: 4px 12px; 
        border-radius: 20px; 
        font-size: 0.75rem; 
        font-weight: bold;
        text-transform: uppercase;
    }
    .instruction-text {
        background: #0f172a;
        padding: 15px;
        border-radius: 8px;
        font-family: 'Courier New', Courier, monospace;
        margin-top: 10px;
        color: #38bdf8;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

# 2. API CONFIG
API_KEY = "AIzaSyA4xwoKlP0iuUtSOkYvpYrADquexHL7YSE"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

# 3. PERMANENT DATA STORAGE
DB_FILE = "master_ops_database.csv"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE).fillna("")
        except:
            return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale"])
    return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale"])

# Load data into session state to keep it persistent during the user session
if 'df' not in st.session_state:
    st.session_state.df = load_db()

# 4. SIDEBAR: DATA INGESTION
with st.sidebar:
    st.header("⚙️ Data Management")
    st.write(f"Database Size: **{len(st.session_state.df)}** Procedures")
    
    uploaded_files = st.file_uploader("Upload SOP PDFs", type="pdf", accept_multiple_files=True)
    
    if uploaded_files and st.button("🚀 Extract & Save Forever"):
        with st.spinner("AI is deep-scanning files..."):
            all_new_rows = []
            for uploaded_file in uploaded_files:
                reader = PdfReader(uploaded_file)
                # Chunks of 5 pages to keep the AI focused
                for i in range(0, len(reader.pages), 5):
                    text = "".join([p.extract_text() for p in reader.pages[i:i+5]])
                    # Refined prompt to ensure valid CSV structure
                    prompt = f"""Extract every operational procedure from the text below. 
                    Format as CSV with exactly 4 columns: System, Process, Instructions, Rationale.
                    Do not include headers. Wrap text in double quotes if it contains commas.
                    Text:
                    {text}"""
                    
                    try:
                        response = model.generate_content(prompt)
                        csv_text = response.text.replace("```csv", "").replace("```", "").strip()
                        # Use quotechar and escapechar to handle messy AI text
                        chunk_df = pd.read_csv(
                            io.StringIO(csv_text), 
                            names=["System", "Process", "Instructions", "Rationale"], 
                            header=None,
                            quotechar='"',
                            skipinitialspace=True
                        )
                        all_new_rows.append(chunk_df)
                    except Exception as e:
                        continue
            
            if all_new_rows:
                new_data = pd.concat(all_new_rows, ignore_index=True)
                # Merge with existing and remove duplicates based on Process name
                combined_df = pd.concat([st.session_state.df, new_data], ignore_index=True)
                st.session_state.df = combined_df.drop_duplicates(subset=['Process'], keep='last')
                st.session_state.df.to_csv(DB_FILE, index=False)
                st.success("Database Updated Successfully!")
                st.rerun()

    if st.button("🗑️ Reset Database"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        st.session_state.df = pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale"])
        st.rerun()

# 5. MAIN INTERFACE: SEARCH

st.title("🏹 Arledge Operational Command")
st.subheader("Manual High-Speed Search Engine")

query = st.text_input("🔍 Search by System, Process name, or Keyword...", placeholder="e.g., 'Oracle', 'Sure Ship', 'Cancellation'")

if query:
    # Manual Filter Logic (searches across all columns)
    df = st.session_state.df
    mask = df.apply(lambda row: query.lower() in row.astype(str).str.lower().values, axis=1)
    results = df[mask]
    
    if not results.empty:
        st.write(f"Found {len(results)} matches:")
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="sop-card">
                <span class="system-tag">{row['System']}</span>
                <h3 style="margin-top:10px; color: #f1f5f9;">{row['Process']}</h3>
                <div class="instruction-text"><b>Step-by-Step Instructions:</b><br>{row['Instructions']}</div>
                <p style="margin-top:15px; color: #94a3b8; font-size: 0.9rem;">
                    <b>Rationale:</b> {row['Rationale']}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning(f"No results found for '{query}'. Try a broader keyword.")
else:
    # Dashboard / Empty State
    df = st.session_state.df
    if not df.empty:
        st.info("Database loaded. Type a keyword above to find a specific procedure.")
        st.write("### Systems Covered")
        systems = df['System'].unique()
        # Responsive grid of buttons for discovered systems
        cols = st.columns(min(len(systems), 4) if len(systems) > 0 else 1)
        for idx, sys in enumerate(systems):
            cols[idx % 4].button(sys, use_container_width=True)
    else:
        st.warning("The database is currently empty. Please upload the SOP PDFs in the sidebar to begin.")
