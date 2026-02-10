import streamlit as st
import pandas as pd
import numpy as np
import io
import json
import urllib.parse
from PyPDF2 import PdfReader
import google.generativeai as genai

# 1. SETUP & AUTH
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# Using the direct key you provided - simplified config
API_KEY = "AIzaSyAFHZDDmcowqD_9TVZBqYSe9LgP-KSXQII"
genai.configure(api_key=API_KEY)

# THE FIX: We use a try-block to auto-assign the best available model string
try:
    # Attempting to find the exact string the API expects
    available_models = [m.name for m in genai.list_models()]
    MODEL_ID = next((m for m in available_models if "gemini-1.5-flash" in m), "models/gemini-1.5-flash")
except:
    MODEL_ID = "models/gemini-1.5-flash"

# 2. UI THEME
st.markdown("""
<style>
    .stApp {background: #0f172a; color: #f1f5f9;}
    .card {background: rgba(255,255,255,0.05); border-radius: 12px; padding: 20px; border: 1px solid #334155;}
    .main-header {text-align:center; padding:15px; border-bottom:3px solid #f97316; margin-bottom:25px;}
    .nano-tile {background: rgba(255,255,255,0.07); border-radius:10px; padding:10px; text-align:center; margin-bottom:10px;}
    .instruction-box {white-space: pre-wrap; font-family: monospace; background: #020617; 
                      color: #e2e8f0; padding: 15px; border-left: 5px solid #f97316; border-radius: 5px;}
</style>
""", unsafe_allow_html=True)

# 3. DATA PERSISTENCE
def load_db():
    try:
        df = pd.read_csv("sop_data.csv")
        # Ensure the Embedding column exists for the search to work
        if "Embedding" not in df.columns:
            df["Embedding"] = ""
        return df.fillna("")
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "Embedding"])

df = load_db()

# 4. VECTOR SEARCH LOGIC
def get_embedding(text, is_query=False):
    try:
        # Task types are critical for retrieval models
        t_type = "retrieval_query" if is_query else "retrieval_document"
        res = genai.embed_content(model="models/embedding-001", content=text, task_type=t_type)
        return json.dumps(res['embedding'])
    except:
        return ""

def calculate_similarity(row_emb, query_emb):
    try:
        if not row_emb or not query_emb: return 0
        a, b = np.array(json.loads(row_emb)), np.array(json.loads(query_emb))
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)
    except:
        return 0

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
for col, (label, icon, url) in zip(cols, platforms):
    with col:
        st.markdown(f'<div class="nano-tile"><b style="color:#94a3b8; font-size:0.7rem;">{label}</b></div>', unsafe_allow_html=True)
        st.link_button(icon, url, use_container_width=True)

st.divider()

# 6. ADMIN UPLOAD (SCRATCH BUILD)
st.sidebar.title("⚙️ Management")
if st.sidebar.checkbox("🚀 Upload New SOP"):
    uploaded_file = st.sidebar.file_uploader("Choose SOP PDF", type="pdf")
    if uploaded_file and st.sidebar.button("✨ Process with AI"):
        with st.spinner("AI is reading the document..."):
            reader = PdfReader(uploaded_file)
            text = "".join([p.extract_text() for p in reader.pages])
            
            # Simple, direct prompt to avoid CSV parsing errors
            prompt = f"Analyze this text and provide the SOP steps in CSV format: System, Process, Instructions, Rationale. Use no headers. Text: {text[:5000]}"
            
            ai_model = genai.GenerativeModel(MODEL_ID)
            response = ai_model.generate_content(prompt)
            
            # Cleaning the AI markdown
            raw_csv = response.text.replace("```csv", "").replace("```", "").strip()
            new_data = pd.read_csv(io.StringIO(raw_csv), names=["System", "Process", "Instructions", "Rationale"], header=None)
            
            # Generate Embeddings immediately so search works
            st.sidebar.info("Indexing for search...")
            new_data["Embedding"] = new_data.apply(lambda x: get_embedding(f"{x['System']} {x['Process']} {x['Instructions']}"), axis=1)
            
            # Save
            updated_df = pd.concat([df, new_data], ignore_index=True)
            updated_df.to_csv("sop_data.csv", index=False)
            st.sidebar.success("SOP Saved to Database!")
            st.rerun()

# 7. SEARCH & DISPLAY
query = st.text_input("🔍 Search Technical Procedures (e.g. 'Collector Setup')")

if query:
    q_emb = get_embedding(query, is_query=True)
    df["score"] = df["Embedding"].apply(lambda x: calculate_similarity(x, q_emb))
    
    # Filter for top results
    results = df[df["score"] > 0.2].sort_values(by="score", ascending=False).head(5)
    
    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f'<div class="card"><h3>📌 {row["System"]} | {row["Process"]}</h3>'
                        f'<p style="color:#94a3b8;">{row["Rationale"]}</p>'
                        f'<div class="instruction-box">{row["Instructions"]}</div></div>', unsafe_allow_html=True)
            st.write("")
    else:
        st.warning("No matches found. Try different keywords.")
