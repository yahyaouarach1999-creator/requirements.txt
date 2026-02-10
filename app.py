import streamlit as st
import pandas as pd
import numpy as np
import io
import json
from PyPDF2 import PdfReader
import google.generativeai as genai

# --------------------------------------------------
# 1. PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# --------------------------------------------------
# 2. 🔑 PUT YOUR API KEY HERE
# --------------------------------------------------
API_KEY = "AIzaSyBPDKoUXeysMOQeex1_LBLXwL8IM7ZPCH0"
genai.configure(api_key=API_KEY)

MODEL_ID = "gemini-1.0-pro"
EMBED_MODEL = "models/embedding-001"
model = genai.GenerativeModel(MODEL_ID)

# --------------------------------------------------
# 3. UI STYLE
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
# 4. DATABASE
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
# 5. EMBEDDING FUNCTION
# --------------------------------------------------
def get_embedding(text, is_query=False):
    try:
        task = "retrieval_query" if is_query else "retrieval_document"
        res = genai.embed_content(
            model=EMBED_MODEL,
            content=text[:3000],
            task_type=task
        )
        return json.dumps(res["embedding"])
    except:
        return ""

# --------------------------------------------------
# 6. HEADER
# --------------------------------------------------
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

# --------------------------------------------------
# 7. ADMIN UPLOAD
# --------------------------------------------------
st.sidebar.title("⚙️ Management")
if st.sidebar.checkbox("🚀 Implement New SOP"):
    pdf_file = st.sidebar.file_uploader("Upload SOP PDF", type="pdf")
    if pdf_file and st.sidebar.button("✨ Extract & Learn"):
        with st.spinner("AI is analyzing..."):
            try:
                reader = PdfReader(pdf_file)
                raw_text = "".join([p.extract_text() or "" for p in reader.pages])

                prompt = f"Extract procedures as CSV. Columns: System, Process, Instructions, Rationale. NO headers. Text: {raw_text[:8000]}"
                response = model.generate_content(prompt)

                csv_data = response.text.replace("```csv", "").replace("```", "").strip()
                new_data = pd.read_csv(io.StringIO(csv_data),
                                       names=["System", "Process", "Instructions", "Rationale"],
                                       header=None)

                st.sidebar.info("Building AI search index...")
                new_data["Embedding"] = new_data.apply(
                    lambda x: get_embedding(f"{x['System']} {x['Process']} {x['Instructions']}"),
                    axis=1
                )

                final_df = pd.concat([df, new_data], ignore_index=True)
                final_df.to_csv("sop_data.csv", index=False)

                st.sidebar.success("Database Updated!")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

# --------------------------------------------------
# 8. SEARCH
# --------------------------------------------------
query = st.text_input("🔍 Search Technical Procedures")

if query and not df.empty:
    q_emb = get_embedding(query, is_query=True)

    def calculate_sim(row_emb):
        if not row_emb or not q_emb:
            return 0
        a, b = np.array(json.loads(row_emb)), np.array(json.loads(q_emb))
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)

    df["score"] = df["Embedding"].apply(calculate_sim)
    results = df.sort_values(by="score", ascending=False).head(5)
    results = results[results["score"] > 0.2]

    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"### 📌 {row['System']} | {row['Process']}")
            st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
            st.divider()
    else:
        st.warning("No matches found.")

elif not query and df.empty:
    st.info("Upload an SOP in the sidebar to build the knowledge base.")
