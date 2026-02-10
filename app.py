import streamlit as st
import pandas as pd
import numpy as np
import io
import json
import urllib.parse
from PyPDF2 import PdfReader
import google.generativeai as genai

# 1. PAGE CONFIG
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# 2. AI CONFIG (The 404 Fix)
# We use the direct string 'gemini-1.5-flash' which works across both v1 and v1beta
API_KEY = "AIzaSyAFHZDDmcowqD_9TVZBqYSe9LgP-KSXQII"
genai.configure(api_key=API_KEY)

# Try the most stable model names in order
MODEL_NAME = 'gemini-1.5-flash' 
EMBED_NAME = 'models/embedding-001'

# 3. PREMIUM UI THEME (Icons & Platforms)
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

# 4. DATABASE LOADING
@st.cache_data(ttl=3600)
def load_data():
    try:
        df = pd.read_csv("sop_data.csv").fillna("")
        if "Embedding" not in df.columns: df["Embedding"] = ""
        return df
    except:
        return pd.DataFrame(columns=["System","Process","Instructions","Rationale","Embedding"])

df = load_data()

# 5. SEARCH LOGIC
def embed_text(text, is_query=False):
    try:
        t_type = "retrieval_query" if is_query else "retrieval_document"
        result = genai.embed_content(model=EMBED_NAME, content=text[:3000], task_type=t_type)
        return json.dumps(result['embedding'])
    except: return ""

def cosine_sim(a, b):
    try:
        if not a or not b: return -1
        vec_a, vec_b = np.array(json.loads(a)), np.array(json.loads(b))
        return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b) + 1e-10)
    except: return -1

# 6. HEADER & PLATFORMS
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

# 7. ADMIN UPLOAD (Fixed for 404)
st.sidebar.title("⚙️ Admin Console")
if st.sidebar.checkbox("🚀 Smart AI Upload"):
    pdf_file = st.sidebar.file_uploader("Upload SOP PDF", type="pdf")
    if pdf_file and st.sidebar.button("✨ Extract & Learn"):
        with st.spinner("AI is analyzing document..."):
            try:
                reader = PdfReader(pdf_file)
                raw_text = "".join([p.extract_text() or "" for p in reader.pages])
                
                # We initialize the model INSIDE the function to ensure the correct name is used
                model = genai.GenerativeModel(MODEL_NAME)
                prompt = f"Extract procedures as CSV. Columns: System, Process, Instructions, Rationale. NO HEADERS. Text: {raw_text[:8000]}"
                response = model.generate_content(prompt)
                
                csv_clean = response.text.replace("```csv", "").replace("```", "").strip()
                new_rows = pd.read_csv(io.StringIO(csv_clean), names=["System", "Process", "Instructions", "Rationale"], header=None)
                
                # Indexing
                st.sidebar.info("Building search index...")
                new_rows["Embedding"] = (new_rows["System"] + " " + new_rows["Process"]).apply(lambda x: embed_text(x))
                
                df_updated = pd.concat([df, new_rows], ignore_index=True)
                df_updated.to_csv("sop_data.csv", index=False)
                
                st.sidebar.success("Database Updated!")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Error: {e}")
                # Added a fallback to help you debug
                st.sidebar.write("Try checking available models in your console.")

# 8. SEARCH ENGINE
st.markdown('<div class="card">', unsafe_allow_html=True)
query = st.text_input("🔍 Search Technical Procedures")
st.markdown('</div>', unsafe_allow_html=True)

if query and not df.empty:
    q_emb = embed_text(query, is_query=True)
    df["score"] = df["Embedding"].apply(lambda x: cosine_sim(x, q_emb))
    results = df.sort_values(by="score", ascending=False).head(5)
    results = results[results["score"] > 0.2]

    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"### 📌 {row['System']} | {row['Process']}")
            st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
            st.divider()
