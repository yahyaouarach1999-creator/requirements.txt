import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Arrow Sales Ops Hub", layout="wide", page_icon="🏹")

# 2. Advanced Styling (The "Creative" Layer)
st.markdown("""
    <style>
    /* Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Mature Card Styling */
    div.stButton > button {
        border-radius: 10px;
        border: 1px solid #000000;
        background-color: #ffffff;
        color: #000000;
        font-weight: bold;
        transition: all 0.3s;
        height: 3em;
        width: 100%;
    }
    
    div.stButton > button:hover {
        background-color: #000000;
        color: #ffffff;
        transform: translateY(-2px);
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Arrow_Electronics_logo.svg/1200px-Arrow_Electronics_logo.svg.png"
st.sidebar.image(logo_url, width=180)
st.sidebar.title("🚀 Navigation")
st.sidebar.markdown("---")
st.sidebar.link_button("📊 Salesforce CRM", "https://arrow.my.salesforce.com")
st.sidebar.link_button("⚙️ Unity Portal", "https://unity.arrow.com")
st.sidebar.link_button("📂 MyConnect", "https://myconnect.arrow.com")

# 4. Main Header & Motivation
st.title("🏹 Sales Ops Excellence Hub")
st.caption("Precision. Speed. Digital Mastery.")

# Motivational Quote of the Day
quotes = [
    "“Excellence is not a skill, it’s an attitude.”",
    "“Success is the sum of small efforts, repeated day in and day out.”",
    "“The best way to predict the future is to create it.”"
]
st.info(np.random.choice(quotes))

# 5. Data Loading
try:
    df = pd.read_csv("sop_data.csv")
    df = df.replace(np.nan, '', regex=True)
    
    if 'search' not in st.session_state:
        st.session_state.search = ""

    def set_search(term):
        st.session_state.search = term

    # 6. Styled Topic Selection
    st.write("### 📂 Categories")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("📦 Order Flow"): set_search("Unity")
    with c2:
        if st.button("🚚 Logistics"): set_search("Venlo")
    with c3:
        if st.button("💳 Finance"): set_search("Refund")
    with c4:
        if st.button("🔄 Clear"): set_search("")

    # 7. Search Bar
    query = st.text_input("", value=st.session_state.search, placeholder="Search for a process (e.g., 'Address', 'Case', 'Tracking')...")

    # 8. Results
    if query:
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
        
        if not results.empty:
            for _, row in results.iterrows():
                with st.expander(f"📝 {row['System']} | {row['Process']}"):
                    st.markdown(f"**Action Steps:**")
                    st.write(row['Instructions'])
                    
                    if str(row['Screenshot_URL']).startswith("http"):
                        st.image(row['Screenshot_URL'], use_container_width=True)
        else:
            st.warning("No procedure matches that search.")
    else:
        st.write("---")
        st.subheader("Welcome to the Operations Engine")
        st.write("Select a category above to begin your workflow.")

except Exception as e:
    st.error(f"⚠️ Load Error: {e}")
