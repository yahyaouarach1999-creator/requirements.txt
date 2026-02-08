import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Arrow Sales Ops Portal", layout="wide", page_icon="🏹")

# 2. Sidebar with Logo and Links
# Updated Logo Link (More stable PNG version)
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

    # 5. Search Logic
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""

    def set_search(term):
        st.session_state.search_query = term

    col1, col2 = st.columns([2, 1])
    with col1:
        # We use a key here to link the widget to session state
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
    query = st.session_state.search_query if not search else search

    if query:
        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
        filtered = df[mask]
        
        if not filtered.empty:
            for _, row in filtered.iterrows():
                with st.expander(f"📂 {row.get('System', 'System')} - {row.get('Process', 'Process')}"):
                    st.write("### 📝 Instructions")
                    st.info(row.get('Instructions', 'No instructions found'))
                    
                    img_url = row.get('Screenshot_URL', '')
                    # Image safety check
                    if str(img_url).startswith('http'):
                        try:
                            st.image(img_url, use_container_width=True)
                        except:
                            st.error("Could not load image. Please check the URL in your CSV.")
        else:
            st.warning(f"No results found for '{query}'.")
    else:
        st.info("Select a popular topic above or type in the search bar to begin.")

except Exception as e:
    st.error(f"⚠️ Error: {e}")        mask = df.apply(lambda x: x.astype(str).str.contains(query, case=False)).any(axis=1)
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
    st.error(f"⚠️ Error: {e}")    # 5. Search Bar and Interface
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 What are you looking for?", placeholder="e.g. Refund, Address Change, Venlo...")

    # 6. Display Results
    if search:
        mask = df.apply(lambda x: x.astype(str).str.contains(search, case=False)).any(axis=1)
        filtered = df[mask]
        
        if not filtered.empty:
            for _, row in filtered.iterrows():
                with st.expander(f"📂 {row.get('System', 'System')} - {row.get('Process', 'Process')}"):
                    st.write("### 📝 Instructions")
                    st.write(row.get('Instructions', 'Steps coming soon.'))
                    
                    img_url = row.get('Screenshot_URL', '')
                    if str(img_url).startswith('http'):
                        st.markdown("---")
                        st.image(img_url, caption="Process Screenshot", use_container_width=True)
        else:
            st.warning("No results found. Try a different keyword.")
    else:
        # Homepage Dashboard view when not searching
        st.markdown("---")
        st.write("### 💡 Popular Topics")
        c1, c2, c3 = st.columns(3)
        c1.button("Refund Approvals", on_click=lambda: st.write("Search 'Refund' above"))
        c2.button("Venlo Shipping", on_click=lambda: st.write("Search 'Venlo' above"))
        c3.button("Customer Setup", on_click=lambda: st.write("Search 'Address' above"))
except Exception as e:
    st.error(f"⚠️ Error: Please check your CSV file format. {e}")
    st.info("Search for a task above.") # <--- This must be on a new line!
