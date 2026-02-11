import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge Arrow Knowledge Center", layout="wide", page_icon="🏹")

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
        box-shadow: 2px 2px 5px rgba(0,0,0,0.03);
    }
    .instructions { 
        background-color: #f8f9fa; 
        padding: 15px; 
        border-left: 5px solid #005a9c; 
        white-space: pre-wrap;
        color: #333;
    }
    .admin-box {
        background-color: #fff4f4;
        padding: 15px;
        border: 1px dashed #d93025;
        border-radius: 5px;
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
    st.title("🏹 OMT Resources")
    st.markdown("### Core Portals")
    st.markdown("[🥷 OMT Ninja](https://omt-ninja.arrow.com) | [📋 ETQ Portal](https://etq.arrow.com)")
    st.markdown("[💼 Salesforce](https://arrow.my.salesforce.com) | [☁️ Oracle Unity](https://ebs.arrow.com)")
    
    st.divider()
    
    # REPORT ISSUE SECTION
    with st.expander("🚨 Report an Issue"):
        issue_type = st.selectbox("Type", ["Data Incorrect", "System Bug", "Missing Process"])
        details = st.text_area("Details")
        if st.button("Submit Report"):
            st.success("Issue logged. Management will review.")

    st.divider()

    # ADMIN ACCESS SECTION
    with st.expander("🔐 Admin Access"):
        admin_email = st.text_input("Arrow Email", placeholder="user@arrow.com")
        if admin_email.lower().endswith("@arrow.com"):
            st.markdown('<div class="admin-box"><b>Admin Mode Active</b></div>', unsafe_allow_html=True)
            if st.button("Clear Cache / Sync Data"):
                st.cache_data.clear()
                st.rerun()
            st.write("Current Database Rows:", len(df))
        elif admin_email:
            st.error("Access restricted to Arrow employees.")

# 4. MAIN INTERFACE
st.title("Arledge Arrow Knowledge Center")
query = st.text_input("", placeholder="Search by keyword (e.g. 'Delink', 'Reno', 'RMA')...")

# 5. SEARCH LOGIC
if query:
    if not df.empty:
        # Searches across all columns for the keyword
        results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
        
        if not results.empty:
            st.write(f"Showing {len(results)} results:")
            for _, row in results.iterrows():
                st.markdown(f"""
                <div class="result-card">
                    <small style="color:gray; float:right;">Ref: {row['File_Source']}</small>
                    <b style="color:#005a9c;">{row['System']}</b>
                    <h3 style="margin-top:0px;">{row['Process']}</h3>
                    <div class="instructions"><b>PROCEDURE:</b><br>{row['Instructions']}</div>
                    <p style="margin-top:10px; font-size:0.9rem;"><i>Rationale: {row['Rationale']}</i></p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error(f"No results found for '{query}'. Please try another keyword.")
    else:
        st.warning("Knowledge base is currently empty.")
else:
    st.info("Welcome to the Arledge Command Center. Enter a keyword above to view internal procedures.")
