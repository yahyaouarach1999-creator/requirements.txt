import streamlit as st
import pandas as pd
import google.generativeai as genai
from PyPDF2 import PdfReader
import io
import urllib.parse

# --- 1. SETTINGS & AI CONFIG ---
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# AI Link (Hidden in Secrets)
try:
    API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = None

# PDF Reading Function
def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "".join([page.extract_text() or "" for page in reader.pages])

# Database Loading
@st.cache_data
def load_data():
    try:
        return pd.read_csv("sop_data.csv").fillna("")
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale"])

df = load_data()

# --- 2. THE SIDEBAR (Your Links + Admin) ---
st.sidebar.title("🏹 Arledge Shortcuts")
st.sidebar.link_button("☁️ Open Salesforce", "https://arrow.lightning.force.com/")
st.sidebar.link_button("📊 OMT Dashboard", "https://arrow.lightning.force.com/lightning/o/Report/home")
st.sidebar.divider()

# The Smart Admin Section
if st.sidebar.checkbox("🚀 Smart Admin Upload"):
    if model:
        st.sidebar.subheader("AI Training Portal")
        new_pdf = st.sidebar.file_uploader("Upload SOP PDF", type="pdf")
        if new_pdf and st.sidebar.button("✨ Extract & Add"):
            with st.sidebar.status("AI Analyzing..."):
                pdf_text = extract_pdf_text(new_pdf)
                prompt = f"Format as CSV (no header): System, Process, Instructions, Rationale. Text: {pdf_text[:10000]}"
                response = model.generate_content(prompt)
                new_rows = pd.read_csv(io.StringIO(response.text), names=["System", "Process", "Instructions", "Rationale"])
                df = pd.concat([df, new_rows], ignore_index=True)
                df.to_csv("sop_data.csv", index=False)
                st.sidebar.success("Database Updated!")
                st.cache_data.clear()
                st.rerun()
    else:
        st.sidebar.error("AI Key missing in Secrets.")

# --- 3. MAIN INTERFACE ---
st.title("🏹 Arledge Operations Command")
st.markdown("---")

# Search Bar
query = st.text_input("🔍 Search Procedures (e.g. 'Price Release', 'V72', 'Dropship')")

if query:
    results = df[df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)]
    
    if not results.empty:
        for idx, row in results.iterrows():
            with st.expander(f"📌 {row['System']} | {row['Process']}"):
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.info(f"**Rationale:** {row['Rationale']}")
                    st.markdown(f"**Step-by-Step:**\n{row['Instructions']}")
                
                with col2:
                    # THE "REPORT ISSUE" BUTTON
                    subject = urllib.parse.quote(f"Issue with SOP: {row['Process']}")
                    body = urllib.parse.quote(f"I found an issue with the {row['Process']} procedure. Please review.")
                    mailto_link = f"mailto:support@arrow.com?subject={subject}&body={body}"
                    st.link_button("🚩 Report Issue", mailto_link)
            st.markdown("---")
    else:
        st.warning("No procedures found for that keyword.")
