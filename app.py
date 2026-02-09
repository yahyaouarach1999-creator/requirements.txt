import streamlit as st
import pandas as pd
import re

# --- PAGE CONFIG ---
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        .main-header { background-color: #0F172A; padding: 10px; color: white; text-align: center; border-bottom: 3px solid #F97316; margin-bottom: 15px; }
        .nano-tile { 
            background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; 
            text-align: center; padding: 5px; transition: 0.2s;
        }
        .nano-tile:hover { border-color: #F97316; background-color: #F1F5F9; transform: translateY(-1px); }
        .nano-label { font-size: 0.6rem; font-weight: 900; color: #64748B; text-transform: uppercase; margin-bottom: 2px; }
        .instruction-box { white-space: pre-wrap; font-family: 'Consolas', monospace; font-size: 0.85rem; background: #1E293B; color: #F8FAFC; padding: 15px; border-left: 5px solid #F97316; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN LOGIC ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def check_email(email):
    # Regex to ensure the email ends exactly with @arrow.com
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@arrow\.com$", email))

if not st.session_state['authenticated']:
    st.markdown('<div class="main-header"><h4>🔒 RESTRICTED ACCESS: ARROW EMPLOYEES ONLY</h4></div>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        user_email = st.text_input("Enter your @arrow.com email to continue:")
        submit_button = st.form_submit_button("Verify Access")
        
        if submit_button:
            if check_email(user_email):
                st.session_state['authenticated'] = True
                st.success("Access Granted!")
                st.rerun()
            else:
                st.error("Access Denied: You must use a valid @arrow.com address.")
    st.stop() # Stops the rest of the app from running until authenticated

# --- APP CONTENT (ONLY RUNS IF AUTHENTICATED) ---
st.markdown('<div class="main-header"><h4>🏹 ARLEDGE OPERATIONS COMMAND</h4></div>', unsafe_allow_html=True)

# --- NAVIGATION TILES ---
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown('<div class="nano-tile"><div class="nano-label">Salesforce</div></div>', unsafe_allow_html=True)
    st.link_button("🚀 CRM", "https://arrowcrm.lightning.force.com/", use_container_width=True)
with col2:
    st.markdown('<div class="nano-tile"><div class="nano-label">SWB Oracle</div></div>', unsafe_allow_html=True)
    st.link_button("💾 Orders", "https://acswb.arrow.com/Swb/", use_container_width=True)
with col3:
    st.markdown('<div class="nano-tile"><div class="nano-label">ETQ Portal</div></div>', unsafe_allow_html=True)
    st.link_button("📋 Forms", "https://arrow.etq.com/prod/rel/#/app/system/portal", use_container_width=True)
with col4:
    st.markdown('<div class="nano-tile"><div class="nano-label">Support</div></div>', unsafe_allow_html=True)
    st.link_button("🛠️ Tickets", "https://arrow.service-now.com/myconnect", use_container_width=True)
with col5:
    st.markdown('<div class="nano-tile"><div class="nano-label">SOS Help</div></div>', unsafe_allow_html=True)
    st.link_button("🆘 Contact", "mailto:yahya.ouarach@arrow.com", use_container_width=True)

st.divider()

# --- SEARCH ENGINE ---
@st.cache_data
def load_data():
    return pd.read_csv("sop_data.csv").fillna("")

df = load_data()
query = st.text_input("🔍 Search 30+ Technical Procedures", placeholder="Search 'LOC Hold', 'CMF Verification'...")

if query:
    results = df[df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)]
    if not results.empty:
        for _, row in results.iterrows():
            with st.expander(f"📌 {row['System']} | {row['Process']}", expanded=True):
                st.caption(f"**Rationale:** {row['Rationale']}")
                st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
    else:
        st.warning("No matches found.")
