import streamlit as st
import pandas as pd
import re
import urllib.parse

# --- 1. SETUP ---
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

import streamlit as st
import pandas as pd
import re
import urllib.parse

# --- 1. SETUP ---
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# --- 2. THE PERMANENT LOGO FIX (Base64) ---
# This is a tiny version of the Arrow logo embedded as data
arrow_logo_base64 = "https://upload.wikimedia.org/wikipedia/commons/e/e0/Arrow_Electronics_Logo.svg"

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .logo-text-container {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-top: -30px;
        }
        .arledge-title {
            font-size: 50px;
            font-weight: 800;
            color: #1E293B;
            font-family: 'Helvetica', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Layout using HTML for perfect alignment
st.markdown(f"""
    <div class="logo-text-container">
        <img src="{arrow_logo_base64}" width="150">
        <div class="arledge-title">ARLEDGE</div>
    </div>
""", unsafe_allow_html=True)

st.divider()

# --- 3. SECURITY GATE ---
if 'authorized' not in st.session_state: st.session_state.authorized = False

if not st.session_state.authorized:
    st.markdown("<div style='text-align:center; padding-top:50px;'>", unsafe_allow_html=True)
    st.write("### 🔒 Secure Internal Access")
    pwd = st.text_input("Enter Access Key", type="password")
    if st.button("Unlock Terminal") or (pwd == "Arrow2026"):
        if pwd == "Arrow2026":
            st.session_state.authorized = True
            st.rerun()
        elif pwd != "":
            st.error("Invalid Key")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 4. DATA LOAD ---
@st.cache_data(ttl=1)
def load_data():
    try:
        df = pd.read_csv("sop_data.csv", encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        return df.fillna("")
    except:
        return pd.DataFrame()

df = load_data()

# --- 5. SEARCH & RESULTS ---
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'search_query' not in st.session_state: st.session_state.search_query = ""

if st.session_state.view == 'home':
    query = st.text_input("", value=st.session_state.search_query, placeholder="Search Systems or SOPs...", label_visibility="collapsed").strip()
    st.session_state.search_query = query

    if query:
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
        for idx, row in results.iterrows():
            with st.container():
                c_a, c_b = st.columns([0.8, 0.2])
                c_a.markdown(f"### {row['Process']}")
                c_a.write(f"System: `{row['System']}`")
                if c_b.button("View", key=f"btn_{idx}"):
                    st.session_state.selected = row
                    st.session_state.view = 'detail'
                    st.rerun()
                st.write("---")
    else:
        st.info("💡 Type a keyword above (e.g., Unity, Venlo, Oracle) to search.")

elif st.session_state.view == 'detail':
    row = st.session_state.selected
    if st.button("← Back"):
        st.session_state.view = 'home'
        st.rerun()
    
    st.title(row['Process'])
    st.write(f"**System:** {row['System']}")
    st.markdown("### Steps")
    for step in row['Instructions'].split('<br>'):
        st.markdown(f"🔹 {step}")

# --- 3. SECURITY GATE ---
if 'authorized' not in st.session_state: st.session_state.authorized = False

if not st.session_state.authorized:
    st.markdown("<div style='text-align:center; padding-top:50px;'>", unsafe_allow_html=True)
    st.write("### 🔒 Secure Internal Access")
    pwd = st.text_input("Enter Access Key", type="password")
    if st.button("Unlock Terminal"):
        if pwd == "Arrow2026":
            st.session_state.authorized = True
            st.rerun()
        else:
            st.error("Invalid Key")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 4. DATA ENGINE ---
@st.cache_data(ttl=1)
def load_data():
    try:
        # Load your CSV
        df = pd.read_csv("sop_data.csv", encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        # Add Last_Updated if it's missing from your file
        if 'Last_Updated' not in df.columns:
            df['Last_Updated'] = "2026-02-08"
        return df.fillna("")
    except:
        return pd.DataFrame()

df = load_data()

# --- 5. STATE MANAGEMENT ---
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'search_query' not in st.session_state: st.session_state.search_query = ""

# --- 6. HOME PAGE (SEARCH) ---
if st.session_state.view == 'home':
    # Search input that remembers its value
    query = st.text_input(
        "Search Box", 
        value=st.session_state.search_query, 
        placeholder="Type System (Unity) or Keyword (RMA)...",
        label_visibility="collapsed"
    ).strip()
    
    st.session_state.search_query = query

    if query:
        # Filter Logic (Searches across all columns)
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
        
        if not results.empty:
            for idx, row in results.iterrows():
                with st.container():
                    c_a, c_b = st.columns([0.85, 0.15])
                    c_a.markdown(f"### {row['Process']}")
                    c_a.markdown(f"**System:** `{row['System']}` | Updated: `{row['Last_Updated']}`")
                    if c_b.button("View Detail", key=f"v_{idx}"):
                        st.session_state.selected = row
                        st.session_state.view = 'detail'
                        st.rerun()
                    st.write("---")
        else:
            st.warning("No matches found in the Arledge database.")
    else:
        st.info("💡 Ready. Type a keyword above to find an SOP.")
        # Optional: Show a few recent items
        for idx, row in df.head(3).iterrows():
            st.write(f"🔹 **{row['System']}**: {row['Process']}")

# --- 7. DETAIL PAGE ---
elif st.session_state.view == 'detail':
    row = st.session_state.selected
    
    # BACK BUTTON (Restores the home view with your previous search)
    if st.button("← Back to Results"):
        st.session_state.view = 'home'
        st.rerun()
    
    st.divider()
    l, r = st.columns([0.6, 0.4])
    
    with l:
        st.title(row['Process'])
        st.write(f"**System:** {row['System']} | **Revised:** {row['Last_Updated']}")
        
        st.subheader("Action Steps")
        steps = row['Instructions'].split('<br>')
        for step in steps:
            st.markdown(f"🔹 {step}")
            
        if row['Email_Template']:
            st.divider()
            st.subheader("📧 Smart Email Template")
            
            # Logic to extract a number from your search query for the template
            num_match = re.search(r'\d+', st.session_state.search_query)
            id_val = num_match.group(0) if num_match else "[ID]"
            tpl = row['Email_Template'].replace("[NUMBER]", id_val)
            
            st.text_area("Template Text:", value=tpl, height=200)
            
            # Outlook Launch Logic
            lines = tpl.split('\n')
            subject = lines[0].replace("Subject: ", "") if lines else "Update"
            body = "\n".join(lines[1:]) if len(lines) > 1 else tpl
            
            mailto = f"mailto:?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
            st.markdown(f'<a href="{mailto}" style="background:#F97316;color:white;padding:12px 24px;text-decoration:none;border-radius:8px;font-weight:bold;display:inline-block;">🚀 Launch Outlook</a>', unsafe_allow_html=True)

    with r:
        if row['Screenshot_URL']:
            st.markdown("### Visual Reference")
            st.image(row['Screenshot_URL'], use_container_width=True)
