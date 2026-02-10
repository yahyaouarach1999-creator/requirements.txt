import streamlit as st
import pandas as pd
import numpy as np
import io
import json
from PyPDF2 import PdfReader
from google import genai

# --------------------------------------------------
# 1. PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# --------------------------------------------------
# 2. GEMINI AI CONFIG (NEW SDK)
# --------------------------------------------------
API_KEY = "AIzaSyA4xwoKlP0iuUtSOkYvpYrADquexHL7YSE"
client = genai.Client(api_key=API_KEY)

CHAT_MODEL = "gemini-1.5-flash"
EMBED_MODEL = "text-embedding-004"

# --------------------------------------------------
# 3. PREMIUM UI
# --------------------------------------------------
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

# --------------------------------------------------
# 4. LOAD DATABASE
# --------------------------------------------------
def load_db():
    try:
        df = pd.read_csv("sop_data.csv")
        if "Embedding" not in df.columns:
            df["Embedding"] = ""
        return df.fillna("")
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "Embedding"])

df = load_db()

# --------------------------------------------------
# 5. EMBEDDINGS (NEW API)
# --------------------------------------------------
def get_embedding(text):
    try:
        response = client.models.embed_content(
            model=EMBED_MODEL,
            contents=text[:3000]
        )
        return json.dumps(response.embeddings[0].values)
    except:
        return ""

# --------------------------------------------------
# 6. HEADER
# --------------------------------------------------
st.markdown('<div class="main-header"><h2>🏹 ARLEDGE OPERATIONS COMMAND CENTER</h2></div>', unsafe_allow_html=True)

# --------------------------------------------------
# 7. ADMIN PDF INGESTION
# --------------------------------------------------
st.sidebar.title("⚙️ SOP Management")

if st.sidebar.checkbox("🚀 Upload SOP PDF"):
    pdf_file = st.sidebar.file_uploader("Upload SOP PDF", type="pdf")

    if pdf_file and st.sidebar.button("✨ Extract & Learn SOP"):
        with st.spinner("AI is extracting procedures..."):
            try:
                reader = PdfReader(pdf_file)
                raw_text = "".join([p.extract_text() or "" for p in reader.pages])

                prompt = f"""
Extract procedures as CSV rows.
Columns: System, Process, Instructions, Rationale.
No headers. Text: {raw_text[:8000]}
"""

                response = client.models.generate_content(
                    model=CHAT_MODEL,
                    contents=prompt
                )

                csv_data = response.text.replace("```csv", "").replace("```", "").strip()

                new_data = pd.read_csv(
                    io.StringIO(csv_data),
                    names=["System", "Process", "Instructions", "Rationale"],
                    header=None
                )

                st.sidebar.info("Generating embeddings...")
                new_data["Embedding"] = new_data.apply(
                    lambda x: get_embedding(f"{x['System']} {x['Process']} {x['Instructions']}"),
                    axis=1
                )

                final_df = pd.concat([df, new_data], ignore_index=True)
                final_df.to_csv("sop_data.csv", index=False)

                st.sidebar.success(f"Added {len(new_data)} SOPs successfully!")
                st.rerun()

            except Exception as e:
                st.sidebar.error(f"Error: {e}")

# --------------------------------------------------
# 8. SEARCH
# --------------------------------------------------
st.subheader("🔍 Intelligent SOP Search")
query = st.text_input("Search technical procedures")

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)

if query and not df.empty:
    q_emb = get_embedding(query)

    def calc_score(row_emb):
        if not row_emb or not q_emb:
            return 0
        a, b = np.array(json.loads(row_emb)), np.array(json.loads(q_emb))
        return cosine_sim(a, b)

    df["score"] = df["Embedding"].apply(calc_score)
    results = df.sort_values("score", ascending=False).head(5)
    results = results[results["score"] > 0.25]

    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"### 📌 {row['System']} | {row['Process']}")
            st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
            st.caption(f"**Rationale:** {row['Rationale']}")
            st.divider()
    else:
        st.warning("No strong matches found.")
else:
    if df.empty:
        st.info("Upload an SOP PDF from the sidebar to build the knowledge base.")
