import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Configuration & Professional Theme
st.set_page_config(page_title="Sales Ops Knowledge Hub", layout="wide", page_icon="🛡️")

# Custom CSS to make it look like a real portal
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stExpander { background-color: white !important; border-radius: 10px !important; box-shadow: 0px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar with Direct Links
st.sidebar.title("🚀 Quick Access")
st.sidebar.markdown("---")
st.sidebar.link_button("🔗 Open Salesforce", "https://arrow.my.salesforce.com")
st.sidebar.link_button("🔗 Open MyConnect", "https://myconnect.arrow.com")
st.sidebar.link_button("🔗 Open Oracle EBS", "https://ebs.arrow.com") # Update URL if different
st.sidebar.markdown("---")
st.sidebar.info("Support: For tool access, contact the IT Helpdesk.")

# 3. App Header
st.title("🛡️ Sales Ops Knowledge Hub")
st.subheader("Internal SOPs & Process Navigation")

# 4. Data Loading Logic
try:
    # sep=None detects if your CSV uses , or ; automatically
    df = pd.read_csv("sop_data.csv", sep=None, engine='python')
    df.columns = df.columns.str.strip()
    df = df.replace(np.nan, '', regex=True)

    # 5. Search Bar and Interface
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
    st.error(f"⚠️ Error: Please check your CSV file format. {e}")        st.info("Search for a task above.")

except Exception as e:
    st.error(f"Data Error: {e}")
