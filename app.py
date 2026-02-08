import streamlit as st
import pandas as pd

# 1. SETUP
st.set_page_config(page_title="Arrow Ops Terminal", layout="wide")

# 2. PROFESSIONAL LIGHT THEME (Data-Dense)
st.markdown("""
<style>
    .stApp { background-color: #F4F7F9; color: #333; font-family: sans-serif; }
    .sop-card { 
        background: white; 
        border: 1px solid #D1D9E0; 
        padding: 15px; 
        border-radius: 4px; 
        margin-bottom: 8px;
    }
    .system-label { 
        color: #0056b3; 
        font-weight: bold; 
        font-size: 11px; 
        text-transform: uppercase;
    }
    .title-label { font-size: 16px; font-weight: bold; margin-bottom: 4px; color: #111; }
    .step-text { font-size: 13px; line-height: 1.4; color: #444; }
    .link-bar { background: #E9ECEF; padding: 10px; border-radius: 4px; margin-bottom: 15px; }
    a { color: #0056b3; text-decoration: none; font-weight: bold; margin-right: 15px; font-size: 12px; }
    .landing-text { text-align: center; margin-top: 100px; color: #6C757D; }
</style>
""", unsafe_allow_html=True)

# 3. COMPACT HEADER LINKS
st.markdown("""
<div class="link-bar">
    <a href="https://arrow.my.salesforce.com" target="_blank">SALESFORCE</a>
    <a href="#">UNITY</a>
    <a href="#">ORACLE</a>
    <a href="#">VENLO</a>
    <a href="#">GTS</a>
</div>
""", unsafe_allow_html=True)

# 4. DATA LOAD
@st.cache_data
def get_data():
    try:
        return pd.read_csv("sop_data.csv").fillna("")
    except:
        return pd.DataFrame()

df = get_data()

# 5. SEARCH TERMINAL
st.title("🏹 Ops Command Center")
query = st.text_input("", placeholder="Type a process or system code (e.g. 'RMA', 'Hold', 'GTS')...")

# 6. CONDITIONAL RENDERING (Nothing shows until query is typed)
if query:
    filtered = df[df.apply(lambda r: r.astype(str).str.contains(query, case=False).any(), axis=1)]
    
    if not filtered.empty:
        st.markdown(f"**Results for: '{query}'**")
        for _, row in filtered.iterrows():
            col_text, col_img = st.columns([0.9, 0.1])
            with col_text:
                st.markdown(f"""
                <div class="sop-card">
                    <div class="system-label">{row['System']}</div>
                    <div class="title-label">{row['Process']}</div>
                    <div class="step-text">{row['Instructions']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_img:
                if row['Screenshot_URL']:
                    st.image(row['Screenshot_URL'], use_container_width=True)
    else:
        st.warning(f"No protocol found for '{query}'. Please check spelling or system code.")
else:
    # LANDING STATE
    st.markdown("""
    <div class="landing-text">
        <h3>Awaiting Command...</h3>
        <p>Enter a system keyword above to retrieve operational protocols.</p>
    </div>
    """, unsafe_allow_html=True)
