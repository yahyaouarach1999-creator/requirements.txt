import streamlit as st
import pandas as pd
import re
import urllib.parse
import os

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { background-color: #F8FAFC; }
        
        .header-container {
            display: flex;
            align-items: center;
            background-color: #1E293B; /* Deep Slate */
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
            border-bottom: 5px solid #F97316; /* Safety Orange */
        }
        .title-text {
            color: white;
            font-size: 48px;
            font-weight: 800;
            margin-left: 25px;
            font-family: 'Segoe UI', sans-serif;
            letter-spacing: 1px;
        }
        .sop-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 6px solid #F97316;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE BRANDING HEADER ---
col1, col2 = st.columns([0.15, 0.85])

with col1:
    # This checks if you uploaded the logo to GitHub
    if os.path.exists("logo.png"):
        st.image("logo.png", width=160)
    else:
        # Fallback if file is missing
        st.warning("Upload logo.png to GitHub")

with col2:
    st.markdown("<div class='title-text'>ARLEDGE</div>", unsafe_allow_html=True)

st.divider()

# --- 3. SECURITY GATE ---
if 'authorized' not in st.session_state: st.session_state.authorized = False

if not st.session_state.authorized:
    st.info("💻 Arledge System: Development Environment")
    pwd = st.text_input("Enter Terminal Key", type="password")
    if st.button("Access Granted") or (pwd == "Arrow2026"):
        if pwd == "Arrow2026":
            st.session_state.authorized = True
            st.rerun()
        elif pwd != "":
            st.error("Invalid Key")
    st.stop()

# --- 4. DATA ENGINE (UTF-8 FOR SYMBOLS) ---
@st.cache_data(ttl=1)
def load_data():
    try:
        # utf-8-sig ensures symbols like é, à, and $ work
        df = pd.read_csv("sop_data.csv", encoding='utf-8-sig').fillna("")
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Screenshot_URL", "Email_Template", "Last_Updated"])

df = load_data()

# --- 5. SEARCH & NAVIGATION ---
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'query' not in st.session_state: st.session_state.query = ""

if st.session_state.view == 'home':
    query = st.text_input("🔍 Search Terminal...", value=st.session_state.query, placeholder="e.g. Unity, RMA, $ Recovery").strip()
    st.session_state.query = query

    if query:
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
        
        for idx, row in results.iterrows():
            st.markdown(f"""
            <div class="sop-card">
                <p style="color:#F97316; font-size:12px; font-weight:bold; margin-bottom:5px;">{row['System']}</p>
                <h3 style="margin-top:0;">{row['Process']}</h3>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔍 Open {row['Process']}", key=f"v_{idx}"):
                st.session_state.selected = row
                st.session_state.view = 'detail'
                st.rerun()
    else:
        st.write("### Welcome, Developer")
        st.caption(f"Indexing {len(df)} Active Processes")

elif st.session_state.view == 'detail':
    row = st.session_state.selected
    if st.button("← Back to Results"):
        st.session_state.view = 'home'
        st.rerun()
    
    st.divider()
    l, r = st.columns([0.6, 0.4])
    
    with l:
        st.title(row['Process'])
        st.write(f"**Platform:** `{row['System']}`")
        
        st.markdown("### 📋 Instructions")
        for step in row['Instructions'].split('<br>'):
            st.markdown(f"🔸 {step}")
            
        if row['Email_Template']:
            st.subheader("📧 Smart Template")
            st.text_area("Live Template:", value=row['Email_Template'], height=200)
            
            # Smart Outlook Link
            sub = row['Email_Template'].split('\n')[0].replace("Subject: ", "")
            mailto = f"mailto:?subject={urllib.parse.quote(sub)}"
            st.markdown(f'<a href="{mailto}" style="background:#F97316;color:white;padding:15px;text-decoration:none;border-radius:8px;font-weight:bold;">🚀 Launch Outlook</a>', unsafe_allow_html=True)

    with r:
        if row['Screenshot_URL']:
            st.image(row['Screenshot_URL'], caption="Reference Screenshot")
