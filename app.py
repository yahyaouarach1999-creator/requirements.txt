import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Arledge Ops Portal", layout="wide", page_icon="🏹")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        .stApp { background-color: #FFFFFF; }
        .main-header {
            background-color: #1E293B; padding: 20px; color: white; text-align: center;
            border-bottom: 4px solid #F97316; margin-bottom: 20px;
        }
        .instructions-box { 
            white-space: pre-wrap; 
            font-family: sans-serif; 
            line-height: 1.6; 
            color: #1E293B; 
            background: #F8FAFC; 
            padding: 20px; 
            border-left: 5px solid #F97316;
            border-radius: 5px; 
        }
        .collector-card {
            background: #FFF7ED;
            padding: 15px;
            border: 1px solid #FDBA74;
            border-radius: 5px;
            color: #7C2D12;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🏹 ARLEDGE <span style="color:#F97316">OPERATIONS</span></h1></div>', unsafe_allow_html=True)

# --- DATA ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("sop_data.csv")
        df.columns = df.columns.str.strip()
        return df.fillna("")
    except: return pd.DataFrame()

df = load_data()

# --- SEARCH ---
query = st.text_input("🔍 Search Operations Knowledge Base", placeholder="Search by Warehouse, Collector, or Process...")

if query and not df.empty:
    results = df[df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)]
    
    if not results.empty:
        for _, row in results.iterrows():
            if row['System'] == 'Finance':
                st.markdown(f'<div class="collector-card"><b>{row["Process"]}</b><br>{row["Instructions"]}</div>', unsafe_allow_html=True)
            else:
                with st.expander(f"📌 {row['System']} | {row['Process']}", expanded=True):
                    st.write(f"**Application:** {row['Rationale']}")
                    st.markdown(f'<div class="instructions-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
    else:
        st.warning("No matching procedures found.")
else:
    st.info("The knowledge base is updated with Navigation, Logistics, Finance, and Dropship procedures.")
