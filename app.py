import streamlit as st
import pandas as pd

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="Arledge Learning", layout="wide", page_icon="🏹")

# --- 2. PROFESSIONAL NAV & SEARCH STYLING ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        .stApp { background-color: #FFFFFF; font-family: 'Inter', sans-serif; }
        
        /* Fixed Header */
        .header-box {
            display: flex;
            align-items: center;
            padding: 20px 5%;
            background: white;
            border-bottom: 1px solid #E2E8F0;
        }
        .logo-text { font-size: 26px; font-weight: 800; color: #1E293B; }
        .logo-orange { color: #F97316; }

        /* Hero Section */
        .hero-banner {
            background: #1E293B;
            color: white;
            padding: 60px 5%;
            border-radius: 15px;
            margin: 20px 0;
        }

        /* Search Bar Visibility Fix */
        .stTextInput > div > div > input {
            background-color: #F8FAFC !important;
            color: #1E293B !important;
            border: 2px solid #CBD5E1 !important;
            height: 50px !important;
            font-size: 18px !important;
        }

        /* Make Cards Look Like Buttons */
        div[data-testid="stMetricValue"] { font-size: 24px !important; color: #F97316 !important; }
        
        .module-card {
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            background: white;
            transition: 0.3s;
            cursor: pointer;
        }
        .module-card:hover { border-color: #F97316; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA LOADING ---
@st.cache_data
def load_data():
    # This matches the comprehensive syllabus + Venlo data we created
    try:
        df = pd.read_csv("sop_data.csv").fillna("")
        return df
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Screenshot_URL", "Email_Template"])

df = load_data()

# --- 4. TOP NAVIGATION ---
st.markdown('<div class="header-box"><div class="logo-text">ARLEDGE <span class="logo-orange">LEARNING</span></div></div>', unsafe_allow_html=True)

# --- 5. SEARCH & INTERACTION ---
st.markdown('<div class="hero-banner"><h1>What do you want to learn today?</h1><p>Search modules, SOPs, and Venlo alerts below.</p></div>', unsafe_allow_html=True)

# This is the functional search bar
query = st.text_input("Search bar", placeholder="Type here to search (e.g., Salesforce, Venlo, Oracle)...", label_visibility="collapsed").strip()

if query:
    # Logic to filter data
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        st.write(f"### Found {len(results)} Modules")
        for idx, row in results.iterrows():
            with st.expander(f"📖 {row['System']} | {row['Process']}", expanded=True):
                col1, col2 = st.columns([0.6, 0.4])
                with col1:
                    st.markdown(f"### Steps")
                    # Replace <br> with newlines for Streamlit display
                    st.write(row['Instructions'].replace("<br>", "\n"))
                    if row['Email_Template']:
                        st.info("📧 Email Template")
                        st.code(row['Email_Template'], language="text")
                with col2:
                    if row['Screenshot_URL']:
                        st.image(row['Screenshot_URL'], caption="Process Visual")
    else:
        st.error("No results found. Try a different keyword.")

else:
    # DEFAULT VIEW: Clickable Mastery Cards
    st.markdown("### 📚 Recommended Paths")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<div class="module-card"><h4>Foundation Mastery</h4><p>View all Foundation SOPs</p></div>', unsafe_allow_html=True)
        if st.button("Open Foundation", use_container_width=True):
            st.info("Searching 'Foundation' for you...")
            # This triggers a search programmatically
            st.session_state.query = "Foundation"

    with c2:
        st.markdown('<div class="module-card"><h4>Arrow.com Mastery</h4><p>View all Arrow.com SOPs</p></div>', unsafe_allow_html=True)
        if st.button("Open Arrow.com", use_container_width=True):
            st.session_state.query = "Arrow.com"

    with c3:
        st.markdown('<div class="module-card"><h4>Verical.com Mastery</h4><p>View all Verical.com SOPs</p></div>', unsafe_allow_html=True)
        if st.button("Open Verical.com", use_container_width=True):
            st.session_state.query = "Verical.com"
