import streamlit as st
import pandas as pd
import webbrowser

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# --- 2. LINKS & RESOURCES ---
LINKS = {
    "Salesforce": "https://arrowcrm.lightning.force.com/lightning/o/Case/list?filterName=My_Open_and_Flagged_With_Reminder",
    "SWB (Oracle)": "https://acswb.arrow.com/Swb/",
    "MyConnect": "https://arrow.service-now.com/myconnect?id=myconnect_home",
    "Help_Email": "wireremit@arrow.com"
}

# --- 3. CUSTOM STYLING (Modern UI) ---
st.markdown(f"""
    <style>
        .stApp {{ background-color: #F1F5F9; }}
        .main-header {{
            background: linear-gradient(90deg, #1E293B 0%, #334155 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 25px;
            border-bottom: 5px solid #F97316;
        }}
        .topic-card {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #F97316;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            transition: transform 0.2s;
            height: 100%;
        }}
        .topic-card:hover {{ transform: translateY(-5px); }}
        .email-box {{
            background: #FFF7ED;
            padding: 15px;
            border-radius: 8px;
            border: 1px dashed #F97316;
        }}
    </style>
""", unsafe_allow_html=True)

# --- 4. TOP NAVIGATION & HELP ---
st.markdown('<div class="main-header"><h1>🏹 Arledge Command Center</h1><p>Global Process Repository & Support Hub</p></div>', unsafe_allow_html=True)

col_search, col_help = st.columns([0.7, 0.3])

with col_search:
    query = st.text_input("🔍 Search Knowledge Base", placeholder="Type a system, warehouse code, or collector name...")

with col_help:
    st.markdown("""
        <div class="email-box">
            <strong>🆘 Need Help?</strong><br>
            <small>Email proof of payment or queries to:</small><br>
            <a href="mailto:wireremit@arrow.com?subject=Support Request" style="color:#F97316; font-weight:bold;">Contact Finance Team</a>
        </div>
    """, unsafe_allow_html=True)

# --- 5. DATA LOADING ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv("sop_data.csv").fillna("")
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Training_Link", "Screenshot_URL"])

df = load_data()

# --- 6. INTERACTIVE TOPIC CARDS (Home Screen) ---
if not query:
    st.subheader("📂 Browse by Topic")
    systems = df['System'].unique()
    cols = st.columns(3)
    
    for i, system in enumerate(systems):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="topic-card">
                    <h3>{system}</h3>
                    <p>Standard operating procedures and training for {system} systems.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"View {system} Docs", key=system):
                query = system

# --- 7. SEARCH RESULTS ---
if query:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for idx, row in results.iterrows():
            with st.container():
                st.markdown("---")
                c1, c2 = st.columns([0.6, 0.4])
                with c1:
                    st.success(f"**{row['System']}**: {row['Process']}")
                    st.markdown(row['Instructions'], unsafe_allow_html=True)
                    
                    # Action Row
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if row['Training_Link']:
                            st.link_button("🚀 Start Training", row['Training_Link'], use_container_width=True)
                    with btn_col2:
                        if "Salesforce" in row['System']:
                            st.link_button("Open Salesforce", LINKS['Salesforce'], use_container_width=True)
                
                with c2:
                    if row['Screenshot_URL']:
                        st.image(row['Screenshot_URL'], use_container_width=True)
    else:
        st.warning("No specific SOP found. Try a different keyword.")
