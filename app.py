import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# Professional Styling
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .result-card { 
        border: 1px solid #e1e4e8; 
        padding: 24px; 
        border-radius: 10px; 
        background-color: #fcfcfc; 
        margin-bottom: 25px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .instructions { 
        background-color: #f8f9fa; 
        padding: 18px; 
        border-left: 6px solid #005a9c; 
        white-space: pre-wrap;
        color: #202124;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .admin-label {
        color: #d93025;
        font-weight: bold;
        font-size: 0.8rem;
        letter-spacing: 1px;
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
    st.title("🏹 Arledge Tools")
    st.markdown("### Quick Access")
    st.markdown("[🥷 OMT Ninja](https://omt-ninja.arrow.com) | [📋 ETQ Portal](https://etq.arrow.com)")
    st.markdown("[💼 Salesforce](https://arrow.my.salesforce.com) | [☁️ Oracle Unity](https://ebs.arrow.com)")
    
    st.divider()
    
    # REPORT ISSUE
    with st.expander("🚨 Report Issue"):
        st.text_input("Process Name")
        st.text_area("What is incorrect?")
        if st.button("Submit to Admin"):
            st.toast("Report sent successfully")

    st.divider()

    # ADMIN ACCESS
    with st.expander("🔐 Admin Access"):
        email = st.text_input("Arrow Email", key="admin_mail")
        if email.lower().endswith("@arrow.com"):
            st.markdown('<p class="admin-label">AUTHORIZED ACCESS</p>', unsafe_allow_html=True)
            if st.button("Reload Master CSV"):
                st.cache_data.clear()
                st.rerun()
            st.write(f"Total Database Records: {len(df)}")
        elif email:
            st.warning("Arrow credentials required.")

# 4. MAIN INTERFACE
st.title("Arledge")
st.caption("Arrow Knowledge Center | Operations Support")
query = st.text_input("", placeholder="Search procedures, systems, or keywords (e.g. 'Reno', 'Delink', 'DID')...")

# 5. SEARCH LOGIC
if query:
    if not df.empty:
        results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
        
        if not results.empty:
            st.write(f"Results for '{query}':")
            for _, row in results.iterrows():
                st.markdown(f"""
                <div class="result-card">
                    <small style="color:gray; float:right;">Source: {row['File_Source']}</small>
                    <b style="color:#005a9c; text-transform: uppercase; font-size:0.8rem;">{row['System']}</b>
                    <h2 style="margin-top:5px; border-bottom: 1px solid #eee; padding-bottom:10px;">{row['Process']}</h2>
                    <div class="instructions"><b>STEP-BY-STEP GUIDANCE:</b><br>{row['Instructions']}</div>
                    <p style="margin-top:10px;"><b>Rationale:</b> {row['Rationale']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("No matching processes found. Please check your keywords.")
    else:
        st.warning("Database not found. Please upload 'master_ops_database.csv'.")
else:
    st.info("System Ready. Please enter a search term above to begin.")
