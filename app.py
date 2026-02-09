import streamlit as st
import pandas as pd
import re

# --- PAGE CONFIG ---
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        .main-header { background-color: #0F172A; padding: 10px; color: white; text-align: center; border-bottom: 3px solid #F97316; margin-bottom: 15px; }
        .nano-tile { background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; text-align: center; padding: 5px; }
        .nano-label { font-size: 0.6rem; font-weight: 900; color: #64748B; text-transform: uppercase; }
        .instruction-box { white-space: pre-wrap; font-family: 'Consolas', monospace; font-size: 0.85rem; background: #1E293B; color: #F8FAFC; padding: 15px; border-left: 5px solid #F97316; border-radius: 4px; }
        /* Make button red and bold */
        div.stButton > button:first-child {
            background-color: #fee2e2;
            color: #dc2626;
            border: 1px solid #dc2626;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# --- AUTH GATE ---
if 'auth' not in st.session_state: st.session_state['auth'] = False
if not st.session_state['auth']:
    with st.form("login"):
        email = st.text_input("Enter @arrow.com email:")
        if st.form_submit_button("Login"):
            if email.endswith("@arrow.com"):
                st.session_state['auth'] = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- NAVIGATION ---
st.markdown('<div class="main-header"><h4>🏹 ARLEDGE OPERATIONS COMMAND</h4></div>', unsafe_allow_html=True)
cols = st.columns(5)
nav = [("CRM", "https://arrowcrm.lightning.force.com/"), ("Orders", "https://acswb.arrow.com/Swb/"), ("Forms", "https://arrow.etq.com/prod/rel/#/app/system/portal"), ("Tickets", "https://arrow.service-now.com/myconnect"), ("SOS", "mailto:yahya.ouarach@arrow.com")]
for i, (label, link) in enumerate(nav):
    with cols[i]: st.link_button(label, link, use_container_width=True)

st.divider()

# --- SEARCH & DATA ---
@st.cache_data(show_spinner=False)
def get_sop():
    return pd.read_csv("sop_data.csv").fillna("N/A")

df = get_sop()
search = st.text_input("🔍 Search Procedures", placeholder="e.g. Price Release...")

if search:
    mask = df.apply(lambda x: x.astype(str).str.contains(search, case=False)).any(axis=1)
    res = df[mask]
    
    if not res.empty:
        for idx, row in res.iterrows():
            # Use columns to put the button next to the title for better visibility
            title_col, btn_col = st.columns([4, 1])
            with title_col:
                st.markdown(f"### 📌 {row['System']} | {row['Process']}")
            with btn_col:
                # This button should now be impossible to miss
                if st.button("🚩 ERROR IN DATA", key=f"err_{idx}"):
                    st.error(f"Reported: {row['Process']}. Notify Yahya immediately.")
            
            st.caption(f"**Rationale:** {row['Rationale']}")
            st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
            st.markdown("---")
    else:
        st.warning("Nothing found.")
