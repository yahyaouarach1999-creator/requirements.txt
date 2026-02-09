import streamlit as st
import pandas as pd

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# --- 2. LINKS & RESOURCES ---
LINKS = {
    "Salesforce": "https://arrowcrm.lightning.force.com/lightning/o/Case/list?filterName=My_Open_and_Flagged_With_Reminder",
    "SWB (Oracle)": "https://acswb.arrow.com/Swb/",
    "MyConnect": "https://arrow.service-now.com/myconnect?id=myconnect_home",
    "Admin_Email": "yahya.ouarach@arrow.com"
}

# --- 3. CUSTOM STYLING ---
st.markdown(f"""
    <style>
        .stApp {{ background-color: #F8FAFC; }}
        .main-header {{
            background: linear-gradient(90deg, #1E293B 0%, #334155 100%);
            padding: 25px; border-radius: 12px; color: white; text-align: center;
            border-bottom: 5px solid #F97316; margin-bottom: 20px;
        }}
        .email-card {{
            background: #FFF7ED; padding: 15px; border-radius: 10px;
            border: 1px dashed #F97316; text-align: center;
        }}
        .topic-card {{
            background: white; padding: 15px; border-radius: 8px;
            border-left: 5px solid #F97316; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            text-align: center; cursor: pointer;
        }}
    </style>
""", unsafe_allow_html=True)

# --- 4. HEADER ---
st.markdown('<div class="main-header"><h1>🏹 Arledge Command Center</h1><p>Global Process Repository & Support Hub</p></div>', unsafe_allow_html=True)

col_search, col_help = st.columns([0.7, 0.3])
with col_search:
    query = st.text_input("🔍 Search Knowledge Base", placeholder="Search by name, alpha letter (A, B, C...), or system...")

with col_help:
    st.markdown(f"""
        <div class="email-card">
            <strong>🆘 Technical Support</strong><br>
            <a href="mailto:{LINKS['Admin_Email']}?subject=Portal Help" style="color:#F97316; font-weight:bold;">{LINKS['Admin_Email']}</a>
        </div>
    """, unsafe_allow_html=True)

# --- 5. DATA LOADING & CLEANING ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("sop_data.csv")
        # Standardize columns and strip hidden spaces to fix 404/KeyErrors
        df.columns = df.columns.str.strip()
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df.fillna("")
    except Exception as e:
        st.error(f"CSV Error: {e}")
        return pd.DataFrame()

df = load_data()

# --- 6. INTERACTIVE TOPICS ---
if not query and not df.empty:
    st.subheader("📂 Browse Categories")
    systems = df['System'].unique()
    cols = st.columns(len(systems) if len(systems) < 5 else 4)
    for i, sys_name in enumerate(systems):
        with cols[i % len(cols)]:
            if st.button(sys_name, use_container_width=True):
                query = sys_name

# --- 7. SEARCH RESULTS ---
if query and not df.empty:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            with st.container():
                st.markdown(f"### 📌 {row.get('Process', 'Module')}")
                c1, c2 = st.columns([0.6, 0.4])
                with c1:
                    st.markdown(row.get('Instructions', ''), unsafe_allow_html=True)
                    st.markdown("---")
                    
                    # Action Buttons
                    b1, b2 = st.columns(2)
                    with b1:
                        t_link = str(row.get('Training_Link', '')).strip()
                        if t_link.startswith("http"):
                            st.link_button("🚀 Start Training", t_link, type="primary", use_container_width=True)
                    with b2:
                        if "Salesforce" in row['System']:
                            st.link_button("Open Salesforce", LINKS['Salesforce'], use_container_width=True)
                        elif "Oracle" in row['System'] or "Finance" in row['System']:
                            st.link_button("Open SWB Oracle", LINKS['SWB (Oracle)'], use_container_width=True)
                
                with c2:
                    if row.get('Screenshot_URL'):
                        st.image(row['Screenshot_URL'], use_container_width=True)
                st.markdown("---")
    else:
        st.warning(f"No results found for '{query}'.")
