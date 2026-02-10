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
    }
</style>
""", unsafe_allow_html=True)

# 2. API CONFIG (Extraction Only)
API_KEY = "AIzaSyA4xwoKlP0iuUtSOkYvpYrADquexHL7YSE"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

# 3. PERMANENT DATA STORAGE
DB_FILE = "master_ops_database.csv"

def load_db():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE).fillna("")
    return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale"])

df = load_db()

# 4. SIDEBAR: DATA INGESTION
with st.sidebar:
    st.header("⚙️ Data Management")
    st.write("Current Database Size:", len(df), "Procedures")
    
    uploaded_files = st.file_uploader("Upload SOP PDFs", type="pdf", accept_multiple_files=True)
    
    if uploaded_files and st.button("🚀 Extract & Save Forever"):
        with st.spinner("AI is deep-scanning files..."):
            all_new_rows = []
            for uploaded_file in uploaded_files:
                reader = PdfReader(uploaded_file)
                # Process in 5-page chunks for maximum accuracy
                for i in range(0, len(reader.pages), 5):
                    text = "".join([p.extract_text() for p in reader.pages[i:i+5]])
                    prompt = f"Extract EVERY procedure as CSV (System, Process, Instructions, Rationale). No headers. Text:\n{text}"
                    try:
                        response = model.generate_content(prompt)
                        csv_text = response.text.replace("```csv", "").replace("```", "").strip()
                        chunk_df = pd.read_csv(io.StringIO(csv_text), names=["System", "Process", "Instructions", "Rationale"], header=None)
                        all_new_rows.append(chunk_df)
                    except:
                        continue
            
            if all_new_rows:
                new_data = pd.concat(all_new_rows, ignore_index=True)
                # Combine with existing, remove duplicates
                df = pd.concat([df, new_data], ignore_index=True).drop_duplicates(subset=['Process'])
                df.to_csv(DB_FILE, index=False)
                st.success("Database Updated!")
                st.rerun()

    if st.button("🗑️ Reset Database"):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.rerun()

# 5. MAIN INTERFACE: SEARCH
st.title("🏹 Arledge Operational Command")
st.subheader("Manual High-Speed Search Engine")

query = st.text_input("🔍 Search by System, Process name, or Keyword...", placeholder="e.g., 'Oracle', 'Sure Ship', 'Cancellation'")

if query:
    # Manual Filter Logic (Looks through all columns for the keyword)
    mask = df.apply(lambda row: query.lower() in row.astype(str).str.lower().values, axis=1)
    results = df[mask]
    
    if not results.empty:
        st.write(f"Found {len(results)} matches:")
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="sop-card">
                <span class="system-tag">{row['System']}</span>
                <h3 style="margin-top:10px;">{row['Process']}</h3>
                <div class="instruction-text"><b>Step-by-Step:</b><br>{row['Instructions']}</div>
                <p style="margin-top:15px; color: #94a3b8;"><b>Rationale:</b> {row['Rationale']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning(f"No results found for '{query}'. Try a broader keyword.")
else:
    # Dashboard View
    if not df.empty:
        st.info("Database loaded. Type a keyword above to find a specific procedure.")
        # Group by System for a clean overview
        st.write("### Systems Covered")
        systems = df['System'].unique()
        cols = st.columns(len(systems) if len(systems) < 5 else 4)
        for idx, sys in enumerate(systems):
            cols[idx % 4].button(sys, disabled=True)
    else:
        st.warning("The database is currently empty. Please upload the SOP files in the sidebar.")
