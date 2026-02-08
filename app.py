import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Ops Academy | Elite", layout="wide", page_icon="🏢")

# 2. THE "CONSULTANT" THEME (Slate, Navy, and Cyan)
executive_style = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    .stApp {
        background-color: #0F172A; /* Deep Charcoal Navy */
        color: #E2E8F0;
        font-family: 'Inter', sans-serif;
    }

    /* Professional Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155;
    }

    /* Glassmorphism Cards */
    .sop-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 35px;
        margin-bottom: 20px;
        transition: 0.4s;
    }
    .sop-card:hover {
        border-color: #38BDF8;
        background: rgba(30, 41, 59, 0.8);
    }

    /* Strategic Context Box */
    .context-highlight {
        background: #0F172A;
        border-left: 5px solid #38BDF8;
        padding: 20px;
        margin-bottom: 25px;
        color: #94A3B8;
        font-size: 0.95em;
        line-height: 1.6;
    }

    /* Badges */
    .system-badge {
        background: #38BDF8;
        color: #0F172A;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Inputs & Buttons */
    .stTextInput input {
        background-color: #1E293B !important;
        color: white !important;
        border: 1px solid #334155 !important;
    }
</style>
"""
st.markdown(executive_style, unsafe_allow_html=True)

# 3. DATA ENGINE
@st.cache_data
def load_vault():
    try:
        df = pd.read_csv("sop_data.csv")
        return df.fillna("")
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Screenshot_URL"])

df = load_vault()

# 4. SIDEBAR & CATEGORY LOGIC
with st.sidebar:
    st.markdown("<h1 style='color:#38BDF8; font-size:22px;'>🏢 EXECUTIVE VAULT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B;'>Standard Operating Procedures v3.1</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 🏷️ Filter by Category")
    category = st.radio("Select Domain:", 
                        ["All Protocols", "Crisis Management", "Financial Integrity", "System Ops", "Trade Compliance"])
    
    st.markdown("---")
    st.info("**ADMIN NOTE:** Oracle ERP is currently undergoing maintenance. Use manual ETL logging for all transactions.")

# 5. MAIN INTERFACE
st.title("Strategic Procedure Repository")
search_query = st.text_input("🔍 Search globally across all system protocols...", placeholder="e.g., Ransomware, RMA, Sanctions")

# 6. FILTERING LOGIC
filtered_df = df.copy()

# Map the categories to keywords in your Process or System column
if category == "Crisis Management":
    filtered_df = df[df['System'].str.contains('Crisis|IT Infrastructure|Security|Operations', case=False)]
elif category == "Financial Integrity":
    filtered_df = df[df['System'].str.contains('Finance|Legal', case=False)]
elif category == "System Ops":
    filtered_df = df[df['System'].str.contains('Unity|Salesforce|Oracle|Warehouse', case=False)]
elif category == "Trade Compliance":
    filtered_df = df[df['System'].str.contains('Compliance|Logistics', case=False)]

if search_query:
    filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

# 7. RENDER CARDS
if not filtered_df.empty:
    for idx, row in filtered_df.iterrows():
        with st.container():
            # Clean up the Instruction text
            content = row['Instructions']
            if "**STRATEGIC CONTEXT:**" in content:
                parts = content.split("<br><br>", 1)
                context = parts[0]
                steps = parts[1] if len(parts) > 1 else ""
            else:
                context = ""
                steps = content

            st.markdown(f"""
            <div class="sop-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="system-badge">{row['System']}</span>
                    <small style="color:#475569;">REF-ID: {idx + 1000}</small>
                </div>
                <h2 style="color:#F8FAFC; margin-top:15px;">{row['Process']}</h2>
                <div class="context-highlight">{context}</div>
                <div style="color:#CBD5E1; line-height:1.7;">{steps}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if row['Screenshot_URL']:
                st.image(row['Screenshot_URL'], use_container_width=True)
                st.markdown("<br>", unsafe_allow_html=True)
else:
    st.warning("No protocols found. Adjust your filters or search terms.")
