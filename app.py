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
        
        /* Branding Header */
        .header-container {
            display: flex;
            align-items: center;
            background-color: #1E293B;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
            border-bottom: 5px solid #F97316;
        }
        .title-text {
            color: white;
            font-size: 48px;
            font-weight: 800;
            margin-left: 25px;
            font-family: 'Segoe UI', sans-serif;
        }
        /* SOP Cards */
        .sop-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 6px solid #F97316;
            margin-bottom: 5px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        /* Template Box */
        .template-box {
            background-color: #F1F5F9;
            padding: 15px;
            border-radius: 8px;
            border: 1px dashed #64748B;
            font-family: monospace;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE BRANDING HEADER ---
col_logo, col_title = st.columns([0.15, 0.85])

with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=160)
    else:
        st.warning("Upload logo.png")

with col_title:
    st.markdown("<div class='title-text'>ARLEDGE</div>", unsafe_allow_html=True)

st.divider()

# --- 3. SECURITY GATE ---
if 'authorized' not in st.session_state: st.session_state.authorized = False

if not st.session_state.authorized:
    st.info("💻 Arledge System: Secure Development Mode")
    pwd = st.text_input("Terminal Key", type="password")
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
        # utf-8-sig handles symbols like é, à, and $
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
    # Quick Stats
    s1, s2, s3 = st.columns(3)
    s1.metric("Active SOPs", len(df))
    s2.metric("Systems", len(df['System'].unique()))
    s3.metric("Smart Templates", len(df[df['Email_Template'] != ""]))

    query = st.text_input("🔍 Search Terminal...", value=st.session_state.query, placeholder="e.g. Unity, RMA, $ Recovery").strip()
    st.session_state.query = query

    if query:
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
        
        for idx, row in results.iterrows():
            st.markdown(f"""<div class="sop-card">
                <p style="color:#F97316; font-size:12px; font-weight:bold; margin-bottom:2px;">{row['System']}</p>
                <h3 style="margin-top:0;">{row['Process']}</h3>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Open Details: {row['Process']}", key=f"v_{idx}"):
                st.session_state.selected = row
                st.session_state.view = 'detail'
                st.rerun()
    else:
        st.write("### Ready for Input")
        st.caption("Awaiting process search or new CSV data...")

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
            
            # Extract ID from search query if possible
            num_match = re.search(r'\d+', st.session_state.query)
            id_val = num_match.group(0) if num_match else "[NUMBER]"
            full_tpl = row['Email_Template'].replace("[NUMBER]", id_val)
            
            # UI Formatting
            parts = full_tpl.split('\n', 1)
            subject = parts[0].replace("Subject: ", "") if parts else "Update"
            body = parts[1] if len(parts) > 1 else full_tpl
            
            st.info(f"**Subject:** {subject}")
            st.code(body, language="text")
            
            mailto = f"mailto:?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
            st.markdown(f'<a href="{mailto}" style="background:#F97316;color:white;padding:15px;text-decoration:none;border-radius:8px;font-weight:bold;display:inline-block;">🚀 Launch Outlook</a>', unsafe_allow_html=True)

    with r:
        if row['Screenshot_URL']:
            st.markdown("### 🖼️ Reference")
            st.image(row['Screenshot_URL'], use_container_width=True)
