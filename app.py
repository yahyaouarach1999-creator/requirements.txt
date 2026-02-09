import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Arledge Ops Knowledge Base", layout="wide", page_icon="🏹")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        .main-header {
            background-color: #1E293B; padding: 25px; color: white; text-align: center;
            border-bottom: 5px solid #F97316; margin-bottom: 25px;
        }
        .instruction-box { 
            white-space: pre-wrap; font-family: 'Consolas', monospace; 
            line-height: 1.6; color: #1E293B; background: #F1F5F9; 
            padding: 20px; border-left: 5px solid #F97316; border-radius: 4px;
        }
        .collector-card {
            background-color: #FFF7ED; border: 1px solid #FDBA74;
            padding: 15px; border-radius: 8px; color: #7C2D12; margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🏹 ARLEDGE <span style="color:#F97316">OPERATIONS</span></h1></div>', unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    return pd.read_csv("sop_data.csv").fillna("")

df = load_data()

# --- SEARCH ---
query = st.text_input("🔍 Search Full Technical SOPs (e.g., 'V90', 'Reno', 'IT')", placeholder="Search the database...")

if query:
    results = df[df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)]
    
    if not results.empty:
        for _, row in results.iterrows():
            if row['System'] == 'Finance':
                st.markdown(f'<div class="collector-card"><b>{row["Process"]}</b><br>{row["Instructions"]}</div>', unsafe_allow_html=True)
            else:
                with st.expander(f"📌 {row['System']} | {row['Process']}", expanded=True):
                    st.write(f"**Application Context:** {row['Rationale']}")
                    st.write("**Full Procedure / Template:**")
                    st.markdown(f'<div class="instruction-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
    else:
        st.warning("No matching procedures found in the database.")
else:
    st.info("The knowledge base is fully updated with the SOP 7 document. Enter a keyword above.")
