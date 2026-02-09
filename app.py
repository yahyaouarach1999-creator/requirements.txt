import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Arledge Operations Portal", layout="wide", page_icon="🏹")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        .main-header { background-color: #1E293B; padding: 25px; color: white; text-align: center; border-bottom: 5px solid #F97316; }
        .card { background-color: #F1F5F9; padding: 20px; border-radius: 10px; border-top: 4px solid #F97316; text-align: center; height: 180px; }
        .instruction-box { white-space: pre-wrap; font-family: 'Consolas', monospace; line-height: 1.6; background: #F8FAFC; padding: 20px; border-left: 5px solid #F97316; border-radius: 4px; }
        .sticky-footer { position: fixed; bottom: 20px; right: 20px; z-index: 1000; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🏹 ARLEDGE OPERATIONS PORTAL</h1></div>', unsafe_allow_html=True)

# --- HOME CARDS (ETQ Link Added) ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="card"><h3>🚀 Salesforce</h3><p>Manage Cases & Support</p></div>', unsafe_allow_html=True)
    st.link_button("Open Salesforce", "https://arrowcrm.lightning.force.com/", use_container_width=True)
with col2:
    st.markdown('<div class="card"><h3>💾 SWB (Oracle)</h3><p>Orders & Alerts</p></div>', unsafe_allow_html=True)
    st.link_button("Open SWB", "https://acswb.arrow.com/Swb/", use_container_width=True)
with col3:
    st.markdown('<div class="card"><h3>📋 ETQ Portal</h3><p>Warehouse Requests</p></div>', unsafe_allow_html=True)
    st.link_button("Open ETQ", "https://arrow.etq.com/prod/rel/#/app/system/portal", use_container_width=True)
with col4:
    st.markdown('<div class="card"><h3>🛠️ MyConnect</h3><p>IT & System Tickets</p></div>', unsafe_allow_html=True)
    st.link_button("Open MyConnect", "https://arrow.service-now.com/myconnect", use_container_width=True)

st.divider()

# --- SEARCH ENGINE ---
@st.cache_data
def load_data():
    return pd.read_csv("sop_data.csv").fillna("")

df = load_data()
query = st.text_input("🔍 Search Full Technical Knowledge Base", placeholder="Search 'Dropship', 'Alerts', 'IT', 'V90'...")

if query:
    results = df[df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)]
    if not results.empty:
        for _, row in results.iterrows():
            with st.expander(f"📌 {row['System']} | {row['Process']}", expanded=True):
                st.write(f"**Rationale:** {row['Rationale']}")
                st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
    else:
        st.warning("No matches found.")
else:
    st.info("Knowledge base is fully updated with 50+ line items from your documentation.")

# --- FLOATING CONTACT SOS BUTTON ---
st.markdown("""
    <div class="sticky-footer">
        <a href="mailto:yahya.ouarach@arrow.com?subject=SOS Assistance Request" target="_blank">
            <button style="background-color: #F97316; color: white; padding: 15px 30px; border: none; border-radius: 50px; font-weight: bold; cursor: pointer; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);">
                🆘 CONTACT SOS
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)
