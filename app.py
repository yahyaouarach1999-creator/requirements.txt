import streamlit as st
import pandas as pd

# 1. Page Setup
st.set_page_config(page_title="Sales Ops Portal", layout="wide")

# 2. Sidebar - IT Support
st.sidebar.title("🆘 Support")
st.sidebar.link_button("Go to MyConnect", "https://myconnect.arrow.com")

# 3. Load the Data
try:
    df = pd.read_csv("sop_data.csv")
    
    st.title("🛡️ Sales Ops Knowledge Hub")
    st.write("Search for Salesforce, Oracle EBS, or SWB tasks below.")

    # 4. Search Bar
    search = st.text_input("🔍 Search (e.g., Refund, Address Change, Venlo)")

    if search:
        filtered = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
        for _, row in filtered.iterrows():
            with st.expander(f"📖 {row['Process']}"):
                st.write(f"**System:** {row['System']}")
                st.write(f"**Instructions:** {row['Instructions']}")
                if 'Screenshot_URL' in row and pd.notnull(row['Screenshot_URL']):
                    st.image(row['Screenshot_URL'])
    else:
        st.info("Type a process name above to see the steps.")

except Exception as e:
    st.error("Wait! Make sure your sop_data.csv file has the right columns: System, Process, Instructions")
