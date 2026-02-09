import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Arledge Ops Portal", layout="wide", page_icon="🏹")

# --- CUSTOM CSS FOR MINIMALIST ICON TILES ---
st.markdown("""
    <style>
        .main-header { background-color: #1E293B; padding: 10px; color: white; text-align: center; border-bottom: 3px solid #F97316; margin-bottom: 20px;}
        .icon-bar { display: flex; justify-content: space-around; gap: 10px; margin-bottom: 30px; }
        .action-tile { 
            background-color: #F8FAFC; padding: 8px 15px; border-radius: 6px; 
            border: 1px solid #E2E8F0; text-align: center; flex: 1;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .action-tile:hover { border-color: #F97316; background-color: #F1F5F9; }
        .action-tile h5 { margin: 0 0 5px 0; font-size: 0.85rem; color: #475569; }
        .instruction-box { white-space: pre-wrap; font-family: 'Consolas', monospace; font-size: 0.9rem; background: #1E293B; color: #F8FAFC; padding: 20px; border-left: 5px solid #F97316; border-radius: 4px; }
        .sticky-footer { position: fixed; bottom: 20px; right: 20px; z-index: 1000; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h4>🏹 ARLEDGE OPERATIONS KNOWLEDGE BASE</h4></div>', unsafe_allow_html=True)

# --- MINIMALIST ICON BAR ---
st.markdown('<div class="icon-bar">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="action-tile"><h5>Salesforce</h5></div>', unsafe_allow_html=True)
    st.link_button("🚀 Launch", "https://arrowcrm.lightning.force.com/", use_container_width=True)
with c2:
    st.markdown('<div class="action-tile"><h5>SWB Oracle</h5></div>', unsafe_allow_html=True)
    st.link_button("💾 Entry", "https://acswb.arrow.com/Swb/", use_container_width=True)
with c3:
    st.markdown('<div class="action-tile"><h5>ETQ Portal</h5></div>', unsafe_allow_html=True)
    st.link_button("📋 Forms", "https://arrow.etq.com/prod/rel/#/app/system/portal", use_container_width=True)
with c4:
    st.markdown('<div class="action-tile"><h5>MyConnect</h5></div>', unsafe_allow_html=True)
    st.link_button("🛠️ Tickets", "https://arrow.service-now.com/myconnect", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- SEARCH ---
@st.cache_data
def load_data():
    return pd.read_csv("sop_data.csv").fillna("")

df = load_data()
query = st.text_input("🔍 Search 60+ Technical Procedures & Templates", placeholder="Enter keyword (e.g., 'V90', 'Sure Ship', 'Price Release')...")

if query:
    results = df[df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)]
    if not results.empty:
        for _, row in results.iterrows():
            with st.expander(f"📌 {row['System']} | {row['Process']}", expanded=True):
                st.write(f"**Application Context:** {row['Rationale']}")
                st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
    else:
        st.warning("No matches found in the technical documentation.")

# --- FLOATING SOS BUTTON ---
st.markdown("""
    <div class="sticky-footer">
        <a href="mailto:yahya.ouarach@arrow.com?subject=SOS Assistance Request" target="_blank">
            <button style="background-color: #F97316; color: white; padding: 12px 24px; border: none; border-radius: 30px; font-weight: bold; cursor: pointer; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);">
                🆘 SOS CONTACT
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)
