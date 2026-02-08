import streamlit as st
import pandas as pd
import re

# 1. PAGE SETUP
st.set_page_config(page_title="Arrow Ops Search", layout="wide")

# 2. ACCESS CONTROL
ACCESS_KEY = "Arrow2026"

if 'access_granted' not in st.session_state:
    st.session_state.access_granted = False

if not st.session_state.access_granted:
    st.markdown("<br><br><div style='text-align:center'>", unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Arrow_Electronics_Logo.svg", width=200)
    st.title("Secure Ops Portal")import streamlit as st
import pandas as pd
import urllib.parse

# ... [Previous Login/Data Loading Code remains same] ...

# --- NEW DETAIL PAGE LOGIC ---
elif st.session_state.view == 'detail':
    row = st.session_state.selected
    if st.button("← Back to Search"):
        st.session_state.view = 'home'
        st.rerun()
    
    st.divider()
    col1, col2 = st.columns([0.6, 0.4])

    with col1:
        st.title(row['Process'])
        st.caption(f"System: {row['System']}")
        
        st.subheader("Action Steps")
        for step in row['Instructions'].split('<br>'):
            st.write(step)

        # --- NEW EMAIL TEMPLATE SECTION ---
        if "Email_Template" in row and row['Email_Template']:
            st.divider()
            st.subheader("📧 Communication Template")
            
            # Display the template in a code box for easy copying
            st.text_area("Copy/Paste Template:", value=row['Email_Template'], height=150)
            
            # Create a "Launch Outlook" button
            template_text = row['Email_Template']
            # Basic parsing to separate Subject from Body for the mailto link
            if "Subject:" in template_text:
                parts = template_text.split("\n\n", 1)
                subject = parts[0].replace("Subject: ", "")
                body = parts[1] if len(parts) > 1 else ""
            else:
                subject = "Internal Inquiry"
                body = template_text
            
            mail_link = f"mailto:?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
            st.markdown(f'<a href="{mail_link}" style="background-color:#0078d4; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;">🚀 Open New Email in Outlook</a>', unsafe_allow_html=True)

    with col2:
        if row['Screenshot_URL']:
            st.image(row['Screenshot_URL'], caption="System Visual Reference")
    user_key = st.text_input("Enter Access Key", type="password")
    if st.button("Unlock"):
        if user_key == ACCESS_KEY:
            st.session_state.access_granted = True
            st.rerun()
        else:
            st.error("Access Denied")
    st.stop()

# 3. LOAD DATA
@st.cache_data(ttl=1)
def load_data():
    try:
        df = pd.read_csv("sop_data.csv").fillna("")
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Screenshot_URL"])

df = load_data()

# 4. NAVIGATION STATE
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'selected' not in st.session_state: st.session_state.selected = None

# 5. HEADER & SEARCH (Visible after login)
st.markdown("<div style='text-align: center; padding: 20px;'><h1>🏹 Arrow Operational Search</h1></div>", unsafe_allow_html=True)

# THE SEARCH BOX
query = st.text_input("", placeholder="Search keywords (e.g., Unity, RMA, Hold)...").strip()

# 6. RESULTS LOGIC
if st.session_state.view == 'home':
    if query:
        # Filter data based on search
        results = df[df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)]
        
        if not results.empty:
            st.write(f"Found {len(results)} matches:")
            for idx, row in results.iterrows():
                if st.button(f"📄 {row['Process']} ({row['System']})", key=f"res_{idx}"):
                    st.session_state.selected = row
                    st.session_state.view = 'detail'
                    st.rerun()
        else:
            st.warning("No matches found. Try a different keyword.")
    else:
        # THIS PREVENTS THE "EMPTY" SCREEN
        st.divider()
        st.subheader("💡 Suggestions")
        st.info("Type 'Unity' to see Order flows, or 'Finance' for Credit tasks.")
        
        # Show the first 3 items by default so it's not empty
        st.write("Top Processes:")
        for idx, row in df.head(3).iterrows():
            if st.button(f"📌 {row['Process']}", key=f"top_{idx}"):
                st.session_state.selected = row
                st.session_state.view = 'detail'
                st.rerun()

# 7. DETAIL PAGE (Another Page)
elif st.session_state.view == 'detail':
    row = st.session_state.selected
    if st.button("← Back to Search"):
        st.session_state.view = 'home'
        st.rerun()
    
    st.divider()
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.header(row['Process'])
        st.caption(f"System: {row['System']}")
        # Split by <br> for clean lines
        for step in row['Instructions'].split('<br>'):
            st.write(step)
    with col2:
        if row['Screenshot_URL']:
            st.image(row['Screenshot_URL'], caption="System View")
