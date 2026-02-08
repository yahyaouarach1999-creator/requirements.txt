import streamlit as st
import pandas as pd
import re
import urllib.parse

# --- AUTH & DATA LOAD ---
ACCESS_KEY = "Arrow2026"
if 'access' not in st.session_state: st.session_state.access = False

if not st.session_state.access:
    st.title("🏹 Ops Login")
    if st.text_input("Key", type="password") == ACCESS_KEY:
        st.session_state.access = True
        st.rerun()
    st.stop()

@st.cache_data(ttl=1)
def get_data():
    df = pd.read_csv("sop_data.csv", encoding='utf-8-sig')
    df.columns = df.columns.str.strip()
    return df.fillna("")

df = get_data()

# --- SEARCH LOGIC ---
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'query_id' not in st.session_state: st.session_state.query_id = ""

if st.session_state.view == 'home':
    st.title("Arrow Operational Search")
    q = st.text_input("Search keywords or enter WEBSO/Case #").strip()
    
    if q:
        # Extract ID (e.g., if user types WEBSO 12345, extract 12345)
        id_match = re.search(r"(\d+)", q)
        if id_match: st.session_state.query_id = id_match.group(1)
        
        results = df[df.apply(lambda x: x.astype(str).str.contains(q, case=False)).any(axis=1)]
        for idx, row in results.iterrows():
            if st.button(f"📄 {row['Process']} ({row['System']})", key=idx):
                st.session_state.selected = row
                st.session_state.view = 'detail'
                st.rerun()

# --- DETAIL PAGE WITH SMART EMAIL ---
elif st.session_state.view == 'detail':
    row = st.session_state.selected
    if st.button("← Back"):
        st.session_state.view = 'home'
        st.rerun()

    st.header(row['Process'])
    
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        st.subheader("Steps")
        for step in row['Instructions'].split('<br>'):
            st.write(step)
            
        if row['Email_Template']:
            st.divider()
            st.subheader("📧 Email Template")
            
            # Smart Replacement: Put the ID into the template
            final_email = row['Email_Template'].replace("[NUMBER]", st.session_state.query_id)
            
            st.text_area("Live Template:", value=final_email, height=150)
            
            # Outlook Launch Logic
            sub_part = final_email.split("\n\n")[0].replace("Subject: ", "")
            body_part = final_email.split("\n\n")[1] if "\n\n" in final_email else final_email
            
            mail_link = f"mailto:?subject={urllib.parse.quote(sub_part)}&body={urllib.parse.quote(body_part)}"
            st.markdown(f'<a href="{mail_link}" style="background:#0078d4;color:white;padding:10px;text-decoration:none;border-radius:5px;">🚀 Generate Outlook Email</a>', unsafe_allow_html=True)

    with col2:
        st.image(row['Screenshot_URL'])
