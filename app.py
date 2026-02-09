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
            padding: 25px;
            color: white;
            text-align: center;
            border-bottom: 4px solid #F97316;
            margin-bottom: 20px;
        }}
        .main-header h1 {{ margin: 0; font-weight: 800; }}
        /* Expander Styling */
        .stExpander {{
            border: 1px solid #E2E8F0 !important;
            border-radius: 8px !important;
            margin-bottom: 10px !important;
        }}
        /* Small Footer SOS */
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
    </style>
""", unsafe_allow_html=True)

# --- 4. TOP NAVIGATION ---
st.markdown('<div class="main-header"><h1>🏹 ARLEDGE <span style="color:#F97316">LEARNING</span></h1></div>', unsafe_allow_html=True)

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
query = st.text_input("🔍 Search Knowledge Base", placeholder="Type a process, system, or alpha letter...")

# --- 7. INTERACTIVE DISPLAY (Clickable Titles) ---
if query and not df.empty:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            # Big Title that reveals info when clicked
            with st.expander(f"📌 {row.get('Process', 'Module')}", expanded=False):
                st.markdown(row.get('Instructions', ''), unsafe_allow_html=True)
                # If a link exists, it remains accessible only inside the expanded area
                proc_link = str(row.get('Training_Link', '')).strip()
                if proc_link.startswith("http"):
                    st.markdown(f"[Click here for additional resource]({proc_link})")
    else:
        st.info("No matching modules found.")
else:
    st.caption("Enter search terms above to view contacts and process details.")

# --- 8. SOS FOOTER ---
st.markdown(f"""
    <div class="footer">
        🆘 Support: <a href="mailto:{LINKS['Admin_Email']}">{LINKS['Admin_Email']}</a>
    </div>
""", unsafe_allow_html=True)
