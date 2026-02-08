import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Arrow Sales Ops Portal", layout="wide", page_icon="🏹")

# 2. Sidebar with Logo and Links
logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Arrow_Electronics_logo.svg/1200px-Arrow_Electronics_logo.svg.png"
st.sidebar.image(logo_url, width=200)
st.sidebar.title("🚀 Quick Access")
st.sidebar.markdown("---")
st.sidebar.link_button("🔗 Open Salesforce", "https://arrow.my.salesforce.com")
st.sidebar.link_button("🔗 Open MyConnect", "https://myconnect.arrow.com")
st.sidebar.link_button("🔗 Open Oracle EBS", "https://ebs.arrow.com")

# 3. App Header
st.title("🛡️ Sales Ops Knowledge Hub")
st.subheader("Internal SOPs & Process Navigation")

# 4. Data Loading
try:
    df = pd.read_csv("sop_data.csv", sep=None, engine='python')
    df.columns = df.columns.str.strip()
    df = df.replace(np.nan, '', regex=True)

    # 5. NEW: Improved Clear Search Logic
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""

    # This function resets the search box
    def clear_text():
        st.session_state.search_query = ""
        st.session_state.main_search = "" # This clears the actual widget

    def set_search(term):
        st.session_state.search_query = term
        st.session_state.main_search = term # This fills the actual widget

    # 6. Popular Topics Buttons
    st.write("### 💡 Popular Topics")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("📑 Refund Approvals"):
        set_search("Refund")
    if c2.button("🌍 Venlo Shipping"):
        set_search("Venlo")
    if c3.button("👤 Customer Setup"):
        set_search("Address")
    if c4.button("🔄 Clear Search", on_click=clear_text):
        pass # The on_click function above handles the reset

    st.markdown("---")

    # 7. Search Bar (Connected to Session State)
    search = st.text_input("🔍 Search for a process", key="main_search")

    # Use the session state to filter results
    query = st.session_state.main_search

    if query:
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        filtered = df[mask]
        
        if not filtered.empty:
            for _, row in filtered.iterrows():
                with st.expander(f"📂 {row.get('System', 'System')} - {row.get('Process', 'Process')}"):
                    st.write("### 📝 Instructions")
                    st.info(row.get('Instructions', 'No instructions found'))
                    
                    img_url = row.get('Screenshot_URL', '')
                    if str(img_url).startswith('http'):
                        st.image(img_url, use_container_width=True)
        else:
            st.warning(f"No results found for '{query}'.")
    else:
        st.info("Select a popular topic above or type in the search bar to begin.")

except Exception as e:
    st.error(f"⚠️ Error: {e}")
