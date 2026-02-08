import streamlit as st
import pandas as pd

# 1. PAGE CONFIG
st.set_page_config(page_title="Arrow Ops Search", layout="wide")

# 2. PROFESSIONAL THEME
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #202124; font-family: 'Arial', sans-serif; }
    
    /* Center the search on home */
    .search-container { text-align: center; padding-top: 100px; }
    
    /* Search Result Links */
    .result-item { margin-bottom: 25px; max-width: 600px; }
    .result-link { color: #1a0dab; font-size: 20px; text-decoration: none; cursor: pointer; }
    .result-link:hover { text-decoration: underline; }
    .result-snippet { color: #4d5156; font-size: 14px; line-height: 1.6; }
    
    /* Deep Dive Page Styling */
    .process-header { border-bottom: 1px solid #DADCE0; padding-bottom: 20px; margin-bottom: 20px; }
    .back-btn { color: #5F6368; text-decoration: none; font-size: 14px; margin-bottom: 20px; display: inline-block; }
</style>
""", unsafe_allow_html=True)

# 3. DATA ENGINE
@st.cache_data
def get_data():
    try:
        return pd.read_csv("sop_data.csv").fillna("")
    except:
        return pd.DataFrame()

df = get_data()

# Initialize Session State for Navigation
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'home'
if 'selected_proc' not in st.session_state:
    st.session_state.selected_proc = None

# --- FUNCTION: RETURN TO SEARCH ---
def go_home():
    st.session_state.view_mode = 'home'
    st.rerun()

# --- PAGE 1: SEARCH INTERFACE (HOME) ---
if st.session_state.view_mode == 'home':
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)
    st.title("🏹 Ops Search")
    query = st.text_input("", placeholder="Search Order Management, RMAs, or Compliance...", key="search_bar")
    st.markdown("</div>", unsafe_allow_html=True)

    if query:
        results = df[df.apply(lambda r: r.astype(str).str.contains(query, case=False).any(), axis=1)]
        
        if not results.empty:
            st.write(f"About {len(results)} results found")
            for idx, row in results.iterrows():
                # Result Title as a Button
                if st.button(f"{row['Process']} | {row['System']}", key=f"res_{idx}"):
                    st.session_state.selected_proc = row
                    st.session_state.view_mode = 'detail'
                    st.rerun()
                st.markdown(f"<p class='result-snippet'>{row['Instructions'][:120]}...</p>", unsafe_allow_html=True)
        else:
            st.warning("No results found.")

# --- PAGE 2: PROCESS DEEP DIVE (THE "OTHER PAGE") ---
elif st.session_state.view_mode == 'detail':
    proc = st.session_state.selected_proc
    
    if st.button("← Back to Results"):
        go_home()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([0.6, 0.4])
    
    with col1:
        st.markdown(f"### {proc['System']} // Process Documentation")
        st.title(proc['Process'])
        st.markdown(f"**Action Steps:**")
        # Split instructions by <br> to show as proper bullets
        steps = proc['Instructions'].split('<br>')
        for step in steps:
            st.markdown(f"{step}")
            
    with col2:
        if proc['Screenshot_URL']:
            st.markdown("**System Visual Reference**")
            st.image(proc['Screenshot_URL'], use_container_width=True)
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("Confidential: For Internal Arrow Use Only")
