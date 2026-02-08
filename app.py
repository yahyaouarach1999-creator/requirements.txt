import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Arrow Sales Ops Hub", layout="wide", page_icon="🏹")

# 2. Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Arrow_Electronics_logo.svg/1200px-Arrow_Electronics_logo.svg.png", width=200)
st.sidebar.title("🚀 Quick Links")
st.sidebar.markdown("---")
st.sidebar.link_button("🔗 Salesforce", "https://arrow.my.salesforce.com")
st.sidebar.link_button("🔗 Unity", "https://unity.arrow.com")
st.sidebar.link_button("🔗 MyConnect", "https://myconnect.arrow.com")

# 3. App Header
st.title("🛡️ Sales Ops Knowledge Hub")
st.subheader("Digital Business & Customer Support SOPs")
st.markdown("---")

# 4. Data Loading
try:
    df = pd.read_csv("sop_data.csv")
    df = df.replace(np.nan, '', regex=True)

    # 5. Search Logic (Session State)
    if 'search' not in st.session_state:
        st.session_state.search = ""

    def set_search(term):
        st.session_state.search = term

    # 6. Popular Topics Buttons
    st.write("### 💡 Quick Search Topics")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("📑 Order Status (Unity)"):
        set_search("Unity")
    if c2.button("🌍 Venlo / Logistics"):
        set_search("Venlo")
    if c3.button("💰 Refunds"):
        set_search("Refund")
    if c4.button("🔄 Clear Search"):
        set_search("")

    # 7. Search Bar
    query = st.text_input("🔍 Search for a process or system...", value=st.session_state.search)

    # 8. Display Results
    if query:
        # Search across all columns
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        results = df[mask]
        
        if not results.empty:
            for _, row in results.iterrows():
                with st.expander(f"📂 {row['System']} - {row['Process']}"):
                    st.write("### 📝 Instructions")
                    st.info(row['Instructions'])
                    
                    img = str(row['Screenshot_URL'])
                    if img.startswith("http"):
                        st.image(img, use_container_width=True)
        else:
            st.warning(f"No results found for '{query}'.")
    else:
        st.write("Please select a topic or search above to see procedures.")

except Exception as e:
    st.error(f"⚠️ System Error: {e}")    if query:
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
