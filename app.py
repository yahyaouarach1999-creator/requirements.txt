import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="OMT Command Center", layout="wide")

# Professional Styling
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .result-card { 
        border: 1px solid #e1e4e8; 
        padding: 20px; 
        border-radius: 8px; 
        background-color: #fcfcfc; 
        margin-bottom: 20px;
    }
    .instructions { 
        background-color: #f1f3f4; 
        padding: 15px; 
        border-left: 5px solid #1a73e8; 
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

# 2. LOAD DATABASE
DB_FILE = "master_ops_database.csv"

@st.cache_data
def load_db():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE).fillna("")
    return pd.DataFrame()

df = load_db()

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("🏹 OMT Tools")
    st.markdown("[🥷 OMT Ninja](https://omt-ninja.arrow.com) | [📋 ETQ Portal](https://etq.arrow.com)")
    st.markdown("[💼 Salesforce](https://arrow.my.salesforce.com) | [☁️ Oracle Unity](https://ebs.arrow.com)")
    if st.button("Clear Cache / Reload Data"):
        st.cache_data.clear()
        st.rerun()

# 4. SEARCH INTERFACE
st.title("Search Procedures")
query = st.text_input("", placeholder="Search by keyword (e.g. 'Delink', 'Reno', 'RMA')...")

# 5. SEARCH LOGIC (Only runs if user types)
if query:
    if not df.empty:
        # This checks every column for the keyword, ignoring uppercase/lowercase
        results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
        
        if not results.empty:
            st.write(f"Showing {len(results)} results:")
            for _, row in results.iterrows():
                st.markdown(f"""
                <div class="result-card">
                    <small style="color:gray; float:right;">Source: {row['File_Source']}</small>
                    <b style="color:#d93025;">{row['System']}</b>
                    <h3>{row['Process']}</h3>
                    <div class="instructions"><b>PROCEDURE STEPS:</b><br>{row['Instructions']}</div>
                    <p style="margin-top:10px;"><i>Rationale: {row['Rationale']}</i></p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error(f"No results found for '{query}'. Please check your spelling.")
    else:
        st.warning("Database file not found. Ensure 'master_ops_database.csv' is in the folder.")
else:
    # Home Page state before searching
    st.info("The Command Center is ready. Enter a keyword above to find the exact steps.")
