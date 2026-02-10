import streamlit as st
import pandas as pd
import numpy as np
import io
import os
import yaml
import urllib.parse
from datetime import datetime
from PyPDF2 import PdfReader
import google.generativeai as genai
import streamlit_authenticator as stauth

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
# 3. AUTHENTICATION (FIXED FOR NEW VERSION)
# --------------------------------------------------
with open("users.yaml") as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login(location="main")

if st.session_state["authentication_status"] is False:
    st.error("Invalid username or password")
    st.stop()
elif st.session_state["authentication_status"] is None:
    st.warning("Please enter your credentials")
    st.stop()

name = st.session_state["name"]
username = st.session_state["username"]

authenticator.logout(location="sidebar")
st.sidebar.success(f"Welcome {name}")

# --------------------------------------------------
# 4. AI CONFIG (SECURE)
# --------------------------------------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

# --------------------------------------------------
# 5. DATA FUNCTIONS
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
# 6. SIDEBAR DASHBOARD
# --------------------------------------------------
st.sidebar.markdown("### 📊 System Metrics")
st.sidebar.metric("Total SOPs", len(df))
st.sidebar.metric("Systems", df["System"].nunique())
st.sidebar.metric("Processes", df["Process"].nunique())

# --------------------------------------------------
# 7. HEADER
# --------------------------------------------------
st.markdown('<div class="main-header"><h2>🏹 ARLEDGE OPERATIONS COMMAND CENTER</h2></div>', unsafe_allow_html=True)

# --------------------------------------------------
# 8. NAVIGATION
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
# 9. ADMIN AI PDF INGESTION
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
# 10. SEMANTIC SEARCH
# --------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🔍 Intelligent SOP Search")
query = st.text_input("Search procedures in plain English")
st.markdown('</div>', unsafe_allow_html=True)

def cosine_sim(a,b): return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

@st.cache_resource
def embed_texts(texts):
    return [genai.embed_content(model="models/embedding-001", content=t)["embedding"] for t in texts]

if "embeddings" not in st.session_state and len(df) > 0:
    st.session_state.embeddings = embed_texts(df["Instructions"].tolist())

results = pd.DataFrame()

if query and len(df) > 0:
    q_embed = genai.embed_content(model="models/embedding-001", content=query)["embedding"]
    scores = [cosine_sim(e, q_embed) for e in st.session_state.embeddings]
    df["score"] = scores
    results = df.sort_values("score", ascending=False).head(5)

for _, row in results.iterrows():
    st.markdown(f"### 📌 {row['System']} | {row['Process']}")
    st.caption(f"**Rationale:** {row['Rationale']}")
    st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)

    subject = urllib.parse.quote(f"SOP Issue Report: {row['Process']}")
    body = urllib.parse.quote(f"Issue with procedure:\nSystem: {row['System']}\nProcess: {row['Process']}")
    st.link_button("🚩 Report Issue", f"mailto:yahya.ouarach@arrow.com?subject={subject}&body={body}")
    st.markdown("---")

# --------------------------------------------------
# 11. AI COPILOT
# --------------------------------------------------
st.divider()
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🧠 Arledge AI Copilot")

question = st.text_area("Ask an operational question")

if st.button("Get AI Guidance") and question:
    with st.spinner("Consulting operations intelligence..."):
        context = "\n\n".join(results["Instructions"].tolist())
        prompt = f"""Answer using ONLY this SOP data:\n{context}\nQUESTION: {question}"""
        try:
            answer = model.generate_content(prompt)
            st.write(answer.text)
        except Exception as e:
            st.error("AI system unavailable")
            st.exception(e)

st.markdown('</div>', unsafe_allow_html=True)
