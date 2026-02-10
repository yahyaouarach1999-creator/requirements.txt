import streamlit as st
import pandas as pd
import numpy as np
import io
import json
from PyPDF2 import PdfReader
import google.generativeai as genai

# 1. PAGE CONFIG
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# 2. AI CONFIG (The Final Stable Fix)
API_KEY = "AIzaSyA4xwoKlP0iuUtSOkYvpYrADquexHL7YSE"
genai.configure(api_key=API_KEY)

# Use the string 'gemini-1.5-flash' directly - it works best for Free Tier projects
MODEL_ID = 'gemini-1.5-flash'
EMBED_MODEL = "models/embedding-001"

# 3. UI STYLE
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #0f172a, #1e293b); color: #f1f5f9;}
.main-header {text-align:center; padding:12px; border-bottom:2px solid #f97316; margin-bottom:20px;}
.instruction-box {white-space: pre-wrap; font-family: monospace; background: #0b1220; color: #f8fafc; padding: 15px; border-left: 4px solid #f97316; border-radius: 6px;}
</style>
""", unsafe_allow_html=True)

# 4. DATA LOGIC
def load_db():
    try:
        df = pd.read_csv("sop_data.csv")
        if "Embedding" not in df.columns: df["Embedding"] = ""
        return df.fillna("")
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "Embedding"])

df = load_db()

def get_embedding(text, task="retrieval_document"):
    try:
        res = genai.embed_content(model=EMBED_MODEL, content=text[:3000], task_type=task)
        return json.dumps(res['embedding'])
    except: return ""

# 5. HEADER
st.markdown('<div class="main-header"><h2>🏹 ARLEDGE OPERATIONS COMMAND CENTER</h2></div>', unsafe_allow_html=True)

# 6. SIDEBAR: PDF INGESTION
st.sidebar.title("⚙️ SOP Management")
if st.sidebar.checkbox("🚀 Upload SOP PDF"):
    pdf_file = st.sidebar.file_uploader("Upload PDF", type="pdf")
    if pdf_file and st.sidebar.button("✨ Extract & Implement"):
        with st.spinner("AI is analyzing document structure..."):
            try:
                reader = PdfReader(pdf_file)
                raw_text = "".join([p.extract_text() or "" for p in reader.pages])

                # Use the GenerativeModel class (Standard for Gemini)
                model = genai.GenerativeModel(MODEL_ID)
                prompt = f"Extract procedures as CSV. Columns: System, Process, Instructions, Rationale. NO headers. Text: {raw_text[:8000]}"
                
                response = model.generate_content(prompt)
                csv_data = response.text.replace("```csv", "").replace("```", "").strip()

                new_data = pd.read_csv(io.StringIO(csv_data), 
                                      names=["System", "Process", "Instructions", "Rationale"], 
                                      header=None)

                st.sidebar.info("Building AI Search Index...")
                new_data["Embedding"] = new_data.apply(lambda x: get_embedding(f"{x['System']} {x['Process']}"), axis=1)

                final_df = pd.concat([df, new_data], ignore_index=True)
                final_df.to_csv("sop_data.csv", index=False)
                st.sidebar.success("Database Updated!")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

# 7. SEARCH ENGINE
st.subheader("🔍 Intelligent SOP Search")
query = st.text_input("Search technical procedures")

if query and not df.empty:
    # Embed the query
    q_res = genai.embed_content(model=EMBED_MODEL, content=query, task_type="retrieval_query")
    q_emb = np.array(q_res['embedding'])

    def score(row_emb):
        if not row_emb: return 0
        a = np.array(json.loads(row_emb))
        return np.dot(a, q_emb) / (np.linalg.norm(a) * np.linalg.norm(q_emb) + 1e-10)

    df["score"] = df["Embedding"].apply(score)
    results = df.sort_values("score", ascending=False).head(5)
    results = results[results["score"] > 0.25]

    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"### 📌 {row['System']} | {row['Process']}")
            st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
            st.divider()
    else:
        st.warning("No matches found.")
