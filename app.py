import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Arrow Sales Ops Portal", layout="wide", page_icon="🏹")

# 2. Sidebar with Logo and Links
# Direct link to a stable Arrow logo
logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Arrow_Electronics_logo.svg/1200px-Arrow_Electronics_logo.svg.png"
st.sidebar.image(logo_url, width=200)

st.sidebar.title("🚀 Quick Access")
st.sidebar.markdown("---")
st.sidebar.link_button("🔗 Open Salesforce", "https://arrow.my.salesforce.com")
st.sidebar.link_button("🔗 Open MyConnect", "https://myconnect.arrow.com")
st.sidebar.link_button("🔗 Open Oracle EBS", "https://ebs.arrow.com")
st.sidebar.markdown("---")

# 3. App Header
st.title("🛡️ Sales Ops Knowledge Hub")
st.subheader("Internal SOPs & Process Navigation")

# 4. Data Loading
try:
    df = pd.read_csv("sop_data.csv", sep=None, engine='python')
    df.columns = df.columns.str.strip()
    df = df.replace(np.nan, '', regex=True)

    # 5. Search Logic (Session State allows buttons to work)
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""

    col1, col2 = st.columns([2, 1])
    with col1:
        # The key="main_search" helps sync the box with the buttons
        search = st.text_input("🔍 Search for a process", value=st.session_state.search_query, key="main_search")

    # 6. Popular Topics Buttons
    st.write("### 💡 Popular Topics")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("📑 Refund Approvals"):
        st.session_state.search_query = "Refund"
        st.rerun()
    if c2.button("🌍 Venlo Shipping"):
        st.session_state.search_query = "Venlo"
        st.rerun()
    if c3.button("👤 Customer Setup"):
        st.session_state.search_query = "Address"
        st.rerun()
    if c4.button("🔄 Clear Search"):
        st.session_state.search_query = ""
        st.rerun()

    st.markdown("---")

    # 7. Display Results
    # We use search if user types, or session_state if they click a button
    query = search if search != st.session_state.search_query else st.session_state.search_query

    if query:
        # This is where the Syntax Error was - now on its own line!
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        filtered = df[mask]
        
        if not filtered.empty:
            for _, row in filtered.iterrows():
                with st.expander(f"📂 {row.get('System', 'System')} - {row.get('Process', 'Process')}"):
                    st.write("### 📝 Instructions")
                    st.info(row.get('Instructions', 'No instructions found'))
                    
                    img_url = row.get('Screenshot_URL', '')
                    if str(img_url).startswith('http'):
                        try:
                            st.image(img_url, use_container_width=True)
                        except:
                            st.warning("🖼️ Image link in CSV is broken or not a direct link.")
        else:
            st.warning(f"No results found for '{query}'.")
    else:
        st.info("Select a popular topic above or type in the search bar to begin.")

except Exception as e:
    st.error(f"⚠️ Error: {e}")
