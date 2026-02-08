import streamlit as st
import pandas as pd

st.set_page_config(page_title="Arrow Sales Ops Hub", layout="wide", page_icon="🏹")

# Sidebar
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Arrow_Electronics_logo.svg/1200px-Arrow_Electronics_logo.svg.png", width=200)
st.sidebar.title("🚀 Quick Links")
st.sidebar.link_button("🔗 Salesforce", "https://arrow.my.salesforce.com")
st.sidebar.link_button("🔗 Unity", "https://unity.arrow.com")
st.sidebar.link_button("🔗 MyConnect", "https://myconnect.arrow.com")

st.title("🛡️ Sales Ops Knowledge Hub")
st.markdown("---")

# Data Load
df = pd.read_csv("sop_data.csv")

# Search Functionality
if 'search' not in st.session_state: st.session_state.search = ""
def set_search(term): st.session_state.search = term

st.write("### 💡 Quick Search Topics")
c1, c2, c3, c4 = st.columns(4)
if c1.button("📑 Order Status"): set_search("Unity")
if c2.button("🌍 Venlo / Logistics"): set_search("Venlo")
if c3.button("💰 Refunds"): set_search("Refund")
if c4.button("🔄 Reset"): set_search("")

query = st.text_input("🔍 Search for a process or system...", value=st.session_state.search)

if query:
    results = df[df.apply(lambda row: query.lower() in row.astype(str).str.lower().values, axis=1)]
    for _, row in results.iterrows():
        with st.expander(f"📂 {row['System']} - {row['Process']}"):
            st.info(row['Instructions'])
            if "http" in str(row['Screenshot_URL']):
                st.image(row['Screenshot_URL'])
else:
    st.write("Please select a topic or search above to see procedures.")        st.session_state.search_query = term
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
