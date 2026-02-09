import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Arledge Ops Portal", layout="wide", page_icon="🏹")

# --- STYLING ---
st.markdown("""
    <style>
        .main-header { background-color: #1E293B; padding: 25px; color: white; text-align: center; border-bottom: 5px solid #F97316; }
        .card { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border-top: 4px solid #F97316; text-align: center; height: 160px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
        .instruction-box { white-space: pre-wrap; font-family: 'Consolas', monospace; line-height: 1.6; background: #F1F5F9; padding: 20px; border-left: 5px solid #F97316; border-radius: 4px; }
        .sticky-footer { position: fixed; bottom: 20px; right: 20px; z-index: 999; }
        .stButton>button { width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🏹 ARLEDGE OPERATIONS PORTAL</h1></div>', unsafe_allow_html=True)
st.write("##")

# --- HOME CARDS (Salesforce & SWB) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="card"><h3>🚀 Salesforce</h3><p>Manage Cases & Support Tasks</p></div>', unsafe_allow_html=True)
    st.link_button("Open Salesforce", "https://arrowcrm.lightning.force.com/")
with col2:
    st.markdown('<div class="card"><h3>💾 SWB (Oracle)</h3><p>Orders & Alert Processing</p></div>', unsafe_allow_html=True)
    st.link_button("Open SWB", "https://acswb.arrow.com/Swb/")
with col3:
    st.markdown('<div class="card"><h3>🛠️ MyConnect</h3><p>IT & Warehouse Tickets</p></div>', unsafe_allow_html=True)
    st.link_button("Open MyConnect", "https://arrow.service-now.com/myconnect")

st.divider()

# --- SEARCH ENGINE ---
@st.cache_data
def load_data():
    return pd.read_csv("sop_data.csv").fillna("")

df = load_data()
query = st.text_input("🔍 Search Knowledge Base (e.g. 'Alerts', 'V90', 'Dropship')", placeholder="Start typing...")

if query:
    results = df[df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)]
    if not results.empty:
        for _, row in results.iterrows():
            with st.expander(f"📌 {row['System']} | {row['Process']}", expanded=True):
                st.caption(f"**SCENARIO:** {row['Rationale']}")
                st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
    else:
        st.warning("No matches found for that keyword.")

# --- STICKY CONTACT BUTTON ---
st.markdown("""
    <div class="sticky-footer">
        <a href="mailto:yahya.ouarach@arrow.com?subject=SOS Assistance Request" target="_blank">
            <button style="background-color: #F97316; color: white; padding: 15px 30px; border: none; border-radius: 50px; font-weight: bold; cursor: pointer; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);">
                🆘 CONTACT SOS
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)
