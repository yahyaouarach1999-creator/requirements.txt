import streamlit as st
import pandas as pd
import numpy as np
import io
import os
import urllib.parse
import json
from datetime import datetime
from PyPDF2 import PdfReader
import google.generativeai as genai

# 1. PAGE CONFIG
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# 2. UI THEME
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #0f172a, #1e293b); color: #f1f5f9;}
.card {background: rgba(255,255,255,0.05); border-radius: 14px; padding: 18px; margin-bottom: 14px;}
.main-header {text-align:center; padding:12px; border-bottom:2px solid #f97316; margin-bottom:20px;}
.instruction-box {white-space: pre-wrap; font-family: monospace; background: #0b1220; color: #f8fafc; padding: 15px; border-left: 4px solid #f97316; border-radius: 6px;}
</style>
""", unsafe_allow_html=True)

# 3. AI CONFIG (Fixed Model Names to solve 404/NotFound)
API_KEY = "AIzaSyAFHZDDmcowqD_9TVZBqYSe9LgP-KSXQII" 
genai.configure(api_key=API_KEY)

# Use full model paths to be safe across all API versions
model = genai.GenerativeModel("models/gemini-1.5-flash") 

# 4. DATA HANDLING
@st.cache_data(ttl=3600)
def load_data():
    try:
        df = pd.read_csv("sop_data.csv")
        df.fillna("", inplace=True)
        return df
    except:
        return pd.DataFrame(columns=["System","Process","Instructions","Rationale","Embedding"])

df = load_data()

# 5. FIXED EMBEDDING LOGIC (Solves "Index Busy" error)
def embed_text(text, is_query=False):
    try:
        # Task type is required for embedding-001
        t_type = "retrieval_query" if is_query else "retrieval_document"
        emb = genai.embed_content(
            model="models/embedding-001",
            content=text[:3000],
            task_type=t_type
        )["embedding"]
        return json.dumps(emb)
    except:
        return ""

def cosine_sim(a, b):
    try:
        if not a or not b: return -1
        vec_a = np.array(json.loads(a))
        vec_b = np.array(json.loads(b))
        return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b) + 1e-10)
    except:
        return -1

# 6. NAVIGATION
st.markdown('<div class="main-header"><h2>🏹 ARLEDGE OPERATIONS COMMAND</h2></div>', unsafe_allow_html=True)
cols = st.columns(5)
links = [("CRM", "https://arrowcrm.lightning.force.com/"), ("Orders", "https://acswb.arrow.com/Swb/"), ("Forms", "https://arrow.etq.com/prod/rel/#/app/system/portal"), ("Tickets", "https://arrow.service-now.com/myconnect"), ("Contact", "mailto:yahya.ouarach@arrow.com")]
for col, (label, url) in zip(cols, links):
    col.link_button(label, url, use_container_width=True)

# 7. ADMIN UPLOAD
st.sidebar.title("⚙️ Admin")
if st.sidebar.checkbox("🚀 Smart AI Upload"):
    pdf = st.sidebar.file_uploader("Upload SOP PDF", type="pdf")
    if pdf and st.sidebar.button("✨ Extract"):
        reader = PdfReader(pdf)
        raw_text = "".join(p.extract_text() for p in reader.pages)
        prompt = f"Extract SOPs as CSV (System, Process, Instructions, Rationale). No headers. Text: {raw_text[:8000]}"
        response = model.generate_content(prompt)
        cleaned = response.text.replace("```csv","").replace("```","").strip()
        new_rows = pd.read_csv(io.StringIO(cleaned), names=["System","Process","Instructions","Rationale"])
        
        # Generate search index
        new_rows["Embedding"] = (new_rows["Process"] + " " + new_rows["Instructions"]).apply(lambda x: embed_text(x))
        
        df = pd.concat([df, new_rows], ignore_index=True)
        df.to_csv("sop_data.csv", index=False)
        st.sidebar.success("Updated!")
        st.rerun()

# 8. SEARCH & DISPLAY
query = st.text_input("🔍 Search procedures...")
if query and len(df) > 0:
    q_emb = embed_text(query, is_query=True)
    df["score"] = df["Embedding"].apply(lambda x: cosine_sim(x, q_emb))
    results = df.sort_values("score", ascending=False).head(3)
    
    for _, row in results.iterrows():
        st.markdown(f"### 📌 {row['System']} | {row['Process']}")
        st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
