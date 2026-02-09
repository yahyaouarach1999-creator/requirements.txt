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

# --- 3. CUSTOM STYLING (Modern UI) ---
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
        /* Top Navigation Buttons */
        .nav-container {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }}
        /* Footer/SOS Styling */
        .footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #F8FAFC;
            color: #64748B;
            text-align: center;
            padding: 10px;
            font-size: 0.8rem;
            border-top: 1px solid #E2E8F0;
        }}
    </style>
""", unsafe_allow_html=True)

# --- 4. TOP NAVIGATION & HEADER ---
st.markdown('<div class="main-header"><h1>🏹 ARLEDGE <span style="color:#F97316">LEARNING</span></h1><p>Search modules below or use the buttons to launch systems.</p></div>', unsafe_allow_html=True)

# Direct System Launch Buttons
nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    st.link_button("🚀 Launch Salesforce", LINKS['Salesforce'], use_container_width=True)
with nav_col2:
    st.link_button("💾 Launch SWB", LINKS['SWB'], use_container_width=True)
with nav_col3:
    st.link_button("🛠️ Launch MyConnect", LINKS['MyConnect'], use_container_width=True)

st.divider()

# --- 5. SEARCH INTERFACE ---
query = st.text_input("🔍 Search", placeholder="Search by Module, System, Collector Letter, or Warehouse Code...")

# --- 6. DATA LOADING ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("sop_data.csv")
        df.columns = df.columns.str.strip()
        # Clean data and remove inaccessible direct links if they exist in CSV
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df.fillna("")
    except:
        return pd.DataFrame()

df = load_data()

# --- 7. DISPLAY LOGIC ---
if query and not df.empty:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            with st.container(border=True):
                st.subheader(f"📌 {row.get('Process', 'Module')}")
                col_txt, col_img = st.columns([0.6, 0.4])
                with col_txt:
                    st.markdown(row.get('Instructions', ''), unsafe_allow_html=True)
                    # Training Button
                    t_link = str(row.get('Training_Link', '')).strip()
                    if t_link.startswith("http"):
                        st.link_button("📝 Start Training", t_link, type="primary")
                with col_img:
                    if row.get('Screenshot_URL'):
                        st.image(row['Screenshot_URL'], use_container_width=True)
    else:
        st.info("No matching modules found.")
else:
    st.caption("Start typing in the search box above to find contacts, training, and processes.")

# --- 8. SMALL SOS FOOTER ---
st.markdown(f"""
    <div class="footer">
        🆘 Technical Support: <a href="mailto:{LINKS['Admin_Email']}">{LINKS['Admin_Email']}</a> | Arledge Learning System 2026
    </div>
""", unsafe_allow_html=True)
