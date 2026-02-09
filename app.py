import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Arledge Operations Portal", layout="wide", page_icon="🏹")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
        .stApp { background-color: #FFFFFF; }
        .main-header {
            background-color: #1E293B; padding: 25px; color: white; text-align: center;
            border-bottom: 4px solid #F97316; margin-bottom: 20px;
        }
        .stExpander { border: 1px solid #E2E8F0 !important; border-radius: 8px !important; margin-bottom: 10px !important; }
        .footer {
            position: fixed; left: 0; bottom: 0; width: 100%; background-color: #F8FAFC;
            color: #64748B; text-align: center; padding: 8px; font-size: 0.75rem; border-top: 1px solid #E2E8F0;
        }
        .instructions-text { white-space: pre-wrap; font-size: 0.95rem; line-height: 1.6; color: #1E293B; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🏹 ARLEDGE <span style="color:#F97316">OPERATIONS</span></h1></div>', unsafe_allow_html=True)

# --- SYSTEM LAUNCHERS ---
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
    except:
        return pd.DataFrame()

df = load_data()
query = st.text_input("🔍 Search Procedures (e.g., 'VXX', 'Dropship', 'Alerts', 'Nogales')", placeholder="Type a warehouse code or process name...")

# --- INTERACTIVE ACCORDION RESULTS ---
if query and not df.empty:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            with st.expander(f"📌 {row['System']} | {row['Process']}"):
                st.markdown(f"**Scenario/Rationale:**\n{row['Rationale']}")
                st.divider()
                st.markdown("**Step-by-Step Instructions:**")
                st.markdown(f'<div class="instructions-text">{row["Instructions"]}</div>', unsafe_allow_html=True)
    else:
        st.warning("No matching procedures found.")
else:
    st.info("Enter a keyword to view full details from SOP 7 and Dropship manuals.")

st.markdown('<div class="footer">🆘 Support: yahya.ouarach@arrow.com</div>', unsafe_allow_html=True)
