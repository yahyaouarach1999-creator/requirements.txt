import streamlit as st
import pandas as pd
import google.generativeai as genai
from PyPDF2 import PdfReader
import io

# --- 1. DATA LOADING ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv("sop_data.csv").fillna("")
    except:
        # Create a blank file if it's missing to prevent errors
        blank_df = pd.DataFrame(columns=["System", "Process", "Instructions", "Rationale"])
        blank_df.to_csv("sop_data.csv", index=False)
        return blank_df

# Define function to read PDF text
def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Load initial data
df = load_data()

# --- 2. AI SETUP ---
try:
    API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = None

# --- 3. ADMIN SIDEBAR LOGIC ---
st.sidebar.title("⚙️ Admin Settings")

if st.sidebar.checkbox("🚀 Smart Admin Upload"):
    if model:
        st.sidebar.subheader("AI PDF Trainer")
        new_pdf = st.sidebar.file_uploader("Upload a PDF SOP", type="pdf")
        
        if new_pdf and st.sidebar.button("✨ Extract & Add to Database"):
            with st.sidebar.status("AI is reading and formatting..."):
                # A. Convert PDF to Text
                pdf_text = extract_pdf_text(new_pdf)
                
                # B. Send to Gemini
                prompt = f"""
                Act as a technical writer. Extract procedures from the text below. 
                Return ONLY valid CSV lines (no header, no markdown code blocks).
                Columns: System, Process, Instructions, Rationale.
                Text to process: {pdf_text[:10000]}
                """
                response = model.generate_content(prompt)
                
                # C. Convert AI response to Dataframe
                try:
                    # We wrap the text in a StringIO so pandas can read it like a file
                    new_rows = pd.read_csv(
                        io.StringIO(response.text), 
                        names=["System", "Process", "Instructions", "Rationale"],
                        header=None
                    )
                    
                    # D. Update CSV File
                    updated_df = pd.concat([df, new_rows], ignore_index=True)
                    updated_df.to_csv("sop_data.csv", index=False)
                    
                    st.sidebar.success(f"Added {len(new_rows)} new procedures!")
                    st.cache_data.clear() # Forces the search bar to see new data
                    st.rerun()
                except Exception as e:
                    st.sidebar.error("AI output was messy. Try a cleaner PDF.")
    else:
        st.sidebar.error("⚠️ Gemini API Key missing in Secrets!")

# --- 4. MAIN SEARCH ENGINE (Displaying your data) ---
st.title("🏹 Arledge Operations Command")
query = st.text_input("🔍 Search procedures...", placeholder="e.g. Price Release, V72, OMT")

if query:
    # Search across all columns
    results = df[df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)]
    
    if not results.empty:
        for idx, row in results.iterrows():
            with st.expander(f"📌 {row['System']} | {row['Process']}"):
                st.info(f"**Rationale:** {row['Rationale']}")
                st.markdown(f"**Step-by-Step Instructions:**\n{row['Instructions']}")
    else:
        st.warning("No matches found in the database.")
