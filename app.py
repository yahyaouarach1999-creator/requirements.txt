import streamlit as st
import pandas as pd
import io
import os
from PyPDF2 import PdfReader
import google.generativeai as genai

# 1. PAGE CONFIG
st.set_page_config(page_title="Arledge Manual Command", layout="wide", page_icon="🏹")

# 2. AI CONFIG (For Extraction Only)
API_KEY = "AIzaSyA4xwoKlP0iuUtSOkYvpYrADquexHL7YSE"
genai.configure(api_key=API_KEY)
# Using the most stable 2026 alias for text generation
MODEL_ID = 'gemini-flash-latest' 

# 3. UI STYLE
st.markdown("""
<style>
    .stApp {background: #0f172a; color: #f1f5f9;}
    .sop-card {background: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #f97316; margin-bottom: 20px;}
    .system-tag {background: #f97316; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;}
</style>
""", unsafe_allow_html=True)

# 4. DATA ENGINE (Manual CSV)
def load_data():
    if os.path.exists("sop_manual.csv"):
        return pd.read_csv("sop_manual.csv").fillna("")
    return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale"])

df = load_data()

# 5. HEADER
st.title("🏹 ARLEDGE MANUAL COMMAND")
st.caption("Failsafe Edition: Keyword Search Enabled | No Embedding Dependencies")

# 6. SIDEBAR: PDF EXTRACTION
with st.sidebar:
    st.header("📋 Data Management")
    uploaded_file = st.file_uploader("Upload SOP PDF", type="pdf")
    
    if uploaded_file and st.button("Extract to Manual DB"):
        with st.spinner("AI is reading and formatting..."):
            try:
                reader = PdfReader(uploaded_file)
                text = "".join([p.extract_text() for p in reader.pages])
                
                model = genai.GenerativeModel(MODEL_ID)
                prompt = f"Convert this SOP into CSV. Columns: System, Process, Instructions, Rationale. NO headers. Text: {text[:8000]}"
                
                response = model.generate_content(prompt)
                csv_clean = response.text.replace("```csv", "").replace("```", "").strip()
                
                new_df = pd.read_csv(io.StringIO(csv_clean), names=["System", "Process", "Instructions", "Rationale"], header=None)
                
                # Append and Save
                df = pd.concat([df, new_df], ignore_index=True)
                df.to_csv("sop_manual.csv", index=False)
                st.success("Manual Database Updated!")
                st.rerun()
            except Exception as e:
                st.error(f"Extraction Error: {e}")

# 7. SEARCH LOGIC (Manual Keyword Filter)
query = st.text_input("🔍 Search by Keyword (System or Process name)", placeholder="e.g. 'Logistics', 'Order Entry'")

if query:
    # Filter rows where the query appears in System or Process (Case Insensitive)
    mask = df.apply(lambda row: query.lower() in row['System'].lower() or query.lower() in row['Process'].lower(), axis=1)
    results = df[mask]
    
    if not results.empty:
        st.write(f"Showing {len(results)} results:")
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="sop-card">
                <span class="system-tag">{row['System']}</span>
                <h3>{row['Process']}</h3>
                <hr style="border: 0.5px solid #334155;">
                <p><b>Instructions:</b><br>{row['Instructions']}</p>
                <p style="color: #94a3b8; font-size: 0.9rem;"><i>Rationale: {row['Rationale']}</i></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No matches found in the manual database.")
else:
    # Show everything if no search
    st.info("Enter a keyword above to filter procedures.")
    if not df.empty:
        st.dataframe(df[["System", "Process"]], use_container_width=True)
