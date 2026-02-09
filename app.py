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
        /* Ensuring the Report Issue button stands out */
        .stButton>button { border-radius: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION GATE ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def check_email(email):
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@arrow\.com$", email))

if not st.session_state['authenticated']:
    st.markdown('<div class="main-header"><h4>🔒 ARROW.COM ACCESS REQUIRED</h4></div>', unsafe_allow_html=True)
    with st.form("auth"):
        user_email = st.text_input("Official Email:")
        if st.form_submit_button("Enter Portal"):
            if check_email(user_email):
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Access Denied: @arrow.com domain only.")
    st.stop()

# --- APP CONTENT ---
st.markdown('<div class="main-header"><h4>🏹 ARLEDGE OPERATIONS COMMAND</h4></div>', unsafe_allow_html=True)

# --- NANO NAVIGATION ---
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
query = st.text_input("🔍 Search Combined Technical Procedures", placeholder="Search 'Verification', 'Price Release'...")

if query:
    results = df[df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)]
    if not results.empty:
        for index, row in results.iterrows():
            # Standard View
            st.markdown(f"### 📌 {row['System']} | {row['Process']}")
            st.caption(f"**Rationale:** {row['Rationale']}")
            st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
            
            # --- THE VISIBLE REPORT ISSUE BUTTON ---
            # Unique key 'issue_index' ensures it displays for every result
            if st.button("🚩 Report Issue", key=f"issue_{index}"):
                st.error(f"Issue logged for {row['Process']}. Please notify Yahya.")
            
            st.markdown("---")
    else:
        st.warning("No matches found.")
import urllib.parse

# Inside your search results loop:
subject = urllib.parse.quote(f"SOP Issue Report: {row['Process']}")
body = urllib.parse.quote(f"User reporting issue with {row['Process']}.\nInstructions found: {row['Instructions']}")
mailto_link = f"mailto:yahya.ouarach@arrow.com?subject={subject}&body={body}"

if st.button("🚩 Report Issue", key=f"issue_{index}"):
    # This creates a link the user clicks to open Outlook/Email
    st.markdown(f'<a href="{mailto_link}" target="_blank">Click here to send email report</a>', unsafe_allow_html=True)
