import streamlit as st
import pandas as pd
import numpy as np
import io
import os
import urllib.parse
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
# 3. AI CONFIG (USES STREAMLIT SECRET)
# --------------------------------------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

# --------------------------------------------------
# 4. DATA FUNCTIONS
# --------------------------------------------------
@st.cache_data(ttl=3600)
def load_data():
    try:
        return pd.read_csv("sop_data.csv").fillna("")
    except:
        df = pd.DataFrame(columns=["System","Process","Instructions","Rationale","Version","Last_Updated"])
        df.to_csv("sop_data.csv", index=False)
        return df

df = load_data()

def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "".join(page.extract_text() or "" for page in reader.pages)

# --------------------------------------------------
# 5. SIDEBAR METRICS
# --------------------------------------------------
st.sidebar.markdown("### 📊 System Metrics")
st.sidebar.metric("Total SOPs", len(df))
st.sidebar.metric("Systems", df["System"].nunique() if len(df) else 0)
st.sidebar.metric("Processes", df["Process"].nunique() if len(df) else 0)

# --------------------------------------------------
# 6. HEADER
# --------------------------------------------------
st.markdown('<div class="main-header"><h2>🏹 ARLEDGE OPERATIONS COMMAND CENTER</h2></div>', unsafe_allow_html=True)

# --------------------------------------------------
# 7. NAVIGATION LINKS
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
# 8. ADMIN AI PDF INGESTION
# --------------------------------------------------
st.sidebar.title("⚙️ Admin Console")
if st.sidebar.checkbox("🚀 Smart AI SOP Upload"):
    pdf = st.sidebar.file_uploader("Upload SOP PDF", type="pdf")
    if pdf and st.sidebar.button("✨ Extract Procedures"):
        with st.spinner("AI is analyzing the document..."):
            try:
                raw_text = extract_pdf_text(pdf)
                prompt = f"""Extract SOP steps into CSV rows.
Columns: System, Process, Instructions, Rationale.
TEXT: {raw_text[:8000]}"""
                response = model.generate_content(prompt)
                cleaned = response.text.replace("```csv","").replace("```","").strip()
                new_rows = pd.read_csv(io.StringIO(cleaned), names=["System","Process","Instructions","Rationale"])
                new_rows["Version"] = 1
                new_rows["Last_Updated"] = datetime.now()
                df_updated = pd.concat([df, new_rows], ignore_index=True)
                df_updated.to_csv("sop_data.csv", index=False)
                st.sidebar.success(f"Added {len(new_rows)} SOPs")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.sidebar.error("AI processing failed")
                st.sidebar.exception(e)

# --------------------------------------------------
# 9. SAFE EMBEDDINGS
# --------------------------------------------------
def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

@st.cache_resource(show_spinner=False)
def embed_single(text):
    try:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text[:3000]
        )
        return result["embedding"]
    except:
        return None

def build_embeddings(data):
    texts = data["Instructions"].fillna("").tolist()
    return [embed_single(t) for t in texts]

if "embeddings" not in st.session_state and len(df) > 0:
    with st.spinner("Preparing AI search index..."):
        st.session_state.embeddings = build_embeddings(df)

# --------------------------------------------------
# 10. SEMANTIC SEARCH
# --------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🔍 Intelligent SOP Search")
query = st.text_input("Search procedures in plain English")
st.markdown('</div>', unsafe_allow_html=True)

results = pd.DataFrame()

if query and len(df) > 0 and "embeddings" in st.session_state:
    try:
        q_embed = genai.embed_content(model="models/embedding-001", content=query)["embedding"]
        scores = []
        for e in st.session_state.embeddings:
            if e is None:
                scores.append(-1)
            else:
                scores.append(cosine_sim(e, q_embed))
        df["score"] = scores
        results = df.sort_values("score", ascending=False).head(5)
    except Exception as e:
        st.error("Search temporarily unavailable")
        st.exception(e)

for _, row in results.iterrows():
    st.markdown(f"### 📌 {row['System']} | {row['Process']}")
    st.caption(f"**Rationale:** {row['Rationale']}")
    st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)

    subject = urllib.parse.quote(f"SOP
