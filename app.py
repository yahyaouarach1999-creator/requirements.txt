import streamlit as st
import pandas as pd
import google.generativeai as genai
from PyPDF2 import PdfReader
import io
import urllib.parse
import re

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# Fetch API Key from Streamlit Secrets (for GitHub Safety)
try:
    API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.warning("Admin Note: API Key not found in Secrets. Smart Upload will be disabled.")
    model = None

# --- 2. HELPER FUNCTIONS ---
def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "".join([page.extract_text() for page in reader.pages])

@st.cache_data
def load_data():
    try:
        return pd.read_csv("sop_data.csv").fillna("")
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale"])

# --- 3. AUTHENTICATION ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.title("🏹 Arledge Operations Portal")
    user_email = st.text_input("Official Email (@arrow.com):")
    if st.button("Access Portal"):
        if "@arrow.com" in user_email.lower():
            st.session_state['auth'] = True
            st.rerun()
        else:
            st.error("Access Restricted.")
    st.stop()

# --- 4. MAIN INTERFACE ---
df = load_data()
st.markdown("### 🏹 ARLEDGE OPERATIONS COMMAND")

# Admin Sidebar
st.sidebar.title("⚙️ Admin Tools")
if st.sidebar.checkbox("🚀 Smart AI Upload"):
    if model:
        new_pdf = st.sidebar.file_uploader("Upload SOP PDF", type="pdf")
        if new_pdf and st.sidebar.button("✨ Extract & Append"):
            with st.spinner("AI is reading and formatting..."):
                raw_text = extract_pdf_text(new_pdf)
                prompt = f"Format this text as CSV: System, Process, Instructions, Rationale. Text: {raw_text[:10000]}"
                response = model.generate_content(prompt)
                
                new_rows = pd.read_csv(io.StringIO(response.text), names=["System", "Process", "Instructions", "Rationale"])
                df = pd.concat([df, new_rows], ignore_index=True)
                df.to_csv("sop_data.csv", index=False)
                st.cache_data.clear()
                st.sidebar.success("Successfully added!")
                st.rerun()
    else:
        st.sidebar.error("Set GEMINI_KEY in Secrets to use this.")

# --- 5. SEARCH ENGINE ---
query = st.text_input("🔍 Search Procedures (e.g., 'Delink', 'Dropship', 'V72')")
if query:
    results = df[df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)]
    for _, row in results.iterrows():
        with st.expander(f"📌 {row['System']} | {row['Process']}"):
            st.info(f"**Rationale:** {row['Rationale']}")
            st.markdown(f"**Instructions:**\n{row['Instructions']}")
