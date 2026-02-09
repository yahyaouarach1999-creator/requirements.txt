import streamlit as st
import pandas as pd

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# --- 2. LINKS & RESOURCES ---
LINKS = {
    "Salesforce": "https://arrowcrm.lightning.force.com/lightning/o/Case/list?filterName=My_Open_and_Flagged_With_Reminder",
    "SWB (Oracle)": "https://acswb.arrow.com/Swb/",
    "MyConnect": "https://arrow.service-now.com/myconnect?id=myconnect_home",
    "Admin_Email": "yahya.ouarach@arrow.com"  # Your primary contact
}

# --- 3. CUSTOM STYLING ---
st.markdown(f"""
    <style>
        .stApp {{ background-color: #F8FAFC; }}
        .main-header {{
            background: linear-gradient(90deg, #1E293B 0%, #334155 100%);
            padding: 25px;
            border-radius: 12px;
            color: white;
            text-align: center;
            border-bottom: 5px solid #F97316;
            margin-bottom: 20px;
        }}
        .email-card {{
            background: #FFF7ED;
            padding: 15px;
            border-radius: 10px;
            border: 1px dashed #F97316;
            text-align: center;
        }}
        .topic-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #F97316;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            text-align: center;
        }}
    </style>
""", unsafe_allow_html=True)

# --- 4. HEADER & TOP BAR ---
st.markdown('<div class="main-header"><h1>🏹 Arledge Command Center</h1><p>Global Process Repository & Support Hub</p></div>', unsafe_allow_html=True)

col_search, col_help = st.columns([0.7, 0.3])

with col_search:
    query = st.text_input("🔍 Search Knowledge Base", placeholder="Type a system, warehouse, or collector name...")

with col_help:
    st.markdown(f"""
        <div class="email-card">
            <strong>🆘 Need Technical Help?</strong><br>
            <small>Contact Admin: yahya.ouarach@arrow.com</small><br>
            <a href="mailto:{LINKS['Admin_Email']}?subject=Arledge Portal Support" style="color:#F97316; font-weight:bold;">Send Email Request</a>
        </div>
    """, unsafe_allow_html=True)

# --- 5. DATA LOADING (The 404 Fix) ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("sop_data.csv")
        # Automatically clean hidden spaces from all cells to prevent 404 errors
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df.fillna("")
    except Exception as e:
        st.error(f"Could not load CSV: {e}")
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Training_Link", "Screenshot_URL", "Email_Template"])

df = load_data()

# --- 6. INTERACTIVE TOPIC CARDS ---
if not query:
    st.subheader("📂 Browse by Category")
    systems = df['System'].unique()
    cols = st.columns(len(systems) if len(systems) < 5 else 4)
    for i, sys_name in enumerate(systems):
        with cols[i % len(cols)]:
            if st.button(sys_name, use_container_width=True):
                query = sys_name

# --- 7. SEARCH RESULTS ---
if query:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            with st.container():
                st.markdown(f"### 📌 {row['Process']}")
                col_text, col_img = st.columns([0.6, 0.4])
                
                with col_text:
                    st.markdown(row['Instructions'], unsafe_allow_html=True)
                    
                    st.markdown("---")
                    btn1, btn2 = st.columns(2)
                    with btn1:
                        # Ensures the link is cleaned before passing to the button
                        clean_link = str(row['Training_Link']).strip()
                        if clean_link:
                            st.link_button("🚀 Start Rise 360 Lesson", clean_link, type="primary", use_container_width=True)
                    with btn2:
                        if "Salesforce" in row['System']:
                            st.link_button("Open Live Salesforce", LINKS['Salesforce'], use_container_width=True)
                        elif "Oracle" in row['System']:
                            st.link_button("Open Live SWB", LINKS['SWB (Oracle)'], use_container_width=True)
                    
                    if row['Email_Template']:
                        with st.expander("✉️ View Email Template"):
                            st.code(row['Email_Template'], language="text")
                
                with col_img:
                    if row['Screenshot_URL']:
                        st.image(row['Screenshot_URL'], use_container_width=True)
                st.markdown("---")
    else:
        st.warning(f"No results for '{query}'. Try searching for 'Warehouse' or 'Collector'.")
