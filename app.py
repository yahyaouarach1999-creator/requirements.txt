import streamlit as st
import pandas as pd
import numpy as np

# 1. CORE CONFIGURATION
st.set_page_config(page_title="Ops Academy | Enterprise", layout="wide", page_icon="⚖️")

# 2. EXECUTIVE STYLE SHEET (Muted, Professional, High-Contrast)
executive_theme = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* Background and Global */
    .stApp {
        background-color: #0F172A; /* Deep Navy Slate */
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }

    /* Professional Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155;
    }

    /* Typography */
    h1, h2, h3 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    /* The "Fancy" Learning Card */
    .sop-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 40px;
        margin-bottom: 25px;
        transition: all 0.3s ease;
    }
    .sop-card:hover {
        border-color: #38BDF8; /* Subtle Blue Glow */
        transform: translateY(-5px);
    }

    /* System Badge */
    .badge {
        background: #334155;
        color: #38BDF8;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Context Box (The "Why") */
    .context-box {
        background: #0F172A;
        border-left: 4px solid #38BDF8;
        padding: 20px;
        margin: 20px 0;
        border-radius: 4px;
        color: #94A3B8;
        font-style: italic;
    }

    /* Search Bar Input */
    .stTextInput input {
        background-color: #1E293B !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }

    /* Buttons */
    .stButton>button {
        background: #0284C7 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #0EA5E9 !important;
        box-shadow: 0 0 15px rgba(14, 165, 233, 0.4);
    }
</style>
"""
st.markdown(executive_theme, unsafe_allow_html=True)

# 3. DATA ARCHITECTURE
@st.cache_data
def get_data():
    try:
        # Loading the CSV you updated
        df = pd.read_csv("sop_data.csv")
        return df.replace(np.nan, '', regex=True)
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Screenshot_URL"])

df = get_data()

# 4. SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("<h2 style='color:#38BDF8;'>⚖️ OPS ACADEMY</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B;'>Enterprise Governance Engine</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.write("🔒 **CERTIFICATION STATUS**")
    st.progress(88)
    st.caption("Advanced Workflow Mastery: 88%")
    
    st.markdown("---")
    st.markdown("### 🛠️ Quick Access")
    if st.button("🚨 Crisis Management"): st.session_state.search = "Strategic"
    if st.button("💰 Financial Integrity"): st.session_state.search = "Finance"
    if st.button("🌐 Trade Compliance"): st.session_state.search = "Compliance"
    if st.button("🔄 Reset View"): st.session_state.search = ""

# 5. HEADER SECTION
st.markdown("<p style='color:#38BDF8; font-weight:600; margin-bottom:0;'>MASTERCLASS SERIES</p>", unsafe_allow_html=True)
st.title("Operations & Strategy Repository")
st.markdown("<p style='color:#94A3B8; font-size:1.1em;'>High-fidelity procedural protocols for global supply chain and enterprise management.</p>", unsafe_allow_html=True)

# 6. SEARCH & FILTERING
if 'search' not in st.session_state:
    st.session_state.search = ""

query = st.text_input("🔍 Search protocol library (e.g. 'RMA', 'Backorder', 'Sanctions')", value=st.session_state.search)

# 7. DYNAMIC CONTENT DISPLAY
if query:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            # Splitting instructions to isolate the "Strategic Context" for special formatting
            raw_instr = row['Instructions']
            if "**STRATEGIC CONTEXT:**" in raw_instr:
                parts = raw_instr.split("<br><br>", 1)
                context = parts[0]
                steps = parts[1] if len(parts) > 1 else ""
            else:
                context = ""
                steps = raw_instr

            st.markdown(f"""
            <div class="sop-card">
                <span class="badge">{row['System']}</span>
                <h2 style="margin-top:10px;">{row['Process']}</h2>
                <div class="context-box">
                    {context}
                </div>
                <div style="line-height:1.8; color:#CBD5E1; font-size:1.05em;">
                    {steps}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if "http" in str(row['Screenshot_URL']):
                st.image(row['Screenshot_URL'], use_container_width=True, caption=f"Protocol Visualization: {row['Process']}")
    else:
        st.info(f"No protocols found matching '{query}'.")
else:
    # Landing State: Show Modules
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 📖 How to use this Academy
        1. **Select a Module:** Use the sidebar or search bar to find a specific workflow.
        2. **Understand the 'Why':** Every protocol starts with a Strategic Context box.
        3. **Execute:** Follow the numbered protocols for 100% compliance.
        """)
    with col2:
        st.markdown("""
        ### 📊 System Health
        * **Unity Cloud:** <span style='color:#10B981;'>ONLINE</span>
        * **SFDC API:** <span style='color:#10B981;'>ONLINE</span>
        * **Oracle ERP:** <span style='color:#F59E0B;'>DEGRADED</span>
        """, unsafe_allow_html=True)
