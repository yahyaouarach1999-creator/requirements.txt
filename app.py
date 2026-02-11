import streamlit as st
import pandas as pd
import os

# 1. SETUP
st.set_page_config(page_title="Arledge OMT Command", layout="wide", page_icon="🏹")

# Professional Styles
st.markdown("""
<style>
    .sop-card { border: 1px solid #e1e4e8; padding: 20px; border-radius: 8px; background-color: #ffffff; margin-bottom: 20px; }
    .step-box { background-color: #f1f3f4; border-left: 5px solid #1a73e8; padding: 15px; margin: 10px 0; white-space: pre-wrap; color: #202124; }
    .system-label { color: #d93025; font-weight: bold; text-transform: uppercase; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# 2. LOAD DATA
DB_FILE = "master_ops_database.csv"

def get_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE).fillna("")
        # Clean the data to ensure search works
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df
    return pd.DataFrame()

df = get_data()

# 3. SIDEBAR LINKS
with st.sidebar:
    st.title("🏹 Tool Links")
    st.markdown("[🥷 OMT Ninja](https://omt-ninja.arrow.com) | [📋 ETQ Portal](https://etq.arrow.com)")
    st.markdown("[💼 Salesforce](https://arrow.my.salesforce.com) | [☁️ Oracle Unity](https://ebs.arrow.com)")
    st.divider()
    if st.button("Refresh Database"): st.rerun()

# 4. SEARCH INTERFACE
st.title("Operational Procedures Search")
query = st.text_input("", placeholder="Search e.g. 'Delink', 'Sure Ship', 'BOM'...")

# 5. SEARCH RESULTS
if query:
    if not df.empty:
        # Case-insensitive search across ALL columns
        mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
        results = df[mask]
        
        if not results.empty:
            st.write(f"Found {len(results)} procedures:")
            for _, row in results.iterrows():
                st.markdown(f"""
                <div class="sop-card">
                    <span style="float:right; font-size:0.7rem; color:grey;">{row['File_Source']}</span>
                    <span class="system-label">{row['System']}</span>
                    <h2>{row['Process']}</h2>
                    <div class="step-box"><strong>INSTRUCTIONS:</strong><br>{row['Instructions']}</div>
                    <p><strong>Rationale:</strong> {row['Rationale']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error(f"No results found for '{query}'. Try a simpler keyword.")
    else:
        st.warning("Database file not found. Please ensure 'master_ops_database.csv' is in your project folder.")
else:
    st.info("System Ready. Please type a keyword to see the full procedure.")
