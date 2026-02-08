import streamlit as st
import pandas as pd
import re
import urllib.parse

# --- 1. CONFIG & SYSTEM THEME ---
st.set_page_config(page_title="Arrow Ops Masterclass", layout="wide", page_icon="🏹")

st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; color: #1E293B; font-family: 'Inter', sans-serif; }
    .search-container { text-align: center; padding: 40px 0 20px 0; background: white; border-bottom: 1px solid #E2E8F0; }
    .sop-card { border: 1px solid #E2E8F0; border-radius: 6px; padding: 18px; background: white; margin-bottom: 12px; border-left: 4px solid #94A3B8; }
    .sop-card:hover { border-left: 4px solid #3B82F6; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
    .system-badge { background: #F1F5F9; color: #475569; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 700; text-transform: uppercase; }
    .instruction-step { padding: 10px 0; border-bottom: 1px solid #F1F5F9; font-size: 15px; color: #334155; }
    .help-box { background: #EFF6FF; border: 1px solid #BFDBFE; padding: 15px; border-radius: 8px; margin-top: 20px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
@st.cache_data(ttl=1)
def load_data():
    try:
        df = pd.read_csv("sop_data.csv", encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        return df.fillna("")
    except Exception as e:
        st.error(f"Error connecting to CSV: {e}")
        return pd.DataFrame()

df = load_data()

# --- 3. SESSION STATE ---
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'selected_row' not in st.session_state: st.session_state.selected_row = None
if 'history' not in st.session_state: st.session_state.history = []

# --- 4. SIDEBAR: STATUS & HELP ---
with st.sidebar:
    st.title("🏹 Ops Command")
    st.divider()
    
    st.subheader("🌐 System Status")
    st.markdown("🟢 Unity: **Online**")
    st.markdown("🟢 SFDC: **Online**")
    st.markdown("🟡 Oracle: **Slow Response**")
    
    st.divider()
    st.subheader("🕒 Recent Items")
    for item in reversed(st.session_state.history[-5:]):
        st.caption(f"ID: {item}")

    st.divider()
    with st.expander("🆘 Need Help?"):
        st.write("Contact the Training Lead if you find an error in the SOPs.")
        lead_email = "training.lead@arrow.com" # CHANGE THIS
        subject = urllib.parse.quote("SOP Feedback / Error Report")
        body = urllib.parse.quote("Hi Team,\n\nI found an issue with the following SOP:\n[Describe issue here]")
        st.markdown(f'<a href="mailto:{lead_email}?subject={subject}&body={body}" style="background:#3B82F6; color:white; padding:10px; border-radius:5px; text-decoration:none; display:block; text-align:center;">📧 Email Training Lead</a>', unsafe_allow_html=True)

# --- 5. PAGE 1: SEARCH PORTAL ---
if st.session_state.view == 'home':
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)
    st.title("Arrow Operational Repository")
    query = st.text_input("", placeholder="Search keywords (RMA, Hold) or enter ID (WEBSO, 00123...)", label_visibility="collapsed").strip()
    st.markdown("</div>", unsafe_allow_html=True)

    if query:
        is_webso = re.search(r"WEBSO\s*(\d+)", query, re.IGNORECASE)
        is_case = re.search(r"\b\d{8}\b", query)
        if (is_webso or is_case) and query not in st.session_state.history:
            st.session_state.history.append(query)

        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]

        if not results.empty:
            if is_webso: st.link_button(f"🚀 Open Order {is_webso.group(1)} in Unity", f"https://unity.arrow.com/orders/{is_webso.group(1)}")
            if is_case: st.link_button(f"🚀 Open Case {is_case.group(0)} in Salesforce", f"https://arrow.my.salesforce.com/{is_case.group(0)}")

            st.write(f"Matches found ({len(results)}):")
            for idx, row in results.iterrows():
                with st.container():
                    st.markdown(f"<div class='sop-card'>", unsafe_allow_html=True)
                    if st.button(f"{row['Process']}", key=f"btn_{idx}"):
                        st.session_state.selected_row = row
                        st.session_state.view = 'detail'
                        st.rerun()
                    st.markdown(f"<span class='system-badge'>{row['System']}</span>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No matches found. Check spelling or try a broader term.")

# --- 6. PAGE 2: DETAIL VIEW ---
elif st.session_state.view == 'detail':
    row = st.session_state.selected_row
    if st.button("← Back to Results"):
        st.session_state.view = 'home'
        st.rerun()
    
    st.divider()
    col1, col2 = st.columns([0.65, 0.35])
    
    with col1:
        st.markdown(f"<span class='system-badge'>{row['System']}</span>", unsafe_allow_html=True)
        st.title(row['Process'])
        steps = row['Instructions'].split('<br>')
        for step in steps:
            st.markdown(f"<div class='instruction-step'>{step}</div>", unsafe_allow_html=True)
            
    with col2:
        if row['Screenshot_URL']:
            st.image(row['Screenshot_URL'], caption="Interface Preview", use_container_width=True)
        
        # In-page report button
        st.markdown("<div class='help-box'>", unsafe_allow_html=True)
        st.write("**Is this SOP incorrect?**")
        rep_sub = urllib.parse.quote(f"Error Report: {row['Process']}")
        st.markdown(f'<a href="mailto:training.lead@arrow.com?subject={rep_sub}" style="color:#2563EB; font-weight:bold;">Report Issue →</a>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
