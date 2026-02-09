import streamlit as st
import pandas as pd

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="Arledge Learning", layout="wide", page_icon="🏹")

# --- 2. LINKS & RESOURCES ---
LINKS = {
    "Salesforce": "https://arrowcrm.lightning.force.com/lightning/o/Case/list?filterName=My_Open_and_Flagged_With_Reminder",
    "SWB (Oracle)": "https://acswb.arrow.com/Swb/",
    "MyConnect": "https://arrow.service-now.com/myconnect?id=myconnect_home"
}

# --- 3. ADVANCED UI STYLING ---
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        .stApp {{ background-color: #FFFFFF; font-family: 'Inter', sans-serif; }}
        
        /* Navigation Bar */
        .nav-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px 5%;
            background: #1E293B;
            color: white;
            border-bottom: 4px solid #F97316;
        }}
        .logo-text {{ font-size: 24px; font-weight: 800; }}
        .nav-links a {{
            color: white;
            text-decoration: none;
            margin-left: 20px;
            font-size: 14px;
            font-weight: 600;
            transition: 0.3s;
        }}
        .nav-links a:hover {{ color: #F97316; }}

        /* Hero & Search Fix */
        .hero-banner {{
            background: #F8FAFC;
            padding: 40px 5%;
            border-bottom: 1px solid #E2E8F0;
            margin-bottom: 30px;
        }}
        .stTextInput input {{
            border: 2px solid #F97316 !important;
            height: 55px !important;
        }}
    </style>
    
    <div class="nav-bar">
        <div class="logo-text">ARLEDGE <span style="color:#F97316;">LEARNING</span></div>
        <div class="nav-links">
            <a href="{LINKS['Salesforce']}" target="_blank">🚀 Salesforce</a>
            <a href="{LINKS['SWB (Oracle)']}" target="_blank">💾 SWB</a>
            <a href="{LINKS['MyConnect']}" target="_blank">🛠 MyConnect</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 4. SEARCH LOGIC ---
st.markdown('<div class="hero-banner"><h1>Training & Process Repository</h1><p>Search modules below or use the top nav to launch systems.</p></div>', unsafe_allow_html=True)

# Functional Search
query = st.text_input("", placeholder="Search by Module, System, Collector Letter, or Warehouse Code...", label_visibility="collapsed").strip()

# --- 5. DATA LOADING & DISPLAY ---
@st.cache_data
def load_data():
    try:
        # Load CSV and ensure all necessary columns exist
        df = pd.read_csv("sop_data.csv").fillna("")
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Training_Link", "Screenshot_URL", "Email_Template"])

df = load_data()

if query:
    # Improved Search: Looks through System, Process, and Instructions
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for idx, row in results.iterrows():
            with st.expander(f"📌 {row['System']} - {row['Process']}", expanded=True):
                c1, c2 = st.columns([0.6, 0.4])
                with c1:
                    st.markdown("### 📋 Instructions")
                    # Renders <br> as actual new lines in the app
                    st.markdown(row['Instructions'], unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # NEW: Start Rise 360 Lesson Button
                    if row.get('Training_Link') and row['Training_Link'] != "":
                        st.link_button("🚀 Start Rise 360 Lesson", row['Training_Link'], use_container_width=True)
                    
                    # Contextual Buttons for Live Systems
                    if "Salesforce" in row['System']:
                        st.link_button("Go to Live Salesforce Cases", LINKS['Salesforce'])
                    elif any(x in row['System'] for x in ["Oracle", "SWB", "Finance"]):
                        st.link_button("Launch Live SWB Oracle", LINKS['SWB (Oracle)'])
                
                with c2:
                    if row.get('Screenshot_URL') and row['Screenshot_URL'] != "":
                        st.image(row['Screenshot_URL'], caption="Process Visual Reference", use_container_width=True)
                    
                    # NEW: Email Template Section
                    if row.get('Email_Template') and row['Email_Template'] != "":
                        st.info("📧 **Email Template Available**")
                        st.code(row['Email_Template'], language="text")
    else:
        st.warning(f"No matches found for '{query}'. Try searching for a specific collector name or warehouse code.")
else:
    # Default View
    st.info("👋 Select a system from the top menu or start typing in the search box to find contacts, training, and processes.")
