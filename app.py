import streamlit as st
import pandas as pd
import numpy as np
import io
import json
import urllib.parse
from datetime import datetime
from PyPDF2 import PdfReader
import google.generativeai as genai

# 1. INITIAL SETUP
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# 2. AI CONFIGURATION (Stabilized Model Paths)
API_KEY = "AIzaSyAFHZDDmcowqD_9TVZBqYSe9LgP-KSXQII"
try:
    genai.configure(api_key=API_KEY)
    # Using 'models/' prefix is the most stable way to call these
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    EMBED_MODEL = "models/embedding-001"
except Exception as e:
    st.error(f"AI Connection Error: {e}")

# 3. STYLING (The Premium Dark Theme)
st.markdown("""
<style>
    .stApp {background: #0f172a; color: #f1f5f9;}
    .card {background: rgba(255,255,255,0.05); border-radius: 12px; padding: 20px; margin-bottom: 15px; border: 1px solid #334155;}
    .main-header {text-align:center; padding:15px; border-bottom:3px solid #f97316; margin-bottom:25px;}
    .instruction-box {white-space: pre-wrap; font-family: 'Courier New', monospace; background: #020617; 
                      color: #6ee7b7; padding: 15px; border-left: 5px solid #f97316; border-radius: 5px;}
</style>
""", unsafe_allow_html=True)

# 4. DATABASE LOGIC
def load_data():
    try:
        df = pd.read_csv("sop_data.csv").fillna("")
        # Ensure 'Embedding' column exists
        if "Embedding" not in df.columns:
            df["Embedding"] = ""
        return df
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "Embedding"])

df = load_data()

# 5. CORE FUNCTIONS (Fixed for Searchability)
def embed_text(text, is_query=False):
    """Generates vectors for search. task_type is MANDATORY to prevent crashes."""
    try:
        t_type = "retrieval_query" if is_query else "retrieval_document"
        result = genai.embed_content(model=EMBED_MODEL, content=text[:3000], task_type=t_type)
        return json.dumps(result['embedding'])
    except:
        return ""

def cosine_sim(a, b):
    try:
        if not a or not b: return -1
        vec_a, vec_b = np.array(json.loads(a)), np.array(json.loads(b))
        return np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b) + 1e-10)
    except:
        return -1

# 6. HEADER & NAVIGATION
st.markdown('<div class="main-header"><h2>🏹 ARLEDGE OPERATIONS COMMAND</h2></div>', unsafe_allow_html=True)

nav_cols = st.columns(5)
nav_links = [
    ("CRM", "https://arrowcrm.lightning.force.com/"),
    ("Orders", "https://acswb.arrow.com/Swb/"),
    ("Forms", "https://arrow.etq.com/prod/rel/#/app/system/portal"),
    ("Tickets", "https://arrow.service-now.com/myconnect"),
    ("Help", "mailto:yahya.ouarach@arrow.com")
]
for col, (label, url) in zip(nav_cols, nav_links):
    col.link_button(label, url, use_container_width=True)

st.divider()

# 7. ADMIN PANEL (The Ingestion Engine)
st.sidebar.title("⚙️ Admin Console")
if st.sidebar.checkbox("🚀 Smart AI Upload"):
    pdf_file = st.sidebar.file_uploader("Upload SOP PDF", type="pdf")
    if pdf_file and st.sidebar.button("✨ Process Manual"):
        with st.spinner("AI is digitizing document..."):
            reader = PdfReader(pdf_file)
            raw_text = "".join([p.extract_text() or "" for p in reader.pages])
            
            prompt = f"Extract procedures as CSV. Columns: System, Process, Instructions, Rationale. NO HEADERS. Text: {raw_text[:8000]}"
            response = model.generate_content(prompt)
            
            # Cleaning AI Response
            csv_data = response.text.replace("```csv", "").replace("```", "").strip()
            new_rows = pd.read_csv(io.StringIO(csv_data), names=["System", "Process", "Instructions", "Rationale"], header=None)
            
            st.sidebar.info("Creating search index...")
            new_rows["Embedding"] = (new_rows["System"] + " " + new_rows["Process"]).apply(lambda x: embed_text(x))
            
            df = pd.concat([df, new_rows], ignore_index=True)
            df.to_csv("sop_data.csv", index=False)
            st.sidebar.success("Manual Added to Database!")
            st.rerun()

# 8. THE SEARCH ENGINE
st.markdown('<div class="card"><h3>🔍 SOP Search</h3>', unsafe_allow_html=True)
query = st.text_input("What do you need help with? (e.g. 'How to release price')")
st.markdown('</div>', unsafe_allow_html=True)

if query:
    # Perform Semantic Search
    q_emb = embed_text(query, is_query=True)
    if q_emb:
        df["score"] = df["Embedding"].apply(lambda x: cosine_sim(x, q_emb))
        # Keyword fallback: if score is low, check for keyword match
        df["keyword_match"] = df.apply(lambda x: query.lower() in str(x).lower(), axis=1)
        
        results = df[(df["score"] > 0.3) | (df["keyword_match"])].sort_values(by="score", ascending=False).head(5)
    else:
        # Emergency Keyword Search only if AI is down
        results = df[df.apply(lambda x: query.lower() in str(x).lower(), axis=1)].head(5)

    if not results.empty:
        for _, row in results.iterrows():
            with st.container():
                st.markdown(f"### 📌 {row['System']} | {row['Process']}")
                st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
                
                # Feedback link
                sub = urllib.parse.quote(f"SOP Feedback: {row['Process']}")
                st.link_button("🚩 Report Issue", f"mailto:yahya.ouarach@arrow.com?subject={sub}")
                st.markdown("---")
    else:
        st.warning("No procedures found for that search. Try different keywords.")

# 9. AI COPILOT (RAG)
st.divider()
st.subheader("🧠 Arledge AI Copilot")
user_q = st.text_area("Ask a complex question (requires search context)")
if st.button("Consult AI") and user_q:
    if query: # Uses the results from the search above as context
        context = "\n\n".join([f"Process: {r['Process']}\nInstructions: {r['Instructions']}" for _, r in results.iterrows()])
        full_prompt = f"Answer this using ONLY the context: {user_q}\n\nCONTEXT:\n{context}"
        try:
            ans = model.generate_content(full_prompt)
            st.info(ans.text)
        except:
            st.error("AI is currently unavailable.")
    else:
        st.warning("Please search for a topic first so the AI has context to read.")
