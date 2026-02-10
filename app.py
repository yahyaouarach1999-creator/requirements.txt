import streamlit as st
import pandas as pd
import numpy as np
import io
import json
from PyPDF2 import PdfReader
import google.generativeai as genai

# 1. PAGE CONFIG
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# 2. AI CONFIG (The 404 & Discovery Fix)
API_KEY = "AIzaSyAFHZDDmcowqD_9TVZBqYSe9LgP-KSXQII"
genai.configure(api_key=API_KEY)

@st.cache_resource
def get_model_id():
    """Finds the exact model name your API key supports to avoid 404 errors."""
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Find any version of 1.5 flash available to you
        target = next((m for m in models if 'gemini-1.5-flash' in m), "gemini-1.5-flash")
        return target
    except:
        return "gemini-1.5-flash"

MODEL_ID = get_model_id()
EMBED_MODEL = "models/embedding-001"

# 3. UI THEME (Icons Restored)
st.markdown("""
<style>
    .stApp {background: linear-gradient(135deg, #0f172a, #1e293b); color: #f1f5f9;}
    .card {background: rgba(255,255,255,0.05); border-radius: 14px; padding: 18px; margin-bottom: 14px; border: 1px solid rgba(255,255,255,0.1);}
    .main-header {text-align:center; padding:12px; border-bottom:2px solid #f97316; margin-bottom:20px;}
    .nano-tile {background: rgba(255,255,255,0.05); border-radius:10px; padding:8px; text-align:center;}
    .nano-label {font-size:0.65rem; font-weight:700; color:#94a3b8; text-transform:uppercase;}
    .instruction-box {white-space: pre-wrap; font-family: monospace; background: #0b1220; color: #f8fafc; padding: 15px; border-left: 4px solid #f97316; border-radius: 6px;}
</style>
""", unsafe_allow_html=True)

# 4. DATABASE INITIALIZATION
def load_db():
    try:
        df = pd.read_csv("sop_data.csv")
        # Ensure the Embedding column is always present for search logic
        if "Embedding" not in df.columns: df["Embedding"] = ""
        return df.fillna("")
    except:
        # Create fresh structure if file is missing/deleted
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "Embedding"])

df = load_db()

# 5. SEARCH LOGIC
def get_embedding(text, is_query=False):
    try:
        t_type = "retrieval_query" if is_query else "retrieval_document"
        res = genai.embed_content(model=EMBED_MODEL, content=text[:3000], task_type=t_type)
        return json.dumps(res['embedding'])
    except: return ""

# 6. HEADER & PLATFORM ICONS
st.markdown('<div class="main-header"><h2>🏹 ARLEDGE OPERATIONS COMMAND</h2></div>', unsafe_allow_html=True)
cols = st.columns(5)
platforms = [
    ("SALESFORCE", "🚀 CRM", "https://arrowcrm.lightning.force.com/"),
    ("SWB ORACLE", "💾 Orders", "https://acswb.arrow.com/Swb/"),
    ("ETQ PORTAL", "📋 Forms", "https://arrow.etq.com/prod/rel/#/app/system/portal"),
    ("SUPPORT", "🛠️ Tickets", "https://arrow.service-now.com/myconnect"),
    ("SOS HELP", "🆘 Contact", "mailto:yahya.ouarach@arrow.com")
]
for col, (label, btn, url) in zip(cols, platforms):
    with col:
        st.markdown(f'<div class="nano-tile"><div class="nano-label">{label}</div></div>', unsafe_allow_html=True)
        st.link_button(btn, url, use_container_width=True)

st.divider()

# 7. DIRECT UPLOAD & IMPLEMENTATION
st.sidebar.title("⚙️ Admin Console")
if st.sidebar.checkbox("🚀 Start New SOP Upload"):
    pdf_file = st.sidebar.file_uploader("Choose PDF File", type="pdf")
    if pdf_file and st.sidebar.button("✨ Extract & Implement"):
        with st.spinner(f"AI using {MODEL_ID}..."):
            try:
                reader = PdfReader(pdf_file)
                raw_text = "".join([p.extract_text() for p in reader.pages])
                
                model = genai.GenerativeModel(MODEL_ID)
                prompt = (f"Analyze this document. Extract procedures as CSV. "
                          f"Columns: System, Process, Instructions, Rationale. "
                          f"NO headers. NO backticks. Text: {raw_text[:8000]}")
                response = model.generate_content(prompt)
                
                # Cleanup CSV formatting from AI
                csv_data = response.text.replace("```csv", "").replace("```", "").strip()
                new_data = pd.read_csv(io.StringIO(csv_data), names=["System", "Process", "Instructions", "Rationale"], header=None)
                
                # Generate Search Vectors Immediately
                st.sidebar.info("Building AI Search Index...")
                new_data["Embedding"] = new_data.apply(lambda x: get_embedding(f"{x['System']} {x['Process']}"), axis=1)
                
                # Combine with existing (or empty) DB
                final_df = pd.concat([df, new_data], ignore_index=True)
                final_df.to_csv("sop_data.csv", index=False)
                st.sidebar.success("Database Rebuilt Successfully!")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Upload failed: {e}")

# 8. SEARCH INTERFACE
query = st.text_input("🔍 Search Technical Procedures (e.g. 'Collector')")

if query and not df.empty:
    q_emb = get_embedding(query, is_query=True)
    
    def calculate_sim(row_emb, query_emb):
        if not row_emb or not query_emb: return 0
        a, b = np.array(json.loads(row_emb)), np.array(json.loads(query_emb))
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)

    df["score"] = df["Embedding"].apply(lambda x: calculate_sim(x, q_emb))
    results = df.sort_values(by="score", ascending=False).head(5)
    results = results[results["score"] > 0.2]

    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"### 📌 {row['System']} | {row['Process']}")
            st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
            st.divider()
    else:
        st.warning("No matches found in the new database.")
elif not query:
    st.info("The database is currently empty. Use the sidebar to upload your first SOP.")
