import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Arledge Ops Portal", layout="wide", page_icon="🏹")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        .main-header { background-color: #1E293B; padding: 25px; color: white; text-align: center; border-bottom: 5px solid #F97316; }
        .card-container { display: flex; gap: 20px; margin-bottom: 30px; justify-content: center; }
        .card { background-color: #F1F5F9; padding: 20px; border-radius: 10px; border-top: 4px solid #F97316; text-align: center; width: 30%; }
        .instruction-box { white-space: pre-wrap; font-family: 'Consolas', monospace; line-height: 1.6; color: #1E293B; background: #F8FAFC; padding: 20px; border-left: 5px solid #F97316; border-radius: 4px; }
        .stButton>button { width: 100%; border-radius: 5px; }
        .fixed-footer { position: fixed; bottom: 20px; right: 20px; z-index: 999; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🏹 ARLEDGE OPERATIONS PORTAL</h1></div>', unsafe_allow_html=True)
st.write("##")

# --- NAVIGATION CARDS (Fixed Home View) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="card"><h3>🚀 Salesforce</h3><p>Cases & Customer Data</p></div>', unsafe_allow_html=True)
    st.link_button("Access Salesforce", "https://arrowcrm.lightning.force.com/")
with col2:
    st.markdown('<div class="card"><h3>💾 SWB (Oracle)</h3><p>Orders & Alert Review</p></div>', unsafe_allow_html=True)
    st.link_button("Access SWB", "https://acswb.arrow.com/Swb/")
with col3:
    st.markdown('<div class="card"><h3>🛠️ MyConnect</h3><p>IT & ETQ Portal</p></div>', unsafe_allow_html=True)
    st.link_button("Access MyConnect", "https://arrow.service-now.com/myconnect")

st.divider()

# --- SEARCH ENGINE ---
@st.cache_data
def load_data():
    return pd.read_csv("sop_data.csv").fillna("")

df = load_data()
query = st.text_input("🔍 Search Technical Knowledge Base", placeholder="e.g. 'Price Release', 'Dropship', 'V90'...")

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
    st.info("The portal is loaded with the latest Alerts and Dropship procedures.")

# --- FIXED CONTACT SOS BUTTON ---
st.markdown("""
    <div class="fixed-footer">
        <a href="mailto:yahya.ouarach@arrow.com?subject=SOS Assistance Request" target="_blank">
            <button style="background-color: #F97316; color: white; padding: 15px 25px; border: none; border-radius: 50px; font-weight: bold; cursor: pointer; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);">
                🆘 CONTACT SOS
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)
