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
    }
    .instructions { 
        background-color: #f8f9fa; 
        padding: 18px; 
        border-left: 6px solid #005a9c; 
        white-space: pre-wrap;
        color: #202124;
    }
    .login-box {
        max-width: 400px;
        margin: 100px auto;
        padding: 30px;
        border: 1px solid #eee;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 2. LOGIN GATEWAY
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.title("🏹 Arledge")
    st.write("Please sign in with your Arrow credentials.")
    user_email = st.text_input("Email Address", placeholder="username@arrow.com")
    if st.button("Sign In"):
        if user_email.lower().endswith("@arrow.com"):
            st.session_state.authenticated = True
            st.session_state.user = user_email
            st.rerun()
        else:
            st.error("Access Restricted. Use your @arrow.com email.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 3. LOAD DATABASE
DB_FILE = "master_ops_database.csv"

@st.cache_data
def load_db():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE).fillna("")
    return pd.DataFrame()

df = load_db()

# 4. SIDEBAR (Only visible after login)
with st.sidebar:
    st.title("Arledge")
    st.write(f"Logged in as: {st.session_state.user}")
    st.divider()
    st.markdown("### Core Tools")
    st.markdown("[🥷 OMT Ninja](https://omt-ninja.arrow.com) | [📋 ETQ Portal](https://etq.arrow.com)")
    st.markdown("[💼 Salesforce](https://arrow.my.salesforce.com) | [☁️ Oracle Unity](https://ebs.arrow.com)")
    
    st.divider()
    with st.expander("🚨 Report Issue"):
        st.text_input("Process Name")
        st.text_area("Details")
        st.button("Submit")

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# 5. MAIN INTERFACE
st.title("Arledge")
query = st.text_input("", placeholder="Search procedures (e.g. 'CoC', 'Price Break', 'PayPal')...")

if query:
    results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="result-card">
                <small style="color:gray; float:right;">Ref: {row['File_Source']}</small>
                <b style="color:#005a9c; text-transform: uppercase;">{row['System']}</b>
                <h2 style="margin-top:5px;">{row['Process']}</h2>
                <div class="instructions"><b>PROCEDURE:</b><br>{row['Instructions']}</div>
                <p style="margin-top:10px;"><i>Rationale: {row['Rationale']}</i></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("No matches found.")
else:
    st.info("Search to begin.")
