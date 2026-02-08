import streamlit as st
import pandas as pd
import numpy as np

# 1. ARCHITECTURAL CONFIG
st.set_page_config(page_title="Arrow Ops Academy", layout="wide", page_icon="🎓")

# 2. COURSERA-STYLE PREMIUM STYLING
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap');
    
    .stApp { background-color: #FFFFFF; font-family: 'Source Sans Pro', sans-serif; }
    
    /* Sidebar: Learning Dashboard Style */
    section[data-testid="stSidebar"] { 
        background-color: #1F2937 !important; 
        color: white !important;
    }

    /* Course Card Design */
    .course-card {
        background: #FFFFFF;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        border-top: 5px solid #2563EB; /* Coursera Blue */
    }

    /* Situation Badge */
    .situation-badge {
        background-color: #EFF6FF;
        color: #1E40AF;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
    }

    /* Fancy Buttons */
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 6px;
        font-weight: 600;
        height: 50px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1D4ED8 !important;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR: THE LEARNING PATH
with st.sidebar:
    st.markdown("<h2 style='color:white;'>🏹 Ops Academy</h2>", unsafe_allow_html=True)
    st.image("logo.png", use_container_width=True)
    st.markdown("---")
    st.write("📂 **YOUR LEARNING PATH**")
    st.caption("✔️ Introduction to Unity")
    st.caption("✔️ Advanced Salesforce Case Mgmt")
    st.caption("🟡 Venlo Logistics Expert")
    st.progress(65)
    st.markdown("---")
    st.link_button("🌐 Open System Terminal", "https://unity.arrow.com")

# 4. MAIN HUB HEADER
st.title("Welcome back, Ops Professional 👋")
st.markdown("#### Explore scenarios and master the global supply chain workflows.")

# 5. DATA ENGINE
@st.cache_data
def load_data():
    try:
        return pd.read_csv("sop_data.csv").replace(np.nan, '', regex=True)
    except:
        return None

df = load_data()

# 6. SCENARIO SELECTOR (Fancy Situations)
st.write("### 🎯 Choose a Situation to Resolve")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.image("https://cdn-icons-png.flaticon.com/512/3502/3502601.png", width=60)
    if st.button("Order is Delayed"): st.session_state.search = "Unity"
with c2:
    st.image("https://cdn-icons-png.flaticon.com/512/2312/2312701.png", width=60)
    if st.button("Shipment Tracking"): st.session_state.search = "Venlo"
with c3:
    st.image("https://cdn-icons-png.flaticon.com/512/2489/2489756.png", width=60)
    if st.button("Payment Issues"): st.session_state.search = "Refund"
with c4:
    st.image("https://cdn-icons-png.flaticon.com/512/1160/1160515.png", width=60)
    if st.button("Reset Dashboard"): st.session_state.search = ""

st.markdown("---")

# 7. SEARCH BAR
query = st.text_input("🔍 Search specific tools or keywords...", value=st.session_state.search)

# 8. SITUATION DISPLAY (Coursera Style)
if query and df is not None:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        for _, row in results.iterrows():
            st.markdown(f"""
            <div class="course-card">
                <span class="situation-badge">{row['System'].upper()} MODULE</span>
                <h2 style="color:#111827; margin-top:10px;">Scenario: {row['Process']}</h2>
                <hr>
                <h4 style="color:#374151;">Step-by-Step Execution:</h4>
                <p style="font-size:16px; line-height:1.6; color:#4B5563;">{row['Instructions']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show the visual aid
            if str(row['Screenshot_URL']).startswith("http"):
                st.image(row['Screenshot_URL'], use_container_width=True, caption=f"Training Visual for {row['Process']}")
    else:
        st.error("No training modules found for this query.")
else:
    st.markdown("""
        <div style='background-color:#F9FAFB; padding:50px; border-radius:15px; text-align:center; border:2px dashed #D1D5DB;'>
            <h3 style='color:#6B728
