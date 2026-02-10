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
def discover_model():
    """Finds the exact model name supported by your API version."""
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Prioritize 1.5 Flash
        flash_path = next((m for m in models if 'gemini-1.5-flash' in m), "models/gemini-1.5-flash")
        return flash_path
    except:
        return "models/gemini-1.5-flash"

MODEL_ID = discover_model()
EMBED_MODEL = "models/embedding-001"

# 3. PREMIUM UI THEME (Icons Restored)
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

# 4. DATA LOGIC (Clean Slate)
def load_db():
    try:
        # Load or create fresh if deleted
        df = pd.read_csv("sop_data.csv").fillna("")
        if "Embedding" not in df.columns: df["Embedding"] = ""
        return df
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "Embedding"])

df = load_db()

def get_embedding(text, is_query=False):
    try:
        t_type = "retrieval_query" if is_query else "retrieval_document"
        res = genai.embed_content(model=EMBED_MODEL, content=text[:3000], task_type=t_type)
        return json.dumps(res['embedding'])
    except: return ""

# 5. HEADER & PLATFORM ICONS
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

# 6. DIRECT UPLOAD & IMPLEMENTATION
st.sidebar.title("⚙️ Admin Console")
if st.sidebar.checkbox("🚀 Direct SOP Implementation"):
    pdf_file = st.sidebar.file_uploader("Upload SOP PDF", type="pdf")
    if pdf_file and st.sidebar.button("✨ Extract & Build Index"):
        with st.spinner(f"AI using discovered model: {MODEL_ID}"):
            try:
                # Read
                reader = PdfReader(pdf_file)
                raw_text = "".join([p.extract_text() for p in reader.pages])
                
                # Extract
                model = genai.GenerativeModel(MODEL_ID)
                prompt = (f"Extract procedures as CSV. Columns: System, Process, Instructions, Rationale. "
                          f"Use no headers or markdown. Text: {raw_text[:8000]}")
                response = model.generate_content(prompt)
                
                # Format
                csv_data = response.text.replace("```csv", "").replace("```", "").strip()
                new_data = pd.read_csv(io.StringIO(csv_data), 
                                      names=["System", "Process", "Instructions", "Rationale"], 
                                      header=None)
                
                # Index (Crucial for search to work immediately)
                st.sidebar.info("Building AI Search Index...")
                new_data["Embedding"] = new_data.apply(lambda x: get_embedding(f"{x['System']} {x['Process']}"), axis=1)
                
                # Save
                final_df = pd.concat([df, new_data], ignore_index=True)
                final_df.to_csv("sop_data.csv", index=False)
                st.sidebar.success("SOP implemented successfully!")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Discovery Error: {e}")

# 7. SEARCH ENGINE
query = st.text_input("🔍 Search Technical Procedures")

if query and not df.empty:
    q_emb = get_embedding(query, is_query=True)
    
    def sim(row_emb, query_emb):
        if not row_emb or not query_emb: return 0
        a, b = np.array(json.loads(row_emb)), np.array(json.loads(query_emb))
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)

    df["score"] = df["Embedding"].apply(lambda x: sim(x, q_emb))
    results = df.sort_values(by="score", ascending=False).head(5)
    results = results[results["score"] > 0.2]

    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"### 📌 {row['System']} | {row['Process']}")
            st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
            st.divider()
    else:
        st.warning("No matches found.")
