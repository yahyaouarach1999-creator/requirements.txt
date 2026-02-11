import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# Professional Styling
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .login-container { max-width: 450px; margin: 100px auto; padding: 40px; border-radius: 12px; border: 1px solid #e1e4e8; background: #fcfcfc; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .result-card { border: 1px solid #e1e4e8; padding: 24px; border-radius: 10px; background-color: #fcfcfc; margin-bottom: 25px; }
    .instructions { background-color: #f8f9fa; padding: 18px; border-left: 6px solid #005a9c; white-space: pre-wrap; color: #202124; line-height: 1.6; }
    .system-badge { background-color: #005a9c; color: white; padding: 4px 12px; border-radius: 4px; font-size: 0.75rem; text-transform: uppercase; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 2. ACCESS CONTROL (LOGIN)
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.title("🏹 Arledge")
    st.write("Secure Access Required")
    user_email = st.text_input("Arrow Email Address", placeholder="e.g. jdoe@arrow.com")
    if st.button("Enter Arledge"):
        if user_email.lower().endswith("@arrow.com"):
            st.session_state.auth = True
            st.session_state.user = user_email
            st.rerun()
        else:
            st.error("Invalid Domain. Access restricted to Arrow Electronics employees.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 3. DATA LOADING
DB_FILE = "master_ops_database.csv"
@st.cache_data
def load_db():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE).fillna("")
    return pd.DataFrame()

df = load_db()

# 4. SIDEBAR
with st.sidebar:
    st.title("Arledge")
    st.caption(f"User: {st.session_state.user}")
    st.divider()
    st.markdown("### Portals")
    st.markdown("[🥷 OMT Ninja](https://omt-ninja.arrow.com) | [📋 ETQ Portal](https://etq.arrow.com)")
    st.markdown("[💼 Salesforce](https://arrow.my.salesforce.com) | [☁️ Oracle Unity](https://ebs.arrow.com)")
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()

# 5. SEARCH & RESULTS
st.title("Search Procedures & Contacts")
query = st.text_input("", placeholder="Search by keyword, collector name, system, or warehouse...")

if query:
    results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    if not results.empty:
        st.write(f"Showing {len(results)} matches:")
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="result-card">
                <div style="float:right;"><span class="system-badge">{row['System']}</span></div>
                <h2 style="margin-top:0;">{row['Process']}</h2>
                <div class="instructions"><b>PROCEDURE / INFO:</b><br>{row['Instructions']}</div>
                <p style="margin-top:15px; font-size:0.9rem;"><b>Rationale:</b> {row['Rationale']}<br>
                <small style="color:gray;">Source: {row['File_Source']}</small></p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error(f"No results found for '{query}'.")
else:
    st.info("The Knowledge Center is active. Type a keyword to begin.")
