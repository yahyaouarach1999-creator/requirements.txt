import streamlit as st
import pandas as pd
import numpy as np

# 1. CORE CONFIGURATION
st.set_page_config(page_title="Arrow Ops Academy", layout="wide", page_icon="🎓")

# 2. THE MASTERCLASS CSS (Coursera Aesthetic)
# We use a single variable to keep the string safe and easy to close
academy_style = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp { background-color: #FFFFFF; font-family: 'Inter', sans-serif; }
    
    /* Sidebar: Deep Oxford Blue */
    section[data-testid="stSidebar"] { background-color: #002147 !important; }
    section[data-testid="stSidebar"] * { color: white !important; }

    /* Learning Cards */
    .learning-card {
        background: #FFFFFF;
        padding: 35px;
        border-radius: 24px;
        border: 1px solid #F3F4F6;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        transition: 0.3s;
    }
    
    /* Instruction Highlight Box */
    .instruction-step {
        background-color: #F9FAFB;
        border-left: 5px solid #0056D2;
        padding: 25px;
        border-radius: 8px;
        font-size: 17px;
        line-height: 1.7;
        color: #374151;
    }

    /* Coursera-Blue Buttons */
    .stButton>button {
        background: #0056D2;
        color: white;
        border-radius: 12px;
        font-weight: 700;
        height: 55px;
        border: none;
        width: 100%;
    }
</style>
"""
st.markdown(academy_style, unsafe_allow_html=True)

# 3. SIDEBAR: PROGRESS TRACKER
with st.sidebar:
    st.markdown("# 🎓 Ops Academy")
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.info("Branding Image Pending")
    
    st.markdown("---")
    st.write("📈 **YOUR MASTERY PROGRESS**")
    st.progress(75)
    st.caption("Advanced Workflow Certification: 75%")
    st.markdown("---")
    st.link_button("🌐 UNITY CLOUD", "https://unity.arrow.com")
    st.link_button("📊 SALESFORCE CRM", "https://arrow.my.salesforce.com")

# 4. HERO SECTION
st.markdown("<h4 style='color:#0056D2; margin-bottom:0;'>MASTERCLASS SERIES</h4>", unsafe_allow_html=True)
st.title("Strategic Supply Chain Operations")
st.markdown("Choose a scenario to unlock professional resolution protocols.")

# 5. DATA LOADING ENGINE
@st.cache_data
def load_vault():
    try:
        data = pd.read_csv("sop_data.csv")
        return data.replace(np.nan, '', regex=True)
    except:
        return None

df = load_vault()

# 6. SCENARIO BUTTONS (SITUATIONS)
st.write("### 🎯 Active Scenarios")
col1, col2, col3, col4 = st.columns(4)

if col1.button("🚨 Emergency Holds"): st.session_state.search = "Emergency"
if col2.button("🚚 Logistics Mastery"): st.session_state.search = "Venlo"
if col3.button("💰 Finance Audit"): st.session_state.search = "Finance"
if col4.button("🔄 Reset Course"): st.session_state.search = ""

# 7. SEARCH BAR
query = st.text_input("Search Academy database...", value=st.session_state.search if 'search' in st.session_state else "")

# 8. MASTERCLASS CONTENT VIEW
if query and df is not None:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="learning-card">
                <p style="color:#0056D2; font-weight:700; font-size:12px; letter-spacing:1px;">MODULE: {row['System'].upper()}</p>
                <h2 style="color:#111827; margin-top:0; font-size:28px;">{row['Process']}</h2>
                <div class="instruction-step">
                    {row['Instructions']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if str(row['Screenshot_URL']).startswith("http"):
                st.image(row['Screenshot_URL'], use_container_width=True)
    else:
        st.warning("No scenarios found for this query.")
else:
    st.markdown("<br><p style='text-align:center; color:#9CA3AF;'>Select a module above to reveal the learning materials.</p>", unsafe_allow_html=True)
