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
query = st.text_input("", placeholder="Search by Module, System, or Process...", label_visibility="collapsed").strip()

# --- 5. DATA LOADING & DISPLAY ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv("sop_data.csv").fillna("")
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Screenshot_URL", "Email_Template"])

df = load_data()

if query:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for idx, row in results.iterrows():
            with st.expander(f"📌 {row['System']} - {row['Process']}", expanded=True):
                c1, c2 = st.columns([0.6, 0.4])
                with c1:
                    st.markdown("### 📋 Instructions")
                    st.write(row['Instructions'].replace("<br>", "\n"))
                    
                    # Contextual Buttons based on the System
                    if "Salesforce" in row['System']:
                        st.link_button("Go to Salesforce Cases", LINKS['Salesforce'])
                    elif "Oracle" in row['System'] or "AC" in row['System']:
                        st.link_button("Launch SWB Oracle", LINKS['SWB (Oracle)'])
                
                with c2:
                    if row['Screenshot_URL']:
                        st.image(row['Screenshot_URL'], use_container_width=True)
    else:
        st.warning("No matches found.")
else:
    # Default View
    st.info("👋 Select a system from the top menu or start typing in the search box to begin your training.")
