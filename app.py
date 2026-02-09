import streamlit as st
import pandas as pd

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="Arledge Command Center", layout="wide", page_icon="🏹")

# --- 2. LINKS & RESOURCES ---
LINKS = {
    "Salesforce": "https://arrowcrm.lightning.force.com/lightning/o/Case/list?filterName=My_Open_and_Flagged_With_Reminder",
    "SWB (Oracle)": "https://acswb.arrow.com/Swb/",
    "MyConnect": "https://arrow.service-now.com/myconnect?id=myconnect_home"
}

# --- 3. CUSTOM STYLING ---
st.markdown(f"""
    <style>
        .stApp {{ background-color: #F8FAFC; }}
        .main-header {{
            background: #1E293B;
            padding: 25px;
            border-radius: 12px;
            color: white;
            text-align: center;
            border-bottom: 5px solid #F97316;
            margin-bottom: 20px;
        }}
        .card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border: 1px solid #E2E8F0;
        }}
    </style>
""", unsafe_allow_html=True)

# --- 4. HEADER ---
st.markdown('<div class="main-header"><h1>🏹 Arledge Command Center</h1><p>Training & Global Support Hub</p></div>', unsafe_allow_html=True)

# --- 5. DATA LOADING (The Link Fix) ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("sop_data.csv")
        # CRITICAL FIX: Strip hidden spaces from ALL columns to prevent 404 errors
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df.fillna("")
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Training_Link", "Screenshot_URL"])

df = load_data()

# --- 6. SEARCH & HELP ---
c1, c2 = st.columns([0.7, 0.3])
with c1:
    query = st.text_input("🔍 Search Knowledge Base", placeholder="Type a system, collector, or process...")
with c2:
    st.info("📬 **Need Help?**\n[Email wireremit@arrow.com](mailto:wireremit@arrow.com)")

# --- 7. TOPIC CARDS (Interactive View) ---
if not query:
    st.subheader("📂 Browse by System")
    systems = df['System'].unique()
    cols = st.columns(len(systems) if len(systems) < 5 else 4)
    for i, sys_name in enumerate(systems):
        with cols[i % len(cols)]:
            if st.button(sys_name, use_container_width=True):
                query = sys_name

# --- 8. RESULTS ---
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
                    
                    # ACTION BUTTONS
                    st.markdown("---")
                    btn1, btn2 = st.columns(2)
                    with btn1:
                        # Fixed URL handling: Ensuring we pass a clean string
                        if row['Training_Link']:
                            st.link_button("🚀 Start Rise 360 Lesson", row['Training_Link'].strip(), type="primary")
                    with btn2:
                        if "Salesforce" in row['System']:
                            st.link_button("Open Live Salesforce", LINKS['Salesforce'])
                        elif "Oracle" in row['System']:
                            st.link_button("Open Live SWB", LINKS['SWB (Oracle)'])
                
                with col_img:
                    if row['Screenshot_URL']:
                        st.image(row['Screenshot_URL'], use_container_width=True)
                st.markdown("---")
    else:
        st.warning(f"No results for '{query}'.")
