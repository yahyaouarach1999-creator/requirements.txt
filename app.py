import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Arrow Sales Ops Hub", layout="wide", page_icon="🏹")

# 2. Sidebar with Arrow Branding
logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Arrow_Electronics_logo.svg/1200px-Arrow_Electronics_logo.svg.png"
st.sidebar.image(logo_url, width=200)
st.sidebar.title("🚀 Quick Links")
st.sidebar.markdown("---")
st.sidebar.link_button("🔗 Salesforce", "https://arrow.my.salesforce.com")
st.sidebar.link_button("🔗 Unity", "https://unity.arrow.com")
st.sidebar.link_button("🔗 MyConnect", "https://myconnect.arrow.com")

# 3. Header Section
st.title("🛡️ Sales Ops Knowledge Hub")
st.subheader("Digital Business & Customer Support SOPs")
st.markdown("---")

# 4. Data Loading Logic
try:
    df = pd.read_csv("sop_data.csv")
    df = df.replace(np.nan, '', regex=True)
    
    # 5. Search State Management
    if 'search' not in st.session_state:
        st.session_state.search = ""

    def set_search(term):
        st.session_state.search = term

    # 6. Popular Topics Buttons
    st.write("### 💡 Quick Search Topics")
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        if st.button("📑 Order Status (Unity)"):
            set_search("Unity")
    
    with c2:
        if st.button("🌍 Venlo / Logistics"):
            set_search("Venlo")
            
    with c3:
        if st.button("💰 Refunds"):
            set_search("Refund")
            
    with c4:
        if st.button("🔄 Clear Search"):
            set_search("")

    # 7. Search Input Box
    query = st.text_input("🔍 Search for a process or system...", value=st.session_state.search)

    # 8. Results Display Section
    st.markdown("---")
    
    if query:
        # Search all columns for the keyword
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
        
        if not results.empty:
            for _, row in results.iterrows():
                with st.expander(f"📂 {row['System']} - {row['Process']}"):
                    st.write("### 📝 Instructions")
                    st.info(row['Instructions'])
                    
                    img_path = str(row['Screenshot_URL'])
                    if img_path.startswith("http"):
                        st.image(img_path, use_container_width=True)
        else:
            st.warning(f"No results found for '{query}'.")
            
    else:
        st.write("### 🏠 Welcome")
        st.info("Select a 'Quick Search Topic' above or type a keyword to see the SOP.")

except Exception as e:
    st.error(f"⚠️ System Error: {e}")
