import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Arledge Ops Portal", layout="wide", page_icon="🏹")

# --- STYLING ---
st.markdown("""
    <style>
        .main-header { background-color: #1E293B; padding: 20px; color: white; text-align: center; border-bottom: 5px solid #F97316; }
        .card { background-color: #F1F5F9; padding: 20px; border-radius: 10px; border-top: 4px solid #F97316; text-align: center; }
        .instruction-box { white-space: pre-wrap; font-family: monospace; background: #F8FAFC; padding: 15px; border-left: 5px solid #F97316; }
        .footer { position: fixed; bottom: 10px; right: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🏹 ARLEDGE OPERATIONS PORTAL</h1></div>', unsafe_allow_html=True)
st.write("---")

# --- HOME CARDS (Salesforce & SWB) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="card"><h3>🚀 Salesforce</h3><p>Manage Cases & Leads</p></div>', unsafe_allow_html=True)
    st.link_button("Open Salesforce", "https://arrowcrm.lightning.force.com/", use_container_width=True)
with col2:
    st.markdown('<div class="card"><h3>💾 SWB (Oracle)</h3><p>Orders & Shipments</p></div>', unsafe_allow_html=True)
    st.link_button("Open SWB", "https://acswb.arrow.com/Swb/", use_container_width=True)
with col3:
    st.markdown('<div class="card"><h3>🛠️ MyConnect</h3><p>IT & ETQ Requests</p></div>', unsafe_allow_html=True)
    st.link_button("Open MyConnect", "https://arrow.service-now.com/myconnect", use_container_width=True)

st.write("---")

# --- SEARCH ---
@st.cache_data
def load_data():
    return pd.read_csv("sop_data.csv").fillna("")

df = load_data()
query = st.text_input("🔍 Search Technical Procedures (V90, Dropship, Sure Ship...)", placeholder="Start typing...")

if query:
    results = df[df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)]
    for _, row in results.iterrows():
        with st.expander(f"📌 {row['System']} | {row['Process']}", expanded=True):
            st.markdown(f"**Scenario:** {row['Rationale']}")
            st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)

# --- CONTACT SOS BUTTON ---
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.link_button("🆘 Contact SOS Team", "mailto:yahya.ouarach@arrow.com?subject=SOS Assistance Request")
st.markdown('</div>', unsafe_allow_html=True)
