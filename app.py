import streamlit as st
import pandas as pd
import numpy as np
import io
import json
from PyPDF2 import PdfReader
import google.generativeai as genai

# 1. AI CONFIG (The 404 Fix)
API_KEY = "AIzaSyA4xwoKlP0iuUtSOkYvpYrADquexHL7YSE"
genai.configure(api_key=API_KEY)

# Use the direct model name. The SDK handles the pathing.
MODEL_ID = 'gemini-1.5-flash'
EMBED_MODEL = "models/embedding-001"

# 2. DATA LOADING (Handles the "Clean Slate" you mentioned)
def load_db():
    try:
        df = pd.read_csv("sop_data.csv")
        if "Embedding" not in df.columns: df["Embedding"] = ""
        return df.fillna("")
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale", "Embedding"])

# 3. PDF PROCESSING LOGIC
def process_pdf(pdf_file, current_df):
    reader = PdfReader(pdf_file)
    raw_text = "".join([p.extract_text() or "" for p in reader.pages])

    # Initialize the model using the stable v1 path
    model = genai.GenerativeModel(MODEL_ID)
    
    prompt = f"""
    Extract technical procedures from this text as CSV rows.
    Columns: System, Process, Instructions, Rationale.
    NO headers, NO markdown backticks.
    Text: {raw_text[:8000]}
    """
    
    # generate_content is the correct method for Gemini models
    response = model.generate_content(prompt)
    
    # Clean the output in case AI adds markdown
    csv_data = response.text.replace("```csv", "").replace("```", "").strip()
    
    new_rows = pd.read_csv(io.StringIO(csv_data), 
                           names=["System", "Process", "Instructions", "Rationale"], 
                           header=None)
    
    # Immediate Embedding for Search
    st.info("Indexing for search...")
    new_rows["Embedding"] = new_rows.apply(
        lambda x: json.dumps(genai.embed_content(
            model=EMBED_MODEL, 
            content=f"{x['System']} {x['Process']}", 
            task_type="retrieval_document"
        )['embedding']), axis=1
    )
    
    return pd.concat([current_df, new_rows], ignore_index=True)

# 4. APP INTERFACE
st.title("🏹 Arledge Operations Command")

df = load_db()

with st.sidebar:
    st.header("⚙️ Admin")
    uploaded_file = st.file_uploader("Upload SOP PDF", type="pdf")
    if uploaded_file and st.button("Implement SOP"):
        df = process_pdf(uploaded_file, df)
        df.to_csv("sop_data.csv", index=False)
        st.success("SOP Added!")
        st.rerun()

# 5. SEARCH LOGIC
query = st.text_input("🔍 Search Procedures")
if query and not df.empty:
    # Embed search query
    q_emb = genai.embed_content(model=EMBED_MODEL, content=query, task_type="retrieval_query")['embedding']
    
    def get_sim(row_emb):
        if not row_emb: return 0
        a, b = np.array(json.loads(row_emb)), np.array(q_emb)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)

    df["score"] = df["Embedding"].apply(get_sim)
    results = df.sort_values("score", ascending=False).head(3)
    
    for _, row in results.iterrows():
        with st.container():
            st.markdown(f"### 📌 {row['System']} | {row['Process']}")
            st.code(row['Instructions'])
            st.divider()
