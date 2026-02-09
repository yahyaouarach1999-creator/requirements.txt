import streamlit as st
import pandas as pd
import re
import urllib.parse
import google.generativeai as genai
from PyPDF2 import PdfReader
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        .main-header { background-color: #0F172A; padding: 10px; color: white; text-align: center; border-bottom: 3px solid #F97316; margin-bottom: 15px; }
        .nano-tile { 
            background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; 
            text-align: center; padding: 5px; transition: 0.2s;
        }
        .nano-tile:hover { border-color: #F97316; background-color: #F1F5F9; transform: translateY(-1px); }
        .nano-label { font-size: 0.6rem; font-weight: 900; color: #64748B; text-transform: uppercase; margin-bottom: 2px; }
        .instruction-box { white-space: pre-wrap; font-family: 'Consolas', monospace; font-size: 0.85rem; background: #1E293B; color: #F8FAFC; padding: 15px; border-left: 5px solid #F97316; border-radius: 4px; }
        .stButton>button { border-radius: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- AI CONFIGURATION ---
# Replace with your key from https://aistudio.google.com/
API_KEY = "YOUR_GEMINI_API_KEY_HERE" 

if API_KEY != "YOUR_GEMINI_API_KEY_HERE":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

# --- HELPER FUNCTIONS ---
def check_email(email):
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@arrow\.com$", email))

@st.cache_data
def load_data():
    try:
        return pd.read_csv("sop_data.csv").fillna("")
    except FileNotFoundError:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale"])

def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# --- AUTHENTICATION GATE ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown('<div class="main-header"><h4>🔒 ARROW.COM ACCESS REQUIRED</h4></div>', unsafe_allow_html=True)
    with st.form("auth"):
        user_email = st.text_input("Official Email:")
        if st.form_submit_button("Enter Portal"):
            if check_email(user_email):
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Access Denied: @arrow.com domain only.")
    st.stop()

# --- LOAD DATA ---
df = load_data()

# --- APP CONTENT ---
st.markdown('<div class="main-header"><h4>🏹 ARLEDGE OPERATIONS COMMAND</h4></div>', unsafe_allow_html=True)

# --- NANO NAVIGATION ---
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

# --- SIDEBAR ADMIN TOOLS ---
st.sidebar.title("⚙️ Admin Settings")
if st.sidebar.checkbox("🚀 Smart PDF Upload"):
    st.sidebar.markdown("### Extract SOP from PDF")
    if model is None:
        st.sidebar.error("Please set your Gemini API Key in the code to use this feature.")
    else:
        new_pdf = st.sidebar.file_uploader("Upload SOP PDF", type="pdf")
        if new_pdf and st.sidebar.button("✨ Extract & Append"):
            with st.spinner("AI analyzing document..."):
                raw_text = extract_pdf_text(new_pdf)
                prompt = f"""
                Act as a technical writer. Extract procedures from the text below.
                Output ONLY valid CSV lines (no header).
                Columns: System, Process, Instructions, Rationale.
                Instructions should be step-by-step.
                Text: {raw_text[:10000]}
                """
                response = model.generate_content(prompt)
                
                try:
                    new_rows_io = io.StringIO(response.text)
                    new_df = pd.read_csv(new_rows_io, names=["System", "Process", "Instructions", "Rationale"])
                    updated_df = pd.concat([df, new_df], ignore_index=True)
                    updated_df.to_csv("sop_data.csv", index=False)
                    st.sidebar.success(f"Added {len(new_df)} rows!")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.sidebar.error("Extraction failed. Try a cleaner PDF.")

# --- SEARCH ENGINE ---
query = st.text_input("🔍 Search Combined Technical
