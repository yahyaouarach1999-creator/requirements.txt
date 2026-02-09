import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Arledge Operations Portal", layout="wide", page_icon="🏹")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        .stApp { background-color: #FFFFFF; }
        .main-header {
            background-color: #1E293B; padding: 20px; color: white; text-align: center;
            border-bottom: 4px solid #F97316; margin-bottom: 20px;
        }
        .stExpander { border: 1px solid #E2E8F0 !important; border-radius: 8px !important; }
        .instructions-text { 
            white-space: pre-wrap; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6; 
            color: #1E293B; 
            background: #F1F5F9; 
            padding: 20px; 
            border-left: 5px solid #F97316;
            border-radius: 5px; 
        }
        .collector-box {
            background: #FFF7ED;
            padding: 15px;
            border: 1px solid #FDBA74;
            border-radius: 5px;
            color: #7C2D12;
        }
        .footer { position: fixed; left: 0; bottom: 0; width: 100%; background: #F8FAFC; text-align: center; padding: 5px; font-size: 0.7rem; border-top: 1px solid #E2E8F0; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🏹 ARLEDGE <span style="color:#F97316">OPERATIONS</span></h1></div>', unsafe_allow_html=True)

# --- QUICK LINKS ---
c1, c2, c3 = st.columns(3)
c1.link_button("🚀 Salesforce", "https://arrowcrm.lightning.force.com/", use_container_width=True)
c2.link_button("💾 SWB (Oracle)", "https://acswb.arrow.com/Swb/", use_container_width=True)
c3.link_button("🛠️ MyConnect", "https://arrow.service-now.com/myconnect", use_container_width=True)

st.divider()

# --- DATA LOADING ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("sop_data.csv")
        df.columns = df.columns.str.strip()
        return df.fillna("")
    except: return pd.DataFrame()

df = load_data()
query = st.text_input("🔍 Search Full Technical Procedures & Collectors", placeholder="Search 'V90', 'Alexis', 'Sure Ship', 'Dropship'...")

if query and not df.empty:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            with st.expander(f"📌 {row['System']} | {row['Process']}", expanded=True):
                if row['System'] == 'Finance':
                    st.markdown(f'<div class="collector-box">{row["Instructions"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f"**Application/Context:** {row['Rationale']}")
                    st.markdown("**Full Un-summarized Process:**")
                    st.markdown(f'<div class="instructions-text">{row["Instructions"]}</div>', unsafe_allow_html=True)
    else: st.warning("No matches found for that keyword.")
else: st.info("Enter a keyword to display full text from SOP 7, Dropship manuals, or Collector contacts.")

st.markdown('<div class="footer">🆘 Support: yahya.ouarach@arrow.com</div>', unsafe_allow_html=True)
