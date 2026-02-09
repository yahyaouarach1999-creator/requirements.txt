import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Arledge Ops Portal", layout="wide", page_icon="🏹")

# --- CUSTOM CSS FOR SMALLER ICONS ---
st.markdown("""
    <style>
        .main-header { background-color: #1E293B; padding: 15px; color: white; text-align: center; border-bottom: 5px solid #F97316; }
        .icon-tile { 
            background-color: #F8FAFC; padding: 10px; border-radius: 8px; 
            border: 1px solid #E2E8F0; text-align: center; height: 110px;
            transition: transform 0.2s;
        }
        .icon-tile:hover { transform: scale(1.02); border-color: #F97316; }
        .icon-tile h4 { margin: 5px 0; font-size: 0.9rem; color: #1E293B; }
        .instruction-box { white-space: pre-wrap; font-family: 'Consolas', monospace; font-size: 0.85rem; background: #F8FAFC; padding: 15px; border-left: 5px solid #F97316; }
        .sticky-footer { position: fixed; bottom: 20px; right: 20px; z-index: 1000; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🏹 ARLEDGE OPERATIONS</h1></div>', unsafe_allow_html=True)

# --- SMALLER ICON BUTTONS ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="icon-tile"><h4>Salesforce</h4></div>', unsafe_allow_html=True)
    st.link_button("🚀 Open", "https://arrowcrm.lightning.force.com/", use_container_width=True)
with c2:
    st.markdown('<div class="icon-tile"><h4>SWB Oracle</h4></div>', unsafe_allow_html=True)
    st.link_button("💾 Open", "https://acswb.arrow.com/Swb/", use_container_width=True)
with c3:
    st.markdown('<div class="icon-tile"><h4>ETQ Portal</h4></div>', unsafe_allow_html=True)
    st.link_button("📋 Open", "https://arrow.etq.com/prod/rel/#/app/system/portal", use_container_width=True)
with c4:
    st.markdown('<div class="icon-tile"><h4>MyConnect</h4></div>', unsafe_allow_html=True)
    st.link_button("🛠️ Open", "https://arrow.service-now.com/myconnect", use_container_width=True)

st.divider()

# --- SEARCH ---
@st.cache_data
def load_data():
    return pd.read_csv("sop_data.csv").fillna("")

df = load_data()
query = st.text_input("🔍 Search 60+ Technical Procedures", placeholder="e.g. 'Venlo', 'Price Release', 'Dropship'...")

if query:
    results = df[df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)]
    if not results.empty:
        for _, row in results.iterrows():
            with st.expander(f"📌 {row['System']} | {row['Process']}", expanded=True):
                st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
    else:
        st.warning("No matches found.")

# --- FLOATING SOS ---
st.markdown("""
    <div class="sticky-footer">
        <a href="mailto:yahya.ouarach@arrow.com?subject=SOS Assistance" target="_blank">
            <button style="background-color: #F97316; color: white; padding: 10px 20px; border: none; border-radius: 50px; font-weight: bold; cursor: pointer; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);">
                🆘 SOS
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)
