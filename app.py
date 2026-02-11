import streamlit as st
import pandas as pd
import os

# 1. PAGE SETUP
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# --- SECURITY CONFIGURATION ---
# ONLY the emails in this list can enter. 
# "arrow@com" or unauthorized emails will be blocked.
AUTHORIZED_USERS = [
    "yahya.ouarach@arrow.com",  
    "support@verical.com",
    "operations@verical.com"
]

# Professional Styling
st.markdown("""
<style>
    .stApp { background-color: #ffffff !important; color: #000000 !important; }
    input { border: 2px solid #005a9c !important; }
    .result-card { 
        border: 1px solid #e1e4e8; padding: 20px; border-radius: 10px; 
        background-color: #fcfcfc; margin-bottom: 20px;
    }
    .instructions { 
        background-color: #f1f3f4; padding: 15px; 
        border-left: 5px solid #005a9c; white-space: pre-wrap; color: #202124 !important; 
    }
    label, p, span, h1, h2, h3 { color: #000000 !important; }
</style>
""", unsafe_allow_html=True)

# 2. SECURE LOGIN GATEWAY
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🏹 Arledge")
    st.subheader("Authorized Personnel Only")
    
    # Trim and lowercase to prevent "Space" errors
    email_input = st.text_input("Enter your Arrow Email", placeholder="user@arrow.com").lower().strip()
    
    if st.button("Verify & Enter"):
        if email_input in AUTHORIZED_USERS:
            st.session_state.auth = True
            st.session_state.user = email_input
            st.rerun()
        else:
            st.error("🚫 Access Denied. Your email is not on the authorized list.")
            st.info("Contact the administrator to be added to the whitelist.")
    st.stop()

# 3. DATABASE LOADING
@st.cache_data
def load_db():
    if os.path.exists("master_ops_database.csv"):
        return pd.read_csv("master_ops_database.csv").fillna("")
    return pd.DataFrame(columns=["System","Process","Instructions","Rationale"])

df = load_db()

# 4. SIDEBAR (Tools & Credential Vault)
with st.sidebar:
    st.title("🏹 Resource Hub")
    st.write(f"Verified: **{st.session_state.user}**")
    st.divider()
    
    st.markdown("### 🛠 Tools")
    st.markdown("• [🥷 OMT Ninja](https://omt-ninja.arrow.com)\n• [📋 ETQ Portal](https://etq.arrow.com)\n• [💼 Salesforce](https://arrow.my.salesforce.com)\n• [☁️ Oracle Unity](https://ebs.arrow.com)")
    
    st.divider()
    with st.expander("🔑 Portal Credentials"):
        st.write("**OnlineComp:** support@verical.com / support")
        st.write("**Newark:** Verical / Vericalnewark")
        st.write("**PEI Genesis:** operations@verical.com / Arrow_OMT")
        st.write("**Verical/Arrow:** operations@verical.com / Verical_OMT")

    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()

# 5. SEARCH INTERFACE
st.title("OMT Knowledge Base")
query = st.text_input("", placeholder="Search 100+ processes (e.g., 'Sure Ship', 'RMA', 'Nogales')...")

if query:
    results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="result-card">
                <span style="color:#005a9c; font-weight:bold; font-size:0.75rem;">{row['System']}</span>
                <h3 style="margin-top:5px;">{row['Process']}</h3>
                <div class="instructions">{row['Instructions']}</div>
                <p style="margin-top:10px; font-size:0.85rem; color:#555;">{row['Rationale']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No matching process found.")
