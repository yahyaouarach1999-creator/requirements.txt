import streamlit as st
import pandas as pd
import numpy as np
import io
import json
from PyPDF2 import PdfReader
import google.generativeai as genai

# --------------------------------------------------
# GEMINI CONFIG (NEW PROJECT / 2026 STABLE)
# --------------------------------------------------
API_KEY = "AIzaSyA4xwoKlP0iuUtSOkYvpYrADquexHL7YSE"
genai.configure(api_key=API_KEY)

# Change: Use 'gemini-flash-latest' instead of 'gemini-1.5-flash'
# This is the industry-standard way to avoid the 404 for new accounts.
MODEL_ID = 'gemini-flash-latest' 
EMBED_MODEL = "models/embedding-001"

# --------------------------------------------------
# HELPER: LIST AVAILABLE MODELS (FOR DEBUGGING)
# --------------------------------------------------
def check_models():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return models
    except:
        return ["Error connecting to API"]

# --------------------------------------------------
# DATA LOGIC
# --------------------------------------------------
def load_db():
    try:
        df = pd.read_csv("sop_data.csv")
        return df.fillna("")
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "Embedding"])

df = load_db()

# --------------------------------------------------
# APP LAYOUT
# --------------------------------------------------
st.title("🏹 Arledge Operational Command")

with st.sidebar:
    st.header("⚙️ System Status")
    available = check_models()
    
    # This will help us see if your key has specific model permissions
    st.write(f"**Connected Model:** {MODEL_ID}")
    with st.expander("Show all permitted models"):
        st.write(available)

    st.divider()
    
    pdf_file = st.file_uploader("Upload New SOP PDF", type="pdf")
    if pdf_file and st.button("🚀 Process SOP"):
        with st.spinner("AI is extracting data..."):
            try:
                reader = PdfReader(pdf_file)
                text = "".join([p.extract_text() for p in reader.pages])
                
                # Re-initialize with the latest alias
                model = genai.GenerativeModel(MODEL_ID)
                prompt = f"Extract procedures as CSV (System, Process, Instructions, Rationale). No header. Text: {text[:8000]}"
                
                response = model.generate_content(prompt)
                
                # Handling empty or blocked responses
                if not response.candidates:
                    st.error("Model failed to generate content. Try a shorter PDF.")
                else:
                    csv_data = response.text.replace("```csv", "").replace("```", "").strip()
                    new_data = pd.read_csv(io.StringIO(csv_data), names=["System", "Process", "Instructions", "Rationale"], header=None)
                    
                    # Embedding logic
                    st.info("Generating Search Vectors...")
                    new_data["Embedding"] = new_data.apply(
                        lambda x: json.dumps(genai.embed_content(model=EMBED_MODEL, content=f"{x['System']} {x['Process']}", task_type="retrieval_document")['embedding']), 
                        axis=1
                    )
                    
                    final_df = pd.concat([df, new_data], ignore_index=True)
                    final_df.to_csv("sop_data.csv", index=False)
                    st.success("Database Rebuilt!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

# --------------------------------------------------
# SEARCH
# --------------------------------------------------
query = st.text_input("🔍 Search Technical Procedures")
if query and not df.empty:
    q_emb = genai.embed_content(model=EMBED_MODEL, content=query, task_type="retrieval_query")['embedding']
    
    def score(row_emb):
        if not row_emb: return 0
        a, b = np.array(json.loads(row_emb)), np.array(q_emb)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)

    df["score"] = df["Embedding"].apply(score)
    results = df.sort_values("score", ascending=False).head(3)
    
    for _, row in results.iterrows():
        st.subheader(f"📌 {row['System']} - {row['Process']}")
        st.info(row['Instructions'])
        st.divider()
