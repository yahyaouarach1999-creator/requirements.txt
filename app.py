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
    </style>
""", unsafe_allow_html=True)

# --- 4. HEADER ---
st.markdown('<div class="main-header"><h1>🏹 Arledge Command Center</h1><p>Global Process Repository & Support Hub</p></div>', unsafe_allow_html=True)

col_search, col_help = st.columns([0.7, 0.3])
with col_search:
    query = st.text_input("🔍 Search Knowledge Base", placeholder="Search by name, system, or alpha letter...")

with col_help:
    st.markdown(f'<div class="email-card"><strong>🆘 Admin Support</strong><br><a href="mailto:{LINKS["Admin_Email"]}" style="color:#F97316;">{LINKS["Admin_Email"]}</a></div>', unsafe_allow_html=True)

# --- 5. DATA LOADING (KeyError Fix) ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("sop_data.csv")
        # Clean white space and normalize column names
        df.columns = df.columns.str.strip()
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df.fillna("")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

df = load_data()

# --- 6. DISPLAY LOGIC ---
if not df.empty and query:
    # Search across all columns
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            with st.container():
                st.subheader(f"📌 {row.get('Process', 'Process Detail')}")
                c1, c2 = st.columns([0.6, 0.4])
                
                with c1:
                    if 'Instructions' in row:
                        st.markdown(row['Instructions'], unsafe_allow_html=True)
                    
                    # Safe Link Handling
                    t_link = str(row.get('Training_Link', '')).strip()
                    if t_link and t_link.startswith('http'):
                        st.link_button("🚀 Start Training", t_link, type="primary")
                    
                    if 'Email_Template' in row and row['Email_Template']:
                        with st.expander("✉️ View Template"):
                            st.code(row['Email_Template'], language="text")

                with c2:
                    if 'Screenshot_URL' in row and row['Screenshot_URL']:
                        st.image(row['Screenshot_URL'], use_container_width=True)
                st.markdown("---")
    else:
        st.warning("No matches found.")
elif df.empty:
    st.error("The CSV file is missing or empty. Please check `sop_data.csv`.")
