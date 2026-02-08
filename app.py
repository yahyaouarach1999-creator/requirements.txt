import streamlit as st
import pandas as pd
import re

# --- 1. CORE CONFIG & SYSTEM THEME ---
st.set_page_config(page_title="Arrow Ops Masterclass", layout="wide", page_icon="🏹")

st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; color: #1E293B; font-family: 'Inter', sans-serif; }
    .search-container { text-align: center; padding: 60px 0 20px 0; background: white; border-bottom: 1px solid #E2E8F0; }
    .sop-card { border: 1px solid #E2E8F0; border-radius: 6px; padding: 18px; background: white; margin-bottom: 12px; cursor: pointer; border-left: 4px solid #94A3B8; }
    .sop-card:hover { border-left: 4px solid #3B82F6; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
    .status-online { color: #10B981; font-size: 10px; font-weight: bold; }
    .system-badge { background: #F1F5F9; color: #475569; padding: 2px 8px; border-radius: 12px; font-size: 10px; font-weight: 700; }
    .instruction-step { padding: 8px 0; border-bottom: 1px solid #F1F5F9; font-size: 14px; color: #334155; }
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

# --- 4. SIDEBAR: STATUS & HISTORY ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/Arrow_Electronics_Logo.svg", width=150)
    st.divider()
    
    st.subheader("🌐 System Status")
    st.markdown("🟢 Unity: **Operational**")
    st.markdown("🟢 SFDC: **Operational**")
    st.markdown("🟡 Oracle: **Maintenance @ 20:00**")
    
    st.divider()
    st.subheader("🕒 Recent Activity")
    if not st.session_state.history:
        st.caption("No recent WEBSO/Case searches.")
    for item in reversed(st.session_state.history[-5:]):
        st.button(f"📄 {item}", key=f"hist_{item}", use_container_width=True)

# --- 5. PAGE 1: SEARCH PORTAL ---
if st.session_state.view == 'home':
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)
    st.title("Arrow Operational Repository")
    query = st.text_input("", placeholder="Search keywords (RMA, Credit) or enter ID (WEBSO, 00123...)", label_visibility="collapsed").strip()
    st.markdown("</div>", unsafe_allow_html=True)

    if query:
        # Reference Pattern Recognition
        is_webso = re.search(r"WEBSO\s*(\d+)", query, re.IGNORECASE)
        is_case = re.search(r"\b\d{8}\b", query)

        if (is_webso or is_case) and query not in st.session_state.history:
            st.session_state.history.append(query)

        # Logic: Global Filter
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]

        if not results.empty:
            # Action Row
            col_a, col_b = st.columns(2)
            if is_webso:
                col_a.link_button(f"🔗 Launch Unity: {is_webso.group(1)}", f"https://unity.arrow.com/orders/{is_webso.group(1)}")
            if is_case:
                col_b.link_button(f"🔗 Launch SFDC: {is_case.group(0)}", f"https://arrow.my.salesforce.com/{is_case.group(0)}")

            st.write(f"Matches found ({len(results)}):")
            for idx, row in results.iterrows():
                with st.container():
                    st.markdown(f"<div class='sop-card'>", unsafe_allow_html=True)
                    if st.button(f"{row['Process']}", key=f"btn_{idx}", help="Click to view full SOP"):
                        st.session_state.selected_row = row
                        st.session_state.view = 'detail'
                        st.rerun()
                    st.markdown(f"<span class='system-badge'>{row['System']}</span>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No matches found. Try searching for a system name like 'Venlo' or 'Finance'.")

# --- 6. PAGE 2: DETAIL SOP VIEW ---
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
        st.write("---")
        steps = row['Instructions'].split('<br>')
        for step in steps:
            st.markdown(f"<div class='instruction-step'>{step}</div>", unsafe_allow_html=True)
            
    with col2:
        if row['Screenshot_URL']:
            st.markdown("### Interface Reference")
            st.image(row['Screenshot_URL'], use_container_width=True)
