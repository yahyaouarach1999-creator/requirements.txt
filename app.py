import streamlit as st
import pandas as pd
import numpy as np

# 1. CORE CONFIGURATION
st.set_page_config(page_title="Arrow Ops Masterclass", layout="wide", page_icon="🏹")

# 2. ELITE DARK THEME (Fixed Syntax & High-Contrast Blue)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&family=Inter:wght@400;700&display=swap');

    .stApp {
        background-color: #0B0E14; 
        color: #D1D5DB;
        font-family: 'Inter', sans-serif;
    }

    /* Card Styling */
    .sop-card {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 30px;
        margin-bottom: 20px;
    }
    
    /* Search Bar Professionalism */
    .stTextInput input {
        background-color: #0B0E14 !important;
        border: 1px solid #58A6FF !important;
        color: #58A6FF !important;
        font-family: 'Roboto Mono', monospace;
    }

    /* Terminal-style Link Buttons */
    .app-link {
        display: inline-block;
        padding: 10px 20px;
        margin-right: 10px;
        border: 1px solid #30363D;
        border-radius: 5px;
        color: #8B949E;
        text-decoration: none;
        font-size: 12px;
        font-weight: bold;
        transition: 0.3s;
    }
    .app-link:hover {
        border-color: #58A6FF;
        color: #58A6FF;
        background: rgba(88, 166, 255, 0.1);
    }

    .strat-header {
        color: #58A6FF;
        text-transform: uppercase;
        font-size: 0.8em;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# 3. DIRECT ACCESS LINKS
st.markdown("""
<div style="padding: 10px 0px 30px 0px;">
    <a class="app-link" href="https://arrow.my.salesforce.com" target="_blank">🔗 SALESFORCE CRM</a>
    <a class="app-link" href="#" target="_blank">🔗 UNITY ERP</a>
    <a class="app-link" href="#" target="_blank">🔗 ORACLE FINANCIALS</a>
    <a class="app-link" href="#" target="_blank">🔗 VENLO LOGISTICS</a>
    <a class="app-link" href="#" target="_blank">🔗 GTS COMPLIANCE</a>
</div>
""", unsafe_allow_html=True)

# 4. DATA ENGINE
@st.cache_data
def load_arrow_data():
    try:
        df = pd.read_csv("sop_data.csv")
        return df.fillna("")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

df = load_arrow_data()

# 5. SEARCH INTERFACE
st.markdown("<h1 style='letter-spacing:-1px; color:white;'>Order Management & CS Academy</h1>", unsafe_allow_html=True)
search_query = st.text_input("SEARCH GLOBAL PROTOCOLS", placeholder="Enter keyword (e.g., 'Credit Hold', 'RMA', 'ECCN')")

# 6. RESULTS LOGIC
if not df.empty:
    if search_query:
        results = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    else:
        results = df

    if not results.empty:
        for _, row in results.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="sop-card">
                    <div class="strat-header">{row['System']} // ARROW GLOBAL OPS</div>
                    <h2 style="color:white; margin-top:5px; margin-bottom:15px;">{row['Process']}</h2>
                    <div style="background:#0D1117; padding:20px; border-radius:5px; border-left:3px solid #58A6FF; margin-bottom:20px;">
                        <p style="color:#CBD5E1; font-size:1.05em; line-height:1.7;">{row['Instructions']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if row['Screenshot_URL']:
                    st.image(row['Screenshot_URL'], use_container_width=True)
    else:
        st.info("NO MATCHING PROTOCOLS FOUND.")
else:
    st.warning("DATA REPOSITORY EMPTY. CHECK CSV UPLOAD.")
