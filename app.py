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

# --------------------------------------------------
# 1. PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# --------------------------------------------------
# 2. PREMIUM UI THEME
# --------------------------------------------------
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #0f172a, #1e293b); color: #f1f5f9;}
.block-container {padding-top: 1rem;}
.card {background: rgba(255,255,255,0.05); backdrop-filter: blur(10px);
border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 18px; margin-bottom: 14px;}
.main-header {text-align:center; padding:12px; border-bottom:2px solid #f97316; margin-bottom:20px;}
.nano-tile {background: rgba(255,255,255,0.05); border-radius:10px; padding:8px; text-align:center;}
.nano-label {font-size:0.65rem; font-weight:700; color:#94a3b8; text-transform:uppercase;}
.instruction-box {white-space: pre-wrap; font-family: monospace; background: #0b1220;
color: #f8fafc; padding: 15px; border-left: 4px solid #f97316; border-radius: 6px;}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 3. AI CONFIG (Fixed Model Strings)
# --------------------------------------------------
# Use your provided key directly or via secrets
API_KEY = "AIzaSyAFHZDDmcowqD_9TVZBqYSe9LgP-KSXQII" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# --------------------------------------------------
# 4. DATA LOADING
# --------------------------------------------------
@st.cache_data(ttl=3600)
def load_data():
    try:
        df = pd.read_csv("sop_data.csv")
        df.fillna("", inplace=True)
        return df
    except:
        df = pd.DataFrame(columns=[
            "System","Process","Instructions","Rationale",
            "Version","Last_Updated","Embedding"
        ])
        df.to_csv("sop_data.csv", index=False)
        return df

df = load_data()

def save_data(dataframe):
    dataframe.to_csv("sop_data.csv", index=False)

# --------------------------------------------------
# 5. PDF TEXT EXTRACTION
# --------------------------------------------------
def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "".join(page.extract_text() or "" for page in reader.pages)

# --------------------------------------------------
# 6. SIDEBAR METRICS
# --------------------------------------------------
st.sidebar.markdown("### 📊 System Metrics")
st.sidebar.metric("Total SOPs", len(df))
st.sidebar.metric("Systems", df["System"].nunique() if len(df) else 0)
st.sidebar.metric("Processes", df["Process"].nunique() if len(df) else 0)

# --------------------------------------------------
# 7. HEADER
# --------------------------------------------------
st.markdown('<div class="main-header"><h2>🏹 ARLEDGE OPERATIONS COMMAND CENTER</h2></div>', unsafe_allow_html=True)

# --------------------------------------------------
# 8. NAVIGATION LINKS
# --------------------------------------------------
cols = st.columns(5)
links = [
    ("Salesforce", "🚀 CRM", "https://arrowcrm.lightning.force.com/"),
    ("SWB Oracle", "💾 Orders", "https://acswb.arrow.com/Swb/"),
    ("ETQ Portal", "📋 Forms", "https://arrow.etq.com/prod/rel/#/app/system/portal"),
    ("Support", "🛠️ Tickets", "https://arrow.service-now.com/myconnect"),
    ("SOS Help", "🆘 Contact", "mailto:yahya.ouarach@arrow.com")
]
for col, (label, btn, url) in zip(cols, links):
    with col:
        st.markdown(f'<div class="nano-tile"><div class="nano-label">{label}</div></div>', unsafe_allow_html=True)
        st.link_button(btn, url, use_container_width=True)

st.divider()

# --------------------------------------------------
# 9. EMBEDDING FUNCTIONS (Fixed for Retrieval)
# --------------------------------------------------
def embed_text(text, is_query=False):
    try:
        # task_type is MANDATORY for Gemini embeddings
        t_type = "retrieval_query" if is_query else "retrieval_document"
        emb = genai.embed_content(
            model="models/embedding-001",
            content=text[:3000],
            task_type=t_type
        )["embedding"]
        return json.dumps(emb)
    except Exception:
        return ""

def cosine_sim(a, b):
    try:
        if not a or not b: return -1
        vec_a = np.array(json.loads(a))
        vec_b = np.array(json.loads(b))
        return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b) + 1e-10)
    except:
        return -1

# --------------------------------------------------
# 10. ADMIN AI PDF INGESTION (Bulletproof CSV)
# --------------------------------------------------
st.sidebar.title("⚙️ Admin Console")
if st.sidebar.checkbox("🚀 Smart AI SOP Upload"):
    pdf = st.sidebar.file_uploader("Upload SOP PDF", type="pdf")
    if pdf and st.sidebar.button("✨ Extract Procedures"):
        with st.spinner("AI is analyzing the document..."):
            try:
                raw_text = extract_pdf_text(pdf)
                prompt = f"""Extract SOP steps. 
                Output ONLY valid CSV rows. NO MARKDOWN. NO HEADERS.
                Columns: System, Process, Instructions, Rationale.
                TEXT: {raw_text[:8000]}"""
                
                response = model.generate_content(prompt)
                cleaned = response.text.replace("```csv","").replace("```","").strip()
                
                new_rows = pd.read_csv(io.StringIO(cleaned),
                                       names=["System","Process","Instructions","Rationale"],
                                       header=None)
                
                new_rows["Version"] = 1
                new_rows["Last_Updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")

                st.sidebar.info("Generating AI Index...")
                # Combined context for better search
                new_rows["Embedding"] = (new_rows["Process"] + " " + new_rows["Instructions"]).apply(lambda x: embed_text(x, is_query=False))

                df_updated = pd.concat([df, new_rows], ignore_index=True)
                save_data(df_updated)

                st.sidebar.success(f"Added {len(new_rows)} SOPs!")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"AI Error: {e}")

# --------------------------------------------------
# 11. SEARCH (Ranked by Relevance)
# --------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🔍 Intelligent SOP Search")
query = st.text_input("Search procedures in plain English (e.g., 'How do I handle dropships?')")
st.markdown('</div>', unsafe_allow_html=True)

results = pd.DataFrame()

if query and len(df) > 0:
    try:
        q_embed = embed_text(query, is_query=True)
        # Apply similarity scoring
        df["score"] = df["Embedding"].apply(lambda x: cosine_sim(x, q_embed))
        results = df.sort_values("score", ascending=False).head(5)
        # Filter out low-relevance matches
        results = results[results["score"] > 0.3]
    except Exception as e:
        st.error("Search index busy. Try again in a moment.")

if not results.empty:
    for _, row in results.iterrows():
        with st.container():
            st.markdown(f"### 📌 {row['System']} | {row['Process']}")
            st.caption(f"**Rationale:** {row['Rationale']}")
            st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)

            subject = urllib.parse.quote(f"SOP Issue: {row['Process']}")
            mailto = f"mailto:yahya.ouarach@arrow.com?subject={subject}"
            st.link_button("🚩 Report Issue", mailto)
            st.markdown("---")
elif query:
    st.warning("No matching procedures found. Try different keywords.")

# --------------------------------------------------
# 12. AI COPILOT (RAG Implementation)
# --------------------------------------------------

st.divider()
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🧠 Arledge AI Copilot")

question = st.text_area("Ask an operational question based on the SOPs above")

if st.button("Get AI Guidance") and question:
    if not results.empty:
        with st.spinner("Consulting operations intelligence..."):
            # Provide the search results as context to the AI
            context = "\n\n".join([f"Process: {r['Process']}\nInstructions: {r['Instructions']}" for _, r in results.iterrows()])
            prompt = f"""You are the Arledge Ops Expert. Answer the question using ONLY the context provided.
            If the answer isn't in the context, say you don't know.
            CONTEXT:
            {context}
            
            QUESTION: {question}"""
            
            try:
                answer = model.generate_content(prompt)
                st.markdown("#### AI Response:")
                st.write(answer.text)
            except Exception as e:
                st.error("AI Copilot is offline.")
    else:
        st.info("Please search for a procedure first so the Copilot has context to read.")

st.markdown('</div>', unsafe_allow_html=True)
