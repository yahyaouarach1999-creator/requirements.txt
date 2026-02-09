import streamlit as st
import pandas as pd
import re
import urllib.parse

# --- 1. SETTINGS ---
st.set_page_config(page_title="Arledge | Learning Portal", layout="wide", page_icon="🏹")

# --- 2. CSS FOR COURSERA / LINKEDIN LEARNING VIBE ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        
        /* Main Theme */
        .stApp { background-color: #FFFFFF; font-family: 'Inter', sans-serif; }
        
        /* Professional Navbar */
        .navbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 5%;
            background: white;
            border-bottom: 1px solid #E2E8F0;
            margin-bottom: 2rem;
        }
        
        .logo-text {
            font-size: 24px;
            font-weight: 800;
            color: #1E293B;
            letter-spacing: -1px;
        }

        /* Hero Section */
        .hero {
            background: linear-gradient(90deg, #1E293B 0%, #334155 100%);
            padding: 60px 5%;
            border-radius: 15px;
            color: white;
            margin-bottom: 40px;
        }

        /* VISIBILITY FIX: Input Box Styling */
        div[data-baseweb="input"] {
            border-radius: 8px !important;
            border: 1px solid #CBD5E1 !important;
        }
        
        input {
            color: #1E293B !important; /* Deep Navy Text */
            font-size: 18px !important;
            font-weight: 500 !important;
        }

        /* Course Card Styling */
        .course-card {
            background: white;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        .course-card:hover {
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            border-color: #F97316;
        }

        .category-tag {
            background: #FFF7ED;
            color: #C2410C;
            padding: 4px 12px;
            border-radius: 99px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER & LOGO ---
# Replaced raw SVG with a clean PNG-style look
st.markdown("""
    <div class="navbar">
        <div style="display: flex; align-items: center;">
            <img src="https://cdn-icons-png.flaticon.com/512/3665/3665912.png" width="40" style="margin-right:15px;">
            <div class="logo-text">ARLEDGE <span style="color:#F97316;">LEARNING</span></div>
        </div>
        <div style="color: #64748B; font-weight: 500;">Internal Knowledge Base</div>
    </div>
""", unsafe_allow_html=True)

# --- 4. SECURITY GATE ---
if 'authorized' not in st.session_state: st.session_state.authorized = False

if not st.session_state.authorized:
    st.markdown('<div class="hero"><h1>Welcome back.</h1><p>Enter your key to access Arledge Learning paths.</p></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1,1,1])
    with col:
        pwd = st.text_input("Access Key", type="password")
        if st.button("Unlock Terminal") or (pwd == "Arrow2026"):
            if pwd == "Arrow2026":
                st.session_state.authorized = True
                st.rerun()
    st.stop()

# --- 5. HERO SEARCH ---
st.markdown("""
    <div class="hero">
        <h1 style="margin:0; font-size: 36px;">What do you want to learn today?</h1>
        <p style="opacity: 0.8;">Search through SOPs, process guides, and templates.</p>
    </div>
""", unsafe_allow_html=True)

# --- 6. DATA ENGINE ---
@st.cache_data(ttl=1)
def load_data():
    try:
        df = pd.read_csv("sop_data.csv").fillna("")
        return df
    except:
        return pd.DataFrame(columns=["System", "Process", "Instructions", "Screenshot_URL", "Email_Template"])

df = load_data()

# --- 7. SEARCH & GRID ---
query = st.text_input("🔍", placeholder="Search by system or process name (e.g. Salesforce, Onboarding)...").strip()

if query:
    mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        st.write(f"Showing {len(results)} learning paths")
        for idx, row in results.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="course-card">
                    <span class="category-tag">{row['System']}</span>
                    <h3 style="margin: 10px 0; color: #1E293B;">{row['Process']}</h3>
                </div>
                """, unsafe_allow_html=True)
                if st.button("View Learning Path", key=f"view_{idx}"):
                    st.session_state.selected = row
                    st.session_state.view = 'detail'
                    st.rerun()
    else:
        st.warning("No courses found matching that search.")
else:
    # Default Grid View
    st.markdown("### 📚 Recommended Paths")
    cols = st.columns(3)
    systems = df['System'].unique()[:3] if not df.empty else ["No Data"]
    for i, sys in enumerate(systems):
        with cols[i]:
            st.markdown(f"""
            <div class="course-card" style="text-align:center;">
                <div style="font-size:40px; margin-bottom:10px;">📖</div>
                <h4 style="color:#1E293B;">{sys} Mastery</h4>
                <p style="color:#64748B; font-size:14px;">View all {sys} SOPs</p>
            </div>
            """, unsafe_allow_html=True)

# --- 8. DETAIL VIEW ---
if 'view' in st.session_state and st.session_state.view == 'detail':
    row = st.session_state.selected
    st.divider()
    if st.button("← Back to Catalog"):
        del st.session_state.view
        st.rerun()
        
    col_l, col_r = st.columns([0.6, 0.4])
    with col_l:
        st.title(row['Process'])
        st.info(f"Source System: {row['System']}")
        st.markdown("### Step-by-Step Guide")
        st.write(row['Instructions'])
    with col_r:
        if row['Screenshot_URL']:
            st.image(row['Screenshot_URL'], use_container_width=True)
