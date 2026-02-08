import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE CONFIG
st.set_page_config(page_title="Arrow Ops Terminal", layout="wide", page_icon="🏹")

# 2. PROFESSIONAL SLATE THEME (High Readability)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    .stApp {
        background-color: #F1F5F9; /* Light Slate Gray Background */
        color: #1E293B;
        font-family: 'Inter', sans-serif;
    }

    /* Side Bar */
    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
    }

    /* Compact Data Cards */
    .sop-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 4px;
        padding: 15px 25px;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Professional Headers */
    .system-tag {
        color: #64748B;
        font-weight: 700;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .process-title {
        color: #0F172A;
        font-size: 1.2rem;
        font-weight: 700;
        margin-top: 2px;
    }

    /* Instruction Text */
    .instruction-text {
        color: #334155;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-top: 10px;
    }

    /* Compact Link Buttons */
    .app-link {
        display: inline-block;
        padding: 6px 12px;
        margin-right: 5px;
        background: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 3px;
        color: #475569;
        text-decoration: none;
        font-size: 11px;
        font-weight: 600;
    }
    .app-link:hover {
        background: #E2E8F0;
        color: #0284C7;
    }

    /* Search Bar Adjustment */
    .stTextInput input {
        border-radius: 4px !important;
        border: 1px solid #CBD5E1 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. GLOBAL NAVIGATION HEADER
st.markdown("""
<div style="background: white; padding: 10px 20px; border-bottom: 2px solid #E2E8F0; margin-bottom: 20px;">
    <a class="app-link" href="https://arrow.my.salesforce.com" target="_blank">SFDC</a>
    <a class="app-link" href="#">UNITY</a>
    <a class="app-link" href="#">ORACLE</a>
    <a class="app-link" href="#">VENLO</a>
    <a class="app-link" href="#">GTS</a>
</div>
""", unsafe_allow_html=True)

# 4. DATA LOADER
@st.cache_data
def load_data():
    try:
        return pd.read_csv("sop_data.csv").fillna("")
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Screenshot_URL"])

df = load_data()

# 5. SEARCH TERMINAL
st.title("🏹 Arrow Operational Repository")
query = st.text_input("Search processes, system codes, or compliance triggers...", placeholder="Try 'Credit Hold' or 'RMA'...")

# 6. COMPACT RENDERING
if not df.empty:
    results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)] if query else df

    for _, row in results.iterrows():
        col1, col2 = st.columns([0.8, 0.2]) # Data is 80%, Image is 20%
        
        with col1:
            st.markdown(f"""
            <div class="sop-card">
                <div class="system-tag">{row['System']}</div>
                <div class="process-title">{row['Process']}</div>
                <div class="instruction-text">{row['Instructions']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            if row['Screenshot_URL']:
                st.image(row['Screenshot_URL'], caption="Ref Image", width=150) # Small thumbnail
else:
    st.warning("No data found in sop_data.csv")
