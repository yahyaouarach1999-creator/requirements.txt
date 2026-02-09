import streamlit as st
import pandas as pd
import re
import urllib.parse
import google.generativeai as genai
from PyPDF2 import PdfReader
import io

# 1. SETUP
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# --- AI CONFIGURATION ---
try:
    API_KEY = "AIzaSyAFHZDDmcowqD_9TVZBqYSe9LgP-KSXQII" 
    genai.configure(api_key=API_KEY)
    
    # CHANGED: Added "models/" prefix for better compatibility
    model = genai.GenerativeModel('models/gemini-1.5-flash') 
except Exception:
    model = None

# --- HELPER FUNCTIONS ---
def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

@st.cache_data
def load_data():
    try:
        return pd.read_csv("sop_data.csv").fillna("")
    except:
        empty_df = pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale"])
        empty_df.to_csv("sop_data.csv", index=False)
        return empty_df

# --- CSS ---
st.markdown("""
    <style>
        .main-header { background-color: #0F172A; padding: 10px; color: white; text-align: center; border-bottom: 3px solid #F97316; margin-bottom: 15px; }
        .nano-tile { background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; text-align: center; padding: 5px; transition: 0.2s; }
        .nano-label { font-size: 0.6rem; font-weight: 900; color: #64748B; text-transform: uppercase; margin-bottom: 2px; }
        .instruction-box { white-space: pre-wrap; font-family: monospace; background: #1E293B; color: #F8FAFC; padding: 15px; border-left: 5px solid #F97316; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# 2. LOAD DATABASE
df = load_data()

# 3. AUTHENTICATION
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.markdown('<div class="main-header"><h4>🔒 ARROW.COM ACCESS REQUIRED</h4></div>', unsafe_allow_html=True)
    user_email = st.text_input("Official Email:")
    if st.button("Enter Portal"):
        if "@arrow.com" in user_email.lower():
            st.session_state['auth'] = True
            st.rerun()
        else:
            st.error("Denied.")
    st.stop()

# 4. MAIN APP CONTENT
st.markdown('<div class="main-header"><h4>🏹 ARLEDGE OPERATIONS COMMAND</h4></div>', unsafe_allow_html=True)

# --- NANO NAVIGATION (Restored Links) ---
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown('<div class="nano-tile"><div class="nano-label">Salesforce</div></div>', unsafe_allow_html=True)
    st.link_button("🚀 CRM", "https://arrowcrm.lightning.force.com/", use_container_width=True)
with col2:
    st.markdown('<div class="nano-tile"><div class="nano-label">SWB Oracle</div></div>', unsafe_allow_html=True)
    st.link_button("💾 Orders", "https://acswb.arrow.com/Swb/", use_container_width=True)
with col3:
    st.markdown('<div class="nano-tile"><div class="nano-label">ETQ Portal</div></div>', unsafe_allow_html=True)
    st.link_button("📋 Forms", "https://arrow.etq.com/prod/rel/#/app/system/portal", use_container_width=True)
with col4:
    st.markdown('<div class="nano-tile"><div class="nano-label">Support</div></div>', unsafe_allow_html=True)
    st.link_button("🛠️ Tickets", "https://arrow.service-now.com/myconnect", use_container_width=True)
with col5:
    st.markdown('<div class="nano-tile"><div class="nano-label">SOS Help</div></div>', unsafe_allow_html=True)
    st.link_button("🆘 Contact", "mailto:yahya.ouarach@arrow.com", use_container_width=True)

st.divider()

# --- ADMIN SIDEBAR ---
st.sidebar.title("⚙️ Admin Console")
if st.sidebar.checkbox("🚀 Smart AI Upload"):
    st.sidebar.info("Upload a PDF to automatically extract procedures into the search engine.")
    new_pdf = st.sidebar.file_uploader("Upload SOP PDF", type="pdf")
    if new_pdf and st.sidebar.button("✨ Extract & Add"):
        with st.spinner("AI is reading PDF and formatting data..."):
            raw_text = extract_pdf_text(new_pdf)
            # Refined prompt for better CSV results
            prompt = f"""Extract all procedures from this text. 
            Format exactly as CSV with NO HEADER. 
            Columns: System, Process, Instructions, Rationale.
            Text: {raw_text[:10000]}"""
            
            response = model.generate_content(prompt)
            
            try:
                # Clean the response text (remove markdown if AI includes it)
                cleaned_csv = response.text.replace('```csv', '').replace('```', '').strip()
                new_rows = pd.read_csv(io.StringIO(cleaned_csv), names=["System", "Process", "Instructions", "Rationale"])
                
                # Merge and Save
                updated_df = pd.concat([df, new_rows], ignore_index=True)
                updated_df.to_csv("sop_data.csv", index=False)
                
                st.sidebar.success(f"Successfully added {len(new_rows)} rows!")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Error parsing data: {e}")

# --- SEARCH ENGINE ---
query = st.text_input("🔍 Search Combined Technical Procedures", placeholder="Search 'Verification', 'Price Release'...")

if query:
    results = df[df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)]
    if not results.empty:
        for index, row in results.iterrows():
            st.markdown(f"### 📌 {row['System']} | {row['Process']}")
            st.caption(f"**Rationale:** {row['Rationale']}")
            st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
            
            # THE RESTORED REPORT ISSUE BUTTON
            subject = urllib.parse.quote(f"SOP Issue Report: {row['Process']}")
            body = urllib.parse.quote(f"Issue with procedure:\nSystem: {row['System']}\nProcess: {row['Process']}\n\nPlease update.")
            mailto_link = f"mailto:yahya.ouarach@arrow.com?subject={subject}&body={body}"
            
            st.link_button("🚩 Report Issue", mailto_link)
            st.markdown("---")
    else:
        st.warning("No matches found.")
