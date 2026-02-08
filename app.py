import streamlit as st
import pandas as pd
import re
import urllib.parse

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# Custom CSS for a professional "Terminal" look
st.markdown("""
    <style>
        /* Hide default Streamlit clutter */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Main App Background */
        .stApp { background-color: #F8FAFC; }

        /* Header Styling */
        .header-container {
            display: flex;
            align-items: center;
            background-color: #1E293B; /* Deep Slate */
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 25px;
            border-bottom: 5px solid #F97316; /* Arrow Orange */
        }
        .logo-img { width: 120px; margin-right: 20px; filter: brightness(0) invert(1); }
        .title-text {
            color: white;
            font-size: 42px;
            font-weight: 800;
            letter-spacing: 2px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* SOP Cards */
        .sop-card {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            border-left: 5px solid #F97316;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE BRANDING HEADER ---
# This uses a robust URL and a CSS container to prevent "broken" layouts
st.markdown(f"""
    <div class="header-container">
        <img src="https://www.arrow.com/arrow-logo.png" class="logo-img">
        <div class="title-text">ARLEDGE</div>
    </div>
""", unsafe_allow_html=True)

# --- 3. SECURITY GATE ---
if 'authorized' not in st.session_state: st.session_state.authorized = False

if not st.session_state.authorized:
    st.info("🔒 Secure Terminal: Development Mode")
    pwd = st.text_input("Access Key", type="password")
    if st.button("Unlock System"):
        if pwd == "Arrow2026":
            st.session_state.authorized = True
            st.rerun()
        else:
            st.error("Invalid Credentials")
    st.stop()

# --- 4. DATA ENGINE ---
@st.cache_data(ttl=1)
def load_data():
    try:
        # encoding='utf-8-sig' handles special characters like é, à, and symbols
        df = pd.read_csv("sop_data.csv", encoding='utf-8-sig').fillna("")
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Screenshot_URL", "Email_Template", "Last_Updated"])

df = load_data()

# --- 5. SEARCH & STATE ---
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'query' not in st.session_state: st.session_state.query = ""

if st.session_state.view == 'home':
    # Search with a clear label
    query = st.text_input("🔍 Search Database (Unity, Finance, etc.)", value=st.session_state.query).strip()
    st.session_state.query = query

    if query:
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
        
        if not results.empty:
            for idx, row in results.iterrows():
                st.markdown(f"""
                <div class="sop-card">
                    <span style="color:#F97316; font-weight:bold;">{row['System']}</span>
                    <h3>{row['Process']}</h3>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Open Details for {row['Process']}", key=f"v_{idx}"):
                    st.session_state.selected = row
                    st.session_state.view = 'detail'
                    st.rerun()
        else:
            st.warning("No matches found.")
    else:
        st.write("### Welcome to Arledge Development")
        st.caption("Active Systems: " + ", ".join(df['System'].unique()))

elif st.session_state.view == 'detail':
    row = st.session_state.selected
    if st.button("← Back to Results"):
        st.session_state.view = 'home'
        st.rerun()
    
    st.divider()
    col_l, col_r = st.columns([0.6, 0.4])
    
    with col_l:
        st.title(row['Process'])
        st.write(f"**System:** `{row['System']}`")
        
        st.subheader("Action Steps")
        for step in row['Instructions'].split('<br>'):
            st.markdown(f"✅ {step}")
            
        if row['Email_Template']:
            st.subheader("📧 Smart Template")
            tpl = row['Email_Template']
            st.text_area("Template:", value=tpl, height=200)
            
            # Outlook Button
            sub = tpl.split('\n')[0]
            mailto = f"mailto:?subject={urllib.parse.quote(sub)}"
            st.markdown(f'<a href="{mailto}" style="background:#F97316; color:white; padding:15px; text-decoration:none; border-radius:5px; font-weight:bold;">Launch Outlook</a>', unsafe_allow_html=True)

    with col_r:
        if row['Screenshot_URL']:
            st.image(row['Screenshot_URL'], caption="Reference Image")
