import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
from PyPDF2 import PdfReader
import io
import urllib.parse

# --- 1. SETTINGS & AI CONFIG ---
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# Using your provided key
API_KEY = "AIzaSyAFHZDDmcowqD_9TVZBqYSe9LgP-KSXQII" 

try:
    genai.configure(api_key=API_KEY)
    # Models for Generation and Embedding
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    EMBED_MODEL = "models/embedding-001"
except Exception as e:
    st.error(f"AI Initialization Error: {e}")
    model = None

# --- 2. HELPER FUNCTIONS ---

def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "".join([page.extract_text() or "" for page in reader.pages])

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("sop_data.csv").fillna("")
        # Ensure required columns exist
        for col in ["System", "Process", "Instructions", "Rationale"]:
            if col not in df.columns:
                df[col] = ""
        return df
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale"])

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)

@st.cache_resource(show_spinner=False)
def get_embeddings(text_list):
    """Fetches embeddings for a batch of text."""
    try:
        result = genai.embed_content(
            model=EMBED_MODEL,
            content=text_list,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        return []

# --- 3. STYLING ---
st.markdown("""
    <style>
        .main-header { background-color: #0F172A; padding: 10px; color: white; text-align: center; border-bottom: 3px solid #F97316; margin-bottom: 15px; }
        .nano-tile { background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; text-align: center; padding: 5px; }
        .nano-label { font-size: 0.6rem; font-weight: 900; color: #64748B; text-transform: uppercase; }
        .instruction-box { white-space: pre-wrap; font-family: monospace; background: #1E293B; color: #F8FAFC; padding: 15px; border-left: 5px solid #F97316; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. DATA INITIALIZATION ---
df = load_data()

# --- 5. AUTHENTICATION ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.markdown('<div class="main-header"><h4>🔒 ARROW.COM ACCESS REQUIRED</h4></div>', unsafe_allow_html=True)
    user_email = st.text_input("Official Email:")
    if st.button("Enter Portal"):
        if "@arrow.com" in user_email.lower():
            st.session_state['auth'] = True
            st.rerun()
        else:
            st.error("Denied.")
    st.stop()

# --- 6. MAIN APP CONTENT ---
st.markdown('<div class="main-header"><h4>🏹 ARLEDGE OPERATIONS COMMAND</h4></div>', unsafe_allow_html=True)

# Navigation Tiles
cols = st.columns(5)
links = [
    ("Salesforce", "🚀 CRM", "https://arrowcrm.lightning.force.com/"),
    ("SWB Oracle", "💾 Orders", "https://acswb.arrow.com/Swb/"),
    ("ETQ Portal", "📋 Forms", "https://arrow.etq.com/prod/rel/#/app/system/portal"),
    ("Support", "🛠️ Tickets", "https://arrow.service-now.com/myconnect"),
    ("SOS Help", "🆘 Contact", "mailto:yahya.ouarach@arrow.com")
]
for i, (label, btn_text, url) in enumerate(links):
    with cols[i]:
        st.markdown(f'<div class="nano-tile"><div class="nano-label">{label}</div></div>', unsafe_allow_html=True)
        st.link_button(btn_text, url, use_container_width=True)

st.divider()

# --- 7. ADMIN SIDEBAR (Smart Upload) ---
st.sidebar.title("⚙️ Admin Console")
if st.sidebar.checkbox("🚀 Smart AI Upload"):
    uploaded_pdf = st.sidebar.file_uploader("Upload SOP PDF", type="pdf")
    if uploaded_pdf and st.sidebar.button("✨ Extract & Learn"):
        with st.spinner("AI is digitizing manual..."):
            raw_text = extract_pdf_text(uploaded_pdf)
            prompt = f"Extract procedures as CSV (no header). Columns: System, Process, Instructions, Rationale. Text: {raw_text[:10000]}"
            response = model.generate_content(prompt)
            
            cleaned_csv = response.text.replace('```csv', '').replace('```', '').strip()
            new_data = pd.read_csv(io.StringIO(cleaned_csv), names=["System", "Process", "Instructions", "Rationale"])
            
            # Combine and Save
            final_df = pd.concat([df, new_data], ignore_index=True)
            final_df.to_csv("sop_data.csv", index=False)
            st.sidebar.success("Database Updated!")
            st.cache_data.clear()
            st.rerun()

# --- 8. SEARCH ENGINE (Vector + Keyword) ---
query = st.text_input("🔍 Search Technical Procedures", placeholder="e.g. 'How to release price' or 'V72 process'")

if query:
    # 1. Keyword Search (Fast)
    keyword_results = df[df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)]
    
    # 2. Vector Search (Semantic) - This finds results based on MEANING
    with st.spinner("Searching context..."):
        try:
            # Embed the search query
            query_embedding = genai.embed_content(
                model=EMBED_MODEL,
                content=query,
                task_type="retrieval_query"
            )['embedding']
            
            # Embed the database instructions (batched)
            doc_texts = (df["System"] + " " + df["Process"] + " " + df["Instructions"]).tolist()
            doc_embeddings = get_embeddings(doc_texts)
            
            if doc_embeddings:
                # Calculate similarities
                scores = [cosine_similarity(query_embedding, doc_emb) for doc_emb in doc_embeddings]
                df["score"] = scores
                vector_results = df[df["score"] > 0.4].sort_values(by="score", ascending=False)
                
                # Combine results
                final_results = pd.concat([keyword_results, vector_results]).drop_duplicates(subset=["Process"])
            else:
                final_results = keyword_results
        except:
            final_results = keyword_results

    # 3. Display Results
    if not final_results.empty:
        for _, row in final_results.iterrows():
            with st.expander(f"📌 {row['System']} | {row['Process']}"):
                st.caption(f"**Rationale:** {row['Rationale']}")
                st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
                
                # Report Issue Email
                sub = urllib.parse.quote(f"SOP Feedback: {row['Process']}")
                mailto = f"mailto:yahya.ouarach@arrow.com?subject={sub}"
                st.link_button("🚩 Report Issue", mailto)
    else:
        st.warning("No procedures found.")
