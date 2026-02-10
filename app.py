import streamlit as st
import pandas as pd
import numpy as np
import io
import json
from PyPDF2 import PdfReader
import google.generativeai as genai

# 1. PAGE CONFIG
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# 2. AI CONFIG (The 404 Fix)
# Removing 'models/' prefix and setting the version explicitly if needed
API_KEY = "AIzaSyA4xwoKlP0iuUtSOkYvpYrADquexHL7YSE"
genai.configure(api_key=API_KEY)

# Use the short name 'gemini-1.5-flash' - the SDK will route to v1 stable automatically
MODEL_ID = 'gemini-1.5-flash' 
EMBED_MODEL = "models/embedding-001"

# Initialize model
model = genai.GenerativeModel(MODEL_ID)

# 3. UI THEME
st.markdown("""
<style>
    .stApp {background: linear-gradient(135deg, #0f172a, #1e293b); color: #f1f5f9;}
    .card {background: rgba(255,255,255,0.05); border-radius: 14px; padding: 18px; margin-bottom: 14px; border: 1px solid rgba(255,255,255,0.1);}
    .main-header {text-align:center; padding:12px; border-bottom:2px solid #f97316; margin-bottom:20px;}
    .instruction-box {white-space: pre-wrap; font-family: monospace; background: #0b1220; color: #f8fafc; padding: 15px; border-left: 4px solid #f97316; border-radius: 6px;}
</style>
""", unsafe_allow_html=True)

# 4. DATABASE INITIALIZATION
def load_db():
    try:
        df = pd.read_csv("sop_data.csv")
        if "Embedding" not in df.columns: df["Embedding"] = ""
        return df.fillna("")
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "Embedding"])

df = load_db()

# 5. VECTOR ENGINE
def get_embedding(text, task="retrieval_document"):
    try:
        res = genai.embed_content(model=EMBED_MODEL, content=text[:3000], task_type=task)
        return json.dumps(res['embedding'])
    except: return ""

# 6. HEADER & SIDEBAR
st.markdown('<div class="main-header"><h2>🏹 ARLEDGE OPERATIONS COMMAND</h2></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Admin")
    uploaded_file = st.file_uploader("Upload SOP PDF", type="pdf")
    
    if uploaded_file and st.button("✨ Implement SOP"):
        with st.spinner("AI is indexing procedures..."):
            try:
                # Read PDF
                reader = PdfReader(uploaded_file)
                raw_text = "".join([p.extract_text() or "" for p in reader.pages])

                # Extraction using stable model
                prompt = f"Extract procedures as CSV. Columns: System, Process, Instructions, Rationale. NO headers. Text: {raw_text[:10000]}"
                response = model.generate_content(prompt)
                
                csv_data = response.text.replace("```csv", "").replace("```", "").strip()
                new_rows = pd.read_csv(io.StringIO(csv_data), 
                                       names=["System", "Process", "Instructions", "Rationale"], 
                                       header=None)
                
                # Immediate Search Indexing
                st.info("Generating Search Vectors...")
                new_rows["Embedding"] = new_rows.apply(lambda x: get_embedding(f"{x['System']} {x['Process']}"), axis=1)
                
                # Update DB
                df = pd.concat([df, new_rows], ignore_index=True)
                df.to_csv("sop_data.csv", index=False)
                st.success("Database Rebuilt!")
                st.rerun()
            except Exception as e:
                st.error(f"Processing Error: {e}")

# 7. SEARCH INTERFACE
query = st.text_input("🔍 Search Technical Procedures")

if query and not df.empty:
    q_res = genai.embed_content(model=EMBED_MODEL, content=query, task_type="retrieval_query")
    q_emb = np.array(q_res['embedding'])

    def sim(row_emb):
        if not row_emb: return 0
        a = np.array(json.loads(row_emb))
        return np.dot(a, q_emb) / (np.linalg.norm(a) * np.linalg.norm(q_emb) + 1e-10)

    df["score"] = df["Embedding"].apply(sim)
    results = df.sort_values("score", ascending=False).head(5)
    results = results[results["score"] > 0.25]

    for _, row in results.iterrows():
        st.markdown(f"### 📌 {row['System']} | {row['Process']}")
        st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
        st.divider()
elif not query:
    st.info("Upload an SOP in the sidebar to begin.")
