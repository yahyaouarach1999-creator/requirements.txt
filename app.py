import streamlit as st
import pandas as pd
import re
import urllib.parse

# --- 1. SETUP ---
st.set_page_config(page_title="Arledge", layout="wide", page_icon="🏹")

# --- 2. CLEAN BRANDING SECTION ---
col1, col2 = st.columns([0.15, 0.85])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Arrow_Electronics_Logo.svg", width=140)
with col2:
    st.markdown("<h1 style='margin-top: 10px; font-size: 45px;'>ARLEDGE</h1>", unsafe_allow_html=True)

st.divider()

# --- 3. SECURITY GATE ---
if 'authorized' not in st.session_state: st.session_state.authorized = False

if not st.session_state.authorized:
    st.markdown("<div style='text-align:center; padding-top:50px;'>", unsafe_allow_html=True)
    st.write("### Secure Internal Access")
    pwd = st.text_input("Enter Access Key", type="password")
    if st.button("Unlock"):
        if pwd == "Arrow2026":
            st.session_state.authorized = True
            st.rerun()
        else:
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

# --- 5. STATE MANAGEMENT ---
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'search_query' not in st.session_state: st.session_state.search_query = ""

# --- 6. HOME PAGE (SEARCH) ---
if st.session_state.view == 'home':
    # Search input that remembers what you typed
    query = st.text_input(
        "", 
        value=st.session_state.search_query, 
        placeholder="Search keywords, systems, or ID #...",
        label_visibility="collapsed"
    ).strip()
    
    st.session_state.search_query = query

    if query:
        # Filter Logic
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
        
        if not results.empty:
            for idx, row in results.iterrows():
                with st.container():
                    c_a, c_b = st.columns([0.85, 0.15])
                    c_a.markdown(f"### {row['Process']}")
                    c_a.markdown(f"**System:** `{row['System']}` | Updated: `{row[df.columns[-1]]}`")
                    if c_b.button("View Details", key=f"v_{idx}"):
                        st.session_state.selected = row
                        st.session_state.view = 'detail'
                        st.rerun()
                    st.write("---")
        else:
            st.warning("No matches found in Arledge database.")
    else:
        st.info("💡 Type a keyword above to start searching.")

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
        st.write(f"**System:** {row['System']}")
        
        st.subheader("Instructions")
        for step in row['Instructions'].split('<br>'):
            st.markdown(f"🔹 {step}")
            
        if row['Email_Template']:
            st.divider()
            st.subheader("📧 Email Template")
            # Extract number from search for the template
            num_match = re.search(r'\d+', st.session_state.search_query)
            id_val = num_match.group(0) if num_match else "[ID]"
            tpl = row['Email_Template'].replace("[NUMBER]", id_val)
            
            st.text_area("Template:", value=tpl, height=180)
            
            # Outlook Link
            sub = tpl.split('\n')[0].replace("Subject: ", "")
            body = "\n".join(tpl.split('\n')[1:])
            mailto = f"mailto:?subject={urllib.parse.quote(sub)}&body={urllib.parse.quote(body)}"
            st.markdown(f'<a href="{mailto}" style="background:#F97316;color:white;padding:12px;text-decoration:none;border-radius:8px;font-weight:bold;">🚀 Open Outlook</a>', unsafe_allow_html=True)

    with r:
        if row['Screenshot_URL']:
            st.image(row['Screenshot_URL'], use_container_width=True)
