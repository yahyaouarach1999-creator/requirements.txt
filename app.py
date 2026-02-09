import streamlit as st
import pandas as pd
import re
import urllib.parse

# --- 1. SETTINGS ---
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# --- 2. DEFINE LOGO FIRST (To avoid NameError) ---
LOGO_SVG = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI0Y5NzMxNiIgZD0iTTEyIDJMMiA3bDEwIDUgMTAtNXYxMEgxMlYyMmw4LTUgNC01Vjd6Ii8+PC9zdmc+"

# --- 3. UI & VISIBILITY FIX ---
# Note the double {{ }} for CSS to work inside an f-string
st.markdown(f"""
    <style>
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        header {{ visibility: hidden; }}
        .stApp {{ background-color: #F8FAFC; }}
        
        .header-container {{
            display: flex;
            align-items: center;
            background-color: #1E293B;
            padding: 15px 25px;
            border-radius: 10px;
            border-bottom: 5px solid #F97316;
            margin-bottom: 20px;
        }}
        .logo-box {{
            background: white;
            padding: 8px;
            border-radius: 5px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .title-text {{
            color: white !important;
            font-size: 40px;
            font-weight: 900;
            margin-left: 20px;
            letter-spacing: 2px;
        }}
        
        /* FIX FOR INVISIBLE TYPING */
        input {{
            color: #000000 !important; /* Black text */
            background-color: #FFFFFF !important; /* White background */
        }}
        label, p, .stMarkdown {{
            color: #1E293B !important;
        }}
    </style>
    
    <div class="header-container">
        <div class="logo-box">
            <img src="{LOGO_SVG}" width="50">
        </div>
        <div class="title-text">ARLEDGE</div>
    </div>
""", unsafe_allow_html=True)

# --- 4. SECURITY GATE ---
if 'authorized' not in st.session_state: 
    st.session_state.authorized = False

if not st.session_state.authorized:
    st.info("🔒 Secure Terminal")
    pwd = st.text_input("Enter Key", type="password")
    if st.button("Unlock") or (pwd == "Arrow2026"):
        if pwd == "Arrow2026":
            st.session_state.authorized = True
            st.rerun()
        elif pwd != "":
            st.error("Invalid")
    st.stop()

# --- 5. DATA ENGINE ---
@st.cache_data(ttl=1)
def load_data():
    try:
        df = pd.read_csv("sop_data.csv", encoding='utf-8-sig').fillna("")
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Screenshot_URL", "Email_Template", "Last_Updated"])

df = load_data()

# --- 6. SEARCH LOGIC ---
st.write("### 🔍 Search Database")
query = st.text_input("Start typing to search SOPs...", placeholder="e.g. Password Reset").strip()

if query:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for idx, row in results.iterrows():
            with st.expander(f"{row['System']} - {row['Process']}"):
                st.markdown(f"**Instructions:**\n{row['Instructions']}")
                if row['Email_Template']:
                    st.code(row['Email_Template'], language="text")
    else:
        st.warning("No matches found.")
