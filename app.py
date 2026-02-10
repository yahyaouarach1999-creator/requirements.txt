import streamlit as st
import pandas as pd
import numpy as np
import io
import json
from PyPDF2 import PdfReader
import google.generativeai as genai

# --------------------------------------------------
# CONFIG & THEME
# --------------------------------------------------
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

st.markdown("""
<style>
    .stApp {background: linear-gradient(135deg, #0f172a, #1e293b); color: #f1f5f9;}
    .card {background: rgba(255,255,255,0.05); border-radius: 14px; padding: 18px; margin-bottom: 14px; border: 1px solid rgba(255,255,255,0.1);}
    .main-header {text-align:center; padding:12px; border-bottom:2px solid #f97316; margin-bottom:20px;}
    .instruction-box {white-space: pre-wrap; font-family: monospace; background: #0b1220; color: #f8fafc; padding: 15px; border-left: 4px solid #f97316; border-radius: 6px;}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# AI INITIALIZATION (STABLE v1 ROUTE)
# --------------------------------------------------
API_KEY = "AIzaSyA4xwoKlP0iuUtSOkYvpYrADquexHL7YSE"
genai.configure(api_key=API_KEY)

# Use the short name 'gemini-1.5-flash' to force the SDK to use the stable v1 path
MODEL_ID = 'gemini-1.5-flash' 
EMBED_MODEL = "models/embedding-001"

# Initialize model globally
model = genai.GenerativeModel(MODEL_ID)

# --------------------------------------------------
# DATABASE & DATA HANDLING
# --------------------------------------------------
def load_db():
    try:
        df = pd.read_csv("sop_data.csv")
        if "Embedding" not in df.columns:
            df["Embedding"] = ""
        return df.fillna("")
    except:
        # Returns empty structure if sop_data.csv was deleted
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "Embedding"])

def get_embedding(text, task="retrieval_document"):
    try:
        res = genai.embed_content(model=EMBED_MODEL, content=text[:3000], task_type=task)
        return json.dumps(res['embedding'])
    except:
        return ""

# --------------------------------------------------
# MAIN INTERFACE
# --------------------------------------------------
st.markdown('<div class="main-header"><h2>🏹 ARLEDGE OPERATIONS COMMAND</h2></div>', unsafe_allow_html=True)

df = load_db()

# SIDEBAR: MANAGEMENT
with st.sidebar:
    st.header("⚙️ Admin Console")
    st.info(f"Model: {MODEL_ID} (Stable)")
    
    uploaded_file = st.file_uploader("Upload SOP PDF", type="pdf")
    
    if uploaded_file and st.button("✨ Implement & Index SOP"):
        with st.spinner("AI is analyzing and building search vectors..."):
            try:
                # 1. Read PDF
                reader = PdfReader(uploaded_file)
                raw_text = "".join([p.extract_text() or "" for p in reader.pages])

                # 2. AI Extraction
                prompt = f"""
                Extract the technical procedures from this text as a CSV format.
                Columns: System, Process, Instructions, Rationale.
                Provide ONLY the raw CSV text. No headers, no markdown blocks.
                Text: {raw_text[:12000]}
                """
                
                response = model.generate_content(prompt)
                
                if response.text:
                    csv_data = response.text.replace("```csv", "").replace("```", "").strip()
                    new_rows = pd.read_csv(io.StringIO(csv_data), 
                                           names=["System", "Process", "Instructions", "Rationale"], 
                                           header=None)
                    
                    # 3. Embedding Generation (Instant Indexing)
                    new_rows["Embedding"] = new_rows.apply(
                        lambda x: get_embedding(f"{x['System']} {x['Process']}"), axis=1
                    )
                    
                    # 4. Save
                    df = pd.concat([df, new_rows], ignore_index=True)
                    df.to_csv("sop_data.csv", index=False)
                    st.success("SOP Implemented Successfully!")
                    st.rerun()
                else:
                    st.error("AI returned an empty response. Check API Quota.")
            except Exception as e:
                st.error(f"Processing Error: {str(e)}")

# MAIN PANEL: SEARCH
st.subheader("🔍 Intelligent Search")
query = st.text_input("Enter keywords (e.g., 'Collector Setup', 'Oracle Orders')")

if query and not df.empty:
    try:
        # Embed Query
        q_res = genai.embed_content(model=EMBED_MODEL, content=query, task_type="retrieval_query")
        q_emb = np.array(q_res['embedding'])

        def calculate_similarity(row_emb):
            if not row_emb: return 0
            a = np.array(json.loads(row_emb))
            return np.dot(a, q_emb) / (np.linalg.norm(a) * np.linalg.norm(q_emb) + 1e-10)

        df["score"] = df["Embedding"].apply(calculate_similarity)
        results = df.sort_values("score", ascending=False).head(5)
        results = results[results["score"] > 0.25] # Match threshold

        if not results.empty:
            for _, row in results.iterrows():
                st.markdown(f"""
                <div class="card">
                    <h3>📌 {row['System']} | {row['Process']}</h3>
                    <div class="instruction-box">{row['Instructions']}</div>
                    <p style='color: #94a3b8; font-size: 0.85rem; margin-top: 10px;'>
                        <b>Rationale:</b> {row['Rationale']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No relevant procedures found. Try different keywords.")
    except Exception as e:
        st.error(f"Search Error: {e}")
elif not query:
    if df.empty:
        st.info("The database is empty. Please upload an SOP PDF in the sidebar to begin.")
    else:
        st.caption("Enter a query above to search the SOP database.")
