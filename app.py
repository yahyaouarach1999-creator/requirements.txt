import streamlit as st
import pandas as pd
import re
import urllib.parse

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="Arrow Ops Masterclass", layout="wide", page_icon="🏹")

st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; color: #1E293B; font-family: 'Inter', sans-serif; }
    .main-header { text-align: center; padding: 40px 0; background: white; border-bottom: 1px solid #E2E8F0; margin-bottom: 30px; }
    .sop-card { border: 1px solid #E2E8F0; border-radius: 8px; padding: 20px; background: white; margin-bottom: 15px; border-left: 5px solid #3B82F6; transition: 0.2s; }
    .sop-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .system-badge { background: #F1F5F9; color: #475569; padding: 4px 12px; border-radius: 15px; font-size: 11px; font-weight: 700; text-transform: uppercase; }
    .instruction-step { padding: 10px 0; border-bottom: 1px solid #F1F5F9; font-size: 15px; }
    .template-box { background: #F8FAFC; border: 1px dashed #CBD5E1; padding: 15px; border-radius: 8px; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

# --- 2. ACCESS CONTROL (THE GATE) ---
ACCESS_KEY = "Arrow2026"

if 'access_granted' not in st.session_state:
    st.session_state.access_granted = False

if not st.session_state.access_granted:
    st.markdown("<div style='text-align:center; padding-top:100px;'>", unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Arrow_Electronics_Logo.svg", width=200)
    st.title("Operations Terminal Login")
    
    # login logic
    user_pwd = st.text_input("Internal Access Key", type="password")
    if st.button("Unlock System"):
        if user_pwd == ACCESS_KEY:
            st.session_state.access_granted = True
            st.rerun()
        else:
            st.error("Invalid Key. Access Denied.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 3. DATA ENGINE ---
@st.cache_data(ttl=1)
def load_master_data():
    try:
        df = pd.read_csv("sop_data.csv", encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        return df.fillna("")
    except Exception as e:
        st.error(f"Critical Error: Could not read CSV. Check headers. {e}")
        return pd.DataFrame()

df = load_master_data()

# --- 4. NAVIGATION & STATE ---
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'selected_row' not in st.session_state: st.session_state.selected_row = None
if 'last_id' not in st.session_state: st.session_state.last_id = ""

# --- 5. PAGE: SEARCH HOME ---
if st.session_state.view == 'home':
    st.markdown("<div class='main-header'><h1>Arrow Ops Search</h1></div>", unsafe_allow_html=True)
    
    query = st.text_input("", placeholder="Search keywords (RMA, Hold) or enter WEBSO/Case #...", label_visibility="collapsed").strip()

    if query:
        # Smart ID Extraction (extract numbers for email templates)
        id_match = re.search(r"(\d+)", query)
        if id_match: st.session_state.last_id = id_match.group(1)

        # Global Search
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]

        if not results.empty:
            st.write(f"Showing {len(results)} matches:")
            for idx, row in results.iterrows():
                st.markdown(f"<div class='sop-card'>", unsafe_allow_html=True)
                if st.button(f"📄 {row['Process']}", key=f"btn_{idx}"):
                    st.session_state.selected_row = row
                    st.session_state.view = 'detail'
                    st.rerun()
                st.markdown(f"<span class='system-badge'>{row['System']}</span>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No matches found. Try searching by system (e.g., 'Unity') or action (e.g., 'Tax').")
    else:
        # STARTING STATE (Prevents empty screen)
        st.info("👋 Hello! Use the search bar above to find instructions and email templates.")
        st.subheader("Frequent Processes")
        quick_cols = st.columns(3)
        for i, (idx, row) in enumerate(df.head(3).iterrows()):
            if quick_cols[i%3].button(f"📌 {row['Process']}", key=f"quick_{idx}", use_container_width=True):
                st.session_state.selected_row = row
                st.session_state.view = 'detail'
                st.rerun()

# --- 6. PAGE: DETAIL VIEW ---
elif st.session_state.view == 'detail':
    row = st.session_state.selected_row
    if st.button("← Back to Results"):
        st.session_state.view = 'home'
        st.rerun()
    
    st.divider()
    col1, col2 = st.columns([0.6, 0.4])
    
    with col1:
        st.markdown(f"<span class='system-badge'>{row['System']}</span>", unsafe_allow_html=True)
        st.title(row['Process'])
        
        st.subheader("Steps to Complete")
        steps = row['Instructions'].split('<br>')
        for step in steps:
            st.markdown(f"<div class='instruction-step'>{step}</div>", unsafe_allow_html=True)
            
        # --- EMAIL TEMPLATE LOGIC ---
        if "Email_Template" in row and row['Email_Template']:
            st.divider()
            st.subheader("📧 Email Template")
            
            # Fill the template with the ID found during search
            id_val = st.session_state.last_id if st.session_state.last_id else "[ID NUMBER]"
            final_email = row['Email_Template'].replace("[NUMBER]", id_val)
            
            st.markdown(f"<div class='template-box'>{final_email.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
            
            # Outlook Button
            try:
                subject = final_email.split('\n')[0].replace("Subject: ", "")
                body = "\n".join(final_email.split('\n')[1:])
                mail_link = f"mailto:?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
                st.markdown(f'<br><a href="{mail_link}" style="background:#0078d4;color:white;padding:12px 20px;text-decoration:none;border-radius:5px;font-weight:bold;">🚀 Launch Outlook Email</a>', unsafe_allow_html=True)
            except:
                st.caption("Manual copy required for this template.")

    with col2:
        if row['Screenshot_URL']:
            st.subheader("Reference")
            st.image(row['Screenshot_URL'], use_container_width=True)
