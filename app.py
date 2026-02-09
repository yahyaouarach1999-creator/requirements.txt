import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Arledge Learning Portal", layout="wide", page_icon="🏹")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        .main-header {
            background-color: #1E293B; padding: 25px; color: white; text-align: center;
            border-bottom: 4px solid #F97316; margin-bottom: 20px;
        }
        .stExpander { border: 1px solid #E2E8F0 !important; border-radius: 8px !important; margin-bottom: 10px !important; }
        .footer {
            position: fixed; left: 0; bottom: 0; width: 100%; background-color: #F8FAFC;
            color: #64748B; text-align: center; padding: 8px; font-size: 0.75rem; border-top: 1px solid #E2E8F0;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🏹 ARLEDGE <span style="color:#F97316">LEARNING</span></h1></div>', unsafe_allow_html=True)

# --- QUICK LINKS ---
c1, c2, c3 = st.columns(3)
c1.link_button("🚀 Salesforce", "https://arrowcrm.lightning.force.com/", use_container_width=True)
c2.link_button("💾 SWB (Oracle)", "https://acswb.arrow.com/Swb/", use_container_width=True)
c3.link_button("🛠️ MyConnect", "https://arrow.service-now.com/myconnect", use_container_width=True)

st.divider()

# --- DATA LOADING ---
@st.cache_data
def load_all_data():
    try:
        df = pd.read_csv("sop_data.csv")
        df.columns = df.columns.str.strip()
        return df.fillna("N/A")
    except:
        return pd.DataFrame()

df = load_all_data()
query = st.text_input("🔍 Search Entire Knowledge Base", placeholder="Search by SOP, Module, or Process...")

# --- INTERACTIVE SEARCH RESULTS ---
if query and not df.empty:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            with st.expander(f"📌 {row['System']} | {row['Process']}"):
                st.markdown(f"### **Instructions:**\n{row['Instructions']}", unsafe_allow_html=True)
                if 'Rationale' in row and row['Rationale'] != "N/A":
                    st.info(f"💡 **Context/Rationale:** {row['Rationale']}")
                if 'Training_Link' in row and row['Training_Link'] != "N/A":
                    st.write(f"🔗 [Access Full Training Module]({row['Training_Link']})")
    else:
        st.warning("No matching procedures found.")
else:
    st.info("Enter a keyword to view the full SOP or Training step.")

st.markdown('<div class="footer">🆘 Technical Support: yahya.ouarach@arrow.com</div>', unsafe_allow_html=True)
