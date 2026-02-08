import streamlit as st
import pandas as pd
import re

# --- CONFIG & THEME ---
st.set_page_config(page_title="Arrow Ops Terminal", layout="wide", page_icon="🏹")

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #202124; font-family: 'Segoe UI', Tahoma, sans-serif; }
    .search-container { text-align: center; padding-top: 80px; padding-bottom: 20px; }
    .sop-card { border: 1px solid #DADCE0; border-radius: 8px; padding: 20px; background: white; margin-bottom: 10px; transition: 0.3s; }
    .sop-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-color: #4285F4; }
    .system-badge { background: #F1F3F4; color: #5F6368; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; text-transform: uppercase; }
    .instruction-step { line-height: 1.6; color: #3C4043; font-size: 15px; margin-bottom: 8px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data(ttl=1)
def load_arrow_data():
    try:
        # utf-8-sig handles Excel-saved CSVs, strip() removes hidden spaces in headers
        df = pd.read_csv("sop_data.csv", encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        return df.fillna("")
    except Exception as e:
        st.error(f"Data Error: {e}")
        return pd.DataFrame()

df = load_arrow_data()

# --- STATE MANAGEMENT ---
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'selected_row' not in st.session_state: st.session_state.selected_row = None
if 'history' not in st.session_state: st.session_state.history = []

# --- SIDEBAR HISTORY ---
with st.sidebar:
    st.title("🏹 Recent")
    if not st.session_state.history:
        st.caption("No recent searches")
    for item in reversed(st.session_state.history[-10:]):
        if st.button(f"🕒 {item}", use_container_width=True):
            st.session_state.view = 'home'
            # Forces re-run with this query via session state if needed

# --- PAGE 1: SEARCH HOME ---
if st.session_state.view == 'home':
    st.markdown("<div class='search-container'><h1>Arrow Operational Search</h1></div>", unsafe_allow_html=True)
    
    query = st.text_input("", placeholder="Enter WEBSO, Case #, or Keyword (e.g. 'RMA', 'Hold')...", key="search_input").strip()

    if query:
        # Detect WEBSO or SFDC Case
        is_webso = re.search(r"WEBSO\s*(\d+)", query, re.IGNORECASE)
        is_case = re.search(r"\b\d{8}\b", query)

        if (is_webso or is_case) and query not in st.session_state.history:
            st.session_state.history.append(query)

        # Smart Filtering
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]

        if not results.empty:
            # Action Buttons for References
            if is_webso:
                st.link_button(f"🚀 Open Order {is_webso.group(1)} in Unity", f"https://unity.arrow.com/orders/{is_webso.group(1)}")
            elif is_case:
                st.link_button(f"🚀 Open Case {is_case.group(0)} in Salesforce", f"https://arrow.my.salesforce.com/{is_case.group(0)}")

            st.write(f"Found {len(results)} matches:")
            for idx, row in results.iterrows():
                with st.container():
                    st.markdown(f"<div class='sop-card'>", unsafe_allow_html=True)
                    if st.button(f"📄 {row['Process']}", key=f"btn_{idx}"):
                        st.session_state.selected_row = row
                        st.session_state.view = 'detail'
                        st.rerun()
                    st.markdown(f"<span class='system-badge'>{row['System']}</span>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("No matches found. Try a broader keyword like 'Unity' or 'Finance'.")

# --- PAGE 2: DETAIL VIEW ---
elif st.session_state.view == 'detail':
    row = st.session_state.selected_row
    
    if st.button("← Back to Search"):
        st.session_state.view = 'home'
        st.rerun()
    
    st.divider()
    col1, col2 = st.columns([0.6, 0.4])
    
    with col1:
        st.markdown(f"<span class='system-badge'>{row['System']}</span>", unsafe_allow_html=True)
        st.title(row['Process'])
        st.subheader("Action Steps")
        # Convert <br> tags to actual new lines
        steps = row['Instructions'].split('<br>')
        for step in steps:
            st.markdown(f"<div class='instruction-step'>{step}</div>", unsafe_allow_html=True)
            
    with col2:
        if row['Screenshot_URL']:
            st.markdown("### System Reference")
            st.image(row['Screenshot_URL'], use_container_width=True)
