import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Arledge Learning", layout="wide", page_icon="🏹")

# --- SYSTEM LINKS ---
LINKS = {
    "Salesforce": "https://arrowcrm.lightning.force.com/",
    "SWB": "https://acswb.arrow.com/Swb/",
    "MyConnect": "https://arrow.service-now.com/myconnect",
    "Admin": "yahya.ouarach@arrow.com"
}

# --- STYLING ---
st.markdown(f"""
    <style>
        .stApp {{ background-color: #FFFFFF; }}
        .main-header {{
            background-color: #1E293B; padding: 25px; color: white; text-align: center;
            border-bottom: 4px solid #F97316; margin-bottom: 20px;
        }}
        .footer {{
            position: fixed; left: 0; bottom: 0; width: 100%; background-color: #F8FAFC;
            color: #64748B; text-align: center; padding: 8px; font-size: 0.75rem; border-top: 1px solid #E2E8F0;
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🏹 ARLEDGE <span style="color:#F97316">LEARNING</span></h1></div>', unsafe_allow_html=True)

# --- NAV BAR ---
c1, c2, c3 = st.columns(3)
c1.link_button("🚀 Salesforce", LINKS['Salesforce'], use_container_width=True)
c2.link_button("💾 SWB (Oracle)", LINKS['SWB'], use_container_width=True)
c3.link_button("🛠️ MyConnect", LINKS['MyConnect'], use_container_width=True)

st.divider()

# --- DATA ENGINE ---
@st.cache_data
def get_data():
    try:
        # Load and force column cleaning to prevent 'KeyError'
        df = pd.read_csv("sop_data.csv")
        df.columns = df.columns.str.strip()
        return df.fillna("")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

df = get_data()
query = st.text_input("🔍 Search SOPs or Collectors", placeholder="Search 'SOP 7', 'Sure Ship', 'Alexis'...")

# --- RESULTS ENGINE ---
if query and not df.empty:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            # CLICKABLE TITLE LOGIC
            with st.expander(f"📌 {row.get('Process', 'Procedure')}"):
                st.markdown(f"**Instructions:**\n{row.get('Instructions', 'No details provided.')}", unsafe_allow_html=True)
                if 'Rationale' in row and row['Rationale']:
                    st.info(f"💡 **Note:** {row['Rationale']}")
    else:
        st.info("No matching data found.")

st.markdown(f'<div class="footer">🆘 Support: <a href="mailto:{LINKS["Admin"]}">{LINKS["Admin"]}</a></div>', unsafe_allow_html=True)
