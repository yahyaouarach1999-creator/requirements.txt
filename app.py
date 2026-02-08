import streamlit as st
import pandas as pd
import re

# 1. SETUP
st.set_page_config(page_title="Arrow Ops Search", layout="wide")

# 2. THEME - Ensuring a clean White/Google look
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    .search-box { text-align: center; padding-top: 50px; }
    /* Hide the standard Streamlit footer and header for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. DATA
@st.cache_data
def load_data():
    try:
        return pd.read_csv("sop_data.csv").fillna("")
    except:
        return pd.DataFrame()

df = load_data()

# 4. INITIALIZE SESSION STATE
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'selected_row' not in st.session_state:
    st.session_state.selected_row = None
if 'history' not in st.session_state:
    st.session_state.history = []

# 5. SIDEBAR (History)
with st.sidebar:
    st.header("🕒 Recent")
    for item in st.session_state.history[-5:]:
        if st.button(f"{item}", use_container_width=True):
             st.session_state.view = 'home'
             # This forces the app to re-run with this query

# 6. PAGE LOGIC: HOME (Search Only)
if st.session_state.view == 'home':
    st.markdown("<div class='search-box'><h1>🏹 Arrow Search</h1></div>", unsafe_allow_html=True)
    
    query = st.text_input("", placeholder="Enter WEBSO, Case #, or Keyword...", key="main_search")

    if query:
        # Detect WEBSO/Case for History
        if "WEBSO" in query.upper() or len(query) == 8:
            if query not in st.session_state.history:
                st.session_state.history.append(query)

        # Logic: Filter results
        results = df[df.apply(lambda r: r.astype(str).str.contains(query, case=False).any(), axis=1)]
        
        if not results.empty:
            st.write(f"Showing {len(results)} results:")
            for idx, row in results.iterrows():
                # Clicking this takes you to "Another Page"
                if st.button(f"📄 {row['Process']} | {row['System']}", key=f"btn_{idx}"):
                    st.session_state.selected_row = row
                    st.session_state.view = 'detail'
                    st.rerun()
        else:
            st.error("No matches found.")

# 7. PAGE LOGIC: DETAIL (The "Another Page")
elif st.session_state.view == 'detail':
    row = st.session_state.selected_row
    
    if st.button("← Back to Search"):
        st.session_state.view = 'home'
        st.rerun()
    
    st.divider()
    
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.caption(row['System'])
        st.title(row['Process'])
        # Display steps as clean text
        st.markdown(row['Instructions'].replace("<br>", "\n"))
        
        # WEBSO Deep Link logic
        webso_match = re.search(r"WEBSO\s*(\d+)", str(st.session_state.history[-1] if st.session_state.history else ""), re.IGNORECASE)
        if webso_match:
            st.link_button(f"Open Order {webso_match.group(1)} in Unity", f"https://unity.arrow.com/order/{webso_match.group(1)}")

    with col2:
        if row['Screenshot_URL']:
            st.image(row['Screenshot_URL'], caption="System Reference")
