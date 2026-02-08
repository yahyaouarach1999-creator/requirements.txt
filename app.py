import streamlit as st
import pandas as pd
import re
import urllib.parse
import base64

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# --- 2. THE PERMANENT LOGO STRING (Base64) ---
# This is the Arrow Logo converted to text so it never breaks
LOGO_IMAGE = "https://www.arrow.com/arrow-logo.png" 

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { background-color: #F8FAFC; }
        
        .header-container {
            display: flex;
            align-items: center;
            background-color: #1E293B;
            padding: 20px 30px;
            border-radius: 12px;
            margin-bottom: 25px;
            border-bottom: 6px solid #F97316;
        }
        .logo-img {
            height: 50px;
            margin-right: 25px;
        }
        .title-text {
            color: white;
            font-size: 45px;
            font-weight: 900;
            font-family: 'Segoe UI', sans-serif;
            letter-spacing: 2px;
            margin: 0;
        }
    </style>
""", unsafe_allow_html=True)

# Render the Header using the direct link and fallback logic
st.markdown(f"""
    <div class="header-container">
        <img src="{LOGO_IMAGE}" class="logo-img">
        <h1 class="title-text">ARLEDGE</h1>
    </div>
""", unsafe_allow_html=True)

st.divider()

# --- 3. SECURITY GATE ---
if 'authorized' not in st.session_state: st.session_state.authorized = False

if not st.session_state.authorized:
    st.info("💻 Arledge Terminal: Restricted Access")
    pwd = st.text_input("Enter Terminal Key", type="password")
    if st.button("Access Granted") or (pwd == "Arrow2026"):
        if pwd == "Arrow2026":
            st.session_state.authorized = True
            st.rerun()
        elif pwd != "":
            st.error("Invalid Key")
    st.stop()

# --- 4. DATA ENGINE ---
@st.cache_data(ttl=1)
def load_data():
    try:
        df = pd.read_csv("sop_data.csv", encoding='utf-8-sig').fillna("")
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Screenshot_URL", "Email_Template", "Last_Updated"])

df = load_data()

# --- 5. STATE & NAVIGATION ---
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'query' not in st.session_state: st.session_state.query = ""

# --- 6. HOME PAGE ---
if st.session_state.view == 'home':
    # Actionable Stats
    c1, c2, c3 = st.columns(3)
    c1.metric("Indexed SOPs", len(df))
    c2.metric("Active Systems", len(df['System'].unique()))
    c3.metric("Email Templates", len(df[df['Email_Template'] != ""]))

    query = st.text_input("🔍 Search Database...", value=st.session_state.query, placeholder="Search by System, ID, or Keywords...").strip()
    st.session_state.query = query

    if query:
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
        
        for idx, row in results.iterrows():
            with st.container():
                st.markdown(f"""
                <div style="background:white; padding:15px; border-radius:10px; border-left:5px solid #F97316; margin-bottom:10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <small style="color:#F97316; font-weight:bold;">{row['System']}</small>
                    <h4 style="margin:0;">{row['Process']}</h4>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"View {row['Process']}", key=f"v_{idx}"):
                    st.session_state.selected = row
                    st.session_state.view = 'detail'
                    st.rerun()
    else:
        st.info("💡 Start by typing a system name or process keyword above.")

# --- 7. DETAIL PAGE ---
elif st.session_state.view == 'detail':
    row = st.session_state.selected
    if st.button("← Back to Results"):
        st.session_state.view = 'home'
        st.rerun()
    
    st.divider()
    l, r = st.columns([0.6, 0.4])
    
    with l:
        st.title(row['Process'])
        st.write(f"**Platform:** `{row['System']}` | **Updated:** {row['Last_Updated']}")
        
        st.markdown("### 📋 Instructions")
        for step in row['Instructions'].split('<br>'):
            st.markdown(f"✅ {step}")
            
        if row['Email_Template']:
            st.divider()
            st.subheader("📧 Smart Email Template")
            
            # Auto-replace [NUMBER] with any digits found in the user's search
            num_match = re.search(r'\d+', st.session_state.query)
            id_val = num_match.group(0) if num_match else "[ID]"
            full_tpl = row['Email_Template'].replace("[NUMBER]", id_val)
            
            # UI Split for Subject/Body
            parts = full_tpl.split('\n', 1)
            subject = parts[0].replace("Subject: ", "") if parts else "Update"
            body = parts[1] if len(parts) > 1 else full_tpl
            
            st.info(f"**Subject:** {subject}")
            st.code(body, language="text")
            
            mailto = f"mailto:?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
            st.markdown(f'<a href="{mailto}" style="background:#F97316;color:white;padding:15px;text-decoration:none;border-radius:8px;font-weight:bold;display:inline-block;">🚀 Launch Outlook</a>', unsafe_allow_html=True)

    with r:
        if row['Screenshot_URL']:
            st.markdown("### 🖼️ Visual Reference")
            st.image(row['Screenshot_URL'], use_container_width=True)
