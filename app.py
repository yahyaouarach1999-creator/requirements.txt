import streamlit as st
import pandas as pd
import re
import urllib.parse

# --- 1. CONFIG & INTERFACE THEME ---
st.set_page_config(page_title="Arledge Knowledge Terminal", layout="wide", page_icon="🏹")

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #1E293B; }
    .arledge-banner { 
        text-align: center; padding: 40px; 
        background: linear-gradient(90deg, #1E293B 0%, #334155 100%); 
        color: white; border-radius: 15px; margin-bottom: 25px;
    }
    .stat-box {
        background: #F8FAFC; padding: 15px; border-radius: 10px;
        text-align: center; border-bottom: 4px solid #F97316;
    }
    .sop-card { 
        border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; 
        background: white; margin-bottom: 12px; border-left: 6px solid #F97316;
        transition: 0.2s;
    }
    .sop-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .verified-badge { color: #10B981; font-weight: bold; font-size: 14px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 2. THE SECURITY GATE ---
if 'authorized' not in st.session_state: st.session_state.authorized = False

if not st.session_state.authorized:
    st.markdown("<div style='text-align:center; padding-top:100px;'>", unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Arrow_Electronics_Logo.svg", width=250)
    st.title("Arledge Knowledge Terminal")
    st.write("Secure Internal Access Only")
    
    pwd = st.text_input("Enter Access Key", type="password")
    if st.button("Unlock Terminal") or (pwd == "Arrow2026"):
        if pwd == "Arrow2026":
            st.session_state.authorized = True
            st.rerun()
        elif pwd != "":
            st.error("Invalid Key")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 3. DATA ARCHITECTURE ---
@st.cache_data(ttl=1)
def load_arledge_data():
    try:
        # Load CSV and ensure headers are clean
        df = pd.read_csv("sop_data.csv", encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        return df.fillna("")
    except:
        # Fallback if file is missing
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Screenshot_URL", "Email_Template", "Last_Updated"])

df = load_arledge_data()

# --- 4. NAVIGATION STATE ---
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'search_id' not in st.session_state: st.session_state.search_id = ""

# --- 5. SEARCH HOME PAGE ---
if st.session_state.view == 'home':
    st.markdown("<div class='arledge-banner'><h1>🏹 Arledge Knowledge Summary</h1><p>Arrow Electronics Operations Repository</p></div>", unsafe_allow_html=True)
    
    # Dashboard Stats
    s1, s2, s3 = st.columns(3)
    s1.markdown(f"<div class='stat-box'><h3>{len(df)}</h3><p>Total SOPs</p></div>", unsafe_allow_html=True)
    s2.markdown(f"<div class='stat-box'><h3>{len(df['System'].unique())}</h3><p>Systems Indexed</p></div>", unsafe_allow_html=True)
    s3.markdown(f"<div class='stat-box'><h3>{len(df[df['Email_Template'] != ''])}</h3><p>Email Templates</p></div>", unsafe_allow_html=True)
    
    st.write("---")
    query = st.text_input("", placeholder="Search by system, keyword, or WEBSO/Case #...", label_visibility="collapsed").strip()

    if query:
        # Extract ID for dynamic emails
        nums = re.findall(r'\d+', query)
        if nums: st.session_state.search_id = nums[0]

        # Fuzzy search logic
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
        
        if not results.empty:
            for idx, row in results.iterrows():
                st.markdown("<div class='sop-card'>", unsafe_allow_html=True)
                col_a, col_b = st.columns([0.8, 0.2])
                col_a.markdown(f"### {row['Process']}")
                col_a.markdown(f"**System:** `{row['System']}` | Updated: `{row['Last_Updated']}`")
                if col_b.button("View SOP", key=f"btn_{idx}"):
                    st.session_state.selected = row
                    st.session_state.view = 'detail'
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        else:
