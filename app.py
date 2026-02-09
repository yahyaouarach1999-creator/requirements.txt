import streamlit as st
import pandas as pd

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="Arledge Learning", layout="wide", page_icon="🏹")

# --- 2. LINKS & RESOURCES ---
LINKS = {
    "Salesforce": "https://arrowcrm.lightning.force.com/",
    "SWB": "https://acswb.arrow.com/Swb/",
    "MyConnect": "https://arrow.service-now.com/myconnect",
    "Admin_Email": "yahya.ouarach@arrow.com"
}

# --- 3. CUSTOM STYLING ---
st.markdown(f"""
    <style>
        .stApp {{ background-color: #FFFFFF; }}
        /* Header Styling */
        .main-header {{
            background-color: #1E293B;
            padding: 30px;
            color: white;
            text-align: center;
            border-bottom: 4px solid #F97316;
            margin-bottom: 20px;
        }}
        .main-header h1 {{ margin-bottom: 5px; font-weight: 800; }}
        /* Footer Styling */
        .footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #F8FAFC;
            color: #64748B;
            text-align: center;
            padding: 8px;
            font-size: 0.75rem;
            border-top: 1px solid #E2E8F0;
            z-index: 100;
        }}
        /* Process Card Styling */
        .process-card {{
            border-left: 5px solid #F97316;
            background-color: #FBFCFE;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 15px;
        }}
    </style>
""", unsafe_allow_html=True)

# --- 4. TOP NAVIGATION & HEADER ---
st.markdown('<div class="main-header"><h1>🏹 ARLEDGE <span style="color:#F97316">LEARNING</span></h1><p>Search modules below or use the top nav to launch systems.</p></div>', unsafe_allow_html=True)

# Direct System Launch Buttons
nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    st.link_button("🚀 Salesforce", LINKS['Salesforce'], use_container_width=True)
with nav_col2:
    st.link_button("💾 SWB (Oracle)", LINKS['SWB'], use_container_width=True)
with nav_col3:
    st.link_button("🛠️ MyConnect", LINKS['MyConnect'], use_container_width=True)

st.divider()

# --- 5. DATA LOADING ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("sop_data.csv")
        df.columns = df.columns.str.strip()
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df.fillna("")
    except:
        return pd.DataFrame()

df = load_data()

# --- 6. SEARCH INTERFACE ---
query = st.text_input("🔍 Search Knowledge Base", placeholder="Enter process name, system, or alpha letter...")

# --- 7. DISPLAY LOGIC ---
if query and not df.empty:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            with st.container():
                st.markdown(f"""<div class="process-card">
                    <h3>📌 {row.get('Process', 'Module')}</h3>
                    <p>{row.get('Instructions', '')}</p>
                </div>""", unsafe_allow_html=True)
                
                # Check for specific link if provided in CSV
                proc_link = str(row.get('Training_Link', '')).strip()
                if proc_link.startswith("http"):
                    st.link_button("🔗 View Resource", proc_link)
    else:
        st.info("No matching results found.")
else:
    st.caption("Start typing above to find contacts and processes.")

# --- 8. SOS FOOTER ---
st.markdown(f"""
    <div class="footer">
        🆘 Support: <a href="mailto:{LINKS['Admin_Email']}">{LINKS['Admin_Email']}</a>
    </div>
""", unsafe_allow_html=True)
